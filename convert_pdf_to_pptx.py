import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py_modules'))
import fitz  # PyMuPDF
from pptx import Presentation
from pptx.util import Inches

def pdf_to_pptx():
    pdf_path = "/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/thesis_compiled.pdf"
    out_pptx = "/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/Multi_Source_Media_Lineage_Exact_NITM.pptx"
    
    doc = fitz.open(pdf_path)
    prs = Presentation()
    
    # 4:3 Beamer ratio (10 inches x 7.5 inches = 4:3)
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    img_dir = "/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/slide_images"
    os.makedirs(img_dir, exist_ok=True)
    
    for i, page in enumerate(doc):
        # Render page at 4x resolution (approx 300 DPI) for ultra-sharp text and graphics
        zoom = 4.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        img_path = os.path.join(img_dir, f"slide_{i+1}.png")
        pix.save(img_path)
        
        # Add slide
        slide = prs.slides.add_slide(blank_layout)
        # Add full-bleed image covering the entire slide
        slide.shapes.add_picture(img_path, Inches(0), Inches(0), width=Inches(10), height=Inches(7.5))
        print(f"Added slide {i+1}/15")
        
    prs.save(out_pptx)
    print(f"[SUCCESS] Exact Beamer-to-PPTX created: {out_pptx}")

if __name__ == "__main__":
    pdf_to_pptx()
