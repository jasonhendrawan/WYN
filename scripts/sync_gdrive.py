import os
import io
import json
import ssl
import time
import urllib.request
from datetime import datetime
from PIL import Image, ExifTags, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# 1. Configuration & Auth
ROOT_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "1ea_ErSBmjNO2_c_ockLfpKm9KKR2YWQq")
CREDS_FILE = os.environ.get("GDRIVE_CREDENTIALS_FILE", "gdrive_credentials.json")
CREDS_JSON_ENV = os.environ.get("GDRIVE_CREDENTIALS_JSON")

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

if CREDS_JSON_ENV:
    creds_info = json.loads(CREDS_JSON_ENV)
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
elif os.path.exists(CREDS_FILE):
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
else:
    print("Error: No Google Drive credentials found in file or environment.")
    exit(1)

drive_service = build('drive', 'v3', credentials=creds)

# Ensure cache directories exist
for d in ['dist/gdrive_cache', 'assets/gdrive_cache']:
    os.makedirs(d, exist_ok=True)

# 2. Load existing data
data_js_path = 'dist/data.js'
if os.path.exists(data_js_path):
    with open(data_js_path, 'r', encoding='utf-8') as f:
        js_str = f.read().replace('window.WYN_DATA = ', '').rstrip(';\n ')
        wyn_data = json.loads(js_str)
else:
    wyn_data = {"last_sync": "", "past_dates": [], "bucket_list": []}

existing_trips = {t['id']: t for t in wyn_data.get('past_dates', [])}

# 3. Helper Functions for EXIF GPS & Routing
def parse_gps_and_date(img_obj):
    try:
        exif = img_obj.getexif()
        if not exif:
            return None, None
        
        dt = ""
        for k, v in exif.items():
            tag = ExifTags.TAGS.get(k, k)
            if tag in ('DateTimeOriginal', 'DateTime', 'DateTimeDigitized'):
                dt = str(v)
                
        gps_ifd = exif.get_ifd(0x8825)
        if not gps_ifd:
            return dt, None
            
        lat_ref = gps_ifd.get(1, 'N')
        lat_raw = gps_ifd.get(2)
        lon_ref = gps_ifd.get(3, 'E')
        lon_raw = gps_ifd.get(4)
        
        if lat_raw and lon_raw:
            def to_deg(raw):
                d = float(raw[0])
                m = float(raw[1]) / 60.0
                s = float(raw[2]) / 3600.0
                return d + m + s
            lat = round(-to_deg(lat_raw) if lat_ref == 'S' else to_deg(lat_raw), 6)
            lon = round(-to_deg(lon_raw) if lon_ref == 'W' else to_deg(lon_raw), 6)
            return dt, [lat, lon]
        return dt, None
    except Exception:
        return None, None

def get_osrm_route(coords_list):
    if len(coords_list) < 2:
        return coords_list
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        coords_str = ";".join([f"{c[1]},{c[0]}" for c in coords_list])
        url = f"https://router.project-osrm.org/route/v1/driving/{coords_str}?overview=full&geometries=geojson"
        req = urllib.request.Request(url, headers={'User-Agent': 'WYN-App/1.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            raw_path = data['routes'][0]['geometry']['coordinates']
            return [[round(p[1], 6), round(p[0], 6)] for p in raw_path]
    except Exception as e:
        print(f"  Warning: OSRM route fetch failed ({e}). Using straight lines.")
        return coords_list

# 4. Fetch Subfolders from Google Drive
print(f"Scanning Google Drive root folder ({ROOT_FOLDER_ID})...")
subfolders_res = drive_service.files().list(
    q=f"'{ROOT_FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
    fields='files(id, name, createdTime)',
    pageSize=100
).execute()

subfolders = subfolders_res.get('files', [])
print(f"Found {len(subfolders)} subfolders in Google Drive.")

updated_trips = []

for folder in subfolders:
    fid = folder['id']
    fname = folder['name']
    
    # Skip non-trip utility folders or excluded photo albums like 'pap sayang aku'
    fname_clean = fname.lower().strip()
    if fname_clean in ['timeline', 'json', 'data', 'backup'] or 'pap sayang aku' in fname_clean:
        print(f"\nSkipping excluded folder: '{fname}' (ID: {fid})")
        continue
        
    print(f"\nProcessing Folder: '{fname}' (ID: {fid})")
    
    # List media files
    media_res = drive_service.files().list(
        q=f"'{fid}' in parents and trashed = false",
        fields='files(id, name, mimeType, size, createdTime, imageMediaMetadata)',
        pageSize=100
    ).execute()
    
    media_files = [f for f in media_res.get('files', []) if f.get('mimeType', '').startswith(('image/', 'video/'))]
    if not media_files:
        print(f"  No media in '{fname}', skipping.")
        continue
        
    media_files.sort(key=lambda x: x.get('createdTime', ''))
    
    # Check if folder already fully synced and cached
    is_cached = fid in existing_trips and len(existing_trips[fid].get('images', [])) == len(media_files)
    if is_cached:
        print(f"  Folder '{fname}' already up to date ({len(media_files)} items), skipping.")
        updated_trips.append(existing_trips[fid])
        continue

    images_data = []
    gps_stops = []
    earliest_date = "2026-08-01"
    cover_image_path = ""
    
    # Look for cover video or image
    cover_candidate = None
    for m in media_files:
        mname_lower = m['name'].lower().strip()
        if mname_lower == 'cover' or mname_lower.startswith(('cover.', 'cover_', 'cover ', 'thumb')) or 'cover' in mname_lower:
            cover_candidate = m
            break
            
    for m in media_files:
        mid = m['id']
        mname = m['name']
        mime = m.get('mimeType', '')
        is_video = mime.startswith('video/')
        ext = os.path.splitext(mname)[1].lower() or ('.mp4' if is_video else '.jpg')
        
        target_name = f"{mid}{ext if is_video else '.jpg'}"
        thumb_name = f"{mid}_thumb.jpg"
        
        target_path = os.path.join('dist/gdrive_cache', target_name)
        thumb_path = os.path.join('dist/gdrive_cache', thumb_name)
        
        dt_str = ""
        coords = None
        
        # Download and process if not cached locally
        if not os.path.exists(target_path):
            print(f"  Downloading & processing: {mname}...")
            req = drive_service.files().get_media(fileId=mid)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while not done:
                _, done = downloader.next_chunk()
            content = fh.getvalue()
            
            if is_video:
                if len(content) < 24 * 1024 * 1024:
                    with open(os.path.join('dist/gdrive_cache', target_name), 'wb') as vf:
                        vf.write(content)
                with open(os.path.join('assets/gdrive_cache', target_name), 'wb') as vf:
                    vf.write(content)
            else:
                try:
                    fh.seek(0)
                    img = Image.open(fh)
                    dt_str, coords = parse_gps_and_date(img)
                    img = ImageOps.exif_transpose(img)
                    
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
                    
                    for d in ['dist/gdrive_cache', 'assets/gdrive_cache']:
                        img.save(os.path.join(d, target_name), 'JPEG', quality=88)
                        t_img = img.copy()
                        t_img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                        t_img.save(os.path.join(d, thumb_name), 'JPEG', quality=82)
                except Exception as e:
                    print(f"    Image parse warning: {e}")
                    for d in ['dist/gdrive_cache', 'assets/gdrive_cache']:
                        with open(os.path.join(d, target_name), 'wb') as of:
                            of.write(content)
        else:
            # Already cached locally, read date from existing trip if available
            if fid in existing_trips:
                existing_img = next((i for i in existing_trips[fid].get('images', []) if mid in i.get('url', '')), None)
                if existing_img:
                    dt_str = existing_img.get('date_taken', '')
                    coords = existing_img.get('coords')
        
        if not dt_str:
            imm = m.get('imageMediaMetadata', {})
            dt_str = imm.get('time') or m.get('createdTime', '').replace('T', ' ')[:19]
            
        if dt_str:
            clean_date = dt_str.replace(':', '-').split(' ')[0]
            if clean_date.startswith('202') and (earliest_date == "2026-08-01" or clean_date < earliest_date):
                earliest_date = clean_date
                
        if coords:
            gps_stops.append((dt_str, coords))
            
        images_data.append({
            "url": f"gdrive_cache/{target_name}",
            "thumb_url": f"gdrive_cache/{thumb_name}" if not is_video else f"gdrive_cache/{target_name}",
            "type": "video" if is_video else "image",
            "date_taken": dt_str or "2026-08-01 12:00:00",
            "coords": coords
        })
        
    # Choose cover image/video
    if cover_candidate:
        ext = os.path.splitext(cover_candidate['name'])[1].lower() or ('.mp4' if cover_candidate.get('mimeType', '').startswith('video/') else '.jpg')
        if cover_candidate.get('mimeType', '').startswith('video/'):
            cover_image_path = f"gdrive_cache/{cover_candidate['id']}{ext}"
        else:
            cover_image_path = f"gdrive_cache/{cover_candidate['id']}_thumb.jpg"
    elif images_data:
        cover_image_path = images_data[0].get('thumb_url') or images_data[0].get('url')
        
    # Preserve or calculate location & stops
    if fid in existing_trips:
        trip_data = existing_trips[fid]
        trip_data['images'] = images_data
        trip_data['image_path'] = cover_image_path
        if not trip_data.get('date'):
            trip_data['date'] = earliest_date
    else:
        # Construct brand new trip
        center_loc = [-6.2088, 106.8456] # Default Jakarta
        timeline_stops = []
        path_coords = []
        
        if gps_stops:
            gps_stops.sort(key=lambda x: x[0])
            center_loc = gps_stops[0][1]
            for s_idx, (st_time, st_coord) in enumerate(gps_stops):
                time_only = st_time.split(' ')[1][:5] if ' ' in st_time else "12:00"
                timeline_stops.append({
                    "name": f"Stop #{s_idx+1}",
                    "time": time_only,
                    "coords": st_coord
                })
                path_coords.append(st_coord)
        else:
            timeline_stops.append({
                "name": fname,
                "time": "12:00",
                "coords": center_loc
            })
            path_coords.append(center_loc)
            
        osrm_path = get_osrm_route(path_coords) if len(path_coords) > 1 else path_coords
        
        trip_data = {
            "id": fid,
            "date": earliest_date,
            "title": fname.strip(),
            "description": f"Memories captured from {fname.strip()}! ✨",
            "image_path": cover_image_path,
            "images": images_data,
            "location": center_loc,
            "timeline_stops": timeline_stops,
            "timeline_path": osrm_path
        }
        
    updated_trips.append(trip_data)

# Sort all trips chronologically
updated_trips.sort(key=lambda x: x.get('date', ''))
wyn_data['past_dates'] = updated_trips
wyn_data['last_sync'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write to dist/data.js and dist/gdrive_cache/data.json
with open('dist/data.js', 'w', encoding='utf-8') as f:
    f.write("window.WYN_DATA = " + json.dumps(wyn_data, indent=2) + ";\n")

with open('dist/gdrive_cache/data.json', 'w', encoding='utf-8') as f:
    json.dump(wyn_data, f, indent=2)

print(f"\n[OK] Synchronization complete! Total trips: {len(updated_trips)}")
for idx, t in enumerate(updated_trips):
    print(f"  {idx+1}. {t['date']} - {t['title']} ({len(t.get('images', []))} items)")
