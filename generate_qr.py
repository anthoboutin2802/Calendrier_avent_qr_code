# generate_qr.py
import csv
import qrcode
from urllib.parse import urlencode, quote_plus
from pathlib import Path

# CONFIG
GITHUB_BASE = "https://anthoboutin2802.github.io/Calendrier_avent_qr_code/"  # <-- Remplace ici
MAPPING_CSV = "mapping.csv"   # format expliqué ci-dessous
OUT_DIR = Path("output_qr")
OUT_DIR.mkdir(exist_ok=True)

def gh_url(params: dict):
    return GITHUB_BASE + "?" + urlencode(params, quote_via=quote_plus)

def make_qr(url, outpath):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(outpath)

with open(MAPPING_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Expected CSV headers: day,img_id,audio_id
# example row: 01,1A2b3C...,0Z9y8X...
links_out = []
for r in rows:
    day = r['day'].strip()
    img_id = r['img_id'].strip()
    audio_id = r['audio_id'].strip()
    params = {
        'img': img_id,
        'audio': audio_id,
        'day': day
    }
    url = gh_url(params)
    filename = f"qr_day_{day.replace(' ','_')}.png"
    outpath = OUT_DIR / filename
    make_qr(url, outpath)
    links_out.append({'day': day, 'url': url, 'qr_file': str(outpath)})

# write links.csv
with open(OUT_DIR / "links.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['day','url','qr_file'])
    w.writeheader()
    for item in links_out:
        w.writerow(item)

print("QR codes et links.csv générés dans", OUT_DIR.resolve())
