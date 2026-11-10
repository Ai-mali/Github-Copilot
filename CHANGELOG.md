# VRE AC Stock - Change Log

Newest first. **Every change adds an entry here and bumps `VERSION`** (one line, no `v`).
Version rule: `MAJOR.MINOR.PATCH` - PATCH = small fix / polish, MINOR = new feature or Excel schema change, MAJOR = big redesign.
The version shows under the app name in the title bar and in the exe file name (`VRE AC Stock v<version>.exe`).

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
