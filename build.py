#!/usr/bin/env python3
"""Build the Yuzu Theme note types.

Outputs (in dist/):
  Yuzu-Theme.apkg          -> import on iPad (AnkiMobile) or desktop; contains 4 note types + sample deck
  templates/<NoteType>/    -> front.html, back.html, styling.css for copy-pasting into an existing note type

Requires: pip install genanki
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
THEME = ROOT / "theme"
DIST = ROOT / "dist"

CSS = (THEME / "styling.css").read_text()
JS = (THEME / "yuzu.js").read_text()
assert "{{" not in JS and "{{" not in CSS, "'{{' would be parsed by Anki as a field"
SCRIPT = f"<script>\n{JS}\n</script>"

# Universal mode: CSS travels inside the JS so one paste themes any note type.
import json
UNIVERSAL_JS = f"var YZ_CSS = {json.dumps(CSS)};\n{JS}"
assert "{{" not in UNIVERSAL_JS and "</script" not in UNIVERSAL_JS


def marker(side):
    return (f'<div class="yz-universal" data-side="{side}" style="display:none">'
            '<span class="yz-u-deck">{{Deck}}</span><span class="yz-u-tags">{{Tags}}</span></div>')


def universal_snippet(side, inline):
    body = f"<script>\n{UNIVERSAL_JS}\n</script>" if inline else '<script src="_yuzu.js"></script>'
    return f"\n<!-- Yuzu Theme (universal) -->\n{marker(side)}\n{body}\n"

TOP_BAR = """<div class="yz-top">
  <div class="yz-deck">{{Deck}}</div>
  <span class="yz-pill" id="yz-timer">⏱ 0:00</span>
  <span class="yz-pill" id="yz-goal"><svg class="yz-ring" viewBox="0 0 22 22"><circle class="bg" cx="11" cy="11" r="9"/><circle class="fg" cx="11" cy="11" r="9"/></svg><span id="yz-goal-n">0</span></span>
  <button class="yz-btn" data-yz="stats" aria-label="Progress">📊</button>
  <button class="yz-btn" data-yz="settings" aria-label="Appearance">🎨</button>
</div>"""


def hint(field):
    return (f'{{{{#{field}}}}}<div class="yz-hint"><span class="yz-hint-label">💡 Tap for hint</span>'
            f'<span class="yz-hint-body">{{{{{field}}}}}</span></div>{{{{/{field}}}}}')


TAGS = '{{#Tags}}<div class="yz-tags">{{Tags}}</div>{{/Tags}}'


def extra(field="Extra"):
    return f'{{{{#{field}}}}}<div class="yz-extra">{{{{{field}}}}}</div>{{{{/{field}}}}}'


def front(q_html, label="Question"):
    return f"""<div class="yz-wrap">
{TOP_BAR}
<div class="yz-face yz-q-face yz-anim">
  <div class="yz-label">{label}</div>
  <div class="yz-q">{q_html}</div>
  {hint("Hint")}
</div>
</div>
{SCRIPT}"""


def back_after_front(a_html, label="Answer"):
    # Script comes along with {{FrontSide}}; it detects #yz-back and switches to answer mode.
    return f"""{{{{FrontSide}}}}
<div class="yz-wrap" id="yz-back">
<div class="yz-face yz-a yz-anim">
  <div class="yz-label">{label}</div>
  <div class="yz-a-content">{a_html}</div>
  {extra()}
  {TAGS}
</div>
</div>"""


NOTE_TYPES = {
    "Yuzu Basic": {
        "fields": ["Front", "Back", "Hint", "Extra"],
        "templates": [("Card 1", front("{{Front}}"), back_after_front("{{Back}}"))],
    },
    "Yuzu Basic (and reversed)": {
        "fields": ["Front", "Back", "Hint", "Extra"],
        "templates": [
            ("Card 1", front("{{Front}}"), back_after_front("{{Back}}")),
            ("Card 2", front("{{Back}}"), back_after_front("{{Front}}")),
        ],
    },
    "Yuzu Type Answer": {
        "fields": ["Front", "Back", "Hint", "Extra"],
        "templates": [(
            "Card 1",
            front('{{Front}}<div style="margin-top:16px">{{type:Back}}</div>'),
            # type-answer must render its comparison on the back, so don't reuse FrontSide's input
            f"""<div class="yz-wrap">
{TOP_BAR}
<div class="yz-face yz-q-face yz-anim"><div class="yz-label">Question</div><div class="yz-q">{{{{Front}}}}</div></div>
</div>
<div class="yz-wrap" id="yz-back">
<div class="yz-face yz-a yz-anim"><div class="yz-label">Answer</div>
<div class="yz-a-content">{{{{type:Back}}}}</div>{extra()}{TAGS}</div>
</div>
{SCRIPT}""",
        )],
    },
    "Yuzu Cloze": {
        "fields": ["Text", "Hint", "Extra"],
        "cloze": True,
        "templates": [(
            "Cloze",
            front("{{cloze:Text}}", label="Fill in"),
            f"""<div class="yz-wrap">
{TOP_BAR}
<div class="yz-face yz-q-face" id="yz-back">
  <div class="yz-label">Answer</div>
  <div class="yz-q">{{{{cloze:Text}}}}</div>
  {extra()}
  {TAGS}
</div>
</div>
{SCRIPT}""",
        )],
    },
}

# Stable IDs so re-importing updates the same note types instead of duplicating them.
IDS = {"Yuzu Basic": 1733000001, "Yuzu Basic (and reversed)": 1733000002,
       "Yuzu Type Answer": 1733000003, "Yuzu Cloze": 1733000004}
DECK_ID = 1733000100

SAMPLES = {
    "Yuzu Basic": [
        ["What is the capital of Japan?", "Tokyo", "Starts with T", "Capital since 1868."],
        ["<b>柚子</b> (yuzu) is a…", "Citrus fruit", "Think winter baths in Japan", ""],
        ["Spaced repetition works because of…", "The spacing effect", "", "Ebbinghaus, 1885"],
    ],
    "Yuzu Basic (and reversed)": [["抹茶", "Matcha (powdered green tea)", "", ""]],
    "Yuzu Type Answer": [["Type the chemical symbol for gold", "Au", "Latin: aurum", ""]],
    "Yuzu Cloze": [["The {{c1::mitochondria}} is the {{c2::powerhouse}} of the cell.", "Biology classic", ""]],
}


def write_templates():
    for name, nt in NOTE_TYPES.items():
        d = DIST / "templates" / name.replace(" ", "_").replace("(", "").replace(")", "")
        d.mkdir(parents=True, exist_ok=True)
        (d / "styling.css").write_text(CSS)
        for tname, q, a in nt["templates"]:
            slug = tname.lower().replace(" ", "")
            (d / f"{slug}_front.html").write_text(q)
            (d / f"{slug}_back.html").write_text(a)


def write_universal():
    d = DIST / "universal"
    d.mkdir(parents=True, exist_ok=True)
    (DIST / "_yuzu.js").write_text(UNIVERSAL_JS)
    for side in ("front", "back"):
        (d / f"{side}-short.html").write_text(universal_snippet(side, inline=False))
        (d / f"{side}-full.html").write_text(universal_snippet(side, inline=True))


def write_apkg():
    import genanki

    deck = genanki.Deck(DECK_ID, "Yuzu Theme::Samples")
    for name, nt in NOTE_TYPES.items():
        model = genanki.Model(
            IDS[name], name,
            fields=[{"name": f} for f in nt["fields"]],
            templates=[{"name": t, "qfmt": q, "afmt": a} for t, q, a in nt["templates"]],
            css=CSS,
            model_type=genanki.Model.CLOZE if nt.get("cloze") else genanki.Model.FRONT_BACK,
        )
        for fields in SAMPLES[name]:
            deck.add_note(genanki.Note(model=model, fields=fields, tags=["yuzu-sample"]))
    pkg = genanki.Package(deck)
    pkg.media_files = [str(DIST / "_yuzu.js")]  # lets the short universal snippet load the theme from media
    pkg.write_to_file(DIST / "Yuzu-Theme.apkg")


if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    write_templates()
    write_universal()
    write_apkg()
    print("Built", DIST / "Yuzu-Theme.apkg")
