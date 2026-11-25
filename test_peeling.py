# Test syntax of Host Peeling / Residual Splicing Attribution
code = """
import torch

def host_peeling_attribution(global_sims, patch_sims, g_ids, threshold=0.70):
    # 1. Identify Host Parent A from Global
    top_a_idx = global_sims.argmax().item()
    parent_a_id = g_ids[top_a_idx]
    
    # 2. Find which query patches belong to Parent A
    # patch_sims: [1000, 35, 35] -> [gallery, gallery_patches, query_patches]
    sim_to_a_per_query_patch = patch_sims[top_a_idx].max(dim=0)[0] # [35]
    
    # 3. Foreign / Donor patches are those with LOW similarity to Host Parent A
    donor_patch_mask = sim_to_a_per_query_patch < threshold
    if not donor_patch_mask.any():
        # Fallback to the patch with lowest similarity to Parent A
        donor_patch_mask = torch.zeros_like(sim_to_a_per_query_patch, dtype=torch.bool)
        donor_patch_mask[sim_to_a_per_query_patch.argmin()] = True
        
    donor_patch_idx = donor_patch_mask.nonzero().squeeze(-1)
    
    # 4. Search gallery for the donor object using ONLY the foreign patch(es)
    # This completely eliminates background false positives!
    foreign_patch_sims = patch_sims[:, :, donor_patch_idx] # [1000, 35, num_foreign]
    donor_scores = foreign_patch_sims.amax(dim=(1, 2)) # [1000]
    
    # Peel off Host Parent A
    donor_scores[top_a_idx] = -1.0
    
    return top_a_idx, donor_scores
"""
print("Syntax OK!")
