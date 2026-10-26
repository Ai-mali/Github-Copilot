# VRE AC Stock — Project Handover

**Repo:** https://github.com/Ai-mali/Antigravity-Stock.git (private workflow — license tool lives OUTSIDE this repo, see §7)
**Product:** Windows desktop app for air-conditioner parts stock management (Daikin + other brands), Excel-backed, no server install.

---

## 1. What it does (business workflow)

```
Delivery-order photo → AI scan → Stock In → Available Stock
     → Dispatch/Stock Out (customer + dates) → Sell Record / Tracking
     → Return & RMA → Restock or Quarantine → Warranty tracking
```

Plus: customer history, brand/model catalog, activity audit log, auto backups, Excel/CSV exports, day/dark themes, custom wallpapers, all dates displayed `DD/MM/YYYY`.

## 2. Architecture — one process, three layers

```
desktop_app.py   PyWebView/WebView2 frameless window + native splash + window controls
      │          spawns backend in a thread (uvicorn, port 8000)
backend.py       FastAPI on 127.0.0.1:8000 — serves ac-stock-tracker.html at "/"
      │          every /api/* call serialized by a global asyncio.Lock
stock_store.py   StockStore wraps openpyxl → daikin_stock.xlsx (the entire database)
```

`ac-stock-tracker.html` (~17,400 lines) is the ENTIRE frontend — HTML + CSS + vanilla JS in one file. It talks to `127.0.0.1:8000/api/*` via `api()`/`apiGet`/`apiPost`/`apiDel` helpers.

## 3. File map

| File | Role |
|---|---|
| `ac-stock-tracker.html` | Whole UI: Stock In, Available Stock, Stock Out, Track List, Return tabs; modals; theme engine |
| `backend.py` | FastAPI routes (35+ endpoints), license middleware, config/ui-prefs, scan endpoint |
| `stock_store.py` | StockStore: workbook load/migrate/save, all business logic, backups, activity log |
| `desktop_app.py` | Desktop shell: splash screen, health check, frameless window, JS↔Python bridge (`DesktopApi`) |
| `license_check.py` | Embedded license verifier (Ed25519) — ships with the app |
| `scanner.py` | Vision-AI calls (Gemini etc.) via urllib; keys from config modal |
| `excel_exports.py` | Ready-export workbooks after each snapshot |
| `comet_layer.py`, `boot_debug_kit.py` | Boot splash animation + boot timing/debug |
| `test_fulfillment_groups.js` | Node test suite (73 tests) for tracking/fulfillment logic |
| `build-exe.bat` | PyInstaller onefile build → `dist\VRE AC Stock.exe` |

## 4. Data model — the Excel workbook IS the database

Sheets inside `daikin_stock.xlsx`:

| Sheet | Columns | Purpose |
|---|---|---|
| `MasterRecord` | Brand, Model, Serial, Date In, Status, Customer, Date Out, Batch | Every unit; Status ∈ `in_stock` / `sold` |
| `Brands` | Brand | Brand list → accordion grouping + colors |
| `ModelBrands` | Model, Brand | model→brand map; deleted when last unit of a model goes (unless sold history needs it) |
| `Returns` | Serial, Model, Customer, Reason, Condition, Notes, Action, Date, Date Out | RMA registry (restock/quarantine) |
| `ActivityLog` | … | audit trail |

**Serial uniqueness rule (important):** a duplicate = same **model + serial**. Same serial under a *different* model is legal. Unit lookups are model-context-aware (`_pair_key`, `_unit_find`).

**Non-serialized items** get synthetic auto-IDs (`_split_dupes(auto_ids=True)`, `_compact_synthetic_ids`).

**Date formats — three zones, never mix them:**
- Workbook canonical: `MM/DD/YYYY`
- Picker/API internal: ISO `YYYY-MM-DD`
- UI display: `DD/MM/YYYY` via `fmtDMY()` / `fmtDMYTime()`
- Editable fields (e.g. edit-unit Date In) parse day-first client-side, submit ISO, and `update_unit` re-canonicalizes to `MM/DD/YYYY`. Never `new Date(ambiguousString)` in JS — use `parseDateAny`/`parseDateDMY`.

**Warranty:** `compute_warranty(date_out, months=12)` → expiry shown in UI + tracked on sold units.

**Sidecar files/dirs next to the workbook:** `backups/` (auto snapshot on every save, pruned to 60 + `ready_exports/`), `delivery_orders/` (Recent DO scan photos, auto-purged >3 days), `permanent_do/` (photos copied here when a scan is committed; never auto-purged; names include `DO number`, `SO number`, document date, and scan date/time), `serial_provenance.json` (model/serial links to permanent DO/SO photos), and `ui_prefs.json` (theme, wallpaper, AI model config, API keys).

## 5. Backend specifics

- Global `_store_lock` serializes **all** `/api/` requests — the workbook isn't concurrency-safe; single-operator design so a lock is correct.
- `licenseGate` middleware (in `backend.py`) returns `403 {"ok":false,"error":"license_required","state":…,"machine":…,"detail":…}` for every `/api/*` EXCEPT `/api/license/status` and `/api/license/activate`. Frontend `api()` catches `license_required` → shows gate.
- `/api/scan` → one full-image vision AI request that extracts document metadata (DO/SO number/date/confidence) plus inventory rows; the uploaded image is archived to `delivery_orders/` before scanning and copied to `permanent_do/` when its stock-in batch is committed.
- `/api/config*` → AI engine router (Gemini keys etc.) stored in `ui_prefs.json`.
- Exports: `/api/export/available` (xlsx), `/api/export/sales`, CSV paths for returns/activity — all emit `DD/MM/YYYY`; filenames use `-` separators (`/` is illegal in filenames).

## 6. Desktop shell (`desktop_app.py`)

- Splash drawn with GDI+ (`comet_layer` animated comet) while WebView2 + backend warm up.
- Health check polls **`/api/license/status`** — always 200 even unlicensed. Never point it at a gated endpoint (a 403 used to hang "Starting services…" forever — that bug is fixed; keep it that way).
- `webview.start(...)` guarded by `_webview2_present()` — missing runtime → MessageBox + official bootstrapper link.
- `DesktopApi` bridge (`window.pywebview.api`): `minimize/toggle_maximize/close`, `save_file`, `open_url` (scheme-whitelisted http/https/tg — used by Purchase Renewal → Telegram).
- Exit via `os._exit(0)` — kills the backend thread instantly, frees the port for instant relaunch.

## 7. Licensing — two repos, one keypair

**In-app (`license_check.py`):** `license.lic` + `license_state.json` beside the exe. Key format `VRE1.<b64url payload>.<b64url Ed25519 sig>`; payload `{app:"VRE-STOCK", customer, machine, expires, issued}`. Checks: signature → machine match → expiry → clock-rollback (last-seen date in `license_state.json`). `machine="*"` = master key (emergency only). `VRE_DEV_BYPASS=1` skips enforcement — **ignored when frozen**.

**Machine ID** = Windows `MachineGuid` → hex-16, grouped `XXXX-XXXX-…` (e.g. `C71A-4CBE-…`). `license_tool.py` reimplements the same algorithm — identical output required.

**Generator (NOT in this repo):** `D:\AI-Project\Devin\License key generator\` → `license_tool.py` (PyQt6 GUI, `license-tool.bat`, `menu`/`sign`/`init` CLI), `VRE-License-Generator.exe` + **`license_private.pem`** — the private key never enters any repo/chat; it must sit beside the generator exe. `License exe\` subfolder holds the pair.

**Customer flow:** app boots → status `missing` → gate shows Machine ID → customer clicks Purchase Renewal (copies ID + opens `https://t.me/chh_ck`) → you run the generator exe → send `VRE1.…` → they paste → `/api/license/activate` writes `license.lic` → unlocked. Expiry ≤30d → dismissible banner; expiry hit → gate (still shows reason + lets a new key activate).

**License admin modal** (topbar 🔑): `.licm-card` design — status banner variants `ok/warn/bad`, meta rows, machine-id input, renew textarea, footer buttons. If you edit copy/activate buttons, label text lives in `.copy-label`/`#licm-activate-txt` spans — writing `textContent` on the button destroys its SVG icon.

## 8. Packaging rules (frozen exe)

`sys.frozen` ⇒ all writable paths resolve to **`Path(sys.executable).parent`** — the exe's folder:
- `_resolve_db_path()` adopts the newest `*.xlsx` beside the exe if `daikin_stock.xlsx` is absent (ignores `~$*` lock files) — customers drop their real workbook with any name.
- `license.lic`, `license_state.json`, `ui_prefs.json`, `serial_provenance.json`, `backups/`, `delivery_orders/`, `permanent_do/` all beside the exe → **install folder must be writable** (never Program Files).
- Bundled read-only assets (`ac-stock-tracker.html`, icons) resolve via `sys._MEIPASS` (`BASE` in backend.py).
- `build-exe.bat` handles: `--collect-all cryptography` (bundled .pyd backends), `--collect-submodules webview`, `--hidden-import multipart` (FastAPI lazily imports it for UploadFile — photo upload breaks without it), uvicorn loop/protocol hidden imports.

## 9. Testing & verification

```bash
node test_fulfillment_groups.js        # 73 tests — tracking/fulfillment/date helpers
python -m py_compile backend.py stock_store.py desktop_app.py license_check.py
# embedded-JS syntax check:
node -e "const fs=require('fs');const s=fs.readFileSync('ac-stock-tracker.html','utf8');[...s.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].forEach((x,i)=>{try{new Function(x[1])}catch(e){console.log('script',i,'FAIL:',e.message)}})"
```

Test suite `eval`s extracted functions — when a render helper gains a dependency (e.g. `fmtDMY`), the harness must expose it too.

**License test matrix** (all verified): missing / malformed / tampered-sig / wrong-machine / expired / master / perpetual / live HTTP 403→activate→200.

## 10. Editing conventions & gotchas

- The HTML file stores some chars as **literal `\u2014`/`\u00b7` text** (6 chars, not the glyph) — exact-match edits and regexes must account for it; test the pattern before scripted replaces.
- Theme: `body.theme-light` = Day mode; CSS vars carry the palette (`--brand-ink` = darkened brand color for *text* in Day mode, `--brand-c` stays vivid for dots/borders). Inline JS-generated colors use `style="--brand-c:…"` custom props so theme toggle needs no re-render.
- Global `font-variant-numeric: slashed-zero` (0 vs 8 legibility).
- Custom pickers: `initDatePicker`, 24h `rs-time` time picker (00–23 × 00–59 min), popovers use explicit solid colors (wallpaper mode makes `--bg-app` translucent — never use it for floating panels).
- `localStorage` keys: `lic_warn_hide` (banner dismiss), theme/accent/wallpaper prefs (mirrored to `ui_prefs.json`).
- Port 8000 is single-instance — a stale backend serves new HTML with old API. Kill the process holding the port before relaunching.
- Modals: `.modal-overlay` + `.open` class; only hard gate (`#license-gate`) is a full-screen takeover.

## 11. Release checklist

1. `build-exe.bat` → `dist\VRE AC Stock.exe`
2. Test in a clean folder: exe + customer's `.xlsx` → boots to gate (no license)
3. Generate key with the generator exe (customer's Machine ID) → activate → data loads
4. Ship: exe + xlsx in a writable folder. Warn about SmartScreen (unsigned) — *More info → Run anyway*.

**Never commit/ship:** `license_private.pem`, `license_state.json`, `*.lic`, real customer workbooks.

## 12. Latest session update

- Corrected the DO/SO strip markup so only the two date fields use centered alignment.
- Delivery Order and Sales Order number fields, tags, and boxes remain left-aligned.
- On the Stock In screen only, pressing Enter after loading/pasting an image triggers the Scan action; inputs, buttons, dialogs, and other tabs retain normal Enter behavior.
- Added the Option D frosted-pill Paste button inside the Stock In drop zone. It uses `navigator.clipboard.read()`, reuses `processLoadedPhoto(File)`, shows inline clipboard errors, and does not trigger the drop zone's file browser.
- Desktop Paste now uses a local `DesktopApi.read_clipboard_image()` Pillow bridge first, so the Windows WebView2 permission popup is avoided; browser/non-desktop mode retains the Clipboard API fallback.
- Added Pillow to `requirements.txt` for the local clipboard image bridge.
- Replaced the serial-linked photo viewer's DO/SO toggle with a styled Download button. The viewer now always shows the archived scan image, and desktop downloads use a native Save As dialog with the last-used folder remembered in `ui_prefs.json`; browser fallback uses `showSaveFilePicker()` or Downloads.
- The viewer download preserves the archived file bytes with `shutil.copyfile`, supports cancel without feedback, and shows inline save success/error status that clears when another serial is opened.
- Rebuilt `dist\VRE AC Stock.exe` with the native clipboard bridge on 2026-10-26. SHA-256: `51E976116642FFAFCEC3D02C4E80549F47BB834608A788FBA82490FA6CEF507C`.
- The rebuilt executable was smoke-launched successfully and remained running for 12 seconds before being closed.
- Rebuilt `dist\VRE AC Stock.exe` again on 2026-10-26 after the serial-photo Download/Save As viewer change. SHA-256: `EE124850865740847538D3D759695BD242FA0AA511C19C9F4231EDE7014CA714`.
- The latest executable was smoke-launched successfully and remained running for 12 seconds before being closed.
- Frontend syntax, `git diff --check`, Python compilation, and all 73 regression tests pass.
- The user explicitly requested that Force Scan not be implemented yet; the current version remains the one to use.
- This session pins the current source and built executable after the photo-viewer Download/Save As change.
- Published stable source commit: `2e3762f` (`Finalize photo download build`).
- Published annotated tag: `stable-20261026-photo-download`.
- Pushed to `origin/main` and `origin/stable-20261026-photo-download` at `https://github.com/Ai-mali/Github-Copilot`.

## 13. Continuation prompt for another Copilot account

Copy the prompt below into the next Copilot chat after opening this repository:

> You are continuing work on the **VRE AC Stock** Windows desktop inventory application in this repository. Read `HANDOVER.md` completely before changing anything. Treat the repository files and this handover as the source of truth; do not assume the previous chat is available.
>
> Current stable source/build point: commit `2e3762f`, annotated tag `stable-20261026-photo-download`. The built executable is `dist\VRE AC Stock.exe`; its latest SHA-256 is `EE124850865740847538D3D759695BD242FA0AA511C19C9F4231EDE7014CA714`.
>
> Important current behavior:
> - Stock In scans the full image once and extracts inventory rows plus DO/SO numbers, dates, and confidence.
> - Scanned photos first go to `delivery_orders` (Recent DOs, 3-day retention).
> - When scanned stock is committed, the photo is copied to `permanent_do`, which is never auto-purged.
> - Permanent filenames include DO number, SO number, document date, scan date, and scan time.
> - `serial_provenance.json` links committed model/serial pairs to the permanent photo and DO/SO metadata.
> - Existing legacy provenance filenames may remain in the JSON; preserve compatibility unless explicitly migrating them.
> - Visible dates use `DD/MM/YYYY`; API/picker values use ISO `YYYY-MM-DD`; workbook dates remain `MM/DD/YYYY`.
> - The DO/SO date picker is editable for correcting an OCR result. The date confidence label and date value are centered in the current UI.
>
> Current status and user decision:
> - The current build includes the background local clipboard bridge and the serial-photo viewer Download button with native Save As.
> - Do not implement Force Scan yet. The user's next planned feature is a low-confidence recovery flow: when scan confidence is below 60%, warn or offer Force Scan, then improve extraction with image enlargement, sharpening, contrast/deskew, and targeted DO/SO/model/serial crops or retries. This is only a future requirement, not current behavior.
> - Inspect `git status` and the latest commit/tag before making changes.
>
> Required working rules:
> - Read relevant code before editing and preserve existing behavior.
> - Do not rebuild the executable unless explicitly requested.
> - Run targeted syntax/tests after changes; the normal regression suite is `node test_fulfillment_groups.js` (currently 73 tests).
> - Do not alter the Excel schema for provenance work.
> - Do not expose or commit credentials, private keys, real licenses, or real customer data.
> - If the user asks for a build, build with `build-exe.bat`, smoke-test the executable, report its path and SHA-256, and only then mark the task complete.
>
> Before ending every work session, update this `HANDOVER.md` with:
> 1. what changed,
> 2. what remains unfinished,
> 3. tests/builds run and their results,
> 4. the current commit/tag/build state,
> 5. any user decisions or constraints from that session.
>
> Do not claim completion while any requested change or verification remains unfinished. Use the existing project conventions and keep changes surgical.

## 14. Handover maintenance rule

This file is the persistent cross-account context. **Update it at the end of every future implementation or build session**, including the current working-tree status, latest stable commit/tag, tests, build artifact/checksum when applicable, remaining work, and the next continuation prompt. Keep the continuation prompt aligned with the actual repository state; do not leave stale claims about a build or completed feature.
