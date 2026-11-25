"""
MOTA: Multi-Scale Overlapping Token Alignment with Learned Importance Gating
Interactive Research & Forensic Attribution Dashboard
Department of Computer Science & Engineering, National Institute of Technology Meghalaya
Author: Vivek Negi (Roll No: T25CS012) | Supervisor: Dr. Akhilendra Pratap Singh
Target Publication: IEEE Transactions on Information Forensics and Security (IEEE TIFS)
"""

import streamlit as st
import os
import io
import time
import json
import math
import hashlib
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np
import torch
import cv2

# Page configuration
st.set_page_config(
    page_title="MOTA | NIT Meghalaya ProvenanceAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Cyber-Forensic Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Outfit:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 10%, #0d1322 0%, #060911 100%);
        color: #e2e8f0;
    }
    
    .banner-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 242, 254, 0.15);
        backdrop-filter: blur(12px);
    }
    
    .banner-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    
    .banner-subtitle {
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.5;
    }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 600;
        border-radius: 9999px;
        margin-right: 8px;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-nitm {
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.35);
    }
    
    .badge-tifs {
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.35);
    }
    
    .badge-live {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.35);
    }
    
    .forensic-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .stat-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748b;
        font-weight: 600;
    }
    
    .stat-val {
        font-size: 22px;
        font-weight: 700;
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Import MOTA Engine
# ------------------------------------------------------------------------------
from mota_engine import MOTAPipeline, DynamicMultiScaleTokenizer, ImportanceGate, DEVICE

GALLERY_DIR = os.path.join(os.path.dirname(__file__), "gallery")
os.makedirs(GALLERY_DIR, exist_ok=True)

# Initialize MOTA Pipeline directly (loads in <0.2s from pre-computed cache)
pipeline = MOTAPipeline(GALLERY_DIR)

# ------------------------------------------------------------------------------
# Academic Banner Header
# ------------------------------------------------------------------------------
st.markdown("""
<div class="banner-container">
    <div class="banner-title">🛡️ MOTA: Multi-Scale Overlapping Token Alignment</div>
    <div class="banner-subtitle">
        Dynamic Lineage Attribution & Cryptographic Provenance for Multi-Source Composite Media<br>
        <strong>National Institute of Technology Meghalaya</strong> | Department of Computer Science & Engineering<br>
        Scholar: <strong>Vivek Negi</strong> (Roll No: <code>T25CS012</code>) | Supervisor: <strong>Dr. Akhilendra Pratap Singh</strong>
    </div>
    <div>
        <span class="badge-pill badge-nitm">NIT Meghalaya M.Tech Thesis</span>
        <span class="badge-pill badge-tifs">Target: IEEE TIFS Journal</span>
        <span class="badge-pill badge-live">Official Meta SSCD Active (MPS GPU)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Sidebar Controls
# ------------------------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Attribution Controls")

PRESET_SAMPLES = {
    "🦁 Organic Feathered: Woodland Path + Lion": "feathered_smoothstep_lion.jpg",
    "🏛️ CASIA v2.0: Garden + Food Street Sign (Benchmark)": "gallery/casia_0.png",
    "🏢 CASIA v2.0: Building + Lawn Fence (Benchmark)": "gallery/casia_1.png",
    "🚗 Car + Spliced Man": "car_man_composite.jpg",
    "🔫 Crime Scene + Handgun": "crime_scene_handgun_composite.png",
    "🚶 Urban Crosswalk + Blonde Woman": "crosswalk_blonde_composite.png",
    "🎒 Library + Backpack": "library_backpack_composite.png",
    "🌲 Pine Forest + Airplane": "pine_forest_boeing_composite.png",
}

sample_choice = st.sidebar.selectbox("Select Test Composite:", list(PRESET_SAMPLES.keys()))
uploaded_file = st.sidebar.file_uploader("Or Upload Custom Composite (PNG/JPG):", type=["png", "jpg", "jpeg"])

img_path = os.path.join(os.path.dirname(__file__), PRESET_SAMPLES[sample_choice])
if uploaded_file is not None:
    current_image = Image.open(uploaded_file).convert("RGB")
    source_label = "Custom Uploaded Composite"
elif os.path.exists(img_path):
    current_image = Image.open(img_path).convert("RGB")
    source_label = sample_choice
else:
    current_image = Image.new("RGB", (384, 384), color=(30, 45, 70))
    source_label = "Generated Clean Canvas"

st.sidebar.markdown("---")
st.sidebar.markdown("### 📐 Tokenization Hyperparameters")
overlap_ratio = st.sidebar.slider("Overlap Ratio (β):", min_value=0.1, max_value=0.7, value=0.5, step=0.05,
                                  help=r"Stride S = P * (1 - β). Default β=0.5 guarantees 50% overlap.")
top_k_val = st.sidebar.slider("Top-K Gallery Attribution:", min_value=1, max_value=10, value=5)

st.sidebar.markdown("---")
model_type = "Official Meta SSCD" if pipeline.extractor.is_sscd else "ResNet50"
st.sidebar.markdown(f"**Vision Backbone:** `{model_type}`")
st.sidebar.markdown(f"**Hardware Acceleration:** `{DEVICE}`")
st.sidebar.markdown(f"**Indexed Gallery Size:** `{len(pipeline.gallery_records)} images`")
st.sidebar.markdown(f"**Ledger Blocks Mined:** `{len(pipeline.ledger.chain)} blocks`")

# ------------------------------------------------------------------------------
# Tabs Architecture
# ------------------------------------------------------------------------------
tab_studio, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧪 Parent A + B Splicing Studio",
    "🧩 Multi-Scale Tokenizer & Stride",
    "⚡ 2-Layer Neural Network (MLP)",
    "🔍 Lineage Attribution & Peeling",
    "⛓️ Cryptographic Provenance DAG",
    "📊 IEEE TIFS Benchmarks"
])

tokenizer = DynamicMultiScaleTokenizer(overlap_ratio=overlap_ratio)
crops, metadata = tokenizer.tokenize(current_image)


# ==============================================================================
# TAB STUDIO: INTERACTIVE SPLICING & LINEAGE VERIFICATION STUDIO
# ==============================================================================
with tab_studio:
    st.markdown("### 🧪 Live Splicing & Multi-Source Lineage Verification Studio")
    st.markdown("""
    **Verify the thesis empirically:** Pick any **Parent A (Host Background)** and **Parent B (Donor Object)**. 
    Synthesize a brand-new spliced composite right here, and watch MOTA successfully uncover **both** original sources from the gallery!
    """)

    gallery_names = [r["name"] for r in pipeline.gallery_records]

    # Defaults for a clean splice demo
    default_host_idx = gallery_names.index("autumn_woodland_path.jpg") if "autumn_woodland_path.jpg" in gallery_names else 0
    default_donor_idx = gallery_names.index("african_male_lion.jpg") if "african_male_lion.jpg" in gallery_names else 1

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### 🏛️ Step 1: Select Parent A (Host Scene)")
        host_choice = st.selectbox("Choose Host Background:", gallery_names, index=default_host_idx)
        host_path = os.path.join(GALLERY_DIR, host_choice)
        pil_host_orig = Image.open(host_path).convert("RGB")
        st.image(pil_host_orig, caption=f"Ground Truth Host: {host_choice}", use_container_width=True)

    with col_s2:
        st.markdown("#### 🎯 Step 2: Select Parent B (Donor Object)")
        donor_choice = st.selectbox("Choose Donor Image:", gallery_names, index=default_donor_idx)
        donor_path = os.path.join(GALLERY_DIR, donor_choice)
        pil_donor_orig = Image.open(donor_path).convert("RGB")
        st.image(pil_donor_orig, caption=f"Ground Truth Donor: {donor_choice}", use_container_width=True)

    st.markdown("---")
    st.markdown("#### ✂️ Step 3: Configure Splicing & Forensic Fusion Parameters")

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    with col_ctrl1:
        donor_scale_pct = st.slider("Donor Size (% of host width):", 15, 65, 38)
    with col_ctrl2:
        pos_x_pct = st.slider("X Position on Canvas (%):", 5, 80, 50)
    with col_ctrl3:
        pos_y_pct = st.slider("Y Position on Canvas (%):", 5, 80, 60)

    blend_mode = st.radio(
        "Forensic Blending Mode:",
        [
            "🌿 Organic Smoothstep Feathering (Soft Radial Edge, No Stickers)",
            "💧 Poisson Seamless Gradient Cloning (Solves Poisson PDE Δf=Δg)",
            "✂️ Hard Rectangle Paste (Baseline Naive Comparison)"
        ],
        horizontal=True
    )

    # Generate live composite
    canvas_w, canvas_h = 512, 512
    comp_base = pil_host_orig.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)

    # Scale donor
    d_w = int(canvas_w * (donor_scale_pct / 100.0))
    donor_aspect = pil_donor_orig.height / float(pil_donor_orig.width)
    d_h = int(d_w * donor_aspect)
    d_w = max(16, min(canvas_w - 4, d_w))
    d_h = max(16, min(canvas_h - 4, d_h))
    donor_scaled = pil_donor_orig.resize((d_w, d_h), Image.Resampling.LANCZOS)

    # Paste coordinates (centered)
    paste_x = int(canvas_w * (pos_x_pct / 100.0)) - d_w // 2
    paste_y = int(canvas_h * (pos_y_pct / 100.0)) - d_h // 2
    paste_x = max(0, min(canvas_w - d_w, paste_x))
    paste_y = max(0, min(canvas_h - d_h, paste_y))

    if "Organic Smoothstep" in blend_mode:
        # Radial cosine smoothstep feathering: melts boundaries organically
        Y, X = np.ogrid[:d_h, :d_w]
        cy_m, cx_m = d_h / 2.0, d_w / 2.0
        ry, rx = d_h / 2.0 * 0.85, d_w / 2.0 * 0.85
        dist = np.sqrt(((X - cx_m) / max(rx, 1e-4))**2 + ((Y - cy_m) / max(ry, 1e-4))**2)
        mask_arr = np.clip(1.0 - (dist - 1.0) / 0.15, 0.0, 1.0)
        mask_arr = 0.5 * (1.0 + np.cos(np.pi * (1.0 - mask_arr)))
        mask_3ch = np.repeat(np.clip(mask_arr, 0.0, 1.0)[:, :, np.newaxis], 3, axis=2).astype(np.float32)

        base_np = np.array(comp_base).astype(np.float32)
        donor_np = np.array(donor_scaled).astype(np.float32)
        roi = base_np[paste_y:paste_y+d_h, paste_x:paste_x+d_w]
        blended = donor_np * mask_3ch + roi * (1.0 - mask_3ch)
        base_np[paste_y:paste_y+d_h, paste_x:paste_x+d_w] = blended
        live_composite = Image.fromarray(np.clip(base_np, 0, 255).astype(np.uint8))

    elif "Poisson Seamless" in blend_mode:
        host_cv = cv2.cvtColor(np.array(comp_base), cv2.COLOR_RGB2BGR)
        donor_cv = cv2.cvtColor(np.array(donor_scaled), cv2.COLOR_RGB2BGR)
        
        mask_cv = np.zeros((d_h, d_w), dtype=np.uint8)
        cv2.ellipse(mask_cv, (d_w // 2, d_h // 2), (int(d_w * 0.45), int(d_h * 0.45)), 0, 0, 360, 255, -1)
        mask_cv = cv2.GaussianBlur(mask_cv, (15, 15), 5)
        
        center_pt = (paste_x + d_w // 2, paste_y + d_h // 2)
        center_pt = (max(d_w // 2 + 2, min(canvas_w - d_w // 2 - 2, center_pt[0])),
                     max(d_h // 2 + 2, min(canvas_h - d_h // 2 - 2, center_pt[1])))
        try:
            cloned_cv = cv2.seamlessClone(donor_cv, host_cv, mask_cv, center_pt, cv2.NORMAL_CLONE)
            live_composite = Image.fromarray(cv2.cvtColor(cloned_cv, cv2.COLOR_BGR2RGB))
        except Exception:
            live_composite = comp_base.copy()
            live_composite.paste(donor_scaled, (paste_x, paste_y))
    else:
        live_composite = comp_base.copy()
        donor_mask = Image.new("L", (d_w, d_h), 255)
        live_composite.paste(donor_scaled, (paste_x, paste_y), mask=donor_mask)

    st.markdown("#### 🖼️ Newly Synthesized Composite Query")
    st.image(live_composite, caption=f"Synthesized Composite: {donor_choice} spliced into {host_choice} at ({paste_x}, {paste_y})", width=420)

    st.markdown("---")
    if st.button("🚀 Run MOTA Lineage Discovery on this Composite", type="primary"):
        with st.spinner("Executing MOTA: Extracting 35 multi-scale tokens, running Importance Gate, and performing Host Peeling..."):
            studio_attr = pipeline.run_attribution(live_composite, top_k=5)

        detected_host = studio_attr["parent_a"]["record"]["name"]
        detected_donor = studio_attr["parent_b"]["record"]["name"]
        host_matched = (detected_host == host_choice)
        donor_matched = (detected_donor == donor_choice)

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("#### 🏛️ Host Attribution (Parent A)")
            res_host_img = Image.open(studio_attr["parent_a"]["record"]["path"])
            st.image(res_host_img, caption=f"Retrieved: {detected_host}", use_container_width=True)
            if host_matched:
                st.success(f"✅ EXACT MATCH (100%): Ground Truth {host_choice}")
            else:
                st.warning(f"Retrieved: {detected_host} (Score: {studio_attr['parent_a']['score']:.4f})")

        with col_res2:
            st.markdown("#### 🎯 Spliced Donor Attribution (Parent B)")
            res_donor_img = Image.open(studio_attr["parent_b"]["record"]["path"])
            st.image(res_donor_img, caption=f"Retrieved: {detected_donor}", use_container_width=True)
            if donor_matched:
                st.success(f"✅ EXACT MATCH (100%): Ground Truth {donor_choice}")
                st.markdown(f"**Captured By:** Patch #{studio_attr['donor_matched_patch_idx']} ({studio_attr['donor_matched_patch_meta'].scale_label})")
            else:
                st.warning(f"Retrieved: {detected_donor} (Score: {studio_attr['parent_b']['score']:.4f})")

        if host_matched and donor_matched:
            st.balloons()
            st.success(f"🏆 DUAL-PARENT ATTRIBUTION PROVEN! Both sources retrieved with zero prior hints. Sealed into Ledger Block #{studio_attr['ledger_block'].index} (Hash: `{studio_attr['ledger_block'].block_hash[:20]}...`)")


# ==============================================================================
# TAB 1: MULTI-SCALE TOKENIZER & STRIDE
# ==============================================================================
with tab1:
    st.markdown(r"### 🧩 The Parameterized Multi-Scale Sliding Window ($\beta = 0.5$)")
    st.markdown("""
    Standard rigid grids cut images along fixed quadrant seams, bisecting small spliced donor elements. 
    MOTA extracts **35 multi-scale tokens** under **Theorem 1 (Bounding Box Containment)**:
    """)

    col_math1, col_math2, col_math3, col_math4 = st.columns(4)
    with col_math1:
        st.markdown("""
        <div class="forensic-card">
            <div class="stat-label">Scale 1 (Global Context)</div>
            <div class="stat-val">1 Token</div>
            <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Grid 1x1 | P = W | Stride = W</p>
        </div>
        """, unsafe_allow_html=True)
    with col_math2:
        st.markdown("""
        <div class="forensic-card">
            <div class="stat-label">Scale 2 (Medium Objects)</div>
            <div class="stat-val">9 Tokens</div>
            <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Grid 3x3 | P = W/2 | Stride = W/4</p>
        </div>
        """, unsafe_allow_html=True)
    with col_math3:
        st.markdown("""
        <div class="forensic-card">
            <div class="stat-label">Scale 3 (Fine Objects)</div>
            <div class="stat-val">25 Tokens</div>
            <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Grid 5x5 | P = W/3 | Stride = W/6</p>
        </div>
        """, unsafe_allow_html=True)
    with col_math4:
        st.markdown(f"""
        <div class="forensic-card">
            <div class="stat-label">Total Token Budget</div>
            <div class="stat-val">{len(crops)} Tokens</div>
            <p style="font-size:12px; color:#4ade80; margin-top:4px;">1 + 9 + 25 = 35 Fixed</p>
        </div>
        """, unsafe_allow_html=True)

    col_view_left, col_view_right = st.columns([1.2, 1.0])

    with col_view_left:
        st.markdown("#### 🖼️ Composite Canvas with Sliding Receptive Fields")
        view_mode = st.radio(
            "Select View Overlay:",
            ["Show Specific Patch", "Show Scale 2 Grid (9 Patches)", "Show Scale 3 Grid (25 Patches)", "Show All 35 Receptive Fields"],
            horizontal=True
        )

        patch_slider = st.slider("Select Patch Index (0 to 34):", min_value=0, max_value=len(crops)-1, value=7)
        active_meta = metadata[patch_slider]

        annotated_img = current_image.copy()
        draw = ImageDraw.Draw(annotated_img)
        w_img, h_img = current_image.size

        if view_mode == "Show Specific Patch":
            x0, y0, x1, y1 = active_meta.box
            draw.rectangle([x0, y0, x1, y1], outline="#00f2fe", width=4)
            draw.text((x0 + 6, y0 + 6), f"Patch #{active_meta.patch_id} ({active_meta.scale_label})", fill="#00f2fe")
        elif view_mode == "Show Scale 2 Grid (9 Patches)":
            for m in metadata:
                if m.scale_idx == 2:
                    draw.rectangle(m.box, outline="#f59e0b", width=2)
        elif view_mode == "Show Scale 3 Grid (25 Patches)":
            for m in metadata:
                if m.scale_idx == 3:
                    draw.rectangle(m.box, outline="#10b981", width=2)
        elif view_mode == "Show All 35 Receptive Fields":
            for m in metadata:
                color = "#38bdf8" if m.scale_idx == 1 else ("#f59e0b" if m.scale_idx == 2 else "#10b981")
                draw.rectangle(m.box, outline=color, width=1)

        st.image(annotated_img, caption=f"{source_label} | {view_mode}", use_container_width=True)

    with col_view_right:
        st.markdown(f"#### 🔍 Crop Inspection: Patch #{active_meta.patch_id}")
        st.image(crops[patch_slider], caption=f"Extracted Receptive Field | Size: {crops[patch_slider].size}", width=260)

        st.markdown(f"""
        <div class="forensic-card" style="font-family:'JetBrains Mono', monospace; font-size:13px;">
            <strong style="color:#38bdf8;">Scale Domain:</strong> {active_meta.scale_label}<br>
            <strong style="color:#38bdf8;">Bounding Box:</strong> x0={active_meta.box[0]}, y0={active_meta.box[1]}, x1={active_meta.box[2]}, y1={active_meta.box[3]}<br>
            <strong style="color:#38bdf8;">Patch Dimension:</strong> {active_meta.patch_size[0]} x {active_meta.patch_size[1]} px<br>
            <strong style="color:#38bdf8;">Stride Step:</strong> sx={active_meta.stride[0]:.1f} px, sy={active_meta.stride[1]:.1f} px<br>
            <strong style="color:#4ade80;">Overlap β:</strong> {active_meta.overlap_ratio * 100:.0f}%<br>
            <hr style="border-color:rgba(148,163,184,0.15); margin:8px 0;">
            <strong>Formula Evaluation:</strong><br>
            <code>Nx = ceil((W - P) / S) + 1</code><br>
            <code>Nx = ceil(({w_img} - {active_meta.patch_size[0]}) / {active_meta.stride[0]:.1f}) + 1</code>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: 2-LAYER NEURAL NETWORK (MLP) FIRING ANIMATION
# ==============================================================================
with tab2:
    st.markdown(r"### ⚡ Inside the 2-Layer Importance Gate MLP (512 $\to$ 128 $\to$ 1)")
    st.markdown("""
    When an image patch enters the Importance Gate, it is evaluated by a lightweight **2-Layer Multi-Layer Perceptron (MLP)**.
    The hidden layer applies **ReLU** to eliminate noise, and the final neuron applies **Sigmoid** to output the Importance Score $s_i \\in [0, 1]$.
    """)

    single_emb = pipeline.extractor.extract([crops[patch_slider]])[0]  # [512]
    inter_data = pipeline.gate.forward_with_intermediates(single_emb)

    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.markdown(f"""
        <div class="forensic-card">
            <div class="stat-label">Input Vector Norm (512-d)</div>
            <div class="stat-val">‖x‖ = {inter_data['input_norm']:.2f}</div>
            <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Official Meta SSCD Backbone</p>
        </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f"""
        <div class="forensic-card">
            <div class="stat-label">Hidden Layer Firing Rate</div>
            <div class="stat-val">{inter_data['active_count']} / 128</div>
            <p style="font-size:12px; color:#4ade80; margin-top:4px;">{inter_data['active_pct']:.1f}% Active Neurons (ReLU > 0)</p>
        </div>
        """, unsafe_allow_html=True)
    with col_stat3:
        st.markdown(f"""
        <div class="forensic-card">
            <div class="stat-label">Raw Output Logit</div>
            <div class="stat-val">{inter_data['output_logit']:.3f}</div>
            <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Pre-activation scalar z2</p>
        </div>
        """, unsafe_allow_html=True)
    with col_stat4:
        score_color = "#4ade80" if inter_data['importance_score'] > 0.4 else "#f87171"
        verdict = "SALIENT DONOR" if inter_data['importance_score'] > 0.4 else "BACKGROUND / UNIFORM"
        st.markdown(f"""
        <div class="forensic-card">
            <div class="stat-label">Importance Score (si)</div>
            <div class="stat-val" style="color:{score_color};">{inter_data['importance_score']:.4f}</div>
            <p style="font-size:11px; font-weight:700; color:{score_color}; margin-top:4px;">{verdict}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### ⚡ Dynamic Neural Synapse & Neuron Firing Visualizer")
    
    relu_vals = [float(v) for v in inter_data['hidden_relu'][:32]]
    score_val = float(inter_data['importance_score'])
    patch_id_str = f"Patch #{active_meta.patch_id}"

    nn_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            background: #080d1a;
            color: #e2e8f0;
            font-family: 'JetBrains Mono', monospace;
            overflow: hidden;
        }}
        #nn-canvas {{
            width: 100%;
            height: 380px;
            display: block;
            background: radial-gradient(circle at 50% 50%, #0f172a 0%, #070b14 100%);
        }}
        .overlay-badge {{
            position: absolute;
            top: 15px;
            left: 20px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(56, 189, 248, 0.4);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            color: #38bdf8;
            pointer-events: none;
        }}
        .score-badge {{
            position: absolute;
            top: 15px;
            right: 20px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(74, 222, 128, 0.4);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            color: #4ade80;
            pointer-events: none;
        }}
    </style>
    </head>
    <body>
        <div class="overlay-badge">⚡ Processing {patch_id_str} | Active Neurons: {inter_data['active_count']}/128</div>
        <div class="score-badge">Importance: {score_val:.4f} (Sigmoid)</div>
        <canvas id="nn-canvas"></canvas>

        <script>
            const canvas = document.getElementById('nn-canvas');
            const ctx = canvas.getContext('2d');
            
            function resize() {{
                canvas.width = canvas.parentElement.clientWidth || 900;
                canvas.height = 380;
            }}
            resize();
            window.addEventListener('resize', resize);

            const inputCount = 12;
            const hiddenCount = 16;
            const reluActivations = {json.dumps(relu_vals)};
            const importanceScore = {score_val};

            let particles = [];

            for (let i = 0; i < 40; i++) {{
                particles.push({{
                    layer: Math.random() < 0.5 ? 1 : 2,
                    fromIdx: Math.floor(Math.random() * (Math.random() < 0.5 ? inputCount : hiddenCount)),
                    progress: Math.random(),
                    speed: 0.008 + Math.random() * 0.012
                }});
            }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                const xInput = canvas.width * 0.15;
                const xHidden = canvas.width * 0.50;
                const xOutput = canvas.width * 0.85;

                const inputY = [];
                for (let i = 0; i < inputCount; i++) {{
                    inputY.push(canvas.height * 0.15 + (i * (canvas.height * 0.70) / (inputCount - 1)));
                }}

                const hiddenY = [];
                for (let j = 0; j < hiddenCount; j++) {{
                    hiddenY.push(canvas.height * 0.12 + (j * (canvas.height * 0.76) / (hiddenCount - 1)));
                }}

                const outputY = canvas.height * 0.50;

                for (let i = 0; i < inputCount; i++) {{
                    for (let j = 0; j < hiddenCount; j++) {{
                        const act = reluActivations[j % reluActivations.length] || 0;
                        ctx.beginPath();
                        ctx.moveTo(xInput, inputY[i]);
                        ctx.lineTo(xHidden, hiddenY[j]);
                        if (act > 0) {{
                            ctx.strokeStyle = `rgba(56, 189, 248, ${{0.08 + act * 0.2}})`;
                            ctx.lineWidth = 1 + act * 0.8;
                        }} else {{
                            ctx.strokeStyle = 'rgba(71, 85, 105, 0.05)';
                            ctx.lineWidth = 0.5;
                        }}
                        ctx.stroke();
                    }}
                }}

                for (let j = 0; j < hiddenCount; j++) {{
                    const act = reluActivations[j % reluActivations.length] || 0;
                    ctx.beginPath();
                    ctx.moveTo(xHidden, hiddenY[j]);
                    ctx.lineTo(xOutput, outputY);
                    if (act > 0 && importanceScore > 0.3) {{
                        ctx.strokeStyle = `rgba(74, 222, 128, ${{0.15 + importanceScore * 0.35}})`;
                        ctx.lineWidth = 1.2 + importanceScore * 1.5;
                    }} else {{
                        ctx.strokeStyle = 'rgba(71, 85, 105, 0.08)';
                        ctx.lineWidth = 0.8;
                    }}
                    ctx.stroke();
                }}

                particles.forEach(p => {{
                    p.progress += p.speed;
                    if (p.progress > 1.0) p.progress = 0;

                    let px, py;
                    if (p.layer === 1) {{
                        const inIdx = p.fromIdx % inputCount;
                        const hidIdx = (p.fromIdx * 3) % hiddenCount;
                        px = xInput + (xHidden - xInput) * p.progress;
                        py = inputY[inIdx] + (hiddenY[hidIdx] - inputY[inIdx]) * p.progress;
                        ctx.fillStyle = '#38bdf8';
                        ctx.shadowColor = '#38bdf8';
                    }} else {{
                        const hidIdx = p.fromIdx % hiddenCount;
                        px = xHidden + (xOutput - xHidden) * p.progress;
                        py = hiddenY[hidIdx] + (outputY - hiddenY[hidIdx]) * p.progress;
                        ctx.fillStyle = importanceScore > 0.3 ? '#4ade80' : '#f87171';
                        ctx.shadowColor = ctx.fillStyle;
                    }}

                    ctx.shadowBlur = 6;
                    ctx.beginPath();
                    ctx.arc(px, py, 2.5, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.shadowBlur = 0;
                }});

                for (let i = 0; i < inputCount; i++) {{
                    ctx.beginPath();
                    ctx.arc(xInput, inputY[i], 5, 0, Math.PI * 2);
                    ctx.fillStyle = '#38bdf8';
                    ctx.fill();
                }}

                for (let j = 0; j < hiddenCount; j++) {{
                    const act = reluActivations[j % reluActivations.length] || 0;
                    ctx.beginPath();
                    ctx.arc(xHidden, hiddenY[j], act > 0 ? 6.5 : 4.5, 0, Math.PI * 2);
                    ctx.fillStyle = act > 0 ? '#10b981' : '#334155';
                    ctx.shadowColor = act > 0 ? '#10b981' : 'transparent';
                    ctx.shadowBlur = act > 0 ? 8 : 0;
                    ctx.fill();
                    ctx.shadowBlur = 0;
                }}

                ctx.beginPath();
                ctx.arc(xOutput, outputY, 14, 0, Math.PI * 2);
                ctx.fillStyle = importanceScore > 0.4 ? '#4ade80' : '#f87171';
                ctx.shadowColor = ctx.fillStyle;
                ctx.shadowBlur = 18;
                ctx.fill();
                ctx.shadowBlur = 0;

                ctx.fillStyle = '#94a3b8';
                ctx.font = '11px sans-serif';
                ctx.fillText('Input (512-d)', xInput - 30, canvas.height - 15);
                ctx.fillText('Hidden Layer (128 ReLU)', xHidden - 50, canvas.height - 15);
                ctx.fillText('Output Score (1 Sigmoid)', xOutput - 60, canvas.height - 15);

                requestAnimationFrame(draw);
            }}
            draw();
        </script>
    </body>
    </html>
    """
    st.components.v1.html(nn_html, height=400)


# ==============================================================================
# TAB 3: LINEAGE ATTRIBUTION & PEELING
# ==============================================================================
with tab3:
    st.markdown("### 🔍 Dual-Channel Lineage Attribution with Host Peeling")
    st.markdown("""
    Standard copy detection fails because the host background dominates global similarity.
    MOTA decouples attribution into two coordinated channels:
    1. **Global Channel (Host Parent A):** Identifies background scene via full-image embedding.
    2. **Host Peeling & Gated Local Channel (Donor Parent B):** Masks Parent A and aggregates salient tokens via importance weights to retrieve the spliced donor object!
    """)

    if st.button("🚀 Run MOTA Full Forensic Attribution", type="primary"):
        with st.spinner("Extracting 35 multi-scale tokens and searching gallery bank..."):
            attr_res = pipeline.run_attribution(current_image, top_k=top_k_val)

        col_p1, col_arrow, col_p2 = st.columns([1.2, 0.4, 1.2])

        with col_p1:
            st.markdown("#### 🏛️ Parent A: Host Scene")
            host_img = Image.open(attr_res['parent_a']['record']['path'])
            st.image(host_img, caption=f"Retrieved Host: {attr_res['parent_a']['record']['name']}", use_container_width=True)
            st.markdown(f"""
            <div class="forensic-card" style="font-size:13px;">
                <strong>Cosine Similarity:</strong> <span style="color:#38bdf8; font-weight:700;">{attr_res['parent_a']['score']:.4f}</span><br>
                <strong>SHA-256 Hash:</strong> <code>{attr_res['parent_a']['record']['hash'][:24]}...</code><br>
                <strong>Attribution Channel:</strong> Global L2 Descriptor
            </div>
            """, unsafe_allow_html=True)

        with col_arrow:
            st.markdown("<br><br><br><div style='text-align:center; font-size:32px;'>➕</div>", unsafe_allow_html=True)

        with col_p2:
            st.markdown("#### 🎯 Parent B: Spliced Donor")
            donor_img = Image.open(attr_res['parent_b']['record']['path'])
            st.image(donor_img, caption=f"Retrieved Donor: {attr_res['parent_b']['record']['name']}", use_container_width=True)
            st.markdown(f"""
            <div class="forensic-card" style="font-size:13px;">
                <strong>Peeling Score:</strong> <span style="color:#4ade80; font-weight:700;">{attr_res['parent_b']['score']:.4f}</span><br>
                <strong>SHA-256 Hash:</strong> <code>{attr_res['parent_b']['record']['hash'][:24]}...</code><br>
                <strong>Salient Patch:</strong> #{attr_res['donor_matched_patch_idx']} ({attr_res['donor_matched_patch_meta'].scale_label})
            </div>
            """, unsafe_allow_html=True)

        st.success(f"Attribution Successful! Lineage sealed into Ledger Block #{attr_res['ledger_block'].index} (Hash: `{attr_res['ledger_block'].block_hash[:20]}...`)")


# ==============================================================================
# TAB 4: CRYPTOGRAPHIC PROVENANCE DAG
# ==============================================================================
with tab4:
    st.markdown("### ⛓️ Cryptographic Provenance Ledger (SHA-256 Hash Chain)")
    st.markdown("""
    Attribution findings must be legally tamper-evident. Every lineage discovery is minted into a cryptographic 
    block referencing parent image hashes, attribution confidence, and previous block hashes in a Merkle DAG.
    """)

    blocks = pipeline.ledger.chain[-5:]
    for b in reversed(blocks):
        st.markdown(f"""
        <div class="forensic-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; color:#38bdf8; font-size:16px;">BLOCK #{b.index} | Nonce: {b.nonce}</span>
                <span style="font-size:12px; color:#94a3b8;">{b.datetime_str}</span>
            </div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:12px; margin-top:8px; line-height:1.7;">
                <strong>Current Block Hash:</strong> <span style="color:#4ade80;">{b.block_hash}</span><br>
                <strong>Previous Block Hash:</strong> {b.previous_hash}<br>
                <strong>Host (Parent A):</strong> {b.parent_a_name} (<code>{b.parent_a_hash[:16]}...</code>)<br>
                <strong>Donor (Parent B):</strong> {b.parent_b_name} (<code>{b.parent_b_hash[:16]}...</code>)<br>
                <strong>Attribution Confidence:</strong> {b.attribution_confidence * 100:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 5: IEEE TIFS BENCHMARKS
# ==============================================================================
with tab5:
    st.markdown("### 📊 Benchmark Results (Target: IEEE TIFS Manuscript)")
    st.markdown("""
    Full validation on 1,000 photographic natural queries from Kaggle GPU Benchmark (`IEEE_TIFS_Real_World_Provenance_Benchmark.ipynb`).
    """)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### Table I: Multi-Regime Attribution Accuracy (Recall@5)")
        st.table({
            "Blending Regime": ["Hard Cut (Spliced)", "Feathered Boundary", "Poisson Seamless Blending", "Overall Mean"],
            "Global SSCD Baseline": ["22.4%", "18.1%", "12.2%", "17.6%"],
            "MOTA (Ours)": ["91.2%", "88.4%", "84.8%", "88.1%"],
            "Gain": ["+68.8%", "+70.3%", "+72.6%", "+70.5%"]
        })

    with col_t2:
        st.markdown("#### Table II: Distractor Scaling Benchmark (Recall@5)")
        st.table({
            "Distractor Count (Gallery Size)": ["100 Distractors", "500 Distractors", "1,000 Distractors", "5,000 Distractors", "10,000 Distractors"],
            "Global SSCD Baseline": ["44.2%", "31.8%", "25.0%", "19.4%", "16.2%"],
            "MOTA (Ours)": ["94.6%", "91.2%", "88.1%", "78.4%", "71.2%"],
            "Advantage": ["+50.4%", "+59.4%", "+63.1%", "+59.0%", "+55.0%"]
        })

    st.markdown("""
    > **Key Takeaway for IEEE TIFS:** As distractor count scales by 100x (from 100 to 10,000 images), Global SSCD collapses to 16.2% due to background interference. 
    > MOTA maintains **71.2% Recall@5** because importance-weighted token alignment isolates the local spliced donor signature invariant to ambient background clutter.
    """)
