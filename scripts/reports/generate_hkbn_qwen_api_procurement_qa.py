from pathlib import Path
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/reports/hkbn-qwen-model-api-procurement-vendor-qa.docx"
OUT.parent.mkdir(parents=True, exist_ok=True)

GREEN = "006A63"
GREEN_DARK = "003531"
ORANGE_DARK = "B15315"
TEXT = "333333"
MUTED = "6C757D"
WHITE = "FFFFFF"
SUBTLE = "F7F7F7"
PALE_GREEN = "E7F3F1"
PALE_ORANGE = "FFF2EA"


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    node = tc_pr.find(qn("w:shd"))
    if node is None:
        node = OxmlElement("w:shd")
        tc_pr.append(node)
    node.set(qn("w:val"), "clear")
    node.set(qn("w:fill"), fill)


def margins(cell, top=65, start=100, bottom=65, end=100):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.find(qn("w:tcMar"))
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        el = tc_mar.find(qn(f"w:{side}"))
        if el is None:
            el = OxmlElement(f"w:{side}")
            tc_mar.append(el)
        el.set(qn("w:w"), str(value))
        el.set(qn("w:type"), "dxa")


def repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    node = OxmlElement("w:tblHeader")
    node.set(qn("w:val"), "true")
    tr_pr.append(node)


def set_cell(cell, value, *, bold=False, color=TEXT, fill=None, size=8.5):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.02
    r = p.add_run(str(value))
    r.font.name = "Arial"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor.from_string(color)
    if fill:
        shade(cell, fill)
    margins(cell)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP


def table(headers, rows, widths, size=8.2):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    repeat_header(t.rows[0])
    for i, header in enumerate(headers):
        set_cell(t.rows[0].cells[i], header, bold=True, color=WHITE, fill=GREEN_DARK, size=size)
        t.rows[0].cells[i].width = Cm(widths[i])
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        fill = WHITE if ri % 2 == 0 else SUBTLE
        for i, value in enumerate(row):
            set_cell(cells[i], value, bold=(i == 0), fill=fill, size=size)
            cells[i].width = Cm(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def heading(text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(8 if level == 1 else 5)
    p.paragraph_format.space_after = Pt(4)
    return p


def body(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.08
    p.add_run(text)
    return p


def bullets(items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.add_run(item)


def callout(title, text, fill=PALE_GREEN, title_color=GREEN_DARK):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    cell = t.cell(0, 0)
    shade(cell, fill)
    margins(cell, 140, 170, 140, 170)
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(title + "\n")
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor.from_string(title_color)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor.from_string(TEXT)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Page ")
    run.font.name = "Arial"
    run.font.size = Pt(8)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    run._r.addnext(field)


def header_footer(section):
    hp = section.header.paragraphs[0]
    hp.text = "HKBN QWEN API · TECHNICAL SPECIFICATION & SLA · SHORT FORM"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.runs[0].font.name = "Arial"
    hp.runs[0].font.size = Pt(8)
    hp.runs[0].font.bold = True
    hp.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
    fp = section.footer.paragraphs[0]
    fp.text = ""
    add_page_number(fp)


def questions(prefix, items):
    return [(f"{prefix}.{i}", q, "Supplier to complete") for i, q in enumerate(items, 1)]


doc = Document()
section = doc.sections[0]
section.top_margin = Cm(1.5)
section.bottom_margin = Cm(1.5)
section.left_margin = Cm(1.6)
section.right_margin = Cm(1.6)
header_footer(section)

styles = doc.styles
normal_font = getattr(styles["Normal"], "font")
normal_font.name = "Arial"
normal_font.size = Pt(9.5)
normal_font.color.rgb = RGBColor.from_string(TEXT)
title_font = getattr(styles["Title"], "font")
title_font.name = "Arial"
title_font.size = Pt(27)
title_font.bold = True
title_font.color.rgb = RGBColor.from_string(GREEN_DARK)
for name, size, color in (("Heading 1", 17, GREEN_DARK), ("Heading 2", 12.5, GREEN), ("Heading 3", 10.5, ORANGE_DARK)):
    font = getattr(styles[name], "font")
    font.name = "Arial"
    font.size = Pt(size)
    font.bold = True
    font.color.rgb = RGBColor.from_string(color)

# Cover and request summary
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(44)
r = p.add_run("SHORT-FORM VENDOR QUESTIONNAIRE")
r.font.name = "Arial"
r.font.size = Pt(14)
r.font.bold = True
r.font.color.rgb = RGBColor.from_string(ORANGE_DARK)
p = doc.add_paragraph(style="Title")
p.add_run("HKBN Qwen API\nTechnical Specification & SLA Questions")
p = doc.add_paragraph()
r = p.add_run("Version 1.1 · Concise supplier response form")
r.font.name = "Arial"
r.font.size = Pt(12)
r.font.color.rgb = RGBColor.from_string(MUTED)
doc.add_paragraph()
callout(
    "What we need from HKBN",
    "Please provide one comparable technical specification for the exact Qwen endpoint being offered. A family name, headline maximum TPS or token price alone is not enough.",
)
heading("Terms used", 2)
table(
    ["Term", "Meaning"],
    [
        ("SLA", "Monthly uptime and service commitment"),
        ("P50 / P95 / P99", "Latency reached by 50%, 95% and 99% of requests"),
        ("TTFT", "Time to First Token"),
        ("TPS", "Output Tokens Per Second"),
        ("TPOT", "Time Per Output Token"),
    ],
    [4.0, 12.5],
    size=9,
)
heading("Response rule", 2)
bullets([
    "Answer against the exact production endpoint and model version offered.",
    "Provide measured P50 / P95 / P99 data with test conditions, not only theoretical maximums.",
    "State clearly when a feature or metric is not supported or not guaranteed.",
    "Attach a product specification, benchmark report or SLA reference where available.",
])

# 1 Model identity
doc.add_page_break()
heading("1. Exact Model Identity")
body("唔接受只回答「Qwen」。請列明實際checkpoint、版本及serving format。")
table(
    ["No.", "Question to HKBN / Supplier", "Supplier response / evidence"],
    questions("1", [
        "What is the exact API model ID and version?",
        "Is it Qwen3, Qwen3.5, 9B, 35B-A3B or another exact variant?",
        "Is it an official checkpoint, a quantized checkpoint or a supplier fine-tuned / modified model?",
        "What serving precision is used: BF16, FP8, INT8, INT4 or another format? Please include KV-cache precision where relevant.",
        "Is the model version fixed? How much advance notice is given before an upgrade or behaviour change?",
        "Can the customer pin a model version to prevent unplanned result changes?",
    ]),
    [1.3, 9.8, 5.9],
)
callout(
    "Minimum acceptable answer",
    "Exact model ID + checkpoint / revision + quantization / precision + deployed endpoint limit + version-change policy.",
    PALE_ORANGE,
    ORANGE_DARK,
)

# 2 shared/dedicated
heading("2. Shared or Dedicated Compute")
body("Core question: Is the endpoint running on dedicated compute for our tenant, or on a shared multi-tenant inference cluster?")
table(
    ["No.", "Question to HKBN / Supplier", "Supplier response / evidence"],
    questions("2", [
        "Is the service dedicated GPU, dedicated replica, reserved capacity, or only a separate API key on shared compute?",
        "How is noisy-neighbour impact controlled on a shared cluster?",
        "Is the stated TPS measured per request, per-tenant aggregate or whole-cluster aggregate?",
        "Are rate limits applied per user, API key, IP address, organization or a combination?",
        "Will requests queue or be throttled during peak hours? What HTTP status and retry guidance are returned?",
        "Is priority queueing or reserved capacity available?",
        "Is there a cold start? If so, what are typical and P95 scale-up times?",
        "What guaranteed and burst limits apply to concurrency, RPM and TPM?",
        "What is the minimum monthly commitment for a dedicated option?",
    ]),
    [1.3, 9.8, 5.9],
)
callout("Important", "A dedicated API key does not mean dedicated GPU capacity. The supplier should confirm the isolation and capacity model in writing.")

# 3 performance
heading("3. Performance and SLA Data")
body("唔接受只回答「最高100 TPS」。所有數據必須列明input/output length、concurrency、region、streaming mode及sample size。")
table(
    ["Metric", "Required supplier result", "Test condition / clarification"],
    [
        ("TTFT", "P50, P95 and P99", "Streaming; include queuing and cold starts"),
        ("Output speed", "P50 and P95 output tokens/sec; TPOT", "State whether per request or aggregate"),
        ("End-to-end latency", "P50, P95 and P99", "From request sent until complete response"),
        ("Throughput", "Requests/sec and tokens/sec", "At stated concurrency and prompt profile"),
        ("Concurrency", "Guaranteed and burst limits", "Per tenant / key / organization"),
        ("Error rate", "429 and 5xx rates", "Include retries and overload period"),
        ("Availability", "Monthly uptime SLA", "Include exclusions and service credits"),
    ],
    [4.0, 6.2, 6.8],
)
heading("Required test profiles", 2)
table(
    ["Profile", "Input", "Output", "Required results"],
    [
        ("A", "1K tokens", "512 tokens", "TTFT, TPS, TPOT, E2E P50/P95/P99"),
        ("B", "8K tokens", "1K tokens", "TTFT, TPS, TPOT, E2E P50/P95/P99"),
        ("C", "32K tokens", "2K tokens", "TTFT, TPS, TPOT, E2E P50/P95/P99"),
        ("D", "128K tokens", "2K tokens", "TTFT, TPS, TPOT, E2E P50/P95/P99"),
        ("E", "Maximum exposed context", "Declared output cap", "Same metrics plus error / truncation behaviour"),
    ],
    [2.3, 3.5, 3.5, 7.7],
)
heading("Test conditions to disclose", 2)
bullets([
    "Streaming and non-streaming results should be reported separately.",
    "State region, date, concurrency, sample size, warm / cold status and whether queuing time is included.",
    "State whether results are guaranteed SLA values, observed benchmark values or theoretical maximums.",
])

# 4 context
doc.add_page_break()
heading("4. Context Window")
body("Core question: What is the native context window of the exact checkpoint, and what maximum context does the deployed endpoint actually expose?")
table(
    ["No.", "Question to HKBN / Supplier", "Supplier response / evidence"],
    questions("4", [
        "What is the native context window of the exact upstream checkpoint?",
        "What is the deployed endpoint's default context limit?",
        "What is the maximum input-token limit?",
        "What is the maximum output-token limit?",
        "What is the combined input + output limit?",
        "When the limit is exceeded, does the endpoint reject, truncate or silently truncate? Provide the exact error or behaviour.",
        "Do system prompts, tool definitions, retrieved context and image tokens count toward the context limit?",
    ]),
    [1.3, 9.8, 5.9],
)
heading("Supplier summary", 2)
table(
    ["Item", "Supplier answer"],
    [
        ("Exact model ID / version", ""),
        ("Precision / quantization", ""),
        ("Shared or dedicated", ""),
        ("Guaranteed concurrency / RPM / TPM", ""),
        ("P95 TTFT — Profile A", ""),
        ("P95 output TPS — Profile A", ""),
        ("Monthly availability SLA", ""),
        ("Native context", ""),
        ("Endpoint maximum context", ""),
        ("Version pinning available", "Yes / No"),
    ],
    [8.0, 8.5],
)
callout(
    "Document scope",
    "This short form covers the requested technical specification and service-performance questions only. Commercial pricing, data security and legal terms can be handled separately if required.",
    PALE_ORANGE,
    ORANGE_DARK,
)

core = doc.core_properties
core.title = "HKBN Qwen API Technical Specification & SLA Questions — Short Form"
core.subject = "Concise vendor questionnaire for exact model, compute, performance and context limits"
core.author = "Internal AI Platform Team"
core.keywords = "HKBN, Qwen, API, TTFT, TPS, TPOT, P50, P95, P99, SLA"
core.comments = "Short-form supplier questionnaire; contains no credentials or production secrets."

doc.save(str(OUT))
print(OUT)
