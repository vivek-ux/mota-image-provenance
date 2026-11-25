"""
Notarize Existing Real Photos onto the Blockchain Ledger
"""
import os
import sys
import json
import hashlib
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GALLERY_DIR = os.path.join(BASE_DIR, "gallery")
sys.path.insert(0, BASE_DIR)
from blockchain import ProvenanceBlockchain

def main():
    print("="*70)
    print("⛏️ MINING BLOCKCHAIN PROOF-OF-PROVENANCE FOR ALL REAL GALLERY PHOTOS")
    print("="*70)

    # Initialize fresh blockchain
    blockchain = ProvenanceBlockchain()
    blockchain.chain = []
    blockchain.create_genesis_block()

    files = sorted([f for f in os.listdir(GALLERY_DIR) if f.endswith(".jpg") or f.endswith(".png")])
    print(f"Found {len(files)} real images in gallery.")

    for idx, fname in enumerate(files, 1):
        fpath = os.path.join(GALLERY_DIR, fname)
        with open(fpath, "rb") as f:
            img_bytes = f.read()

        title = fname.replace(".jpg", "").replace(".png", "").replace("_", " ").title()
        author = "Vivek Negi (M.Tech CSE)" if "sunset_in_" in fname else "Verified Photography Network"

        try:
            with Image.open(fpath) as im:
                dims = f"{im.width}x{im.height}"
        except Exception:
            dims = "500x334"

        res = blockchain.notarize_image(
            image_bytes=img_bytes,
            title=title,
            author=author,
            dimensions=dims
        )
        print(f"[{idx:02d}/{len(files)}] Mined Block #{res['block_index']}: '{title}' (Hash: {res['image_hash'][:12]}...)")

    print("="*70)
    print(f"✅ Finished! Total Blocks: {blockchain.get_block_height()} | Ledger: blockchain_ledger.json")
    print("="*70)

if __name__ == "__main__":
    main()
