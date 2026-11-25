import os
import urllib.request
import json
import time
from PIL import Image

# Curated list of verified, real-world public photography (36 distinct real photos)
REAL_PHOTOS = [
    # --- People & Candids ---
    {
        "id": "real_student_library",
        "url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1000&q=85",
        "title": "University Students Studying in Modern Library",
        "category": "people",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_young_woman_cafe",
        "url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=1000&q=85",
        "title": "Young Woman Portrait Natural Light",
        "category": "people",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_man_walking_street",
        "url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=1000&q=85",
        "title": "Young Man Candid Street Portrait",
        "category": "people",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_woman_portrait_outdoor",
        "url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=1000&q=85",
        "title": "Smiling Woman Golden Hour Portrait",
        "category": "people",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_man_casual_jacket",
        "url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1000&q=85",
        "title": "Young Professional Man Portrait",
        "category": "people",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_person_walking_sidewalk",
        "url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1000&q=85",
        "title": "Young Woman Walking City Sidewalk",
        "category": "people",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_photographer_candid",
        "url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=1000&q=85",
        "title": "Street Photographer Outdoor Portrait",
        "category": "people",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_traveler_viewpoint",
        "url": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1000&q=85",
        "title": "Solo Traveler on Scenic Road Trip",
        "category": "people",
        "author": "Verified Real Photography / Unsplash"
    },

    # --- Urban & Architecture (Authentic Environments) ---
    {
        "id": "real_cozy_coffee_shop",
        "url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=1000&q=85",
        "title": "Warm Artisan Coffee Shop Interior",
        "category": "urban",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_modern_library_hall",
        "url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1000&q=85",
        "title": "Grand University Library Study Hall",
        "category": "urban",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_city_crosswalk_downtown",
        "url": "https://images.unsplash.com/photo-1477959858617-67f30bc75b82?w=1000&q=85",
        "title": "Downtown Urban Street & Crosswalk",
        "category": "urban",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_rainy_city_evening",
        "url": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1000&q=85",
        "title": "Evening City Street with Streetlamps",
        "category": "urban",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_metro_subway_station",
        "url": "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?w=1000&q=85",
        "title": "Modern Underground Metro Platform",
        "category": "urban",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_quiet_bookstore_interior",
        "url": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1000&q=85",
        "title": "Cozy Independent Bookstore Shelves",
        "category": "urban",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_college_campus_pathway",
        "url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1000&q=85",
        "title": "Historic University Campus Brick Pathway",
        "category": "urban",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_rooftop_sunset_skyline",
        "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1000&q=85",
        "title": "Glass Skyscraper Architectural Perspective",
        "category": "urban",
        "author": "Verified Real Photography / Unsplash"
    },

    # --- Vehicles & Travel ---
    {
        "id": "real_classic_sports_car",
        "url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1000&q=85",
        "title": "Porsche Sports Coupe on Mountain Road",
        "category": "vehicles",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_luxury_black_coupe",
        "url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1000&q=85",
        "title": "Modern Sports Car in Studio Lighting",
        "category": "vehicles",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_vintage_caferacer_bike",
        "url": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=1000&q=85",
        "title": "Custom Cafe Racer Motorcycle",
        "category": "vehicles",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_commercial_flight_wing",
        "url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1000&q=85",
        "title": "Airplane In Flight Above Cloud Layer",
        "category": "vehicles",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_scenic_highway_drive",
        "url": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1000&q=85",
        "title": "Supercar Rear Profile in Open Countryside",
        "category": "vehicles",
        "author": "Verified Real Photography / Unsplash"
    },

    # --- Scenic Nature & Landscapes ---
    {
        "id": "real_himalayan_mountain_ridge",
        "url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1000&q=85",
        "title": "Majestic Alpine Mountain Ridges",
        "category": "nature",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_misty_pine_treeline",
        "url": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1000&q=85",
        "title": "Misty Evergreen Forest in Morning Light",
        "category": "nature",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_turquoise_glacial_lake",
        "url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1000&q=85",
        "title": "Pristine Glacial Lake & Mountain Range",
        "category": "nature",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_pacific_ocean_coastline",
        "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1000&q=85",
        "title": "Tropical Ocean Shoreline & Clean Beach",
        "category": "nature",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_golden_sunlight_forest",
        "url": "https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=1000&q=85",
        "title": "Sun Rays Piercing Forest Canopy",
        "category": "nature",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_desert_sand_dunes",
        "url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=1000&q=85",
        "title": "Golden Desert Sand Dunes Sunset",
        "category": "nature",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_starry_night_milkyway",
        "url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1000&q=85",
        "title": "Starry Night Sky Over Mountain Peak",
        "category": "nature",
        "author": "Verified Real Photography / Unsplash"
    },

    # --- Real Everyday & Forensic Objects ---
    {
        "id": "real_wooden_work_desk",
        "url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1000&q=85",
        "title": "Minimalist Tech Workspace with Laptop",
        "category": "objects",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_analog_slr_camera",
        "url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=1000&q=85",
        "title": "Classic Analog 35mm Camera on Surface",
        "category": "objects",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_luxury_wrist_watch",
        "url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1000&q=85",
        "title": "Minimalist Modern Wristwatch",
        "category": "objects",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_leather_travel_bag",
        "url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=1000&q=85",
        "title": "Vintage Canvas & Leather Backpack",
        "category": "objects",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_ceramic_coffee_mug",
        "url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=1000&q=85",
        "title": "Hot Espresso Coffee Cup on Wood",
        "category": "objects",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_headphones_audio",
        "url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1000&q=85",
        "title": "High-Fidelity Studio Headphones",
        "category": "objects",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_sneakers_athletic",
        "url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1000&q=85",
        "title": "Red Athletic Running Shoes",
        "category": "objects",
        "author": "Verified Real Photography / Unsplash"
    },
    {
        "id": "real_sunglasses_travel",
        "url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=1000&q=85",
        "title": "Designer Sunglasses on Wooden Surface",
        "category": "objects",
        "author": "Verified Real Photography / Unsplash"
    }
]

def download_and_verify():
    gallery_dir = os.path.join(os.path.dirname(__file__), "gallery")
    os.makedirs(gallery_dir, exist_ok=True)
    
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    
    downloaded = []
    print(f"Starting download of {len(REAL_PHOTOS)} curated real-world photographs...")

    for idx, item in enumerate(REAL_PHOTOS):
        dest_filename = f"{item['id']}.jpg"
        dest_path = os.path.join(gallery_dir, dest_filename)
        
        try:
            req = urllib.request.Request(item["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp, open(dest_path, "wb") as out_file:
                out_file.write(resp.read())
            
            # Verify and standardize image (max dimension 1200, high quality JPEG)
            with Image.open(dest_path) as img:
                img = img.convert("RGB")
                img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
                img.save(dest_path, "JPEG", quality=92)
            
            size_kb = os.path.getsize(dest_path) // 1024
            print(f"[{idx+1}/{len(REAL_PHOTOS)}] OK: {dest_filename} ({size_kb} KB) - {item['title']}")
            downloaded.append({
                "filename": dest_filename,
                "title": item["title"],
                "author": item["author"],
                "category": item["category"]
            })
            time.sleep(0.1) # polite pause
        except Exception as e:
            print(f"[{idx+1}/{len(REAL_PHOTOS)}] FAILED: {dest_filename} -> {e}")

    # Save manifest
    manifest_path = os.path.join(os.path.dirname(__file__), "real_gallery_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(downloaded, f, indent=2)
    print(f"\nSuccessfully downloaded and processed {len(downloaded)} real photographs!")
    return downloaded

if __name__ == "__main__":
    download_and_verify()
