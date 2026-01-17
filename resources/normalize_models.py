import csv
import re
import sys
from urllib.parse import urljoin

URL_BASE = "https://tubosilescapes.com.ar/"

# Años: (62/65), (18->), (13 ->)
YEAR_RANGE_RE = re.compile(r"\(\s*(\d{2})\s*/\s*(\d{2})\s*\)\s*$")
YEAR_OPEN_RE  = re.compile(r"\(\s*(\d{2})\s*(?:-\s*>|->)\s*\)\s*$")

BODY_HINTS = (
    "SIN BAUL", "CON BAUL", "CAB. DOBLE", "CAB DOBLE",
)

ENGINE_HINTS = (
    "DIESEL", "DSL", "TD", "TURBO", "MPFI", "8V", "16V",
)

def yy_to_year4(yy: str) -> int:
    """
    Pivot simple: >= 60 => 19xx, si no => 20xx
    62->1962, 09->2009, 00->2000
    """
    y = int(yy)
    return 1900 + y if y >= 60 else 2000 + y

def clean_text(s: str) -> str:
    s = (s or "").strip()
    # comillas externas
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1].strip()
    # CSV escape "" -> "
    s = s.replace('""', '"')
    # espacios repetidos
    s = re.sub(r"\s+", " ", s).strip()
    return s

def fix_common_typos(s: str) -> str:
    # error visto en tu lista
    return s.replace("CHEVRLET", "CHEVROLET")

def extract_production(raw: str):
    """
    Devuelve (texto_sin_anios, production_str)
    production_str: '1995-2008' o '2018-ACTUALIDAD'
    """
    s = raw.strip()

    m_open = YEAR_OPEN_RE.search(s)
    if m_open:
        y_from = yy_to_year4(m_open.group(1))
        base = s[:m_open.start()].strip()
        return base, f"{y_from}-ACTUALIDAD"

    m_rng = YEAR_RANGE_RE.search(s)
    if m_rng:
        y_from = yy_to_year4(m_rng.group(1))
        y_to = yy_to_year4(m_rng.group(2))
        base = s[:m_rng.start()].strip()
        return base, f"{y_from}-{y_to}"

    return s, ""

def looks_like_engine(token: str) -> bool:
    t = token.upper()
    has_cc = bool(re.search(r"\d\.\d", t))  # 1.6, 2.0, 2.8
    has_hint = any(h in t for h in ENGINE_HINTS)
    return has_cc or has_hint

def looks_like_body(token: str) -> bool:
    t = token.upper()
    return any(h in t for h in BODY_HINTS)

def split_models_on_and(name_part: str):
    """
    Si aparece ' y ' o ' e ' en el NOMBRE base (sin motores),
    generamos múltiples modelos.
    Regla deliberadamente conservadora: sólo split si NO hay cilindradas.
    """
    s = name_part.strip()

    # Si hay motor/cilindrada en el nombre base, no splitteamos.
    if re.search(r"\d\.\d", s):
        return [s]

    # Normalizamos conectores con espacios
    for sep in (" y ", " e "):
        if sep in s.lower():
            # Hacemos split preservando el texto original con un split "case-insensitive"
            parts = re.split(rf"\s{sep.strip()}\s", s, flags=re.IGNORECASE)
            parts = [p.strip() for p in parts if p.strip()]
            if len(parts) >= 2:
                return parts

    return [s]

def normalize_row(raw_model: str, image: str, brand: str):
    raw_model = fix_common_typos(clean_text(raw_model))
    image = (image or "").strip()

    s_wo_years, production = extract_production(raw_model)

    # Split por guiones: [modelo_base, token1, token2, ...]
    parts = [p.strip() for p in s_wo_years.split(" - ") if p.strip()]
    model_base = parts[0] if parts else s_wo_years
    detail_tokens = parts[1:] if len(parts) > 1 else []

    # Remover la marca del inicio si viene embebida (CHEVROLET CORSA -> CORSA)
    b = (brand or "").strip().upper()
    mb = model_base.strip()
    if b and mb.upper().startswith(b + " "):
        mb = mb[len(b):].strip()

    # Split en múltiples modelos si aplica (PRISMA y ONIX -> 2 filas)
    model_names = split_models_on_and(mb)

    version_parts = []
    details_parts = []

    for token in detail_tokens:
        t = clean_text(token)

        if looks_like_body(t):
            details_parts.append(t.upper())
            continue

        # Si es engine: normalizar comas -> " | "
        if looks_like_engine(t):
            sub = [x.strip() for x in t.split(",") if x.strip()]
            version_parts.extend(sub)
            continue

        # Si no es body ni engine, lo mandamos a version (trim/variante)
        version_parts.append(t)

    # Normalizaciones finales
    version = " | ".join([v for v in version_parts if v]).strip()
    details = " | ".join([d for d in details_parts if d]).strip()
    image_url = urljoin(URL_BASE, image) if image else ""

    out = []
    for name in model_names:
        out.append({
            "vehiclemodel_brand": b,
            "vehiclemodel_name": name,
            "vehiclemodel_version": version,
            "vehiclemodel_production": production,
            "vehiclemodel_details": details,
            "image_url": image_url,
            "raw_model": raw_model,
        })

    return out

def main(input_csv: str, output_csv: str, brand: str):
    with open(input_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    out_rows = []
    for r in rows:
        raw_model = r.get("model") or r.get("Modelo") or ""
        image = r.get("image") or r.get("imagen") or r.get("img") or ""
        out_rows.extend(normalize_row(raw_model, image, brand))

    # Deduplicado (por si hay repetidos exactos)
    seen = set()
    unique = []
    for it in out_rows:
        key = (
            it["vehiclemodel_brand"],
            it["vehiclemodel_name"],
            it["vehiclemodel_version"],
            it["vehiclemodel_production"],
            it["vehiclemodel_details"],
            it["image_url"],
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(it)

    fieldnames = [
        "vehiclemodel_brand",
        "vehiclemodel_name",
        "vehiclemodel_version",
        "vehiclemodel_production",
        "vehiclemodel_details",
        "image_url",
        "raw_model",
    ]

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(unique)

    print(f"OK: {len(unique)} filas -> {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python normalize_vehiclemodels.py <input.csv> <output.csv> <BRAND>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
