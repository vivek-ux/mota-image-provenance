---
title: MOTA Multi-Source Media Lineage Attribution
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.67.0"
app_file: app.py
pinned: false
license: apache-2.0
---

# 🛡️ MOTA: Multi-Scale Overlapping Token Alignment with Learned Importance Gating

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.67.0-ff4b4b.svg)](https://streamlit.io/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Target: IEEE TIFS](https://img.shields.io/badge/Target-IEEE_TIFS-purple.svg)](https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security)

**Department of Computer Science & Engineering**  
**National Institute of Technology Meghalaya (NIT Meghalaya)**  
**Author:** Vivek Negi (Roll No: `T25CS012`)  
**Supervisor:** Dr. Akhilendra Pratap Singh  
**Target Publication:** *IEEE Transactions on Information Forensics and Security (IEEE TIFS)*

---

## 📌 Executive Summary & Novelty

Modern reverse image search systems (e.g., Google Lens, Meta SSCD global) compress an entire image into a **single global feature vector**. When presented with a **multi-source composite** (e.g., a foreign donor object spliced onto a dominant host background), the global embedding is overwhelmed by the host scene, causing donor retrieval recall to collapse to **16.2%**.

Conversely, patch-based forensic forgery localization models only output binary heatmaps showing *where* manipulation occurred, but **cannot attribute ancestral lineage** back to original database source images.

**MOTA (Multi-Scale Overlapping Token Alignment)** resolves both bottlenecks:
1. **Parameterized Multi-Scale Tokenizer ($\beta = 0.5$):** Formulates sliding receptive fields across 3 scales ($1 + 9 + 25 = 35$ fixed tokens) with a 50% overlap stride ($S_{k,x} = \frac{W}{2g_{k,x}}$). Under **Theorem 1 (Bounding Box Containment)**, this mathematically guarantees that any spliced donor element up to the stride dimension is captured intact without spatial fracture.
2. **2-Layer Importance Gate MLP ($512 \to 128 \to 1$):** A compact neural gating mechanism ($65,793$ parameters) with **LayerNorm**, **ReLU**, and **Sigmoid** activation. It dynamically evaluates the 35 tokens and scores spliced donor regions ($s_i \approx 0.94$) while suppressing uniform background clutter ($s_i \approx 0.08$).
3. **Decoupled Peeling Attribution & Cryptographic Ledger:** Decouples global host identification from gated local donor retrieval via host peeling, and mints every attribution discovery into an immutable **SHA-256 Merkle DAG ledger**.

---

## 🔬 Mathematical Formulations

### 1. Parameterized Stride Equation
For an image of dimension $W \times H$, scale divisor $g_k \in \{1, 2, 3\}$, and overlap ratio $\beta = 0.5$:
$$P_{k,x} = \frac{W}{g_{k,x}}, \quad S_{k,x} = P_{k,x} \cdot (1 - \beta) = \frac{W}{2g_{k,x}}$$

The number of patches along each axis is:
$$N_x = \left\lceil \frac{W - P_{k,x}}{S_{k,x}} \right\rceil + 1$$

* **Scale 1 ($g_1 = 1$):** $P_1 = W, S_1 = W \implies 1 \times 1 = \mathbf{1 \text{ Token}}$ (Global Scene Context)
* **Scale 2 ($g_2 = 2$):** $P_2 = W/2, S_2 = W/4 \implies 3 \times 3 = \mathbf{9 \text{ Tokens}}$ (Medium Objects / Context)
* **Scale 3 ($g_3 = 3$):** $P_3 = W/3, S_3 = W/6 \implies 5 \times 5 = \mathbf{25 \text{ Tokens}}$ (Fine Objects / Details)
* **Total Token Budget:** $1 + 9 + 25 = \mathbf{35 \text{ Tokens}}$

### 2. Theorem 1 (Bounding Box Containment)
$$\text{Let } \mathcal{B} = [x_{\min}, y_{\min}, x_{\max}, y_{\max}] \text{ be a spliced bounding box with width } w \le S_{k,x} \text{ and height } h \le S_{k,y}.$$
$$\exists j \in \{1, \dots, N_k\} \quad \text{such that} \quad \mathcal{B} \subseteq \Omega_j$$
*Proof:* Because consecutive window origins advance by exactly $S_k$, and window width $P_k = 2S_k$, any bounding box spanning $\le S_k$ cannot simultaneously intersect both window margins without being wholly enclosed by at least one overlapping receptive field $\Omega_j$. $\blacksquare$

---

## ⚡ 2-Layer Importance Gate Architecture

```
Patch Embedding (512-d)
         │
         ▼
┌─────────────────────────────────┐
│ Linear Layer (512 -> 128)       │
│ LayerNorm (128)                 │
│ ReLU Activation [max(0, x)]     │
│ Dropout (0.1)                   │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Linear Layer (128 -> 1)         │
│ Sigmoid Activation [σ(z)]       │
└─────────────────────────────────┘
         │
         ▼
Importance Weight si ∈ [0.0, 1.0]
```

---

## 📊 Experimental Results (IEEE TIFS Validation)

### Table I: Attribution Accuracy across Blending Regimes (Recall@5)
| Blending Regime | Global SSCD Baseline | MOTA (Ours) | Absolute Gain |
| :--- | :---: | :---: | :---: |
| **Hard Cut (Raw Splice)** | 22.4% | **91.2%** | **+68.8%** |
| **Feathered Boundary** | 18.1% | **88.4%** | **+70.3%** |
| **Poisson Seamless Blending** | 12.2% | **84.8%** | **+72.6%** |
| **Overall Mean** | 17.6% | **88.1%** | **+70.5%** |

### Table II: Distractor Scaling Benchmark (Recall@5)
| Distractor Scale | Global SSCD Baseline | MOTA (Ours) | Advantage |
| :--- | :---: | :---: | :---: |
| **100 Distractors** | 44.2% | **94.6%** | +50.4% |
| **500 Distractors** | 31.8% | **91.2%** | +59.4% |
| **1,000 Distractors** | 25.0% | **88.1%** | +63.1% |
| **5,000 Distractors** | 19.4% | **78.4%** | +59.0% |
| **10,000 Distractors** | 16.2% | **71.2%** | **+55.0%** |

---

## 💻 Running the Interactive Dashboard Locally

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/vivek-ux/mota-image-provenance.git
cd mota-image-provenance

# Using uv (recommended) or standard venv:
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Launch the Streamlit App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Free Cloud Deployment Guide

### Option A: 1-Click Streamlit Community Cloud (Free Forever)
1. Push this repository to your GitHub account (`vivek-ux/mota-image-provenance`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New App**, select repository `vivek-ux/mota-image-provenance`, branch `main`, and main file path `app.py`.
4. Click **Deploy!** Your app will be live at `https://mota-image-provenance.streamlit.app`.

### Option B: Hugging Face Spaces (Free CPU 24/7)
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **Create new Space**.
2. Space Name: `mota-image-provenance`.
3. Space SDK: **Streamlit**.
4. Hardware: **Free (2 vCPU, 16 GB RAM)**.
5. Push this repository to the Hugging Face Space git remote or link your GitHub repository. Hugging Face reads the YAML metadata in this `README.md` and starts the app automatically!

---

## 📁 Repository Structure
```
├── app.py                                           # Streamlit Interactive Forensic Dashboard
├── mota_engine.py                                   # Core PyTorch Engine (Tokenizer, MLP, Peeling, Ledger)
├── requirements.txt                                 # Production Python Dependencies
├── IEEE_TIFS_Real_World_Provenance_Benchmark.ipynb  # Complete 22-Cell Kaggle Master Benchmark Notebook
├── tifs_manuscript.tex                              # IEEEtran Journal LaTeX Manuscript
├── provenance.bib                                   # BibTeX References
├── gallery/                                         # Photographic Gallery Dataset for Attribution
├── car_man_composite.jpg                           # Sample Composite 1 (Car + Man)
├── crime_scene_handgun_composite.png                # Sample Composite 2 (Crime Scene + Handgun)
├── crosswalk_blonde_composite.png                   # Sample Composite 3 (Crosswalk + Blonde Woman)
└── library_backpack_composite.png                   # Sample Composite 4 (Library + Backpack)
```

---

## 📜 Citation & Academic Credit
If you find this work or codebase helpful in your research, please cite:
```bibtex
@article{negi2027mota,
  author    = {Vivek Negi and Akhilendra Pratap Singh},
  title     = {Multi-Source Composite Media Lineage Attribution via Dynamic Token Alignment and Importance Gating},
  journal   = {IEEE Transactions on Information Forensics and Security},
  year      = {2027},
  note      = {Under Review}
}
```
