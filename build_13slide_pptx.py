#!/usr/bin/env python3
"""
build_13slide_pptx.py
Builds the comprehensive 13-slide master presentation deck for Vivek Negi's M.Tech CSE DAC Progress Review:
- Features Slide 3: "Anatomy of a Composite Image: How Forgery is Formed" (with composite_formation_pipeline.png)
- Features Slide 11: "2D FFT Spectral Forensics & Radial Gating" (with fft_diffusion_vs_real_comparison.png)
- Strictly 13 slides (< 15 pages), executive pink/rose palette, warning-free.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py_modules'))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_13slide_deck():
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

    def add_footer(slide, current_slide, total_slides=13):
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
        p1.alignment = PP_ALIGN.LEFT
        p1.margin_left = Inches(0.5)

        # Context Box
        b2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), footer_top, Inches(6.0), footer_height)
        b2.fill.solid()
        b2.fill.fore_color.rgb = c_navy
        b2.line.color.rgb = c_navy
        tf2 = b2.text_frame
        tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = tf2.paragraphs[0]
        p2.text = "M.Tech Thesis DAC Progress Review (Comprehensive 13-Slide Defense)"
        p2.font.size = Pt(11)
        p2.font.color.rgb = c_white
        p2.alignment = PP_ALIGN.LEFT
        p2.margin_left = Inches(0.3)

        # Slide Number Box
        b3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.8), footer_top, Inches(1.533), footer_height)
        b3.fill.solid()
        b3.fill.fore_color.rgb = c_blue
        b3.line.color.rgb = c_blue
        tf3 = b3.text_frame
        tf3.vertical_anchor = MSO_ANCHOR.MIDDLE
        p3 = tf3.paragraphs[0]
        p3.text = f"{current_slide} / {total_slides}"
        p3.font.size = Pt(12)
        p3.font.bold = True
        p3.font.color.rgb = c_white
        p3.alignment = PP_ALIGN.CENTER

    def add_header(slide, title_text, category_tag=""):
        header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05))
        header.fill.solid()
        header.fill.fore_color.rgb = c_white
        header.line.color.rgb = c_gray_border
        tf = header.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.8)
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.03), Inches(13.333), Inches(0.04))
        rule.fill.solid()
        rule.fill.fore_color.rgb = c_blue
        rule.line.color.rgb = c_blue

    def create_card(slide, left, top, width, height, title="", title_color=c_blue, bg_color=c_gray_bg, border_color=c_gray_border):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(8)
        return card

    def add_bullet(card, bold_prefix, text_body, pt_size=11, space_after=6):
        tf = card.text_frame
        p = tf.add_paragraph()
        p.space_after = Pt(space_after)
        p.font.size = Pt(pt_size)
        
        run_bullet = p.add_run()
        run_bullet.text = "• "
        run_bullet.font.bold = True
        run_bullet.font.color.rgb = c_blue
        
        run_bold = p.add_run()
        run_bold.text = bold_prefix + " "
        run_bold.font.bold = True
        run_bold.font.color.rgb = c_navy
        
        run_text = p.add_run()
        run_text.text = text_body
        run_text.font.color.rgb = c_dark

    # ==========================================================================
    # SLIDE 1: TITLE PAGE
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_white
    bg1.line.fill.background()

    band = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.25))
    band.fill.solid()
    band.fill.fore_color.rgb = c_blue
    band.line.fill.background()

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.9))
    card1.fill.solid()
    card1.fill.fore_color.rgb = c_gray_bg
    card1.line.color.rgb = c_gray_border
    card1.line.width = Pt(2)
    tf1 = card1.text_frame
    tf1.word_wrap = True
    tf1.margin_top = Inches(0.4)

    p = tf1.paragraphs[0]
    p.text = "NATIONAL INSTITUTE OF TECHNOLOGY MEGHALAYA"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.alignment = PP_ALIGN.CENTER

    p = tf1.add_paragraph()
    p.text = "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING"
    p.font.size = Pt(11)
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(15)

    p = tf1.add_paragraph()
    p.text = "ProvenanceAI: Multi-Source Media Lineage Retrieval and Cryptographic Blockchain Verification"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(6)

    p = tf1.add_paragraph()
    p.text = "Master of Technology (CSE) DAC Progress Review — Comprehensive Defense"
    p.font.size = Pt(13)
    p.font.color.rgb = c_blue
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(20)

    t_box = s1.shapes.add_table(1, 2, Inches(1.8), Inches(4.3), Inches(9.733), Inches(1.4))
    t = t_box.table
    c0 = t.cell(0, 0)
    c0.fill.solid()
    c0.fill.fore_color.rgb = c_white
    p_c0 = c0.text_frame.paragraphs[0]
    p_c0.text = "Research Scholar:\nVivek Negi\nRoll No: T25CS012\nM.Tech (CSE) 2025–2027"
    p_c0.font.size = Pt(11)
    p_c0.font.color.rgb = c_dark
    p_c0.font.bold = True

    c1 = t.cell(0, 1)
    c1.fill.solid()
    c1.fill.fore_color.rgb = c_white
    p_c1 = c1.text_frame.paragraphs[0]
    p_c1.text = "Thesis Supervisor:\nDr. Akhilendra Pratap Singh\nAssistant Professor, Dept of CSE\nNIT Meghalaya, Sohra"
    p_c1.font.size = Pt(11)
    p_c1.font.color.rgb = c_dark
    p_c1.font.bold = True

    add_footer(s1, 1, 13)

    # ==========================================================================
    # SLIDE 2: MOTIVATION & PROBLEM STATEMENT
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Motivation: What is Composite Media Lineage?")
    add_footer(s2, 2, 13)

    c2_1 = create_card(s2, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "The Problem: Multi-Source Derivatives")
    add_bullet(c2_1, "Single-Source vs Composite Media:", "Traditional reverse search assumes 1-to-1 duplication. Real-world tampering fuses multiple parents.")
    add_bullet(c2_1, "Parent A (Background Plate):", "Covers 70%–85% of the canvas (e.g., scenic highway, empty crime scene desk).")
    add_bullet(c2_1, "Parent B (Spliced Donor Object):", "Localized critical asset covering only 10%–30% of pixels (e.g., 9mm handgun, HSRP license plate).")
    add_bullet(c2_1, "The Core Objective:", "Given query composite Q, accurately trace both Parent A and Parent B from an open-world gallery.")

    c2_2 = create_card(s2, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "High-Stakes Forensic Threat Models")
    add_bullet(c2_2, "1. Crime Scene Evidence Contraband Planting:", "Placing a weapon on an innocent suspect's desk to falsify violent criminal offenses.")
    add_bullet(c2_2, "2. Vehicle Hit-and-Run Registration Tampering:", "Splicing High-Security Registration Plates (HSRP) onto getaway cars to mislead police cameras.")
    add_bullet(c2_2, "3. Alibi & Presence Fabrication:", "Compositing individuals into remote locations (e.g., mountain overlooks) to engineer fake alibis.")
    add_bullet(c2_2, "Evidentiary Requirement:", "Courts mandate mathematical proof of both parent identities and cryptographically certified temporal precedence.")

    # ==========================================================================
    # SLIDE 3: VISUAL & MATHEMATICAL ANATOMY OF A COMPOSITE (NEW DIAGRAM)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Anatomy of a Composite Image: How Forgery is Formed")
    add_footer(s3, 3, 13)

    c3_top = create_card(s3, Inches(0.8), Inches(1.18), Inches(11.733), Inches(1.85), "Mathematical Formulation of Multi-Source Composition")
    add_bullet(c3_top, "Composition Formula:", "I_comp(x,y) = (1 - M(x,y)) ⊙ I_A(x,y) + M(x,y) ⊙ I_B(x,y), where M ∈ [0, 1] is the spatial alpha mask.")
    add_bullet(c3_top, "Boundary Transition Zone:", "Forensic blending applies Gaussian edge feathering along ∂M to eliminate hard seam gradients, concealing splicing artifacts from human eyes.")

    comp_fig = os.path.join(os.path.dirname(__file__), "composite_formation_pipeline.png")
    if os.path.exists(comp_fig):
        s3.shapes.add_picture(comp_fig, Inches(0.8), Inches(3.18), Inches(11.733), Inches(3.65))

    # ==========================================================================
    # SLIDE 4: THE BACKGROUND DOMINANCE PARADOX
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "The Core Technical Problem: Background Dominance Paradox")
    add_footer(s4, 4, 13)

    c4_1 = create_card(s4, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "The Global Average Pooling (GAP) Flaw")
    add_bullet(c4_1, "How Vision Models Form Representations:", "SOTA models (Meta SSCD, ResNet-50, CLIP) condense feature maps into a single global vector v ∈ R^D.")
    add_bullet(c4_1, "Mathematical Area Imbalance:", "Because Parent A occupies ≥75% of pixels, background activations completely dominate the embedding sum.")
    add_bullet(c4_1, "The Cosine Similarity Trap:", "cos(v_query, v_ParentA) ≈ 0.96 (100% Top-1 Recall) while cos(v_query, v_ParentB) ≤ 0.42 (Drops out of Top-50).")
    add_bullet(c4_1, "Baseline Failure:", "Standard SSCD achieves 0% dual-parent recall on multi-source composites.")

    c4_2 = create_card(s4, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Why Rigid Tile Slicing Fails")
    add_bullet(c4_2, "Naive Grid Partitioning (2x2 / 3x3):", "Splitting an image into non-overlapping square tiles breaks down in practical forensics.")
    add_bullet(c4_2, "Boundary Fragmentation:", "Objects placed near image centers (e.g., license plates or handguns) are bisected into separate quadrants.")
    add_bullet(c4_2, "Loss of Semantic Coherence:", "A quarter of a handgun or half a license plate cannot match full-object gallery embeddings.")
    add_bullet(c4_2, "Combinatorial Explosion:", "Naive patch comparisons explode search latency across large databases without intelligent gating.")

    # ==========================================================================
    # SLIDE 5: LITERATURE REVIEW & RESEARCH GAPS
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Literature Review & Research Gaps")
    add_footer(s5, 5, 13)

    t5_shape = s5.shapes.add_table(5, 4, Inches(0.8), Inches(1.3), Inches(11.733), Inches(4.3))
    t5 = t5_shape.table
    t5.columns[0].width = Inches(2.2)
    t5.columns[1].width = Inches(2.3)
    t5.columns[2].width = Inches(3.2)
    t5.columns[3].width = Inches(4.033)

    headers = ["Forensic Approach", "Key Literature", "Technical Mechanism", "Fatal Research Gap"]
    for col_idx, h_text in enumerate(headers):
        cell = t5.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_white

    table_data = [
        ("Perceptual Hashing", "pHash, BlockHash", "DCT frequency quantization & luminance", "Fails under cropping, rotation, or 5% local object insertion."),
        ("Single-Source Lineage", "Moreira et al. (2018), Dias et al. (2012)", "MST phylogenetic trees on global vectors", "Assumes 1-to-1 derivation; completely blind to multi-donor splicing."),
        ("Digital Watermarking", "C2PA / Content Credentials", "Cryptographic EXIF / metadata injection", "Fragile: stripped immediately by social media re-compression or screenshots."),
        ("ProvenanceAI (Ours)", "Negi & Singh (2026)", "Two-Stream Neural Patch Consensus + Blockchain", "Disentangles dual parents (88.89% Recall@5) with immutable SHA-256 ledger.")
    ]

    for row_idx, row_vals in enumerate(table_data, start=1):
        for col_idx, val in enumerate(row_vals):
            cell = t5.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_gray_bg if row_idx % 2 == 1 else c_white
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            if row_idx == 4:
                p.font.bold = True
                p.font.color.rgb = c_blue
            else:
                p.font.color.rgb = c_dark

    c5_bot = create_card(s5, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.05), "Research Gap Addressed")
    add_bullet(c5_bot, "The Unresolved Gap:", "Prior methods either detect forgery without finding donors, or find single duplicates while ignoring multi-parent combinations.")

    # ==========================================================================
    # SLIDE 6: PROPOSED ARCHITECTURE
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Proposed Architecture: Dynamic Patching & Lineage Engine")
    add_footer(s6, 6, 13)

    c6_top = create_card(s6, Inches(0.8), Inches(1.18), Inches(11.733), Inches(2.0), "End-to-End Pipeline Overview")
    add_bullet(c6_top, "1. Multi-Scale Slicing:", "Slides overlapping windows at 3 scales (25%, 35%, 50%) with 50% stride, mathematically ensuring centered donor objects are never bisected.")
    add_bullet(c6_top, "2. Neural Importance Gate:", "2-layer MLP evaluates visual entropy, suppresses empty sky/walls (w_i -> 0), and unmasks minority donor tokens (w_i -> 1).")

    arch_fig = os.path.join(os.path.dirname(__file__), "dynamic_patching_architecture.png")
    if os.path.exists(arch_fig):
        s6.shapes.add_picture(arch_fig, Inches(0.8), Inches(3.32), Inches(11.733), Inches(3.55))

    # ==========================================================================
    # SLIDE 7: BLOCKCHAIN PROOF-OF-PROVENANCE
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Cryptographic Layer: Proof-of-Provenance Blockchain")
    add_footer(s7, 7, 13)

    c7_1 = create_card(s7, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Immutable Cryptographic Ledger Mechanics")
    add_bullet(c7_1, "Genesis Block 0:", "Initialized with fixed zero-state hash H_0 = 0x0000... at system genesis.")
    add_bullet(c7_1, "Block Sealing Formula:", "H_k = SHA-256(H_(k-1) || T_k || h_pixel || z_SSCD || Parent_IDs).")
    add_bullet(c7_1, "Cascade Tamper Invalidation:", "Modifying 1 pixel bit in Block k shatters all downstream hashes H_(k+1...N), alerting forensic auditors immediately.")
    add_bullet(c7_1, "129 Verified Blocks:", "All 45 benchmark evaluation composites notarized and verified on our live NITM ledger.")

    c7_2 = create_card(s7, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Temporal Precedence Invariant Verification")
    add_bullet(c7_2, "The Core Temporal Invariant:", "A composite derivative cannot legally precede its constituent donor sources: T_ParentA ≤ T_Composite ∧ T_ParentB ≤ T_Composite.")
    add_bullet(c7_2, "On-Chain Audit Protocol:", "The verification engine interrogates block timestamps: if claimant asset T_X > T_Evidence, consensus flags: 'Invalid Temporal Lineage'.")
    add_bullet(c7_2, "Courtroom Evidentiary Admissibility:", "Meets Section 65B Indian Evidence Act criteria for electronic record certification.")

    # ==========================================================================
    # SLIDE 8: SOFTWARE ARCHITECTURE & TECH STACK
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Implementation Details & Computational Software Stack")
    add_footer(s8, 8, 13)

    t8_shape = s8.shapes.add_table(6, 3, Inches(0.8), Inches(1.3), Inches(11.733), Inches(4.3))
    t8 = t8_shape.table
    t8.columns[0].width = Inches(3.0)
    t8.columns[1].width = Inches(3.2)
    t8.columns[2].width = Inches(5.533)

    t8_headers = ["Subsystem Layer", "Library / Framework", "Operational Role & Engineering Parameters"]
    for col_idx, h_text in enumerate(t8_headers):
        cell = t8.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_white

    stack_data = [
        ("Feature Backbone", "PyTorch, Meta SSCD (ResNet-50)", "512-dim L2-normalized feature embeddings per image / patch token."),
        ("Importance Gating", "2-Layer MLP (R^512 -> R^128 -> 1)", "Trained on synthetic composites; extracts localized donor tokens."),
        ("High-Speed Indexing", "FAISS (IndexFlatIP)", "Sub-millisecond cosine retrieval across gallery of size N=300."),
        ("Frequency Forensics", "NumPy 2D FFT, SciPy ndimage", "Radial spectral energy decay E_HF calculation and notch filtering."),
        ("Blockchain Ledger", "Python hashlib (SHA-256)", "129 immutable blocks, genesis linking, and temporal validation.")
    ]

    for row_idx, row_vals in enumerate(stack_data, start=1):
        for col_idx, val in enumerate(row_vals):
            cell = t8.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_gray_bg if row_idx % 2 == 1 else c_white
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = c_dark

    c8_bot = create_card(s8, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.05), "Benchmarked Compute Infrastructure")
    add_bullet(c8_bot, "Hardware Platform:", "Tesla T4 GPU (16 GB VRAM) at NIT Meghalaya High Performance Lab. Inference latency: 42ms per dual-parent audit.")

    # ==========================================================================
    # SLIDE 9: EXPERIMENTAL RESULTS
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Experimental Evaluation & Real-World Evidentiary Scenarios")
    add_footer(s9, 9, 13)

    c9_1 = create_card(s9, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Quantitative Benchmark: MS-COCO 2017")
    add_bullet(c9_1, "Dataset Splits:", "210 Train / 45 Val / 45 Test multi-source composites generated across 80 semantic categories.")
    add_bullet(c9_1, "Baseline Global GAP Retrieval:", "Parent A Recall@5 = 95.56% | Parent B Recall@5 = 13.33% (Catastrophic failure on small objects).")
    add_bullet(c9_1, "ProvenanceAI Two-Stream Consensus:", "Parent A Recall@5 = 97.78% | Parent B Recall@5 = 88.89% (+75.56% absolute improvement!).")
    add_bullet(c9_1, "Mean Reciprocal Rank (MRR):", "Surges from 0.089 to 0.742 for localized donor retrieval.")

    c9_2 = create_card(s9, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Real-World Evidentiary Case Studies")
    add_bullet(c9_2, "Case 1: Hit-and-Run Registration Swap:", "Vehicle background matched at Sim=0.9412 (Rank 1). Forged HSRP plate matched at Sim=0.8874 (Rank 1).")
    add_bullet(c9_2, "Case 2: Crime Scene Handgun Planting:", "Office desk background matched at Sim=0.9388 (Rank 1). 9mm handgun matched at Sim=0.8912 (Rank 1).")
    add_bullet(c9_2, "Case 3: Suspect Alibi Fabrication:", "Mountain overlook background matched at Sim=0.9521. Spliced suspect matched at Sim=0.8745.")
    add_bullet(c9_2, "Orthogonal Negative Rejection:", "Unrelated gallery assets reliably score ≤ 0.1102.")

    # ==========================================================================
    # SLIDE 10: THEORETICAL BOUNDARY: GENERATIVE DIFFUSION VS REAL CAMERA OPTICS
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Theoretical Boundary: Generative Diffusion vs. Real Camera Optics")
    add_footer(s10, 10, 13)

    c10_1 = create_card(s10, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Where Physical Splicing Retrieval Fails")
    add_bullet(c10_1, "Generative Latent Inpainting:", "When media is modified via Meta AI Emu or Stable Diffusion 3.5, NO physical donor image exists in the real world.")
    add_bullet(c10_1, "The False-Neighbor Failure Mode:", "Unguided nearest-neighbor search forced false matches (matching synthetic sun disc to yellow headphones based on color).")
    add_bullet(c10_1, "Theoretical Root Cause:", "Diffusion decoders synthesize pixels in compressed latent space Z, lacking natural camera sensor Photo-Response Non-Uniformity (PRNU).")

    c10_2 = create_card(s10, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Forensic Solution: Frequency Domain Gating")
    add_bullet(c10_2, "High-Frequency Energy Attenuation:", "Diffusion upsampling filters out high-frequency sensor noise, leaving a characteristic dead outer ring in 2D FFT.")
    add_bullet(c10_2, "Deconvolution Cross-Spikes:", "ResNet deconvolution layers introduce unnatural periodic cross-axis spikes along u=0 and v=0.")
    add_bullet(c10_2, "Null-Hypothesis Rejection Gate:", "If spectral energy ratio E_HF < 0.880, the engine refuses false donor retrieval and issues: 'Synthetic Latent Inpainting'.")
    add_bullet(c10_2, "Audit Outcome:", "Parent A background remains verified on-chain, while synthesized regions are flagged without hallucinations.")

    # ==========================================================================
    # SLIDE 11: 2D FFT SPECTRAL FORENSICS & RADIAL GATING (NEW DIAGRAM)
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "2D FFT Spectral Forensics: Real Optics vs. Synthetic Diffusion")
    add_footer(s11, 11, 13)

    c11_top = create_card(s11, Inches(0.8), Inches(1.18), Inches(11.733), Inches(2.2), "2D Fast Fourier Transform Radial Energy Decision Rule")
    add_bullet(c11_top, "High-Frequency Energy Ratio:", "E_HF = [sum_{r > r_c} S(u, v)] / [sum S(u, v)], where S(u, v) = 20 log(|F(u, v)| + ε).")
    add_bullet(c11_top, "Forensic Decision Boundary:", "If E_HF ≥ 0.880: Natural camera sensor PRNU confirmed -> Proceed to dual-parent donor retrieval.")
    add_bullet(c11_top, "Synthetic Detection Gate:", "If E_HF < 0.880: Latent diffusion inpainting detected -> Flag 'Synthetic Inpaint (No Physical Donor)'.")

    fft_fig = os.path.join(os.path.dirname(__file__), "fft_diffusion_vs_real_comparison.png")
    if os.path.exists(fft_fig):
        s11.shapes.add_picture(fft_fig, Inches(0.8), Inches(3.52), Inches(11.733), Inches(3.35))

    # ==========================================================================
    # SLIDE 12: DEPLOYMENT & FUTURE ENGINEERING SCOPE
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Deployment & Live Interactive Forensics Demonstration")
    add_footer(s12, 12, 13)

    c12_1 = create_card(s12, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Live Dashboard & Forensics Workbench")
    add_bullet(c12_1, "Operational Host:", "Running live at http://localhost:8502 for real-time committee demonstration.")
    add_bullet(c12_1, "Tab 1 (Lineage Audit):", "Interactive query upload, dual-parent retrieval, and on-chain verification.")
    add_bullet(c12_1, "Tab 4 (Blockchain Ledger):", "129 sealed blocks with live cryptographic hash cascade validation.")
    add_bullet(c12_1, "Tab 6 (2D FFT Lab):", "Interactive wave synthesizer (1--2500 waves) and surgical notch frequency filters.")

    c12_2 = create_card(s12, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Thesis Completion & 4th Semester Scope")
    add_bullet(c12_2, "Current Progress Review Status:", "Core architectural design, dataset benchmarking, and blockchain completed.")
    add_bullet(c12_2, "Final 4th Semester Roadmap:", "Extending patch consensus to short-form video streams (Reels/Shorts keyframes).")
    add_bullet(c12_2, "Edge Model Optimization:", "INT8 quantization of Importance Gate for mobile forensic field inspection.")
    add_bullet(c12_2, "Target Publications:", "Submitting to IEEE Transactions on Information Forensics and Security (TIFS).")

    # ==========================================================================
    # SLIDE 13: KEY REFERENCES & LITERATURE CITATIONS
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Key References & Literature Citations")
    add_footer(s13, 13, 13)

    c13 = create_card(s13, Inches(0.8), Inches(1.3), Inches(11.733), Inches(5.5), "Key Academic Literature Citations")
    add_bullet(c13, "[1] Moreira et al. (2018):", "Image Provenance Analysis at Scale, IEEE Transactions on Information Forensics and Security, 13(12):2857--2871.")
    add_bullet(c13, "[2] Pizzi et al. (2022):", "A Self-Supervised Descriptor for Image Copy Detection (SSCD), IEEE/CVF CVPR, pp. 14532--14542.")
    add_bullet(c13, "[3] Dias, Rocha, Goldenstein (2012):", "Image Phylogeny by Minimal Spanning Trees, IEEE TPAMI, 34(12):2362--2375.")
    add_bullet(c13, "[4] Guillaro et al. (2023):", "TruFor: Leveraging All-Round Clues for Trustworthy Image Forgery Detection, IEEE/CVF CVPR, pp. 9606--9615.")
    add_bullet(c13, "[5] Coalition for Content Provenance (C2PA, 2024):", "C2PA Technical Specifications: Content Credentials Standard, C2PA Consortium.")
    add_bullet(c13, "[6] Chen, Yao, Niu (2024):", "A Single Simple Patch is All You Need for AI-Generated Image Detection, arXiv:2402.01123.")

    p_end = c13.text_frame.add_paragraph()
    p_end.text = "Thank You! Questions & Committee Discussion."
    p_end.font.size = Pt(16)
    p_end.font.bold = True
    p_end.font.color.rgb = c_blue
    p_end.alignment = PP_ALIGN.CENTER
    p_end.space_before = Pt(18)

    # Save presentations
    out_path1 = os.path.join(os.path.dirname(__file__), "DAC_Review_Vivek_Negi_10Slides.pptx")
    out_path2 = os.path.join(os.path.dirname(__file__), "Multi_Source_Media_Lineage_NITM.pptx")
    prs.save(out_path1)
    prs.save(out_path2)
    print(f"Successfully generated strictly 13-slide PowerPoint presentations:")
    print(f"1. {out_path1}")
    print(f"2. {out_path2}")

if __name__ == "__main__":
    build_13slide_deck()
