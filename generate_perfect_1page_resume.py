import sys
sys.path.insert(0, '/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/py_modules')
import fitz
import shutil

def try_render(font_size=9.0, line_height=1.2, section_margin=4.0):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {{
        font-family: 'Times New Roman', Times, serif;
        font-size: {font_size}pt;
        line-height: {line_height};
        color: #111;
        margin: 0;
        padding: 0;
    }}
    .header {{
        text-align: center;
        margin-bottom: 4pt;
    }}
    .name {{
        font-size: 16pt;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5pt;
    }}
    .contact {{
        font-size: 8pt;
        margin-top: 2pt;
    }}
    a {{
        color: #111;
        text-decoration: underline;
    }}
    .section-title {{
        font-size: 9.5pt;
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 0.75pt solid #222;
        margin-top: {section_margin}pt;
        margin-bottom: 2pt;
        padding-bottom: 1pt;
        letter-spacing: 0.3pt;
    }}
    table.item-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 1.5pt;
        margin-bottom: 1pt;
    }}
    table.item-table td {{
        padding: 0;
        vertical-align: top;
    }}
    .title-left {{
        font-weight: bold;
        font-size: 8.8pt;
    }}
    .title-right {{
        text-align: right;
        font-size: 8.5pt;
        font-style: italic;
    }}
    .sub-left {{
        font-style: italic;
        font-size: 8.5pt;
    }}
    .sub-right {{
        text-align: right;
        font-size: 8.2pt;
        font-style: italic;
    }}
    ul {{
        margin: 1pt 0 2pt 12pt;
        padding: 0;
    }}
    li {{
        margin-bottom: 1pt;
        font-size: 8.5pt;
        line-height: 1.18;
    }}
    .skills-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 1pt;
    }}
    .skills-table td {{
        padding: 0.5pt 0;
        font-size: 8.5pt;
        vertical-align: top;
    }}
    .skill-label {{
        font-weight: bold;
        white-space: nowrap;
        width: 20%;
    }}
    </style>
    </head>
    <body>

    <div class="header">
        <div class="name">Vivek Negi</div>
        <div class="contact">
            Dehradun, Uttarakhand &nbsp;|&nbsp; +91-8077481802 &nbsp;|&nbsp; 
            <a href="mailto:viveknegi177@gmail.com">viveknegi177@gmail.com</a> &nbsp;|&nbsp; 
            <a href="https://linkedin.com/in/vivek-negi-b46070222">linkedin.com/in/vivek-negi</a> &nbsp;|&nbsp; 
            <a href="https://github.com/vivek-ux">github.com/vivek-ux</a>
        </div>
    </div>

    <div class="section-title">Professional Summary</div>
    <div style="font-size: 8.5pt; line-height: 1.2; margin-bottom: 2pt;">
    Software Engineer with nearly 2 years of enterprise systems engineering experience at <b>HSBC Technology India</b>, currently pursuing <b>M.Tech in CSE at NIT Meghalaya</b>. Strong hands-on expertise building concurrent, high-reliability Java 17 and Spring Boot microservices with Redis, PostgreSQL, and distributed transaction patterns, alongside research experience in GPU-accelerated deep learning pipelines. Solved <b>270+ LeetCode problems</b> with a proven track record of elite discipline and situational leadership (<b>Indian Air Force SSB Recommended</b>).
    </div>

    <div class="section-title">Technical Skills</div>
    <table class="skills-table">
        <tr>
            <td class="skill-label">Languages:</td>
            <td>Java 17, SQL, C++, Bash</td>
        </tr>
        <tr>
            <td class="skill-label">Backend &amp; Distributed:</td>
            <td>Spring Boot, Microservices, REST APIs, Redis (SETNX Idempotency &amp; Caching), Token Bucket Rate Limiting, Snowflake 64-Bit IDs, Pessimistic/Optimistic Locking, Transactional Outbox Pattern</td>
        </tr>
        <tr>
            <td class="skill-label">Databases &amp; Cloud:</td>
            <td>PostgreSQL, Google Cloud BigQuery, Google Cloud Platform (GCP), Cloud Scheduler</td>
        </tr>
        <tr>
            <td class="skill-label">AI / Deep Learning:</td>
            <td>PyTorch, TorchScript, CUDA/GPU Batching, Computer Vision (SSCD, Contrastive Learning)</td>
        </tr>
        <tr>
            <td class="skill-label">Tools &amp; Testing:</td>
            <td>Docker, Git, Maven, Postman, JUnit 5, Mockito, CI/CD Pipelines, Linux</td>
        </tr>
    </table>

    <div class="section-title">Professional Experience</div>
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
        <li>Engineered and maintained enterprise end-of-day (EOD) financial batch processing pipelines across multi-node GCP clusters, ensuring strict SLA adherence for downstream settlement ledgers.</li>
        <li>Profiled and optimized complex SQL and Google BigQuery queries, eliminating indexing bottlenecks and reducing runtimes across multi-million row financial transaction datasets.</li>
        <li>Diagnosed critical L2/L3 production incidents via centralized log telemetry; drove root-cause analysis (RCA) and partnered with development squads to validate and deploy zero-downtime hotfixes.</li>
        <li>Automated pipeline recovery workflows and data ingestion jobs using GCP Cloud Scheduler and BigQuery integrations, maintaining 99.9% processing uptime.</li>
    </ul>

    <div class="section-title">Projects</div>
    <table class="item-table">
        <tr>
            <td class="title-left">UltraScale FinCore &amp; Distributed Wallet Engine <span style="font-weight: normal; font-size: 8pt; color: #444;">| Java 17, Spring Boot, PostgreSQL, Redis, Docker</span></td>
            <td class="title-right"></td>
        </tr>
    </table>
    <ul>
        <li>Architected a high-concurrency financial transaction and booking engine handling peer-to-peer transfers, flash-sale inventory, and immutable ledgers with sub-5ms latency and zero over-selling across 100+ concurrent threads.</li>
        <li>Engineered a <b>64-bit Twitter Snowflake ID Generator</b> (41-bit timestamp, 5-bit datacenter, 5-bit worker, 12-bit sequence) generating <b>1.5M+ time-sorted unique IDs/sec</b> with NTP clock-drift protection and spin-wait handling.</li>
        <li>Built a non-blocking <b>Token Bucket Rate Limiter</b> to shed burst traffic (<code>HTTP 429</code>) and protect database connection pools, alongside a <b>Redis <code>SETNX</code> Idempotency Store</b> (24h TTL) preventing duplicate charges across network retries.</li>
        <li>Prevented race conditions using pluggable <b>Pessimistic (<code>SELECT ... FOR UPDATE</code>)</b> and <b>Optimistic CAS (<code>@Version</code>)</b> locking strategies coupled with a <b>Transactional Outbox Pattern</b> for guaranteed at-least-once event delivery.</li>
    </ul>

    <table class="item-table">
        <tr>
            <td class="title-left">ProvenanceAI: Multi-Source Media Lineage &amp; Blockchain Engine <span style="font-weight: normal; font-size: 8pt; color: #444;">| Deep Learning, ResNet-50/SSCD, SHA-256 Blockchain</span></td>
            <td class="title-right"></td>
        </tr>
    </table>
    <ul>
        <li>Developed a dual-channel visual attribution engine to trace both background scenes (Parent A) and spliced donor objects (Parent B) across a 1,000-image MS-COCO gallery and 300 composite queries on an NVIDIA Tesla T4 GPU.</li>
        <li>Engineered a Multi-Scale Dynamic Overlapping Slicer (50% stride) and a 2-layer MLP Importance Gate (&lt;70k params), boosting dual-parent retrieval accuracy from 44.44% to <b>88.89% Recall@5</b> (+44.45% over global SSCD).</li>
        <li>Integrated a <b>129-block SHA-256 Proof-of-Provenance Blockchain Ledger</b> to verify temporal creation precedence and a <b>2D FFT Spectral Filter</b> to detect synthetic latent diffusion inpainting in under 380ms.</li>
    </ul>

    <div class="section-title">Education</div>
    <table class="item-table">
        <tr>
            <td class="title-left">National Institute of Technology Meghalaya</td>
            <td class="title-right">Sohra, India</td>
        </tr>
        <tr>
            <td class="sub-left">Master of Technology (M.Tech) in Computer Science and Engineering</td>
            <td class="sub-right">Expected 2027</td>
        </tr>
    </table>
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

    <div class="section-title">Key Achievements</div>
    <ul>
        <li><b>Indian Air Force SSB Recommendation:</b> Recommended for Flying Officer position by Air Force Selection Board (<b>AFSB Varanasi</b>) for AFCAT 1, 2024 (top ~1% selection rate across 5-day psychological, situational, and leadership evaluations).</li>
        <li><b>Algorithmic Problem Solving:</b> Solved <b>270+ problems on LeetCode</b> spanning Data Structures, Dynamic Programming, Graphs, and Concurrency.</li>
    </ul>

    </body>
    </html>
    """

    mediabox = fitz.Rect(0, 0, 612, 792)
    rect = fitz.Rect(28, 24, 612-28, 792-24)

    def rectfn(rect_num, filled):
        return mediabox, rect, fitz.Identity

    story = fitz.Story(html)
    doc = story.write_with_links(rectfn)
    return doc

doc = try_render(font_size=8.8, line_height=1.17, section_margin=3.5)
print(f"Rendered: {len(doc)} pages")
doc.save('/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/vivek_negi_resume.pdf')
print("Saved to scratch directory.")
