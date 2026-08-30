# Google Cloud Integration Setup Guide for WYN

This guide explains how to set up a Google Service Account to sync images from a Google Drive folder and bucket list ideas from a Google Sheet.

---

## 🛠️ Step 1: Create a Google Cloud Project & Enable APIs

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `WYN-Web-App`).
3. Enable the following APIs:
   * **Google Drive API**: Go to "APIs & Services" > "Library", search for "Google Drive API", and click **Enable**.
   * **Google Sheets API**: Search for "Google Sheets API" in the library and click **Enable**.

---

## 🔑 Step 2: Create a Service Account & Download Credentials

1. In the Google Cloud Console, go to **IAM & Admin** > **Service Accounts**.
2. Click **Create Service Account** at the top.
3. Fill in the details:
   * **Service account name**: e.g., `wyn-api-service`
   * Click **Create and Continue**, then click **Done**.
4. You will see your new Service Account in the list. Copy its email address (it looks like `wyn-api-service@project-name.iam.gserviceaccount.com`).
5. Click on the Service Account name to open its settings.
6. Go to the **Keys** tab.
7. Click **Add Key** > **Create new key**.
8. Select **JSON** as the key type and click **Create**.
9. A JSON file will be downloaded to your computer.
10. Rename this file to `gdrive_credentials.json` and move it to the root of your project directory (`f:\Jason\Documents\Python Projects\WYN\gdrive_credentials.json`).

> [!WARNING]
> Do NOT commit `gdrive_credentials.json` to GitHub! It is already added to `.gitignore` to keep your credentials safe.

---

## 📂 Step 3: Set up Google Drive (Past Dates Timeline)

1. Open your Google Drive.
2. Create a new folder (e.g., `WYN Date Memories`).
3. Right-click the folder and choose **Share**.
4. Paste the **Service Account email address** you copied in Step 2.
5. Make sure the role is set to **Viewer** (or **Editor**), and click **Share**.
6. Look at the URL of the folder in your browser. It looks like:
   `https://drive.google.com/drive/folders/YOUR_FOLDER_ID_HERE`
7. Copy the `YOUR_FOLDER_ID_HERE` string. This is your **Google Drive Folder ID**. You will set this in `rxconfig.py` (or pass it to the state).

### Filename Naming Convention:
Name the image files in this folder using this exact format to let the app parse them automatically:
`YYYY-MM-DD_Title_Description.jpg`

* **Example:** `2026-02-14_Valentine Dinner_A romantic night at our favorite French bistro downtown.jpg`
* **How it displays:**
  * **Date:** February 14, 2026
  * **Title:** Valentine Dinner
  * **Description:** A romantic night at our favorite French bistro downtown.
  * **Image:** Displays the photo itself.

---

## 📊 Step 4: Set up Google Sheets (Future Date Bucket List)

1. Open [Google Sheets](https://sheets.google.com) and create a blank spreadsheet.
2. In the first row, create the following headers exactly (case-insensitive, spaces are ignored):
   * Column A: `Idea`
   * Column B: `Category`
   * Column C: `Notes`
   * Column D: `Completed`
3. Add a few rows of date ideas. Under the `Completed` column, write `TRUE` or `FALSE` (or check/uncheck checkboxes).
4. Share the sheet with the **Service Account email address** as a **Viewer** or **Editor**.
5. Copy the URL of the spreadsheet from your browser. It looks like:
   `https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID_HERE/edit...`
6. You will put this URL or the Spreadsheet ID in the app config to load the spreadsheet rows dynamically.

---

## ⚙️ Step 5: Configure the Reflex App

Open `rxconfig.py` and specify your credentials:

```python
import reflex as rx

config = rx.Config(
    app_name="wyn",
    # Add your Google configuration here:
    gdrive_folder_id="YOUR_FOLDER_ID_HERE",
    gsheets_url="https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID_HERE/edit",
)
```

*(Note: The app will run in **Mock Mode** using beautiful sample memories if no credentials file is found!)*
