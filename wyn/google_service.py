import os
import re
import json
import datetime
import io
import logging
import gspread

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WYN_GoogleService")

# Mock data to use if Google credentials are not set up yet
MOCK_DATA = {
    "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "past_dates": [
        {
            "id": "mock_1",
            "date": "2026-02-14",
            "title": "Valentine's Day Dinner",
            "description": "We went to the cozy French bistro downtown. The lavender dessert was amazing and we spent three hours talking about everything and nothing.",
            "image_path": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&auto=format&fit=crop&q=60",
            "images": [
                {"url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&auto=format&fit=crop&q=60", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800&auto=format&fit=crop&q=60", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1543007630-9710e4a00a20?w=800&auto=format&fit=crop&q=60", "type": "image"}
            ]
        },
        {
            "id": "mock_2",
            "date": "2026-03-21",
            "title": "Stargazing at the Lake",
            "description": "Drove up to the lake with hot chocolate, blankets, and a telescope. The sky was perfectly clear and we saw a shooting star!",
            "image_path": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=800&auto=format&fit=crop&q=60",
            "images": [
                {"url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=800&auto=format&fit=crop&q=60", "type": "image"},
                {"url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4", "type": "video"},
                {"url": "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=800&auto=format&fit=crop&q=60", "type": "image"}
            ]
        },
        {
            "id": "mock_3",
            "date": "2026-04-12",
            "title": "Art Museum & Coffee",
            "description": "Explored the contemporary art exhibition. You wore your favorite purple sweater and got a lavender latte at the museum cafe.",
            "image_path": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&auto=format&fit=crop&q=60",
            "images": [
                {"url": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&auto=format&fit=crop&q=60", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1482160549825-59d1b23cb208?w=800&auto=format&fit=crop&q=60", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1445116572660-236099ec97a0?w=800&auto=format&fit=crop&q=60", "type": "image"}
            ]
        },
        {
            "id": "mock_4",
            "date": "2026-05-30",
            "title": "First Picnic of Spring",
            "description": "Set up a blanket under the giant cherry blossom tree. We brought strawberries, cheese, crackers, and played cards all afternoon.",
            "image_path": "https://images.unsplash.com/photo-1526218626217-dc65a29bb444?w=800&auto=format&fit=crop&q=60",
            "images": [
                {"url": "https://images.unsplash.com/photo-1526218626217-dc65a29bb444?w=800&auto=format&fit=crop&q=60", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&auto=format&fit=crop&q=60", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop&q=60", "type": "image"}
            ]
        }
    ],
    "bucket_list": [
        {
            "idea": "Hot Air Balloon Ride",
            "category": "Adventure",
            "notes": "Catch the sunrise and take lots of photos.",
            "completed": False
        },
        {
            "idea": "Couples Cooking Class",
            "category": "Food",
            "notes": "Learn to make fresh pasta from scratch.",
            "completed": False
        },
        {
            "idea": "Weekend Cabin Getaway",
            "category": "Adventure",
            "notes": "Find a cozy cabin in the woods with a fireplace.",
            "completed": False
        },
        {
            "idea": "Paint and Sip Night",
            "category": "Chill",
            "notes": "Paint portraits of each other (even if they look funny).",
            "completed": False
        },
        {
            "idea": "Karaoke Duet Night",
            "category": "Chill",
            "notes": "Sing our hearts out to classic 80s love songs.",
            "completed": True
        },
        {
            "idea": "Try the Spicy Ramen Challenge",
            "category": "Food",
            "notes": "See who can handle Level 5 spicy ramen at Ichiraku.",
            "completed": True
        }
    ]
}


def ensure_thumbnail(local_path, cache_dir, img_id, ext):
    """
    Ensure a thumbnail exists for the given image path.
    Returns the web path to the thumbnail.
    """
    ext_lower = ext.lower()
    
    # We only generate thumbnails for images
    if ext_lower not in [".jpg", ".jpeg", ".png", ".webp"]:
        return f"gdrive_cache/{img_id}{ext}"
        
    thumb_filename = f"{img_id}_thumb{ext_lower}"
    local_thumb_path = os.path.join(cache_dir, thumb_filename)
    web_thumb_path = f"gdrive_cache/{thumb_filename}"
    
    if os.path.exists(local_thumb_path):
        return web_thumb_path
        
    try:
        from PIL import Image, ImageOps
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            resample_filter = Image.ANTIALIAS
            
        with Image.open(local_path) as img:
            # Auto-orient the image based on EXIF data
            img = ImageOps.exif_transpose(img)
            # Resize image to fit within 1000x1000 box, maintaining aspect ratio
            img.thumbnail((1000, 1000), resample_filter)
            # Save thumbnail with optimization
            img.save(local_thumb_path, optimize=True, quality=85)
            logger.info(f"Generated thumbnail for {img_id}")
            return web_thumb_path
    except Exception as e:
        logger.error(f"Failed to generate thumbnail for {local_path}: {e}")
        return f"gdrive_cache/{img_id}{ext}"


def ensure_thumb_url_in_data(data_dict):
    """Ensure every image dict has a 'thumb_url' key, defaulting to 'url'."""
    for trip in data_dict.get("past_dates", []):
        # Ensure cover image_path is set
        if "image_path" not in trip:
            trip["image_path"] = ""
        # Process images list
        for img in trip.get("images", []):
            if "thumb_url" not in img:
                img["thumb_url"] = img.get("url", "")
    return data_dict


def parse_filename(filename):
    """
    Parse date, title, and description from filename.
    Format: YYYY-MM-DD_Title_Description.ext
    Returns a dict with date, title, description, or default values if parse fails.
    """
    # Remove file extension
    base_name, _ = os.path.splitext(filename)
    
    # Try parsing YYYY-MM-DD_Title_Description
    pattern = r"^(\d{4}-\d{2}-\d{2})_(.*?)_(.*)$"
    match = re.match(pattern, base_name)
    
    if match:
        return {
            "date": match.group(1),
            "title": match.group(2).replace("_", " "),
            "description": match.group(3).replace("_", " ")
        }
        
    # Try parsing YYYY-MM-DD_Title
    pattern_short = r"^(\d{4}-\d{2}-\d{2})_(.*)$"
    match_short = re.match(pattern_short, base_name)
    if match_short:
        return {
            "date": match_short.group(1),
            "title": match_short.group(2).replace("_", " "),
            "description": ""
        }
        
    # Fallback: Use filename as title, current date as date
    return {
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "title": base_name.replace("_", " "),
        "description": ""
    }


def get_exif_date(file_path):
    """
    Try to read the EXIF date taken metadata from the image file.
    DateTimeOriginal is tag 36867.
    DateTimeDigitized is tag 36868.
    DateTime is tag 306.
    Returns YYYY-MM-DD or None if not found/error.
    """
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag in ("DateTimeOriginal", "DateTimeDigitized", "DateTime"):
                        # Format: "YYYY:MM:DD HH:MM:SS" -> "YYYY-MM-DD"
                        date_part = value.split(" ")[0].replace(":", "-")
                        # Basic validation: YYYY-MM-DD is 10 chars
                        if len(date_part) == 10 and date_part[4] == '-' and date_part[7] == '-':
                            return date_part
    except Exception as e:
        logger.debug(f"Failed to read EXIF date for {file_path}: {e}")
    return None

def get_exif_datetime(file_path):
    """
    Try to read the EXIF date taken metadata from the image file.
    Returns full datetime string 'YYYY-MM-DD HH:MM:SS' or None if not found/error.
    """
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                # Prefer DateTimeOriginal > DateTimeDigitized > DateTime
                for preferred_tag in ("DateTimeOriginal", "DateTimeDigitized", "DateTime"):
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == preferred_tag and isinstance(value, str):
                            # Format: "YYYY:MM:DD HH:MM:SS" -> "YYYY-MM-DD HH:MM:SS"
                            parts = value.split(" ", 1)
                            date_part = parts[0].replace(":", "-")
                            time_part = parts[1] if len(parts) > 1 else "00:00:00"
                            if len(date_part) == 10 and date_part[4] == '-' and date_part[7] == '-':
                                return f"{date_part} {time_part}"
    except Exception as e:
        logger.debug(f"Failed to read EXIF datetime for {file_path}: {e}")
    return None


KNOWN_LOCATIONS = {
    "thamrin": [-6.1953, 106.8231],
    "upfinity": [-6.1953, 106.8231],
    "aquarium": [-6.1754, 106.7900],
    "neo soho": [-6.1754, 106.7900],
    "blok m": [-6.2443, 106.7981],
    "ashta": [-6.2241, 106.8097],
    "gukbap": [-6.2443, 106.7981],
    "bekasi": [-6.2383, 106.9756],
    "teras winiy": [-6.2600, 106.8100],
    "church": [-6.2000, 106.8200],
    "moana": [-6.1754, 106.8272],
    "jakarta": [-6.2088, 106.8456],
    "lake": [-6.3000, 106.8000],
    "bistro": [-6.2200, 106.8000],
    "museum": [-6.1750, 106.8200],
    "picnic": [-6.2100, 106.8300],
}

def _convert_gps_to_degrees(value):
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return None

def get_exif_gps(file_path):
    """Extract lat/lon from image EXIF if available."""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
        with Image.open(file_path) as img:
            exif = img._getexif()
            if not exif:
                return None
            gps_info = {}
            for key, val in exif.items():
                name = TAGS.get(key, key)
                if name == "GPSInfo":
                    for t in val:
                        sub_tag = GPSTAGS.get(t, t)
                        gps_info[sub_tag] = val[t]
            if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                lat = _convert_gps_to_degrees(gps_info["GPSLatitude"])
                lon = _convert_gps_to_degrees(gps_info["GPSLongitude"])
                if lat is not None and lon is not None:
                    if gps_info.get("GPSLatitudeRef", "N") != "N":
                        lat = -lat
                    if gps_info.get("GPSLongitudeRef", "E") != "E":
                        lon = -lon
                    return [round(lat, 5), round(lon, 5)]
    except Exception as e:
        logger.debug(f"Could not extract GPS from {file_path}: {e}")
    return None

def match_location_from_title(title):
    """Match trip title to known coordinates."""
    if not title:
        return [-6.2088, 106.8456]
    title_lower = title.lower()
    for key, coords in KNOWN_LOCATIONS.items():
        if key in title_lower:
            return coords
    return [-6.2088, 106.8456]

def get_data_filepath():
    """Get the path to the cached data JSON file."""
    # Place it inside assets/gdrive_cache/data.json
    cache_dir = os.path.join("assets", "gdrive_cache")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, "data.json")

_GLOBAL_DATA_CACHE = None

def normalize_past_dates_list(dates: list[dict]) -> list[dict]:
    """Normalize trip image paths and metadata for direct state consumption."""
    normalized = []
    for trip in dates:
        t = dict(trip)
        path = t.get("image_path", "")
        if path and not path.startswith("http"):
            t["image_path"] = path.lstrip("/")
        t["is_external"] = path.startswith("http") if path else False
        
        is_video = False
        if path:
            is_video = path.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))
        t["is_cover_video"] = is_video
        
        raw_imgs = t.get("images", [])
        norm_imgs = []
        for img in raw_imgs:
            if isinstance(img, str):
                is_vid = img.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))
                url = img.lstrip("/")
                norm_imgs.append({
                    "url": url,
                    "thumb_url": url,
                    "type": "video" if is_vid else "image",
                    "is_external": url.startswith("http"),
                    "date_taken": "",
                })
            elif isinstance(img, dict):
                url = img.get("url", "").lstrip("/")
                thumb = img.get("thumb_url", url).lstrip("/")
                mtype = img.get("type", "image")
                norm_imgs.append({
                    "url": url,
                    "thumb_url": thumb,
                    "type": mtype,
                    "is_external": url.startswith("http"),
                    "date_taken": img.get("date_taken", ""),
                })
        t["images"] = norm_imgs
        t["photos_count"] = len(norm_imgs)
        normalized.append(t)
    return normalized

def save_cached_data(data_dict):
    """Save data to in-memory cache, PostgreSQL, and cache directories."""
    global _GLOBAL_DATA_CACHE
    sync_result = ensure_thumb_url_in_data(auto_check_completed(data_dict))
    _GLOBAL_DATA_CACHE = sync_result
    
    # Save to PostgreSQL
    try:
        from . import db
        db.init_db()
        db.save_trips_to_db(sync_result.get("past_dates", []))
        db.save_bucket_to_db(sync_result.get("bucket_list", []))
    except Exception as db_err:
        logger.warning(f"Failed to persist to PostgreSQL: {db_err}")

    paths = [
        get_data_filepath(),
        os.path.join("uploaded_files", "gdrive_cache", "data.json"),
    ]
    for p in paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(sync_result, f, indent=4)
        except Exception as e:
            logger.error(f"Error writing cache to {p}: {e}")
    return sync_result

def update_trip_date_in_cache(trip_id, new_date):
    """Update date of a specific trip in cached data and re-sort."""
    try:
        from . import db
        db.update_trip_date_in_db(trip_id, new_date)
    except Exception as db_err:
        logger.warning(f"Failed to update trip date in PostgreSQL: {db_err}")

    data = load_cached_data()
    for trip in data.get("past_dates", []):
        if trip.get("id") == trip_id:
            trip["date"] = new_date
            break
    if "past_dates" in data:
        data["past_dates"].sort(key=lambda x: x.get("date", ""))
    return save_cached_data(data)

def save_favorites_in_cache(favorites_list):
    """Save favorited image URLs to cache and PostgreSQL."""
    data = load_cached_data()
    data["favorites"] = favorites_list
    return save_cached_data(data)


def auto_check_completed(data_dict):
    """
    Automatically build the bucket list showing:
    - Checked items: trip names of the past trips that have been done (from Drive folders).
    - Unchecked items: plans from the Google Sheet that have not yet been matched to a folder.
    """
    past_dates = data_dict.get("past_dates", [])
    sheet_bucket_list = data_dict.get("bucket_list", [])
    
    # Extract completed trip titles (lowercase for comparison)
    completed_trips_lower = {t.get("title", "").lower().strip(): t for t in past_dates if t.get("title")}
    
    final_bucket_list = []
    
    # 1. Add all completed trips as checked items in the bucket list
    for trip in past_dates:
        title = trip.get("title", "").strip()
        trip_id = trip.get("id", "")
        if title:
            # Check if this trip exists in sheet to borrow its category/notes
            cat = "Adventure"
            notes = ""
            for item in sheet_bucket_list:
                if item.get("idea", "").lower().strip() == title.lower().strip():
                    cat = item.get("category", "Adventure")
                    notes = item.get("notes", "")
                    break
                    
            final_bucket_list.append({
                "idea": title,
                "category": cat,
                "notes": notes,
                "completed": True,
                "date": trip.get("date", ""),
                "trip_id": trip_id
            })
            
    # 2. Add sheet plans that have not been done yet
    for item in sheet_bucket_list:
        idea = item.get("idea", "")
        idea_lower = idea.lower().strip()
        if idea_lower not in completed_trips_lower:
            final_bucket_list.append({
                "idea": idea,
                "category": item.get("category", "General"),
                "notes": item.get("notes", ""),
                "completed": False,
                "date": item.get("date", ""),
                "trip_id": ""
            })
            
    data_dict["bucket_list"] = final_bucket_list
    return data_dict

def load_cached_data():
    """Load data from in-memory cache, PostgreSQL, or local JSON cache instantly."""
    global _GLOBAL_DATA_CACHE
    if _GLOBAL_DATA_CACHE is not None:
        return _GLOBAL_DATA_CACHE

    # 1. Try local JSON cache first for lightning-fast 0.001s local startup
    filepath = get_data_filepath()
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "past_dates" in data:
                    data["past_dates"].sort(key=lambda x: x.get("date", ""))
                _GLOBAL_DATA_CACHE = ensure_thumb_url_in_data(auto_check_completed(data))
                return _GLOBAL_DATA_CACHE
        except Exception as e:
            logger.error(f"Error loading cached data: {e}")

    # 2. Try PostgreSQL
    try:
        from . import db
        trips = db.get_all_trips()
        if trips:
            bucket = db.get_all_bucket_items()
            favs = db.get_favorites()
            _GLOBAL_DATA_CACHE = {
                "past_dates": trips,
                "bucket_list": bucket,
                "favorites": favs,
                "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return _GLOBAL_DATA_CACHE
    except Exception as db_err:
        logger.debug(f"PostgreSQL fetch fallback to mock: {db_err}")
            
    # 3. Fallback to mock data
    try:
        processed_mock = ensure_thumb_url_in_data(auto_check_completed(dict(MOCK_DATA)))
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(processed_mock, f, indent=4)
        _GLOBAL_DATA_CACHE = processed_mock
        return _GLOBAL_DATA_CACHE
    except Exception as e:
        logger.error(f"Error writing initial mock cache: {e}")
        
    _GLOBAL_DATA_CACHE = ensure_thumb_url_in_data(auto_check_completed(dict(MOCK_DATA)))
    return _GLOBAL_DATA_CACHE

def sync_google_services(credentials_path="gdrive_credentials.json", folder_id=None, spreadsheet_url=None):
    """
    Sync images from Google Drive folder and bucket list from Google Sheets.
    Saves metadata to assets/gdrive_cache/data.json and downloads images locally.
    
    If credentials_path does not exist, it will write/ensure the mock data is cached
    and return that.
    """
    if not os.path.exists(credentials_path):
        logger.warning(f"Credentials file '{credentials_path}' not found. Using fallback mock data.")
        return load_cached_data()
        
    try:
        # Import google modules here to prevent startup errors if libraries are missing
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload
        
        # Scopes required
        scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        # Load credentials
        creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        
        # 1. Sync Past Dates from Google Drive
        past_dates = []
        cache_dir = "uploaded_files/gdrive_cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
            
        if folder_id:
            drive_service = build('drive', 'v3', credentials=creds)
            
            # Query for subfolders first
            subfolder_query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            subfolder_results = drive_service.files().list(
                q=subfolder_query,
                pageSize=100,
                fields="files(id, name, description, createdTime)"
            ).execute()
            
            subfolders = subfolder_results.get('files', [])
            
            if subfolders:
                logger.info(f"Found {len(subfolders)} subfolders in Google Drive root folder.")
                for folder in subfolders:
                    subfolder_id = folder['id']
                    subfolder_name = folder['name']
                    subfolder_desc = folder.get('description', '')
                    
                    # Query for files inside this subfolder
                    image_query = f"'{subfolder_id}' in parents and trashed = false"
                    image_results = drive_service.files().list(
                        q=image_query,
                        pageSize=50,
                        fields="files(id, name, mimeType, createdTime, size)"
                    ).execute()
                    
                    media_files = [f for f in image_results.get('files', []) if f.get('mimeType', '').startswith('image/') or f.get('mimeType', '').startswith('video/')]
                    
                    if not media_files:
                        logger.warning(f"No media files found in subfolder '{subfolder_name}'. Skipping.")
                        continue
                    
                    # Sort media files by createdTime (earliest to latest)
                    media_files.sort(key=lambda x: x.get('createdTime', ''))
                    
                    # Find cover image/video (filename starts with 'cover' case-insensitive)
                    cover_img = None
                    for img in media_files:
                        name_lower = img['name'].lower()
                        name_without_ext, _ = os.path.splitext(name_lower)
                        if name_without_ext == "cover" or name_without_ext.startswith("cover_"):
                            cover_img = img
                            break
                            
                    if not cover_img:
                        # Fallback to the first image in the folder
                        only_images = [img for img in media_files if img.get('mimeType', '').startswith('image/')]
                        if only_images:
                            cover_img = only_images[0]
                        else:
                            # If no images, fallback to the first video
                            cover_img = media_files[0] if media_files else None
                        
                    cover_id = cover_img['id'] if cover_img else None
                    created_time_str = cover_img.get('createdTime', '') if cover_img else (media_files[0].get('createdTime', '') if media_files else '')
                    
                    # Download all images/videos in this folder and cache them
                    images_web_paths = []
                    cover_web_path = ""
                    
                    for item in media_files:
                        img_id = item['id']
                        img_name = item['name']
                        mime_type = item.get('mimeType', '')
                        media_type = "video" if mime_type.startswith('video/') else "image"
                        file_size = int(item.get('size', 0)) if item.get('size') else 0
                        
                        _, ext = os.path.splitext(img_name)
                        if not ext:
                            ext = ".mp4" if media_type == "video" else ".jpg"
                        local_filename = f"{img_id}{ext}"
                        local_path = os.path.join(cache_dir, local_filename)
                        
                        # For very large videos (> 50MB), stream directly from Drive CDN
                        if media_type == "video" and file_size > 50 * 1024 * 1024 and not os.path.exists(local_path):
                            logger.info(f"Using direct Drive stream for large video ({file_size / (1024*1024):.1f} MB): {img_name}")
                            img_web_path = f"https://lh3.googleusercontent.com/d/{img_id}"
                            img_thumb_web_path = f"https://drive.google.com/thumbnail?id={img_id}&sz=w800"
                        else:
                            img_web_path = f"gdrive_cache/{local_filename}"
                            if not os.path.exists(local_path):
                                logger.info(f"Downloading media from Drive: {img_name} -> {local_path}")
                                try:
                                    request = drive_service.files().get_media(fileId=img_id)
                                    fh = io.BytesIO()
                                    downloader = MediaIoBaseDownload(fh, request)
                                    done = False
                                    while done is False:
                                        status, done = downloader.next_chunk()
                                    fh.seek(0)
                                    with open(local_path, "wb") as f:
                                        f.write(fh.read())
                                except Exception as download_err:
                                    logger.error(f"Failed downloading {img_name}: {download_err}")
                                    continue
                            else:
                                logger.debug(f"Media already cached locally: {img_name}")
                            
                            if media_type == "image":
                                img_thumb_web_path = ensure_thumbnail(local_path, cache_dir, img_id, ext)
                            else:
                                img_thumb_web_path = img_web_path
                        
                        # Get per-image EXIF datetime
                        img_datetime = ""
                        if media_type == "image":
                            img_datetime = get_exif_datetime(local_path) or ""
                        if not img_datetime:
                            # Fallback to Drive createdTime for this file
                            file_created = item.get('createdTime', '')
                            if file_created:
                                img_datetime = file_created.replace("T", " ").split(".")[0]
                            
                        images_web_paths.append({
                            "url": img_web_path,
                            "thumb_url": img_thumb_web_path,
                            "type": media_type,
                            "date_taken": img_datetime
                        })
                        if cover_id and img_id == cover_id:
                            cover_web_path = img_thumb_web_path
                    
                    # Sort images by their individual date_taken (earliest first)
                    images_web_paths.sort(key=lambda x: x.get("date_taken", ""))
                    
                    # Get earliest EXIF date from per-image dates for the trip-level date
                    exif_dates = [m["date_taken"].split(" ")[0] for m in images_web_paths if m.get("date_taken")]
                    if exif_dates:
                        date_taken = min(exif_dates)
                    else:
                        if created_time_str:
                            date_taken = created_time_str.split("T")[0]
                        else:
                            date_taken = datetime.date.today().strftime("%Y-%m-%d")
                            
                    fallback_cover = ""
                    for media in images_web_paths:
                        if media["type"] == "image":
                            fallback_cover = media["thumb_url"]
                            break
                    # Extract GPS from photos or fallback to title geocoding
                    trip_location = None
                    for m in images_web_paths:
                        loc_p = os.path.join(cache_dir, os.path.basename(m.get("url", "")))
                        if os.path.exists(loc_p) and m.get("type") == "image":
                            gps = get_exif_gps(loc_p)
                            if gps:
                                trip_location = gps
                                break
                    if not trip_location:
                        trip_location = match_location_from_title(subfolder_name)

                    past_dates.append({
                        "id": subfolder_id,
                        "date": date_taken,
                        "title": subfolder_name,
                        "description": subfolder_desc,
                        "image_path": cover_web_path or fallback_cover,
                        "images": images_web_paths,
                        "location": trip_location,
                    })
            else:
                logger.info("No subfolders found. Falling back to direct root image sync.")
                # Root image sync fallback
                query = f"'{folder_id}' in parents and trashed = false"
                results = drive_service.files().list(
                    q=query,
                    pageSize=100,
                    fields="files(id, name, mimeType, createdTime, size)"
                ).execute()
                
                items = results.get('files', [])
                media_files = [f for f in items if f.get('mimeType', '').startswith('image/') or f.get('mimeType', '').startswith('video/')]
                
                # Sort media files by createdTime (earliest to latest)
                media_files.sort(key=lambda x: x.get('createdTime', ''))
                
                for item in media_files:
                    mime_type = item.get('mimeType', '')
                    file_id = item['id']
                    filename = item['name']
                    created_time_str = item.get('createdTime', '')
                    media_type = "video" if mime_type.startswith('video/') else "image"
                    file_size = int(item.get('size', 0)) if item.get('size') else 0
                    
                    parsed = parse_filename(filename)
                    _, ext = os.path.splitext(filename)
                    if not ext:
                        ext = ".mp4" if media_type == "video" else ".jpg"
                    local_filename = f"{file_id}{ext}"
                    local_path = os.path.join(cache_dir, local_filename)
                    
                    if media_type == "video" and file_size > 50 * 1024 * 1024 and not os.path.exists(local_path):
                        logger.info(f"Using direct Drive stream for large video ({file_size / (1024*1024):.1f} MB): {filename}")
                        image_web_path = f"https://lh3.googleusercontent.com/d/{file_id}"
                        img_thumb_web_path = f"https://drive.google.com/thumbnail?id={file_id}&sz=w800"
                    else:
                        image_web_path = f"gdrive_cache/{local_filename}"
                        if not os.path.exists(local_path):
                            logger.info(f"Downloading media from Drive: {filename} -> {local_path}")
                            try:
                                request = drive_service.files().get_media(fileId=file_id)
                                fh = io.BytesIO()
                                downloader = MediaIoBaseDownload(fh, request)
                                done = False
                                while done is False:
                                    status, done = downloader.next_chunk()
                                fh.seek(0)
                                with open(local_path, "wb") as f:
                                    f.write(fh.read())
                            except Exception as download_err:
                                logger.error(f"Failed downloading {filename}: {download_err}")
                                continue
                        else:
                            logger.debug(f"Media already cached locally: {filename}")
                        
                        if media_type == "image":
                            img_thumb_web_path = ensure_thumbnail(local_path, cache_dir, file_id, ext)
                        else:
                            img_thumb_web_path = image_web_path
                    
                    # Try reading EXIF datetime if it's an image
                    img_datetime = ""
                    date_taken = None
                    if media_type == "image" and os.path.exists(local_path):
                        img_datetime = get_exif_datetime(local_path) or ""
                        date_taken = get_exif_date(local_path)
                    if not img_datetime and created_time_str:
                        img_datetime = created_time_str.replace("T", " ").split(".")[0]
                    if not date_taken:
                        date_taken = parsed["date"] or (created_time_str.split("T")[0] if created_time_str else datetime.date.today().strftime("%Y-%m-%d"))
                    
                    root_loc = match_location_from_title(parsed["title"])
                    past_dates.append({
                        "id": file_id,
                        "date": date_taken,
                        "title": parsed["title"],
                        "description": parsed["description"],
                        "image_path": img_thumb_web_path,
                        "images": [{"url": image_web_path, "thumb_url": img_thumb_web_path, "type": media_type, "date_taken": img_datetime}],
                        "location": root_loc,
                    })
                    
            # Sort past dates chronologically (earliest to latest)
            past_dates.sort(key=lambda x: x["date"])
        else:
            logger.warning("No Google Drive Folder ID provided. Skipping Drive sync.")
            # Keep existing cached past dates or mock data
            current_cache = load_cached_data()
            past_dates = current_cache.get("past_dates", MOCK_DATA["past_dates"])
            
        # 2. Sync Bucket List from Google Sheets
        bucket_list = []
        if spreadsheet_url:
            gc = gspread.authorize(creds)
            # Open spreadsheet (by URL or Key)
            sh = None
            if "docs.google.com/spreadsheets" in spreadsheet_url:
                sh = gc.open_by_url(spreadsheet_url)
            else:
                sh = gc.open_by_key(spreadsheet_url)
                
            # Read first worksheet
            worksheet = sh.get_worksheet(0)
            rows = worksheet.get_all_records() # Reads headers automatically
            
            # Format row data to match expected bucket_list structure
            # Expecting columns: Idea, Category, Notes, Completed
            for row in rows:
                # Normalize keys to lowercase for flexible parsing
                normalized_row = {k.lower().strip(): v for k, v in row.items()}
                
                idea = normalized_row.get("idea", "")
                if not idea:
                    # Skip empty rows
                    continue
                    
                category = normalized_row.get("category", "General")
                notes = normalized_row.get("notes", "")
                completed_raw = normalized_row.get("completed", False)
                
                # Handle cell value conversions for boolean
                if isinstance(completed_raw, str):
                    completed = completed_raw.strip().upper() in ["TRUE", "YES", "1", "CHECKED", "X"]
                else:
                    completed = bool(completed_raw)
                    
                date = str(normalized_row.get("date", "")).strip()
                if not date:
                    date = str(normalized_row.get("target date", "")).strip()
                if not date:
                    date = str(normalized_row.get("target_date", "")).strip()

                bucket_list.append({
                    "idea": str(idea),
                    "category": str(category),
                    "notes": str(notes),
                    "completed": completed,
                    "date": date
                })
        else:
            logger.warning("No Google Sheets Spreadsheet URL/Key provided. Skipping Sheets sync.")
            # Keep existing cached bucket list or mock data
            current_cache = load_cached_data()
            bucket_list = current_cache.get("bucket_list", MOCK_DATA["bucket_list"])
            
        # Save compiled data to local JSON cache
        sync_result = {
            "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "past_dates": past_dates,
            "bucket_list": bucket_list
        }
        
        # Auto check completed plans based on folder names
        sync_result = auto_check_completed(sync_result)
        sync_result = ensure_thumb_url_in_data(sync_result)
        
        filepath = get_data_filepath()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(sync_result, f, indent=4)
            
        logger.info("Successfully synchronized with Google Cloud Services.")
        return sync_result
        
    except Exception as e:
        logger.error(f"Error during Google Cloud Sync: {e}", exc_info=True)
        # On error, return cached data
        return load_cached_data()

def save_bucket_list_to_sheets(bucket_list, credentials_path="gdrive_credentials.json", spreadsheet_url=None):
    """
    Save the bucket list back to the Google Sheet.
    Pushes the latest checklist ideas, categories, notes, completed status, and target dates.
    """
    if not spreadsheet_url:
        logger.warning("No Google Sheets Spreadsheet URL provided. Cannot save to sheet.")
        return False
        
    if not os.path.exists(credentials_path):
        logger.warning(f"Credentials file '{credentials_path}' not found. Cannot save to sheet.")
        return False
        
    try:
        from google.oauth2.service_account import Credentials
        
        # Scopes required
        scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        gc = gspread.authorize(creds)
        
        if "docs.google.com/spreadsheets" in spreadsheet_url:
            sh = gc.open_by_url(spreadsheet_url)
        else:
            sh = gc.open_by_key(spreadsheet_url)
            
        worksheet = sh.get_worksheet(0)
        
        # Default header names
        headers = ["Idea", "Category", "Notes", "Completed", "Date"]
        
        rows_to_write = []
        for item in bucket_list:
            # We save all items. For completed items, completed is True.
            rows_to_write.append([
                str(item.get("idea", "")),
                str(item.get("category", "General")),
                str(item.get("notes", "")),
                "TRUE" if item.get("completed", False) else "FALSE",
                str(item.get("date", ""))
            ])
            
        # Rewrite the entire sheet
        all_data = [headers] + rows_to_write
        worksheet.clear()
        worksheet.update(values=all_data, range_name='A1')
        logger.info(f"Successfully saved {len(rows_to_write)} plans to Google Sheets.")
        return True
    except Exception as e:
        logger.error(f"Error saving bucket list to Sheets: {e}", exc_info=True)
        return False
