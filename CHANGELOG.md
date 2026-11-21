# VRE AC Stock - Change Log

Newest first. **Every change adds an entry here and bumps `VERSION`** (one line, no `v`).
Version rule: `MAJOR.MINOR.PATCH` - PATCH = small fix / polish, MINOR = new feature or Excel schema change, MAJOR = big redesign.
The version shows under the app name in the title bar and in the exe file name (`VRE AC Stock v<version>.exe`).

## 1.4.26 - 2026-11-21
- Changed: Available pair hover line now starts with "Pair:" and says "1 set" / "N sets"; in the serial hover tooltip the "Pair: <partner model>" line sits on a dark background (amber "Pair:", white model name) so it is easy to read.

## 1.4.25 - 2026-11-21
- Changed: the Available pair hover line now follows the mouse along the model row (flips to the left near the right edge) and always uses a dark box with high-contrast text, so it is readable in light and dark theme.

## 1.4.24 - 2026-11-21
- Added: Available Stock - indoor / outdoor pairs from the Model Catalog. Hover a model row that has a pair to see one small line on that row: partner model, complete sets (the smaller of the two stocks) and, only when something is left over, "+3 indoor" / "+5 outdoor"; the serial hover now also shows an amber "Pair: <partner model>" line. A small link icon marks the rows that have a pair; models without a pair show nothing. Rows are not merged.

## 1.4.23 - 2026-11-16
- Changed: search suggestions (history) are now kept per search bar instead of one shared list: the brand bars (Available, Stock Out sidebars) suggest brands only, the customer bar (Sell Record sidebar) customers only, the "Serial or model" bars serials / models only; the Sell Record, Return and Activity bars (which also take customers) each keep their own list. The old shared history is sorted once into these lists (known brand / customer names go to the brand / customer bars, the rest to serial / model).

## 1.4.22 - 2026-11-15
- Changed: Return screen - the customer name now has its own full-width row under Date In / Date Out, so long names (e.g. NATIONAL ASSEMBLY) are shown in full instead of being cut off.
- Removed: the "View dispatch log" link above the serial search on the Return screen.

## 1.4.21 - 2026-11-15
- Added: Sell Record - tick customers for export like the Available brands: Ctrl+Click, Shift+Click (range) or click the round icon (hover hint after 0.3s). Ticked customers show a green check and the table shows only them. Right-click a customer for the export menu ("Export this Customer" / "Export Selected"). The export button turns green "Export N customers" and gives ONE Excel file with one sheet per customer (all of that customer's records). Esc or the small x clears the ticks. Exports are logged in Activity History.
- Removed: the small warranty-status dot on the customer round icons in the Sell Record sidebar.

## 1.4.20 - 2026-11-15
- Changed: Sell Record - the Destination header and the customer names are centered in their column (like the other columns), and the customer name font is a little smaller (12px -> 11px). Same in the expanded unit list.

## 1.4.19 - 2026-11-15
- Changed: Sell Record - the (BRAND) tag now sits under the model name instead of beside it, so a long model name and its brand are both shown in full (e.g. MTD 200-FLOW 690M3/H + KRUGER FAN).
- Changed: Sell Record - Date in / Dispatched / Warranty columns have a fixed width, so the gaps between them are smaller and the spare width goes to Model and Destination.

## 1.4.18 - 2026-11-15
- Changed: Sell Record table for the small laptop screen - Date in / Dispatched / Warranty / Quantity / Status columns are narrower and the freed width goes to Model and Destination (customer name), so names are cut off far less; the table no longer needs a horizontal scroll at 1280px.
- Changed: Sell Record warranty shows a green (amber / red) dot plus the days ("364 days") instead of the word "Active"; hover the cell for the state and expiry date.
- Changed: the small (BRAND) tag after the model name shrinks first, so the model name stays readable.

## 1.4.17 - 2026-11-15
- Added: Activity History now records every Model Catalog save as a "Catalog Edited" entry listing what was added, changed (Category / Type / HP / Pair, old -> new) and removed. A save that changes nothing is not logged.

## 1.4.16 - 2026-11-15
- Changed: Available toolbar - the three buttons are icon-only at every window width, in this order: Group Export (box with arrow out), Modify the Category (circular arrows, orange number = models still needing a category), Standard Export (download tray). Tooltips name each one. While brands are ticked the green button still shows "Export N brands".

## 1.4.15 - 2026-11-15
- Added: Activity History now records every Available Stock export (standard, manual format, per-brand) and every Sell Records export as an "Export" entry (what, layout / brands, file name, units). Exports do not create a backup snapshot.

## 1.4.14 - 2026-11-15
- Fixed: Model Catalog window - Save is locked only by a Wall Mounted, Ceiling Cassette or Conceal Duct row whose Category or Pair you changed and that has no pair. Other categories (Panel, VRV FCU Wall Mounted, ...) and old rows you have not touched never lock Save.

## 1.4.13 - 2026-11-15
- Changed: Model Catalog window - Save is locked (greyed out) while a Wall Mounted, Ceiling Cassette or Conceal Duct model has no pair. The row shows "needs a pair" with a red Pair box, and "Save locked: N models need a pair" appears in the footer (click it to jump to the row). Give it a pair or change its category (e.g. Other) to unlock Save.

## 1.4.12 - 2026-11-15
- Changed: manual-format export - inside every group the rows are ordered by Type: Inverter first, then other types, Non inverter last (catalog order inside each). Rows with extra indoor/outdoor units now stay in their place instead of moving to the bottom; the Note column is unchanged.

## 1.4.11 - 2026-11-14
- Changed: manual-format export - inside each group the complete indoor/outdoor sets come first; sets with extra indoor or outdoor units move to the bottom of the group (highest balance first), so the clean rows read together.
- Changed: Wall Mounted, Ceiling Cassette and Conceal Duct only list models that have a pair in `model_catalog.xlsx`; a model without a pair goes to the "Other" group (with a note) until you set its pair in the Model Catalog window.

## 1.4.10 - 2026-11-13
- Changed: manual-format export - the Note column uses the same font and colour as the rest of the table (Times New Roman 11, black; header bold black) instead of grey italic. Still outside the print area.

## 1.4.9 - 2026-11-13
- Changed: manual-format Available Stock export - the table now ends at Balance: the title bar spans NO. to Balance and the print area is A:H, so the Note column (kept for your own eyes, shown without fill or borders) is not printed.

## 1.4.8 - 2026-11-13
- Changed: Model Catalog - a suggestion you forget with its x is only hidden until the program is closed; every suggestion comes back at the next start (nothing is saved any more). Reopening the window in the same session keeps it hidden. An old `catalogHiddenSuggestions` entry left in ui_prefs.json by v1.4.6/1.4.7 is simply ignored.

## 1.4.7 - 2026-11-13
- Changed: the Pair (outdoor) box in the Model Catalog now uses the same suggestion list as Category and Type, with an x on each suggestion to forget it (stored in ui_prefs.json like the others; models and the catalog file are not touched). Models that cannot be paired (itself, already someone's outdoor unit) are not offered; models still needing a category are listed first.

## 1.4.6 - 2026-11-13
- Fixed: the x on a Model Catalog suggestion now only forgets that suggestion (it disappears from the list and stays gone after restarts, remembered in ui_prefs.json as `catalogHiddenSuggestions`). It no longer touches any model: no confirmation, nothing sent back to "Needs category". Typing or choosing the name again brings it back. The x inside a box (clears that model's own value) is unchanged.

## 1.4.5 - 2026-11-13
- Added: Model Catalog - a small x inside the Category, Type and Pair boxes (shows when the box has text; click to empty it). Clearing the Category of an already-catalogued model asks first and sends it back to "Needs category" (its Type/HP/Pair are dropped on Save).
- Added: Category and Type now use their own suggestion list (instead of the browser's) with an x on every suggestion to remove it. Removing a suggestion that models still use asks first: for a category those models go back to "Needs category", for a type their Type is emptied. "Inverter" and "Non inverter" are always offered, so they have no x.
- Changed: the suggestion list shows everything when you open the box and filters while you type; the current value is highlighted; arrow keys + Enter work; the first Esc closes the list, the next closes the window.

## 1.4.4 - 2026-11-13
- Fixed: Model Catalog tabs no longer mix - "All models" lists only models that already have a category (its count now matches), "Needs category" lists only the ones still to do. A model you just categorised stays in "Needs category" until you press Save, then it moves to "All models".

## 1.4.3 - 2026-11-13
- Changed: Model Catalog opens on "Needs category" by default (when anything still needs a category), and in the "All models" tab the models that still need a category are listed first.
- Changed: the Excel preview now shows live numbers instead of placeholders: the real Brand, TOTAL, Booking and Balance of the model (an indoor/outdoor set shows the number of complete sets, like the export), and they update when you change the Pair.
- Backend: `GET /api/model-catalog` returns `stock_info` (brand / stock / booked per model) instead of `stocked`; `model_catalog.stock_info()` replaces `stocked_models()`.

## 1.4.2 - 2026-11-13
- Fixed: Model Catalog Excel preview now shows the real group number (e.g. "III Multi Split CU"). It follows the export: groups are numbered in catalog order and groups with no stock are skipped, so a new category shows the next number after the existing groups. The preview table also stretches to the full width of the window, with the export's column proportions.
- Backend: `GET /api/model-catalog` also returns `stocked` (names of models in stock/booked) for the numbering; `model_catalog.stocked_models()`.

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
