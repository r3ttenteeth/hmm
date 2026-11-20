# Yuzu Theme for Anki (works on iPad)

A themed set of Anki note types with a settings panel, stats, a heatmap, streaks, a daily goal, a timer and animations. It is built entirely from card templates (HTML, CSS and JavaScript), so it runs in **AnkiMobile on iPad/iPhone**, Anki desktop, AnkiDroid and AnkiWeb.

> **Why it isn't a real add-on:** AnkiMobile can't run add-ons. Card templates are the only thing that syncs to iPad and can run code, so this theme only changes the **review screen**. It can't change the deck list, menus or Anki's own Stats screen.

## Features

| | |
|---|---|
| 🎨 **6 themes** | Yuzu, Matcha, Sakura, Ocean, Lavender, Mono |
| 🌗 **Dark mode** | Follows Anki's night mode automatically, or force Light or Dark |
| 🖼 **Backgrounds** | Aurora, Gradient, Waves, Dots, Grid, Plain, or your own image |
| 🃏 **Card styles** | Raised, Glass (frosted), Flat, Minimal |
| ✨ **Animations** | Pop, Flip, Slide, Fade, None (respects Reduce Motion) |
| 🔤 **Fonts and size** | System, Rounded, Serif, Mono, plus a text-size slider |
| ⏱ **Timer** | Live on the question side, frozen on the answer side |
| 🎯 **Daily goal ring** | Progress toward a goal you set, with confetti when you reach it |
| 📊 **Progress panel** | Today's count and time, current and best streak, cards this session, a 6‑month heatmap and all-time totals |
| 💡 **Tap-to-reveal hints** | Optional `Hint` field (press `H` on a keyboard) |
| 🏷 **Tag chips, Extra field, deck name** | Each one can be switched on or off |

Open the settings with the 🎨 button and the stats with the 📊 button, both at the top of every card.

## Install on iPad (no computer needed)

1. On your iPad, download **[`dist/Yuzu-Theme.apkg`](dist/Yuzu-Theme.apkg)** from GitHub (tap the file, then *Download raw file*). It saves to the Files app.
2. In Files, tap the `.apkg` and choose *Share → AnkiMobile*, or in AnkiMobile tap *Add/Export → Import*.
3. This adds 4 note types and a small sample deck (`Yuzu Theme::Samples`):
   - **Yuzu Basic**: Front, Back, Hint, Extra
   - **Yuzu Basic (and reversed)**
   - **Yuzu Type Answer**
   - **Yuzu Cloze**: Text, Hint, Extra
4. To use the theme with **your existing cards**: *Browse → select the cards → Change Note Type → Yuzu Basic* (or Yuzu Cloze), then match up the fields.

You can also import the file on Anki desktop and sync. The note types will then reach your iPad.

## Theme imported or shared decks (no note-type change)

Shared decks come with their own note types, so they won't look different until you add the snippet below. Do this once per note type, and every card that uses it gets themed, including new ones:

1. Import `Yuzu-Theme.apkg` first. This also installs the theme script (`_yuzu.js`) into your media folder.
2. Open the deck's note type: **desktop:** *Tools → Manage Note Types → (the deck's type) → Cards*. **AnkiMobile:** find *Notetypes* in the settings, pick the type, then *Cards*.
3. Paste at the **very end** of the **Front Template**:
   ```html
   <div class="yz-universal" data-side="front" style="display:none"><span class="yz-u-deck">{{Deck}}</span><span class="yz-u-tags">{{Tags}}</span></div>
   <script src="_yuzu.js"></script>
   ```
4. Paste at the **very end** of the **Back Template** (only `front` changes to `back`):
   ```html
   <div class="yz-universal" data-side="back" style="display:none"><span class="yz-u-deck">{{Deck}}</span><span class="yz-u-tags">{{Tags}}</span></div>
   <script src="_yuzu.js"></script>
   ```
5. If the note type has several card types (e.g. *Recognition* and *Production*), repeat steps 3–4 for each one.
6. Save and sync.

You don't need to change **Styling**: the theme adds its own CSS. The deck's own content and layout stay the same, wrapped inside the themed card. To undo, delete the pasted lines.

**If the short snippet shows nothing new** (e.g. `_yuzu.js` didn't sync to the device), paste the contents of `dist/universal/front-full.html` and `back-full.html` instead. They include the whole theme and don't need the media file.

## Install by copy-paste (keep your own note type)

Use **Manage Note Types → (your type) → Cards** and paste in:
- `dist/templates/<Type>/card1_front.html` → Front Template
- `dist/templates/<Type>/card1_back.html` → Back Template
- `dist/templates/<Type>/styling.css` → Styling

The templates expect the field names `Front`, `Back`, `Hint` and `Extra` (or `Text` for cloze). Rename them in the templates if yours are different. `Hint` and `Extra` are optional.

## Notes and limits

- **Settings and theme stats are saved on each device** (the browser storage inside Anki), so set your theme once on iPad and once on desktop. If iOS clears the app's web data, the theme's stats reset. Anki's own review history is never touched.
- Theme stats count each time you **reveal an answer on a Yuzu card**. Cards on other note types aren't counted.
- The timer starts when the question appears. Time per card is capped at 5 minutes so that leaving a card open doesn't skew the average.
- **Background image:** paste an `https://` URL (needs internet), or put a file named something like `_yuzu_bg.jpg` in your media folder and type its file name. (Media names starting with `_` aren't removed by *Check Media*.)
- **Day rollover** uses the "New day starts at" hour in the settings panel (default 4 AM, the same as Anki's default).

## Building from source

```bash
pip install genanki
python3 build.py      # writes dist/Yuzu-Theme.apkg and dist/templates/
```

Edit `theme/styling.css` and `theme/yuzu.js`. Don't put two opening curly braces in a row in either file, because Anki reads that as a field. The build checks for this.

Re-importing an updated `.apkg` updates the same note types, because their IDs are fixed.
