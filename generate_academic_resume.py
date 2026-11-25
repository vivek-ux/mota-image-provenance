import sys
sys.path.insert(0, '/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/py_modules')
import fitz

def generate_academic_pdf():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        font-family: 'Times New Roman', Times, serif;
        font-size: 8.8pt;
        line-height: 1.18;
        color: #111;
        margin: 0;
        padding: 0;
    }
    .header {
        text-align: center;
        margin-bottom: 4pt;
    }
    .name {
        font-size: 16.5pt;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5pt;
    }
    .sub-title {
        font-size: 9pt;
        font-weight: bold;
        color: #222;
        margin-top: 1pt;
    }
    .contact {
        font-size: 8pt;
        margin-top: 2pt;
    }
    a {
        color: #111;
        text-decoration: underline;
    }
    .section-title {
        font-size: 9.5pt;
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 0.75pt solid #222;
        margin-top: 3.5pt;
        margin-bottom: 2pt;
        padding-bottom: 1pt;
        letter-spacing: 0.3pt;
    }
    table.item-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1.5pt;
        margin-bottom: 1pt;
    }
    table.item-table td {
        padding: 0;
        vertical-align: top;
    }
    .title-left {
        font-weight: bold;
        font-size: 8.8pt;
    }
    .title-right {
        text-align: right;
        font-size: 8.4pt;
        font-style: italic;
    }
    .sub-left {
        font-style: italic;
        font-size: 8.4pt;
    }
    .sub-right {
        text-align: right;
        font-size: 8.2pt;
        font-style: italic;
    }
    ul {
        margin: 1pt 0 2pt 12pt;
        padding: 0;
    }
    li {
        margin-bottom: 1pt;
        font-size: 8.4pt;
        line-height: 1.16;
    }
    .skills-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1pt;
    }
    .skills-table td {
        padding: 0.5pt 0;
        font-size: 8.4pt;
        vertical-align: top;
    }
    .skill-label {
        font-weight: bold;
        white-space: nowrap;
        width: 22%;
    }
    </style>
    </head>
    <body>

    <div class="header">
        <div class="name">Vivek Negi</div>
        <div class="sub-title">Candidate for Assistant Professor — Computer Science &amp; Engineering</div>
        <div class="contact">
            Dehradun, Uttarakhand &nbsp;|&nbsp; +91-8077481802 &nbsp;|&nbsp; 
            <a href="mailto:viveknegi177@gmail.com">viveknegi177@gmail.com</a> &nbsp;|&nbsp; 
            <a href="https://linkedin.com/in/vivek-negi-b46070222">linkedin.com/in/vivek-negi</a> &nbsp;|&nbsp; 
            <a href="https://github.com/vivek-ux">github.com/vivek-ux</a>
        </div>
    </div>

    <div class="section-title">Academic &amp; Professional Summary</div>
    <div style="font-size: 8.4pt; line-height: 1.18; margin-bottom: 2pt;">
    Computer Science scholar pursuing <b>M.Tech in CSE at NIT Meghalaya</b> with <b>nearly 2 years of enterprise software engineering experience at HSBC Technology India</b>. Strong pedagogical and theoretical foundation in Core CS (Data Structures &amp; Algorithms, Database Management Systems, Operating Systems, Computer Networks) coupled with active research in Deep Learning and Computer Vision. Proven record of disciplined academic leadership, analytical problem-solving (<b>GATE Qualified, 270+ LeetCode problems</b>), and situational character (<b>Indian Air Force SSB Recommended</b>).
    </div>

    <div class="section-title">Education</div>
    <table class="item-table">
        <tr>
            <td class="title-left">National Institute of Technology Meghalaya <span style="font-weight: normal; font-size: 8pt;">(Institute of National Importance)</span></td>
            <td class="title-right">Sohra, India</td>
        </tr>
        <tr>
            <td class="sub-left">Master of Technology (M.Tech) in Computer Science and Engineering</td>
            <td class="sub-right">Expected 2027</td>
        </tr>
    </table>
    <div style="font-size: 8pt; margin-left: 2pt; margin-bottom: 1.5pt; color: #333;">
        &bull; <i>Focus Areas:</i> Deep Learning, Computer Vision Provenance, Advanced Algorithms, Distributed Database Systems.
    </div>

    <table class="item-table">
        <tr>
            <td class="title-left">Graphic Era University</td>
            <td class="title-right">Dehradun, India</td>
        </tr>
        <tr>
            <td class="sub-left">Bachelor of Technology (B.Tech) in Computer Science and Engineering</td>
            <td class="sub-right">2023</td>
        </tr>
    </table>

    <div class="section-title">Teaching &amp; Research Competencies</div>
    <table class="skills-table">
        <tr>
            <td class="skill-label">Core Teaching Areas:</td>
            <td>Data Structures &amp; Algorithms, Database Management Systems (SQL), Operating Systems, Computer Networks, Object-Oriented Programming (Java/C++), Software Engineering</td>
        </tr>
        <tr>
            <td class="skill-label">Research Specializations:</td>
            <td>Computer Vision, Deep Learning, Image Provenance &amp; Media Lineage, Contrastive Learning, Distributed Ledgers</td>
        </tr>
        <tr>
            <td class="skill-label">Programming &amp; Tools:</td>
            <td>Java 17, Python, C++, SQL, PyTorch, Google BigQuery, PostgreSQL, Docker, Git, Linux</td>
        </tr>
    </table>

    <div class="section-title">Master's Thesis Research</div>
    <table class="item-table">
        <tr>
            <td class="title-left">Multi-Source Media Lineage Retrieval with Dynamic Alignment &amp; Gating</td>
            <td class="title-right">NIT Meghalaya</td>
        </tr>
        <tr>
            <td class="sub-left">Advisor: Dr. Akhilendra Pratap Singh, Department of Computer Science &amp; Engineering</td>
            <td class="sub-right">2025 &ndash; 2027</td>
        </tr>
    </table>
    <ul>
        <li>Formulated an end-to-end visual provenance framework to track spliced composite media against 1,000+ gallery images on MS-COCO, presenting findings with high faculty commendation for commercialization.</li>
        <li>Engineered a 3-tier Dynamic Slicing hierarchy (Global, Anchor, and Overlapping Slices) overcoming spatial fragmentation pitfalls of rigid grids, increasing Recall@5 from 53.3% to 75.5%.</li>
        <li>Designed a 2-layer MLP Importance Gating network using Contrastive Margin Loss to suppress background distractors, boosting full lineage retrieval accuracy to <b>88.89% Recall@5</b> (+37.8% over baseline).</li>
        <li>Developed batched GPU tensor extraction in PyTorch with L2-normalized 512-D descriptors, reducing gallery indexing latency from 28 minutes to under <b>45 seconds</b>.</li>
    </ul>

    <div class="section-title">Industry Engineering Experience</div>
    <table class="item-table">
        <tr>
            <td class="title-left">HSBC Technology India</td>
            <td class="title-right">Pune, Maharashtra</td>
        </tr>
        <tr>
            <td class="sub-left">Software Engineer &mdash; Production Systems &amp; Reliability</td>
            <td class="sub-right">Aug 2023 &ndash; Jun 2025</td>
        </tr>
    </table>
    <ul>
        <li>Engineered and monitored enterprise end-of-day (EOD) financial batch processing pipelines across multi-node GCP clusters, ensuring strict SLA adherence for downstream settlement ledgers.</li>
        <li>Profiled and optimized complex SQL and Google BigQuery queries, eliminating indexing bottlenecks and reducing runtimes across multi-million row financial transaction datasets.</li>
        <li>Diagnosed critical L2/L3 production incidents via centralized log telemetry; authored detailed Root-Cause Analysis (RCA) documents and guided junior associates through resolution workflows.</li>
        <li>Automated pipeline recovery workflows and data ingestion jobs using GCP Cloud Scheduler, maintaining 99.9% processing uptime.</li>
    </ul>

    <div class="section-title">Academic &amp; Technical Projects</div>
    <table class="item-table">
        <tr>
            <td class="title-left">Distributed Fintech Wallet &amp; Concurrency Engine <span style="font-weight: normal; font-size: 8pt; color: #444;">| Java 17, Spring Boot, PostgreSQL, Redis</span></td>
            <td class="title-right"></td>
        </tr>
    </table>
    <ul>
        <li>Implemented high-concurrency ledger service modeling distributed transaction boundaries, pessimistic row-level locking (<code>SELECT ... FOR UPDATE</code>), and idempotency keys to prevent double-spending in financial systems.</li>
        <li>Constructed educational lab demonstrations for ACID transaction rollbacks, race conditions, and outbox event streaming patterns.</li>
    </ul>

    <div class="section-title">Honors &amp; Key Achievements</div>
    <ul>
        <li><b>Graduate Aptitude Test in Engineering (GATE):</b> Qualified in Computer Science &amp; Information Technology.</li>
        <li><b>Indian Air Force SSB Recommendation:</b> Recommended for Flying Officer position by Air Force Selection Board (<b>AFSB Varanasi</b>) for AFCAT 1, 2024 (top ~1% selection rate across 5-day psychological, situational, and leadership evaluations).</li>
        <li><b>Algorithmic Discipline:</b> Solved <b>270+ problems on LeetCode</b> across Data Structures, Dynamic Programming, and Concurrency.</li>
    </ul>

    </body>
    </html>
    """

    mediabox = fitz.Rect(0, 0, 612, 792) # Letter
    rect = fitz.Rect(26, 22, 612-26, 792-22) # Margins

    def rectfn(rect_num, filled):
        return mediabox, rect, fitz.Identity

    story = fitz.Story(html)
    doc = story.write_with_links(rectfn)
    print(f"Generated Academic PDF with {len(doc)} pages.")
    output_path = '/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/vivek_negi_academic_resume.pdf'
    doc.save(output_path)
    return len(doc)

generate_academic_pdf()
