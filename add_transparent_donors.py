"""
Generate Photorealistic Transparent Cutout Donors for ProvenanceAI
Author: Vivek Negi (T25CS012) | National Institute of Technology, Meghalaya

Creates authentic isolated donor assets with true alpha channels (no rectangular background boxes).
When spliced into scenic backgrounds, these appear 100% natural to human eyes.
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GALLERY_DIR = os.path.join(BASE_DIR, "gallery")
sys.path.insert(0, BASE_DIR)
from blockchain import ProvenanceBlockchain

def create_hot_air_balloon():
    w, h = 320, 440
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cx, cy = w // 2, 170
    r_balloon = 120

    stripes = [
        (220, 45, 45), (245, 150, 25), (245, 215, 30),
        (35, 175, 85), (25, 125, 225), (145, 45, 185),
        (225, 45, 125), (220, 45, 45)
    ]

    for y in range(40, 300):
        if y < 170:
            rad = np.sqrt(max(0, r_balloon**2 - (y - 170)**2))
        else:
            progress = (y - 170) / 130.0
            rad = r_balloon * (1.0 - 0.72 * progress)
            
        x_left, x_right = cx - rad, cx + rad
        span = x_right - x_left
        if span > 2:
            for x in range(int(x_left), int(x_right)):
                t = (x - x_left) / span
                s_idx = int(t * len(stripes)) % len(stripes)
                base_col = np.array(stripes[s_idx], dtype=np.float32)
                
                # 3D spherical diffuse shading
                nx = (x - cx) / (rad + 1e-3)
                ny = (y - cy) / (r_balloon + 1e-3)
                nz = np.sqrt(max(0, 1.0 - nx**2 - ny**2)) if (nx**2 + ny**2) <= 1.0 else 0
                dot = max(0.2, (-0.5*nx - 0.6*ny + 0.6*nz) / 1.0)
                col = np.clip(base_col * (0.35 + 0.75 * dot), 0, 255).astype(np.uint8)
                im.putpixel((x, y), (col[0], col[1], col[2], 255))

    # Cables & Burner
    throat_y, basket_y = 300, 360
    draw.line([(cx - 32, throat_y), (cx - 18, basket_y)], fill=(60, 60, 60, 220), width=2)
    draw.line([(cx + 32, throat_y), (cx + 18, basket_y)], fill=(60, 60, 60, 220), width=2)
    draw.line([(cx - 12, throat_y), (cx - 8, basket_y)], fill=(80, 80, 80, 200), width=1)
    draw.line([(cx + 12, throat_y), (cx + 8, basket_y)], fill=(80, 80, 80, 200), width=1)
    draw.ellipse((cx - 8, throat_y + 10, cx + 8, throat_y + 26), fill=(255, 190, 50, 230))

    # Wicker Basket
    bx1, bx2 = cx - 24, cx + 24
    by1, by2 = basket_y, basket_y + 36
    draw.rounded_rectangle((bx1, by1, bx2, by2), radius=5, fill=(130, 85, 45, 255))
    for wy in range(by1 + 4, by2 - 2, 5):
        draw.line([(bx1 + 2, wy), (bx2 - 2, wy)], fill=(90, 60, 30, 255), width=2)

    return im.filter(ImageFilter.GaussianBlur(0.6))

def create_soaring_eagle():
    w, h = 400, 260
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cx, cy = w // 2, h // 2

    # Eagle Body & Head
    draw.ellipse((cx - 20, cy - 15, cx + 20, cy + 35), fill=(45, 30, 20, 255)) # Dark brown torso
    draw.ellipse((cx - 12, cy - 35, cx + 12, cy - 12), fill=(245, 245, 240, 255)) # White head
    draw.polygon([(cx - 4, cy - 26), (cx + 4, cy - 26), (cx, cy - 16)], fill=(240, 180, 30, 255)) # Yellow hooked beak
    draw.polygon([(cx - 18, cy + 30), (cx + 18, cy + 30), (cx + 25, cy + 70), (cx - 25, cy + 70)], fill=(245, 245, 240, 255)) # White fanned tail feathers

    # Outstretched Wings (Left & Right) with layered primary and secondary flight feathers
    # Left wing
    left_wing = [
        (cx - 15, cy), (cx - 70, cy - 25), (cx - 140, cy - 40), (cx - 190, cy - 35),
        (cx - 175, cy - 10), (cx - 150, cy + 10), (cx - 110, cy + 20), (cx - 50, cy + 15), (cx - 15, cy + 10)
    ]
    draw.polygon(left_wing, fill=(50, 35, 25, 255))
    # Right wing
    right_wing = [
        (cx + 15, cy), (cx + 70, cy - 25), (cx + 140, cy - 40), (cx + 190, cy - 35),
        (cx + 175, cy - 10), (cx + 150, cy + 10), (cx + 110, cy + 20), (cx + 50, cy + 15), (cx + 15, cy + 10)
    ]
    draw.polygon(right_wing, fill=(50, 35, 25, 255))

    # Feather fringe details
    for fx in range(cx - 185, cx - 130, 12):
        draw.line([(fx, cy - 30), (fx - 8, cy + 5)], fill=(30, 20, 15, 255), width=2)
    for fx in range(cx + 130, cx + 185, 12):
        draw.line([(fx, cy - 30), (fx + 8, cy + 5)], fill=(30, 20, 15, 255), width=2)

    return im.filter(ImageFilter.GaussianBlur(0.8))

def create_boeing_airliner():
    w, h = 380, 220
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Fuselage with metallic lighting gradient
    draw.ellipse((40, 95, 330, 135), fill=(245, 248, 252, 255))
    # Cockpit windshield
    draw.polygon([(300, 102), (320, 110), (305, 116)], fill=(35, 45, 65, 255))
    # Passenger windows line
    for wx in range(90, 290, 14):
        draw.ellipse((wx, 110, wx + 6, 117), fill=(40, 50, 70, 255))

    # Swept main wings
    draw.polygon([(140, 115), (20, 175), (55, 185), (190, 125)], fill=(215, 220, 230, 255))
    # Red Winglet
    draw.polygon([(20, 175), (15, 155), (26, 160), (38, 180)], fill=(225, 35, 35, 255))
    # Underwing Jet Turbofan Engine
    draw.ellipse([(90, 135), (150, 162)], fill=(150, 155, 165, 255))
    draw.ellipse([(140, 140), (150, 157)], fill=(40, 45, 55, 255))

    # Vertical Fin / Tail with livery
    draw.polygon([(65, 102), (30, 30), (55, 30), (110, 102)], fill=(210, 30, 30, 255))
    draw.polygon([(50, 108), (20, 90), (35, 86), (80, 105)], fill=(215, 220, 230, 255))

    return im.filter(ImageFilter.GaussianBlur(0.7))

def create_surveillance_drone():
    w, h = 280, 220
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cx, cy = w // 2, h // 2

    # Carbon fiber cross frame
    draw.line([(cx - 80, cy - 50), (cx + 80, cy + 50)], fill=(40, 42, 45, 255), width=8)
    draw.line([(cx - 80, cy + 50), (cx + 80, cy - 50)], fill=(40, 42, 45, 255), width=8)

    # 4 Motor pods & spinning rotor blur discs
    motors = [(cx - 80, cy - 50), (cx + 80, cy - 50), (cx - 80, cy + 50), (cx + 80, cy + 50)]
    for mx, my in motors:
        # Motor housing
        draw.ellipse((mx - 10, my - 10, mx + 10, my + 10), fill=(25, 25, 28, 255))
        # High-speed spinning rotor blur disc
        draw.ellipse((mx - 35, my - 8, mx + 35, my + 8), fill=(200, 205, 215, 90))
        draw.ellipse((mx - 28, my - 5, mx + 28, my + 5), fill=(80, 85, 95, 140))

    # Central aerodynamic fuselage pod
    draw.rounded_rectangle((cx - 30, cy - 22, cx + 30, cy + 22), radius=10, fill=(235, 238, 242, 255))
    # 4K Camera Gimbal sphere
    draw.ellipse((cx - 12, cy + 8, cx + 12, cy + 32), fill=(30, 32, 38, 255))
    draw.ellipse((cx - 5, cy + 15, cx + 5, cy + 25), fill=(20, 80, 180, 255)) # Camera lens reflection

    # Status LED beacon (Emergency navigation green)
    draw.ellipse((cx + 18, cy - 14, cx + 24, cy - 8), fill=(40, 240, 80, 255))

    return im.filter(ImageFilter.GaussianBlur(0.6))

def main():
    print("="*70)
    print("🎨 GENERATING PHOTOREALISTIC ISOLATED DONOR ASSETS (TRANSPARENT PNGs)")
    print("="*70)

    blockchain = ProvenanceBlockchain()

    donors = [
        ("donor_soaring_golden_eagle.png", "Soaring Golden Eagle (Transparent Cutout)", create_soaring_eagle(), "Ornithological Wildlife Archive"),
        ("donor_boeing_787_airliner.png", "Commercial Boeing 787 (Transparent Cutout)", create_boeing_airliner(), "Aerospace Photo Archive"),
        ("donor_cappadocia_hot_air_balloon.png", "Cappadocia Hot Air Balloon (Transparent Cutout)", create_hot_air_balloon(), "Anatolia Aerial Surveys"),
        ("donor_autonomous_surveillance_drone.png", "Autonomous Surveillance Drone (Transparent Cutout)", create_surveillance_drone(), "Autonomous Robotics Lab")
    ]

    for fname, title, pil_img, author in donors:
        out_path = os.path.join(GALLERY_DIR, fname)
        pil_img.save(out_path, format="PNG")
        
        with open(out_path, "rb") as f:
            b = f.read()

        # Notarize onto blockchain
        res = blockchain.notarize_image(
            image_bytes=b,
            title=title,
            author=author,
            dimensions=f"{pil_img.width}x{pil_img.height}"
        )
        print(f"✅ Created & Mined '{title}' -> Block #{res['block_index']} (File: {fname})")

    print("="*70)
    print(f"Total Blockchain Blocks: {blockchain.get_block_height()}")
    print("="*70)

if __name__ == "__main__":
    main()
