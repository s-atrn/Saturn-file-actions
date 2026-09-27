# 🪐 Saturn File Actions

A lightweight, modern Windows context menu tool.

---

## ✨ Features

* **Instant Context Menu Integration:** Right-click any file on Windows 10/11 to access the converter instantly.
* **Universal Conversion Support:**
  * **Images:** PNG, JPG, JPEG, WEBP, BMP, ICO, GIF
  * **Documents & Data:** PDF, DOCX, TXT, JSON, CSV, XLSX, HTML, MD
  * **Media (Audio/Video):** MP4, MKV, AVI, MP3, WAV, FLAC
  * **Archives:** ZIP, TAR.GZ, 7Z
  * **Custom Formats:** Type any custom extension manually.

---

## Remove it from the right click menu

`reg delete "HKEY_CLASSES_ROOT\*\shell\SaturnFileConverter" /f`

---

## 🛠️ Project Structure

```text
Saturn-file-actions/
├── saturn_actions.py       # Core conversion logic and Tkinter UI
├── setup.py                # Automated installation & registry configuration script
├── saturn.ico              # Custom ringed Saturn icon
├── installer.iss           # Inno Setup script for building the standalone installer
└── README.md               # Project documentation
