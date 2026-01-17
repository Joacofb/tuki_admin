import csv
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URL = "https://tubosilescapes.com.ar/productos.php?linea=4&marca=17"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    "Referer": URL,
}

r = requests.get(URL, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

items = []
for tr in soup.select("tr"):
    a = tr.select_one("td a.lightview[href]")
    if not a:
        continue

    href = a.get("href", "").strip()
    if not href.lower().endswith((".jpg", ".jpeg")):
        continue

    tds = tr.find_all("td")
    if len(tds) < 2:
        continue

    model = tds[1].get_text(" ", strip=True)
    img_url = urljoin(URL, href)

    items.append({"model": model, "image": img_url})

# Deduplicado por si hay repeticiones
seen = set()
unique = []
for it in items:
    key = (it["model"], it["image"])
    if key in seen:
        continue
    seen.add(key)
    unique.append(it)

with open("modelos_volkswagen.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["model", "image"])
    w.writeheader()
    w.writerows(unique)

print(f"OK: {len(unique)} filas -> tubosil_modelos.csv")
