"""Gera dados fictícios de vendas e metas para uma empresa de eletrônicos.

O objetivo é fornecer uma base consistente para visualizações em BI/Streamlit.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

STATE_CONFIG = [
    {"uf": "SP", "regiao": "Sudeste", "cidades": ["São Paulo", "Campinas", "Santos", "São José dos Campos"], "peso": 0.26},
    {"uf": "RJ", "regiao": "Sudeste", "cidades": ["Rio de Janeiro", "Niterói", "Volta Redonda"], "peso": 0.14},
    {"uf": "MG", "regiao": "Sudeste", "cidades": ["Belo Horizonte", "Uberlândia", "Juiz de Fora"], "peso": 0.12},
    {"uf": "PR", "regiao": "Sul", "cidades": ["Curitiba", "Londrina", "Maringá"], "peso": 0.1},
    {"uf": "RS", "regiao": "Sul", "cidades": ["Porto Alegre", "Caxias do Sul", "Pelotas"], "peso": 0.09},
    {"uf": "SC", "regiao": "Sul", "cidades": ["Florianópolis", "Joinville", "Blumenau"], "peso": 0.08},
    {"uf": "BA", "regiao": "Nordeste", "cidades": ["Salvador", "Feira de Santana", "Vitória da Conquista"], "peso": 0.07},
    {"uf": "PE", "regiao": "Nordeste", "cidades": ["Recife", "Jaboatão", "Olinda"], "peso": 0.05},
    {"uf": "GO", "regiao": "Centro-Oeste", "cidades": ["Goiânia", "Anápolis", "Aparecida de Goiânia"], "peso": 0.05},
    {"uf": "DF", "regiao": "Centro-Oeste", "cidades": ["Brasília", "Taguatinga", "Ceilândia"], "peso": 0.04},
]

CHANNELS = [
    {"nome": "E-commerce", "peso": 0.45, "desconto_base": 0.08},
    {"nome": "Marketplace", "peso": 0.22, "desconto_base": 0.11},
    {"nome": "Loja Física", "peso": 0.2, "desconto_base": 0.05},
    {"nome": "Parceiros B2B", "peso": 0.13, "desconto_base": 0.03},
]

CATEGORIES = [
    {
        "nome": "Smartphones",
        "marcas": [
            {"nome": "Nova Mobile", "produtos": ["Nova One", "Nova Max", "Nova Air"], "preco_base": 2300},
            {"nome": "Apex", "produtos": ["Apex S10", "Apex S10 Pro", "Apex Neo"], "preco_base": 3100},
            {"nome": "Orion", "produtos": ["Orion Pulse", "Orion Horizon"], "preco_base": 2800},
        ],
    },
    {
        "nome": "TVs & Áudio",
        "marcas": [
            {"nome": "Lumina", "produtos": ["Lumina Vision 50", "Lumina Vision 65", "Lumina Soundbar"], "preco_base": 2400},
            {"nome": "Vertex", "produtos": ["Vertex OLED 55", "Vertex OLED 65", "Vertex Beam"], "preco_base": 3600},
        ],
    },
    {
        "nome": "Notebooks",
        "marcas": [
            {"nome": "Helix", "produtos": ["Helix Pro 14", "Helix Pro 16", "Helix Flex"], "preco_base": 4200},
            {"nome": "Nimbus", "produtos": ["Nimbus Air", "Nimbus Studio", "Nimbus Go"], "preco_base": 3800},
        ],
    },
    {
        "nome": "Acessórios",
        "marcas": [
            {"nome": "Pulse", "produtos": ["Pulse Buds", "Pulse ANC", "Pulse Fit"], "preco_base": 320},
            {"nome": "Volt", "produtos": ["Volt Charger", "Volt Power Hub", "Volt Cable Kit"], "preco_base": 180},
            {"nome": "Photon", "produtos": ["Photon Mouse", "Photon Keyboard"], "preco_base": 250},
        ],
    },
    {
        "nome": "Casa Inteligente",
        "marcas": [
            {"nome": "HomeX", "produtos": ["HomeX Hub", "HomeX Cam", "HomeX Sensor Pack"], "preco_base": 650},
            {"nome": "Nexa", "produtos": ["Nexa Lamp", "Nexa Plug", "Nexa Thermo"], "preco_base": 420},
        ],
    },
    {
        "nome": "Gaming & Consoles",
        "marcas": [
            {"nome": "Arcade", "produtos": ["Arcade One", "Arcade Elite"], "preco_base": 3200},
            {"nome": "Blitz", "produtos": ["Blitz Pad", "Blitz Headset", "Blitz Chair"], "preco_base": 900},
        ],
    },
]

SAZONALIDADE = {
    1: 0.88,
    2: 0.9,
    3: 1.0,
    4: 1.03,
    5: 1.07,
    6: 1.12,
    7: 1.08,
    8: 1.1,
    9: 1.18,
    10: 1.22,
    11: 1.3,
    12: 1.4,
}


def sample_dates(total: int, start_date: pd.Timestamp, end_date: pd.Timestamp) -> np.ndarray:
    dias = pd.date_range(start=start_date, end=end_date, freq="D")
    pesos = np.array([SAZONALIDADE[d.month] for d in dias], dtype=float)
    pesos = pesos / pesos.sum()
    return np.random.choice(dias, size=total, p=pesos)


def generate_sales(rows: int, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    datas = pd.to_datetime(sample_dates(rows, start_date, end_date))
    registros = []

    estado_pesos = [estado["peso"] for estado in STATE_CONFIG]
    canal_pesos = [canal["peso"] for canal in CHANNELS]

    for i, dt in enumerate(datas, start=1):
        dt = pd.Timestamp(dt)
        estado = random.choices(STATE_CONFIG, weights=estado_pesos, k=1)[0]
        canal = random.choices(CHANNELS, weights=canal_pesos, k=1)[0]
        categoria = random.choice(CATEGORIES)
        marca = random.choice(categoria["marcas"])
        produto = random.choice(marca["produtos"])

        preco_base = marca["preco_base"]
        preco = np.random.normal(loc=preco_base, scale=preco_base * 0.12)
        preco = max(preco, preco_base * 0.55)

        quantidade = int(
            np.random.choice(
                [1, 1, 1, 1, 2, 2, 3, 4, 5],
                p=[0.22, 0.2, 0.18, 0.15, 0.1, 0.08, 0.04, 0.02, 0.01],
            )
        )

        desconto = float(np.clip(np.random.normal(canal["desconto_base"], 0.03), 0, 0.3))
        bruto = preco * quantidade
        receita = bruto * (1 - desconto)

        custo_ratio_base = 0.58 if categoria["nome"] not in {"Acessórios", "Casa Inteligente"} else 0.5
        custo_ratio = float(np.clip(np.random.normal(custo_ratio_base, 0.05), 0.38, 0.8))
        custo = receita * custo_ratio
        lucro = receita - custo
        margem_pct = (lucro / receita * 100) if receita else 0

        registros.append(
            {
                "pedido_id": f"P{dt:%y%m}-{i:05d}",
                "data": dt.normalize(),
                "ano": dt.year,
                "mes": dt.month,
                "estado": estado["uf"],
                "regiao": estado["regiao"],
                "cidade": random.choice(estado["cidades"]),
                "canal": canal["nome"],
                "categoria": categoria["nome"],
                "marca": marca["nome"],
                "produto": produto,
                "preco_unitario": round(preco, 2),
                "quantidade": quantidade,
                "desconto": round(desconto, 3),
                "receita": round(receita, 2),
                "custo": round(custo, 2),
                "lucro": round(lucro, 2),
                "margem_pct": round(margem_pct, 2),
            }
        )

    df = pd.DataFrame(registros)
    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)
    df["trimestre"] = df["data"].dt.to_period("Q").astype(str)
    return df


def build_targets(sales_df: pd.DataFrame) -> pd.DataFrame:
    agrupado = sales_df.groupby(["ano_mes", "estado", "canal"], as_index=False).agg(
        faturamento=("receita", "sum"),
        pedidos=("pedido_id", "nunique"),
    )

    rng = np.random.default_rng(RANDOM_SEED + 7)
    fator_meta = rng.normal(loc=1.05, scale=0.07, size=len(agrupado))
    fator_ped = rng.normal(loc=1.03, scale=0.05, size=len(agrupado))

    agrupado["meta_faturamento"] = (agrupado["faturamento"] * fator_meta).round(2)
    agrupado["meta_pedidos"] = np.maximum(
        (agrupado["pedidos"] * fator_ped).round().astype(int), agrupado["pedidos"]
    )

    return agrupado[["ano_mes", "estado", "canal", "meta_faturamento", "meta_pedidos"]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera dados fictícios de vendas e metas.")
    parser.add_argument(
        "--records",
        type=int,
        default=8000,
        help="Quantidade de pedidos a gerar (padrão: 8000)",
    )
    parser.add_argument(
        "--start",
        type=str,
        default="2023-01-01",
        help="Data inicial no formato YYYY-MM-DD (padrão: 2023-01-01)",
    )
    parser.add_argument(
        "--end",
        type=str,
        default="2024-12-31",
        help="Data final no formato YYYY-MM-DD (padrão: 2024-12-31)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data"),
        help="Diretório de saída para os CSVs (padrão: data)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    start_date = pd.to_datetime(args.start)
    end_date = pd.to_datetime(args.end)

    if end_date < start_date:
        raise ValueError("A data final precisa ser maior ou igual à data inicial.")

    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)

    sales_df = generate_sales(args.records, start_date, end_date)
    targets_df = build_targets(sales_df)

    sales_path = output_dir / "sales_data.csv"
    targets_path = output_dir / "monthly_targets.csv"

    sales_df.to_csv(sales_path, index=False)
    targets_df.to_csv(targets_path, index=False)

    print(f"Foram gerados {len(sales_df):,} pedidos fictícios.".replace(",", "."))
    print(f"Dados salvos em: {sales_path}")
    print(f"Metas salvas em: {targets_path}")


if __name__ == "__main__":
    main()
