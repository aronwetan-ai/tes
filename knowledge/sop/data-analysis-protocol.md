# Data Analysis Protocol — SCOPE→PRESCRIBE Flow

Versi: 1.0
Created: 2026-05-17
Owner: `@brandflow.analytics` + `@crypto.data` + Operator
Source: Adapted from SUPERAGENT v2 m5.md

---

## Purpose

6-step protocol untuk transform raw data → actionable prescription.
Reusable cross-company. Setiap analysis output WAJIB akhiri dengan exactly 3 prescriptions.

---

## When To Use

- BrandFlow analytics weekly review (engagement metrics, content performance)
- Crypto Consultant data work (`@crypto.data` aggregations)
- Cross-company performance reporting (weekly recap data)
- Any "analyze this CSV/spreadsheet/log" request

NOT untuk:
- Crypto research synthesis (sudah ada 6-layer format)
- Real-time monitoring alerts (sudah ada threshold triggers)

---

## The 6 Steps

### Step 1 — SCOPE

```
Pertanyaan exact yang dijawab:
  → "What's the engagement rate trend WoW for crypto-influencer client?"
  → BUKAN: "Analyze the data"

Output: 1 sentence question.
```

Salah scope = analysis useless.

---

### Step 2 — ACQUIRE

```
Required inputs:    [list]
Available inputs:   [list]
Gap:                [missing data + plan to fill or work-around]
```

Identify gap dulu. Don't proceed dengan asumsi.

---

### Step 3 — NORMALIZE

```
Steps:
- Deduplicate
- Reformat (consistent units, datetime, currency)
- Handle nulls (drop / impute / flag)
- Outlier handling (cap / remove / investigate)
```

Show work. Reproducibility matters.

---

### Step 4 — PROCESS

```
Patterns:    [trend, seasonality, correlation]
Anomalies:   [outliers, breaks]
Segments:    [groupby analysis]
Deltas:      [period-over-period change %]
```

**Rule:** Always include delta/trend. Snapshot alone is insufficient.

---

### Step 5 — RENDER

```
Visualization:  chart / table / sparkline (per appropriate)
Summary:       narrative paragraph (3-5 sentences)
Output file:   actual artifact (CSV/XLSX/MD), not inline preview
Path:          companies/<company>/tasks/analysis-YYYY-MM-DD.<ext>
```

Reference template (Python/pandas):

```python
import pandas as pd

df = pd.read_csv('input.csv')
print(df.describe(), df.isnull().sum())

# Aggregate per segment
out = df.groupby('segment')['value'].agg(
    total='sum',
    avg='mean',
    n='count',
)

# Multi-sheet output
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as w:
    out.to_excel(w, sheet_name='Summary')
    df.to_excel(w, sheet_name='Source', index=False)

print("✅ output.xlsx ready")
```

---

### Step 6 — PRESCRIBE

**Always exactly 3 prescriptions.** Specific, executable, owned.

```
[PRESCRIPTION 1]
  What:   <action>
  Owner:  <agent>
  When:   <by date>
  Expected impact: <metric → target>

[PRESCRIPTION 2] ...
[PRESCRIPTION 3] ...
```

3 = enough untuk prioritization, tidak overwhelming.

---

## Performance Indicators (Quick Reference)

```
throughput:   total + period-over-period delta %
activity:     active + new + lapsed units
efficiency:   input → qualified → converted %
acquisition:  cost per new unit
retention:    lifetime yield per unit
return:       output / input ratio %
```

Pick 3-5 yang relevan untuk question. Don't dump all 6.

---

## Output Format

```
[ANALYSIS — YYYY-MM-DD]
Question: <1 sentence>
Period:   <date range>
Source:   <data origin>

[KEY FACTS]
- <data point + delta>
- <data point + delta>

[PATTERNS]
- <observation>

[ANOMALIES]
- <if any>

[3 PRESCRIPTIONS]
1. <action> — owner — by date — impact
2. <action> — owner — by date — impact
3. <action> — owner — by date — impact

[ARTIFACT]
Path: <output file>

[CAVEATS]
- <data limitations>
- <interpretation caveats>
```

---

## Boundary #4 Awareness

Kalau analysis hasilnya akan dipublish/share keluar:
- Tier 3 → butuh Fathur approval
- Tetap perlu disclaimer kalau data finansial

---

## Reference

- Source: `update/v2/openclaw/skills/m5.md`
- Used by: `@brandflow.analytics`, `@crypto.data`
