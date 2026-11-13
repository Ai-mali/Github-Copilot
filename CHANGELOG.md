# VRE AC Stock - Change Log

Newest first. **Every change adds an entry here and bumps `VERSION`** (one line, no `v`).
Version rule: `MAJOR.MINOR.PATCH` - PATCH = small fix / polish, MINOR = new feature or Excel schema change, MAJOR = big redesign.
The version shows under the app name in the title bar and in the exe file name (`VRE AC Stock v<version>.exe`).

## 1.4.1 - 2026-11-13
- Changed: Model Catalog window - Category, Type and Pair are now click-to-edit text boxes like HP (click for the suggestion list, or just type). Typing "wall mounted" re-uses the existing "Wall Mounted" group; a new name starts a new group. Tab moves to the next box and edits no longer redraw the table.
- Added: a live "Excel export preview" strip under the table - a mini copy of the export that highlights where the box you are editing lands (Category = grey group heading, Type = Type column, HP = Horse power column, Model + Pair = Model column as INDOOR/OUTDOOR).
- Fixed: a model cannot be its own outdoor partner, or the partner of two models (clear message instead of a save error).

## 1.4.0 - 2026-11-13
- Added: Model Catalog window on Available Stock (new "Catalog" button next to the export buttons) - set each model's Category, Type, HP and outdoor Pair from inside the app instead of editing model_catalog.xlsx by hand. Category / Type / Pair are dropdowns (+ "New category..."), "+ Add model" adds a model that is not in stock yet, tabs "All models" / "Needs category", search box. Save keeps the previous list as model_catalog.bak and writes the new file aside first, so a failed save never damages the catalog (a clear message is shown if the file is open in Excel).
- Added: yellow note on Available Stock ("N models in stock are not categorised yet") with a "Set now" button and a count badge on the Catalog button. It disappears when every in-stock model has a category or is the outdoor partner of a catalogued model.
- Backend: `GET/POST /api/model-catalog`; `model_catalog.save_catalog / validate_entries / uncategorised`. Stock records, Stock In/Out, Return and the existing exports are untouched. Choosing a category cannot be undone from the window (rows are never deleted there).

## 1.3.1 - 2026-11-13
- Fixed: the manual-format Available Stock export now looks like the hand-made sheet: Times New Roman 11 (title 20 bold), black thin borders, Horse power shown as 0.0, dark-red zero Balance, same column widths and row heights, portrait A4 fit-to-width centred printing. Only the Brand column widens when a brand name would be cut off.

## 1.3.0 - 2026-11-13
- Added: Available Stock - second export button "Export Excel (manual format)" next to the normal one. It builds the hand-made layout: groups numbered I, II, III... (no gaps; empty groups left out), columns NO | Type | Model | Horse power | Brand | TOTAL | Booking | Balance, indoor/outdoor sets on one row ("FCC50AV1/RC50AGV1" = number of complete sets), plus the Broken sheet. The normal Export button and the per-brand export are unchanged; the new button hides while brands are ticked.
- Added: `model_catalog.xlsx` (Model | Category | Type | HP | Pair) is created next to the database the first time it is needed, from a built-in list taken from the manual Ending Balance / Available sheets. Edit it any time - it is never overwritten. Models in stock but not in the catalog go to an "Other" group at the bottom with the note "Not in model_catalog.xlsx". New file `model_catalog.py`; backend `GET /api/export/available?layout=manual`.
- Note column appears only when a row needs it (a set with unmatched indoor/outdoor units, or an "Other" model).

## 1.2.0 - 2026-11-12
- Added: Available Stock "Export all" now adds a second sheet "Broken" (NO | SERIAL/DESC | MODEL | CUSTOMER | NOTES) listing every unit that is Quarantined right now. Units released back to stock (Action Taken = Restocked) drop off the list automatically. No Broken sheet when nothing is quarantined. Exporting selected brands does not include it. The automatic backup copy in backups/ready_exports also gets the sheet.

## 1.1.1 - 2026-11-10
- Available Stock: Shift+click selects a range of brands (Ctrl+Shift+click adds a range).

## 1.1.0 - 2026-11-10
- Added: Available Stock - export only the brands you pick. Ctrl+click a brand in the left list (or click its round icon) to tick it: a green check replaces the initials, the right-hand list shows only ticked brands, and the top button becomes "Export N brands" (a small x next to it, or Esc, clears the ticks). With nothing ticked it still exports everything, exactly as before.
- Added: right-click a brand for a compact export menu - one brand: "Export this Brand (N units)"; several ticked brands: "Export Selected (N brands - N units)". Resting the mouse on a round icon for 0.3s shows "Ctrl+Click to Select".
- Added: backend `GET /api/export/available?brand=A&brand=B` - one Excel file with one sheet per brand (brands with no units are skipped; without `brand` the output is unchanged). `excel_exports.build_available_workbook(records, now, brands=None)`.
- Fixed: Ctrl+click / avatar click no longer triggers the brand rename double-click.

## 1.0.6 - 2026-11-05
- Fixed: the green drag-selection box (Available Stock marquee) could get stuck on screen - even across tabs - until the app was restarted, when the mouse button was released outside the window or over the title bar. The box now always ends: on any mouse move with no button held, window blur, tab hidden, drag start, Esc, and when switching tabs.

## 1.0.5 - 2026-11-05
- Fixed: Return tab search box - the ACTIVE / EXPIRING / EXPIRED warranty tag no longer covers the serial/description text; room is reserved for it and long text ends with "...".
- Fixed: Processed Returns Registry - Date In / Date Out / Returned now use the same font, size and colour and are no longer cut off (wider date columns, table scrolls sideways if the panel is very narrow); headers "Serial" and "Returned" fit instead of being truncated.

## 1.0.4 - 2026-11-05
- Changed: Sell Record tab compact spacing - records-log header 50->42px, column header 44->34px, gap between sale blocks 10->6px, sale header strip 32->26px, rows 62->50px, expanded unit rows 44->38px (head 38->32), pagination bar 49->41px. About 20% more sales visible without scrolling.

## 1.0.3 - 2026-11-05
- Changed: the Dispatch & Checkout / Staging Cart split is no longer remembered - it resets to the default (automatic) size every time the app starts. Dragging and double-click reset still work during the session; the 4px gap stays.

## 1.0.2 - 2026-11-05
- Changed: Stock Out right column - the gap between Dispatch & Checkout and Dispatch Staging Cart is now 4px (about 1mm).
- Added: drag that gap up/down to resize the Dispatch & Checkout card (the Staging Cart takes the rest; the checkout form scrolls inside when squeezed, minimum 96px). Double-click the gap to reset to automatic. The size is remembered (`soCheckoutH` in ui_prefs.json). Not active in the narrow stacked layout (<=1120px).

## 1.0.1 - 2026-11-04
- Fixed: Stock In left column dragged to its narrowest - the Status Log title and the All / Iss / OK filters (plus the clear button) now stay on one line instead of wrapping; smaller title/filter text and tighter padding in compact mode only.

## 1.0.0 - 2026-11-04
First versioned release. Everything below is included.
- Added: version label under the app name; `VERSION` + `CHANGELOG.md`; exe is built as `VRE AC Stock v<version>.exe`.
- Added: brand cards (Available Stock, Stock Out sidebars) show the date the brand was **created**. New **Created** column in the Brands sheet; existing brands were backfilled once with their first received date.
- Changed: Stock Out title shows the cart count, e.g. "Stock Out & Dispatch (N units in the Cart)".
- Changed: removed the Available Stock / Stock Out subtitles and the staged-count labels; 10px gap under headers.
- Changed: staged cart cards are equal size (48px) with ellipsis.
- Added: small Paste button inside every search box; removed the Sell Record breakdown/filter card.
- Fixed: Stock In left column width is remembered; drag-and-drop photo zone centered.
- Added: serial photo viewer with smooth zoom/drag; native clipboard read for the Paste button.
