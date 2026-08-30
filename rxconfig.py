import reflex as rx
import os

config = rx.Config(
    app_name="wyn",
    cors_allowed_origins=["*"],
    db_url=os.environ.get(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_a4uAMZfocK0I@ep-withered-feather-b3n0w2vd.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    ),
    # Google cloud integration
    gdrive_folder_id=os.environ.get("GDRIVE_FOLDER_ID", "1ea_ErSBmjNO2_c_ockLfpKm9KKR2YWQq"),
    gsheets_url=os.environ.get("GSHEETS_URL", "https://docs.google.com/spreadsheets/d/18_uLK-ppsJ8umVAlZVPBYHhxYEZnkebWJXdn5KkRDP0/edit"),
)