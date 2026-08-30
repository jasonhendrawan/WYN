import os
import json
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
import rxconfig

logger = logging.getLogger("WYN_DB")

DB_URL = getattr(
    rxconfig.config,
    "db_url",
    "postgresql://neondb_owner:npg_a4uAMZfocK0I@ep-withered-feather-b3n0w2vd.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
)

def get_connection():
    """Create a new connection to PostgreSQL with a 3s connect timeout."""
    return psycopg2.connect(DB_URL, connect_timeout=3)

def init_db():
    """Create necessary database tables if they do not exist."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # 1. Trips table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS trips (
                        id VARCHAR(128) PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        date VARCHAR(32) NOT NULL,
                        description TEXT DEFAULT '',
                        image_path TEXT DEFAULT '',
                        lat DOUBLE PRECISION,
                        lng DOUBLE PRECISION,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 2. Trip Media table (thumbnails and streaming URLs)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS trip_media (
                        id VARCHAR(128) PRIMARY KEY,
                        trip_id VARCHAR(128) REFERENCES trips(id) ON DELETE CASCADE,
                        url TEXT NOT NULL,
                        thumb_url TEXT NOT NULL,
                        media_type VARCHAR(16) DEFAULT 'image',
                        date_taken VARCHAR(64) DEFAULT '',
                        is_favorite BOOLEAN DEFAULT FALSE,
                        sort_order INT DEFAULT 0
                    );
                    CREATE INDEX IF NOT EXISTS idx_trip_media_trip_id ON trip_media(trip_id);
                """)

                # 3. Bucket List table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS bucket_items (
                        id SERIAL PRIMARY KEY,
                        idea VARCHAR(255) NOT NULL,
                        category VARCHAR(64) DEFAULT 'General',
                        notes TEXT DEFAULT '',
                        completed BOOLEAN DEFAULT FALSE,
                        target_date VARCHAR(32) DEFAULT '',
                        trip_id VARCHAR(128) DEFAULT ''
                    );
                """)

                # 4. Favorites table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS favorites (
                        url TEXT PRIMARY KEY,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 5. App Settings table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS app_settings (
                        key VARCHAR(64) PRIMARY KEY,
                        value TEXT
                    );
                """)

                conn.commit()
                logger.info("Neon PostgreSQL tables verified & initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize PostgreSQL tables: {e}")

def get_all_trips() -> list[dict]:
    """Fetch all trips with their media items from PostgreSQL, sorted by date."""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, title, date, description, image_path, lat, lng
                    FROM trips
                    ORDER BY date ASC;
                """)
                trips_rows = cur.fetchall()

                if not trips_rows:
                    return []

                cur.execute("""
                    SELECT id, trip_id, url, thumb_url, media_type AS type, date_taken, is_favorite, sort_order
                    FROM trip_media
                    ORDER BY sort_order ASC, date_taken ASC;
                """)
                media_rows = cur.fetchall()

                # Group media by trip_id
                media_by_trip = {}
                for m in media_rows:
                    tid = m["trip_id"]
                    if tid not in media_by_trip:
                        media_by_trip[tid] = []
                    media_by_trip[tid].append({
                        "url": m["url"],
                        "thumb_url": m["thumb_url"] or m["url"],
                        "type": m["type"],
                        "date_taken": m["date_taken"] or "",
                    })

                trips = []
                for t in trips_rows:
                    trip_id = t["id"]
                    loc = None
                    if t["lat"] is not None and t["lng"] is not None:
                        loc = [t["lat"], t["lng"]]
                    trips.append({
                        "id": trip_id,
                        "title": t["title"],
                        "date": t["date"],
                        "description": t["description"] or "",
                        "image_path": t["image_path"] or "",
                        "images": media_by_trip.get(trip_id, []),
                        "location": loc,
                    })
                return trips
    except Exception as e:
        logger.error(f"Error fetching trips from PostgreSQL: {e}")
        return []

def get_all_bucket_items() -> list[dict]:
    """Fetch all bucket list items from PostgreSQL."""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT idea, category, notes, completed, target_date AS date, trip_id
                    FROM bucket_items
                    ORDER BY completed ASC, id ASC;
                """)
                rows = cur.fetchall()
                return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"Error fetching bucket list from PostgreSQL: {e}")
        return []

def get_favorites() -> list[str]:
    """Fetch list of favorited media URLs."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT url FROM favorites;")
                rows = cur.fetchall()
                return [r[0] for r in rows]
    except Exception as e:
        logger.error(f"Error fetching favorites from PostgreSQL: {e}")
        return []

def save_trips_to_db(past_dates: list[dict]):
    """Bulk upsert trips and media items into PostgreSQL."""
    if not past_dates:
        return
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for trip in past_dates:
                    trip_id = str(trip.get("id", ""))
                    if not trip_id:
                        continue
                    title = trip.get("title", "")
                    date_val = trip.get("date", "")
                    desc = trip.get("description", "")
                    img_path = trip.get("image_path", "")
                    loc = trip.get("location")
                    lat, lng = (None, None)
                    if loc and isinstance(loc, (list, tuple)) and len(loc) == 2:
                        lat, lng = float(loc[0]), float(loc[1])

                    cur.execute("""
                        INSERT INTO trips (id, title, date, description, image_path, lat, lng, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        ON CONFLICT (id) DO UPDATE SET
                            title = EXCLUDED.title,
                            date = EXCLUDED.date,
                            description = EXCLUDED.description,
                            image_path = EXCLUDED.image_path,
                            lat = EXCLUDED.lat,
                            lng = EXCLUDED.lng,
                            updated_at = CURRENT_TIMESTAMP;
                    """, (trip_id, title, date_val, desc, img_path, lat, lng))

                    # Insert/Update media items
                    images = trip.get("images", [])
                    for idx, img in enumerate(images):
                        if isinstance(img, str):
                            img_url = img
                            thumb = img
                            m_type = "image"
                            dt = ""
                        elif isinstance(img, dict):
                            img_url = img.get("url", "")
                            thumb = img.get("thumb_url", img_url)
                            m_type = img.get("type", "image")
                            dt = img.get("date_taken", "")
                        else:
                            continue

                        media_id = f"{trip_id}_{idx}"
                        cur.execute("""
                            INSERT INTO trip_media (id, trip_id, url, thumb_url, media_type, date_taken, sort_order)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (id) DO UPDATE SET
                                url = EXCLUDED.url,
                                thumb_url = EXCLUDED.thumb_url,
                                media_type = EXCLUDED.media_type,
                                date_taken = EXCLUDED.date_taken,
                                sort_order = EXCLUDED.sort_order;
                        """, (media_id, trip_id, img_url, thumb, m_type, dt, idx))

                conn.commit()
                logger.info(f"Saved {len(past_dates)} trips to Neon PostgreSQL.")
    except Exception as e:
        logger.error(f"Error saving trips to PostgreSQL: {e}")

def save_bucket_to_db(bucket_list: list[dict]):
    """Save bucket list items to PostgreSQL."""
    if not bucket_list:
        return
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM bucket_items;")
                for item in bucket_list:
                    cur.execute("""
                        INSERT INTO bucket_items (idea, category, notes, completed, target_date, trip_id)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (
                        item.get("idea", ""),
                        item.get("category", "General"),
                        item.get("notes", ""),
                        bool(item.get("completed", False)),
                        item.get("date", ""),
                        item.get("trip_id", "")
                    ))
                conn.commit()
                logger.info(f"Saved {len(bucket_list)} bucket items to Neon PostgreSQL.")
    except Exception as e:
        logger.error(f"Error saving bucket list to PostgreSQL: {e}")

def update_trip_date_in_db(trip_id: str, new_date: str):
    """Update trip date in PostgreSQL."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE trips
                    SET date = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s;
                """, (new_date, trip_id))
                conn.commit()
    except Exception as e:
        logger.error(f"Error updating trip date in PostgreSQL: {e}")

def toggle_favorite_in_db(url: str) -> list[str]:
    """Toggle a favorite URL in PostgreSQL and return updated list."""
    clean_url = url.lstrip("/")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT url FROM favorites WHERE url = %s;", (clean_url,))
                if cur.fetchone():
                    cur.execute("DELETE FROM favorites WHERE url = %s;", (clean_url,))
                else:
                    cur.execute("INSERT INTO favorites (url) VALUES (%s) ON CONFLICT DO NOTHING;", (clean_url,))
                conn.commit()
        return get_favorites()
    except Exception as e:
        logger.error(f"Error toggling favorite in PostgreSQL: {e}")
        return []
