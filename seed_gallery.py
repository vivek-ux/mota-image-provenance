"""
Seed default gallery images and notarize them onto the Provenance Blockchain.
"""

import os
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from blockchain import ProvenanceBlockchain
from provenance_engine import ProvenanceEngine

GALLERY_DIR = os.path.join(os.path.dirname(__file__), "gallery")
os.makedirs(GALLERY_DIR, exist_ok=True)

blockchain = ProvenanceBlockchain()
engine = ProvenanceEngine(GALLERY_DIR)

def create_mountain_landscape():
    img = Image.new("RGB", (600, 450), color=(135, 206, 235)) # Sky
    draw = ImageDraw.Draw(img)
    # Sun
    draw.ellipse((450, 40, 530, 120), fill=(255, 223, 0), outline=(255, 165, 0))
    # Mountains
    draw.polygon([(0, 450), (180, 180), (360, 450)], fill=(70, 90, 120))
    draw.polygon([(150, 450), (340, 150), (520, 450)], fill=(50, 70, 95))
    draw.polygon([(300, 450), (480, 210), (600, 450)], fill=(80, 100, 130))
    # Green meadow
    draw.rectangle([0, 360, 600, 450], fill=(34, 139, 34))
    return img

def create_vintage_car():
    img = Image.new("RGB", (600, 450), color=(240, 240, 245)) # Clean studio
    draw = ImageDraw.Draw(img)
    # Car body
    draw.rounded_rectangle([120, 220, 480, 320], radius=25, fill=(220, 20, 60))
    # Car cabin
    draw.polygon([(200, 220), (250, 140), (380, 140), (430, 220)], fill=(180, 10, 40))
    draw.polygon([(215, 215), (255, 150), (310, 150), (310, 215)], fill=(200, 240, 255))
    draw.polygon([(325, 215), (325, 150), (375, 150), (415, 215)], fill=(200, 240, 255))
    # Wheels
    draw.ellipse((160, 290, 230, 360), fill=(30, 30, 30), outline=(200, 200, 200), width=4)
    draw.ellipse((370, 290, 440, 360), fill=(30, 30, 30), outline=(200, 200, 200), width=4)
    return img

def create_golden_eagle():
    img = Image.new("RGB", (600, 450), color=(230, 245, 255))
    draw = ImageDraw.Draw(img)
    # Eagle wings
    draw.polygon([(300, 200), (80, 100), (200, 240)], fill=(139, 69, 19))
    draw.polygon([(300, 200), (520, 100), (400, 240)], fill=(139, 69, 19))
    # Body
    draw.ellipse((260, 160, 340, 280), fill=(160, 82, 45))
    # Head & beak
    draw.ellipse((275, 120, 325, 170), fill=(255, 255, 255))
    draw.polygon([(320, 140), (345, 150), (320, 160)], fill=(255, 215, 0))
    return img

def create_modern_office():
    img = Image.new("RGB", (600, 450), color=(220, 225, 230))
    draw = ImageDraw.Draw(img)
    # Windows & City view
    for x in range(40, 560, 90):
        draw.rectangle([x, 50, x + 70, 220], fill=(100, 149, 237), outline=(150, 150, 150), width=3)
    # Floor
    draw.rectangle([0, 250, 600, 450], fill=(139, 115, 85))
    # Conference Table
    draw.polygon([(100, 380), (500, 380), (440, 290), (160, 290)], fill=(50, 50, 50))
    return img

SEEDS = [
    ("Mountain Landscape (Alps)", create_mountain_landscape, "Vivek Negi (NITM)"),
    ("Red Vintage Sports Car", create_vintage_car, "National Geographic Archive"),
    ("Golden Soaring Eagle", create_golden_eagle, "Smithsonian Wildlife"),
    ("Modern High-Rise Office", create_modern_office, "Architecture Digest")
]

def seed():
    print("[*] Seeding default gallery and notarizing to Blockchain...")
    for title, generator_fn, author in SEEDS:
        filename = title.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".png"
        filepath = os.path.join(GALLERY_DIR, filename)

        img = generator_fn()
        img.save(filepath, format="PNG")

        with open(filepath, "rb") as f:
            img_bytes = f.read()

        # Check if already notarized
        img_hash = blockchain.get_latest_block().records[0].get("image_hash") if blockchain.chain else ""
        notarized = blockchain.notarize_image(
            image_bytes=img_bytes,
            title=title,
            author=author,
            dimensions=f"{img.width}x{img.height}"
        )
        print(f"  [+] Notarized Block #{notarized['block_index']} | {title} | Hash: {notarized['image_hash'][:16]}...")

    print("[*] Seeding complete! Blockchain ledger ready.")

if __name__ == "__main__":
    seed()
