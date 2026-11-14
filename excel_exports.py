"""Ready-to-read Excel export builders shared by the HTTP endpoints and the
automatic snapshot sidecars in backups/ready_exports/ — those are written on
every backup so the key views (Available Stock, Sell Record) can be opened
straight in Excel even when the app itself won't start.
"""
import datetime
import io
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.properties import PageSetupProperties

_TITLE_FILL = PatternFill("solid", fgColor="00B0F0")
_THIN = Side(style="thin", color="9E9E9E")
_BORDER = Border(left=_THIN, right=_THIN, top=_THIN, bottom=_THIN)


def _sheet_title(name: str, used: set) -> str:
    """Excel sheet names: max 31 chars, none of []:*?/\\, unique."""
    base = re.sub(r"[\[\]:*?/\\]", " ", str(name)).strip()[:31] or "Sheet"
    title, n = base, 2
    while title.lower() in used:
        suffix = f" ({n})"
        title = base[:31 - len(suffix)] + suffix
        n += 1
    used.add(title.lower())
    return title


def _fill_available_sheet(ws, keys, stock, booked, title="Available Stock"):
    """One sheet in the manual layout: NO | Model | Brand | TOTAL | Booking | Balance."""
    ws.sheet_view.zoomScale = 85

    ws.merge_cells("A1:F1")
    t = ws["A1"]
    t.value = title
    t.font = Font(bold=True, size=14)
    t.fill = _TITLE_FILL
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 24

    headers = ["NO.", "Model", "Brand", "TOTAL", "Booking", "Balance"]
    center = Alignment(horizontal="center", vertical="center")
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=2, column=c, value=h)
        cell.font = Font(bold=True)
        cell.alignment = center
        cell.border = _BORDER
    ws.auto_filter.ref = "A2:F2"
    ws.freeze_panes = "A3"

    num_fmt = "0.00"
    for i, (brand, model) in enumerate(keys, 1):
        r = i + 2
        total = stock.get((brand, model), 0) + booked.get((brand, model), 0)
        bking = booked.get((brand, model), 0)
        balance = total - bking
        vals = [i, model, brand, total, bking]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.border = _BORDER
            cell.alignment = center
        for c in (4, 5):
            ws.cell(row=r, column=c).number_format = num_fmt
        bal = ws.cell(row=r, column=6, value=f"=D{r}-E{r}")
        bal.number_format = num_fmt
        bal.border = _BORDER
        bal.alignment = center
        if balance <= 0:
            bal.font = Font(color="FF0000")

    for col, w in zip("ABCDEF", (10.3, 29.0, 11.9, 13.4, 13.9, 13.6)):
        ws.column_dimensions[col].width = w


def _count_stock(records, now):
    """({(brand, model): in-stock units}, {(brand, model): booked units}).
    Booked = sold with a Date Out still in the future."""
    from stock_store import IN_STOCK, SOLD, parse_datetime_safe

    stock, booked = {}, {}
    for rec in records:
        status = str(rec.get("Status") or "").strip()
        key = (str(rec.get("Brand") or "").strip() or "UNBRANDED",
               str(rec.get("Model") or "").strip())
        if status == IN_STOCK:
            stock[key] = stock.get(key, 0) + 1
        elif status == SOLD:
            dt = parse_datetime_safe(str(rec.get("Date Out") or ""))
            if dt and dt > now:
                booked[key] = booked.get(key, 0) + 1
    return stock, booked


def _fill_broken_sheet(ws, broken):
    """'Broken' sheet: NO | SERIAL/DESC | MODEL | CUSTOMER | NOTES."""
    center = Alignment(horizontal="center", vertical="center")
    for c, h in enumerate(["NO", "SERIAL/DESC", "MODEL", "CUSTOMER", "NOTES"], 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = Font(bold=True)
        cell.alignment = center
        cell.border = _BORDER
    ws.auto_filter.ref = "A1:E1"
    ws.freeze_panes = "A2"
    for i, (serial, model, customer, notes) in enumerate(broken, 1):
        for c, v in enumerate((i, serial, model, customer, notes), 1):
            cell = ws.cell(row=i + 1, column=c, value=v)
            cell.border = _BORDER
            if c == 1:
                cell.alignment = center
    for col, w in zip("ABCDE", (6.0, 18.0, 24.0, 18.0, 40.0)):
        ws.column_dimensions[col].width = w


def _broken_rows(records, returns):
    """Units that are Quarantined right now. Released units flip back to
    In Stock (and their Returns entry to 'Restocked'), so they drop out on
    their own. Notes come from the latest open 'Quarantined' Returns entry."""
    from stock_store import QUARANTINED

    def k(r):
        return (str(r.get("Serial") or "").strip().lower(),
                str(r.get("Model") or "").strip().lower())

    notes = {}
    for ret in returns or []:
        if str(ret.get("Action") or "").strip() == "Quarantined":
            notes[k(ret)] = str(ret.get("Notes") or "").strip()   # last one wins
    rows = []
    for rec in records:
        if str(rec.get("Status") or "").strip() == QUARANTINED:
            rows.append((str(rec.get("Serial") or "").strip(),
                         str(rec.get("Model") or "").strip(),
                         str(rec.get("Customer") or "").strip(),
                         notes.get(k(rec), "")))
    rows.sort(key=lambda r: (r[1].upper(), r[0].upper()))
    return rows


def build_available_workbook(records, now=None, brands=None, returns=None) -> bytes:
    """Per-model summary in the user's manual 'Available Stock' layout:
    NO | Model | Brand | TOTAL | Booking | Balance.
    TOTAL = physical units (in stock + booked for future dispatch);
    Balance = TOTAL - Booking = what can still be dispatched today.

    brands=None  -> one 'Available' sheet with every brand (the default export).
    brands=[...] -> one sheet per chosen brand (brands with no units are
                    skipped); returns b"" when nothing is left to export.

    The full export (brands=None) also gets a 'Broken' sheet listing the units
    that are Quarantined right now (omitted when there are none). Per-brand
    exports never include it."""
    now = now or datetime.datetime.now()
    stock, booked = _count_stock(records, now)

    keys = sorted(set(stock) | set(booked),
                  key=lambda k: (k[0].upper(), k[1].upper()))

    wb = Workbook()
    if brands is None:
        ws = wb.active
        ws.title = "Available"
        _fill_available_sheet(ws, keys, stock, booked)
        broken = _broken_rows(records, returns)
        if broken:
            _fill_broken_sheet(wb.create_sheet("Broken"), broken)
    else:
        wanted = []
        for b in brands:
            b = str(b).strip().upper()
            if b and b not in wanted:
                wanted.append(b)
        used, first = set(), True
        for b in sorted(wanted):
            bkeys = [k for k in keys if k[0].upper() == b]
            if not bkeys:
                continue                      # brand with no units: no sheet
            ws = wb.active if first else wb.create_sheet()
            first = False
            brand_name = bkeys[0][0]
            ws.title = _sheet_title(brand_name, used)
            _fill_available_sheet(ws, bkeys, stock, booked,
                                  title=f"Available Stock - {brand_name}")
        if first:
            return b""

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


_GROUP_FILL = PatternFill("solid", fgColor="A5A5A5")
# Same look as the hand-made Available sheet: Times New Roman 11, black thin borders
_MFONT = "Times New Roman"
_MBLACK = Side(style="thin", color="000000")
_MBORDER = Border(left=_MBLACK, right=_MBLACK, top=_MBLACK, bottom=_MBLACK)


def _roman(n: int) -> str:
    out = ""
    for v, sym in ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += sym
            n -= v
    return out


def _manual_groups(stock, booked, catalog):
    """Group the stock into the manual layout.
    Returns [(category, [row dict, ...]), ...] - categories in catalog order,
    empty ones left out, 'Other' (models not in the catalog) last."""
    keys = set(stock) | set(booked)
    order = {}
    for e in catalog:
        order.setdefault(e["category"] or "Other", len(order))

    def counts(key):
        return stock.get(key, 0), booked.get(key, 0)

    # a partner (outdoor) model can belong to ONE indoor row only
    claimed = {}
    for e in catalog:
        p = e["pair"].lower()
        if p and p != e["model"].lower() and p not in claimed:
            claimed[p] = e["model"].lower()

    rows, consumed = [], set()
    brands = {b for b, _ in keys}
    for e in catalog:
        if claimed.get(e["model"].lower(), e["model"].lower()) != e["model"].lower():
            continue          # listed as another row's outdoor partner: shown in that set
        p = e["pair"].lower()
        paired = bool(p) and claimed.get(p) == e["model"].lower()
        for b in sorted(brands):
            ikeys = [k for k in keys if k[0] == b and k[1].lower() == e["model"].lower()]
            okeys = ([k for k in keys if k[0] == b and k[1].lower() == p]
                     if paired else [])
            if not ikeys and not okeys:
                continue
            ik = ikeys[0] if ikeys else (b, e["model"])
            if not paired:
                consumed.add(ik)
                s, bk = counts(ik)
                rows.append({"cat": e["category"] or "Other", "ord": len(rows), "type": e["type"],
                             "model": ik[1], "hp": e["hp"], "brand": b,
                             "stock": s, "booked": bk, "note": ""})
                continue
            ok = okeys[0] if okeys else (b, e["pair"])
            consumed.update((ik, ok))
            (si, bi), (so, bo) = counts(ik), counts(ok)
            s, bk = min(si, so), min(bi, bo)
            extras = []
            if si + bi > s + bk:
                extras.append(f"{si + bi - s - bk} x {ik[1]} without outdoor")
            if so + bo > s + bk:
                extras.append(f"{so + bo - s - bk} x {ok[1]} without indoor")
            rows.append({"cat": e["category"] or "Other", "ord": len(rows), "type": e["type"],
                         "model": f"{ik[1]}/{ok[1]}", "hp": e["hp"], "brand": b,
                         "stock": s, "booked": bk, "note": "; ".join(extras)})

    groups = {}
    for r in rows:
        groups.setdefault(r["cat"], []).append(r)
    out = [(c, sorted(groups[c], key=lambda r: r["ord"]))
           for c in sorted(groups, key=lambda c: order.get(c, 10**6))]

    other = []
    for k in sorted(keys - consumed, key=lambda k: (k[0].upper(), k[1].upper())):
        s, bk = counts(k)
        other.append({"cat": "Other", "ord": 0, "type": "", "model": k[1], "hp": "",
                      "brand": k[0], "stock": s, "booked": bk,
                      "note": "Not in model_catalog.xlsx"})
    if other:
        out = [g for g in out if g[0] != "Other"]
        out.append(("Other", other))
    return out


def _fill_manual_sheet(ws, groups):
    """NO | Type | Model | Horse power | Brand | TOTAL | Booking | Balance
    with a numbered (I, II, ...) grey heading row for each group."""
    ws.sheet_view.zoomScale = 85
    has_note = any(r["note"] for _, rows in groups for r in rows)
    last = "H"                  # the printed table ends at Balance; Note sits outside it
    ncols = 8
    center = Alignment(horizontal="center", vertical="center")

    ws.merge_cells(f"A1:{last}1")
    t = ws["A1"]
    t.value = "Available Stock"
    t.font = Font(name=_MFONT, bold=True, size=20, color="000000")
    t.fill = _TITLE_FILL
    t.border = _MBORDER
    t.alignment = center
    ws.row_dimensions[1].height = 36.5

    heads = ["NO.", "Type", "Model", "Horse power", "Brand", "TOTAL", "Booking", "Balance"]
    for c, h in enumerate(heads, 1):
        cell = ws.cell(row=2, column=c, value=h)
        cell.font = Font(name=_MFONT, bold=True, size=11, color="000000")
        cell.fill = _TITLE_FILL
        cell.alignment = center
        cell.border = _MBORDER
    if has_note:                # for your own eyes only: same font and colour as the table, no fill / borders, not printed
        nh = ws.cell(row=2, column=9, value="Note")
        nh.font = Font(name=_MFONT, bold=True, size=11, color="000000")
        nh.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[2].height = 28.5
    ws.freeze_panes = "A3"

    r = 3
    for gi, (cat, rows) in enumerate(groups, 1):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.fill = _GROUP_FILL
            cell.border = _MBORDER
            cell.font = Font(name=_MFONT, bold=True, size=11, color="000000")
        ws.cell(row=r, column=1, value=_roman(gi)).alignment = center
        ws.cell(row=r, column=2, value=cat).alignment = Alignment(vertical="center")
        ws.row_dimensions[r].height = 24.5
        r += 1
        for i, row in enumerate(rows, 1):
            total = row["stock"] + row["booked"]
            vals = [i, row["type"], row["model"], row["hp"], row["brand"], total, row["booked"]]
            for c, v in enumerate(vals, 1):
                ws.cell(row=r, column=c, value=v if v != "" else None)
            ws.cell(row=r, column=8, value=f"=F{r}-G{r}")
            if has_note and row["note"]:
                nc = ws.cell(row=r, column=9, value=row["note"])
                nc.font = Font(name=_MFONT, size=11, color="000000")
                nc.alignment = Alignment(horizontal="left", vertical="center")
            for c in range(1, ncols + 1):
                cell = ws.cell(row=r, column=c)
                cell.border = _MBORDER
                cell.alignment = center
                cell.font = Font(name=_MFONT, size=11, color="000000")
                if c == 4:
                    cell.number_format = "0.0"
                elif c in (6, 7, 8):
                    cell.number_format = "0.00"
            if row["stock"] <= 0:
                ws.cell(row=r, column=8).font = Font(name=_MFONT, size=11, color="9C0006")
            ws.row_dimensions[r].height = 24.5
            r += 1

    widths = [8.73, 18.18, 36.45, 14.18, 14.45, 13.73, 14.09, 15.0] + ([40.0] if has_note else [])
    # same widths as the hand-made sheet; only the Brand column grows when a
    # brand name would be cut off (e.g. "DAIKIN-AIR CONDITIONER")
    longest = max((len(r["brand"]) for _, rows in groups for r in rows), default=0)
    widths[4] = max(widths[4], min(longest * 1.15 + 2, 32.0))
    for c, w in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + c)].width = w

    # printing like the hand-made sheet: portrait A4, fit to one page wide, centred,
    # and only NO. .. Balance (the Note column is not printed)
    ws.print_area = f"A1:H{r - 1}"
    ws.page_setup.orientation = "portrait"
    ws.page_setup.paperSize = 9
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.print_options.horizontalCentered = True


def build_available_manual_workbook(records, now=None, returns=None, catalog=None) -> bytes:
    """Available Stock in the manual (hand-made) layout: groups I, II, III...
    with indoor/outdoor sets on one row, driven by model_catalog.xlsx
    (`catalog` = model_catalog.load_catalog()). Adds the 'Broken' sheet
    (quarantined units) exactly like the standard full export."""
    import model_catalog

    now = now or datetime.datetime.now()
    if catalog is None:
        catalog = model_catalog.seed_entries()
    stock, booked = _count_stock(records, now)
    wb = Workbook()
    ws = wb.active
    ws.title = "Available"
    _fill_manual_sheet(ws, _manual_groups(stock, booked, catalog))
    broken = _broken_rows(records, returns)
    if broken:
        _fill_broken_sheet(wb.create_sheet("Broken"), broken)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def _warranty_label(w: dict) -> str:
    """Same wording the app shows: 'Active · 366 days' / Expiring / Expired."""
    st, days = w.get("status"), w.get("daysRemaining")
    if st == "active":
        return f"Active · {days} days"
    if st == "expiring":
        return f"Expiring · {days} days"
    if st == "expired":
        return "Expired"
    return "—"


def sell_rows(track: list[dict], now=None) -> list[dict]:
    """store.track_list() dicts -> the row shape build_sell_workbook writes."""
    from stock_store import parse_datetime_safe

    now = now or datetime.datetime.now()
    rows = []
    for r in track:
        dt = parse_datetime_safe(str(r.get("dateOut") or ""))
        rows.append({
            "model": r.get("model", ""), "serial": r.get("serial", ""),
            "dateIn": r.get("dateIn", ""), "dateOut": r.get("dateOut", ""),
            "customer": r.get("customer", ""),
            "wstatus": _warranty_label(r.get("warranty") or {}),
            "wexpiry": (r.get("warranty") or {}).get("expiry", ""),
            "status": "Booked" if (dt and dt > now) else "Dispatched",
        })
    return rows


def build_sell_workbook(rows: list[dict], title: str = "Sell Records") -> bytes:
    """One row per sold unit: NO | Model | Serial | Date In | Dispatched At |
    Customer | Warranty Status | Warranty Expiry | Status."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Sell Record"
    ws.sheet_view.zoomScale = 85

    headers = ["NO.", "Model", "Serial Num/Desc", "Date In", "Dispatched At",
               "Customer Destination", "Warranty Status", "Warranty Expiry",
               "Status"]
    ws.merge_cells("A1:I1")
    t = ws["A1"]
    t.value = str(title or "Sell Records")[:80]
    t.font = Font(bold=True, size=14)
    t.fill = _TITLE_FILL
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 24

    center = Alignment(horizontal="center", vertical="center")
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=2, column=c, value=h)
        cell.font = Font(bold=True)
        cell.alignment = center
        cell.border = _BORDER
    ws.auto_filter.ref = "A2:I2"
    ws.freeze_panes = "A3"

    for i, row in enumerate(rows, 1):
        vals = [i,
                row.get("model", ""), row.get("serial", ""),
                row.get("dateIn", ""), row.get("dateOut", ""),
                row.get("customer", ""), row.get("wstatus", ""),
                row.get("wexpiry", ""), row.get("status", "Dispatched")]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=i + 2, column=c, value=v)
            cell.border = _BORDER
            cell.alignment = center

    for col, w in zip("ABCDEFGHI", (7, 24, 22, 14, 18, 24, 16, 16, 12)):
        ws.column_dimensions[col].width = w

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def write_ready_exports(store, keep: int = 10) -> list[Path]:
    """Drop Available-Stock + Sell-Record workbooks beside the snapshots so a
    crash never leaves the user without a readable copy. Keeps the newest
    `keep` of each kind, overwriting in a loop."""
    from stock_store import DB_PATH

    out_dir = DB_PATH.parent / "backups" / "ready_exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d_%H%M%S")

    written = []
    for prefix, data in (
        ("Available-Stock", build_available_workbook(store.records, now,
                                 returns=store.returns)),
        ("Sell-Record", build_sell_workbook(
            sell_rows(store.track_list(), now),
            f"Sell Record — {now:%Y-%m-%d %H:%M}")),
    ):
        dest = out_dir / f"{prefix}_{stamp}.xlsx"
        i = 2
        while dest.exists():
            dest = out_dir / f"{prefix}_{stamp}_{i}.xlsx"
            i += 1
        dest.write_bytes(data)
        written.append(dest)

    for prefix in ("Available-Stock", "Sell-Record"):
        olds = sorted(out_dir.glob(f"{prefix}_*.xlsx"),
                      key=lambda p: p.stat().st_mtime)
        for f in olds[:-keep]:
            try:
                f.unlink()
            except OSError:
                pass
    return written
