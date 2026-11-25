import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def generate_bold_architecture():
    # 16:8.5 aspect ratio, ultra-tight margins, high DPI
    fig, ax = plt.subplots(figsize=(16, 8.5), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    
    # Elegant Slate Background
    bg_color = '#F8FAFC'
    fig.patch.set_facecolor(bg_color)

    # High-Contrast Executive Palette
    c_navy = '#0F172A'       # Slate 900
    c_blue = '#1E3A8A'       # Deep Blue
    c_cyan = '#0284C7'       # Electric Cyan
    c_dark = '#1E293B'       # Slate 800
    c_card_border = '#94A3B8'# Slate 400
    c_green = '#047857'      # Emerald 700
    c_red = '#B91C1C'        # Red 700
    c_amber = '#B45309'      # Amber 700

    # 5 Major Stages (Full Height Columns - maximizing every pixel)
    stages = [
        {"x": 0.3, "w": 2.7, "title": "STAGE 1", "sub": "Suspect Composite", "bg": "#FFFFFF", "border": c_navy},
        {"x": 3.3, "w": 2.9, "title": "STAGE 2", "sub": "74-Crop Funnel", "bg": "#FFFFFF", "border": c_cyan},
        {"x": 6.5, "w": 3.0, "title": "STAGE 3", "sub": "SSCD + Neural Gate", "bg": "#FFFFFF", "border": '#4338CA'},
        {"x": 9.8, "w": 3.2, "title": "STAGE 4", "sub": "Dual-Stream FAISS", "bg": "#FFFFFF", "border": c_green},
        {"x": 13.3, "w": 2.4, "title": "STAGE 5", "sub": "SHA-256 Ledger", "bg": "#FFFFFF", "border": c_amber}
    ]

    for s in stages:
        # Outer Card
        card = FancyBboxPatch((s["x"], 0.7), s["w"], 7.5, boxstyle="round,pad=0.08,rounding_size=0.2",
                              facecolor=s["bg"], edgecolor=s["border"], linewidth=2.5, zorder=1)
        ax.add_patch(card)
        # Header Badge
        badge = FancyBboxPatch((s["x"]+0.15, 7.45), s["w"]-0.3, 0.6, boxstyle="round,pad=0.04,rounding_size=0.1",
                               facecolor=s["border"], edgecolor='none', zorder=2)
        ax.add_patch(badge)
        ax.text(s["x"] + s["w"]/2, 7.75, s["title"], ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF', zorder=3)
        ax.text(s["x"] + s["w"]/2, 7.15, s["sub"], ha='center', va='center', fontsize=11, fontweight='bold', color=s["border"], zorder=3)

    # -------------------------------------------------------------------------
    # STAGE 1: INPUT COMPOSITE (Visual & Bold)
    # -------------------------------------------------------------------------
    # Composite Box
    box_img = FancyBboxPatch((0.5, 3.4), 2.3, 3.4, boxstyle="round,pad=0.05,rounding_size=0.15",
                             facecolor='#F1F5F9', edgecolor=c_navy, linewidth=2, zorder=3)
    ax.add_patch(box_img)
    ax.text(1.65, 6.45, "Query Composite $I_Q$", ha='center', va='center', fontsize=12, fontweight='bold', color=c_navy, zorder=4)

    # Background Desk
    rect_bg = patches.Rectangle((0.65, 3.7), 2.0, 2.4, facecolor='#E2E8F0', edgecolor='#64748B', linewidth=1.5, zorder=4)
    ax.add_patch(rect_bg)
    ax.text(1.65, 5.2, "HOST SCENE\n(Desk: 85% Pixels)", ha='center', va='center', fontsize=10, fontweight='bold', color='#334155', zorder=5)

    # Spliced Gun
    rect_gun = patches.Rectangle((1.1, 3.9), 1.1, 0.75, facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=2.5, zorder=6)
    ax.add_patch(rect_gun)
    ax.text(1.65, 4.27, "SPLICED DONOR\n(Gun: 15% Area)", ha='center', va='center', fontsize=9, fontweight='bold', color='#991B1B', zorder=7)

    # Bottom Alert Callout
    ax.text(1.65, 1.9, "FATAL FLAW:\nGlobal Average Pooling\ndrowns out the 15% gun\ninside the 85% desk!", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#B91C1C',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF2F2', edgecolor='#F87171', lw=1.8), zorder=4)

    # Arrow 1 -> 2
    ax.annotate("", xy=(3.3, 4.5), xytext=(2.8, 4.5),
                arrowprops=dict(arrowstyle="->,head_width=0.5,head_length=0.5", color=c_cyan, lw=3.5), zorder=10)

    # -------------------------------------------------------------------------
    # STAGE 2: 74-CROP FUNNEL (Bold Multi-Scale)
    # -------------------------------------------------------------------------
    scales = [
        {"y": 5.7, "title": "Scale 1: 50% Window", "sub": "200 x 150  |  9 Crops\nCaptures Coarse Context", "col": "#0284C7", "bg": "#E0F2FE"},
        {"y": 4.2, "title": "Scale 2: 35% Window", "sub": "140 x 105  |  16 Crops\nCaptures Medium Objects", "col": "#0284C7", "bg": "#E0F2FE"},
        {"y": 2.7, "title": "Scale 3: 25% Window", "sub": "100 x 75   |  49 Crops\nCaptures Tight Spliced Gun!", "col": "#D97706", "bg": "#FEF3C7"}
    ]
    for sc in scales:
        b = FancyBboxPatch((3.5, sc["y"]-0.55), 2.5, 1.25, boxstyle="round,pad=0.04,rounding_size=0.1",
                           facecolor=sc["bg"], edgecolor=sc["col"], linewidth=2, zorder=3)
        ax.add_patch(b)
        ax.text(4.75, sc["y"]+0.25, sc["title"], ha='center', va='center', fontsize=10.5, fontweight='bold', color=sc["col"], zorder=4)
        ax.text(4.75, sc["y"]-0.2, sc["sub"], ha='center', va='center', fontsize=9, fontweight='bold', color=c_dark, zorder=4)

    ax.text(4.75, 1.35, "50% STRIDE GUARANTEE:\nDelta x = 0.5W, Delta y = 0.5H\nZero Blind Spots: 74 Total Crops", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0369A1',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#F0F9FF', edgecolor='#38BDF8', lw=1.8), zorder=4)

    # Arrow 2 -> 3
    ax.annotate("", xy=(6.5, 4.5), xytext=(6.0, 4.5),
                arrowprops=dict(arrowstyle="->,head_width=0.5,head_length=0.5", color='#4338CA', lw=3.5), zorder=10)

    # -------------------------------------------------------------------------
    # STAGE 3: EMBEDDING & NEURAL ATTENTION GATE
    # -------------------------------------------------------------------------
    # Meta SSCD Box
    b_sscd = FancyBboxPatch((6.7, 5.1), 2.6, 1.7, boxstyle="round,pad=0.05,rounding_size=0.12",
                            facecolor='#EEF2FF', edgecolor='#4338CA', linewidth=2.2, zorder=3)
    ax.add_patch(b_sscd)
    ax.text(8.0, 6.35, "Meta SSCD Model", ha='center', va='center', fontsize=12, fontweight='bold', color='#3730A3', zorder=4)
    ax.text(8.0, 5.7, "Self-Supervised ResNet-50\nTransforms each crop to\n512-D Normalized Vector", ha='center', va='center', fontsize=9.5, fontweight='bold', color=c_dark, zorder=4)

    # Arrow SSCD -> MLP
    ax.annotate("", xy=(8.0, 4.4), xytext=(8.0, 5.1),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", color='#4338CA', lw=3.0), zorder=10)

    # Neural MLP Attention Gate
    b_mlp = FancyBboxPatch((6.7, 2.1), 2.6, 2.2, boxstyle="round,pad=0.05,rounding_size=0.12",
                           facecolor='#F0FDF4', edgecolor=c_green, linewidth=2.5, zorder=3)
    ax.add_patch(b_mlp)
    ax.text(8.0, 3.9, "Neural Attention Gate", ha='center', va='center', fontsize=11.5, fontweight='bold', color=c_green, zorder=4)
    ax.text(8.0, 3.35, "2-Layer MLP (ReLU + Sigmoid)\nLearns Salience Scoring", ha='center', va='center', fontsize=9.5, color='#166534', zorder=4)
    ax.text(8.0, 2.55, "DISCARDS BACKGROUND\nSelects Top 5 Salient Patches!\n(Done in < 15 ms on GPU)", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#15803D',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#DCFCE7', edgecolor='#4ADE80', lw=1.2), zorder=5)

    # Arrow 3 -> 4
    ax.annotate("", xy=(9.8, 5.5), xytext=(9.3, 5.5),
                arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.45", color=c_blue, lw=3.0), zorder=10)
    ax.annotate("", xy=(9.8, 3.2), xytext=(9.3, 3.2),
                arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.45", color='#D97706', lw=3.0), zorder=10)

    # -------------------------------------------------------------------------
    # STAGE 4: DUAL-STREAM FAISS & CONSENSUS
    # -------------------------------------------------------------------------
    # Stream A (Global Scene)
    b_sa = FancyBboxPatch((10.0, 4.9), 2.8, 1.8, boxstyle="round,pad=0.05,rounding_size=0.12",
                          facecolor='#F0F9FF', edgecolor=c_blue, linewidth=2.2, zorder=3)
    ax.add_patch(b_sa)
    ax.text(11.4, 6.35, "STREAM A: Global Scene", ha='center', va='center', fontsize=11, fontweight='bold', color=c_blue, zorder=4)
    ax.text(11.4, 5.75, "Query: 512-D Full-Image Vector\nTarget: Open-World FAISS Index", ha='center', va='center', fontsize=9, color=c_dark, zorder=4)
    ax.text(11.4, 5.18, "--> Parent A: DESK (Sim = 0.9412)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0369A1', zorder=4)

    # Stream B (Donor Patch)
    b_sb = FancyBboxPatch((10.0, 2.8), 2.8, 1.8, boxstyle="round,pad=0.05,rounding_size=0.12",
                          facecolor='#FEF3C7', edgecolor='#D97706', linewidth=2.2, zorder=3)
    ax.add_patch(b_sb)
    ax.text(11.4, 4.25, "STREAM B: Salient Patch", ha='center', va='center', fontsize=11, fontweight='bold', color='#B45309', zorder=4)
    ax.text(11.4, 3.65, "Query: Top-5 Salient Vectors\nTarget: Open-World FAISS Index", ha='center', va='center', fontsize=9, color=c_dark, zorder=4)
    ax.text(11.4, 3.08, "--> Parent B: GUN (Sim = 0.8874)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#B45309', zorder=4)

    # Consensus Badge
    b_con = FancyBboxPatch((10.0, 1.0), 2.8, 1.5, boxstyle="round,pad=0.05,rounding_size=0.12",
                           facecolor='#ECFDF5', edgecolor=c_green, linewidth=2.5, zorder=3)
    ax.add_patch(b_con)
    ax.text(11.4, 2.1, "LINEAGE CONSENSUS", ha='center', va='center', fontsize=11, fontweight='bold', color=c_green, zorder=4)
    ax.text(11.4, 1.45, "Parent A != Parent B\nTWO DISTINCT PARENTS VERIFIED!\n(Dual Recall@1: 88.9%)", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#065F46', zorder=4)

    # Arrow 4 -> 5
    ax.annotate("", xy=(13.3, 3.5), xytext=(12.8, 3.5),
                arrowprops=dict(arrowstyle="->,head_width=0.5,head_length=0.5", color=c_amber, lw=3.5), zorder=10)

    # -------------------------------------------------------------------------
    # STAGE 5: SHA-256 BLOCKCHAIN CUSTODY
    # -------------------------------------------------------------------------
    b_blk = FancyBboxPatch((13.45, 2.7), 2.1, 4.0, boxstyle="round,pad=0.05,rounding_size=0.15",
                           facecolor='#FFFBEB', edgecolor=c_amber, linewidth=2.5, zorder=3)
    ax.add_patch(b_blk)
    ax.text(14.5, 6.35, "BLOCK #128", ha='center', va='center', fontsize=12, fontweight='bold', color='#92400E', zorder=4)
    
    blk_items = [
        ("PrevHash:", "0x8a9f...3c"),
        ("Parent A:", "0x14d3...e7"),
        ("Parent B:", "0x93b7...a1"),
        ("Time Proof:", "T_A, T_B <= T_Q"),
        ("Block Hash:", "0x7c42...9f")
    ]
    y_b = 5.7
    for label, val in blk_items:
        ax.text(14.5, y_b, f"{label} {val}", ha='center', va='center', fontsize=8.5, family='monospace', fontweight='bold', color=c_dark, zorder=4)
        y_b -= 0.65

    # Legal Seal Box
    ax.text(14.5, 1.5, "LEGAL CUSTODY:\nSec 65B Evidence Act\nTamper-Proof Ledger\n100% Immutable", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#065F46',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#D1FAE5', edgecolor='#10B981', lw=1.8), zorder=4)

    # Top/Bottom Pipeline Latency Summary Bar
    bar = patches.Rectangle((0.3, 0.08), 15.4, 0.45, facecolor='#0F172A', zorder=10)
    ax.add_patch(bar)
    ax.text(8.0, 0.31, "END-TO-END AUDIT LATENCY: 42.4 ms  |  DUAL-PARENT RECALL: 88.9%  |  CRYPTOGRAPHIC CUSTODY: 100% IMMUTABLE",
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#FFFFFF', zorder=11)

    output_path = "/Users/viveknegi/Downloads/DAC_Presentation_Overleaf/provenance_ai_system_architecture.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Generated bold, massive architecture diagram successfully.")

if __name__ == "__main__":
    generate_bold_architecture()
