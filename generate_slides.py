"""
Generates Samia's slides matching the team presentation design exactly.

Team design tokens (extracted from TFL_Pipeline_Presentation.pptx):
  BG           #F4F6F9  slide background
  TITLE_BAR    #0019A8  full-width top bar h=1.0"
  TITLE_TEXT   white 30pt bold at (0.4, 0.15)
  SECTION_BAR  #0055CC  sub-header bar h=0.45"
  SECTION_TEXT white 18pt bold
  CARD_BG      #E8F0FE  panel background
  CARD_ALT     #F0F4FF  alternating row
  CARD_HDR     #0055CC  card header stripe h=0.38"
  CARD_HDR_T   white 14pt bold
  CARD_BODY    white 12-15pt  OR  #1A1A2E on light bg
  DIM_HDR      #004499  dimension table header
  FACT_HDR     #DC241F  fact table header
  BADGE_BAR    #0055CC  tech-badge pill at bottom
  BODY_TEXT    #1A1A2E
  GOLD         #FFC000  highlight
  CODE_BG      #1A1A2E  dark code panel
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Design tokens ─────────────────────────────────────────────────────────────
BG          = RGBColor(0xF4, 0xF6, 0xF9)
TITLE_BAR   = RGBColor(0x00, 0x19, 0xA8)
SECTION_BAR = RGBColor(0x00, 0x55, 0xCC)
CARD_BG     = RGBColor(0xE8, 0xF0, 0xFE)
CARD_ALT    = RGBColor(0xF0, 0xF4, 0xFF)
CARD_HDR    = RGBColor(0x00, 0x55, 0xCC)
DIM_HDR     = RGBColor(0x00, 0x44, 0x99)
FACT_HDR    = RGBColor(0xDC, 0x24, 0x1F)
CODE_BG     = RGBColor(0x1A, 0x1A, 0x2E)
BODY_TEXT   = RGBColor(0x1A, 0x1A, 0x2E)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
GOLD        = RGBColor(0xFF, 0xC0, 0x00)
GREEN       = RGBColor(0x00, 0x88, 0x44)
TEAL        = RGBColor(0x00, 0x88, 0x88)
LIGHT_GREY  = RGBColor(0xCC, 0xD6, 0xE0)
CODE_TEXT   = RGBColor(0xAD, 0xE5, 0xFF)

# Slide dimensions
W = Inches(13.33)
H = Inches(7.50)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

# ── Primitive helpers ──────────────────────────────────────────────────────────
def rect(slide, l, t, w, h, fill, line_color=None):
    s = slide.shapes.add_shape(1, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line_color:
        s.line.color.rgb = line_color; s.line.width = Pt(0.5)
    else:
        s.line.fill.background(); s.line.width = 0
    return s

def tb(slide, text, l, t, w, h,
       size=14, bold=False, color=BODY_TEXT,
       align=PP_ALIGN.LEFT, italic=False, wrap=True):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf  = box.text_frame; tf.word_wrap = wrap
    p   = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return box

def tb_multi(slide, lines, l, t, w, h,
             size=12, bold=False, color=BODY_TEXT,
             align=PP_ALIGN.LEFT, line_spacing=1.0):
    """Multi-line textbox — each item in lines is a string."""
    box = slide.shapes.add_textbox(l, t, w, h)
    tf  = box.text_frame; tf.word_wrap = True
    for i, text in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(2)
        run = p.add_run(); run.text = text
        run.font.size  = Pt(size)
        run.font.bold  = bold
        run.font.color.rgb = color
    return box

# ── Compound helpers ───────────────────────────────────────────────────────────
def slide_chrome(slide, title, subtitle=None):
    """Background + title bar (matches team exactly)."""
    rect(slide, 0, 0, W, H, fill=BG)
    rect(slide, 0, 0, W, Inches(1.0), fill=TITLE_BAR)
    tb(slide, title,
       Inches(0.4), Inches(0.15), Inches(12.5), Inches(0.7),
       size=30, bold=True, color=WHITE)
    if subtitle:
        tb(slide, subtitle,
           Inches(0.4), Inches(0.72), Inches(12.5), Inches(0.28),
           size=12, color=RGBColor(0xE8, 0xF0, 0xFE), italic=True)

def section_bar(slide, text, t):
    """Blue section header bar (like team's #0055CC bars)."""
    rect(slide, Inches(0.4), t, Inches(12.5), Inches(0.42), fill=SECTION_BAR)
    tb(slide, text,
       Inches(0.55), t + Inches(0.04), Inches(12.2), Inches(0.38),
       size=16, bold=True, color=WHITE)

def card_box(slide, l, t, w, h, header_text, body_lines,
             hdr_color=CARD_HDR, bg_color=CARD_BG, body_size=11):
    """Card with coloured header strip + body text."""
    rect(slide, l, t, w, h, fill=bg_color)
    rect(slide, l, t, w, Inches(0.36), fill=hdr_color)
    tb(slide, header_text,
       l + Inches(0.1), t + Inches(0.04), w - Inches(0.2), Inches(0.3),
       size=13, bold=True, color=WHITE)
    if body_lines:
        tb_multi(slide, body_lines,
                 l + Inches(0.12), t + Inches(0.4), w - Inches(0.22),
                 h - Inches(0.44), size=body_size, color=BODY_TEXT)

def tech_badges(slide, tags):
    """Row of small blue pills at the bottom (y=6.5)."""
    x = Inches(0.4)
    for tag in tags:
        w = Inches(len(tag) * 0.11 + 0.3)
        rect(slide, x, Inches(6.52), w, Inches(0.36), fill=SECTION_BAR)
        tb(slide, tag, x + Inches(0.08), Inches(6.55),
           w - Inches(0.1), Inches(0.3), size=11, bold=True, color=WHITE)
        x += w + Inches(0.12)


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Agenda  (no title slide; team title is slide 1 of the merged deck)
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "What I'll Cover — PostgreSQL to HDFS",
             "Starting point: data is already loaded and validated in PostgreSQL")

items = [
    ("01", FACT_HDR,    "What's Already in PostgreSQL",
     "Star schema — 6 tables, 5,812 validated records ready to move"),
    ("02", SECTION_BAR, "Step 1 — Sqoop: PostgreSQL to HDFS",
     "Bulk JDBC transfer to the Hadoop distributed file system"),
    ("03", SECTION_BAR, "HDFS Landing Zone",
     "How the raw data is stored on the cluster after Sqoop"),
    ("04", GREEN,       "Key Design Decisions & Results",
     "Why each tool was chosen, and what was successfully delivered"),
]

for i, (num, color, title, desc) in enumerate(items):
    row_t = Inches(1.15) + i * Inches(1.1)
    rect(sl, Inches(0.4), row_t, Inches(12.5), Inches(1.0), fill=CARD_BG)
    rect(sl, Inches(0.4), row_t, Inches(0.6), Inches(1.0), fill=color)
    tb(sl, num,
       Inches(0.4), row_t + Inches(0.3), Inches(0.6), Inches(0.4),
       size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb(sl, title,
       Inches(1.15), row_t + Inches(0.1), Inches(4.5), Inches(0.38),
       size=15, bold=True, color=BODY_TEXT)
    tb(sl, desc,
       Inches(1.15), row_t + Inches(0.52), Inches(11.5), Inches(0.38),
       size=12, color=RGBColor(0x33, 0x33, 0x66))

tech_badges(sl, ["Sqoop", "HDFS", "Jenkins", "TEXTFILE", "MapReduce"])


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Pipeline Architecture (my section)
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "Pipeline Architecture — My Section",
             "PostgreSQL is the starting point — this slide shows what I own")

# Flow boxes — same style as team slide 3
boxes = [
    (Inches(0.4),  "PostgreSQL\nSource DB",    "testdb\n13.42.152.118",        FACT_HDR),
    (Inches(3.05), "Apache\nSqoop",            "JDBC import\nto HDFS",         GREEN),
    (Inches(5.7),  "HDFS\nRaw Data",           "/tmp/tfl_project\n_hadoop/",    TITLE_BAR),
    (Inches(8.35), "Hive\ntfl_db",             "External\nTables",             RGBColor(0x88, 0x24, 0xAA)),
    (Inches(10.9), "Spark /\nCurated Layer",   "Teammates'\nsection",          RGBColor(0x44, 0x88, 0x00)),
]
BOX_W = Inches(2.35); BOX_H = Inches(1.7); BOX_T = Inches(1.3)

for idx, (l, label, sub, color) in enumerate(boxes):
    rect(sl, l, BOX_T, BOX_W, BOX_H, fill=color)
    tb_multi(sl, [label],
             l + Inches(0.1), BOX_T + Inches(0.15), BOX_W - Inches(0.2),
             Inches(0.7), size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb_multi(sl, [sub],
             l + Inches(0.1), BOX_T + Inches(0.9), BOX_W - Inches(0.2),
             Inches(0.7), size=11, color=RGBColor(0xFF, 0xFF, 0xAA),
             align=PP_ALIGN.CENTER)
    if idx < 4:
        ax = l + BOX_W + Inches(0.04)
        tb(sl, "->", ax, BOX_T + Inches(0.6), Inches(0.25), Inches(0.5),
           size=20, bold=True, color=TITLE_BAR, align=PP_ALIGN.CENTER)

# "MY SECTION" underline bracket
rect(sl, Inches(0.4), BOX_T + BOX_H + Inches(0.12),
     Inches(8.25), Inches(0.06), fill=GOLD)
tb(sl, "YOUR SECTION  (Slides 4 - 13)",
   Inches(1.5), BOX_T + BOX_H + Inches(0.22), Inches(6.0), Inches(0.35),
   size=12, bold=True, color=BODY_TEXT)

# "Data already here" callout
rect(sl, Inches(0.4), BOX_T - Inches(0.5), Inches(2.35), Inches(0.42),
     fill=GOLD)
tb(sl, "Data already loaded here",
   Inches(0.45), BOX_T - Inches(0.46), Inches(2.25), Inches(0.36),
   size=10, bold=True, color=BODY_TEXT, align=PP_ALIGN.CENTER)

# Section sub-header and HDFS layout
section_bar(sl, "HDFS Directory Layout (after Sqoop)", Inches(3.3))
tb_multi(sl, [
    "/tmp/tfl_project_hadoop/dim_networks_full_load/       part-m-00000  (1 row)",
    "/tmp/tfl_project_hadoop/dim_lines_full_load/          part-m-00000  (14 rows)",
    "/tmp/tfl_project_hadoop/dim_stations_full_load/       part-m-00000  (436 rows)",
    "/tmp/tfl_project_hadoop/fact_passenger_entry_exit_full_load/  part-m-00000  (4,771 rows)",
], Inches(0.5), Inches(3.82), Inches(12.3), Inches(2.55),
   size=12, color=BODY_TEXT)

tech_badges(sl, ["Sqoop", "HDFS", "Hive", "beeline", "MapReduce"])


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — What's Already in PostgreSQL
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "Starting Point — What's Already in PostgreSQL",
             "13.42.152.118:5432 / testdb  |  Star schema  |  5,812 validated records")

section_bar(sl, "6 Tables — Dimension + Fact", Inches(1.1))

tables = [
    ("dim_date",                  "15",    "Annual time periods 2007 - 2021",             DIM_HDR,  CARD_BG),
    ("dim_lines",                 "14",    "Tube/rail lines with official colours",        DIM_HDR,  CARD_ALT),
    ("dim_networks",              "1",     "Network type (Underground / Rail)",            DIM_HDR,  CARD_BG),
    ("dim_stations",              "436",   "Station master — Night Tube, DLR, Overground flags", DIM_HDR, CARD_ALT),
    ("fact_station_lines",        "575",   "Bridge — many-to-many station to line mapping", FACT_HDR, CARD_BG),
    ("fact_passenger_entry_exit", "4,771", "Core fact — annual entry/exit counts per station", FACT_HDR, CARD_ALT),
]

# Header row
HDR_T = Inches(1.65)
rect(sl, Inches(0.4), HDR_T, Inches(4.2), Inches(0.38), fill=DIM_HDR)
rect(sl, Inches(4.65), HDR_T, Inches(1.1), Inches(0.38), fill=DIM_HDR)
rect(sl, Inches(5.8),  HDR_T, Inches(7.1), Inches(0.38), fill=DIM_HDR)
for text, l, w in [("Table Name", 0.5, 4.0), ("Records", 4.65, 1.0), ("Description", 5.9, 6.9)]:
    tb(sl, text, Inches(l), HDR_T + Inches(0.04), Inches(w), Inches(0.3),
       size=12, bold=True, color=WHITE)

ROW_H = Inches(0.73)
for i, (name, cnt, desc, hdr, bg) in enumerate(tables):
    row_t = Inches(2.05) + i * ROW_H
    rect(sl, Inches(0.4),  row_t, Inches(4.2), ROW_H, fill=bg)
    rect(sl, Inches(4.65), row_t, Inches(1.1), ROW_H, fill=bg)
    rect(sl, Inches(5.8),  row_t, Inches(7.1), ROW_H, fill=bg)
    rect(sl, Inches(0.4),  row_t, Inches(0.06), ROW_H, fill=hdr)
    tb(sl, name, Inches(0.55), row_t + Inches(0.2), Inches(4.0), Inches(0.4),
       size=12, bold=True, color=hdr)
    tb(sl, cnt, Inches(4.65), row_t + Inches(0.2), Inches(1.0), Inches(0.4),
       size=13, bold=True, color=BODY_TEXT, align=PP_ALIGN.CENTER)
    tb(sl, desc, Inches(5.9), row_t + Inches(0.2), Inches(6.8), Inches(0.4),
       size=12, color=BODY_TEXT)

tb(sl, "Blue = Dimension table    Red = Fact table    "
       "All FK constraints enforced at DB level    10 indexes    4 views",
   Inches(0.4), Inches(6.6), Inches(12.5), Inches(0.32),
   size=10, color=RGBColor(0x55, 0x55, 0x88), italic=True)


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Star Schema Diagram
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "PostgreSQL — Star Schema We Are Moving",
             "2 fact tables  |  4 dimension tables  |  FK-enforced  |  ready for Sqoop")

def schema_box(slide, l, t, w, h, title, cols, hdr_color):
    rect(slide, l, t, w, h, fill=WHITE, line_color=hdr_color)
    rect(slide, l, t, w, Inches(0.33), fill=hdr_color)
    tb(slide, title,
       l + Inches(0.1), t + Inches(0.04), w - Inches(0.2), Inches(0.26),
       size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb_multi(slide, cols,
             l + Inches(0.1), t + Inches(0.37), w - Inches(0.2),
             h - Inches(0.42), size=9, color=BODY_TEXT)

# Centre: fact_passenger_entry_exit
schema_box(sl, Inches(4.5), Inches(1.3), Inches(4.3), Inches(3.1),
           "fact_passenger_entry_exit",
           ["entry_exit_id  PK",
            "station_id     FK",
            "date_id        FK",
            "total_entry_exit",
            "estimated_entries",
            "estimated_exits",
            "record_type / data_source"], FACT_HDR)

# Bottom centre: bridge
schema_box(sl, Inches(4.5), Inches(4.7), Inches(4.3), Inches(1.55),
           "fact_station_lines  (bridge)",
           ["station_line_id  PK",
            "station_id FK    line_id FK",
            "is_interchange   effective_from"], FACT_HDR)

# Left: dim_stations
schema_box(sl, Inches(0.3), Inches(1.3), Inches(3.8), Inches(3.0),
           "dim_stations",
           ["station_id  PK",
            "station_name",
            "network_id  FK",
            "has_night_tube  BOOL",
            "has_dlr / has_overground",
            "is_active"], DIM_HDR)

# Right: dim_date
schema_box(sl, Inches(9.1), Inches(1.3), Inches(3.8), Inches(2.3),
           "dim_date",
           ["date_id  PK",
            "year   quarter   month",
            "is_annual  BOOL",
            "period_label",
            "period_start / period_end"], DIM_HDR)

# Bottom left: dim_networks
schema_box(sl, Inches(0.3), Inches(4.55), Inches(2.2), Inches(1.7),
           "dim_networks",
           ["network_id  PK",
            "network_name",
            "network_type"], DIM_HDR)

# Bottom right: dim_lines
schema_box(sl, Inches(9.1), Inches(3.9), Inches(3.8), Inches(2.0),
           "dim_lines",
           ["line_id  PK",
            "line_name",
            "line_colour  (hex)",
            "is_night_service  BOOL"], DIM_HDR)

# FK arrows (text-based, matching team style)
for txt, l, t in [
    ("FK", Inches(4.15), Inches(2.3)),
    ("FK", Inches(8.85), Inches(2.3)),
    ("FK", Inches(4.15), Inches(5.3)),
    ("FK", Inches(7.25), Inches(5.3)),
]:
    tb(sl, txt, l, t, Inches(0.3), Inches(0.25),
       size=8, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

tb(sl, "Red = Fact    Blue = Dimension    "
       "5,812 records  |  all FK relationships enforced at PostgreSQL level",
   Inches(0.4), Inches(6.65), Inches(12.5), Inches(0.3),
   size=10, color=RGBColor(0x55, 0x55, 0x88), italic=True)


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Step 1: Sqoop
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "Step 1 — PostgreSQL to HDFS via Apache Sqoop",
             "Script: src/raw_layer/full_load/raw_sqoop_full_load.sh  |  Triggered by Jenkins per table")

# Left panel — how it works
rect(sl, Inches(0.4), Inches(1.15), Inches(5.7), Inches(5.45), fill=CARD_BG)
rect(sl, Inches(0.4), Inches(1.15), Inches(5.7), Inches(0.36), fill=CARD_HDR)
tb(sl, "How Sqoop works here",
   Inches(0.5), Inches(1.18), Inches(5.5), Inches(0.3),
   size=13, bold=True, color=WHITE)

points = [
    ("Jenkins-driven",    "Jenkins calls the script once per table, passing table name and HDFS target path as parameters"),
    ("Source table",      "Reads from aparna.<table>_full_load (schema + _full_load suffix) using --query flag"),
    ("--query flag",      "SELECT * FROM aparna.dim_stations_full_load WHERE $CONDITIONS"),
    ("--delete-target-dir", "Clears existing HDFS directory before writing — safe full refresh"),
    ("--num-mappers 1",   "Single mapper = one clean output file per table, no fragmentation"),
    ("Control table",     "After each run: updates aparna.sqoop_control with row count, MAX PK, status=SUCCESS"),
]
for i, (label, detail) in enumerate(points):
    t = Inches(1.6) + i * Inches(0.84)
    rect(sl, Inches(0.5), t + Inches(0.04), Inches(0.05), Inches(0.6), fill=SECTION_BAR)
    tb(sl, label, Inches(0.65), t, Inches(5.2), Inches(0.3),
       size=12, bold=True, color=SECTION_BAR)
    tb(sl, detail, Inches(0.65), t + Inches(0.3), Inches(5.2), Inches(0.48),
       size=11, color=BODY_TEXT)

# Right panel — code
rect(sl, Inches(6.3), Inches(1.15), Inches(6.7), Inches(5.45), fill=CODE_BG)
rect(sl, Inches(6.3), Inches(1.15), Inches(6.7), Inches(0.36), fill=SECTION_BAR)
tb(sl, "raw_sqoop_full_load.sh  (actual Sqoop command)",
   Inches(6.4), Inches(1.18), Inches(6.5), Inches(0.3),
   size=13, bold=True, color=WHITE)

code_lines = [
    "# Called by Jenkins:  $0 <table> <hdfs_dir>",
    "REAL_TABLE=$1   TARGET_DIR=$2",
    "",
    "sqoop import \\",
    "  -Dmapreduce.framework.name=local \\",
    "  --connect jdbc:postgresql://13.42.152.118:5432/testdb \\",
    "  --username admin  --password admin123 \\",
    "  --query \"SELECT * FROM aparna.${FULL_LOAD_TABLE}",
    "           WHERE \\$CONDITIONS\" \\",
    "  --target-dir ${TARGET_DIR} \\",
    "  --delete-target-dir \\",
    "  --fields-terminated-by ',' \\",
    "  --null-string '\\\\N' \\",
    "  --num-mappers 1",
    "",
    "# Then updates sqoop_control:",
    "#  last_value, last_row_count,",
    "#  last_run_time, status=SUCCESS",
]
tb_multi(sl, code_lines, Inches(6.4), Inches(1.6), Inches(6.5), Inches(4.85),
         size=10.5, color=CODE_TEXT)

tech_badges(sl, ["Apache Sqoop", "JDBC", "Jenkins", "--delete-target-dir", "sqoop_control"])


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — HDFS Landing Zone
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "HDFS Landing Zone — After Sqoop Completes",
             "6 subdirectories  |  one CSV file per table  |  /tmp/tfl_project_hadoop/")

# Left: directory tree
rect(sl, Inches(0.4), Inches(1.15), Inches(6.0), Inches(5.45), fill=CODE_BG)
rect(sl, Inches(0.4), Inches(1.15), Inches(6.0), Inches(0.36), fill=SECTION_BAR)
tb(sl, "HDFS directory structure",
   Inches(0.5), Inches(1.18), Inches(5.8), Inches(0.3),
   size=13, bold=True, color=WHITE)
tree_lines = [
    "/tmp/tfl_project_hadoop/",
    "  |-- dim_networks_full_load/",
    "  |     part-m-00000    (1 row)",
    "  |-- dim_lines_full_load/",
    "  |     part-m-00000    (14 rows)",
    "  |-- dim_date_full_load/",
    "  |     part-m-00000    (15 rows)",
    "  |-- dim_stations_full_load/",
    "  |     part-m-00000    (436 rows)",
    "  |-- fact_station_lines_full_load/",
    "  |     part-m-00000    (575 rows)",
    "  |-- fact_passenger_entry_exit_full_load/",
    "        part-m-00000    (4,771 rows)",
]
tb_multi(sl, tree_lines, Inches(0.55), Inches(1.6), Inches(5.7), Inches(4.85),
         size=11, color=CODE_TEXT)

# Right: storage facts + why HDFS
rect(sl, Inches(6.6), Inches(1.15), Inches(6.5), Inches(2.45), fill=CARD_BG)
rect(sl, Inches(6.6), Inches(1.15), Inches(6.5), Inches(0.36), fill=CARD_HDR)
tb(sl, "Storage facts",
   Inches(6.7), Inches(1.18), Inches(6.3), Inches(0.3),
   size=13, bold=True, color=WHITE)
facts = [
    "Format      CSV (comma-delimited TEXTFILE)",
    "Header row  preserved in each file",
    "Mappers     1 per table  (-m 1 flag)",
    "Files       6 total — one per table",
    "Total rows  5,812",
]
tb_multi(sl, facts, Inches(6.75), Inches(1.6), Inches(6.2), Inches(1.88),
         size=12, color=BODY_TEXT)

rect(sl, Inches(6.6), Inches(3.75), Inches(6.5), Inches(2.85), fill=CARD_BG)
rect(sl, Inches(6.6), Inches(3.75), Inches(6.5), Inches(0.36), fill=CARD_HDR)
tb(sl, "Why HDFS?",
   Inches(6.7), Inches(3.78), Inches(6.3), Inches(0.3),
   size=13, bold=True, color=WHITE)
why_items = [
    ("Distributed storage",
     "Data split across nodes — Hive and Spark\nread it in parallel"),
    ("Fault tolerant",
     "3x block replication — no data loss on\nnode failure"),
    ("Tool-agnostic",
     "Hive, Spark, and Presto all read the same\nfiles simultaneously"),
]
for i, (h, d) in enumerate(why_items):
    t = Inches(4.2) + i * Inches(0.8)
    tb(sl, h, Inches(6.75), t, Inches(6.2), Inches(0.28),
       size=12, bold=True, color=SECTION_BAR)
    tb(sl, d, Inches(6.75), t + Inches(0.27), Inches(6.2), Inches(0.45),
       size=11, color=BODY_TEXT)

tech_badges(sl, ["HDFS", "TEXTFILE", "part-m-00000", "3x replication"])


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Key Design Decisions
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "Key Design Decisions",
             "Why each tool and pattern was chosen")

decisions = [
    (SECTION_BAR,
     "Why Sqoop instead of a custom Python/Spark script?",
     "Sqoop is purpose-built for RDBMS-to-HDFS bulk transfer. It handles JDBC type "
     "mapping automatically, uses MapReduce for parallelism, and integrates natively "
     "with the Hadoop cluster — no custom connector code needed."),
    (GREEN,
     "Why TEXTFILE (CSV) format — not Parquet?",
     "The raw layer must be an exact, unmodified copy of the source. TEXTFILE is "
     "human-readable and auditable directly on HDFS. Conversion to Parquet happens "
     "in the curated layer after quality checks are applied — clean separation of concerns."),
    (DIM_HDR,
     "Why --delete-target-dir on every run?",
     "Ensures every full load is a clean, idempotent refresh. No stale data from a "
     "previous run can mix with the new data. If the job fails mid-way, the next run "
     "starts fresh — no manual cleanup needed."),
    (FACT_HDR,
     "Why --num-mappers 1 (single mapper)?",
     "Multiple mappers write multiple part files per table. A single mapper produces "
     "one clean file per table, which is simpler to inspect, audit, and "
     "work with during debugging and verification."),
]

for i, (color, question, answer) in enumerate(decisions):
    t = Inches(1.15) + i * Inches(1.48)
    rect(sl, Inches(0.4), t, Inches(12.5), Inches(1.38), fill=CARD_BG)
    rect(sl, Inches(0.4), t, Inches(0.1), Inches(1.38), fill=color)
    tb(sl, question, Inches(0.62), t + Inches(0.1), Inches(12.0), Inches(0.32),
       size=13, bold=True, color=color)
    tb(sl, answer, Inches(0.62), t + Inches(0.48), Inches(12.0), Inches(0.8),
       size=12, color=BODY_TEXT)

tech_badges(sl, ["Sqoop", "JDBC", "TEXTFILE", "--delete-target-dir", "--num-mappers 1"])


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Results
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "Results — What Was Delivered",
             "End-to-end verified: PostgreSQL -> HDFS via Sqoop")

# Top metrics row (matching team slide 1 stat style)
metrics = [
    ("5,812",  "Records moved\nPostgreSQL to HDFS"),
    ("6",      "Tables landed\nin HDFS"),
    ("15",     "Years of data\n2007 - 2021"),
    ("436",    "London stations\nfully mapped"),
    ("0",      "Orphaned FK\nrecords"),
]
for i, (val, label) in enumerate(metrics):
    l = Inches(0.4) + i * Inches(2.6)
    rect(sl, l, Inches(1.15), Inches(2.4), Inches(1.7), fill=CARD_BG)
    rect(sl, l, Inches(1.15), Inches(2.4), Inches(0.36), fill=SECTION_BAR)
    tb(sl, val, l, Inches(1.55), Inches(2.4), Inches(0.65),
       size=30, bold=True, color=TITLE_BAR, align=PP_ALIGN.CENTER)
    tb(sl, label, l, Inches(2.15), Inches(2.4), Inches(0.6),
       size=10, color=BODY_TEXT, align=PP_ALIGN.CENTER)

# Bottom left: checklist
rect(sl, Inches(0.4), Inches(3.05), Inches(5.9), Inches(3.55), fill=CARD_BG)
rect(sl, Inches(0.4), Inches(3.05), Inches(5.9), Inches(0.36), fill=CARD_HDR)
tb(sl, "Validation checklist",
   Inches(0.5), Inches(3.08), Inches(5.7), Inches(0.3),
   size=13, bold=True, color=WHITE)

checks = [
    "Sqoop imports completed for all 6 tables",
    "5,812 records landed in HDFS",
    "One clean file per table (part-m-00000)",
    "sqoop_control updated with SUCCESS status",
    "HDFS directory listing verified after each run",
    "Zero orphaned FK records in source",
    "Jenkins pipeline executed end-to-end",
    "All 6 _full_load tables transferred correctly",
]
for i, chk in enumerate(checks):
    row_t = Inches(3.52) + i * Inches(0.38)
    tb(sl, "OK", Inches(0.5), row_t, Inches(0.5), Inches(0.34),
       size=10, bold=True, color=GREEN)
    tb(sl, chk, Inches(1.0), row_t, Inches(5.1), Inches(0.34),
       size=11, color=BODY_TEXT)

# Bottom right: sample query
rect(sl, Inches(6.5), Inches(3.05), Inches(6.6), Inches(3.55), fill=CODE_BG)
rect(sl, Inches(6.5), Inches(3.05), Inches(6.6), Inches(0.36), fill=SECTION_BAR)
tb(sl, "Sample Hive query on tfl_db (top 5 stations 2019)",
   Inches(6.6), Inches(3.08), Inches(6.4), Inches(0.3),
   size=12, bold=True, color=WHITE)

query_lines = [
    "SELECT s.station_name,",
    "       SUM(f.total_entry_exit) AS pax",
    "FROM   fact_passenger_entry_exit f",
    "JOIN   dim_stations s USING (station_id)",
    "JOIN   dim_date d     USING (date_id)",
    "WHERE  d.year = 2019",
    "GROUP  BY s.station_name",
    "ORDER  BY pax DESC LIMIT 5;",
    "",
    "1. King's Cross St. Pancras  99,408,000",
    "2. Waterloo                  94,196,000",
    "3. Victoria                  82,564,000",
    "4. London Bridge             72,119,000",
    "5. Liverpool Street          66,972,000",
]
tb_multi(sl, query_lines, Inches(6.6), Inches(3.5), Inches(6.35), Inches(2.95),
         size=10.5, color=CODE_TEXT)

tech_badges(sl, ["Sqoop", "HDFS", "Jenkins", "sqoop_control", "TEXTFILE"])


# ════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Summary
# ════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_chrome(sl, "Summary — PostgreSQL to HDFS Raw Layer",
             "What my section delivers to the team pipeline")

section_bar(sl, "What I Delivered", Inches(1.15))

summary = [
    (SECTION_BAR,
     "Starting Point",
     "PostgreSQL testdb already holds 6 validated tables — 5,812 FK-clean records "
     "in a star schema. This is the source of truth for the entire pipeline."),
    (GREEN,
     "Step 1 — Sqoop Transfer",
     "Jenkins triggers raw_sqoop_full_load.sh once per table. Sqoop reads from "
     "aparna.<table>_full_load via JDBC and writes clean TEXTFILE data to "
     "/tmp/tfl_project_hadoop/ on HDFS."),
    (DIM_HDR,
     "Audit Trail",
     "After each table load, the script queries PostgreSQL to get row count and MAX PK, "
     "then updates aparna.sqoop_control with status=SUCCESS. Full traceability per table."),
    (FACT_HDR,
     "Handoff",
     "6 clean CSV datasets sitting in HDFS under /tmp/tfl_project_hadoop/ — "
     "ready for the curated layer (teammates' section) to consume via Spark "
     "and transform into Gold Parquet tables."),
]

for i, (color, label, text) in enumerate(summary):
    t = Inches(1.72) + i * Inches(1.22)
    rect(sl, Inches(0.4), t, Inches(12.5), Inches(1.1), fill=CARD_BG)
    rect(sl, Inches(0.4), t, Inches(0.1), Inches(1.1), fill=color)
    tb(sl, label, Inches(0.65), t + Inches(0.08), Inches(2.5), Inches(0.32),
       size=14, bold=True, color=color)
    tb(sl, text, Inches(3.3), t + Inches(0.08), Inches(9.4), Inches(0.9),
       size=12, color=BODY_TEXT)

tech_badges(sl, ["PostgreSQL", "Sqoop", "HDFS", "Jenkins", "sqoop_control", "TEXTFILE"])


# ── Save ──────────────────────────────────────────────────────────────────────
OUT = r"c:\Users\samia\Big_Data_Project\TfL_Pipeline_PostgreSQL_to_Hive.pptx"
prs.save(OUT)
print(f"Saved: {OUT}  ({len(prs.slides)} slides)")
