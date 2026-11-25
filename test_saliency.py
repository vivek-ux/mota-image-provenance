# Let's inspect the actual diagnostic code
code = """
import numpy as np
import torch

# Test how patch variance filters out flat background gradient matches
def compute_patch_saliency(crop_pil):
    arr = np.array(crop_pil).astype(np.float32)
    # Variance of gradients (Laplacian variance / edge density)
    # Flat gradient backgrounds have very low variance compared to objects
    var = np.var(arr)
    return var
"""
