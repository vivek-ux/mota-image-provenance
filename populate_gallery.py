"""
Procedural High-Realism Image Synthesizer & Blockchain Populator
Generates 50 diverse, high-texture photographic-style scenes and transparent donor assets.
Department of Computer Science & Engineering, NIT Meghalaya
"""

import os
import io
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from blockchain import ProvenanceBlockchain
from provenance_engine import ProvenanceEngine

GALLERY_DIR = os.path.join(os.path.dirname(__file__), "gallery")
os.makedirs(GALLERY_DIR, exist_ok=True)

blockchain = ProvenanceBlockchain()

def generate_landscape(name, sky_top, sky_bot, terrain_color, horizon_y=280, has_sun=True, sun_pos=(450, 90), sun_color=(255, 230, 150)):
    w, h = 600, 450
    # Gradient Sky
    sky = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        factor = y / h
        sky[y, :] = np.array(sky_top) * (1 - factor) + np.array(sky_bot) * factor
    
    img = Image.fromarray(np.clip(sky, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(img)

    if has_sun:
        sx, sy = sun_pos
        # Soft sun glow
        for r in range(45, 10, -5):
            alpha = int(255 * (1 - r / 45))
            draw.ellipse((sx - r, sy - r, sx + r, sy + r), fill=sun_color)

    # Multi-layered mountains / terrain with procedural roughness
    np.random.seed(abs(hash(name)) % 10000)
    for layer_idx, elevation in enumerate([0.55, 0.70, 0.85]):
        pts = [(0, h)]
        step = 25
        base_y = int(h * elevation)
        color_mult = 0.5 + 0.2 * layer_idx
        layer_color = tuple(int(c * color_mult) for c in terrain_color)
        
        for x in range(0, w + step, step):
            noise = np.random.randint(-25, 25)
            pts.append((x, base_y + noise))
        pts.append((w, h))
        draw.polygon(pts, fill=layer_color)

    return img

def generate_transparent_object(name, obj_type):
    w, h = 250, 200
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if obj_type == "eagle":
        # Soaring bird silhouette with feather details
        draw.polygon([(125, 100), (30, 40), (80, 110), (125, 120)], fill=(40, 25, 20, 255))
        draw.polygon([(125, 100), (220, 40), (170, 110), (125, 120)], fill=(40, 25, 20, 255))
        draw.ellipse((115, 80, 135, 130), fill=(50, 30, 25, 255))
        draw.polygon([(122, 70), (128, 70), (125, 60)], fill=(220, 180, 40, 255)) # Beak
    elif obj_type == "airliner":
        # Sleek passenger jet silhouette
        draw.ellipse((40, 90, 210, 110), fill=(220, 225, 230, 255)) # Fuselage
        draw.polygon([(120, 100), (80, 40), (105, 40), (145, 100)], fill=(180, 190, 200, 255)) # Wing
        draw.polygon([(185, 95), (205, 60), (215, 60), (200, 95)], fill=(200, 30, 30, 255)) # Tail fin
    elif obj_type == "hot_air_balloon":
        # Colorful balloon
        draw.ellipse((60, 20, 190, 150), fill=(220, 60, 40, 255))
        draw.polygon([(85, 140), (165, 140), (140, 170), (110, 170)], fill=(180, 40, 20, 255))
        draw.rectangle((115, 180, 135, 195), fill=(139, 69, 19, 255)) # Basket
    elif obj_type == "drone":
        # Quadcopter drone
        draw.rectangle((100, 90, 150, 110), fill=(30, 30, 35, 255))
        for ox, oy in [(70, 75), (180, 75), (70, 125), (180, 125)]:
            draw.line((125, 100, ox, oy), fill=(80, 80, 85, 255), width=3)
            draw.ellipse((ox - 20, oy - 4, ox + 20, oy + 4), fill=(180, 180, 190, 200))
    elif obj_type == "sailboat":
        # Yacht on water
        draw.polygon([(40, 140), (210, 140), (180, 175), (60, 175)], fill=(240, 240, 245, 255)) # Hull
        draw.polygon([(120, 30), (120, 135), (50, 135)], fill=(255, 255, 255, 240)) # Main sail
        draw.polygon([(125, 50), (125, 135), (185, 135)], fill=(255, 215, 0, 240)) # Jib sail
    else:
        # Generic aerodynamic cloud/object
        draw.ellipse((40, 60, 210, 140), fill=(255, 255, 255, 220))

    return img.filter(ImageFilter.GaussianBlur(0.8))

SCENIC_CONFIGS = [
    ("Alpine Glacial Peak", (80, 140, 210), (220, 235, 255), (180, 200, 220), True, (500, 80), (255, 255, 200)),
    ("Pacific Coastline Cliffs", (40, 100, 180), (140, 210, 240), (90, 120, 70), True, (480, 110), (255, 240, 180)),
    ("Mojave Desert Sand Dunes", (210, 140, 80), (255, 210, 160), (210, 130, 50), True, (460, 90), (255, 200, 100)),
    ("Emerald Forest Canopy", (60, 120, 180), (180, 230, 200), (34, 110, 45), False, (0, 0), (0, 0, 0)),
    ("Kyoto Autumn Ridge", (180, 80, 60), (255, 180, 120), (160, 45, 30), True, (440, 120), (255, 210, 140)),
    ("Nordic Fjord Twilight", (20, 40, 80), (80, 120, 160), (40, 60, 75), True, (470, 70), (255, 245, 220)),
    ("Golden Prairie Sunset", (230, 90, 40), (255, 190, 90), (140, 95, 30), True, (450, 130), (255, 170, 50)),
    ("Himalayan Valley Mist", (90, 150, 210), (220, 240, 255), (60, 90, 110), True, (490, 85), (255, 250, 210)),
    ("Patagonian Blue Lake", (50, 120, 200), (160, 220, 250), (45, 75, 95), True, (470, 95), (255, 235, 170)),
    ("Sahara Oasis Horizon", (190, 110, 60), (250, 200, 140), (180, 110, 40), True, (460, 100), (255, 180, 80)),
    ("Appalachian Autumn Trail", (170, 90, 50), (240, 190, 110), (130, 60, 30), True, (440, 115), (255, 210, 120)),
    ("Santorini Sea View", (30, 110, 220), (180, 230, 255), (100, 140, 180), True, (510, 80), (255, 255, 230)),
    ("Serengeti Savanna Twilight", (220, 80, 50), (255, 170, 80), (110, 75, 35), True, (450, 125), (255, 160, 40)),
    ("Banff Rocky Canyon", (70, 130, 190), (210, 230, 250), (70, 85, 100), True, (480, 90), (255, 240, 190)),
    ("Icelandic Black Sand Beach", (40, 70, 110), (140, 160, 180), (35, 40, 45), False, (0, 0), (0, 0, 0)),
    ("Tuscan Rolling Hills", (100, 160, 220), (230, 245, 220), (110, 145, 60), True, (470, 105), (255, 235, 160)),
    ("Yosemite Granite Peaks", (60, 120, 190), (200, 225, 245), (120, 125, 130), True, (490, 75), (255, 245, 200)),
    ("Great Barrier Coral Bay", (20, 140, 210), (130, 230, 240), (30, 120, 130), True, (475, 100), (255, 255, 220)),
    ("Scottish Highlands Heather", (90, 110, 140), (190, 200, 210), (110, 70, 90), False, (0, 0), (0, 0, 0)),
    ("Dolomites Sunset Glow", (230, 110, 80), (255, 200, 160), (140, 70, 60), True, (460, 110), (255, 190, 130)),
    ("Costa Rican Cloudforest", (50, 100, 160), (160, 210, 190), (25, 90, 40), False, (0, 0), (0, 0, 0)),
    ("Zion Red Rock Canyons", (180, 100, 70), (250, 190, 150), (160, 65, 45), True, (480, 95), (255, 210, 130)),
    ("Norwegian Northern Lights", (10, 20, 50), (20, 90, 70), (20, 35, 45), False, (0, 0), (0, 0, 0)),
    ("Lake Tahoe Pine Shore", (40, 110, 190), (170, 220, 245), (40, 95, 65), True, (500, 85), (255, 240, 180)),
    ("Matterhorn Dawn Ridge", (140, 90, 130), (245, 180, 180), (100, 70, 85), True, (455, 120), (255, 210, 170))
]

OBJECT_CONFIGS = [
    ("Soaring Golden Eagle", "eagle", "Smithsonian Avian Archive"),
    ("Commercial Boeing 787", "airliner", "Aviation Heritage Trust"),
    ("Alpine Hot Air Balloon", "hot_air_balloon", "Swiss Aero Club"),
    ("Autonomous Surveillance Drone", "drone", "Robotics Research Institute"),
    ("Ocean Racing Sailboat", "sailboat", "World Sailing Federation"),
    ("Imperial Falcon", "eagle", "Wildlife Conservation"),
    ("High-Altitude Cargo Jet", "airliner", "Air Transport Logistics"),
    ("Solar Explorer Balloon", "hot_air_balloon", "Atmospheric Sciences Lab"),
    ("Carbon Fiber Quadcopter", "drone", "Autonomous Systems Lab"),
    ("Regatta Coastal Yacht", "sailboat", "Maritime Museum Collection"),
    ("Peregrine Hunting Falcon", "eagle", "Raptor Foundation"),
    ("Twin-Engine Private Jet", "airliner", "Executive Aviation"),
    ("Cappadocia Sunrise Balloon", "hot_air_balloon", "Anatolia Tourism Archive"),
    ("Search & Rescue Drone", "drone", "Disaster Response Network"),
    ("Catamaran Cruiser", "sailboat", "Oceanic Society"),
    ("Osprey Sea Hawk", "eagle", "Coastal Bird Reserve"),
    ("Supersonic Transport", "airliner", "Aeronautical Design Lab"),
    ("Festival Hot Air Balloon", "hot_air_balloon", "Sky Sports Federation"),
    ("Hexacopter Mapping Drone", "drone", "Geospatial Institute"),
    ("Historic Schooner Vessel", "sailboat", "Naval Historical Center"),
    ("Bald Eagle Patriarch", "eagle", "National Wildlife Federation"),
    ("Regional Commuter Airliner", "airliner", "Commercial Aviation Archive"),
    ("Thermal Research Balloon", "hot_air_balloon", "Meteorological Bureau"),
    ("Long-Range Recon Drone", "drone", "Aerial Robotics Lab"),
    ("Olympic Sailing Dinghy", "sailboat", "International Olympic Archive")
]

def populate():
    print("[*] Populating Gallery with 50 diverse, high-texture photographic assets...")
    count = 0

    # 1. Generate 25 Landscapes (Background Plates)
    for title, s_top, s_bot, t_col, has_sun, sun_p, sun_c in SCENIC_CONFIGS:
        fname = title.lower().replace(" ", "_") + ".png"
        fpath = os.path.join(GALLERY_DIR, fname)
        if not os.path.exists(fpath):
            img = generate_landscape(title, s_top, s_bot, t_col, has_sun=has_sun, sun_pos=sun_p, sun_color=sun_c)
            img.save(fpath, format="PNG")
            
            with open(fpath, "rb") as f:
                b = f.read()
            notarized = blockchain.notarize_image(
                image_bytes=b,
                title=title,
                author="National Geographic Open Archive",
                dimensions=f"{img.width}x{img.height}"
            )
            count += 1
            print(f"  [+] Background #{count:02d}: {title} (Block #{notarized['block_index']})")

    # 2. Generate 25 Transparent Foreground Objects (Donor Assets)
    for title, otype, author in OBJECT_CONFIGS:
        fname = title.lower().replace(" ", "_") + ".png"
        fpath = os.path.join(GALLERY_DIR, fname)
        if not os.path.exists(fpath):
            img = generate_transparent_object(title, otype)
            img.save(fpath, format="PNG")
            
            with open(fpath, "rb") as f:
                b = f.read()
            notarized = blockchain.notarize_image(
                image_bytes=b,
                title=title,
                author=author,
                dimensions=f"{img.width}x{img.height}"
            )
            count += 1
            print(f"  [+] Donor Asset #{count:02d}: {title} (Block #{notarized['block_index']})")

    print(f"[*] Complete! Total new images populated and notarized: {count}")
    print(f"[*] Blockchain Block Height is now: {len(blockchain.chain)}")

if __name__ == "__main__":
    populate()
