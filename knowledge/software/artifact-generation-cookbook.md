# Artifact Generation Cookbook — File Output Templates

Versi: 1.0
Created: 2026-05-17
Owner: NexusAI (technical) + cross-company (template usage)
Source: Adapted from SUPERAGENT v2 m8.md

---

## Purpose

Reference cookbook untuk render output ke berbagai format file.
Reusable saat ada client work, external delivery, atau Fathur butuh artifact konkret.

---

## Render Targets

| Format | Use Case | Method | Library |
|--------|----------|--------|---------|
| `.md` | Specs, reports, prompts | Direct emit | none |
| `.docx` | Proposals, contracts, briefs | python-docx | `pip install python-docx` |
| `.xlsx` | Trackers, models, budgets | openpyxl | `pip install openpyxl` |
| `.pptx` | Decks, pitches | python-pptx | `pip install python-pptx` |
| `.pdf` | Final delivery, invoices | reportlab | `pip install reportlab` |
| `.json/.yaml` | Config, schemas | Direct emit | yaml: `pip install pyyaml` |
| `.py/.js/.sh` | Executable scripts | Direct emit | none |

---

## Templates Struktural

### A. Proposal (Client / Pitch)

```
1. Summary             — 1 paragraph, what + why now
2. Problem             — 1-2 paragraphs articulating friction
3. Solution            — 2-3 paragraphs, our approach
4. Timeline            — phases + dates
5. Investment          — pricing tiers (3 tiers usually)
6. Proof               — testimonials / case studies / metrics
7. Next step           — single specific action
```

### B. Technical Spec

```
# [ID] — [name]
## Capabilities
## Requirements
## Setup
## Usage
## Reference
```

### C. Insight Report

```
1. Executive summary   — 1 paragraph
2. Method              — how data was gathered
3. Findings            — patterns + facts
4. Analysis            — what it means
5. Prescriptions       — exactly 3 (per data-analysis-protocol)
6. Appendix            — sources, methodology details
```

---

## Quick Render Examples

### DOCX — Proposal (python-docx)

```python
from docx import Document
from docx.shared import Pt, Inches

doc = Document()
doc.add_heading('Proposal: <Client Name>', 0)

doc.add_heading('Summary', level=1)
doc.add_paragraph('We propose...')

doc.add_heading('Investment', level=1)
table = doc.add_table(rows=4, cols=3)
table.style = 'Light Grid'
table.cell(0, 0).text = 'Tier'
table.cell(0, 1).text = 'Includes'
table.cell(0, 2).text = 'Investment'
# ... fill rows ...

doc.save('proposal-clientname-2026-05-17.docx')
print("✅ proposal saved")
```

### XLSX — Multi-Sheet Tracker (openpyxl)

```python
import pandas as pd

summary_df = pd.DataFrame({...})
detail_df = pd.DataFrame({...})

with pd.ExcelWriter('tracker.xlsx', engine='openpyxl') as w:
    summary_df.to_excel(w, sheet_name='Summary', index=False)
    detail_df.to_excel(w, sheet_name='Detail', index=False)

print("✅ tracker.xlsx saved")
```

### PDF — Simple Invoice (reportlab)

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas('invoice-001.pdf', pagesize=A4)
c.setFont('Helvetica-Bold', 16)
c.drawString(50, 800, 'INVOICE')
c.setFont('Helvetica', 11)
c.drawString(50, 770, 'To: <Client>')
c.drawString(50, 750, 'Date: 2026-05-17')
c.drawString(50, 720, 'Total: IDR <amount>')
c.save()

print("✅ invoice saved")
```

### PPTX — Pitch Deck (python-pptx)

```python
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])  # title slide
slide.shapes.title.text = '<Project Name>'
slide.placeholders[1].text = '<Tagline>'

slide2 = prs.slides.add_slide(prs.slide_layouts[1])  # title + content
slide2.shapes.title.text = 'The Problem'
slide2.placeholders[1].text = '...'

prs.save('deck-2026-05-17.pptx')
print("✅ deck saved")
```

---

## Render Protocol

1. Confirm scope (max 1 clarifying exchange)
2. Generate artifact (actual file, not preview)
3. Save to descriptive path: `<context>-<topic>-<YYYY-MM-DD>.<ext>`
4. Deliver path/link
5. Offer one specific next edit

**Rules:**
- Filename descriptif: `q3-analysis.xlsx` BUKAN `output.xlsx`
- Always actual file, never inline-only
- Always offer next edit option

---

## Naming Convention

```
<context>-<topic>-<date>.<ext>

Examples:
  brandflow-weekly-recap-2026-05-17.docx
  crypto-research-FL-2026-05-17-001.pdf
  nexusai-spec-dashboard-2026-05-17.md
  proposal-newclient-2026-05-17.docx
```

---

## Output Path Convention

| Type | Path |
|------|------|
| Company internal artifact | `companies/<company>/tasks/<filename>` |
| Cross-company deliverable | `tests/integration/<filename>` or `memory/global-<date>.md` |
| Client deliverable (post-approval) | `companies/<company>/clients/<client>/<filename>` |

---

## Boundary #4 Awareness

- Internal artifact (Fathur reads) → Tier 1, generate freely
- External delivery (client/public) → Tier 3, butuh Fathur approval sebelum kirim
- Disclaimer wajib di artifact financial (lihat `companies/crypto-consultant/skills/reporting/SKILL.md`)

---

## Reference

- Source: `update/v2/openclaw/skills/m8.md`
- Used by: All companies (artifact delivery)
