"""
bundle_for_sharing.py
Pakuje aplikację do samodzielnego archiwum ZIP (przepisnik_rodzinny.zip),
które można zgrać na pendrive lub wysłać mailem/chmurą.
"""

import os
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_FILE = os.path.join(BASE_DIR, "przepisnik_rodzinny.zip")

print("📦 Przygotowywanie paczki do udostępnienia (przepisnik_rodzinny.zip)...")

items_to_zip = [
    "index.html",
    "app.js",
    "style.css",
    "manifest.json",
    "sw.js",
    "recipes.json",
    "icons",
    "images",
    "ksiazka_kucharska.pdf"
]

if os.path.exists(ZIP_FILE):
    os.remove(ZIP_FILE)

with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for item in items_to_zip:
        item_path = os.path.join(BASE_DIR, item)
        if not os.path.exists(item_path):
            continue
        if os.path.isdir(item_path):
            for root, dirs, files in os.walk(item_path):
                for f in files:
                    if f == ".DS_Store":
                        continue
                    fp = os.path.join(root, f)
                    arc = os.path.relpath(fp, BASE_DIR)
                    zipf.write(fp, arc)
        else:
            zipf.write(item_path, item)

zip_size_mb = os.path.getsize(ZIP_FILE) / (1024 * 1024)
print(f"🎉 Sukces! Utworzono plik: {ZIP_FILE} ({zip_size_mb:.1f} MB)")
