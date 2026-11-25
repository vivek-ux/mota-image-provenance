#!/usr/bin/env python3
"""
generate_composite_diagram.py
Generates a crisp 4-panel forensic educational graphic:
"How a Composite Image is Created (Mathematical & Visual Breakdown)"
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def generate_composite_diagram():
    out_dir = "/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance"
    out_path = os.path.join(out_dir, "composite_formation_pipeline.png")

    bg_path = os.path.join(out_dir, "gallery", "crime_scene_desk.jpg")
    donor_path = os.path.join(out_dir, "donor_handgun_exact.png")
    comp_path = os.path.join(out_dir, "crime_scene_handgun_composite.png")

    img_bg = Image.open(bg_path).convert("RGB").resize((400, 300))
    img_comp = Image.open(comp_path).convert("RGB").resize((400, 300))
    
    # Load donor with transparency
    img_donor = Image.open(donor_path).convert("RGBA").resize((400, 300))
    
    # Extract alpha mask
    donor_arr = np.array(img_donor)
    alpha = donor_arr[:, :, 3]
    mask_binary = (alpha > 20).astype(np.float32)

    # Dark studio background for donor cutout visualization
    donor_rgb = donor_arr[:, :, :3]
    checker = np.ones((300, 400, 3), dtype=np.uint8) * 35
    # Place donor on dark background
    donor_preview = np.where(mask_binary[:, :, None] > 0, donor_rgb, checker)

    fig, axes = plt.subplots(1, 4, figsize=(15, 3.8), facecolor='#0b0f19')

    # Panel 1: Parent Plate A
    axes[0].imshow(img_bg)
    axes[0].set_title("1. Parent Plate A (Background)\nAuthentic Scene Plate", color='#38bdf8', fontsize=11, fontweight='bold', pad=10)
    axes[0].axis('off')
    for s in axes[0].spines.values():
        s.set_edgecolor('#38bdf8')
        s.set_linewidth(1.5)

    # Panel 2: Parent Plate B
    axes[1].imshow(donor_preview)
    axes[1].set_title("2. Parent Plate B (Donor)\nIsolated Object Cutout", color='#ec4899', fontsize=11, fontweight='bold', pad=10)
    axes[1].axis('off')
    for s in axes[1].spines.values():
        s.set_edgecolor('#ec4899')
        s.set_linewidth(1.5)

    # Panel 3: Alpha Feathering Mask
    axes[2].imshow(mask_binary, cmap='magma')
    axes[2].set_title("3. Spatial Feathering Mask\nM(x,y) Boundary Weights", color='#f59e0b', fontsize=11, fontweight='bold', pad=10)
    axes[2].axis('off')
    for s in axes[2].spines.values():
        s.set_edgecolor('#f59e0b')
        s.set_linewidth(1.5)

    # Panel 4: Composite Spliced Result
    axes[3].imshow(img_comp)
    axes[3].set_title("4. Multi-Source Composite\nI_comp = (1-M)⊙I_A + M⊙I_B", color='#10b981', fontsize=11, fontweight='bold', pad=10)
    axes[3].axis('off')
    for s in axes[3].spines.values():
        s.set_edgecolor('#10b981')
        s.set_linewidth(2)

    fig.text(0.5, 0.05, "Mathematical Composition Formulation: Seamless Linear Alpha Blending across Boundary Manifold",
             color='#94a3b8', fontsize=10, ha='center', fontweight='medium')

    plt.tight_layout(rect=[0.02, 0.08, 0.98, 0.95])
    plt.savefig(out_path, dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated composite formation diagram at: {out_path}")

if __name__ == "__main__":
    generate_composite_diagram()
