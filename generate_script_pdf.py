# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    PageBreak, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

NAVY       = HexColor("#0D1B2A")
MID_NAVY   = HexColor("#1B2B45")
BLUE       = HexColor("#009DE0")
TEAL       = HexColor("#00C9B1")
LIGHT_GREY = HexColor("#CCD6E0")
YELLOW     = HexColor("#FFD166")
WHITE_HEX  = HexColor("#FFFFFF")
BODY_TEXT  = HexColor("#2C2C3E")

OUT = r"c:\Users\samia\Big_Data_Project\Presentation_Script.pdf"
W, H = A4

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Presentation Script - PostgreSQL to Hive",
    author="Samia Anis",
)

# ── Page callbacks ────────────────────────────────────────────────────────────
def on_first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, H - 0.18*cm, W, 0.18*cm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, W, 0.18*cm, fill=1, stroke=0)
    canvas.restoreState()

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(HexColor("#F4F6FA"))
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, H - 1.15*cm, W, 0.12*cm, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 0.9*cm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0.9*cm, W, 0.08*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LIGHT_GREY)
    canvas.drawString(2*cm, H - 0.78*cm,
        "Presentation Script  |  PostgreSQL to Hive  |  TfL Big Data Project")
    canvas.drawString(2*cm, 0.32*cm, "Samia Anis  |  Big Data Project  |  2026")
    canvas.drawRightString(W - 2*cm, 0.32*cm, f"Page {doc.page}")
    canvas.restoreState()

# ── Slide block helper ────────────────────────────────────────────────────────
def slide_block(number, title, subtitle, paragraphs, tip=None):
    items = []

    header_data = [[
        Paragraph(f"SLIDE {number}", ParagraphStyle(
            "sn", fontSize=9, fontName="Helvetica-Bold",
            textColor=TEAL, leading=11)),
        Paragraph(title, ParagraphStyle(
            "sh", fontSize=13, fontName="Helvetica-Bold",
            textColor=WHITE_HEX, leading=16)),
    ]]
    ht = Table(header_data, colWidths=[2.2*cm, 14.3*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), NAVY),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0),(0, 0),  8),
        ("LEFTPADDING",  (1,0),(1, 0),  6),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
    ]))
    items.append(ht)

    if subtitle:
        items.append(Paragraph(subtitle, ParagraphStyle(
            "ss", fontSize=9.5, fontName="Helvetica-Oblique",
            textColor=BLUE, leading=13, spaceBefore=3, spaceAfter=6, leftIndent=4)))

    items.append(Spacer(1, 0.15*cm))

    rows = [[Paragraph(p, ParagraphStyle(
        "sp", fontSize=11, fontName="Helvetica",
        textColor=BODY_TEXT, leading=17, alignment=TA_JUSTIFY, spaceAfter=5,
    ))] for p in paragraphs]

    if rows:
        st = Table(rows, colWidths=[16.5*cm])
        st.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), WHITE_HEX),
            ("BOX",          (0,0),(-1,-1), 0.5, LIGHT_GREY),
            ("LEFTPADDING",  (0,0),(-1,-1), 14),
            ("RIGHTPADDING", (0,0),(-1,-1), 14),
            ("TOPPADDING",   (0,0),(0, 0),  10),
            ("BOTTOMPADDING",(0,-1),(0,-1), 10),
            ("TOPPADDING",   (0,1),(-1,-1), 4),
            ("BOTTOMPADDING",(0,0),(-1,-2), 0),
            ("LINEBEFORE",   (0,0),(0,-1),  3, TEAL),
        ]))
        items.append(st)

    if tip:
        td = [[Paragraph(f"Delivery tip: {tip}", ParagraphStyle(
            "tp", fontSize=9.5, fontName="Helvetica-Oblique",
            textColor=HexColor("#7A4800"), leading=13))]]
        tt = Table(td, colWidths=[16.5*cm])
        tt.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), HexColor("#FFF8E1")),
            ("BOX",          (0,0),(-1,-1), 0.5, YELLOW),
            ("LEFTPADDING",  (0,0),(-1,-1), 10),
            ("RIGHTPADDING", (0,0),(-1,-1), 10),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ]))
        items.append(Spacer(1, 0.15*cm))
        items.append(tt)

    items.append(Spacer(1, 0.5*cm))
    items.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GREY))
    items.append(Spacer(1, 0.4*cm))
    return KeepTogether(items)


# ── Build story ───────────────────────────────────────────────────────────────
story = []

# COVER
story.append(Spacer(1, 4*cm))
story.append(Paragraph("Presenter Script", ParagraphStyle(
    "ct", fontSize=32, fontName="Helvetica-Bold",
    textColor=WHITE_HEX, alignment=TA_CENTER, leading=38, spaceAfter=10)))
story.append(Paragraph(
    "PostgreSQL to Hive &mdash; Data Ingestion &amp; Raw Layer Pipeline",
    ParagraphStyle("cs", fontSize=15, fontName="Helvetica-Oblique",
                   textColor=TEAL, alignment=TA_CENTER, leading=20, spaceAfter=6)))
story.append(Spacer(1, 0.4*cm))

div = Table([[""]], colWidths=[12*cm])
div.setStyle(TableStyle([("LINEBELOW",(0,0),(-1,-1),1.5,BLUE),
                          ("TOPPADDING",(0,0),(-1,-1),0),
                          ("BOTTOMPADDING",(0,0),(-1,-1),0)]))
story.append(div)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("TfL Big Data Project", ParagraphStyle(
    "cm", fontSize=12, fontName="Helvetica",
    textColor=LIGHT_GREY, alignment=TA_CENTER, leading=16, spaceAfter=4)))
story.append(Paragraph("Samia Anis  |  2026", ParagraphStyle(
    "cm2", fontSize=11, fontName="Helvetica",
    textColor=LIGHT_GREY, alignment=TA_CENTER, leading=14, spaceAfter=4)))
story.append(Spacer(1, 2*cm))

meta_rows = [
    ["Total Slides",        "9  (slides 4-12 in the team deck)"],
    ["Estimated Duration",  "8 - 10 minutes"],
    ["Starting Point",      "Data already loaded in PostgreSQL"],
    ["Scope",               "PostgreSQL  to  HDFS (Sqoop)  to  Hive External Tables"],
    ["Handoff To",          "Spark Curated Layer (teammates)"],
]
mt = Table(meta_rows, colWidths=[5*cm, 10*cm])
mt.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), MID_NAVY),
    ("TEXTCOLOR",     (0,0),(0,-1),  TEAL),
    ("TEXTCOLOR",     (1,0),(1,-1),  WHITE_HEX),
    ("FONTNAME",      (0,0),(0,-1),  "Helvetica-Bold"),
    ("FONTNAME",      (1,0),(1,-1),  "Helvetica"),
    ("FONTSIZE",      (0,0),(-1,-1), 11),
    ("LEFTPADDING",   (0,0),(-1,-1), 12),
    ("TOPPADDING",    (0,0),(-1,-1), 8),
    ("BOTTOMPADDING", (0,0),(-1,-1), 8),
    ("ROWBACKGROUNDS",(0,0),(-1,-1), [MID_NAVY, HexColor("#162236")]),
    ("BOX",           (0,0),(-1,-1), 0.5, BLUE),
    ("INNERGRID",     (0,0),(-1,-1), 0.3, HexColor("#253D5B")),
]))
story.append(mt)
story.append(PageBreak())

# HOW TO USE
how = [[Paragraph(
    "<b>How to use this script</b><br/><br/>"
    "Each section matches one slide in the PowerPoint deck. "
    "The script is written in natural spoken language &mdash; read it aloud a few times "
    "before the presentation so it sounds conversational rather than read off a page. "
    "Yellow tip boxes give delivery guidance for that specific slide.",
    ParagraphStyle("hw", fontSize=11, fontName="Helvetica",
                   textColor=BODY_TEXT, leading=17, alignment=TA_JUSTIFY))]]
ht2 = Table(how, colWidths=[16.5*cm])
ht2.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,-1), HexColor("#EAF6FF")),
    ("BOX",          (0,0),(-1,-1), 1, BLUE),
    ("LEFTPADDING",  (0,0),(-1,-1), 14),
    ("RIGHTPADDING", (0,0),(-1,-1), 14),
    ("TOPPADDING",   (0,0),(-1,-1), 12),
    ("BOTTOMPADDING",(0,0),(-1,-1), 12),
    ("LINEBEFORE",   (0,0),(0,-1),  4, BLUE),
]))
story.append(ht2)
story.append(Spacer(1, 0.8*cm))


# ── SLIDES ────────────────────────────────────────────────────────────────────

story.append(slide_block(
    1, "Agenda — What I'll Cover", "Your first slide in the team deck (slide 4 overall)",
    [
        "Hi everyone. My name is Samia, and I'll be presenting the raw data pipeline section — from PostgreSQL through to HDFS.",
        "Here's what I'll cover. First, I'll give you a quick look at what's already sitting in PostgreSQL — the star schema and the six tables we're working with. Then I'll walk through the pipeline architecture to show exactly which part is mine. After that I'll cover the Sqoop transfer to HDFS and the HDFS landing zone. And I'll finish with the key design decisions and results.",
        "The whole thing follows what's called a Bronze or Raw layer pattern — we move data exactly as-is, with no transformations, so it can be audited and replayed at any time.",
    ],
    tip="This is your first slide — set the tone calmly and confidently. Point to each of the four numbered items as you mention them. Do not rush."
))

story.append(slide_block(
    2, "Pipeline Architecture — My Section", "Shows where your section starts and ends",
    [
        "This is the full picture of my section.",
        "The pipeline starts at PostgreSQL on the left — this is our starting point, the data is already here. From PostgreSQL, Jenkins triggers Apache Sqoop, which reads the data over JDBC and writes it directly into HDFS on the Hadoop cluster as clean CSV files.",
        "You can see the bracket at the bottom marking my section — PostgreSQL through to HDFS. The curated layer on the right is where my teammates pick up from — they consume the HDFS data with Spark.",
        "One important note on the PostgreSQL box: I've marked it as the starting point. The data loading from CSV into PostgreSQL was done previously — my job is everything from PostgreSQL onwards.",
    ],
    tip="Point at the PostgreSQL box and say clearly 'this is where I start'. Then trace the arrows right as you describe each step. This prevents confusion about what you own."
))

story.append(slide_block(
    3, "What's Already in PostgreSQL", "The star schema — our source data",
    [
        "Before I show the Sqoop transfer, let me quickly show you what's in PostgreSQL that we're moving.",
        "We have six tables structured as a star schema. Four dimension tables: dim_networks with one row for the network type, dim_lines with 14 tube and rail lines, dim_date with 15 annual time periods from 2007 to 2021, and dim_stations with 436 London stations — each station carries flags for Night Tube, DLR, Overground, and the Elizabeth line.",
        "Then two fact tables. fact_station_lines is a bridge table handling the many-to-many relationship between stations and lines — 575 records. And the main fact table, fact_passenger_entry_exit, with 4,771 records of annual passenger counts per station.",
        "In total 5,812 records, all validated — foreign keys enforced, no orphaned records. This clean state is what Sqoop will pick up and transfer to HDFS.",
    ],
    tip="This slide is context, not deep detail. Keep the pace moving — you're just showing the audience what the source looks like before you move it. 60 seconds maximum."
))

story.append(slide_block(
    4, "PostgreSQL Star Schema Diagram", "Relational structure we are moving to Hive",
    [
        "This is the actual schema in PostgreSQL.",
        "In the centre is the main fact table, fact_passenger_entry_exit. It has two foreign keys — one to dim_stations for the WHERE, and one to dim_date for the WHEN. Classic star pattern.",
        "The bridge table fact_station_lines sits below it, linking stations and lines with a foreign key to each.",
        "The dimensions surround the facts: dim_stations on the left with all the station service flags, dim_date on the right with the time dimension, dim_networks at the bottom left, and dim_lines at the bottom right.",
        "All these foreign key relationships are enforced at the database level. So by the time Sqoop reads this data, we already know it's referentially clean. We're not just moving raw files — we're moving a validated, structured dataset.",
    ],
    tip="You do not need to read every column name. Just trace the FK arrows and explain the relationships. 60 to 90 seconds is enough for this slide."
))

story.append(slide_block(
    5, "Step 1 — Sqoop: PostgreSQL to HDFS", "Script: src/raw_layer/full_load/raw_sqoop_full_load.sh  |  Triggered by Jenkins per table",
    [
        "Now the first real step of my section — moving the data from PostgreSQL into HDFS using Apache Sqoop.",
        "The script is called raw_sqoop_full_load.sh, and it's Jenkins-driven. Jenkins calls it once per table, passing two parameters: the table name and the HDFS target directory. You can see this in the code — REAL_TABLE equals dollar-one, TARGET_DIR equals dollar-two.",
        "On the source side, we're not reading from a plain table name. Each source table has a full-load suffix in PostgreSQL — so dim_stations becomes aparna.dim_stations_full_load. The script maps the table name to the right source automatically. It uses the --query flag rather than --table, which gives us the flexibility to apply that WHERE dollar-CONDITIONS clause that Sqoop requires for splitting.",
        "For the flags — --delete-target-dir clears the existing HDFS directory before writing, so every run is a clean full refresh with no stale data left behind. --num-mappers 1 means one mapper per table, which produces a single clean output file rather than fragmented part files.",
        "After Sqoop finishes, the script queries MAX on the primary key and COUNT of rows from PostgreSQL, and updates aparna.sqoop_control with the last value, row count, run time, and a status of SUCCESS. That control table is our audit trail — it tracks exactly what landed, and when.",
    ],
    tip="The JDBC URL and -m 1 flag are the two things most likely to get questions. Be ready to explain them confidently. The JDBC URL is just a standard connection string. The -m 1 choice is about simplicity over parallelism."
))

story.append(slide_block(
    6, "HDFS Landing Zone", "What the data looks like after Sqoop",
    [
        "After Sqoop finishes, the data is sitting in HDFS. This is what the directory structure looks like.",
        "Everything lives under /tmp/tfl_project_hadoop/. Each table has its own subdirectory with a full-load suffix — so dim_stations becomes dim_stations_full_load, fact_passenger_entry_exit becomes fact_passenger_entry_exit_full_load, and so on. Inside each directory is a single file called part-m-00000 — that single file is the output from our one Sqoop mapper.",
        "The format is plain CSV — comma-delimited text, with the header row still included. The downstream curated layer handles parsing from there.",
        "Why HDFS and not just keep it in PostgreSQL? Three reasons. First, it's distributed — the data is spread across multiple nodes so Hive and Spark can read it in parallel. Second, it's fault tolerant — HDFS replicates each block three times, so a node failure doesn't lose data. Third, it's tool-agnostic — Hive, Spark, and Presto can all read the same HDFS files at the same time without competing.",
        "PostgreSQL is great for constraints and transactional queries, but it's a bottleneck for large analytical workloads. HDFS is designed exactly for that kind of scale.",
    ],
    tip="Point at the directory tree while you describe it. The audience processes hierarchical structure much faster when someone physically traces the path."
))

story.append(slide_block(
    7, "Key Design Decisions", "Why each tool and pattern was chosen",
    [
        "I want to take a moment to explain the reasoning behind the key choices we made, because each one was deliberate.",
        "First — why Sqoop and not a custom Python script to write to HDFS directly? Sqoop is purpose-built for RDBMS-to-HDFS bulk transfer. It handles PostgreSQL type mapping automatically, uses MapReduce for parallelism, and integrates natively with the cluster. Custom code would need to replicate all of that and would be much harder to maintain.",
        "Second — why TEXTFILE and not Parquet? The raw layer must be an exact, unmodified copy of the source. TEXTFILE is human-readable and can be audited directly on HDFS without special tooling. We leave the Parquet conversion to the curated layer — clean separation of concerns.",
        "Third — why --delete-target-dir on every run? This makes every load a clean, idempotent full refresh. No stale data from a previous run can mix with new data. If a run fails halfway through, the next run starts from scratch automatically.",
        "Fourth — why --num-mappers 1, a single mapper? Multiple mappers write multiple part files per table. A single file per table is simpler to inspect, easier to debug, and cleaner for downstream processing.",
    ],
    tip="Pause between each of the four decisions. Each one is a self-contained argument. Rushing through them makes it sound like a list rather than a reasoned architectural choice."
))

story.append(slide_block(
    8, "Results", "What was delivered and verified",
    [
        "Let me show you what we actually delivered.",
        "5,812 records successfully transferred from PostgreSQL to HDFS via Sqoop. Six tables landed in HDFS. Fifteen years of historical data. 436 stations fully mapped. And zero orphaned foreign key records.",
        "The checklist on the left shows every validation step we ran — Sqoop imports for all six tables, HDFS file counts, sqoop_control updated with SUCCESS status, Jenkins pipeline executed end-to-end. Everything passed.",
        "On the right is a sample query that can be run against the data once it reaches the curated layer. This shows the kind of analytical output the pipeline enables — top five busiest stations in 2019 — which proves the data that landed in HDFS is clean and complete.",
    ],
    tip="Focus on the checklist as your proof of delivery. The sample query shows the business value of the data that was moved."
))

story.append(slide_block(
    9, "Summary & Handoff", "What you built and what comes next",
    [
        "To summarise my section.",
        "I started with data already in PostgreSQL — a validated star schema with 5,812 records across six tables. Jenkins triggered raw_sqoop_full_load.sh once per table, and Sqoop transferred all six tables from PostgreSQL into HDFS as clean single-file CSV datasets under /tmp/tfl_project_hadoop/. After each run, the sqoop_control table was updated with the row count and status.",
        "What I hand off to my teammates is six clean datasets sitting in HDFS, ready to be consumed by Spark for the curated layer transformations they'll present next.",
        "Thank you — happy to take any questions.",
    ],
    tip="After saying 'happy to take any questions', look up, pause, and wait. Do not fill the silence. Let the audience come to you."
))

# ── Q&A PAGE ─────────────────────────────────────────────────────────────────
story.append(PageBreak())

qa_hdr = [[Paragraph("Anticipated Q&amp;A", ParagraphStyle(
    "qt", fontSize=16, fontName="Helvetica-Bold", textColor=WHITE_HEX, leading=20))]]
qa_t = Table(qa_hdr, colWidths=[16.5*cm])
qa_t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,-1), NAVY),
    ("LEFTPADDING",  (0,0),(-1,-1), 14),
    ("TOPPADDING",   (0,0),(-1,-1), 10),
    ("BOTTOMPADDING",(0,0),(-1,-1), 10),
    ("LINEBEFORE",   (0,0),(0,-1),  4, TEAL),
]))
story.append(qa_t)
story.append(Spacer(1, 0.5*cm))

qa_pairs = [
    ("Why use Sqoop instead of writing a Python script to move data to HDFS?",
     "Sqoop is purpose-built for this. It handles JDBC type mapping from PostgreSQL "
     "automatically, manages MapReduce parallelism, and writes output that Hive reads "
     "natively. A custom Python script would need to replicate the JDBC driver, handle "
     "type conversions, manage HDFS writes directly, and deal with partial failures. "
     "That's a lot of infrastructure code for something Sqoop already solves."),
    ("What is sqoop_control and why is it used?",
     "sqoop_control is a PostgreSQL table that acts as an audit log for every Sqoop run. "
     "After each table is loaded, the script queries MAX on the primary key and COUNT of rows, "
     "then writes those values plus a SUCCESS status into sqoop_control. "
     "This gives full traceability — you can see exactly what landed in HDFS, how many rows, "
     "and when, without having to inspect HDFS directly."),
    ("Why not load directly from CSV to HDFS and skip PostgreSQL?",
     "PostgreSQL gives us a validation checkpoint. FK constraints, type checking, and "
     "null handling all catch problems at the database level before the data reaches "
     "HDFS. If we bypassed PostgreSQL, bad data would silently land in HDFS and only "
     "surface when a downstream Spark job fails — which is much harder to debug."),
    ("Why TEXTFILE and not Parquet in the raw HDFS layer?",
     "The raw layer is an unmodified copy of the source. TEXTFILE is human-readable "
     "and can be inspected directly on HDFS without special tooling. Parquet is a "
     "compressed columnar format that's great for analytics but harder to audit. "
     "We convert to Parquet in the curated layer, after quality checks — "
     "that's a clean separation of concerns."),
    ("Why use -m 1 (single mapper) in Sqoop? Doesn't that slow it down?",
     "For our dataset size — a few thousand rows per table — the overhead of "
     "coordinating multiple mappers outweighs the benefit. More importantly, "
     "multiple mappers write multiple part files per table, which adds complexity "
     "when auditing or debugging. A single file per table is clean and simple. "
     "If the dataset were millions of rows, we would increase the mapper count."),
]

for q, a in qa_pairs:
    q_data = [[Paragraph(q, ParagraphStyle(
        "qq", fontSize=11, fontName="Helvetica-Bold",
        textColor=NAVY, leading=15))]]
    qt = Table(q_data, colWidths=[16.5*cm])
    qt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), HexColor("#E3F2FD")),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LINEBEFORE",   (0,0),(0,-1),  3, BLUE),
    ]))
    a_data = [[Paragraph(a, ParagraphStyle(
        "qa", fontSize=11, fontName="Helvetica",
        textColor=BODY_TEXT, leading=16, alignment=TA_JUSTIFY))]]
    at = Table(a_data, colWidths=[16.5*cm])
    at.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), WHITE_HEX),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("RIGHTPADDING", (0,0),(-1,-1), 12),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("BOX",          (0,0),(-1,-1), 0.3, LIGHT_GREY),
        ("LINEBEFORE",   (0,0),(0,-1),  3, TEAL),
    ]))
    story.append(KeepTogether([qt, at, Spacer(1, 0.4*cm)]))

doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
print(f"Saved: {OUT}")
