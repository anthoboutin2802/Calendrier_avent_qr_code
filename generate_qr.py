import csv
import qrcode
from urllib.parse import urlencode, quote_plus
from pathlib import Path

# URL de ton site GitHub Pages (avec le / final)
GITHUB_BASE = "https://anthoboutin2802.github.io/Calendrier_avent_qr_code/"

MAPPING_CSV = "mapping.csv"
OUT_DIR = Path("output_qr")
OUT_DIR.mkdir(exist_ok=True)

def gh_url(params: dict) -> str:
    return GITHUB_BASE + "?" + urlencode(params, quote_via=quote_plus)

def make_qr(url: str, outpath: Path):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(outpath)

with open(MAPPING_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

links_out = []

# mapping.csv : day,img,audio
for r in rows:
    day = r['day'].strip()
    img_file = r['img'].strip()
    audio_file = r['audio'].strip()

    params = {
        "img": img_file,
        "audio": audio_file,
        "day": day
    }

    url = gh_url(params)
    filename = f"qr_day_{day.replace(' ', '_')}.png"
    outpath = OUT_DIR / filename
    make_qr(url, outpath)

    links_out.append({
        "day": day,
        "url": url,
        "qr_file": str(outpath)
    })

# fichier de log pratique
with open(OUT_DIR / "links.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=["day", "url", "qr_file"])
    w.writeheader()
    for item in links_out:
        w.writerow(item)

print("QR codes et links.csv générés dans", OUT_DIR.resolve())
