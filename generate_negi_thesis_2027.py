import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py_modules'))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional NIT Meghalaya Color Palette
    c_blue = RGBColor(24, 116, 205)       # Dodger Blue (#1874CD)
    c_navy = RGBColor(0, 43, 91)         # Navy Blue (#002B5B)
    c_dark = RGBColor(33, 37, 41)        # Text Charcoal (#212529)
    c_card_bg = RGBColor(248, 250, 252)  # Soft background (#F8FAFC)
    c_border = RGBColor(226, 232, 240)   # Clean light border (#E2E8F0)
    c_white = RGBColor(255, 255, 255)
    c_green = RGBColor(22, 101, 52)      # Deep Forest Green (#166534)
    c_green_bg = RGBColor(220, 252, 231) # Light green highlight
    c_crimson = RGBColor(185, 28, 28)    # Crimson red (#B91C1C)
    c_footer_gray = RGBColor(241, 245, 249)

    def add_footer(slide, current_slide, total_slides=15):
        f_top = Inches(7.05)
        f_height = Inches(0.45)
        
        # Left: Author
        b1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), f_top, Inches(5.8), f_height)
        b1.fill.solid()
        b1.fill.fore_color.rgb = c_blue
        b1.line.color.rgb = c_blue
        tf1 = b1.text_frame
        tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = tf1.paragraphs[0]
        p1.text = "Vivek Negi – T25CS012 (NIT Meghalaya)"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = c_white
        p1.alignment = PP_ALIGN.CENTER
        
        # Middle: Title
        b2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), f_top, Inches(6.0), f_height)
        b2.fill.solid()
        b2.fill.fore_color.rgb = c_footer_gray
        b2.line.color.rgb = c_footer_gray
        tf2 = b2.text_frame
        tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = tf2.paragraphs[0]
        p2.text = "Multi-Source Media Lineage Retrieval"
        p2.font.size = Pt(12)
        p2.font.color.rgb = c_dark
        p2.alignment = PP_ALIGN.CENTER

        # Right: Slide Number
        b3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.8), f_top, Inches(1.533), f_height)
        b3.fill.solid()
        b3.fill.fore_color.rgb = c_navy
        b3.line.color.rgb = c_navy
        tf3 = b3.text_frame
        tf3.vertical_anchor = MSO_ANCHOR.MIDDLE
        p3 = tf3.paragraphs[0]
        p3.text = f"{current_slide} / {total_slides}"
        p3.font.size = Pt(12)
        p3.font.bold = True
        p3.font.color.rgb = c_white
        p3.alignment = PP_ALIGN.CENTER

    def add_header(slide, title_text):
        header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05))
        header.fill.solid()
        header.fill.fore_color.rgb = c_blue
        header.line.color.rgb = c_blue
        
        tf = header.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.LEFT
        tf.margin_left = Inches(0.8)

    def add_bullet(tf, title, desc="", level=0, size=16, space_before=10, bold_color=c_navy):
        p = tf.add_paragraph() if len(tf.paragraphs[0].text) > 0 else tf.paragraphs[0]
        p.level = level
        p.space_before = Pt(space_before)
        if title:
            r1 = p.add_run()
            r1.text = title + (" " if desc else "")
            r1.font.bold = True
            r1.font.size = Pt(size)
            r1.font.color.rgb = bold_color
        if desc:
            r2 = p.add_run()
            r2.text = desc
            r2.font.size = Pt(size)
            r2.font.color.rgb = c_dark

    # ==========================================================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    t_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.9))
    t_card.fill.solid()
    t_card.fill.fore_color.rgb = c_blue
    t_card.line.color.rgb = c_navy
    t_card.line.width = Pt(2)
    tf = t_card.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Multi-Source Lineage Retrieval in Composite Media\nwith Dynamic Token Alignment and Importance Gating"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.alignment = PP_ALIGN.CENTER

    meta = s1.shapes.add_textbox(Inches(1.5), Inches(2.55), Inches(10.333), Inches(4.3))
    mtf = meta.text_frame
    mtf.word_wrap = True
    
    p = mtf.paragraphs[0]
    p.text = "Vivek Negi"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER
    
    p = mtf.add_paragraph()
    p.text = "Roll No: T25CS012"
    p.font.size = Pt(16)
    p.font.color.rgb = c_dark
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(3)

    p = mtf.add_paragraph()
    p.text = "Under the guidance of"
    p.font.size = Pt(14)
    p.font.italic = True
    p.font.color.rgb = c_dark
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(6)

    p = mtf.add_paragraph()
    p.text = "Dr. Akhilendra Pratap Singh"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(2)

    logo_path = "/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/pictures/NIT logo.jpeg"
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(6.266), Inches(4.45), height=Inches(0.75))
        inst_top = Inches(5.3)
    else:
        inst_top = Inches(4.7)

    inst_box = s1.shapes.add_textbox(Inches(1.5), inst_top, Inches(10.333), Inches(1.5))
    itf = inst_box.text_frame
    
    p = itf.paragraphs[0]
    p.text = "NATIONAL INSTITUTE OF TECHNOLOGY MEGHALAYA"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.alignment = PP_ALIGN.CENTER
    
    p = itf.add_paragraph()
    p.text = "Department of Computer Science and Engineering\nNational Institute of Technology Meghalaya\nSohra, India"
    p.font.size = Pt(13)
    p.font.color.rgb = c_dark
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(3)

    p = itf.add_paragraph()
    p.text = "October 26, 2026"
    p.font.size = Pt(13)
    p.font.color.rgb = c_dark
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(5)

    add_footer(s1, 1)

    # ==========================================================================
    # SLIDE 2: INTRODUCTION
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Introduction: What is Composite Media Lineage?")
    
    cbox = s2.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(5.5))
    ctf = cbox.text_frame
    ctf.word_wrap = True

    add_bullet(ctf, "• Traditional Copy Detection:", "Search engines like Google Lens or TinEye look for exact copies or lightly edited duplicates of a single image.", space_before=8)
    add_bullet(ctf, "• The Composite Problem:", "In the real world, manipulated media usually takes parts from two or more different images:", space_before=16)
    add_bullet(ctf, "– Parent A (Background):", "The main scene or landscape.", level=1, size=15, space_before=6)
    add_bullet(ctf, "– Parent B (Donor):", "An object (car, person, animal) cut from another photo.", level=1, size=15, space_before=6)
    add_bullet(ctf, "• Our Goal:", "Build a system that takes a composite query and searches a gallery of thousands of photos to find both Parent A and Parent B.", space_before=16)
    add_bullet(ctf, "• Why it matters:", "Copyright protection, fake news verification, and digital evidence investigation.", space_before=16)

    add_footer(s2, 2)

    # ==========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Core Problem: Background Dominance")

    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.733), Inches(0.8))
    card.fill.solid()
    card.fill.fore_color.rgb = c_navy
    card.line.color.rgb = c_navy
    ctf = card.text_frame
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = ctf.paragraphs[0]
    p.text = "Why Existing AI Models Fail on Composites\nExisting vision models compress the entire image into a single global vector."
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.alignment = PP_ALIGN.CENTER

    cbox = s3.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(11.733), Inches(4.5))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "• The Background Wins:", "Because the background covers 70%–85% of the image, the AI focuses almost entirely on the background. It finds Parent A with 100% accuracy.", space_before=10)
    add_bullet(tf, "• The Donor is Lost:", "The smaller donor object (covering only 15%–35%) is completely ignored by the global vector, causing donor recall to fail.", space_before=14)
    add_bullet(tf, "• Rigid Grids Cut Objects in Half:", "Cutting an image into fixed 2 × 2 or 3 × 3 squares chops objects placed in the center into four pieces, destroying their shape.", space_before=14)
    add_bullet(tf, "• No Retraining Allowed:", "Retraining giant models (ResNets/ViTs) is too expensive and causes them to forget general features. We must solve this with a lightweight approach.", space_before=14)

    add_footer(s3, 3)

    # ==========================================================================
    # SLIDE 4: LITERATURE REVIEW 1 - SSCD
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Literature Review: Meta SSCD (CVPR 2022)")
    
    pcard = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.85))
    pcard.fill.solid()
    pcard.fill.fore_color.rgb = c_card_bg
    pcard.line.color.rgb = c_border
    ptf = pcard.text_frame
    p = ptf.paragraphs[0]
    p.text = "Paper: A Self-Supervised Descriptor for Image Copy Detection\nAuthors: E. Pizzi, S. Durasamy, S. Couprie, M. Douze, A. Gordo (Meta AI)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy

    cbox = s4.shapes.add_textbox(Inches(0.8), Inches(2.25), Inches(11.733), Inches(4.6))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "• What it does:", space_before=6)
    add_bullet(tf, "–", "Meta AI trained a ResNet-50 on millions of images using self-supervised contrastive learning specifically for copy detection.", level=1, size=15, space_before=3)
    add_bullet(tf, "–", "Produces a compact, 512-dimensional visual fingerprint for any image.", level=1, size=15, space_before=3)

    add_bullet(tf, "• Why it is strong:", space_before=12)
    add_bullet(tf, "–", "Highly robust against heavy JPEG compression, color changes, and crops.", level=1, size=15, space_before=3)
    add_bullet(tf, "–", "Currently the gold-standard backbone for image retrieval benchmarks.", level=1, size=15, space_before=3)

    add_bullet(tf, "• Limitation for our task:", space_before=12, bold_color=c_crimson)
    add_bullet(tf, "–", "It was designed for single images. On composites, its global pooling is blind to small, localized pasted objects.", level=1, size=15, space_before=3)

    add_footer(s4, 4)

    # ==========================================================================
    # SLIDE 5: LITERATURE REVIEW 2 - TRUFOR
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Literature Review: TruFor (CVPR 2023)")

    pcard = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.85))
    pcard.fill.solid()
    pcard.fill.fore_color.rgb = c_card_bg
    pcard.line.color.rgb = c_border
    ptf = pcard.text_frame
    p = ptf.paragraphs[0]
    p.text = "Paper: TruFor: Leveraging All-Round Clues for Trustworthy Forgery Detection\nAuthors: F. Guillaro, D. Cozzolino, A. Sud, N. Dufour, L. Verdoliva"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy

    cbox = s5.shapes.add_textbox(Inches(0.8), Inches(2.25), Inches(11.733), Inches(4.6))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "• What it does:", space_before=6)
    add_bullet(tf, "–", "Uses computer vision to inspect subtle camera sensor noise, compression traces, and lighting inconsistencies across image pixels.", level=1, size=15, space_before=3)
    add_bullet(tf, "–", "Outputs a heatmap showing exactly which part of an image was forged.", level=1, size=15, space_before=3)

    add_bullet(tf, "• Why it is strong:", space_before=12)
    add_bullet(tf, "–", "Best-in-class performance at localizing spliced boundaries.", level=1, size=15, space_before=3)

    add_bullet(tf, "• Limitation for our task:", space_before=12, bold_color=c_crimson)
    add_bullet(tf, "– Detection is not Attribution:", "TruFor can tell you \"this car was pasted into the photo\", but it cannot find the source file the car came from. It has no gallery search capability.", level=1, size=15, space_before=3)

    add_footer(s5, 5)

    # ==========================================================================
    # SLIDE 6: LITERATURE REVIEW 3 - SINGLE SIMPLE PATCH
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Literature Review: Single Simple Patch Network (2024)")

    pcard = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.85))
    pcard.fill.solid()
    pcard.fill.fore_color.rgb = c_card_bg
    pcard.line.color.rgb = c_border
    ptf = pcard.text_frame
    p = ptf.paragraphs[0]
    p.text = "Paper: A Single Simple Patch is All You Need for AI-generated Image Detection\nAuthors: Jiaxuan Chen, Jieteng Yao, Li Niu (arXiv:2402.01123, April 2024)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy

    cbox = s6.shapes.add_textbox(Inches(0.8), Inches(2.25), Inches(11.733), Inches(4.6))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "• What it does:", space_before=6)
    add_bullet(tf, "–", "Discovered that image generators (GANs, Diffusion) focus heavily on generating complex textures, while neglecting authentic camera sensor noise in simple/smooth patches.", level=1, size=15, space_before=3)
    add_bullet(tf, "–", "Extracts noise fingerprints from just a single simple patch using high-pass filters to distinguish real images from AI fakes.", level=1, size=15, space_before=3)

    add_bullet(tf, "• Why it connects to our work:", space_before=12)
    add_bullet(tf, "–", "Proves that local patch-level evidence carries vital forensic clues that global image representations discard.", level=1, size=15, space_before=3)

    add_bullet(tf, "• Limitation for our task:", space_before=12, bold_color=c_crimson)
    add_bullet(tf, "–", "It is strictly a binary classifier (Real vs. Fake). It cannot trace multi-parent lineages or search an image gallery for source assets.", level=1, size=15, space_before=3)

    add_footer(s6, 6)

    # ==========================================================================
    # SLIDE 7: LITERATURE REVIEW 4 - AIGIBENCH
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Literature Review: AIGIBench (NeurIPS 2025)")

    pcard = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.85))
    pcard.fill.solid()
    pcard.fill.fore_color.rgb = c_card_bg
    pcard.line.color.rgb = c_border
    ptf = pcard.text_frame
    p = ptf.paragraphs[0]
    p.text = "Paper: Is Artificial Intelligence Generated Image Detection a Solved Problem?\nAuthors: Ziqiang Li, Jiazhen Yan, Ziwen He, Kai Zeng, et al. (NeurIPS 2025)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy

    cbox = s7.shapes.add_textbox(Inches(0.8), Inches(2.25), Inches(11.733), Inches(4.6))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "• What it does:", space_before=6)
    add_bullet(tf, "–", "The latest comprehensive benchmark evaluating 11 state-of-the-art detectors across 23 modern generative subsets (SDXL, FLUX, Midjourney-v6, DALLE-3).", level=1, size=15, space_before=3)
    add_bullet(tf, "–", "Reveals that existing detectors experience massive failure drops when applied to in-the-wild content and face-swaps.", level=1, size=15, space_before=3)

    add_bullet(tf, "• Key Insight That Validates Our Method:", space_before=12, bold_color=c_green)
    add_bullet(tf, "–", "In Section 3.4, they proved that resizing an image destroys forensic details, whereas cropping preserves fine-grained local structures and high frequencies.", level=1, size=15, space_before=3)
    add_bullet(tf, "–", "This directly justifies our proposed Dynamic Cropping/Slicing strategy over global resized representations!", level=1, size=15, space_before=3)

    add_footer(s7, 7)

    # ==========================================================================
    # SLIDE 8: PROPOSED ARCHITECTURE (CLEAN & BEAUTIFUL - NO BLACK BOXES!)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Proposed Architecture")

    # Flowchart Row 1
    r1_nodes = [
        ("Composite Query Q\n+ Gallery", Inches(0.8), Inches(1.35), Inches(2.4), c_blue),
        ("Dynamic Overlap\nSlicing", Inches(3.8), Inches(1.35), Inches(2.4), c_green),
        ("Frozen SSCD\nFeatures", Inches(6.8), Inches(1.35), Inches(2.4), c_blue),
        ("MLP Importance\nGate", Inches(9.8), Inches(1.35), Inches(2.4), c_green)
    ]
    for text, left, top, width, fill_c in r1_nodes:
        shp = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.72))
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill_c
        shp.line.color.rgb = c_navy
        shp.line.width = Pt(1.5)
        tf = shp.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.CENTER

    # Row 1 Arrows
    for a_x in [Inches(3.25), Inches(6.25), Inches(9.25)]:
        arr = s8.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, a_x, Inches(1.58), Inches(0.5), Inches(0.22))
        arr.fill.solid()
        arr.fill.fore_color.rgb = c_blue
        arr.line.color.rgb = c_blue

    # Down Arrow
    arr_d = s8.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(10.9), Inches(2.12), Inches(0.22), Inches(0.48))
    arr_d.fill.solid()
    arr_d.fill.fore_color.rgb = c_blue
    arr_d.line.color.rgb = c_blue

    # Flowchart Row 2
    r2_nodes = [
        ("Dual-Channel\nCandidate Fusion", Inches(9.8), Inches(2.65), Inches(2.4), c_green),
        ("Evaluate Recall@5\n(Parent A & B)", Inches(6.8), Inches(2.65), Inches(2.4), c_blue),
        ("Blockchain / Ledger\nTimestamp Audit", Inches(3.8), Inches(2.65), Inches(2.4), c_navy)
    ]
    for text, left, top, width, fill_c in r2_nodes:
        shp = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.72))
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill_c
        shp.line.color.rgb = c_navy
        shp.line.width = Pt(1.5)
        tf = shp.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.CENTER

    # Row 2 Arrows
    for a_x in [Inches(9.25), Inches(6.25)]:
        arr = s8.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, a_x, Inches(2.88), Inches(0.5), Inches(0.22))
        arr.fill.solid()
        arr.fill.fore_color.rgb = c_blue
        arr.line.color.rgb = c_blue

    # Clean "Three Simple Steps" Card (NO overlapping boxes, NO black borders!)
    card_bg = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(11.733), Inches(3.1))
    card_bg.fill.solid()
    card_bg.fill.fore_color.rgb = c_card_bg
    card_bg.line.color.rgb = c_blue
    card_bg.line.width = Pt(1.5)
    
    # Title strip inside card
    title_strip = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(11.733), Inches(0.55))
    title_strip.fill.solid()
    title_strip.fill.fore_color.rgb = c_blue
    title_strip.line.color.rgb = c_blue
    t_tf = title_strip.text_frame
    t_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = t_tf.paragraphs[0]
    p.text = "Three Simple Steps"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.alignment = PP_ALIGN.LEFT
    t_tf.margin_left = Inches(0.3)

    # Bullet text inside card
    c_text = s8.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(11.333), Inches(2.4))
    ctf = c_text.text_frame
    ctf.word_wrap = True

    add_bullet(ctf, "1. Extract Smart Patches:", "Use center crops and overlapping windows so no donor object gets cut in half.", level=0, size=15, space_before=4)
    add_bullet(ctf, "2. Weight by Importance:", "A tiny 2-layer neural network learns to highlight the donor patch and ignore repetitive background.", level=0, size=15, space_before=10)
    add_bullet(ctf, "3. Dual Channel Search:", "Search for Parent A using the whole image, and Parent B using the weighted patches.", level=0, size=15, space_before=10)

    add_footer(s8, 8)

    # ==========================================================================
    # SLIDE 9: DYNAMIC OVERLAPPING SLICING
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Methodology: Dynamic Overlapping Slicing")

    lbox = s9.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(7.2), Inches(5.4))
    ltf = lbox.text_frame
    ltf.word_wrap = True

    add_bullet(ltf, "The Problem with Rigid Grids:", space_before=4, bold_color=c_navy)
    add_bullet(ltf, "•", "Cutting an image into a rigid 2 × 2 grid splits centered objects into 4 pieces.", level=1, size=15, space_before=4)
    add_bullet(ltf, "•", "SSCD cannot recognize one-quarter of a dog or a car.", level=1, size=15, space_before=4)

    add_bullet(ltf, "Our Dynamic Slicing Solution:", space_before=16, bold_color=c_navy)
    add_bullet(ltf, "• Center Anchors:", "Crops centered at 50% and 66% scale guarantee centered objects are captured intact.", level=1, size=15, space_before=4)
    add_bullet(ltf, "• Overlapping Windows:", "Sliding windows with 33% step ensure boundary objects are never chopped.", level=1, size=15, space_before=4)

    # Right Diagram
    d_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.3), Inches(4.2), Inches(5.4))
    d_card.fill.solid()
    d_card.fill.fore_color.rgb = c_card_bg
    d_card.line.color.rgb = c_border

    img_outer = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.2), Inches(3.2))
    img_outer.fill.solid()
    img_outer.fill.fore_color.rgb = RGBColor(241, 245, 249)
    img_outer.line.color.rgb = c_dark
    img_outer.line.width = Pt(1.5)

    v_line = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.37), Inches(1.8), Inches(0.04), Inches(3.2))
    v_line.fill.solid()
    v_line.fill.fore_color.rgb = c_crimson
    v_line.line.color.rgb = c_crimson

    h_line = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.8), Inches(3.37), Inches(3.2), Inches(0.04))
    h_line.fill.solid()
    h_line.fill.fore_color.rgb = c_crimson
    h_line.line.color.rgb = c_crimson

    c_anchor = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.3), Inches(2.3), Inches(2.2), Inches(2.2))
    c_anchor.fill.background()
    c_anchor.line.color.rgb = c_green
    c_anchor.line.width = Pt(3)

    c_donor = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.8), Inches(2.8), Inches(1.2), Inches(1.2))
    c_donor.fill.solid()
    c_donor.fill.fore_color.rgb = RGBColor(254, 226, 226)
    c_donor.line.color.rgb = c_crimson
    c_donor.line.width = Pt(2)
    dtf = c_donor.text_frame
    dtf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = dtf.paragraphs[0]
    p.text = "Donor"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_crimson
    p.alignment = PP_ALIGN.CENTER

    lbl_top = s9.shapes.add_textbox(Inches(8.8), Inches(1.85), Inches(3.2), Inches(0.4))
    p = lbl_top.text_frame.paragraphs[0]
    p.text = "Center Anchor Crop"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = c_green
    p.alignment = PP_ALIGN.CENTER

    lbl_bot = s9.shapes.add_textbox(Inches(8.4), Inches(5.2), Inches(4.0), Inches(0.8))
    p = lbl_bot.text_frame.paragraphs[0]
    p.text = "Figure: Center anchor capturing donor intact."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER

    add_footer(s9, 9)

    # ==========================================================================
    # SLIDE 10: LEARNED MLP IMPORTANCE GATE
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Methodology: Learned MLP Importance Gate")

    cbox = s10.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(5.5))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "• The Idea:", "Not all patches are equally useful. Background patches are repetitive (sky, grass, road) and already match Parent A. We need the model to pay attention to the spliced donor.", space_before=8)
    add_bullet(tf, "• How it works:", space_before=16)
    add_bullet(tf, "–", "We feed each patch embedding into a tiny 2-layer neural network (MLP).", level=1, size=15, space_before=4)
    add_bullet(tf, "–", "The MLP assigns an importance weight between 0 and 1 to each patch.", level=1, size=15, space_before=4)
    add_bullet(tf, "–", "Patches containing the donor object get high weights (≈ 0.45), while background patches get near zero.", level=1, size=15, space_before=4)

    add_bullet(tf, "• Fast & Lightweight:", space_before=16, bold_color=c_green)
    add_bullet(tf, "–", "Contains less than 70,000 parameters.", level=1, size=15, space_before=4)
    add_bullet(tf, "–", "Trains in under 1 minute on a free GPU without touching or fine-tuning the heavy foundation model.", level=1, size=15, space_before=4)

    add_footer(s10, 10)

    # ==========================================================================
    # SLIDE 11: EXPERIMENTAL SETUP
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Experimental Setup")

    cbox = s11.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(5.5))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "• 100% Real Photographs:", "Used real-world natural images from the official MS-COCO 2017 dataset (people, vehicles, animals, indoor/outdoor scenes).", space_before=8)
    add_bullet(tf, "• Gallery Database:", "1,000 unindexed natural photos acting as the search space.", space_before=14)
    add_bullet(tf, "• Composite Queries:", "300 realistic photographic composites created with Gaussian edge blending (donor size controlled between 15%–35%).", space_before=14)
    add_bullet(tf, "• Data Splits:", "70% Training (210 queries), 15% Validation (45 queries), and 15% Held-Out Test (45 queries).", space_before=14)
    add_bullet(tf, "• Hardware:", "NVIDIA Tesla T4 GPU running on cloud environment.", space_before=14)
    add_bullet(tf, "• Primary Metric:", "Full Lineage Recall@5 (Did the top 5 results contain BOTH Parent A and Parent B?).", space_before=14)

    add_footer(s11, 11)

    # ==========================================================================
    # SLIDE 12: EXPERIMENTAL RESULTS TABLE
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Experimental Results (Held-Out Test Set)")

    rows, cols = 6, 5
    table_shape = s12.shapes.add_table(rows, cols, Inches(0.8), Inches(1.35), Inches(11.733), Inches(2.7))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(4.6)
    tbl.columns[1].width = Inches(1.7)
    tbl.columns[2].width = Inches(1.7)
    tbl.columns[3].width = Inches(2.0)
    tbl.columns[4].width = Inches(1.733)

    data = [
        ["Method / Architecture", "Parent A", "Parent B", "Full Lineage", "Latency"],
        ["Global SSCD Baseline", "100.00%", "51.11%", "51.11%", "193 ms"],
        ["Uniform Local (Rigid 2 × 2, 3 × 3)", "100.00%", "53.33%", "53.33%", "2277 ms"],
        ["Uniform Local (Dynamic Overlap)", "100.00%", "75.56%", "75.56%", "2117 ms"],
        ["SSCD + MLP Gate (Rigid)", "100.00%", "82.22%", "82.22%", "2265 ms"],
        ["SSCD + MLP Gate (Dynamic) [Ours]", "100.00%", "88.89%", "88.89%", "2125 ms"]
    ]

    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
            p.font.size = Pt(13)
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = c_navy
                p.font.bold = True
                p.font.color.rgb = c_white
            elif r_idx == 5:
                cell.fill.solid()
                cell.fill.fore_color.rgb = c_green_bg
                p.font.bold = True
                p.font.color.rgb = c_green
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = c_white if r_idx % 2 == 1 else c_card_bg
                p.font.color.rgb = c_dark

    k_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.4))
    k_card.fill.solid()
    k_card.fill.fore_color.rgb = c_card_bg
    k_card.line.color.rgb = c_border
    ktf = k_card.text_frame
    ktf.word_wrap = True
    
    p = ktf.paragraphs[0]
    p.text = "Key Takeaways"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    add_bullet(ktf, "• Global baseline misses half the donors:", "Achieves only 51.11% full lineage.", level=0, size=14, space_before=6)
    add_bullet(ktf, "• Dynamic slicing gives an instant +22.23% leap:", "Proves boundary crossing was the main reason rigid grids failed.", level=0, size=14, space_before=4)
    add_bullet(ktf, "• Proposed system achieves 88.89%:", "Near 9 out of 10 composites have both source parents retrieved in top 5!", level=0, size=14, space_before=4)

    add_footer(s12, 12)

    # ==========================================================================
    # SLIDE 13: DISCUSSION OF RESULTS
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Discussion: Why Did Our Method Work So Well?")

    cbox = s13.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(5.5))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "1. Dynamic Slicing Fixed Object Cutting (+22.23% gain):", space_before=6, bold_color=c_navy)
    add_bullet(tf, "–", "By simply introducing center-anchors and overlapping crops, the donor object is always captured in full in at least one crop.", level=1, size=15, space_before=4)

    add_bullet(tf, "2. The Gate Filtered Out Background Clutter (+13.33% gain):", space_before=16, bold_color=c_navy)
    add_bullet(tf, "–", "Background patches (sky, ground) generated false matches with other gallery images.", level=1, size=15, space_before=4)
    add_bullet(tf, "–", "The MLP gate assigned near-zero weight to these clutter patches and focused search attention strictly on the donor object.", level=1, size=15, space_before=4)

    add_bullet(tf, "3. Background Accuracy Remained at 100%:", space_before=16, bold_color=c_navy)
    add_bullet(tf, "–", "By keeping a dedicated global channel for Parent A, we never sacrificed background recall while hunting for the donor.", level=1, size=15, space_before=4)

    add_footer(s13, 13)

    # ==========================================================================
    # SLIDE 14: FUTURE WORK
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Future Work: Blockchain-Audited Media Lineage")

    cbox = s14.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(5.5))
    tf = cbox.text_frame
    tf.word_wrap = True

    add_bullet(tf, "• Why Blockchain?", "Visual AI can retrieve candidate images, but cannot legally prove which image was created first. A malicious user can claim their composite is the original.", space_before=6)

    add_bullet(tf, "• On-Chain Hash Notarization:", space_before=14)
    add_bullet(tf, "–", "When a creator takes a photo, its SHA-256 visual hash is recorded onto an immutable blockchain (e.g., Polygon / Ethereum).", level=1, size=15, space_before=3)
    add_bullet(tf, "–", "Gives each photo an unalterable, tamper-proof timestamp.", level=1, size=15, space_before=3)

    add_bullet(tf, "• Smart Contract Provenance Auditing:", space_before=14, bold_color=c_navy)
    add_bullet(tf, "–", "A smart contract verifies the lineage condition:", level=1, size=15, space_before=3)

    fcard = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(4.9), Inches(9.733), Inches(1.1))
    fcard.fill.solid()
    fcard.fill.fore_color.rgb = c_navy
    fcard.line.color.rgb = c_navy
    ftf = fcard.text_frame
    ftf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = ftf.paragraphs[0]
    p.text = "Timestamp(Parent A) < Timestamp(Query)\n∧  Timestamp(Parent B) < Timestamp(Query)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.alignment = PP_ALIGN.CENTER

    lbox2 = s14.shapes.add_textbox(Inches(1.2), Inches(6.1), Inches(11.0), Inches(0.8))
    p = lbox2.text_frame.paragraphs[0]
    p.text = "– If verified, the smart contract automatically settles copyright attribution or licensing royalties between creators."
    p.font.size = Pt(15)
    p.font.color.rgb = c_dark

    add_footer(s14, 14)

    # ==========================================================================
    # SLIDE 15: CONCLUSION & REFERENCES
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Conclusion & Key References")

    scard = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(2.2))
    scard.fill.solid()
    scard.fill.fore_color.rgb = c_card_bg
    scard.line.color.rgb = c_border
    stf = scard.text_frame
    stf.word_wrap = True
    p = stf.paragraphs[0]
    p.text = "Summary of Contributions:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    add_bullet(stf, "•", "Solved the Background Dominance Paradox in multi-source image attribution without retraining heavy vision backbones.", level=0, size=14, space_before=5)
    add_bullet(stf, "•", "Dynamic overlapping tokenization resolved boundary cuts, boosting recall by +22%.", level=0, size=14, space_before=3)
    add_bullet(stf, "•", "Our lightweight MLP gate achieved 88.89% Full Lineage Recall@5 on real photos.", level=0, size=14, space_before=3)

    rcard = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(11.733), Inches(2.3))
    rcard.fill.solid()
    rcard.fill.fore_color.rgb = c_card_bg
    rcard.line.color.rgb = c_border
    rtf = rcard.text_frame
    rtf.word_wrap = True
    p = rtf.paragraphs[0]
    p.text = "Key References:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    refs = [
        "1. E. Pizzi et al., \"A Self-Supervised Descriptor for Image Copy Detection,\" CVPR, 2022.",
        "2. F. Guillaro et al., \"TruFor: Leveraging All-Round Clues for Forgery Detection,\" CVPR, 2023.",
        "3. J. Chen, J. Yao, L. Niu, \"A Single Simple Patch is All You Need for AI-generated Image Detection,\" arXiv:2402.01123, 2024.",
        "4. Z. Li, J. Yan, Z. He, K. Zeng, et al., \"Is Artificial Intelligence Generated Image Detection a Solved Problem? (AIGIBench),\" NeurIPS, 2025."
    ]
    for r in refs:
        p = rtf.add_paragraph()
        p.text = r
        p.font.size = Pt(12)
        p.font.color.rgb = c_dark
        p.space_before = Pt(3)

    tbox = s15.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.7))
    p = tbox.text_frame.paragraphs[0]
    p.text = "Thank You!   Questions & Discussion"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.alignment = PP_ALIGN.CENTER

    add_footer(s15, 15)

    out_file = "/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/negi_thesis_2027.pptx"
    prs.save(out_file)
    print(f"[SUCCESS] Saved as {out_file}")

if __name__ == "__main__":
    build_presentation()
