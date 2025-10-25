import asyncio
from dataclasses import dataclass
import yaml
from playwright.async_api import async_playwright
from datetime import datetime
import csv
import os

# ===================== Configuração =====================
@dataclass
class Config:
    site_url: str
    poll_interval: float = 0.6

# ===================== Funções de utilidade =====================
def salvar_resultado(numero, cor):
    os.makedirs("data", exist_ok=True)
    path = "data/rolling_350.csv"
    novo = {"datahora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "numero": numero, "cor": cor}

    existe = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["datahora", "numero", "cor"])
        if not existe:
            w.writeheader()
        w.writerow(novo)
    print(f"[{novo['datahora']}] {cor.upper()} - {numero}")

# ===================== Monitor Blaze =====================
async def monitor(cfg: Config):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(cfg.site_url)
        print("Monitorando resultados em tempo real...\n")

        vistos = set()

        while True:
            try:
                itens = await page.query_selector_all("div.entries div.entry")
                resultados = []
                for item in itens:
                    texto = (await item.inner_text()).strip()
                    cor = "black" if "preto" in texto.lower() else "red" if "vermelho" in texto.lower() else "white"
                    numero = "".join([c for c in texto if c.isdigit()])
                    if numero:
                        resultados.append((numero, cor))
                if resultados:
                    ultimo = resultados[0]
                    if ultimo not in vistos:
                        vistos.add(ultimo)
                        salvar_resultado(ultimo[0], ultimo[1])
                await asyncio.sleep(cfg.poll_interval)
            except Exception as e:
                print("Erro:", e)
                await asyncio.sleep(3)

# ===================== Execução =====================
if __name__ == "__main__":
    cfg = Config(site_url="https://blaze.bet.br/pt/games/double")
    try:
        asyncio.run(monitor(cfg))
    except KeyboardInterrupt:
        print("Encerrando monitoramento.")
