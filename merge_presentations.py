# -*- coding: utf-8 -*-
"""
Merge Samia's slides into the team presentation.
- Skips our title slide (team already has one)
- Skips the incremental load slide
- Inserts after existing slide 3 (Pipeline Architecture overview)
"""
from pptx import Presentation
from pptx.util import Inches
from lxml import etree
import copy

TEAM_FILE  = r"C:\Users\samia\Downloads\TFL_Pipeline_Presentation.pptx"
MY_FILE    = r"C:\Users\samia\Big_Data_Project\TfL_Pipeline_PostgreSQL_to_Hive.pptx"
OUT_FILE   = r"C:\Users\samia\Big_Data_Project\TfL_Team_Presentation_Merged.pptx"

# Insert position: after slide index 2 (existing slide 3 - Pipeline Architecture)
INSERT_AFTER = 2

# ── Slide indices to copy from our file (0-based) ────────────────────────────
# Our slides (redesigned, 10 slides, no title, no incremental):
#  0  Agenda
#  1  Pipeline Architecture (my section)
#  2  What's Already in PostgreSQL
#  3  Star Schema Diagram
#  4  Step 1 - Sqoop
#  5  HDFS Landing Zone
#  6  Step 2 - Hive Tables
#  7  Key Design Decisions
#  8  Results
#  9  Summary
MY_SLIDE_INDICES = [0, 1, 2, 3, 4, 5, 6, 7, 8]

PML_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"

def copy_slide_into(dst_prs, src_slide):
    """
    Copy src_slide (all shapes + background) into dst_prs as a new blank slide.
    Works for shape-only slides (no external image relationships).
    """
    blank_layout = dst_prs.slide_layouts[6]          # fully blank layout
    new_slide    = dst_prs.slides.add_slide(blank_layout)

    # ── Replace shape tree content ──────────────────────────────────────────
    new_sp_tree = new_slide.shapes._spTree
    src_sp_tree = src_slide.shapes._spTree

    # Remove children that the blank layout added
    for child in list(new_sp_tree):
        new_sp_tree.remove(child)

    # Deep-copy every child from source shape tree
    for child in src_sp_tree:
        new_sp_tree.append(copy.deepcopy(child))

    # ── Copy slide background (colour fill) ─────────────────────────────────
    src_bg = src_slide._element.find(f"{{{PML_NS}}}bg")
    if src_bg is not None:
        new_slide._element.insert(0, copy.deepcopy(src_bg))

    # ── Copy any color map override ─────────────────────────────────────────
    src_clr = src_slide._element.find(f"{{{PML_NS}}}clrMapOvr")
    if src_clr is not None:
        new_slide._element.append(copy.deepcopy(src_clr))

    return new_slide


def move_slide(prs, from_idx, to_idx):
    """Move slide at from_idx to to_idx inside prs."""
    xml_slides = prs.slides._sldIdLst
    slides     = list(xml_slides)
    slide_el   = slides[from_idx]
    xml_slides.remove(slide_el)
    xml_slides.insert(to_idx, slide_el)


# ── Load both presentations ──────────────────────────────────────────────────
team_prs = Presentation(TEAM_FILE)
my_prs   = Presentation(MY_FILE)

team_count_before = len(team_prs.slides)
print(f"Team presentation: {team_count_before} existing slides")
print(f"Our presentation:  {len(my_prs.slides)} slides total")
print(f"Slides to insert:  {MY_SLIDE_INDICES} ({len(MY_SLIDE_INDICES)} slides)")
print(f"Inserting after existing slide {INSERT_AFTER + 1}")
print()

# ── Copy our slides to the END of the team presentation ─────────────────────
for idx in MY_SLIDE_INDICES:
    src = my_prs.slides[idx]
    copy_slide_into(team_prs, src)
    print(f"  Copied our slide {idx + 1}")

# ── Move inserted slides to correct position ─────────────────────────────────
# They currently sit at positions [team_count_before .. team_count_before + n-1]
# We want them at [INSERT_AFTER+1 .. INSERT_AFTER+n]
num_inserted = len(MY_SLIDE_INDICES)
new_total    = len(team_prs.slides)

print(f"\nMoving {num_inserted} slides to position {INSERT_AFTER + 2}...")

for i in range(num_inserted):
    # After each move the indices shift, so always grab from current end block
    current_pos = new_total - num_inserted + i
    target_pos  = INSERT_AFTER + 1 + i
    if current_pos != target_pos:
        move_slide(team_prs, current_pos, target_pos)

# ── Save ─────────────────────────────────────────────────────────────────────
team_prs.save(OUT_FILE)
print(f"\nMerged presentation saved: {OUT_FILE}")
print(f"Total slides: {len(team_prs.slides)}")

# Print final slide order
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
print("\nFinal slide order:")
for i, slide in enumerate(team_prs.slides):
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.text.strip().replace('\n', ' ')
            if t:
                texts.append(t[:60])
    label = " | ".join(texts[:2]) if texts else "(no text)"
    marker = "  << SAMIA" if (INSERT_AFTER + 1) <= i <= (INSERT_AFTER + num_inserted) else ""
    print(f"  Slide {i+1:2d}: {label[:80]}{marker}")
