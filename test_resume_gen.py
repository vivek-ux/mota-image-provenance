import sys
sys.path.insert(0, '/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/py_modules')
import fitz

html = """
<!DOCTYPE html>
<html>
<head>
<style>
@page {
    size: letter;
    margin: 0;
}
body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 9.5pt;
    line-height: 1.25;
    color: #111;
    margin: 0;
    padding: 0;
}
.header {
    text-align: center;
    margin-bottom: 6pt;
}
.name {
    font-size: 18pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
}
.contact {
    font-size: 8.5pt;
    margin-top: 2pt;
}
a {
    color: #111;
    text-decoration: underline;
}
.section-title {
    font-size: 10.5pt;
    font-weight: bold;
    text-transform: uppercase;
    border-bottom: 0.75pt solid #222;
    margin-top: 5pt;
    margin-bottom: 3pt;
    padding-bottom: 1pt;
    letter-spacing: 0.3pt;
}
.row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1pt;
}
table.item-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 2pt;
    margin-bottom: 1pt;
}
table.item-table td {
    padding: 0;
    vertical-align: top;
}
.title-left {
    font-weight: bold;
    font-size: 9.5pt;
}
.title-right {
    text-align: right;
    font-size: 9pt;
    font-style: italic;
}
.sub-left {
    font-style: italic;
    font-size: 9pt;
}
.sub-right {
    text-align: right;
    font-size: 8.5pt;
    font-style: italic;
}
ul {
    margin: 1pt 0 3pt 14pt;
    padding: 0;
}
li {
    margin-bottom: 1.5pt;
    font-size: 9pt;
    line-height: 1.22;
}
.skills-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 2pt;
}
.skills-table td {
    padding: 1pt 0;
    font-size: 9pt;
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
    <div class="contact">
        Dehradun, Uttarakhand &nbsp;|&nbsp; +91-8077481802 &nbsp;|&nbsp; 
        <a href="mailto:viveknegi177@gmail.com">viveknegi177@gmail.com</a> &nbsp;|&nbsp; 
        <a href="https://linkedin.com/in/vivek-negi-b46070222">linkedin.com/in/vivek-negi</a> &nbsp;|&nbsp; 
        <a href="https://github.com/vivek-ux">github.com/vivek-ux</a>
    </div>
</div>

<div class="section-title">Professional Summary</div>
<div style="font-size: 9pt; line-height: 1.25; margin-bottom: 3pt;">
Software Engineer with nearly 2 years of enterprise systems engineering experience at <b>HSBC Technology India</b>, currently pursuing <b>M.Tech in CSE at NIT Meghalaya</b>. Strong hands-on expertise building concurrent, high-reliability Java 17 and Spring Boot microservices with Redis, PostgreSQL, and distributed transaction patterns, alongside research experience in GPU-accelerated deep learning pipelines. Solved <b>270+ LeetCode problems</b> with a proven track record of elite discipline and situational leadership (<b>Indian Air Force SSB Recommended</b>).
</div>

<div class="section-title">Technical Skills</div>
<table class="skills-table">
    <tr>
        <td class="skill-label">Languages:</td>
        <td>Java 17, Python, SQL, C++, Bash</td>
    </tr>
    <tr>
        <td class="skill-label">Backend & Distributed:</td>
        <td>Spring Boot, Microservices, Spring Security, REST APIs, Redis Caching, Pessimistic Locking, Transactional Outbox Pattern, Event-Driven Architecture</td>
    </tr>
    <tr>
        <td class="skill-label">Databases & Cloud:</td>
        <td>PostgreSQL, Google Cloud BigQuery, Google Cloud Platform (GCP), Cloud Scheduler</td>
    </tr>
    <tr>
        <td class="skill-label">AI / Deep Learning:</td>
        <td>PyTorch, TorchScript, CUDA/GPU Batching, Computer Vision (SSCD, Contrastive Learning)</td>
    </tr>
    <tr>
        <td class="skill-label">Tools & Testing:</td>
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
        <td class="title-left">Distributed Fintech Wallet Service <span style="font-weight: normal; font-size: 8.5pt;">| Java 17, Spring Boot, PostgreSQL, Redis, Docker</span></td>
        <td class="title-right"></td>
    </tr>
</table>
<ul>
    <li>Architected a high-concurrency digital wallet service handling balance management, peer-to-peer transfers, and transaction ledgers with strict financial consistency guarantees.</li>
    <li>Prevented race conditions and double-spending under high concurrency using ordered pessimistic row-level locking (<code>SELECT ... FOR UPDATE</code>) within bounded <code>@Transactional</code> boundaries.</li>
    <li>Implemented distributed idempotency keys via Redis TTL, preventing duplicate payment submissions across transient client network retries.</li>
    <li>Engineered a database-backed Transactional Outbox Pattern with an asynchronous retry state worker to decouple event publishing from core transactions, eliminating dual-write inconsistencies.</li>
    <li>Developed comprehensive integration test suites using JUnit 5 and Mockito, thoroughly validating concurrent race conditions, transaction rollbacks, and idempotency states.</li>
</ul>

<table class="item-table">
    <tr>
        <td class="title-left">Multi-Source Image Lineage Retrieval Pipeline <span style="font-weight: normal; font-size: 8.5pt;">| PyTorch, Meta SSCD, TorchScript, CUDA</span></td>
        <td class="title-right"></td>
    </tr>
</table>
<ul>
    <li>Developed an end-to-end visual provenance retrieval pipeline to detect and trace spliced donor image components against a 1,000+ image candidate gallery on the MS-COCO dataset.</li>
    <li>Engineered a 3-tier Dynamic Slicing hierarchy (Global, Anchor, and Overlapping Slices) overcoming spatial fragmentation pitfalls of rigid grids, increasing Recall@5 from 53.3% to 75.5%.</li>
    <li>Designed a 2-layer MLP Importance Gating network using Contrastive Margin Loss to suppress background distractors, boosting full lineage retrieval accuracy to <b>88.89% Recall@5</b> (+37.8% over baseline).</li>
    <li>Implemented batched GPU tensor extraction in PyTorch with L2-normalized 512-D descriptors, slashing gallery indexing latency from 28 minutes to under <b>45 seconds</b>.</li>
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
<table class="item-table" style="margin-top: 2pt;">
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

mediabox = fitz.Rect(0, 0, 612, 792) # Letter
rect = fitz.Rect(32, 28, 612-32, 792-28) # 0.44 in left/right, 0.38 in top/bottom

def rectfn(rect_num, filled):
    return mediabox, rect, fitz.Identity

story = fitz.Story(html)
doc = story.write_with_links(rectfn)
print(f"Generated PDF with {len(doc)} pages.")
doc.save('/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/vivek_negi_resume.pdf')
