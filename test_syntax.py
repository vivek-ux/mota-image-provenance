import os

# Test syntax of the proposed Kaggle cell
code = """
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm
from PIL import Image

def evaluate_provenance_lineage(queries, queries_dir, global_bank, patch_bank, gallery_ids, 
                                extractor, tokenizer, top_k=5, filter_mode=None):
    \"\"\"
    Dual-Channel Multi-Source Provenance Attribution:
    - Primary Channel (Parent A / Host): Global GeM-SSCD representation (captures host scene).
    - Secondary Channel (Parent B / Donor): MOTA Max-Patch Consensus (captures localized donor).
    - Unified Lineage Attribution: Top candidates from Global + Top candidates from Local Max-Patch.
    \"\"\"
    if filter_mode:
        eval_queries = [q for q in queries if q["blending_mode"] == filter_mode]
    else:
        eval_queries = queries
        
    hits_a, hits_b, hits_both = 0, 0, 0
    total = len(eval_queries)
    device = global_bank.device
    
    for q in eval_queries:
        img_path = os.path.join(queries_dir, f"{q['query_id']}.jpg")
        pil_img = Image.open(img_path).convert("RGB")
        
        # 1. Global Feature Extraction (for Host / Parent A)
        t = extractor.preprocess(pil_img).unsqueeze(0).to(device)
        with torch.no_grad():
            q_g = extractor(t) # [1, 512]
        global_sims = torch.matmul(q_g, global_bank.T).squeeze(0) # [N_gal]
        
        # 2. MOTA Local Token Alignment (for Donor / Parent B)
        crops = tokenizer.get_crops(pil_img)
        t_crops = torch.stack([extractor.preprocess(c) for c in crops]).to(device)
        with torch.no_grad():
            q_p = extractor(t_crops) # [T_q, 512]
            
        # patch_bank: [N_gal, T_g, 512], q_p: [T_q, 512]
        # patch_sims: [N_gal, T_g, T_q]
        patch_sims = torch.einsum('ndt,qt->ndq', patch_bank, q_p)
        
        # Max-patch alignment: best match between candidate patches and query tokens
        # donor_scores[g] = max_{j in T_g, i in T_q} <p_{g,j}, q_i>
        donor_scores = patch_sims.amax(dim=(1, 2)) # [N_gal]
        
        # Top-K for Parent A from Global
        topk_a_idx = torch.topk(global_sims, k=top_k).indices.cpu().numpy()
        retrieved_a = [gallery_ids[idx] for idx in topk_a_idx]
        
        # Top-K for Parent B from Local Max-Patch (excluding detected Parent A)
        top_parent_a_idx = topk_a_idx[0]
        donor_scores_masked = donor_scores.clone()
        donor_scores_masked[top_parent_a_idx] = -1.0 # peel off Host Parent A
        topk_b_idx = torch.topk(donor_scores_masked, k=top_k).indices.cpu().numpy()
        retrieved_b = [gallery_ids[idx] for idx in topk_b_idx]
        
        # Combined Unified Attribution Set (Top 3 Global + Top 2 Local Donor)
        unified_idx = list(topk_a_idx[:3]) + [idx for idx in topk_b_idx if idx not in topk_a_idx[:3]][:2]
        retrieved_lineage = [gallery_ids[idx] for idx in unified_idx]
        
        got_a = q['parent_a'] in retrieved_a
        got_b = q['parent_b'] in retrieved_b
        got_both = (q['parent_a'] in retrieved_lineage) and (q['parent_b'] in retrieved_lineage)
        
        if got_a: hits_a += 1
        if got_b: hits_b += 1
        if got_both: hits_both += 1
        
    return {
        "Parent A R@5": f"{(hits_a / total) * 100:.2f}%",
        "Parent B R@5": f"{(hits_b / total) * 100:.2f}%",
        "Full Lineage R@5": f"{(hits_both / total) * 100:.2f}%",
        "Samples": total
    }
"""
print("Syntax OK!")
