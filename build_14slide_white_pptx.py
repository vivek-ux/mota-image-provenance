#!/usr/bin/env python3
"""
build_14slide_white_pptx.py
Builds the 14-slide Master PowerPoint deck in the clean Minimalist White & Slate-Grey theme:
Features all 5 visual diagrams embedded natively:
1. Slide 3: composite_formation_pipeline.png
2. Slide 5: sscd_feature_extraction_flow.png
3. Slide 6: dynamic_patching_step_flow.png
4. Slide 7: dynamic_patching_architecture.png
5. Slide 8: blockchain_provenance_flow.png
6. Slide 13: fft_diffusion_vs_real_comparison.png
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py_modules'))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean White & Slate Grey Theme
    c_white = RGBColor(255, 255, 255)
    c_navy = RGBColor(30, 58, 138)         # Deep Executive Navy
    c_blue = RGBColor(37, 99, 235)         # Sapphire Blue
    c_dark = RGBColor(15, 23, 42)          # Slate-900 High Contrast Text
    c_gray_bg = RGBColor(248, 250, 252)    # Slate-50 Clean Card
    c_gray_border = RGBColor(203, 213, 225) # Slate-300 Subtle Border
    c_teal = RGBColor(13, 148, 136)

    def add_footer(slide, current_slide, total_slides=14):
        footer_top = Inches(7.05)
        footer_height = Inches(0.45)
        
        b1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), footer_top, Inches(5.8), footer_height)
        b1.fill.solid()
        b1.fill.fore_color.rgb = c_navy
        b1.line.color.rgb = c_navy
        tf1 = b1.text_frame
        tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = tf1.paragraphs[0]
        p1.text = "Vivek Negi – T25CS012 (NIT Meghalaya)"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = c_white
        p1.margin_left = Inches(0.5)

        b2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), footer_top, Inches(6.0), footer_height)
        b2.fill.solid()
        b2.fill.fore_color.rgb = c_gray_bg
        b2.line.color.rgb = c_gray_border
        tf2 = b2.text_frame
        tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = tf2.paragraphs[0]
        p2.text = "M.Tech Thesis DAC Progress Review (Comprehensive 14-Slide Defense)"
        p2.font.size = Pt(11)
        p2.font.color.rgb = c_navy
        p2.margin_left = Inches(0.3)

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

    def add_header(slide, title_text):
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

    def create_card(slide, left, top, width, height, title="", title_color=c_navy, bg_color=c_gray_bg, border_color=c_gray_border):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.18)
        tf.margin_bottom = Inches(0.18)
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(6)
        return card

    def add_bullet(card, bold_prefix, text_body, pt_size=10.5, space_after=5):
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

    # SLIDE 1: TITLE
    s1 = prs.slides.add_slide(blank_layout)
    c1 = create_card(s1, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.9), bg_color=c_white)
    tf1 = c1.text_frame
    p = tf1.paragraphs[0]
    p.text = "NATIONAL INSTITUTE OF TECHNOLOGY MEGHALAYA"
    p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = c_blue; p.alignment = PP_ALIGN.CENTER
    p = tf1.add_paragraph()
    p.text = "Department of Computer Science and Engineering"
    p.font.size = Pt(11); p.font.color.rgb = c_navy; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(14)
    p = tf1.add_paragraph()
    p.text = "ProvenanceAI: Multi-Source Media Lineage Retrieval and Cryptographic Blockchain Verification"
    p.font.size = Pt(21); p.font.bold = True; p.font.color.rgb = c_navy; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(6)
    p = tf1.add_paragraph()
    p.text = "Master of Technology (CSE) DAC Progress Review — Comprehensive Defense"
    p.font.size = Pt(13); p.font.color.rgb = c_blue; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(20)

    t_box = s1.shapes.add_table(1, 2, Inches(1.8), Inches(4.3), Inches(9.733), Inches(1.4))
    t = t_box.table
    c0 = t.cell(0, 0); c0.fill.solid(); c0.fill.fore_color.rgb = c_gray_bg
    p0 = c0.text_frame.paragraphs[0]
    p0.text = "Research Scholar:\nVivek Negi (Roll No: T25CS012)\nM.Tech (CSE) 2025–2027"; p0.font.bold = True; p0.font.color.rgb = c_dark
    c1_cell = t.cell(0, 1); c1_cell.fill.solid(); c1_cell.fill.fore_color.rgb = c_gray_bg
    p1 = c1_cell.text_frame.paragraphs[0]
    p1.text = "Thesis Supervisor:\nDr. Akhilendra Pratap Singh\nAssistant Professor, Dept of CSE, NIT Meghalaya"; p1.font.bold = True; p1.font.color.rgb = c_dark
    add_footer(s1, 1)

    # SLIDE 2: MOTIVATION
    s2 = prs.slides.add_slide(blank_layout); add_header(s2, "Motivation: What is Composite Media Lineage?"); add_footer(s2, 2)
    c2_1 = create_card(s2, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "The Problem: Multi-Source Derivatives")
    add_bullet(c2_1, "Beyond 1-to-1 Duplicates:", "Real-world tampering fuses multiple parents (Background + Spliced Object).")
    add_bullet(c2_1, "Parent A (Background):", "Covers 70%–85% of canvas (e.g., highway, empty crime scene desk).")
    add_bullet(c2_1, "Parent B (Spliced Donor):", "Critical localized asset covering only 10%–30% (e.g., weapon, license plate).")
    add_bullet(c2_1, "Core Objective:", "Retrieve both Parent A and Parent B and prove temporal precedence.")

    c2_2 = create_card(s2, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "High-Impact Forensic Threat Scenarios")
    add_bullet(c2_2, "1. Evidence Planting:", "Splicing a weapon onto an innocent suspect's desk.")
    add_bullet(c2_2, "2. Hit-and-Run Fraud:", "Forging a fake number plate onto a getaway car.")
    add_bullet(c2_2, "3. Alibi Fabrication:", "Splicing individuals into scenic overlooks to fake geographic presence.")
    add_bullet(c2_2, "Courtroom Mandate:", "Legal admissibility requires cryptographic proof of parents and timestamps.")

    # SLIDE 3: VISUAL ANATOMY (DIAGRAM)
    s3 = prs.slides.add_slide(blank_layout); add_header(s3, "Anatomy of a Composite Image: How Forgeries Are Made"); add_footer(s3, 3)
    c3_top = create_card(s3, Inches(0.8), Inches(1.18), Inches(11.733), Inches(1.8), "How a Multi-Source Forgery is Created (Step-by-Step)")
    add_bullet(c3_top, "Composition Formula:", "Composite = (1 - Mask) * Background Scene + Mask * Donor Cutout.")
    add_bullet(c3_top, "Boundary Blending:", "Alpha edge feathering eliminates visible seam lines to fool human vision.")
    f_comp = os.path.join(out_dir, "composite_formation_pipeline.png")
    if os.path.exists(f_comp): s3.shapes.add_picture(f_comp, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.7))

    # SLIDE 4: DOMINANCE PARADOX
    s4 = prs.slides.add_slide(blank_layout); add_header(s4, "The Background Dominance Paradox"); add_footer(s4, 4)
    c4_1 = create_card(s4, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Why Standard AI Models Fail")
    add_bullet(c4_1, "Single Global Vector:", "Standard vision models compress images into one average vector.")
    add_bullet(c4_1, "Background Overpowers Donor:", "Because background covers 80%, its activations overwhelm the embedding.")
    add_bullet(c4_1, "Donor Disappears:", "The 20% spliced donor object is completely ignored during search.")
    c4_2 = create_card(s4, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "The Result: 13.3% Failure Rate")
    add_bullet(c4_2, "Baseline Failure:", "Standard nearest-neighbor achieves only 13.33% donor recall.")
    add_bullet(c4_2, "Why Rigid Grids Fail:", "Cutting images into fixed squares slices centered objects in half.")
    add_bullet(c4_2, "Our Research Challenge:", "How to separate both parents without manual human bounding boxes!")

    # SLIDE 5: FOUNDATION META SSCD (DIAGRAM)
    s5 = prs.slides.add_slide(blank_layout); add_header(s5, "Foundation: What is Meta SSCD? (Image to Numbers)"); add_footer(s5, 5)
    c5_top = create_card(s5, Inches(0.8), Inches(1.18), Inches(11.733), Inches(1.8), "Converting Images into 512-Dimensional Mathematical Fingerprints")
    add_bullet(c5_top, "Self-Supervised Copy Detection:", "ResNet-50 trained on 50M image variations converts pixels into 512 numbers.")
    add_bullet(c5_top, "Cosine Metric:", "All vectors normalized to unit length (||v||=1); inner product equals cosine similarity.")
    f_sscd = os.path.join(out_dir, "sscd_feature_extraction_flow.png")
    if os.path.exists(f_sscd): s5.shapes.add_picture(f_sscd, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.7))

    # SLIDE 6: DYNAMIC PATCHING (DIAGRAM)
    s6 = prs.slides.add_slide(blank_layout); add_header(s6, "Dynamic Patching & Importance Gating Pipeline"); add_footer(s6, 6)
    c6_top = create_card(s6, Inches(0.8), Inches(1.18), Inches(11.733), Inches(1.8), "How Dynamic Patching Works (Mathematical Guarantee)")
    add_bullet(c6_top, "Multi-Scale Overlapping Windows:", "3 window scales (25%, 35%, 50%) slide with 50% stride overlap -> object never bisected!")
    add_bullet(c6_top, "Neural Importance Gate:", "2-layer MLP filters empty sky/walls (w -> 0) and highlights donor objects (w -> 1).")
    f_dp = os.path.join(out_dir, "dynamic_patching_step_flow.png")
    if os.path.exists(f_dp): s6.shapes.add_picture(f_dp, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.7))

    # SLIDE 7: END-TO-END ARCHITECTURE (DIAGRAM)
    s7 = prs.slides.add_slide(blank_layout); add_header(s7, "Proposed Architecture: Two-Stream Lineage Engine"); add_footer(s7, 7)
    c7_top = create_card(s7, Inches(0.8), Inches(1.18), Inches(11.733), Inches(1.8), "Complete System Flow: Patching -> Gating -> Retrieval -> Blockchain")
    add_bullet(c7_top, "Dual-Stream Matching:", "Stream A recovers Parent A background; Stream B recovers Parent B donor.")
    add_bullet(c7_top, "Consensus Verification:", "Confirms both parents are distinct gallery assets with certified timestamps.")
    f_arch = os.path.join(out_dir, "dynamic_patching_architecture.png")
    if os.path.exists(f_arch): s7.shapes.add_picture(f_arch, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.7))

    # SLIDE 8: BLOCKCHAIN EXPLAINED (DIAGRAM)
    s8 = prs.slides.add_slide(blank_layout); add_header(s8, "Cryptographic Layer: Proof-of-Provenance Blockchain"); add_footer(s8, 8)
    c8_top = create_card(s8, Inches(0.8), Inches(1.18), Inches(11.733), Inches(1.8), "The Digital 'Wax Seal' Chain (Easy Language)")
    add_bullet(c8_top, "Chained Blocks:", "Block k seals data + hash of Block k-1. Tampering 1 pixel in an old image breaks all 129 blocks!")
    add_bullet(c8_top, "Temporal Precedence:", "A composite cannot exist before its parents: Time_Parents <= Time_Composite.")
    f_bc = os.path.join(out_dir, "blockchain_provenance_flow.png")
    if os.path.exists(f_bc): s8.shapes.add_picture(f_bc, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.7))

    # SLIDE 9: LITERATURE SURVEY
    s9 = prs.slides.add_slide(blank_layout); add_header(s9, "Literature Survey & Research Gaps"); add_footer(s9, 9)
    t9 = s9.shapes.add_table(5, 4, Inches(0.8), Inches(1.3), Inches(11.733), Inches(4.3)).table
    t9.columns[0].width = Inches(2.5); t9.columns[1].width = Inches(2.2); t9.columns[2].width = Inches(3.2); t9.columns[3].width = Inches(3.833)
    for i, h in enumerate(["Approach", "Key Works", "Mechanism", "Fatal Limitation"]):
        cell = t9.cell(0, i); cell.fill.solid(); cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.color.rgb = c_white; p.font.size = Pt(11)
    rows = [
        ("Perceptual Hashing", "pHash, BlockHash", "Global image frequencies", "Fails under crop or small 10% object insertion."),
        ("Single-Source Trees", "Moreira (2018), Dias (2012)", "Trees on global vectors", "Assumes 1-to-1 copying; blind to multi-donor splicing."),
        ("Digital Watermarking", "C2PA Standard", "Metadata injection", "Fragile: stripped by social media re-saving."),
        ("ProvenanceAI (Ours)", "Negi & Singh (2026)", "Dynamic Patching + Blockchain", "Recovers both parents (88.9% Recall) with immutable ledger.")
    ]
    for r_i, r in enumerate(rows, 1):
        for c_i, val in enumerate(r):
            cell = t9.cell(r_i, c_i); cell.fill.solid(); cell.fill.fore_color.rgb = c_gray_bg if r_i%2==1 else c_white
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(10)
            if r_i == 4: p.font.bold = True; p.font.color.rgb = c_blue

    # SLIDE 10: IMPLEMENTATION TECH STACK
    s10 = prs.slides.add_slide(blank_layout); add_header(s10, "Implementation Details & Computational Software Stack"); add_footer(s10, 10)
    t10 = s10.shapes.add_table(6, 3, Inches(0.8), Inches(1.3), Inches(11.733), Inches(4.3)).table
    t10.columns[0].width = Inches(3.0); t10.columns[1].width = Inches(3.2); t10.columns[2].width = Inches(5.533)
    for i, h in enumerate(["Pipeline Layer", "Tool / Framework", "Operational Role"]):
        cell = t10.cell(0, i); cell.fill.solid(); cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.color.rgb = c_white; p.font.size = Pt(11)
    s_rows = [
        ("Feature Backbone", "PyTorch + Meta SSCD (ResNet-50)", "512-dim normalized feature embeddings per patch."),
        ("Importance Gating", "2-Layer Neural MLP", "Learns to unmask small spliced objects from dominant scenes."),
        ("Fast Index Search", "Meta FAISS (IndexFlatIP)", "Sub-millisecond cosine search across gallery of size N=300."),
        ("Frequency Forensics", "NumPy 2D FFT, SciPy", "Measures radial high-frequency decay to detect synthetic diffusion."),
        ("Blockchain Ledger", "Python hashlib (SHA-256)", "129 immutable blocks with parent lineage and timestamps.")
    ]
    for r_i, r in enumerate(s_rows, 1):
        for c_i, val in enumerate(r):
            cell = t10.cell(r_i, c_i); cell.fill.solid(); cell.fill.fore_color.rgb = c_gray_bg if r_i%2==1 else c_white
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(10)
    c10_bot = create_card(s10, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.05), "Benchmark Infrastructure")
    add_bullet(c10_bot, "Hardware Platform:", "Tesla T4 GPU (16 GB VRAM) at NIT Meghalaya High Performance Lab. Latency: 42ms per audit.")

    # SLIDE 11: EXPERIMENTAL RESULTS
    s11 = prs.slides.add_slide(blank_layout); add_header(s11, "Experimental Evaluation & Real-World Evidentiary Scenarios"); add_footer(s11, 11)
    c11_1 = create_card(s11, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Quantitative Benchmark: MS-COCO 2017")
    add_bullet(c11_1, "Baseline Global GAP:", "Parent A Recall@5 = 95.56% | Parent B Recall@5 = 13.33% (Fails on small objects).")
    add_bullet(c11_1, "ProvenanceAI (Ours):", "Parent A Recall@5 = 97.78% | Parent B Recall@5 = 88.89% (+75.56% absolute improvement!).")
    add_bullet(c11_1, "Mean Reciprocal Rank:", "Surges from 0.089 to 0.742 for localized donor retrieval.")
    c11_2 = create_card(s11, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Real-World Evidentiary Case Studies")
    add_bullet(c11_2, "Case 1 (Plate Swap):", "Vehicle matched at Sim=0.9412 (Rank 1). Forged plate matched at Sim=0.8874 (Rank 1).")
    add_bullet(c11_2, "Case 2 (Handgun Planting):", "Desk matched at Sim=0.9388 (Rank 1). Handgun matched at Sim=0.8912 (Rank 1).")
    add_bullet(c11_2, "Negative Rejection:", "Unrelated gallery assets reliably score <= 0.1102.")

    # SLIDE 12: THEORETICAL BOUNDARY (AI DIFFUSION)
    s12 = prs.slides.add_slide(blank_layout); add_header(s12, "Theoretical Boundary: Generative Diffusion vs. Real Cameras"); add_footer(s12, 12)
    c12_1 = create_card(s12, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Where Physical Matching Fails: AI Inpainting")
    add_bullet(c12_1, "No Physical Donor:", "When modified via Meta AI Emu / SD 3.5, NO real-world donor photo exists.")
    add_bullet(c12_1, "False Neighbor Hallucination:", "Unguided search forces a false match (e.g., matching synthetic sun to headphones).")
    c12_2 = create_card(s12, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Camera Sensors vs. AI Math")
    add_bullet(c12_2, "Physical Cameras:", "Leave natural microscopic sensor noise (PRNU) across high frequencies.")
    add_bullet(c12_2, "Diffusion Models:", "Synthesize in latent space, leaving an unnaturally smooth, dead frequency rim.")
    add_bullet(c12_2, "Our Solution:", "Execute 2D FFT Frequency Filter to detect AI diffusion before searching database!")

    # SLIDE 13: 2D FFT FORENSICS (DIAGRAM)
    s13 = prs.slides.add_slide(blank_layout); add_header(s13, "2D FFT Spectral Forensics: Real Optics vs. AI Diffusion"); add_footer(s13, 13)
    c13_top = create_card(s13, Inches(0.8), Inches(1.18), Inches(11.733), Inches(1.8), "2D Fast Fourier Transform Decision Rule")
    add_bullet(c13_top, "Dartboard Analogy:", "Center = smooth ambient light. Outer Ring = fine camera sensor noise (PRNU).")
    add_bullet(c13_top, "Decision Boundary:", "If High-Frequency Ratio E_HF >= 0.88 -> Real Camera; if E_HF < 0.88 -> AI Diffusion (Flagged)!")
    f_fft = os.path.join(out_dir, "fft_diffusion_vs_real_comparison.png")
    if os.path.exists(f_fft): s13.shapes.add_picture(f_fft, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.7))

    # SLIDE 14: DEPLOYMENT & CONCLUSION
    s14 = prs.slides.add_slide(blank_layout); add_header(s14, "Deployment, Live Demonstration & Conclusion"); add_footer(s14, 14)
    c14_1 = create_card(s14, Inches(0.8), Inches(1.3), Inches(5.7), Inches(5.5), "Live Interactive Workbench (Port 8502)")
    add_bullet(c14_1, "Local Host:", "Active daemon running at http://localhost:8502 for real-time committee review.")
    add_bullet(c14_1, "Tab 1 (Audit):", "Upload query composite, unmask donors, check on-chain block.")
    add_bullet(c14_1, "Tab 4 (Ledger):", "129 sealed blocks with live tamper cascade validation.")
    add_bullet(c14_1, "Tab 6 (2D FFT Lab):", "Interactive wave synthesizer (1--2500 waves) and surgical notch filters.")
    c14_2 = create_card(s14, Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.5), "Thesis Status & Final Semester Scope")
    add_bullet(c14_2, "Current Progress Review:", "Core architecture, benchmarks, and blockchain fully operational.")
    add_bullet(c14_2, "4th Semester Roadmap:", "Extending patch consensus to short-form video keyframes.")
    add_bullet(c14_2, "Publication Target:", "Submitting research paper to IEEE TIFS.")

    p_end = c14_2.text_frame.add_paragraph()
    p_end.text = "Thank You! Questions & Discussion."
    p_end.font.size = Pt(14); p_end.font.bold = True; p_end.font.color.rgb = c_navy; p_end.alignment = PP_ALIGN.CENTER; p_end.space_before = Pt(12)

    out1 = os.path.join(out_dir, "DAC_Review_Vivek_Negi_10Slides.pptx")
    out2 = os.path.join(out_dir, "Multi_Source_Media_Lineage_NITM.pptx")
    prs.save(out1); prs.save(out2)
    print("Successfully built 14-slide White & Slate-Grey PPTX decks!")

if __name__ == "__main__":
    build_deck()
