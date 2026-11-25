import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py_modules'))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_10slide_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Executive Pink / Rose Palette (Academic Presentation)
    c_blue = RGBColor(219, 39, 119)       # Vibrant Rose Pink
    c_navy = RGBColor(112, 16, 56)        # Deep Velvet Plum
    c_dark = RGBColor(30, 41, 59)         # Slate Charcoal Text
    c_gray_bg = RGBColor(253, 242, 248)   # Soft Blush Background
    c_gray_border = RGBColor(244, 114, 182) # Soft Pink Border
    c_white = RGBColor(255, 255, 255)
    c_green = RGBColor(16, 185, 129)      # Emerald Green
    c_green_bg = RGBColor(236, 253, 245)
    c_amber = RGBColor(245, 158, 11)      # Warning Amber
    c_crimson = RGBColor(225, 29, 72)
    c_footer_gray = RGBColor(253, 242, 248)

    def add_footer(slide, current_slide, total_slides=11):
        footer_top = Inches(7.05)
        footer_height = Inches(0.45)
        
        # Author Box
        b1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), footer_top, Inches(5.8), footer_height)
        b1.fill.solid()
        b1.fill.fore_color.rgb = c_blue
        b1.line.color.rgb = c_blue
        tf1 = b1.text_frame
        tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = tf1.paragraphs[0]
        p1.text = "Vivek Negi – T25CS012 (NIT Meghalaya)"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = c_white
        p1.alignment = PP_ALIGN.CENTER
        
        # Topic Box
        b2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), footer_top, Inches(6.0), footer_height)
        b2.fill.solid()
        b2.fill.fore_color.rgb = c_footer_gray
        b2.line.color.rgb = c_footer_gray
        tf2 = b2.text_frame
        tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = tf2.paragraphs[0]
        p2.text = "M.Tech Thesis DAC Progress Review (7-Min)"
        p2.font.size = Pt(11)
        p2.font.color.rgb = c_dark
        p2.alignment = PP_ALIGN.CENTER

        # Slide Number Box
        b3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.8), footer_top, Inches(1.533), footer_height)
        b3.fill.solid()
        b3.fill.fore_color.rgb = c_navy
        b3.line.color.rgb = c_navy
        tf3 = b3.text_frame
        tf3.vertical_anchor = MSO_ANCHOR.MIDDLE
        p3 = tf3.paragraphs[0]
        p3.text = f"{current_slide} / {total_slides}"
        p3.font.size = Pt(11)
        p3.font.bold = True
        p3.font.color.rgb = c_white
        p3.alignment = PP_ALIGN.CENTER

    def add_header(slide, title_text, category_tag=""):
        header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05))
        header.fill.solid()
        header.fill.fore_color.rgb = c_navy
        header.line.color.rgb = c_navy
        
        tf = header.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.LEFT
        tf.margin_left = Inches(0.8)

    def create_card(slide, left, top, width, height, title="", title_color=c_blue, bg_color=c_gray_bg, border_color=c_gray_border):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.25)
        tf.margin_right = Inches(0.3)
        tf.margin_bottom = Inches(0.2)
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(8)
        return tf

    def add_bullet(tf, bold_prefix, text="", size=14, space_before=6, bold_color=c_navy):
        p = tf.add_paragraph() if len(tf.paragraphs[0].text) > 0 else tf.paragraphs[0]
        p.space_before = Pt(space_before)
        if bold_prefix:
            r1 = p.add_run()
            r1.text = bold_prefix + (" " if text else "")
            r1.font.bold = True
            r1.font.size = Pt(size)
            r1.font.color.rgb = bold_color
        if text:
            r2 = p.add_run()
            r2.text = text
            r2.font.size = Pt(size)
            r2.font.color.rgb = c_dark

    # ==========================================================================
    # SLIDE 1: TITLE PAGE
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    t_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(2.2))
    t_box.fill.solid()
    t_box.fill.fore_color.rgb = c_navy
    t_box.line.color.rgb = c_blue
    t_box.line.width = Pt(2.5)
    tf1 = t_box.text_frame
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "ProvenanceAI: Multi-Source Media Lineage Retrieval\nand Cryptographic Proof-of-Provenance Verification"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.alignment = PP_ALIGN.CENTER

    p2 = tf1.add_paragraph()
    p2.text = "M.Tech Thesis DAC Progress Review (Strictly 10 Slides | 7-Minute Review)"
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(186, 230, 253)
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    m_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(3.1), Inches(10.333), Inches(3.6))
    m_card.fill.solid()
    m_card.fill.fore_color.rgb = c_gray_bg
    m_card.line.color.rgb = c_gray_border
    mtf = m_card.text_frame
    mtf.word_wrap = True
    
    p = mtf.paragraphs[0]
    p.text = "Vivek Negi"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER
    
    p = mtf.add_paragraph()
    p.text = "Roll Number: T25CS012"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(4)

    p = mtf.add_paragraph()
    p.text = "Under the Supervision of"
    p.font.size = Pt(14)
    p.font.color.rgb = c_dark
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(14)

    p = mtf.add_paragraph()
    p.text = "Dr. Akhilendra Pratap Singh"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(4)

    p = mtf.add_paragraph()
    p.text = "Department of Computer Science and Engineering\nNational Institute of Technology Meghalaya, Sohra"
    p.font.size = Pt(15)
    p.font.color.rgb = c_dark
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(4)

    p = mtf.add_paragraph()
    p.text = "Review Date: November 18, 2026"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(10)

    # ==========================================================================
    # SLIDE 2: MOTIVATION & PROBLEM STATEMENT
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Motivation: What is Composite Media Lineage?")
    add_footer(s2, 2)

    c2_1 = create_card(s2, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "The Problem: Multi-Source Derivatives")
    add_bullet(c2_1, "Single-Source vs Composite Media:", "Traditional reverse search (Google Lens, TinEye) assumes 1-to-1 duplication. Real-world tampering fuses multiple parents.")
    add_bullet(c2_1, "Parent A (Background Plate):", "Covers 70%–85% of the canvas (e.g., scenic highway, empty crime scene desk).")
    add_bullet(c2_1, "Parent B (Spliced Donor Object):", "Localized critical asset covering only 10%–30% of pixels (e.g., 9mm handgun, HSRP license plate).")
    add_bullet(c2_1, "The Core Objective:", "Given a query composite Q, accurately trace both Parent A and Parent B from an open-world gallery of authenticated images.")

    c2_2 = create_card(s2, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "High-Stakes Forensic Threat Models")
    add_bullet(c2_2, "1. Crime Scene Evidence Contraband Planting:", "Placing a weapon on an innocent suspect's desk to falsify violent criminal offenses.")
    add_bullet(c2_2, "2. Vehicle Hit-and-Run Registration Tampering:", "Splicing High-Security Registration Plates (HSRP) onto getaway cars to mislead police APNR cameras.")
    add_bullet(c2_2, "3. Alibi & VIP Presence Fabrication:", "Compositing individuals into remote locations (e.g., mountain overlooks) to engineer fake alibis.")
    add_bullet(c2_2, "Evidentiary Requirement:", "Courts mandate mathematical proof of both parent identities and cryptographically certified temporal precedence.")

    # ==========================================================================
    # SLIDE 3: THE BACKGROUND DOMINANCE PARADOX
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Core Technical Problem: Background Dominance Paradox")
    add_footer(s3, 3)

    c3_1 = create_card(s3, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "The Global Average Pooling (GAP) Flaw")
    add_bullet(c3_1, "How Vision Models Form Representations:", "SOTA models (Meta SSCD, ResNet-50, CLIP) condense feature maps into a single global vector v ∈ R^D.")
    add_bullet(c3_1, "Mathematical Area Imbalance:", "Because Parent A occupies ≥75% of the pixels, background activations completely dominate the embedding sum.")
    add_bullet(c3_1, "The Cosine Similarity Trap:", "cos(v_query, v_ParentA) ≈ 0.96 (100% Top-1 Recall) while cos(v_query, v_ParentB) ≤ 0.42 (Drops out of Top-50).")
    add_bullet(c3_1, "Baseline Failure:", "Standard SSCD achieves 0% dual-parent recall on multi-source composites.")

    c3_2 = create_card(s3, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Why Rigid Tile Slicing Fails")
    add_bullet(c3_2, "Naive Grid Partitioning (2x2 / 3x3):", "Splitting an image into non-overlapping square tiles breaks down in practical forensics.")
    add_bullet(c3_2, "Boundary Fragmentation:", "Objects placed near image centers (e.g., license plates or handguns) are bisected into 4 separate quadrants.")
    add_bullet(c3_2, "Loss of Semantic Coherence:", "A quarter of a handgun or half a license plate cannot match full-object gallery embeddings.")
    add_bullet(c3_2, "Combinatorial Explosion:", "Naive patch comparisons explode search latency across large databases without intelligent gating.")

    # ==========================================================================
    # SLIDE 4: LITERATURE REVIEW & RESEARCH GAPS
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Literature Review & Research Gaps")
    add_footer(s4, 4)

    # Table Shape
    t_shape = s4.shapes.add_table(5, 4, Inches(0.8), Inches(1.3), Inches(11.733), Inches(3.8))
    t = t_shape.table
    t.columns[0].width = Inches(2.3)
    t.columns[1].width = Inches(3.2)
    t.columns[2].width = Inches(3.2)
    t.columns[3].width = Inches(3.033)

    headers = ["Author / Framework", "Core Methodology", "Critical Limitation", "ProvenanceAI Advantage"]
    for j, h in enumerate(headers):
        cell = t.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = c_white

    data = [
        ("Pizzi et al.\n(CVPR 2022 SSCD)", "Self-Supervised Contrastive Learning with entropy regularization", "Holistic global pooling completely drops localized donors (<30%)", "Decouples background from localized patch consensus"),
        ("Guillaro et al.\n(CVPR 2023 TruFor)", "Transformer-based tamper mask localization + Noiseprint++", "Localizes pixel tampering but CANNOT retrieve donor from database", "Retrieves physical parent assets from large-scale gallery"),
        ("C2PA Standard\n(Adobe / MS 2024)", "Hardware-signed cryptographic EXIF metadata manifests", "Vulnerable to social media stripping (WhatsApp, Web, compression)", "Perceptual visual hashing independent of fragile EXIF"),
        ("ProvenanceAI\n(Our Proposed)", "Dynamic Tokenizer + Saliency Gate + SHA-256 Merkle Ledger", "Solved dual-parent lineage recovery & legal precedence", "88.89% Dual-Lineage Recall@5 + 129 Immutable Blocks")
    ]

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = t.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_green_bg if i == 3 else (c_gray_bg if i % 2 == 1 else c_white)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = c_navy if i == 3 else c_dark
            if i == 3:
                p.font.bold = True

    c4_b = create_card(s4, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.5), "Key Research Gap Summary")
    add_bullet(c4_b, "The Open Scientific Gap:", "No prior framework bridges localized visual donor retrieval with cryptographic temporal precedence. ProvenanceAI is the first system to achieve both simultaneously.", size=13, space_before=2)

    # ==========================================================================
    # SLIDE 5: PROPOSED ARCHITECTURE
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Proposed Architecture: Two-Stream Neural Patch Consensus")
    add_footer(s5, 5)

    c5_1 = create_card(s5, Inches(0.8), Inches(1.3), Inches(3.7), Inches(5.5), "1. Dynamic Tokenizer")
    add_bullet(c5_1, "Multi-Scale Slicing:", "Sliding overlapping windows across 25%, 35%, and 50% canvas dimensions.", size=13)
    add_bullet(c5_1, "50% Stride Overlap:", "Guarantees donor objects are captured intact without boundary truncation.", size=13)
    add_bullet(c5_1, "Scale Invariance:", "Handles both micro-donors (license plates) and macro-donors (human subjects).", size=13)

    c5_2 = create_card(s5, Inches(4.8), Inches(1.3), Inches(3.7), Inches(5.5), "2. Saliency Gate (MLP)")
    add_bullet(c5_2, "Learned Attention:", "2-Layer MLP evaluates patch variance and edge entropy to assign weight w_i ∈ [0, 1].", size=13)
    add_bullet(c5_2, "Mathematical Gate:", "w_i = σ(W_2 · ReLU(W_1 f_i + b_1) + b_2)", size=13)
    add_bullet(c5_2, "Noise Elimination:", "Downweights blank sky and uniform background patches to 0.", size=13)

    c5_3 = create_card(s5, Inches(8.8), Inches(1.3), Inches(3.7), Inches(5.5), "3. Consensus Aggregator")
    add_bullet(c5_3, "Trained Alpha Tuning:", "Balances global background vs. local donor consensus (α = 0.25).", size=13)
    add_bullet(c5_3, "Scoring Formula:", "Score = 0.25 · S_global + 0.75 · max_i(w_i · cos(f_i, g_j))", size=13)
    add_bullet(c5_3, "Outcome:", "75% local patch consensus rescues suppressed donor without degrading background.", size=13)

    # ==========================================================================
    # SLIDE 6: BLOCKCHAIN PROOF-OF-PROVENANCE
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Cryptographic Layer: Proof-of-Provenance Blockchain")
    add_footer(s6, 6)

    c6_1 = create_card(s6, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Why AI Alone Fails in Courtrooms")
    add_bullet(c6_1, "Statistical vs. Legal Proof:", "AI outputs probability scores (e.g., 94% similarity). It cannot prove WHO created an image first.")
    add_bullet(c6_1, "The Reverse-Attribution Attack:", "A malicious actor can download an authentic photo, forge a composite, and claim their composite was original.")
    add_bullet(c6_1, "The Legal Precedence Theorem:", "A composite Q is a proven forgery if and only if both parent assets exist on-chain with earlier timestamps: Time(Parent A) < Time(Q) ∧ Time(Parent B) < Time(Q).")

    c6_2 = create_card(s6, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Decentralized SHA-256 Ledger Implementation")
    add_bullet(c6_2, "Immutable Ledger State:", "129 verified blocks actively mined with SHA-256 hash pointers and Proof-of-Work nonces.")
    add_bullet(c6_2, "On-Chain Notarization:", "Every parent photograph, transparent donor, and composite is cryptographically hashed at registration.")
    add_bullet(c6_2, "Merkle DAG Certification:", "The engine automatically generates tamper-evident JSON audit receipts linking composite hashes to on-chain parent blocks.")
    add_bullet(c6_2, "Admissibility:", "Meets strict digital forensics chain-of-custody standards.")

    # ==========================================================================
    # SLIDE 7: SOFTWARE ARCHITECTURE & TECH STACK
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Implementation Details & Computational Software Stack")
    add_footer(s7, 7)

    t7_shape = s7.shapes.add_table(6, 3, Inches(0.8), Inches(1.3), Inches(11.733), Inches(3.8))
    t7 = t7_shape.table
    t7.columns[0].width = Inches(3.0)
    t7.columns[1].width = Inches(4.5)
    t7.columns[2].width = Inches(4.233)

    h7 = ["Subsystem Layer", "Technology / Framework", "Operational Function"]
    for j, h in enumerate(h7):
        cell = t7.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = c_white

    d7 = [
        ("Core Neural Pipeline", "Python 3.9+, NumPy, PyTorch", "Feature extraction, vector tokenization, MLP gating"),
        ("Hardware Acceleration", "Apple Silicon MPS / NVIDIA CUDA", "Sub-second tensor inference (<0.40s per audit)"),
        ("Forensic VFX Studio", "Pillow (PIL), OpenCV, ImageEnhance", "Alpha matting, de-fringing, Ambient Occlusion (AO)"),
        ("Blockchain Protocol", "Python hashlib (SHA-256)", "Mining Proof-of-Precedence blocks & Merkle DAG receipts"),
        ("Interactive UI Suite", "Streamlit Multi-Tab Dashboard", "5-Tab executive forensic workbench on port 8502")
    ]

    for i, row in enumerate(d7):
        for j, val in enumerate(row):
            cell = t7.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_gray_bg if i % 2 == 1 else c_white
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = c_dark

    c7_b = create_card(s7, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.5), "Enterprise Security & Zero Cloud Dependency")
    add_bullet(c7_b, "Local Air-Gapped Security:", "100% local computation. No proprietary police or judicial evidence is ever transmitted to commercial third-party cloud APIs (OpenAI, AWS).", size=13, space_before=2)

    # ==========================================================================
    # SLIDE 8: EXPERIMENTAL RESULTS & REAL-WORLD DATASETS
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Experimental Evaluation & Real-World Evidentiary Scenarios")
    add_footer(s8, 8)

    c8_1 = create_card(s8, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Benchmark Results (thesis2027 Split)")
    add_bullet(c8_1, "Global Baseline (SSCD):", "Parent A: 100.0% | Parent B: 44.44% | Lineage Recall@5: 44.44%")
    add_bullet(c8_1, "Rigid 2x2 Grid Tiles:", "Parent A: 100.0% | Parent B: 66.67% | Lineage Recall@5: 66.67%")
    add_bullet(c8_1, "Rigid 3x3 Grid Tiles:", "Parent A: 100.0% | Parent B: 66.67% | Lineage Recall@5: 66.67%")
    add_bullet(c8_1, "ProvenanceAI (Our Proposed):", "Parent A: 100.0% | Parent B: 88.89% | Lineage Recall@5: 88.89%", bold_color=c_green)
    add_bullet(c8_1, "Net Breakthrough:", "+44.45% absolute improvement over SOTA copy detection baselines.", size=13)

    c8_2 = create_card(s8, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Evaluated on 40+ Authentic Real Photographs")
    add_bullet(c8_2, "Case 1: Vehicle License Plate Tampering:", "Porsche sports car + Indian HSRP Plate (DL 01 AB 4921) -> 99.8% A, 92.4% B.")
    add_bullet(c8_2, "Case 2: Crime Scene Weapon Fabrication:", "Wooden office desk + Tactical 9mm Handgun -> 99.9% A, 96.5% B.")
    add_bullet(c8_2, "Case 3: Mountain Overlook Alibi Fraud:", "Scenic overlook + Studio young man -> 99.96% A, 92.4% B.")
    add_bullet(c8_2, "Case 4: Pedestrian Urban Splicing:", "City crosswalk + Blonde woman in trench coat -> 99.88% A, 92.4% B.")
    add_bullet(c8_2, "Case 5 & 6: Campus & Workspace Splicing:", "Modern library hall + leather backpack & Work desk + luxury watch -> 99.9% A, 98.3% B.")

    # ==========================================================================
    # SLIDE 9: FAILURE MODES: GENERATIVE DIFFUSION & SPECTRAL GATING
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Failure Mode Analysis: Latent Diffusion Boundary & 2D FFT Spectral Gating")
    add_footer(s9, 9)

    c9_1 = create_card(s9, Inches(0.8), Inches(1.18), Inches(5.7), Inches(2.35), "Where Physical Splicing Retrieval Fails")
    add_bullet(c9_1, "Generative Latent Inpainting:", "When media is modified via Meta AI Emu / SD 3.5, NO physical donor image exists in the real world.")
    add_bullet(c9_1, "The False-Neighbor Trap:", "Unguided nearest-neighbor search forced false matches (matching synthetic sun to yellow headphones based on color).")
    add_bullet(c9_1, "Root Cause:", "Diffusion decoders synthesize in latent space Z, lacking natural camera sensor Photo-Response Non-Uniformity (PRNU).")

    c9_2 = create_card(s9, Inches(6.8), Inches(1.18), Inches(5.7), Inches(2.35), "Our Solution: 2D FFT Radial Spectral Gating")
    add_bullet(c9_2, "Spectral Decision Rule:", "Measures high-frequency power ratio E_HF = sum_{r > r_c} S(u,v) / sum S(u,v) across suspect patches.")
    add_bullet(c9_2, "Synthetic Signature Detection:", "Diffusion synthesis leaves characteristic outer-rim frequency roll-offs and deconvolution cross-spikes.")
    add_bullet(c9_2, "Null-Hypothesis Rejection Gate:", "If E_HF < 0.880, engine refuses false donor retrieval and flags: 'Synthetic Latent Inpainting (No Physical Donor)'.")

    # Forensic Visual: Real Camera vs AI Diffusion 2D FFT Comparison
    fft_fig_path = os.path.join(os.path.dirname(__file__), "fft_diffusion_vs_real_comparison.png")
    if os.path.exists(fft_fig_path):
        s9.shapes.add_picture(fft_fig_path, Inches(0.8), Inches(3.62), Inches(11.733), Inches(3.18))

    # ==========================================================================
    # SLIDE 10: DEPLOYMENT & FUTURE ENGINEERING SCOPE
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Deployment & Future Engineering Scope")
    add_footer(s10, 10)

    c10_1 = create_card(s10, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Remote Deployment & Public Demonstration")
    add_bullet(c10_1, "Public Live Demonstration Link:", "To demonstrate the dashboard to remote reviewers and committee members without local setups:")
    add_bullet(c10_1, "Local Operational Lab Host:", "http://localhost:8502 (Active on laboratory machine)", bold_color=c_blue)
    add_bullet(c10_1, "Secure Public Live Tunnel:", "https://uuunw-115-245-187-126.run.pinggy-free.link (Operational SSL Tunnel)", bold_color=c_green)
    add_bullet(c10_1, "Interactive Verification:", "External evaluators can upload suspect composites and inspect on-chain provenance in real time.")

    c10_2 = create_card(s10, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Modular Technical Scope & Completion Status")
    add_bullet(c10_2, "1. Video-Stream Provenance:", "Extending patch consensus to temporal keyframes in short-form video clips (Reels/Shorts).")
    add_bullet(c10_2, "2. Mobile-Edge Quantization:", "INT8 weight quantization of the Importance Gate MLP for offline smartphone verification.")
    add_bullet(c10_2, "3. Interactive Lineage GUI:", "Expanding the Streamlit interface with interactive, zoomable Directed Acyclic Graph (DAG) trees.")
    add_bullet(c10_2, "Thesis Completion Status:", "All core research requirements fully accomplished, benchmarked at 88.89% recall, and ready for defense.", bold_color=c_navy)

    # ==========================================================================
    # SLIDE 11: KEY REFERENCES & LITERATURE CITATIONS
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Key References & Literature Citations")
    add_footer(s11, 11, total_slides=11)

    c11_1 = create_card(s11, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Foundational Literature (2012–2022)")
    add_bullet(c11_1, "Moreira et al. (IEEE T-IFS 2018):", "Image Provenance Analysis at Scale. Established pairwise image graph formulation and minimum spanning trees.")
    add_bullet(c11_1, "Pizzi et al. (CVPR 2022 SSCD):", "A Self-Supervised Descriptor for Image Copy Detection. State-of-the-art holistic copy detection benchmark.")
    add_bullet(c11_1, "Dias, Rocha & Goldenstein (IEEE TPAMI 2012):", "Image Phylogeny by Minimal Spanning Trees. Original mathematical foundation of media genealogy.")

    c11_2 = create_card(s11, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Modern Standards & AI Forensics (2023–2026)")
    add_bullet(c11_2, "Guillaro et al. (CVPR 2023 TruFor):", "Leveraging All-Round Clues for Trustworthy Image Forgery Detection with Noiseprint++ camera artifacts.")
    add_bullet(c11_2, "C2PA Technical Standard (2024):", "Content Credentials Architecture for Digital Media Authenticity (Adobe, Microsoft, Intel).")
    add_bullet(c11_2, "Chen et al. (2024) & Li et al. (NeurIPS 2025):", "Single Simple Patch & AIGIBench benchmark for synthetic and inpainting detection.")
    add_bullet(c11_2, "Summary & Acknowledgement:", "Thank You! Welcoming questions and discussion from the DAC committee.", bold_color=c_navy)

    # Save outputs
    out_dac = os.path.join(os.path.dirname(__file__), "DAC_Review_Vivek_Negi_10Slides.pptx")
    out_main = os.path.join(os.path.dirname(__file__), "Multi_Source_Media_Lineage_NITM.pptx")
    prs.save(out_dac)
    prs.save(out_main)
    print(f"Successfully generated strictly 11-slide PowerPoint presentations:")
    print(f"1. {out_dac}")
    print(f"2. {out_main}")

if __name__ == "__main__":
    build_10slide_deck()
