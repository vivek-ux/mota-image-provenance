"""
MOTA Engine: Multi-Scale Overlapping Token Alignment with Learned Importance Gating
Department of Computer Science & Engineering, National Institute of Technology Meghalaya
Author: Vivek Negi (T25CS012) | Supervisor: Dr. Akhilendra Pratap Singh
Target: IEEE Transactions on Information Forensics and Security (IEEE TIFS)

Exact PyTorch implementation replicating:
- Parameterized Stride Equation with beta = 0.5 (Scale 1: 1, Scale 2: 9, Scale 3: 25 -> 35 Tokens)
- Official Meta SSCD TorchScript feature extractor (512-d L2 normalized)
- 2-Layer Importance Gate MLP (512 -> 128 -> 1) with LayerNorm, ReLU, and Sigmoid
- Host Peeling & Donor Attribution Pipeline (Max-Sim Token Alignment)
- SHA-256 Cryptographic Provenance Ledger
"""

import math
import hashlib
import json
import time
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision.models as models

# Device selection: MPS (Apple Silicon), CUDA (NVIDIA), or CPU
if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")


# ==============================================================================
# 1. PARAMETERIZED MULTI-SCALE TOKENIZER (Theorem 1: Bounding Box Containment)
# ==============================================================================
@dataclass
class PatchMetadata:
    patch_id: int
    scale_idx: int
    scale_label: str
    grid_div: Tuple[int, int]
    box: Tuple[int, int, int, int]  # (x0, y0, x1, y1)
    patch_size: Tuple[int, int]     # (pw, ph)
    stride: Tuple[float, float]     # (sx, sy)
    overlap_ratio: float


class DynamicMultiScaleTokenizer:
    """
    Extracts multi-scale overlapping spatial patches under parameterized stride:
    S_{k,x} = (W / (2 * g_{k,x}))
    Scale 1 (g=1): 1 global view
    Scale 2 (g=2): 3x3 = 9 overlapping views (stride W/4)
    Scale 3 (g=3): 5x5 = 25 overlapping views (stride W/6)
    Total: 1 + 9 + 25 = 35 tokens.
    """
    def __init__(self, scales=[(1, 1), (2, 2), (3, 3)], overlap_ratio=0.5):
        self.scales = scales
        self.overlap = overlap_ratio

    def tokenize(self, pil_img: Image.Image) -> Tuple[List[Image.Image], List[PatchMetadata]]:
        w, h = pil_img.size
        crops = []
        metadata = []
        patch_counter = 0

        for k, (gx, gy) in enumerate(self.scales, start=1):
            if gx == 1 and gy == 1:
                # Scale 1: Whole Image Context (Global Token)
                crops.append(pil_img)
                meta = PatchMetadata(
                    patch_id=patch_counter,
                    scale_idx=1,
                    scale_label="Scale 1 (Global Context)",
                    grid_div=(1, 1),
                    box=(0, 0, w, h),
                    patch_size=(w, h),
                    stride=(w, h),
                    overlap_ratio=0.0
                )
                metadata.append(meta)
                patch_counter += 1
                continue

            pw = w / float(gx)
            ph = h / float(gy)
            stride_x = pw * (1.0 - self.overlap)
            stride_y = ph * (1.0 - self.overlap)
            nx = int(math.ceil((w - pw) / stride_x)) + 1
            ny = int(math.ceil((h - ph) / stride_y)) + 1

            scale_label = f"Scale {k} ({nx}x{ny} Grid, g={gx})"

            for iy in range(ny):
                for ix in range(nx):
                    x0 = min(ix * stride_x, w - pw)
                    y0 = min(iy * stride_y, h - ph)
                    x1 = x0 + pw
                    y1 = y0 + ph
                    box = (int(x0), int(y0), int(x1), int(y1))
                    cropped = pil_img.crop(box)
                    crops.append(cropped)

                    meta = PatchMetadata(
                        patch_id=patch_counter,
                        scale_idx=k,
                        scale_label=scale_label,
                        grid_div=(gx, gy),
                        box=box,
                        patch_size=(int(pw), int(ph)),
                        stride=(stride_x, stride_y),
                        overlap_ratio=self.overlap
                    )
                    metadata.append(meta)
                    patch_counter += 1

        return crops, metadata


# ==============================================================================
# 2. 2-LAYER IMPORTANCE GATE MLP (Universal Approximation)
# ==============================================================================
class ImportanceGate(nn.Module):
    """
    Exact 2-Layer MLP Importance Gate from Kaggle Benchmark:
    - Layer 1: Linear(512, 128) -> LayerNorm(128) -> ReLU() -> Dropout(0.1)
    - Layer 2: Linear(128, 1) -> Sigmoid / Softmax
    Capacity: 65,793 parameters.
    """
    def __init__(self, in_dim=512, hidden_dim=128):
        super().__init__()
        self.fc1 = nn.Linear(in_dim, hidden_dim)
        self.ln = nn.LayerNorm(hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.1)
        self.fc2 = nn.Linear(hidden_dim, 1)

        self._init_weights()

    def _init_weights(self):
        nn.init.kaiming_normal_(self.fc1.weight, nonlinearity='relu')
        nn.init.zeros_(self.fc1.bias)
        nn.init.xavier_normal_(self.fc2.weight)
        nn.init.zeros_(self.fc2.bias)

    def forward(self, patch_embs: torch.Tensor) -> torch.Tensor:
        """
        patch_embs: [Batch, T, 512] or [T, 512]
        returns normalized attention weights across patches
        """
        is_2d = (patch_embs.dim() == 2)
        if is_2d:
            patch_embs = patch_embs.unsqueeze(0)  # [1, T, 512]

        x = self.fc1(patch_embs)
        x = self.ln(x)
        x = self.relu(x)
        x = self.dropout(x)
        logits = self.fc2(x).squeeze(-1)  # [Batch, T]
        weights = F.softmax(logits, dim=-1)

        if is_2d:
            weights = weights.squeeze(0)
        return weights

    def forward_with_intermediates(self, patch_emb: torch.Tensor) -> Dict:
        """
        Runs a single 512-dim patch embedding and extracts all intermediate
        layer activations for live visualization of the neural network.
        """
        self.eval()
        with torch.no_grad():
            if patch_emb.dim() == 1:
                patch_emb = patch_emb.unsqueeze(0)  # [1, 512]

            # Layer 1
            z1 = self.fc1(patch_emb)               # [1, 128] linear sum
            z1_norm = self.ln(z1)                   # [1, 128] normalized
            a1 = self.relu(z1_norm)                 # [1, 128] ReLU activations (>= 0)

            # Layer 2
            z2 = self.fc2(a1).squeeze(-1)           # [1] raw logit
            score_sigmoid = torch.sigmoid(z2).item() # [0, 1] importance score

            # Active neuron statistics
            a1_np = a1.squeeze(0).cpu().numpy()
            active_count = int(np.sum(a1_np > 0))
            active_pct = (active_count / len(a1_np)) * 100.0

            return {
                "input_norm": float(torch.norm(patch_emb).item()),
                "hidden_z1": z1_norm.squeeze(0).cpu().numpy(),
                "hidden_relu": a1_np,
                "active_count": active_count,
                "active_pct": active_pct,
                "output_logit": float(z2.item()),
                "importance_score": float(score_sigmoid)
            }


# ==============================================================================
# 3. FEATURE EXTRACTOR (Meta SSCD Official / ResNet50 Fallback)
# ==============================================================================
class FeatureExtractor:
    """
    Generates 512-dimensional L2-normalized feature vectors.
    Uses official Meta SSCD TorchScript if available, otherwise ResNet50.
    """
    def __init__(self, weights_path: Optional[str] = None):
        self.device = DEVICE
        self.model = None
        self.is_sscd = False

        # Check default paths for sscd_disc_mixup.torchscript.pt
        if weights_path is None:
            script_dir = os.path.dirname(__file__)
            cand1 = os.path.join(script_dir, "sscd_disc_mixup.torchscript.pt")
            cand2 = "sscd_disc_mixup.torchscript.pt"
            if os.path.exists(cand1):
                weights_path = cand1
            elif os.path.exists(cand2):
                weights_path = cand2
            else:
                # Auto-download official Meta SSCD if missing
                try:
                    import urllib.request
                    target_dest = cand1
                    url = "https://dl.fbaipublicfiles.com/sscd-copy-detection/sscd_disc_mixup.torchscript.pt"
                    print(f"[MOTA Engine] Downloading official Meta SSCD from {url}...")
                    urllib.request.urlretrieve(url, target_dest)
                    weights_path = target_dest
                except Exception as dl_err:
                    print(f"[MOTA Engine] Auto-download failed: {dl_err}")

        if weights_path and os.path.exists(weights_path):
            try:
                self.model = torch.jit.load(weights_path, map_location=self.device)
                self.model.eval()
                self.is_sscd = True
                self.transform = transforms.Compose([
                    transforms.Resize((288, 288)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])
                ])
                print(f"[MOTA Engine] Active: Official Meta SSCD ({weights_path}) on {self.device}")
            except Exception as e:
                print(f"[MOTA Engine] Failed loading SSCD: {e}, falling back to ResNet50")

        if self.model is None:
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
            ])
            resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
            modules = list(resnet.children())[:-1]
            self.backbone = nn.Sequential(*modules).to(self.device)
            self.projector = nn.Linear(2048, 512).to(self.device)
            self.backbone.eval()
            self.projector.eval()
            print("[MOTA Engine] Active: ResNet50 Fallback (512-d L2 Normalized)")

    def extract(self, pil_imgs: List[Image.Image]) -> torch.Tensor:
        """
        Extracts 512-d embeddings for a list of PIL images.
        Returns: torch.Tensor [N, 512], L2 normalized.
        """
        tensors = torch.stack([self.transform(img.convert("RGB")) for img in pil_imgs]).to(self.device)
        with torch.no_grad():
            if self.is_sscd:
                feats = self.model(tensors)
            else:
                raw_feats = self.backbone(tensors).squeeze(-1).squeeze(-1)
                feats = self.projector(raw_feats)
            feats = F.normalize(feats, p=2, dim=-1)
        return feats


# ==============================================================================
# 4. CRYPTOGRAPHIC PROVENANCE LEDGER (SHA-256 Block DAG)
# ==============================================================================
@dataclass
class LineageBlock:
    index: int
    timestamp: float
    datetime_str: str
    composite_hash: str
    parent_a_hash: str
    parent_a_name: str
    parent_b_hash: str
    parent_b_name: str
    attribution_confidence: float
    importance_weight: float
    previous_hash: str
    nonce: int
    block_hash: str


class CryptographicLineageLedger:
    def __init__(self, ledger_file="mota_blockchain_ledger.json"):
        self.ledger_file = ledger_file
        self.chain: List[LineageBlock] = []
        self._load_or_init()

    def _load_or_init(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, "r") as f:
                    data = json.load(f)
                self.chain = [LineageBlock(**b) for b in data]
                return
            except Exception:
                pass
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = LineageBlock(
            index=0,
            timestamp=1700000000.0,
            datetime_str="2026-11-25 00:00:00 UTC",
            composite_hash="0" * 64,
            parent_a_hash="0" * 64,
            parent_a_name="GENESIS_HOST",
            parent_b_hash="0" * 64,
            parent_b_name="GENESIS_DONOR",
            attribution_confidence=1.0,
            importance_weight=1.0,
            previous_hash="0" * 64,
            nonce=42,
            block_hash=hashlib.sha256(b"NITM_MOTA_GENESIS_BLOCK").hexdigest()
        )
        self.chain = [genesis]
        self._save()

    def _save(self):
        with open(self.ledger_file, "w") as f:
            json.dump([asdict(b) for b in self.chain], f, indent=2)

    def mint_attribution_block(self, composite_img: Image.Image,
                               parent_a_name: str, parent_a_hash: str,
                               parent_b_name: str, parent_b_hash: str,
                               confidence: float, importance_w: float) -> LineageBlock:
        prev_block = self.chain[-1]
        now = time.time()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(now))

        comp_bytes = composite_img.tobytes()
        comp_hash = hashlib.sha256(comp_bytes).hexdigest()

        nonce = 0
        while True:
            content = f"{prev_block.index + 1}{now}{comp_hash}{parent_a_hash}{parent_b_hash}{prev_block.block_hash}{nonce}"
            b_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            if b_hash.startswith("00"):
                break
            nonce += 1

        new_block = LineageBlock(
            index=prev_block.index + 1,
            timestamp=now,
            datetime_str=now_str,
            composite_hash=comp_hash,
            parent_a_hash=parent_a_hash,
            parent_a_name=parent_a_name,
            parent_b_hash=parent_b_hash,
            parent_b_name=parent_b_name,
            attribution_confidence=float(confidence),
            importance_weight=float(importance_w),
            previous_hash=prev_block.block_hash,
            nonce=nonce,
            block_hash=b_hash
        )
        self.chain.append(new_block)
        self._save()
        return new_block


# ==============================================================================
# 5. MOTA MASTER PIPELINE (With Fast Cache)
# ==============================================================================
class MOTAPipeline:
    def __init__(self, gallery_dir: str):
        self.gallery_dir = gallery_dir
        self.tokenizer = DynamicMultiScaleTokenizer(overlap_ratio=0.5)
        self.extractor = FeatureExtractor()
        self.gate = ImportanceGate(in_dim=512, hidden_dim=128).to(DEVICE)
        self.ledger = CryptographicLineageLedger()

        self.gallery_records: List[Dict] = []
        self.gallery_embs: Optional[torch.Tensor] = None
        self._build_gallery_index()

    def _build_gallery_index(self):
        if not os.path.exists(self.gallery_dir):
            return

        cache_file = os.path.join(self.gallery_dir, "sscd_gallery_embs.pt")
        meta_cache = os.path.join(self.gallery_dir, "gallery_meta.json")

        valid_exts = {".jpg", ".jpeg", ".png"}
        filenames = sorted([fn for fn in os.listdir(self.gallery_dir) if os.path.splitext(fn)[1].lower() in valid_exts])

        # Check if cache is valid
        if os.path.exists(cache_file) and os.path.exists(meta_cache):
            try:
                with open(meta_cache, "r") as f:
                    records = json.load(f)
                if len(records) == len(filenames):
                    self.gallery_records = records
                    self.gallery_embs = torch.load(cache_file, map_location=self.extractor.device)
                    print(f"[MOTA Pipeline] Loaded {len(records)} pre-computed SSCD embeddings from cache.")
                    return
            except Exception as e:
                print(f"[MOTA Pipeline] Cache load failed ({e}), re-indexing gallery...")

        # Re-index gallery
        imgs = []
        records = []
        for fn in filenames:
            fpath = os.path.join(self.gallery_dir, fn)
            try:
                p_img = Image.open(fpath).convert("RGB")
                imgs.append(p_img)
                with open(fpath, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                records.append({
                    "name": fn,
                    "path": fpath,
                    "hash": file_hash,
                    "size": p_img.size
                })
            except Exception:
                pass

        if imgs:
            self.gallery_records = records
            self.gallery_embs = self.extractor.extract(imgs)
            try:
                torch.save(self.gallery_embs, cache_file)
                with open(meta_cache, "w") as f:
                    json.dump(records, f)
                print(f"[MOTA Pipeline] Cached {len(records)} gallery embeddings.")
            except Exception:
                pass

    def run_attribution(self, composite_img: Image.Image, top_k=5) -> Dict:
        """
        Executes dual-channel lineage attribution with host peeling and Max-Sim matching.
        """
        crops, metadata = self.tokenizer.tokenize(composite_img)
        patch_embs = self.extractor.extract(crops)  # [35, 512]

        global_emb = patch_embs[0:1]               # [1, 512]
        local_embs = patch_embs                     # [35, 512]

        # 1. Host Attribution (Global Channel)
        global_sims = torch.matmul(global_emb, self.gallery_embs.T).squeeze(0) # [G]
        top_host_scores, top_host_indices = torch.topk(global_sims, k=top_k)

        host_match = self.gallery_records[top_host_indices[0].item()]
        host_score = float(top_host_scores[0].item())

        # 2. Importance Gating (MLP)
        with torch.no_grad():
            weights = self.gate(local_embs)         # [35] normalized weights
        weights_np = weights.cpu().numpy()

        # 3. Donor Attribution (Local Max-Sim Channel with Host Peeling)
        token_sims = torch.matmul(local_embs, self.gallery_embs.T) # [35, G]
        
        # Max-Sim across all 35 patches for each candidate gallery image
        max_sims, best_patch_indices = token_sims.max(dim=0)      # [G]
        
        # Peel off detected Host (Parent A)
        peeled_donor_scores = max_sims.clone()
        peeled_donor_scores[top_host_indices[0]] = -1.0

        top_donor_scores, top_donor_indices = torch.topk(peeled_donor_scores, k=top_k)
        donor_match = self.gallery_records[top_donor_indices[0].item()]
        donor_score = float(top_donor_scores[0].item())
        donor_matched_patch = int(best_patch_indices[top_donor_indices[0]].item())

        # Identify highest saliency patch
        salient_patch_idx = int(np.argmax(weights_np))
        salient_meta = metadata[salient_patch_idx]

        # Mint cryptographic block
        block = self.ledger.mint_attribution_block(
            composite_img=composite_img,
            parent_a_name=host_match["name"],
            parent_a_hash=host_match["hash"],
            parent_b_name=donor_match["name"],
            parent_b_hash=donor_match["hash"],
            confidence=(host_score + donor_score) / 2.0,
            importance_w=float(weights_np[salient_patch_idx])
        )

        return {
            "crops": crops,
            "metadata": metadata,
            "weights": weights_np,
            "salient_patch_idx": salient_patch_idx,
            "salient_patch_meta": salient_meta,
            "donor_matched_patch_idx": donor_matched_patch,
            "donor_matched_patch_meta": metadata[donor_matched_patch],
            "parent_a": {
                "record": host_match,
                "score": host_score,
                "top_k": [(self.gallery_records[idx.item()]["name"], float(sc.item()))
                          for idx, sc in zip(top_host_indices, top_host_scores)]
            },
            "parent_b": {
                "record": donor_match,
                "score": donor_score,
                "top_k": [(self.gallery_records[idx.item()]["name"], float(sc.item()))
                          for idx, sc in zip(top_donor_indices, top_donor_scores)]
            },
            "ledger_block": block
        }
