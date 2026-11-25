import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

def create_system_architecture():
    # Setup canvas: wide aspect ratio (16:7), ultra high DPI
    fig, ax = plt.subplots(figsize=(16, 7.2), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7.2)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Color Palette: Modern Minimalist Slate-Grey & Tech-Blue
    c_bg_box = '#F8FAFC'
    c_border = '#CBD5E1'
    c_blue = '#1E3A8A'       # Primary deep blue
    c_cyan = '#0284C7'       # Vibrant tech cyan
    c_dark = '#0F172A'       # Slate black
    c_gray = '#475569'       # Muted slate text
    c_accent_green = '#059669' # Emerald verification
    c_accent_orange = '#D97706' # Orange donor/patch

    # Title Banner
    ax.text(8.0, 6.85, "ProvenanceAI: End-to-End System Architecture Pipeline", 
            ha='center', va='center', fontsize=18, fontweight='bold', color=c_dark, family='sans-serif')
    ax.text(8.0, 6.45, "Multi-Scale Overlapping Gridding  |  SSCD Embedding  |  Neural Attention Gate  |  Dual-Stream Consensus  |  Blockchain Custody",
            ha='center', va='center', fontsize=10.5, color=c_gray, style='italic', family='sans-serif')

    # 5 Major Architectural Stages (Columns)
    stages = [
        {"x": 0.4, "w": 2.4, "title": "Stage 1: Input", "sub": "Suspect Composite", "color": "#E2E8F0"},
        {"x": 3.2, "w": 2.6, "title": "Stage 2: Gridding", "sub": "74 Multi-Scale Crops", "color": "#E0F2FE"},
        {"x": 6.2, "w": 2.7, "title": "Stage 3: Embedding", "sub": "SSCD + Neural Gate", "color": "#EEF2FF"},
        {"x": 9.3, "w": 3.2, "title": "Stage 4: Dual Retrieval", "sub": "FAISS Consensus Engine", "color": "#F0FDF4"},
        {"x": 12.9, "w": 2.7, "title": "Stage 5: Custody", "sub": "SHA-256 Blockchain", "color": "#FEF3C7"}
    ]

    # Draw Stage Enclosures (soft background cards)
    for s in stages:
        rect = FancyBboxPatch((s["x"], 0.5), s["w"], 5.6, boxstyle="round,pad=0.08,rounding_size=0.2",
                              facecolor=s["color"], edgecolor=c_border, linewidth=1.2, alpha=0.5, zorder=1)
        ax.add_patch(rect)
        ax.text(s["x"] + s["w"]/2, 5.85, s["title"], ha='center', va='center', fontsize=11, fontweight='bold', color=c_blue)
        ax.text(s["x"] + s["w"]/2, 5.60, s["sub"], ha='center', va='center', fontsize=8.5, color=c_gray)

    # -------------------------------------------------------------
    # STAGE 1: INPUT COMPOSITE
    # -------------------------------------------------------------
    # Query Image representation
    box_q = FancyBboxPatch((0.6, 2.7), 2.0, 2.5, boxstyle="round,pad=0.04,rounding_size=0.15",
                           facecolor="#FFFFFF", edgecolor=c_blue, linewidth=2, zorder=2)
    ax.add_patch(box_q)
    ax.text(1.6, 4.8, "Query Composite $I_Q$", ha='center', va='center', fontsize=10, fontweight='bold', color=c_dark)
    
    # Visual inner elements (Desk + Spliced Gun)
    rect_desk = patches.Rectangle((0.75, 3.1), 1.7, 1.4, facecolor="#F1F5F9", edgecolor="#94A3B8", linewidth=1.2, zorder=3)
    ax.add_patch(rect_desk)
    ax.text(1.6, 3.95, "Host Scene\n(Desk: ~85%)", ha='center', va='center', fontsize=8, color=c_gray, zorder=4)
    
    rect_gun = patches.Rectangle((1.2, 3.25), 0.7, 0.45, facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=1.5, zorder=5)
    ax.add_patch(rect_gun)
    ax.text(1.55, 3.47, "Spliced Donor\n(Gun: ~15%)", ha='center', va='center', fontsize=7, fontweight='bold', color="#991B1B", zorder=6)

    # Note
    ax.text(1.6, 1.6, "Challenge:\nGlobal average pooling\nmasks the 15% donor.", 
            ha='center', va='center', fontsize=8, color=c_gray, bbox=dict(boxstyle='square,pad=0.3', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.8))

    # Arrow 1 -> 2
    ax.annotate("", xy=(3.2, 3.9), xytext=(2.7, 3.9),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", color=c_cyan, lw=2.5))

    # -------------------------------------------------------------
    # STAGE 2: MULTI-SCALE 50% OVERLAP GRIDDING (74 CROPS)
    # -------------------------------------------------------------
    # 3 Scale boxes
    scales_info = [
        {"y": 4.5, "txt": "Scale 1 (50% Win): 9 Crops\nWindow: 200 x 150 (Context)", "col": "#0284C7"},
        {"y": 3.3, "txt": "Scale 2 (35% Win): 16 Crops\nWindow: 140 x 105 (Medium)", "col": "#0284C7"},
        {"y": 2.1, "txt": "Scale 3 (25% Win): 49 Crops\nWindow: 100 x 75 (Tight Splicing)", "col": "#D97706"}
    ]
    for sc in scales_info:
        b = FancyBboxPatch((3.4, sc["y"]-0.4), 2.2, 0.85, boxstyle="round,pad=0.04,rounding_size=0.1",
                           facecolor="#FFFFFF", edgecolor=sc["col"], linewidth=1.5, zorder=2)
        ax.add_patch(b)
        ax.text(4.5, sc["y"], sc["txt"], ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_dark)

    ax.text(4.5, 1.05, "50% Overlap Stride Guarantee:\n$\\Delta x = 0.5 W, \\; \\Delta y = 0.5 H$\n$\\rightarrow 74$ Total Intact Crops", 
            ha='center', va='center', fontsize=8, fontweight='bold', color=c_blue,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFFFFF', edgecolor=c_cyan, lw=1.2))

    # Arrow 2 -> 3
    ax.annotate("", xy=(6.2, 3.9), xytext=(5.7, 3.9),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", color=c_cyan, lw=2.5))

    # -------------------------------------------------------------
    # STAGE 3: EMBEDDING & NEURAL ATTENTION GATING
    # -------------------------------------------------------------
    # SSCD Feature Extractor
    b_sscd = FancyBboxPatch((6.4, 4.3), 2.3, 1.0, boxstyle="round,pad=0.04,rounding_size=0.1",
                            facecolor="#FFFFFF", edgecolor=c_blue, linewidth=1.5, zorder=2)
    ax.add_patch(b_sscd)
    ax.text(7.55, 4.9, "Meta SSCD Model", ha='center', va='center', fontsize=9, fontweight='bold', color=c_blue)
    ax.text(7.55, 4.55, "Self-Supervised ResNet-50\n$74 \\times 512$-D Embeddings", ha='center', va='center', fontsize=7.5, color=c_gray)

    # Arrow SSCD -> Gate
    ax.annotate("", xy=(7.55, 3.8), xytext=(7.55, 4.25),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.3", color=c_blue, lw=1.8))

    # Neural Attention Gate (MLP)
    b_mlp = FancyBboxPatch((6.4, 2.3), 2.3, 1.45, boxstyle="round,pad=0.04,rounding_size=0.1",
                           facecolor="#FFFFFF", edgecolor="#4F46E5", linewidth=1.8, zorder=2)
    ax.add_patch(b_mlp)
    ax.text(7.55, 3.45, "Neural Salience Gate (MLP)", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#4F46E5")
    ax.text(7.55, 3.10, "Linear(512 $\\to$ 64) + ReLU\nLinear(64 $\\to$ 1) + Sigmoid", ha='center', va='center', fontsize=7.5, color=c_gray)
    ax.text(7.55, 2.60, "Discards Flat Background\nFilter: 74 $\\to$ Top 5 Patches", ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_accent_green)

    ax.text(7.55, 1.05, "Parallel Batching:\nMatrix Multiplication in CUDA\nLatency: < 15 ms", 
            ha='center', va='center', fontsize=8, color=c_gray,
            bbox=dict(boxstyle='square,pad=0.3', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.8))

    # Arrow 3 -> 4
    ax.annotate("", xy=(9.3, 4.6), xytext=(8.8, 4.6),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", color=c_blue, lw=2))
    ax.annotate("", xy=(9.3, 2.9), xytext=(8.8, 2.9),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", color="#D97706", lw=2))

    # -------------------------------------------------------------
    # STAGE 4: DUAL-STREAM FAISS RETRIEVAL & CONSENSUS
    # -------------------------------------------------------------
    # Stream A: Global Scene Match
    b_st_a = FancyBboxPatch((9.5, 4.1), 2.8, 1.25, boxstyle="round,pad=0.04,rounding_size=0.1",
                            facecolor="#FFFFFF", edgecolor=c_blue, linewidth=1.5, zorder=2)
    ax.add_patch(b_st_a)
    ax.text(10.9, 5.05, "Stream A: Global Scene Retrieval", ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_blue)
    ax.text(10.9, 4.70, "Query: 512-D Whole-Image Vector", ha='center', va='center', fontsize=7.5, color=c_gray)
    ax.text(10.9, 4.35, "-> Parent A: Desk (Sim = 0.9412)", ha='center', va='center', fontsize=8, fontweight='bold', color=c_accent_green)

    # Stream B: Salient Patches Match
    b_st_b = FancyBboxPatch((9.5, 2.4), 2.8, 1.25, boxstyle="round,pad=0.04,rounding_size=0.1",
                            facecolor="#FFFFFF", edgecolor="#D97706", linewidth=1.5, zorder=2)
    ax.add_patch(b_st_b)
    ax.text(10.9, 3.35, "Stream B: Local Donor Retrieval", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#D97706")
    ax.text(10.9, 3.00, "Query: Top-5 Salient Patch Vectors", ha='center', va='center', fontsize=7.5, color=c_gray)
    ax.text(10.9, 2.65, "-> Parent B: Handgun (Sim = 0.8874)", ha='center', va='center', fontsize=8, fontweight='bold', color=c_accent_green)

    # Dual Consensus Engine Box
    b_con = FancyBboxPatch((9.5, 0.85), 2.8, 1.15, boxstyle="round,pad=0.04,rounding_size=0.1",
                           facecolor="#FFFFFF", edgecolor=c_accent_green, linewidth=1.8, zorder=2)
    ax.add_patch(b_con)
    ax.text(10.9, 1.65, "Dual-Stream Consensus Engine", ha='center', va='center', fontsize=9, fontweight='bold', color=c_accent_green)
    ax.text(10.9, 1.25, "Confirms Disjoint Lineage Origins:\nParent A != Parent B -> Forgery Flagged", ha='center', va='center', fontsize=7.5, color=c_dark)

    # Arrow inside Stage 4 -> Consensus
    ax.annotate("", xy=(10.9, 2.05), xytext=(10.9, 2.35),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.25", color=c_accent_green, lw=1.5))

    # Arrow 4 -> 5
    ax.annotate("", xy=(12.9, 2.7), xytext=(12.4, 2.7),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", color=c_blue, lw=2.5))

    # -------------------------------------------------------------
    # STAGE 5: CRYPTOGRAPHIC BLOCKCHAIN LEDGER
    # -------------------------------------------------------------
    # Blockchain Block Representation
    b_blk = FancyBboxPatch((13.1, 2.5), 2.3, 2.8, boxstyle="round,pad=0.04,rounding_size=0.15",
                           facecolor="#FFFFFF", edgecolor="#B45309", linewidth=2, zorder=2)
    ax.add_patch(b_blk)
    ax.text(14.25, 5.0, "SHA-256 Custody Block", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#B45309")
    
    blk_lines = [
        "Index: #128",
        "PrevHash: 0x8a9f...3c",
        "Timestamp: $T_{comp}$",
        "Parent A Hash: 0x14d...e7",
        "Parent B Hash: 0x93b...a1",
        "Proof: T_A, T_B <= T_comp",
        "BlockHash: 0x7c42...9f"
    ]
    y_pos = 4.55
    for l in blk_lines:
        ax.text(14.25, y_pos, l, ha='center', va='center', fontsize=7, family='monospace', color=c_dark)
        y_pos -= 0.32

    ax.text(14.25, 1.2, "Legal Validity:\nSection 65B Indian Evidence Act\nTamper-Proof Audit Trail\nChain Integrity Intact",
            ha='center', va='center', fontsize=7.5, fontweight='bold', color="#065F46",
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#ECFDF5', edgecolor='#10B981', lw=1.2))

    # Bottom summary footer bar inside the image
    rect_bar = patches.Rectangle((0.4, 0.05), 15.2, 0.35, facecolor="#0F172A", zorder=10)
    ax.add_patch(rect_bar)
    ax.text(8.0, 0.22, "End-to-End Pipeline Latency: 42.4 ms  |  Overall Dual-Parent Recall@1: 88.9%  |  Cryptographic Custody: 100% Immutable",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color="#FFFFFF", zorder=11)

    plt.tight_layout()
    output_path = "/Users/viveknegi/Downloads/DAC_Presentation_Overleaf/provenance_ai_system_architecture.png"
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"Generated successfully at {output_path}")

if __name__ == "__main__":
    create_system_architecture()
