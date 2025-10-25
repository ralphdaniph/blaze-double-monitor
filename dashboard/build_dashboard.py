import os, pandas as pd
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA = os.path.join(ROOT, "data", "rolling_350.csv")
OUT = os.path.join(ROOT, "dashboard", "dashboard.html")

os.makedirs(os.path.dirname(OUT), exist_ok=True)

if os.path.exists(DATA):
    df = pd.read_csv(DATA)
else:
    df = pd.DataFrame(columns=["datahora","numero","cor"])

total = len(df)
reds = int((df["cor"] == "red").sum()) if total else 0
blacks = int((df["cor"] == "black").sum()) if total else 0
whites = int((df["cor"] == "white").sum()) if total else 0
updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

rows = df.tail(50).to_dict(orient="records")
tbody = "".join(
    f"<tr><td>{r.get('datahora','')}</td><td>{r.get('numero','')}</td><td>{r.get('cor','')}</td></tr>"
    for r in rows
)

html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Beco • Dashboard</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;background:#0b0f14;color:#e7eaf0;margin:24px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:16px 0}}
.card{{background:#111827;border:1px solid #1f2937;border-radius:12px;padding:16px}}
h1{{margin:0 0 8px 0}} h2{{margin:6px 0 0 0}}
table{{width:100%;border-collapse:collapse;margin-top:12px}}
th,td{{border-bottom:1px solid #1f2937;padding:8px 10px;text-align:left}}
.pill{{display:inline-block;padding:2px 8px;border-radius:999px;background:#1f2937}}
.red{{color:#f87171}} .black{{color:#93c5fd}} .white{{color:#e5e7eb}}
</style></head>
<body>
<h1>Beco • Dashboard</h1>
<p>Atualizado: {updated}</p>
<div class="grid">
  <div class="card"><div>Total</div><h2>{total}</h2></div>
  <div class="card"><div>Vermelhos</div><h2 class="red">{reds}</h2></div>
  <div class="card"><div>Pretos</div><h2 class="black">{blacks}</h2></div>
  <div class="card"><div>Brancos</div><h2 class="white">{whites}</h2></div>
</div>
<div class="card">
  <h3>Últimos 50 giros</h3>
  <table>
    <thead><tr><th>Quando</th><th>Número</th><th>Cor</th></tr></thead>
    <tbody>{tbody}</tbody>
  </table>
</div>
</body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("OK:", OUT)
