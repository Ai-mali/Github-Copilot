# VRE AC Stock - Change Log

Newest first. **Every change adds an entry here and bumps `VERSION`** (one line, no `v`).
Version rule: `MAJOR.MINOR.PATCH` - PATCH = small fix / polish, MINOR = new feature or Excel schema change, MAJOR = big redesign.
The version shows under the app name in the title bar and in the exe file name (`VRE AC Stock v<version>.exe`).

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
