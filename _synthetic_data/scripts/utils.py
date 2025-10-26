"""
Reusable utilities for synthetic data generation scripts.

This module provides comprehensive utilities for generating deterministic synthetic data
that preserves original field structure while anonymizing sensitive information.

Key Features:
- Deterministic generation using salt-based hashing for consistency
- File I/O helpers with robust encoding handling
- Spatial utilities for point-in-polygon operations
- Professional vocabulary generators for realistic synthetic data
- Field validation and normalization utilities
- Property composition preserving original field order

Main Categories:
- Deterministic helpers: stable_choice, stable_randint, stable_weighted_choice
- File I/O: load_geojson, save_geojson_single_line
- Spatial utilities: build_locality_index, resolve_localitate
- Property composition: compose_properties, compose_properties_generic
- Numeric jittering: stable_jitter_number, jitter_numeric_str
- Professional generators: fake_address, generate_fibre_spec, pick_obs, etc.
- Identifier utilities: normalize_identifier, format_fttb_code, deterministic_uuid5

All functions use deterministic algorithms based on seed strings to ensure
reproducible synthetic data generation across runs.
"""

from __future__ import annotations

import hashlib
import uuid
import json
import os
from numbers import Integral
from typing import Any, Dict, List, Tuple

try:
    from shapely.geometry import shape, Point  # type: ignore
    from shapely.strtree import STRtree  # type: ignore
except Exception as exc:  # pragma: no cover - runtime import guard
    raise SystemExit(
        "This script requires shapely. Install via: pip install shapely"
    ) from exc


# --------------------
# Deterministic helpers
# --------------------

def get_salt() -> str:
    return os.environ.get("ANONYMIZE_SALT", "default-demo-salt")


def stable_choice(seed: str, options: List[str]) -> str:
    hash_hex = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    idx = int(hash_hex[:8], 16) % len(options)
    return options[idx]


# ---------
# File I/O
# ---------

def load_geojson(path: str) -> Dict[str, Any]:
    """Load GeoJSON with robust decoding.

    Strategy:
    - Try utf-8 first
    - If decoding fails, read raw bytes, replace NBSP (0xA0) with space, then try utf-8
    - Fallback to common legacy encodings (cp1252, cp1250, latin-1)
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except UnicodeDecodeError:
        pass

    # Read raw bytes and attempt fixes
    with open(path, "rb") as bf:
        data = bf.read()

    # Replace NBSP (0xA0) with normal space
    data = data.replace(b"\xA0", b" ")

    for enc in ("utf-8", "cp1252", "cp1250", "latin-1"):
        try:
            text = data.decode(enc)
            return json.loads(text)
        except Exception:
            continue

    # Last resort: decode utf-8 with replacement to avoid crashing
    text = data.decode("utf-8", errors="replace")
    return json.loads(text)


def save_geojson_single_line(obj: Dict[str, Any], path: str) -> None:
    """Write GeoJSON with single-line-per-feature formatting.

    - Preserves collection type and name
    - Emits one JSON line per feature for readability in large files
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        fc_type = obj.get("type", "FeatureCollection")
        # Always set collection name to absolute output path
        fc_name = os.path.abspath(path)
        features = obj.get("features", [])

        f.write("{\n")
        f.write(f"  \"type\": {json.dumps(fc_type)},\n")
        f.write(f"  \"name\": {json.dumps(fc_name, ensure_ascii=False)},\n")
        f.write("  \"features\": [\n")
        for idx, feat in enumerate(features):
            line = json.dumps(feat, ensure_ascii=False, separators=(",", ": "))
            f.write("    " + line)
            if idx < len(features) - 1:
                f.write(",")
            f.write("\n")
        f.write("  ]\n")
        f.write("}\n")


# -----------------
# Spatial utilities
# -----------------

def build_locality_index(localitati_fc: Dict[str, Any]) -> Tuple[STRtree, List[Dict[str, Any]], List[Any]]:
    polygons: List[Any] = []
    props_list: List[Dict[str, Any]] = []
    for feat in localitati_fc.get("features", []):
        geom = shape(feat.get("geometry"))
        props = feat.get("properties", {})
        polygons.append(geom)
        props_list.append(props)
    tree = STRtree(polygons)
    return tree, props_list, polygons


def resolve_localitate(pt: Point, tree: STRtree, props_list: List[Dict[str, Any]], polygons: List[Any]) -> str:
    candidates = tree.query(pt)
    for candidate in candidates:
        if isinstance(candidate, Integral):
            idx = int(candidate)
            poly = polygons[idx]
        else:
            poly = candidate
            try:
                idx = polygons.index(poly)
            except ValueError:
                idx = -1
        if hasattr(poly, "contains") and poly.contains(pt):
            if 0 <= idx < len(props_list):
                props = props_list[idx]
                return props.get("NUME") or props.get("COMUNA") or "UNKNOWN"
    return "UNKNOWN"


# --------------------
# Property composition
# --------------------

def compose_properties(
    localitate: str,
    id_tabela: str,
    observatii_1: str,
    observatii_2: str,
    original_props: Dict[str, Any],
    order: List[str] | None = None,
) -> Dict[str, Any]:
    """Compose properties preserving ordering and appending any original extras.

    Default order: LOCALITATE, ID_TABELA, OBSERVATII_1, OBSERVATII_2
    """
    if order is None:
        order = ["LOCALITATE", "ID_TABELA", "OBSERVATII_1", "OBSERVATII_2"]

    base_values = {
        "LOCALITATE": localitate,
        "ID_TABELA": id_tabela,
        "OBSERVATII_1": observatii_1,
        "OBSERVATII_2": observatii_2,
    }

    props_out: Dict[str, Any] = {}
    for key in order:
        if key in base_values:
            props_out[key] = base_values[key]

    # Append remaining original props preserving input iteration order
    for key in original_props.keys():
        if key not in props_out:
            props_out[key] = original_props[key]

    return props_out


def compose_properties_generic(
    base_props: Dict[str, Any],
    original_props: Dict[str, Any],
    order: List[str],
) -> Dict[str, Any]:
    """Compose properties from an explicit base dict and desired order.

    - Keys in `order` are emitted first if present in `base_props`
    - Remaining keys from `base_props` not in `order` follow
    - Remaining keys from `original_props` then appended preserving their order
    """
    props_out: Dict[str, Any] = {}
    for key in order:
        if key in base_props:
            props_out[key] = base_props[key]
    for key, value in base_props.items():
        if key not in props_out:
            props_out[key] = value
    for key in original_props.keys():
        if key not in props_out:
            props_out[key] = original_props[key]
    return props_out


# -----------------
# Numeric jittering
# -----------------

def _parse_float(value: Any) -> float:
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return 0.0


def _decimal_places_of(value: Any) -> int:
    s = str(value)
    if "." in s:
        return len(s.split(".")[-1])
    return 0


def stable_jitter_number(original: float, seed: str, min_delta: float = 1.0, max_delta: float = 100.0) -> float:
    """Deterministically add or subtract a delta in [min_delta, max_delta]."""
    hash_hex = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    # delta from first 12 hex chars
    delta_fraction = int(hash_hex[:12], 16) / float(0xFFFFFFFFFFFF)
    delta = min_delta + (max_delta - min_delta) * delta_fraction
    # sign from next nibble
    sign_bit = int(hash_hex[12], 16) % 2
    signed_delta = delta if sign_bit == 0 else -delta
    candidate = original + signed_delta
    if candidate < 0:
        candidate = 0.0
    return candidate


def jitter_numeric_str(original_value: Any, seed: str, min_delta: float = 1.0, max_delta: float = 100.0) -> str:
    original_num = _parse_float(original_value)
    new_num = stable_jitter_number(original_num, seed, min_delta=min_delta, max_delta=max_delta)
    decimals = _decimal_places_of(original_value)
    fmt = f"{{:.{decimals}f}}"
    return fmt.format(new_num)


# -----------------
# Deterministic RNG
# -----------------

def stable_randint(min_value_inclusive: int, max_value_inclusive: int, seed: str) -> int:
    if min_value_inclusive > max_value_inclusive:
        min_value_inclusive, max_value_inclusive = max_value_inclusive, min_value_inclusive
    span = max_value_inclusive - min_value_inclusive + 1
    hash_hex = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    value = int(hash_hex[:8], 16) % span
    return min_value_inclusive + value


def stable_letter(seed: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    idx = stable_randint(0, len(alphabet) - 1, seed)
    return alphabet[idx]


# -----------------
# Fake generators
# -----------------

_STREET_TYPES = ["Strada", "Bulevardul", "Calea", "Aleea", "Splaiul", "Piata"]
_STREET_NAMES = [
    "Independentei",
    "Unirii",
    "Eroilor",
    "Capitalei",
    "Constructorilor",
    "Viitorului",
    "Trandafirilor",
    "Stejarului",
    "Castanilor",
    "Lalelelor",
]


def fake_address(seed: str) -> str:
    st_type = stable_choice(seed + ":t", _STREET_TYPES)
    st_name = stable_choice(seed + ":n", _STREET_NAMES)
    number = stable_randint(1, 299, seed + ":nr")
    block = stable_letter(seed + ":bl")
    stair = stable_letter(seed + ":sc")
    return f"{st_type} {st_name}, Nr. {number}, Bl. {block} Sc. {stair}"


_FIBRE_CAPACITIES = [24, 48, 72, 96, 144, 192]


def generate_fibre_spec(seed: str) -> str:
    segments = stable_randint(1, 3, seed + ":seg")
    parts: List[str] = []
    for i in range(segments):
        count = stable_randint(1, 3, seed + f":c{i}")
        cap = stable_choice(seed + f":k{i}", [str(c) for c in _FIBRE_CAPACITIES])
        parts.append(f"{count}x{cap}")
    return "/".join(parts)


# ----------------------
# Localitati-specific
# ----------------------

def jitter_integer_str(original_value: Any, seed: str, min_delta: int = 1, max_delta: int = 10) -> str:
    try:
        original = int(float(str(original_value).replace(",", ".")))
    except Exception:
        original = 0
    delta = stable_randint(min_delta, max_delta, seed + ":d")
    sign = stable_randint(0, 1, seed + ":s")
    signed_delta = delta if sign == 0 else -delta
    candidate = original + signed_delta
    if candidate < 0:
        candidate = 0
    return str(candidate)


_PONI_CAPACITIES = [24, 48, 64, 72, 96, 128]


def generate_tip_poni(seed: str) -> str:
    count = stable_randint(1, 10, seed + ":c")
    capacity = stable_choice(seed + ":k", [str(c) for c in _PONI_CAPACITIES])
    return f"{count}x{capacity}"


_IMPLEMENTARE_VALUES = [
    "Activ",
    "In executie",
    "Planificat",
    "Proiectare",
    "Aprobat",
    "Neaprobat",
    "In analiza",
    "Suspendat temporar",
    "Finalizat",
]


def pick_implementare(seed: str) -> str:
    return stable_choice(seed, _IMPLEMENTARE_VALUES)


_OBS_VALUES = [
    "audit retea",
    "extindere planificata",
    "modernizare echipamente",
    "revizie periodica",
    "documentatie actualizata",
    "alocare resurse",
    "retele vechi",
    "",
]


def pick_obs(seed: str) -> str:
    return stable_choice(seed, _OBS_VALUES)


_PROIECTANT_VALUES = [
    "intern",
    "contractor",
    "proiectant licentiat",
    "doc. ANCOM",
    "studiu fezabilitate",
    "proiect tehnic",
]


def pick_proiectant(seed: str) -> str:
    return stable_choice(seed, _PROIECTANT_VALUES)


# ----------------------
# Scari-specific helpers
# ----------------------

_TIP_ART_VALUES = ["Strada", "Bulevard", "Aleea", "Calea", "Piata"]


def normalize_tip_art(value: str | None, seed: str) -> str:
    if value:
        v = value.strip().capitalize()
        # fix common typo
        if v == "Stradda":
            v = "Strada"
        if v in _TIP_ART_VALUES:
            return v
    return stable_choice(seed, _TIP_ART_VALUES)


_DIGIT_TO_LETTER = {
    "1": "A",
    "2": "B",
    "3": "C",
    "4": "D",
    "5": "E",
    "6": "F",
    "7": "G",
    "8": "H",
    "9": "I",
    "0": "J",
}


def _number_to_letters(n: int) -> str:
    """Convert 1->A, 2->B, ..., 26->Z, 27->AA (Excel-style)."""
    if n <= 0:
        return "A"
    result = []
    while n > 0:
        n -= 1
        n, rem = divmod(n, 26)
        result.append(chr(ord('A') + rem))
    return "".join(reversed(result))


def digits_to_letters_only(value: str | None) -> str:
    """Transform NR_SCARA to letters only.

    - Whole number sequences are converted using 1->A..26->Z, 27->AA mapping
    - Existing letters are kept (uppercased)
    - Non-alphanumeric characters are ignored
    """
    if not value:
        return "A"
    s = str(value)
    out_parts: List[str] = []
    num_buf: List[str] = []

    def flush_num_buf():
        if num_buf:
            try:
                n = int("".join(num_buf))
            except Exception:
                n = 0
            out_parts.append(_number_to_letters(n))
            num_buf.clear()

    for ch in s:
        if ch.isdigit():
            num_buf.append(ch)
        elif ch.isalpha():
            flush_num_buf()
            out_parts.append(ch.upper())
        else:
            # ignore separators; just flush any pending number
            flush_num_buf()
    flush_num_buf()
    return "".join(out_parts) or "A"


# ----------------------
# General identifiers
# ----------------------

def normalize_identifier(text: str | None) -> str:
    if not text:
        return "UNKNOWN"
    import re
    s = str(text).strip()
    s = re.sub(r"[^0-9A-Za-z]+", "_", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_").upper() or "UNKNOWN"


def format_fttb_code(localitate: str | None, seq: int, county_code: str = "VS") -> str:
    initial = (localitate or "").strip()[:1].upper() or "X"
    return f"{county_code}{initial}{seq:04d}"


def stable_weighted_choice(seed: str, options_with_weights: List[Tuple[str, int]]) -> str:
    total = sum(max(0, w) for _, w in options_with_weights)
    if total <= 0:
        # fallback to equal weights
        values = [v for v, _ in options_with_weights]
        return stable_choice(seed, values)
    hash_hex = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    pick = int(hash_hex[:8], 16) % total
    acc = 0
    for value, weight in options_with_weights:
        w = max(0, weight)
        if acc + w > pick:
            return value
        acc += w
    # fallback
    return options_with_weights[-1][0]


# ---------------------------------
# PON/FTTH1000 specific conveniences
# ---------------------------------

def jitter_integer(
    original_value: Any,
    seed: str,
    min_delta: int,
    max_delta: int,
    min_value: int,
    max_value: int,
) -> int:
    try:
        orig = int(float(str(original_value).replace(",", ".")))
    except Exception:
        orig = 0
    delta = stable_randint(min_delta, max_delta, seed + ":d")
    sign = stable_randint(0, 1, seed + ":s")
    candidate = orig + (delta if sign == 0 else -delta)
    if candidate < min_value:
        candidate = min_value
    if candidate > max_value:
        candidate = max_value
    return candidate


def extract_locality_from_olt(olt_value: Any) -> str:
    if not olt_value:
        return "UNKNOWN"
    text = str(olt_value)
    # patterns like: olt01.barlad_3_9 → locality between first '.' and next '_' or end
    loc = ""
    if "." in text:
        after = text.split(".", 1)[1]
        if "_" in after:
            loc = after.split("_", 1)[0]
        else:
            loc = after
    else:
        loc = text
    return normalize_identifier(loc)


def normalize_tip_pachet_catv(value: Any, seed: str) -> str:
    if value is None or str(value).strip() == "":
        return ""
    val = str(value).strip().lower()
    candidates = [
        ("Analog", 10),
        ("Digital", 60),
        ("Digital HD", 25),
        ("Full", 5),
    ]
    # heuristic mapping
    if "analog" in val:
        return "Analog"
    if "hd" in val:
        return "Digital HD"
    if "full" in val:
        return "Full"
    if "digit" in val:
        return "Digital"
    return stable_weighted_choice(seed, candidates)


_VERIF_ACOPERIRE_VALUES = [
    "verificat teren",
    "desk-check",
    "confirmat apel",
    "in analiza",
    "",
]


def pick_verif_acoperire(seed: str) -> str:
    return stable_choice(seed, _VERIF_ACOPERIRE_VALUES)


def pick_tip_proiect(original_value: Any, seed: str) -> str:
    val = str(original_value).strip().upper() if original_value is not None else ""
    mapping = {
        "GHN": "FTTH-GHN",
        "GVN": "FTTH-GVN",
        "GVO": "FTTH-GVO",
    }
    if val in mapping:
        return mapping[val]
    options = ["FTTH-GHN", "FTTH-GVN", "FTTH-GVO", "FTTB-MDU", "FTTH-GPON"]
    return stable_choice(seed, options)


def compute_digi_id(year_month: str, seq: int, salt: str) -> str:
    base = f"{year_month}:{seq}:{salt}"
    h = hashlib.sha256(base.encode("utf-8")).hexdigest()
    chk = (int(h[:4], 16) % 676)  # 26*26
    c1 = chr(ord('A') + (chk // 26))
    c2 = chr(ord('A') + (chk % 26))
    return f"DGI-{year_month}-{seq:06d}-{c1}{c2}"


def deterministic_uuid5(seed: str) -> str:
    """Generate a stable UUIDv5 from a seed string; returns uppercase canonical form."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed)).upper()


