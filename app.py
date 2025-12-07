from __future__ import annotations

from pathlib import Path
import urllib.parse

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Painel de Vendas - Eletrônicos",
    page_icon="💡",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "sales_data.csv"
TARGETS_PATH = Path(__file__).parent / "data" / "monthly_targets.csv"
LOGO_PATH = Path(__file__).parent / "assets" / "logo.svg"

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root {
  --bg: #070d1b;
  --panel: rgba(15, 20, 38, 0.9);
  --card: rgba(20, 32, 58, 0.82);
  --accent: #f59e0b;
  --accent2: #0ea5e9;
  --text: #dce8ff;
  --muted: #9fb2d4;
}
html, body, [class*="stApp"] {
  font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
  background: radial-gradient(circle at 12% 20%, #1b2c5a 0, #0b1224 38%, #070d1b 75%);
  color: var(--text);
}
[data-testid="stHeader"] {background: linear-gradient(120deg, #0b1224 0%, rgba(11,18,36,0.55) 100%);} 
[data-testid="stSidebar"] {
  background: radial-gradient(circle at 20% 15%, rgba(14,165,233,0.22), rgba(14,165,233,0.08) 28%, rgba(7,13,27,0.95) 80%);
  border-right: 1px solid rgba(255,255,255,0.05);
  box-shadow: 12px 0 28px rgba(0,0,0,0.28);
}
[data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stMultiSelect, [data-testid="stSidebar"] .stDateInput {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 0.35rem 0.35rem 0.15rem;
}
.filter-card {background: linear-gradient(180deg, rgba(14,165,233,0.16), rgba(14,165,233,0.05)); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 0.8rem 0.9rem; margin-bottom: 0.6rem; box-shadow: 0 18px 30px rgba(0,0,0,0.24);}
.section-title {font-size: 1.1rem; letter-spacing: .5px; color: var(--muted); text-transform: uppercase;}
.metric-card {background: var(--card); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 0.9rem 1rem; box-shadow: 0 15px 40px rgba(0,0,0,0.25);}
[data-testid="stMetric"] {background: transparent; padding: 0;}
[data-testid="stMetric"] > div {width: 100%;}
.kpi-number {font-size: 1.8rem; font-weight: 700; color: #f8fafc;}
.stMetric-value {font-size: 2rem !important;}
.stMetric-label {font-size: 0.9rem !important; color: var(--muted) !important;}
[data-testid="stMetricValue"] {white-space: nowrap !important; overflow: visible !important; text-overflow: clip !important;}
.meta-card {background: linear-gradient(120deg, rgba(14,165,233,0.12), rgba(245,158,11,0.12)); border: 1px solid rgba(14,165,233,0.3); border-radius: 16px; padding: 1rem;}
.meta-row {display: flex; justify-content: space-between; align-items: center; font-weight: 600; color: var(--text);} 
.meta-row.muted {color: var(--muted); font-weight: 500;}
.meta-bar {width: 100%; height: 10px; background: rgba(255,255,255,0.08); border-radius: 999px; overflow: hidden; margin: 0.5rem 0;}
.meta-fill {height: 100%; background: linear-gradient(90deg, #0ea5e9, #f59e0b);}
.small-label {color: var(--muted); font-size: 0.9rem;}
.filter-summary {display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.4rem 0 0.8rem;}
.chip {background: linear-gradient(120deg, rgba(14,165,233,0.14), rgba(14,165,233,0.05)); border: 1px solid rgba(14,165,233,0.35); color: var(--text); padding: 0.32rem 0.65rem; border-radius: 999px; font-size: 0.9rem;}
.chip b {color: #f8fafc; margin-right: 0.25rem;}
</style>
"""


def fmt_currency(value: float) -> str:
    return f"R$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_percent(value: float) -> str:
    return f"{value:.1f}%"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    data = pd.read_csv(DATA_PATH, parse_dates=["data"])
    data["ano_mes"] = pd.PeriodIndex(data["data"], freq="M").astype(str)
    data["mes_ord"] = pd.PeriodIndex(data["data"], freq="M").to_timestamp()
    targets = pd.read_csv(TARGETS_PATH)
    return data, targets


def filter_data(df: pd.DataFrame, filtros: dict) -> pd.DataFrame:
    mask = (
        (df["data"].dt.date >= filtros["inicio"]) &
        (df["data"].dt.date <= filtros["fim"]) &
        (df["estado"].isin(filtros["estados"])) &
        (df["canal"].isin(filtros["canais"])) &
        (df["categoria"].isin(filtros["categorias"]))
    )
    return df.loc[mask].copy()


def monthly_meta_vs_real(filtered: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    real = (
        filtered.groupby("ano_mes", as_index=False)
        .agg(realizado=("receita", "sum"))
    )
    real["mes_ord"] = pd.PeriodIndex(real["ano_mes"], freq="M").to_timestamp()

    meta = (
        targets.groupby("ano_mes", as_index=False)
        .agg(meta=("meta_faturamento", "sum"))
    )
    meta["mes_ord"] = pd.PeriodIndex(meta["ano_mes"], freq="M").to_timestamp()

    combinado = pd.merge(meta, real, on=["ano_mes", "mes_ord"], how="outer").fillna(0)
    return combinado.sort_values("mes_ord")


def main() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if not DATA_PATH.exists() or not TARGETS_PATH.exists():
        st.error("Arquivos de dados não encontrados. Execute `python generate_data.py` para criar os CSVs.")
        st.stop()

    df, targets = load_data()

    min_date, max_date = df["data"].min().date(), df["data"].max().date()
    default_estados = sorted(df["estado"].unique())
    default_canais = sorted(df["canal"].unique())
    default_categorias = sorted(df["categoria"].unique())

    header_html = """
        <div style="display:flex; align-items:center; gap: 0.75rem; margin-bottom: 0.6rem;">
          <div style="width:14px; height:14px; border-radius:50%; background: linear-gradient(120deg, #0ea5e9, #f59e0b);"></div>
          <div style="font-size:1.35rem; font-weight:700; letter-spacing:0.4px; color:#e2e8f0;">Análise de performance</div>
        </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # inicializa estado dos filtros apenas uma vez para evitar conflito com widgets
    if "periodo" not in st.session_state:
        st.session_state["periodo"] = (min_date, max_date)
    if "estados_filter" not in st.session_state:
        st.session_state["estados_filter"] = default_estados
    if "canais_filter" not in st.session_state:
        st.session_state["canais_filter"] = default_canais
    if "categorias_filter" not in st.session_state:
        st.session_state["categorias_filter"] = default_categorias

    def reset_filters() -> None:
        st.session_state["periodo"] = (min_date, max_date)
        st.session_state["estados_filter"] = default_estados
        st.session_state["canais_filter"] = default_canais
        st.session_state["categorias_filter"] = default_categorias

    with st.sidebar:
        st.markdown(
            """
            <div class='filter-card'>
              <div class='section-title'>Painel de filtros</div>
              <div class='small-label'>Use os drop-downs para refinar visão</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if LOGO_PATH.exists():
            svg_content = LOGO_PATH.read_text(encoding="utf-8", errors="ignore")
            data_uri = "data:image/svg+xml;utf8," + urllib.parse.quote(svg_content)
            st.markdown(f"<img src='{data_uri}' style='width:100%;' />", unsafe_allow_html=True)
        with st.expander("Filtros", expanded=True):
            st.button("Limpar filtros", use_container_width=True, on_click=reset_filters)
            periodo = st.date_input(
                "Período",
                value=st.session_state["periodo"],
                min_value=min_date,
                max_value=max_date,
                key="periodo",
            )
            if isinstance(periodo, (list, tuple)) and len(periodo) == 2:
                inicio, fim = periodo
            else:
                inicio, fim = min_date, max_date

            estados = st.multiselect("Estados", default_estados, default=st.session_state["estados_filter"], key="estados_filter")
            canais = st.multiselect("Canais", default_canais, default=st.session_state["canais_filter"], key="canais_filter")
            categorias = st.multiselect("Categorias", default_categorias, default=st.session_state["categorias_filter"], key="categorias_filter")

    filtros = {
        "inicio": inicio,
        "fim": fim,
        "estados": estados or default_estados,
        "canais": canais or default_canais,
        "categorias": categorias or default_categorias,
    }

    filtrado = filter_data(df, filtros)

    if filtrado.empty:
        st.warning("Sem dados para os filtros selecionados.")
        st.stop()

    metas_filtradas = targets[
        targets["estado"].isin(filtros["estados"]) &
        targets["canal"].isin(filtros["canais"]) &
        targets["ano_mes"].isin(filtrado["ano_mes"].unique())
    ]

    chips = [
        ("Período", f"{inicio:%d/%m/%Y} - {fim:%d/%m/%Y}"),
        ("Estados", ", ".join(filtros["estados"])),
        ("Canais", ", ".join(filtros["canais"])),
        ("Categorias", ", ".join(filtros["categorias"])),
    ]
    chips_html = "".join([f"<span class='chip'><b>{label}:</b> {valor}</span>" for label, valor in chips])
    st.markdown(f"<div class='filter-summary'>{chips_html}</div>", unsafe_allow_html=True)

    receita_total = float(filtrado["receita"].sum())
    pedidos = int(filtrado["pedido_id"].nunique())
    ticket = receita_total / pedidos if pedidos else 0
    margem_pct = (float(filtrado["lucro"].sum()) / receita_total * 100) if receita_total else 0

    meta_total = float(metas_filtradas["meta_faturamento"].sum()) if not metas_filtradas.empty else 0
    meta_ped = int(metas_filtradas["meta_pedidos"].sum()) if not metas_filtradas.empty else 0
    progresso_meta = (receita_total / meta_total * 100) if meta_total else 0
    gap_meta = receita_total - meta_total

    st.markdown("<div class='section-title'>Performance consolidada</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1.3, 1, 1, 1])
    col1.metric("Faturamento", fmt_currency(receita_total), delta=f"{progresso_meta:.1f}% da meta")
    col2.metric("Pedidos", f"{pedidos:,}".replace(",", "."), delta=f"Meta: {meta_ped:,}".replace(",", "."))
    col3.metric("Ticket médio", fmt_currency(ticket))
    col4.metric("Margem", fmt_percent(margem_pct))

    st.markdown(
        f"""
        <div class='meta-card'>
          <div class='meta-row'>
            <span>Meta vs realizado</span>
            <span>{fmt_currency(meta_total)}</span>
          </div>
          <div class='meta-bar'>
            <div class='meta-fill' style='width:{min(progresso_meta, 180):.1f}%;'></div>
          </div>
          <div class='meta-row muted'>Gap: {fmt_currency(gap_meta)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)

    meta_real = monthly_meta_vs_real(filtrado, metas_filtradas)
    fig_meta = px.bar(
        meta_real,
        x="mes_ord",
        y=["meta", "realizado"],
        barmode="group",
        color_discrete_map={"meta": "#f59e0b", "realizado": "#0ea5e9"},
        labels={"value": "R$", "mes_ord": "Mês", "variable": ""},
        title="Meta vs. realizado por mês",
    )
    fig_meta.update_layout(margin=dict(l=0, r=0, t=40, b=30))

    canal = (
        filtrado.groupby("canal", as_index=False)
        .agg(receita=("receita", "sum"), pedidos=("pedido_id", "nunique"), margem=("lucro", "sum"))
    )
    canal["margem_pct"] = (canal["margem"] / canal["receita"] * 100).round(1)
    fig_canal = px.bar(
        canal.sort_values("receita"),
        x="receita",
        y="canal",
        orientation="h",
        color="margem_pct",
        color_continuous_scale=["#0ea5e9", "#14b8a6", "#f59e0b"],
        labels={"receita": "Receita", "canal": "Canal", "margem_pct": "Margem %"},
        title="Receita por canal",
    )
    fig_canal.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=50, b=10))

    categoria = (
        filtrado.groupby(["categoria", "marca"], as_index=False)
        .agg(receita=("receita", "sum"))
    )
    fig_categoria = px.treemap(
        categoria,
        path=["categoria", "marca"],
        values="receita",
        color="categoria",
        title="Mix por categoria e marca",
    )
    fig_categoria.update_layout(margin=dict(l=0, r=0, t=50, b=10))

    estados = (
        filtrado.groupby("estado", as_index=False)
        .agg(receita=("receita", "sum"), margem=("lucro", "sum"))
    )
    estados["margem_pct"] = (estados["margem"] / estados["receita"] * 100).round(1)
    fig_estado = px.bar(
        estados.sort_values("receita", ascending=False),
        x="estado",
        y="receita",
        color="margem_pct",
        color_continuous_scale=["#0ea5e9", "#22c55e", "#f59e0b"],
        labels={"estado": "UF", "receita": "Receita", "margem_pct": "Margem %"},
        title="Receita por estado",
    )
    fig_estado.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=50, b=10))

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(fig_meta, use_container_width=True)
        st.plotly_chart(fig_categoria, use_container_width=True)
    with col_b:
        st.plotly_chart(fig_canal, use_container_width=True)
        st.plotly_chart(fig_estado, use_container_width=True)

    base_prod = (
        filtrado.groupby(["produto", "marca", "categoria"], as_index=False)
        .agg(
            receita=("receita", "sum"),
            pedidos=("pedido_id", "nunique"),
            ticket=("receita", "mean"),
        )
    )

    prod_ec = (
        filtrado.groupby(["produto", "marca", "categoria", "estado", "canal"], as_index=False)
        .agg(receita=("receita", "sum"))
    )
    meta_ec = metas_filtradas.groupby(["estado", "canal"], as_index=False).agg(meta_ec=("meta_faturamento", "sum"))
    receita_tot = prod_ec.groupby(["estado", "canal"], as_index=False).agg(receita_total_ec=("receita", "sum"))

    prod_ec = (
        prod_ec.merge(meta_ec, on=["estado", "canal"], how="left")
        .merge(receita_tot, on=["estado", "canal"], how="left")
    )
    prod_ec["meta_calc"] = np.where(
        prod_ec["receita_total_ec"] > 0,
        prod_ec["meta_ec"] * (prod_ec["receita"] / prod_ec["receita_total_ec"]),
        0,
    )

    meta_prod = prod_ec.groupby(["produto", "marca", "categoria"], as_index=False).agg(meta=("meta_calc", "sum"))
    produtos = base_prod.merge(meta_prod, on=["produto", "marca", "categoria"], how="left")
    produtos["meta"] = produtos["meta"].fillna(0)
    produtos["atingido_pct"] = np.where(produtos["meta"] > 0, (produtos["receita"] / produtos["meta"]) * 100, np.nan)

    produtos = produtos.sort_values("receita", ascending=False).head(12)
    produtos["receita"] = produtos["receita"].round(2)
    produtos["meta"] = produtos["meta"].round(2)
    produtos["ticket"] = produtos["ticket"].round(2)
    produtos["atingido_pct"] = produtos["atingido_pct"].round(1)
    produtos["% atingido"] = produtos["atingido_pct"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "—")

    produtos_fmt = produtos.rename(
        columns={
            "receita": "Realizado",
            "meta": "Meta",
            "pedidos": "Pedidos",
            "ticket": "Ticket médio",
        }
    )
    produtos_fmt = produtos_fmt[
        ["produto", "marca", "categoria", "Meta", "Realizado", "% atingido", "Pedidos", "Ticket médio"]
    ]

    st.markdown("<div class='section-title'>Top produtos</div>", unsafe_allow_html=True)
    st.dataframe(
        produtos_fmt,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Base totalmente fictícia gerada em Python para demonstração de análises de vendas, mix de produtos e metas."
    )


if __name__ == "__main__":
    main()
