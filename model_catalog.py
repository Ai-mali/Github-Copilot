"""Model catalog for the manual-format 'Available Stock' export.

model_catalog.xlsx lives next to the stock database. One row per model:

    Model | Category | Type | HP | Pair (outdoor)

* Category  - the group heading in the export (I, II, III ... are numbered
              automatically, in the order the categories first appear here).
* Type      - free text shown in the Type column (Inverter, FCFC, ...).
* HP        - horse power (leave blank when it does not apply).
* Pair      - the outdoor model that is sold together with this indoor model;
              the export shows one row "INDOOR/OUTDOOR" for the set.

The file is created from SEED_ROWS the first time it is needed and is never
overwritten afterwards, so edit it freely. Models that are in stock but not
listed here are exported in an "Other" group at the bottom.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

CATALOG_HEADER = ["Model", "Category", "Type", "HP", "Pair (outdoor)"]

_WM, _VWM, _MS = "Wall Mounted", "VRV FCU Wall Mounted", "Multi Split CU"
_CC, _VCC = "Ceiling Cassette", "VRV FCU Ceiling Cassette"
_CD, _PN, _VCU = "Conceal Duct", "Panel", "VRV CU"
_RC, _YB, _DP = "Remote Controller", "Y-Branch", "Drain Pump"
_AP, _MC = "Air Purifier", "Mobile Controller"

# (Model, Category, Type, HP, Pair)
SEED_ROWS = [
    ("FTKH50AV1F", _WM, "Inverter", 2, "RKU50FGV1"),
    ("FTKU25AV1F", _WM, "Inverter", 1, "RKU25FGV1"),
    ("FTKU35AV1F", _WM, "Inverter", 1.5, "RKU35FGV1"),
    ("FTKE25AV1F", _WM, "Inverter", 1, "RKE25AV1"),
    ("FTKE35AV1F", _WM, "Inverter", 1.5, "RKE35AV1"),
    ("FTKE50AV1F", _WM, "Inverter", 2, "RKE50AV1"),
    ("FTV25CV19", _WM, "Non inverter", 1, "RV25CV19"),
    ("FTV35CV19", _WM, "Non inverter", 1.5, "RV35CV19"),
    ("FXAQ25PVE", _VWM, "VRV, FCU", 1, ""),
    ("FXAQ32AVM", _VWM, "VRV, FCU", 1.5, ""),
    ("MKM80PVM", _MS, "Multi split, CU", 3.5, ""),
    ("FCFC71AV1F", _CC, "Inverter", 3, "RZFC71AGV19"),
    ("FCFC125AV1F", _CC, "Inverter", 5, "RZFC125AY19"),
    ("FCFG71AV1F", _CC, "Inverter-Kiriu", 3, ""),
    ("FCCV60AV1F", _CC, "Kiriu", 2.5, "RGFV60AGV1"),
    ("FCCV125AV1F", _CC, "Kiriu", 5, "RGFV125AGY1"),
    ("FCC50AV1", _CC, "Non inverter", 2, "RC50AGV1"),
    ("FCC85AV1", _CC, "Non inverter", 3, "RC85AGV1"),
    ("FCC100AV1", _CC, "Non inverter", 4, ""),
    ("RZFC50AGV1", _CC, "Inverter", 2, ""),
    ("RZFC85AV1", _CC, "Inverter", 3, ""),
    ("RZFC100AV1", _CC, "Inverter", 4, ""),
    ("FXFQ25AVM", _VCC, "VRV, FCU", 1, ""),
    ("FXFQ50AVM", _VCC, "VRV, FCU", 2, ""),
    ("FXFQ125AVM", _VCC, "VRV, FCU", 5, ""),
    ("FDMFC60AV1", _CD, "Inverter", 2.5, "RZFC60AGV1"),
    ("FDMC100AV1", _CD, "Non Inverter", 4, "RC100AGV1"),
    ("RZFC125AY1", _CD, "Inverter", 5, ""),
    ("BCR50FF", _PN, "FCFC", "", ""),
    ("BCR50GF", _PN, "FCFG", "", ""),
    ("BC50F", _PN, "FCC", "", ""),
    ("BC50GF", _PN, "FCCV", "", ""),
    ("BYCQ125EAF", _PN, "FCF,FXFQ", "", ""),
    ("RXMQ6BVM", _VCU, "VRV, CU", 6, ""),
    ("RXQ8AYM", _VCU, "VRV, CU", 8, ""),
    ("BRC1E63", _RC, "", "", ""),
    ("BRC1H63K", _RC, "", "", ""),
    ("BRC7M676", _RC, "", "", ""),
    ("BRC2E61", _RC, "", "", ""),
    ("ARBLN03321", _YB, "", "", ""),
    ("ARBLN07121", _YB, "", "", ""),
    ("ARBLN01621", _YB, "", "", ""),
    ("KHRP26A22T7", _YB, "", "", ""),
    ("KHRP26A33T7", _YB, "", "", ""),
    ("KHRP26A72T7", _YB, "", "", ""),
    ("Optional Drain Pump", _DP, "", "", ""),
    ("BDU510A250VM", _DP, "", "", ""),
    ("MC55UVM-7", _AP, "", "", ""),
    ("MC40UVM6-7", _AP, "", "", ""),
    ("BRP072C42-1", _MC, "", "", ""),
    ("BRP072C42", _MC, "", "", ""),
]


def seed_entries() -> list[dict]:
    return [_entry(*r) for r in SEED_ROWS]


def _entry(model, category, type_="", hp="", pair="") -> dict:
    return {"model": str(model or "").strip(), "category": str(category or "").strip(),
            "type": str(type_ or "").strip(), "hp": hp if hp not in (None, "") else "",
            "pair": str(pair or "").strip()}


def catalog_path() -> Path:
    from stock_store import DB_PATH
    return Path(DB_PATH).parent / "model_catalog.xlsx"


def write_catalog(path, entries=None) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font

    entries = entries if entries is not None else seed_entries()
    wb = Workbook()
    ws = wb.active
    ws.title = "Catalog"
    ws.append(CATALOG_HEADER)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="center")
    for e in entries:
        ws.append([e["model"], e["category"], e["type"], e["hp"], e["pair"]])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:E{max(ws.max_row, 2)}"
    for col, w in zip("ABCDE", (26, 26, 18, 8, 22)):
        ws.column_dimensions[col].width = w

    help_ = wb.create_sheet("How to use")
    for line in (
        "model_catalog.xlsx - used by 'Export (manual format)' on Available Stock.",
        "",
        "Model     : exact model name as it appears in the app (not case sensitive).",
        "Category  : group heading. Groups are numbered I, II, III... automatically,",
        "            in the order the categories first appear in the Catalog sheet,",
        "            and groups with no stock are left out (no gaps in the numbering).",
        "Type      : text shown in the Type column.",
        "HP        : horse power (blank for panels, controllers, ...).",
        "Pair      : outdoor model sold with this indoor model. The export shows one",
        "            row 'INDOOR/OUTDOOR' = number of complete sets. A model can be",
        "            the Pair of only ONE row.",
        "",
        "Models in stock that are not listed here appear in an 'Other' group at the",
        "bottom with the note 'Not in model_catalog.xlsx' - add them here and export again.",
        "This file is never overwritten by the app. Delete it to get the default list back.",
    ):
        help_.append([line])
    help_.column_dimensions["A"].width = 100
    wb.save(path)


def ensure_catalog(path=None) -> Path | None:
    """Create the default catalog file if it does not exist. Never overwrites.
    Returns the path (or None when it cannot be written)."""
    p = Path(path) if path else catalog_path()
    if p.exists():
        return p
    try:
        write_catalog(p)
        return p
    except Exception:
        return None


def load_catalog(path=None) -> list[dict]:
    """Read model_catalog.xlsx. Falls back to the built-in default list when
    the file is missing or unreadable, so an export never fails because of it."""
    p = Path(path) if path else catalog_path()
    try:
        from openpyxl import load_workbook
        wb = load_workbook(p, read_only=True, data_only=True)
        ws = wb["Catalog"] if "Catalog" in wb.sheetnames else wb.worksheets[0]
        rows = ws.iter_rows(values_only=True)
        head = [str(h or "").strip().lower() for h in next(rows)]

        def col(prefix):
            return next((i for i, h in enumerate(head) if h.startswith(prefix)), None)

        ix = {k: col(k) for k in ("model", "category", "type", "hp", "pair")}
        if ix["model"] is None or ix["category"] is None:
            raise ValueError("Catalog needs Model and Category columns")
        out, seen = [], set()
        for r in rows:
            def get(k):
                i = ix[k]
                return r[i] if i is not None and i < len(r) else ""
            e = _entry(get("model"), get("category"), get("type"), get("hp"), get("pair"))
            if e["model"] and e["model"].lower() not in seen:
                seen.add(e["model"].lower())
                out.append(e)
        wb.close()
        return out
    except Exception:
        return seed_entries()


def _clean_hp(v):
    if v in (None, ""):
        return ""
    try:
        f = float(str(v).strip())
    except ValueError:
        return str(v).strip()
    return int(f) if f == int(f) else f


def validate_entries(raw) -> tuple[list[dict] | None, str]:
    """Clean the rows sent by the Model Catalog window.
    Returns (entries, "") or (None, error message). Rows without a model or a
    category are dropped; a model may appear once; an outdoor (pair) model can
    belong to only one indoor row."""
    if not isinstance(raw, list):
        return None, "Invalid catalog data"
    out, seen, claimed = [], set(), {}
    for r in raw:
        if not isinstance(r, dict):
            continue
        e = _entry(r.get("model"), r.get("category"), r.get("type"),
                   _clean_hp(r.get("hp")), r.get("pair"))
        if not e["model"] or not e["category"]:
            continue
        if max(len(e["model"]), len(e["category"]), len(e["type"]), len(e["pair"])) > 80:
            return None, f"Text too long in row {e['model']}"
        k = e["model"].lower()
        if k in seen:
            return None, f"{e['model']} is listed twice"
        seen.add(k)
        p = e["pair"].lower()
        if p:
            if p == k:
                return None, f"{e['model']} cannot be paired with itself"
            if p in claimed:
                return None, (f"{e['pair']} is already the outdoor unit of "
                              f"{claimed[p]} - one outdoor model can belong to one row only")
            claimed[p] = e["model"]
        out.append(e)
    return out, ""


def save_catalog(raw, path=None) -> tuple[bool, str]:
    """Validate and write model_catalog.xlsx, keeping the previous version as
    model_catalog.bak. The new file is written aside first and swapped in, so a
    failure never leaves a half-written catalog."""
    entries, err = validate_entries(raw)
    if entries is None:
        return False, err
    p = Path(path) if path else catalog_path()
    tmp = p.with_name(p.stem + ".tmp.xlsx")
    try:
        write_catalog(tmp, entries)
        if p.exists():
            shutil.copy2(p, p.with_suffix(".bak"))
        os.replace(tmp, p)
        return True, ""
    except PermissionError:
        return False, "model_catalog.xlsx is open in Excel - close it and try again"
    except Exception as ex:                                   # pragma: no cover
        return False, f"Could not save the catalog ({ex})"
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass


def uncategorised(records, entries, now=None) -> list[dict]:
    """Models that are in stock (or booked) but have no catalog category and are
    not the outdoor partner of a catalogued row -> [{model, brand, units}]."""
    import datetime
    import excel_exports

    stock, booked = excel_exports._count_stock(records, now or datetime.datetime.now())
    known = {e["model"].lower() for e in entries if e["category"]}
    claimed = {e["pair"].lower() for e in entries if e["pair"] and e["category"]}
    out = {}
    for (brand, model) in set(stock) | set(booked):
        if model.lower() in known or model.lower() in claimed or not model:
            continue
        units = stock.get((brand, model), 0) + booked.get((brand, model), 0)
        o = out.setdefault(model.lower(), {"model": model, "brand": brand, "units": 0})
        o["units"] += units
    return sorted(out.values(), key=lambda d: d["model"].upper())


def stock_info(records, now=None) -> dict:
    """{lower-case model: {brand, stock, booked}} for every model in stock or
    booked. The Model Catalog window uses it to number the preview groups
    (groups with no stock are skipped, like the export) and to show the real
    brand / TOTAL / Booking / Balance in the Excel preview."""
    import datetime
    import excel_exports

    stock, booked = excel_exports._count_stock(records, now or datetime.datetime.now())
    info = {}
    for key in set(stock) | set(booked):
        brand, model = key
        if not model:
            continue
        s, b = stock.get(key, 0), booked.get(key, 0)
        o = info.setdefault(model.lower(), {"brand": brand, "stock": 0, "booked": 0, "_best": -1})
        if s + b > o["_best"]:                    # brand with the most units wins
            o["brand"], o["_best"] = brand, s + b
        o["stock"] += s
        o["booked"] += b
    for o in info.values():
        o.pop("_best", None)
    return info
