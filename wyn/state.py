import asyncio
import reflex as rx
from rxconfig import config
from . import google_service

MOCK_RICH_DATA = {
    "last_sync": "Mock Mode (Demo)",
    "past_dates": [
        {
            "id": "mock_1",
            "date": "2026-02-14",
            "title": "Valentine's Day Dinner",
            "description": "Cozy French bistro downtown. We sat by the window and laughed about our first date.",
            "image_path": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&auto=format&fit=crop&q=80",
            "images": [
                {"url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&auto=format&fit=crop&q=80", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800&auto=format&fit=crop&q=80", "type": "image"}
            ]
        },
        {
            "id": "mock_2",
            "date": "2026-03-21",
            "title": "Stargazing at the Lake",
            "description": "Brought blankets and a giant thermos of hot cocoa. Saw three shooting stars!",
            "image_path": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=800&auto=format&fit=crop&q=80",
            "images": [
                {"url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=800&auto=format&fit=crop&q=80", "type": "image"},
                {"url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4", "type": "video"}
            ]
        },
        {
            "id": "mock_3",
            "date": "2026-04-12",
            "title": "Museum of Modern Art",
            "description": "Explored the galleries and argued about whether a blank canvas is actually art.",
            "image_path": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&auto=format&fit=crop&q=80",
            "images": [
                {"url": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&auto=format&fit=crop&q=80", "type": "image"}
            ]
        },
        {
            "id": "mock_4",
            "date": "2026-05-02",
            "title": "Botanical Gardens Walk",
            "description": "Spring flowers were in full bloom. The orchid greenhouse was incredibly warm and beautiful.",
            "image_path": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&auto=format&fit=crop&q=80",
            "images": [
                {"url": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&auto=format&fit=crop&q=80", "type": "image"}
            ]
        },
        {
            "id": "mock_5",
            "date": "2026-05-30",
            "title": "Upfinity Thamrin Nine (FIRST DATE)",
            "description": "Breathtaking sunset view from Jakarta's highest deck. Took a ton of pictures together.",
            "image_path": "https://images.unsplash.com/photo-1526218626217-dc65a29bb444?w=800&auto=format&fit=crop&q=80",
            "images": [
                {"url": "https://images.unsplash.com/photo-1526218626217-dc65a29bb444?w=800&auto=format&fit=crop&q=80", "type": "image"}
            ]
        },
        {
            "id": "mock_6",
            "date": "2026-06-13",
            "title": "Jakarta Aquarium",
            "description": "Walked under the shark tunnel. We got soaked watching the penguin feeding show!",
            "image_path": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop&q=80",
            "images": [
                {"url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop&q=80", "type": "image"}
            ]
        },
        {
            "id": "mock_7",
            "date": "2026-06-20",
            "title": "Blok M",
            "description": "Neighbour -> berkelana -> Gukbap 111 -> blm tau WKWKWK",
            "image_path": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&auto=format&fit=crop&q=80",
            "images": [
                {"url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&auto=format&fit=crop&q=80", "type": "image"}
            ]
        },
        {
            "id": "mock_8",
            "date": "2026-07-04",
            "title": "Road Trip to Bandung",
            "description": "Escaped the Jakarta heat. Enjoyed hot tea in the cool mountain breeze at the tea plantation.",
            "image_path": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&auto=format&fit=crop&q=80",
            "images": [
                {"url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&auto=format&fit=crop&q=80", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&auto=format&fit=crop&q=80", "type": "image"}
            ]
        }
    ],
    "bucket_list": [
        {
            "idea": "Road Trip to Bandung",
            "category": "Adventure",
            "notes": "Escaped the Jakarta heat. Enjoyed hot tea in the cool mountain breeze at the tea plantation.",
            "completed": True,
            "trip_id": "mock_8"
        },
        {
            "idea": "Blok M",
            "category": "Food",
            "notes": "Neighbour -> berkelana -> Gukbap 111 -> blm tau WKWKWK",
            "completed": True,
            "trip_id": "mock_7"
        },
        {
            "idea": "Jakarta Aquarium",
            "category": "Chill",
            "notes": "Walked under the shark tunnel. We got soaked watching the penguin feeding show!",
            "completed": True,
            "trip_id": "mock_6"
        },
        {
            "idea": "Upfinity Thamrin Nine (FIRST DATE)",
            "category": "Adventure",
            "notes": "Breathtaking sunset view from Jakarta's highest deck. Took a ton of pictures together.",
            "completed": True,
            "trip_id": "mock_5"
        },
        {
            "idea": "Botanical Gardens Walk",
            "category": "Chill",
            "notes": "Spring flowers were in full bloom. The orchid greenhouse was incredibly warm and beautiful.",
            "completed": True,
            "trip_id": "mock_4"
        },
        {
            "idea": "Museum of Modern Art",
            "category": "Chill",
            "notes": "Explored the galleries and argued about whether a blank canvas is actually art.",
            "completed": True,
            "trip_id": "mock_3"
        },
        {
            "idea": "Stargazing at the Lake",
            "category": "Adventure",
            "notes": "Brought blankets and a giant thermos of hot cocoa. Saw three shooting stars!",
            "completed": True,
            "trip_id": "mock_2"
        },
        {
            "idea": "Valentine's Day Dinner",
            "category": "Food",
            "notes": "Cozy French bistro downtown. We sat by the window and laughed about our first date.",
            "completed": True,
            "trip_id": "mock_1"
        },
        {
            "idea": "Couples Cooking Class",
            "category": "Food",
            "notes": "Learn to make handmade pasta together.",
            "completed": False,
            "trip_id": ""
        },
        {
            "idea": "Hot Air Balloon Ride",
            "category": "Adventure",
            "notes": "Catch the sunrise over the valleys.",
            "completed": False,
            "trip_id": ""
        },
        {
            "idea": "Paint and Sip Night",
            "category": "Chill",
            "notes": "Paint funny portraits of each other.",
            "completed": False,
            "trip_id": ""
        },
        {
            "idea": "Cozy Cabin Weekend",
            "category": "Chill",
            "notes": "Rent a small cabin in the woods with a fireplace.",
            "completed": False,
            "trip_id": ""
        }
    ]
}

_INITIAL_CACHE = google_service.load_cached_data()

class State(rx.State):
    """The application state."""
    # Data states
    past_dates: list[dict] = []
    bucket_list: list[dict] = []
    favorites: list[str] = []
    last_sync: str = "Never"
    is_syncing: bool = False
    
    # Navigation and UI states
    active_tab: str = "timeline"
    filter_category: str = "All"
    selected_trip_id: str = ""
    theme_mode: str = "dark"
    
    # Lightbox states
    lightbox_url: str = ""
    lightbox_type: str = ""
    lightbox_is_external: bool = False
    
    # Trip Date Edit states
    edit_date_dialog_open: bool = False
    edit_date_trip_id: str = ""
    edit_date_trip_title: str = ""
    edit_date_value: str = ""
    
    # Edit/Add plan dialog states
    plan_dialog_open: bool = False
    plan_is_editing: bool = False
    form_plan_original_idea: str = ""
    form_plan_idea: str = ""
    form_plan_category: str = "General"
    form_plan_notes: str = ""
    form_plan_completed: bool = False
    form_plan_date: str = ""
    
    def load_data(self):
        """Instant in-memory load."""
        data = google_service.load_cached_data()
        self.past_dates = google_service.normalize_past_dates_list(data.get("past_dates", []))
        self.bucket_list = data.get("bucket_list", [])
        self.favorites = data.get("favorites", [])
        self.last_sync = data.get("last_sync", "Never")
        
    def _normalize_past_dates(self, dates: list[dict]) -> list[dict]:
        normalized = []
        for trip in dates:
            t = dict(trip)
            path = t.get("image_path", "")
            if path and not path.startswith("http"):
                t["image_path"] = path.lstrip("/")
            t["is_external"] = path.startswith("http") if path else False
            
            # Check if cover is a video
            is_video = False
            if path:
                is_video = path.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))
            t["is_cover_video"] = is_video
            
            raw_imgs = t.get("images", [])
            norm_imgs = []
            for img in raw_imgs:
                if isinstance(img, str):
                    is_video = img.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))
                    url = img.lstrip("/")
                    norm_imgs.append({
                        "url": url,
                        "thumb_url": url,
                        "type": "video" if is_video else "image",
                        "is_external": url.startswith("http"),
                        "date_taken": ""
                    })
                elif isinstance(img, dict):
                    media = dict(img)
                    url = media.get("url", "")
                    if url and not url.startswith("http"):
                        media["url"] = url.lstrip("/")
                    media["is_external"] = url.startswith("http") if url else False
                    if "thumb_url" not in media or not media["thumb_url"]:
                        media["thumb_url"] = media["url"]
                    elif not media["thumb_url"].startswith("http"):
                        media["thumb_url"] = media["thumb_url"].lstrip("/")
                    norm_imgs.append(media)
            t["images"] = norm_imgs
            normalized.append(t)
        return normalized

    async def sync_data(self):
        """Sync data from Google Drive and Sheets asynchronously."""
        self.is_syncing = True
        yield  # Yield to update the UI with the loading spinner immediately
        
        # Access config variables
        folder_id = getattr(config, "gdrive_folder_id", "")
        sheets_url = getattr(config, "gsheets_url", "")
        
        # Run the sync in background thread so WebSocket never times out
        data = await asyncio.to_thread(
            google_service.sync_google_services,
            credentials_path="gdrive_credentials.json",
            folder_id=folder_id,
            spreadsheet_url=sheets_url
        )
        
        self.past_dates = self._normalize_past_dates(data.get("past_dates", []))
        self.bucket_list = data.get("bucket_list", [])
        self.favorites = data.get("favorites", [])
        self.last_sync = data.get("last_sync", "Never")
        self.is_syncing = False
        
        # Show toast message based on mode
        has_credentials = google_service.os.path.exists("gdrive_credentials.json")
        if has_credentials:
            if folder_id or sheets_url:
                yield rx.toast("Successfully synced with Google Cloud!")
            else:
                yield rx.toast("Service credentials found, but folder/sheet configuration is empty.")
        else:
            yield rx.toast("No credentials file found. Running in Mock Mode with sample data.")

    def toggle_favorite(self, url: str):
        """Toggle favorite heart on an image."""
        clean_url = url.lstrip("/")
        if clean_url in self.favorites or url in self.favorites:
            self.favorites = [u for u in self.favorites if u != clean_url and u != url]
        else:
            self.favorites = self.favorites + [clean_url]
        google_service.save_favorites_in_cache(self.favorites)

    def open_edit_date(self, trip_id: str):
        """Open date editor modal for a specific trip."""
        self.edit_date_trip_id = str(trip_id)
        for trip in self.past_dates:
            if str(trip.get("id")) == str(trip_id):
                self.edit_date_trip_title = trip.get("title", "")
                self.edit_date_value = trip.get("date", "")
                break
        self.edit_date_dialog_open = True

    def close_edit_date(self):
        """Close date editor modal."""
        self.edit_date_dialog_open = False

    def set_edit_date_value(self, val: str):
        """Set new date value in editor."""
        self.edit_date_value = val

    def save_trip_date(self):
        """Save updated trip date and re-sort timeline."""
        if not self.edit_date_trip_id or not self.edit_date_value:
            self.edit_date_dialog_open = False
            return
        updated_data = google_service.update_trip_date_in_cache(self.edit_date_trip_id, self.edit_date_value)
        self.past_dates = self._normalize_past_dates(updated_data.get("past_dates", []))
        self.edit_date_dialog_open = False
        return rx.toast(f"Date updated for '{self.edit_date_trip_title}'!")

    def set_tab(self, tab: str):
        self.active_tab = tab

    def toggle_theme(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        
    def click_bucket_item(self, item: dict):
        """Click handler for plans item: switches tab to timeline and opens gallery."""
        if item.get("completed") and item.get("trip_id"):
            self.active_tab = "timeline"
            self.selected_trip_id = item.get("trip_id")
        
    def set_filter(self, category: str):
        self.filter_category = category

    def select_trip(self, trip_id: str):
        self.selected_trip_id = trip_id

    def close_gallery(self):
        self.selected_trip_id = ""

    def open_lightbox(self, url: str, media_type: str):
        self.lightbox_url = url
        self.lightbox_type = media_type
        self.lightbox_is_external = url.startswith("http") if url else False

    def close_lightbox(self):
        self.lightbox_url = ""
        self.lightbox_type = ""

    def close_plan_dialog(self):
        self.plan_dialog_open = False

    def toggle_plan_dialog(self, is_open: bool):
        self.plan_dialog_open = is_open

    def set_form_plan_idea(self, value: str):
        self.form_plan_idea = value

    def set_form_plan_category(self, value: str):
        self.form_plan_category = value

    def set_form_plan_notes(self, value: str):
        self.form_plan_notes = value

    def set_form_plan_completed(self, value: bool):
        self.form_plan_completed = value

    def set_form_plan_date(self, value: str):
        self.form_plan_date = value

    def open_add_plan(self):
        self.plan_dialog_open = True
        self.plan_is_editing = False
        self.form_plan_original_idea = ""
        self.form_plan_idea = ""
        self.form_plan_category = "General"
        self.form_plan_notes = ""
        self.form_plan_completed = False
        self.form_plan_date = ""

    def open_edit_plan(self, item: dict):
        self.plan_dialog_open = True
        self.plan_is_editing = True
        self.form_plan_original_idea = item.get("idea", "")
        self.form_plan_idea = item.get("idea", "")
        self.form_plan_category = item.get("category", "General")
        self.form_plan_notes = item.get("notes", "")
        self.form_plan_completed = bool(item.get("completed", False))
        self.form_plan_date = item.get("date", "")

    def save_plan(self):
        if not self.form_plan_idea.strip():
            return rx.toast("Plan title cannot be empty!")
            
        new_item = {
            "idea": self.form_plan_idea.strip(),
            "category": self.form_plan_category.strip(),
            "notes": self.form_plan_notes.strip(),
            "completed": self.form_plan_completed,
            "date": self.form_plan_date.strip(),
            "trip_id": ""
        }

        # Check if we are editing an existing item or adding a new one
        if self.plan_is_editing:
            # Update the existing item
            for i, item in enumerate(self.bucket_list):
                if item.get("idea", "") == self.form_plan_original_idea:
                    # Retain trip_id if completed status didn't change
                    trip_id = item.get("trip_id", "") if self.form_plan_completed else ""
                    new_item["trip_id"] = trip_id
                    self.bucket_list[i] = new_item
                    break
        else:
            self.bucket_list.append(new_item)

        self._persist_bucket_list()
        self.plan_dialog_open = False
        return rx.toast("Plan saved successfully!")

    def delete_plan(self):
        if self.plan_is_editing:
            self.bucket_list = [item for item in self.bucket_list if item.get("idea", "") != self.form_plan_original_idea]
            self._persist_bucket_list()
            self.plan_dialog_open = False
            return rx.toast("Plan deleted successfully!")

    def _persist_bucket_list(self):
        import json
        import os
        filepath = google_service.get_data_filepath()
        data = {}
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        
        clean_bucket = []
        for item in self.bucket_list:
            clean_bucket.append({
                "idea": str(item.get("idea", "")),
                "category": str(item.get("category", "General")),
                "notes": str(item.get("notes", "")),
                "completed": bool(item.get("completed", False)),
                "date": str(item.get("date", "")),
                "trip_id": str(item.get("trip_id", ""))
            })
            
        data["bucket_list"] = clean_bucket
        data["last_sync"] = self.last_sync
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error persisting bucket list to JSON: {e}")
            
        # Push changes to Google Sheets
        sheets_url = getattr(config, "gsheets_url", "")
        if sheets_url:
            try:
                google_service.save_bucket_list_to_sheets(
                    clean_bucket,
                    credentials_path="gdrive_credentials.json",
                    spreadsheet_url=sheets_url
                )
            except Exception as e:
                print(f"Error syncing bucket list to Sheets: {e}")

    @rx.var
    def completed_list(self) -> list[dict]:
        """Get all completed items."""
        return [item for item in self.bucket_list if item.get("completed", False)]

    @rx.var
    def plans_list(self) -> list[dict]:
        """Get all active plans."""
        return [item for item in self.bucket_list if not item.get("completed", False)]

    @rx.var
    def filtered_completed_list(self) -> list[dict]:
        """Filtered completed list based on active category filter."""
        items = self.completed_list
        if self.filter_category == "All":
            return items
        return [item for item in items if item.get("category") == self.filter_category]

    @rx.var
    def filtered_plans_list(self) -> list[dict]:
        """Filtered active plans list based on active category filter."""
        items = self.plans_list
        if self.filter_category == "All":
            return items
        return [item for item in items if item.get("category") == self.filter_category]

    @rx.var
    def bucket_categories(self) -> list[str]:
        """Get all unique categories present in the active list based on active tab."""
        items = self.completed_list if self.active_tab == "completed" else self.plans_list
        categories = set(item.get("category", "General") for item in items)
        return ["All"] + sorted(list(categories))
        
    @rx.var
    def total_completed(self) -> int:
        return sum(1 for item in self.bucket_list if item.get("completed", False))

    @rx.var
    def total_wishlist(self) -> int:
        return sum(1 for item in self.bucket_list if not item.get("completed", False))

    @rx.var
    def total_past(self) -> int:
        return len(self.past_dates)

    @rx.var
    def selected_trip(self) -> dict:
        """Return the details of the selected trip for the gallery modal."""
        for trip in self.past_dates:
            if str(trip.get("id")) == self.selected_trip_id:
                return trip
        return {}

    @rx.var
    def selected_trip_images(self) -> list[dict]:
        """Return the images list of the selected trip, normalized to dicts."""
        for trip in self.past_dates:
            if str(trip.get("id")) == self.selected_trip_id:
                raw_imgs = trip.get("images", [])
                normalized = []
                for img in raw_imgs:
                    if isinstance(img, str):
                        # Infer type from extension
                        is_video = img.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))
                        normalized.append({
                            "url": img,
                            "type": "video" if is_video else "image",
                            "is_external": img.startswith("http"),
                            "date_taken": ""
                        })
                    elif isinstance(img, dict):
                        media = dict(img)
                        if "is_external" not in media:
                            url = media.get("url", "")
                            media["is_external"] = url.startswith("http") if url else False
                        if "date_taken" not in media:
                            media["date_taken"] = ""
                        normalized.append(media)
                return normalized
        return []

    @rx.var
    def selected_trip_title(self) -> str:
        """Return the title of the selected trip."""
        for trip in self.past_dates:
            if str(trip.get("id")) == self.selected_trip_id:
                return trip.get("title", "")
        return ""

    @rx.var
    def selected_trip_desc(self) -> str:
        """Return the description of the selected trip."""
        for trip in self.past_dates:
            if str(trip.get("id")) == self.selected_trip_id:
                return trip.get("description", "")
        return ""

    @rx.var
    def selected_trip_date(self) -> str:
        """Return the date of the selected trip."""
        for trip in self.past_dates:
            if str(trip.get("id")) == self.selected_trip_id:
                return trip.get("date", "")
        return ""

    @rx.var
    def next_adventure_details(self) -> dict:
        """
        Find the closest future plan with a date.
        Returns a dict:
        {
            "has_adventure": bool,
            "title": str,
            "days_left": int,
            "date": str,
            "category": str
        }
        """
        import datetime
        today = datetime.date.today()
        
        future_plans = []
        for item in self.bucket_list:
            if item.get("completed", False):
                continue
            date_str = item.get("date", "")
            if date_str:
                try:
                    plan_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    if plan_date >= today:
                        days_left = (plan_date - today).days
                        future_plans.append({
                            "title": item.get("idea", ""),
                            "days_left": days_left,
                            "date": date_str,
                            "category": item.get("category", "General")
                        })
                except Exception:
                    pass
                    
        if not future_plans:
            return {
                "has_adventure": False,
                "title": "",
                "days_left": 0,
                "date": "",
                "category": ""
            }
            
        # Find the one with the smallest days_left
        future_plans.sort(key=lambda x: x["days_left"])
        closest = future_plans[0]
        return {
            "has_adventure": True,
            "title": closest["title"],
            "days_left": closest["days_left"],
            "date": closest["date"],
            "category": closest["category"]
        }

    @rx.var
    def days_together(self) -> int:
        """Calculate days together since August 2, 2026."""
        import datetime
        start = datetime.date(2026, 8, 2)
        today = datetime.date.today()
        diff = (today - start).days
        return max(1, diff + 1)

    @rx.var
    def highlight_images(self) -> list[dict]:
        """Return full item dicts for all favorited/hearted images across all trips."""
        highlights = []
        fav_set = set(self.favorites)
        for trip in self.past_dates:
            for img in trip.get("images", []):
                u = img.get("url", "")
                if u in fav_set or u.lstrip("/") in fav_set:
                    highlights.append({
                        "url": u,
                        "thumb_url": img.get("thumb_url", u),
                        "type": img.get("type", "image"),
                        "is_external": img.get("is_external", False),
                        "trip_title": trip.get("title", ""),
                        "trip_date": trip.get("date", ""),
                        "trip_id": trip.get("id", ""),
                        "date_taken": img.get("date_taken", ""),
                    })
        return highlights

    @rx.var
    def total_highlights(self) -> int:
        return len(self.highlight_images)

    @rx.var
    def map_locations_json(self) -> str:
        """JSON list of trip map markers with coordinates and info."""
        import json
        points = []
        for trip in self.past_dates:
            loc = trip.get("location")
            if loc and isinstance(loc, (list, tuple)) and len(loc) == 2:
                points.append({
                    "id": str(trip.get("id", "")),
                    "title": str(trip.get("title", "")),
                    "date": str(trip.get("date", "")),
                    "lat": float(loc[0]),
                    "lng": float(loc[1]),
                    "image": str(trip.get("image_path", "")),
                    "count": len(trip.get("images", [])),
                })
        return json.dumps(points)
