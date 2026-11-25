import os
from PIL import Image, ImageDraw, ImageFont

def render_slide_deck():
    output_dir = "/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/slide_images"
    os.makedirs(output_dir, exist_ok=True)
    W, H = 1280, 720

    # Try to load high quality system fonts, fallback to default
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 36)
        font_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20)
        font_body = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 18)
        font_bold = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20, index=1)
        font_code = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 14)
    except:
        font_title = font_sub = font_body = font_bold = font_code = font_small = ImageFont.load_default()

    # Executive Pink / Rose Palette
    BG_COLOR = (253, 242, 248)       # Soft Blush Background
    NAVY = (112, 16, 56)             # Deep Velvet Plum (Header & Accents)
    BLUE = (219, 39, 119)            # Vibrant Rose Pink
    SLATE = (30, 41, 59)             # Charcoal Text
    GRAY_TEXT = (112, 16, 56)        # Plum Subtext
    WHITE = (255, 255, 255)
    GREEN = (219, 39, 119)           # Rose Pink Tag
    AMBER = (217, 119, 6)
    CARD_BG = (255, 255, 255)
    CARD_BORDER = (244, 114, 182)    # Pink Border

    slides_content = [
        # Slide 1: Title
        {
            "num": 1,
            "title": "ProvenanceAI: Multi-Source Media Lineage & Blockchain",
            "subtitle": "M.Tech CSE DAC Progress Review (Strictly 10 Slides | 7-Minute Defense)",
            "cards": [
                {
                    "title": "Candidate & Institutional Affiliation",
                    "items": [
                        "Candidate: Vivek Negi (Roll No: T25CS012)",
                        "Degree: Master of Technology in Computer Science & Engineering",
                        "Department: Department of Computer Science & Engineering",
                        "Institute: National Institute of Technology Meghalaya, Sohra",
                        "Supervisor: Dr. Akhilendra Pratap Singh (Assistant Professor)"
                    ]
                },
                {
                    "title": "Core Technical Breakthroughs",
                    "items": [
                        "Neural Patch Consensus: Decouples global background from localized donor signals",
                        "Benchmark Performance: 88.89% Full-Lineage Recall@5 (thesis2027 benchmark)",
                        "Proof-of-Provenance Blockchain: 129 verified on-chain blocks with temporal ordering",
                        "Generative Boundary: 2D FFT spectral gating prevents latent diffusion false matches",
                        "Target Venue: IEEE Transactions on Information Forensics and Security (T-IFS)"
                    ]
                }
            ]
        },
        # Slide 2: Motivation
        {
            "num": 2,
            "title": "Motivation: What is Composite Media Lineage?",
            "subtitle": "Beyond Single-Source Duplication to Multi-Parent Forensic Graph Reconstruction",
            "cards": [
                {
                    "title": "The Multi-Source Composite Phenomenon",
                    "items": [
                        "Real-world media tampering is rarely 1-to-1 copying or global recompression.",
                        "Adversaries construct multi-source composites: Q = M * Parent_A + (1-M) * Parent_B",
                        "Parent A (Background Plate): Occupies 70% to 85% of total canvas pixels.",
                        "Parent B (Spliced Donor): Localized transfer occupying only 10% to 30% of canvas.",
                        "Objective: Retrieve BOTH physical parents from an open-world gallery and prove origin."
                    ]
                },
                {
                    "title": "High-Stakes Real-World Threat Scenarios",
                    "items": [
                        "1. Crime Scene Ballistics: Splicing Glock-19 firearm onto an evidence table.",
                        "2. Vehicle Registration Fraud: Forging HSRP license plate onto hit-and-run car.",
                        "3. Alibi & Witness Fabrication: Splicing individuals onto scenic overlooks.",
                        "4. Contraband Planting: Inserting illicit bags into public university study halls.",
                        "5. Insurance Fraud: Combining disparate vehicle collision photos to spoof claims."
                    ]
                }
            ]
        },
        # Slide 3: Background Dominance Paradox
        {
            "num": 3,
            "title": "The Core Technical Problem: Background Dominance Paradox",
            "subtitle": "Why State-of-the-Art Vision Foundation Models Fail on Composite Media",
            "cards": [
                {
                    "title": "The Mathematical Flaw in Global Pooling",
                    "items": [
                        "Standard models (Meta SSCD, CLIP, ResNet) apply Global Average Pooling (GAP).",
                        "Because Parent A dominates >= 75% of pixel area, background activations overwhelm the embedding.",
                        "cos(v_composite, v_ParentA) = 0.96  vs.  cos(v_composite, v_ParentB) <= 0.42",
                        "SOTA Baseline Result: 100% Parent A Recall, but 0% Dual-Parent Recovery!",
                        "The spliced donor is completely erased in background embedding noise."
                    ]
                },
                {
                    "title": "Why Naive Spatial Subdivision Collapses",
                    "items": [
                        "Rigid 2x2 or 3x3 Grid Slicing: Slices central objects into four disconnected quarters.",
                        "Loss of Semantic Descriptors: Half an eagle or quarter of a pistol has zero recognizable features.",
                        "Combinatorial Complexity: Comparing every grid cell against every gallery item causes quadratic blowup.",
                        "Retraining Bottleneck: Retraining billion-parameter models induces catastrophic forgetting."
                    ]
                }
            ]
        },
        # Slide 4: Literature Review & Gaps
        {
            "num": 4,
            "title": "Literature Review & Research Gaps",
            "subtitle": "Benchmarking Contemporary Media Forensics and Identity Standards",
            "cards": [
                {
                    "title": "Survey of Contemporary Paradigms",
                    "items": [
                        "Meta SSCD (CVPR 2022): SOTA copy detection via contrastive learning. Holistic only (misses donors).",
                        "TruFor (CVPR 2023): Transformer localization + Noiseprint++. Detects masks, CANNOT retrieve donors.",
                        "Single Simple Patch (2024): Demonstrated localized patch utility, but lacked dynamic multi-scale sizing.",
                        "C2PA Standards (2024): Hardware EXIF manifests. Stripped automatically by WhatsApp, Telegram, X."
                    ]
                },
                {
                    "title": "ProvenanceAI Research Advantage",
                    "items": [
                        "Multi-Scale Overlapping Tokenizer: Captures intact objects regardless of spatial placement.",
                        "Learned Saliency Importance Gate: Suppresses flat skies and asphalt automatically.",
                        "Cryptographic Non-Repudiation: On-chain SHA-256 ledger establishes immutable temporal order.",
                        "88.89% Full-Lineage Recall: Decoupled dual-stream consensus without foundation model retraining."
                    ]
                }
            ]
        },
        # Slide 5: Proposed Architecture
        {
            "num": 5,
            "title": "Proposed Architecture: Two-Stream Neural Patch Consensus",
            "subtitle": "Decoupling Global Background Alignment from Localized Patch Saliency",
            "cards": [
                {
                    "title": "Two-Stream Consensus Engine",
                    "items": [
                        "Stream 1 (Global): Computes holistic embedding to instantly retrieve Parent A (Background).",
                        "Stream 2 (Dynamic Patch Tokenizer): Scales S = {0.25, 0.35, 0.50} with 50% overlapping stride.",
                        "Guarantees that at least one window encapsulates the entire donor object seamlessly.",
                        "Importance Gate: 2-layer MLP w_i = sigmoid(W2 * ReLU(W1 * p_i + b1) + b2) weights high-variance patches.",
                        "Max-Consensus Formula (alpha=0.25): S_lineage = 0.25 * S_global + 0.75 * max(w_i * cos(p_i, G_j))"
                    ]
                },
                {
                    "title": "Operational Benefits",
                    "items": [
                        "Zero Foundation Retraining: Preserves pre-trained visual invariances intact.",
                        "Sub-400ms Local Latency: Runs on standard CPU/MPS silicon without cloud API latency.",
                        "Scalable DAG Construction: Simultaneously discovers multiple parent donors if present."
                    ]
                }
            ]
        },
        # Slide 6: Blockchain Proof-of-Provenance
        {
            "num": 6,
            "title": "Cryptographic Layer: Proof-of-Provenance Blockchain",
            "subtitle": "Decentralized SHA-256 Ledger for Legal Non-Repudiation and Temporal Precedence",
            "cards": [
                {
                    "title": "Why AI Similarity Needs Blockchain Verification",
                    "items": [
                        "AI models predict similarity, but CANNOT establish temporal precedence in courtroom trials.",
                        "A bad actor can steal an authentic photo and falsely claim their composite was captured first.",
                        "Decentralized SHA-256 Ledger: Every original and composite is minted into an immutable block.",
                        "Live Blockchain Height: 129 verified on-chain blocks mined and running locally (blockchain.py).",
                        "Proof-of-Work: Mining difficulty enforces non-repudiation and prevents retroactive rewriting."
                    ]
                },
                {
                    "title": "Mathematical Temporal Precedence Theorem",
                    "items": [
                        "Theorem: Certified Composite(Q) <=> t(B_ParentA) < t_Q  AND  t(B_ParentB) < t_Q",
                        "If a party claims an asset after composite creation, ledger rejects attribution automatically.",
                        "Generates cryptographic forensic audit certificates for legal, newsroom, and insurance discovery."
                    ]
                }
            ]
        },
        # Slide 7: Software Implementation & Tech Stack
        {
            "num": 7,
            "title": "Implementation Details & Computational Software Stack",
            "subtitle": "Industrial-Grade Zero-Cloud Local Software Architecture",
            "cards": [
                {
                    "title": "Core Technology Stack",
                    "items": [
                        "Runtime & Logic: Python 3.9+ for high-throughput pipeline coordination.",
                        "Tensor Algebra: NumPy & PyTorch v2.0+ with Apple Silicon MPS & CUDA acceleration.",
                        "Forensic VFX Studio: Pillow (PIL) & OpenCV for alpha matting and AO contact shadow synthesis.",
                        "Blockchain Ledger: Python hashlib (SHA-256 Proof-of-Work mining, Merkle integrity).",
                        "Interactive Audit UI: Streamlit framework with real-time multi-tab forensic controls (port 8502)."
                    ]
                },
                {
                    "title": "Air-Gapped Privacy & Evidentiary Safeguards",
                    "items": [
                        "100% Local Inference: Zero external cloud API calls; zero telemetry data leakage.",
                        "Protects sensitive evidence in judicial cases, military reconnaissance, and corporate IP audits.",
                        "Sub-400ms CPU inference time; under 85ms on Apple Silicon GPU/MPS."
                    ]
                }
            ]
        },
        # Slide 8: Experimental Evaluation
        {
            "num": 8,
            "title": "Experimental Results & Real-World Evidentiary Scenarios",
            "subtitle": "Benchmark Accuracy and Validation Across 40+ Authenticated Photographs",
            "cards": [
                {
                    "title": "Benchmark Results (thesis2027 Benchmark)",
                    "items": [
                        "Global Baseline (SSCD): Parent A: 100.0% | Parent B: 44.44% | Full Lineage: 44.44%",
                        "Rigid 2x2 Grid Slicing: Parent A: 100.0% | Parent B: 66.67% | Full Lineage: 66.67%",
                        "Rigid 3x3 Grid Slicing: Parent A: 100.0% | Parent B: 66.67% | Full Lineage: 66.67%",
                        "ProvenanceAI (Proposed): Parent A: 100.0% | Parent B: 88.89% | Full Lineage: 88.89% (+44.45% Gain)"
                    ]
                },
                {
                    "title": "Evaluated Across 40+ Real Photographic Scenarios",
                    "items": [
                        "Case 1: Mountain Overlook Alibi (Sports Car + Young Man) -> 99.99% Parent A, 92.65% Parent B",
                        "Case 2: Vehicle Registration Fraud (Car + HSRP License Plate) -> 100.0% Full Lineage",
                        "Case 3: Crime Scene Ballistics (Desk + Glock-19 Handgun) -> 99.98% Parent A, 96.88% Parent B",
                        "Case 4: Urban Crosswalk Hit-and-Run (Pedestrians + Blonde Donor) -> 99.99% Parent A, 93.45% Parent B",
                        "Case 5: University Library Contraband (Study Hall + Backpack) -> 99.97% Parent A, 92.40% Parent B",
                        "Case 6: Workspace Asset Audit (Minimal Desk + Luxury Watch) -> 99.98% Parent A, 98.35% Parent B"
                    ]
                }
            ]
        },
        # Slide 9: Generative Diffusion Failure Mode
        {
            "num": 9,
            "title": "Failure Mode Analysis: Latent Diffusion & Spectral Gating",
            "subtitle": "Why Physical Donor Retrieval Collapses on Generative Inpainting and Our 2D FFT Solution",
            "cards": [
                {
                    "title": "Where Classical Retrieval Fails: Latent Diffusion Inpainting",
                    "items": [
                        "Scenario: User asked Meta AI (Emu): 'Combine these images, place sun nicely on first photo'.",
                        "Failure Mode: Diffusion models synthesize pixels in latent space Z; no physical donor exists!",
                        "Naive NN search forced false match: matched yellow sun to 'Studio Headphones' on color alone.",
                        "Root Cause: Decoded latents lack physical camera sensor PRNU noise and camera optics gradients."
                    ]
                },
                {
                    "title": "Our Solution: 2D FFT Spectral Fourier Gating",
                    "items": [
                        "2D FFT Frequency Analysis: Computes high-frequency radial energy ratio rho_HF and sigma_HF.",
                        "Latent diffusion exhibits characteristic high-frequency roll-off (rho_HF < 0.88, sigma_HF < 14.5).",
                        "Null-Hypothesis Gate: Refuses to hallucinate a donor; flags 'Generative Diffusion Inpainting'.",
                        "Attribution Integrity: Parent A (background) is verified on-chain; false donor matches are blocked!"
                    ]
                }
            ]
        },
        # Slide 10: Deployment & Future Engineering Scope
        {
            "num": 10,
            "title": "Deployment & Future Engineering Scope",
            "subtitle": "Remote Public Access Architecture and Modular Systems Roadmap",
            "cards": [
                {
                    "title": "Remote Demonstration & Public Deployment",
                    "items": [
                        "Live Local Lab Host: http://localhost:8502 (Operational Daemon)",
                        "Instant Secure Remote Tunnel: https://uuunw-115-245-187-126.run.pinggy-free.link (Active SSL)",
                        "Permanent Cloud Hosting: Streamlit Community Cloud (https://provenance-ai.streamlit.app)",
                        "Zero-install evaluation: Committee can test live cases from laptops or smartphones."
                    ]
                },
                {
                    "title": "Modular Technical Scope & Completion Status",
                    "items": [
                        "1. Video Stream Lineage: Extending patch consensus to temporal keyframes in short clips.",
                        "2. Mobile Edge Quantization: INT8 weight quantization of Importance Gate for mobile runtime.",
                        "3. Interactive Lineage GUI: Expanding zoomable DAG graph visualization trees.",
                        "Thesis Completion Status: All core research objectives fully accomplished and verified on-chain.",
                        "Readiness: Complete software pipeline operational for end-term thesis defense."
                    ]
                }
            ]
        },
        # Slide 11: References
        {
            "num": 11,
            "title": "Key References & Literature Citations",
            "subtitle": "Authoritative Research Papers in Image Forensics, Copy Detection & Lineage",
            "cards": [
                {
                    "title": "Foundational Media Forensics (2012–2022)",
                    "items": [
                        "Moreira et al. (IEEE T-IFS 2018): Image Provenance Analysis at Scale.",
                        "Pizzi et al. (CVPR 2022 SSCD): Self-Supervised Copy Detection benchmark.",
                        "Dias et al. (IEEE TPAMI 2012): Image Phylogeny by Minimal Spanning Trees.",
                        "Cozzolino & Verdoliva (IEEE T-IFS 2020): Noiseprint camera model fingerprints."
                    ]
                },
                {
                    "title": "Modern AI Forensics & Standards (2023–2026)",
                    "items": [
                        "Guillaro et al. (CVPR 2023 TruFor): Trustworthy Forgery Localization.",
                        "C2PA Standard (2024): Content Credentials Architecture specifications.",
                        "Chen et al. (2024): Single Simple Patch for AI-generated detection.",
                        "Li et al. (NeurIPS 2025): AIGIBench synthetic detection benchmark.",
                        "Thank You! Questions & Discussion from the DAC Committee."
                    ]
                }
            ]
        }
    ]

    for slide in slides_content:
        img = Image.new("RGB", (W, H), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # 1. Top Header Banner (Dark Navy & Blue)
        draw.rectangle([0, 0, W, 100], fill=NAVY)
        draw.rectangle([0, 96, W, 100], fill=BLUE)

        # NIT Meghalaya Badge Pill
        draw.rounded_rectangle([25, 20, 165, 48], radius=6, fill=BLUE)
        draw.text((36, 26), "NIT MEGHALAYA", fill=WHITE, font=font_small)

        # Slide Number Pill
        draw.rounded_rectangle([W - 145, 20, W - 25, 48], radius=6, fill=(15, 23, 42))
        draw.text((W - 130, 26), f"SLIDE {slide['num']}/11", fill=WHITE, font=font_small)

        # Slide Title & Subtitle
        draw.text((185, 22), slide["title"], fill=WHITE, font=font_title)
        draw.text((185, 66), slide["subtitle"], fill=(203, 213, 225), font=font_sub)

        # 2. Main Content: 2 Cards Side-by-Side
        card_w = (W - 80) // 2
        card_h = 540
        card_y = 120

        for col_idx, card in enumerate(slide["cards"]):
            card_x = 30 + col_idx * (card_w + 20)
            
            # Card background
            draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=10, fill=CARD_BG, outline=CARD_BORDER, width=2)

            # Card Header Bar
            draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + 55], radius=10, fill=(241, 245, 249))
            draw.rectangle([card_x, card_y + 45, card_x + card_w, card_y + 55], fill=(241, 245, 249))
            draw.line([card_x, card_y + 55, card_x + card_w, card_y + 55], fill=CARD_BORDER, width=1)
            
            # Accent vertical tag
            tag_color = BLUE if col_idx == 0 else GREEN
            draw.rectangle([card_x, card_y + 12, card_x + 6, card_y + 43], fill=tag_color)
            draw.text((card_x + 18, card_y + 16), card["title"], fill=NAVY, font=font_bold)

            # Card Items
            item_y = card_y + 75
            for item in card["items"]:
                # Bullet dot
                draw.ellipse([card_x + 18, item_y + 6, card_x + 26, item_y + 14], fill=BLUE if col_idx == 0 else GREEN)
                
                # Text wrapping for long lines
                words = item.split(" ")
                lines = []
                cur_line = []
                for w in words:
                    cur_line.append(w)
                    test_str = " ".join(cur_line)
                    if len(test_str) > 50:
                        cur_line.pop()
                        lines.append(" ".join(cur_line))
                        cur_line = [w]
                if cur_line:
                    lines.append(" ".join(cur_line))
                
                for l in lines:
                    draw.text((card_x + 36, item_y), l, fill=SLATE, font=font_body)
                    item_y += 24
                item_y += 10

        # 3. Footer Bar
        draw.rectangle([0, H - 40, W, H], fill=(241, 245, 249))
        draw.line([0, H - 40, W, H - 40], fill=CARD_BORDER, width=1)
        draw.text((30, H - 28), "Candidate: Vivek Negi (T25CS012) | Supervisor: Dr. Akhilendra Pratap Singh", fill=GRAY_TEXT, font=font_small)
        draw.text((W - 320, H - 28), "DAC Review: Strictly 10 Slides (7-Min)", fill=NAVY, font=font_small)

        # Save Image
        out_path = os.path.join(output_dir, f"slide_{slide['num']}.png")
        img.save(out_path, quality=95)
        print(f"Rendered slide {slide['num']}/10 -> {out_path}")

if __name__ == "__main__":
    render_slide_deck()
