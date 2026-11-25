#!/usr/bin/env python3
"""
generate_all_slide_visuals.py
Generates crisp, high-contrast, professional visual diagrams for Vivek's M.Tech presentation:
1. sscd_feature_extraction_flow.png: Image to numbers (512-D vector)
2. dynamic_patching_step_flow.png: Image -> Multi-Scale Grids -> SSCD -> 2-Layer MLP Importance Gate
3. blockchain_provenance_flow.png: Linked SHA-256 blocks with temporal precedence
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

out_dir = "/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance"
os.makedirs(out_dir, exist_ok=True)

# ==============================================================================
# 1. SSCD: IMAGE TO NUMBERS (512-D EMBEDDING)
# ==============================================================================
def make_sscd_diagram():
    fig, ax = plt.subplots(figsize=(13, 3.6), facecolor='white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 3.6)
    ax.axis('off')

    # Palette: Minimalist White, Grey & Deep Navy/Sapphire
    c_slate_dark = '#0f172a'
    c_slate_card = '#f8fafc'
    c_slate_border = '#cbd5e1'
    c_blue = '#2563eb'
    c_teal = '#0d9488'

    # Box 1: Input Image
    b1 = patches.FancyBboxPatch((0.4, 0.4), 2.4, 2.8, boxstyle="round,pad=0.1", facecolor=c_slate_card, edgecolor=c_slate_border, lw=1.5)
    ax.add_patch(b1)
    ax.text(1.6, 2.8, "INPUT IMAGE", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    # Mini image preview
    img_sample_path = os.path.join(out_dir, "clean_handgun_no_fringe.png")
    if os.path.exists(img_sample_path):
        sample_img = Image.open(img_sample_path).convert("RGB").resize((120, 90))
        ax.imshow(sample_img, extent=[0.8, 2.4, 1.2, 2.4])
    else:
        ax.text(1.6, 1.8, "[ Raw Pixels ]\n(224 x 224 x 3)", color=c_slate_dark, fontsize=9, ha='center')
    ax.text(1.6, 0.7, "RGB Pixel Tensor\n[0, 255] Range", color='#64748b', fontsize=8, ha='center')

    # Arrow 1 -> 2
    ax.annotate('', xy=(3.4, 1.8), xytext=(2.9, 1.8), arrowprops=dict(arrowstyle="->", color=c_blue, lw=2.5))

    # Box 2: ResNet-50 Feature Extractor
    b2 = patches.FancyBboxPatch((3.5, 0.4), 3.2, 2.8, boxstyle="round,pad=0.1", facecolor=c_slate_card, edgecolor=c_blue, lw=1.5)
    ax.add_patch(b2)
    ax.text(5.1, 2.8, "META SSCD BACKBONE", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    ax.text(5.1, 2.3, "ResNet-50 Convolutional Layers", color=c_slate_dark, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(5.1, 1.6, "• Conv1 -> Residual Blocks (50 layers)\n• Pre-trained on 50M image pairs\n• Invariant to blur, compression, crop", color='#475569', fontsize=8, ha='center')
    ax.text(5.1, 0.7, "Learns Semantic Fingerprints", color=c_teal, fontsize=8, fontweight='bold', ha='center')

    # Arrow 2 -> 3
    ax.annotate('', xy=(7.3, 1.8), xytext=(6.8, 1.8), arrowprops=dict(arrowstyle="->", color=c_blue, lw=2.5))

    # Box 3: L2 Hypersphere Normalization
    b3 = patches.FancyBboxPatch((7.4, 0.4), 2.2, 2.8, boxstyle="round,pad=0.1", facecolor=c_slate_card, edgecolor=c_slate_border, lw=1.5)
    ax.add_patch(b3)
    ax.text(8.5, 2.8, "NORMALIZATION", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    ax.text(8.5, 2.1, "L2 Unit Length\n||v||_2 = 1.0", color=c_slate_dark, fontsize=10, fontweight='bold', ha='center')
    ax.text(8.5, 1.3, "Projects vector onto\n512-D unit hypersphere", color='#475569', fontsize=8, ha='center')
    ax.text(8.5, 0.7, "Inner Product = Cosine Sim", color=c_blue, fontsize=8, fontweight='bold', ha='center')

    # Arrow 3 -> 4
    ax.annotate('', xy=(10.2, 1.8), xytext=(9.7, 1.8), arrowprops=dict(arrowstyle="->", color=c_blue, lw=2.5))

    # Box 4: Output Numerical Vector (Image to Numbers)
    b4 = patches.FancyBboxPatch((10.3, 0.4), 2.3, 2.8, boxstyle="round,pad=0.1", facecolor='#eff6ff', edgecolor=c_blue, lw=2)
    ax.add_patch(b4)
    ax.text(11.45, 2.8, "OUTPUT NUMBERS", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    ax.text(11.45, 2.3, "512-D Feature Vector", color=c_slate_dark, fontsize=10, fontweight='bold', ha='center')
    vec_text = "[ +0.142,\n  -0.891,\n  +0.052,\n  +0.318,\n   ...\n  -0.204 ]"
    ax.text(11.45, 1.45, vec_text, color=c_slate_dark, fontsize=8.5, fontfamily='monospace', ha='center')
    ax.text(11.45, 0.65, "Instant FAISS Match!", color=c_teal, fontsize=8, fontweight='bold', ha='center')

    plt.tight_layout()
    out_p = os.path.join(out_dir, "sscd_feature_extraction_flow.png")
    plt.savefig(out_p, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated sscd_feature_extraction_flow.png")

# ==============================================================================
# 2. DYNAMIC PATCHING: MULTI-SCALE GRIDS -> SSCD -> 2-LAYER MLP GATE
# ==============================================================================
def make_dynamic_patching_diagram():
    fig, ax = plt.subplots(figsize=(14, 4.0), facecolor='white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.0)
    ax.axis('off')

    c_slate_dark = '#0f172a'
    c_slate_card = '#f8fafc'
    c_slate_border = '#cbd5e1'
    c_blue = '#2563eb'
    c_pink = '#db2777'
    c_emerald = '#059669'
    c_amber = '#d97706'

    # Box 1: Spliced Composite Image
    b1 = patches.FancyBboxPatch((0.4, 0.5), 2.5, 3.1, boxstyle="round,pad=0.1", facecolor=c_slate_card, edgecolor=c_slate_border, lw=1.5)
    ax.add_patch(b1)
    ax.text(1.65, 3.2, "1. SPLICED COMPOSITE", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    # Draw composite simulation
    rect_bg = patches.Rectangle((0.7, 1.4), 1.9, 1.5, facecolor='#e2e8f0', edgecolor='#94a3b8')
    ax.add_patch(rect_bg)
    ax.text(1.65, 2.3, "Desk (80% Background)", color='#64748b', fontsize=8, ha='center')
    # Donor
    rect_donor = patches.Rectangle((1.3, 1.6), 0.7, 0.5, facecolor=c_pink, edgecolor='#be185d')
    ax.add_patch(rect_donor)
    ax.text(1.65, 1.75, "Gun (20%)", color='white', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(1.65, 0.8, "Target: Isolate the Gun\nwithout human masks!", color='#475569', fontsize=8, ha='center')

    # Arrow 1 -> 2
    ax.annotate('', xy=(3.4, 2.0), xytext=(3.0, 2.0), arrowprops=dict(arrowstyle="->", color=c_blue, lw=2.5))

    # Box 2: Multi-Scale Overlapping Windows (Dynamic Patching)
    b2 = patches.FancyBboxPatch((3.5, 0.5), 3.0, 3.1, boxstyle="round,pad=0.1", facecolor=c_slate_card, edgecolor=c_blue, lw=1.5)
    ax.add_patch(b2)
    ax.text(5.0, 3.2, "2. DYNAMIC PATCHING", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    ax.text(5.0, 2.8, "Overlapping Multi-Scale Slicing", color=c_slate_dark, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(5.0, 1.9, "• 3 Scales: 25%, 35%, 50%\n• 50% Sliding Stride Overlap\n• Generates ~49 candidate crops\n• Object NEVER split in half!", color='#334155', fontsize=8.5, ha='center')
    ax.text(5.0, 0.8, "Solves Rigid Grid Failure!", color=c_emerald, fontsize=8.5, fontweight='bold', ha='center')

    # Arrow 2 -> 3
    ax.annotate('', xy=(7.0, 2.0), xytext=(6.6, 2.0), arrowprops=dict(arrowstyle="->", color=c_blue, lw=2.5))

    # Box 3: SSCD Patch Encoder
    b3 = patches.FancyBboxPatch((7.1, 0.5), 2.8, 3.1, boxstyle="round,pad=0.1", facecolor=c_slate_card, edgecolor=c_slate_border, lw=1.5)
    ax.add_patch(b3)
    ax.text(8.5, 3.2, "3. SSCD PATCH ENCODING", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    ax.text(8.5, 2.8, "Each Patch -> 512-D Vector", color=c_slate_dark, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(8.5, 1.9, "• Patch 1 (Empty desk) -> p_1\n• Patch 2 (Corner wood) -> p_2\n• Patch 14 (Handgun) -> p_14\n• All L2-normalized: ||p_i||=1", color='#334155', fontsize=8.5, ha='center')
    ax.text(8.5, 0.8, "Feature Map Generation", color=c_blue, fontsize=8.5, fontweight='bold', ha='center')

    # Arrow 3 -> 4
    ax.annotate('', xy=(10.4, 2.0), xytext=(10.0, 2.0), arrowprops=dict(arrowstyle="->", color=c_blue, lw=2.5))

    # Box 4: 2-Layer Neural MLP Importance Gate
    b4 = patches.FancyBboxPatch((10.5, 0.5), 3.1, 3.1, boxstyle="round,pad=0.1", facecolor='#f0fdf4', edgecolor=c_emerald, lw=2)
    ax.add_patch(b4)
    ax.text(12.05, 3.2, "4. 2-LAYER NEURAL GATE", color=c_emerald, fontsize=10, fontweight='bold', ha='center')
    ax.text(12.05, 2.75, "MLP Attention Weighting", color=c_slate_dark, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(12.05, 1.85, "• w_i = σ(W_2 ReLU(W_1 p_i))\n• Empty Sky / Desk -> w ≈ 0.05\n• Handgun Patch -> w = 0.94!\n• Unmasks small donor cleanly", color='#334155', fontsize=8.5, ha='center')
    ax.text(12.05, 0.8, "Recall Jumps 13% -> 88.9%!", color=c_pink, fontsize=9, fontweight='bold', ha='center')

    plt.tight_layout()
    out_p = os.path.join(out_dir, "dynamic_patching_step_flow.png")
    plt.savefig(out_p, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated dynamic_patching_step_flow.png")

# ==============================================================================
# 3. BLOCKCHAIN PROVENANCE: EASY-TO-UNDERSTAND LINKED BLOCKS
# ==============================================================================
def make_blockchain_diagram():
    fig, ax = plt.subplots(figsize=(13, 3.6), facecolor='white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 3.6)
    ax.axis('off')

    c_slate_dark = '#0f172a'
    c_blue = '#2563eb'
    c_teal = '#0d9488'
    c_amber = '#d97706'
    c_crimson = '#dc2626'

    # Block 1
    b1 = patches.FancyBboxPatch((0.5, 0.4), 3.2, 2.8, boxstyle="round,pad=0.1", facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.5)
    ax.add_patch(b1)
    ax.text(2.1, 2.8, "BLOCK #1 (PARENT A)", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    ax.text(2.1, 2.3, "Authentic Background Plate", color=c_slate_dark, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(2.1, 1.6, "• Timestamp: 09:00 AM\n• Image: Desk Scene\n• SHA-256: 0x4f8a...3b21\n• Prev Hash: 0x0000 (Genesis)", color='#475569', fontsize=8.5, ha='center')
    ax.text(2.1, 0.7, "NOTARIZED ORIGINAL", color=c_teal, fontsize=8.5, fontweight='bold', ha='center')

    # Arrow 1 -> 2 (Hash Link)
    ax.annotate('Link Hash', xy=(4.3, 1.8), xytext=(3.8, 1.8), arrowprops=dict(arrowstyle="->", color=c_blue, lw=2.5), color=c_blue, fontsize=8, ha='center', va='bottom')

    # Block 2
    b2 = patches.FancyBboxPatch((4.5, 0.4), 3.2, 2.8, boxstyle="round,pad=0.1", facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.5)
    ax.add_patch(b2)
    ax.text(6.1, 2.8, "BLOCK #2 (PARENT B)", color=c_blue, fontsize=10, fontweight='bold', ha='center')
    ax.text(6.1, 2.3, "Authentic Donor Cutout", color=c_slate_dark, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(6.1, 1.6, "• Timestamp: 10:15 AM\n• Image: 9mm Handgun\n• SHA-256: 0x7c92...11d0\n• Prev Hash: 0x4f8a (Block #1)", color='#475569', fontsize=8.5, ha='center')
    ax.text(6.1, 0.7, "NOTARIZED DONOR", color=c_teal, fontsize=8.5, fontweight='bold', ha='center')

    # Arrow 2 -> 3 (Hash Link)
    ax.annotate('Link Hash', xy=(8.3, 1.8), xytext=(7.8, 1.8), arrowprops=dict(arrowstyle="->", color=c_blue, lw=2.5), color=c_blue, fontsize=8, ha='center', va='bottom')

    # Block 3: Composite
    b3 = patches.FancyBboxPatch((8.5, 0.4), 4.0, 2.8, boxstyle="round,pad=0.1", facecolor='#fef2f2', edgecolor=c_crimson, lw=2)
    ax.add_patch(b3)
    ax.text(10.5, 2.8, "BLOCK #3 (FORGED COMPOSITE)", color=c_crimson, fontsize=10, fontweight='bold', ha='center')
    ax.text(10.5, 2.3, "Planted Spliced Evidence", color=c_slate_dark, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(10.5, 1.6, "• Timestamp: 02:45 PM\n• Lineage Proof: [Block #1 + Block #2]\n• Temporal Check: 09:00, 10:15 <= 02:45\n• Result: Valid Precedence Verified!", color='#334155', fontsize=8.5, ha='center')
    ax.text(10.5, 0.7, "TAMPER-PROOF FORENSIC PROOF", color=c_crimson, fontsize=8.5, fontweight='bold', ha='center')

    plt.tight_layout()
    out_p = os.path.join(out_dir, "blockchain_provenance_flow.png")
    plt.savefig(out_p, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated blockchain_provenance_flow.png")

if __name__ == "__main__":
    make_sscd_diagram()
    make_dynamic_patching_diagram()
    make_blockchain_diagram()
