import time

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Estação Meteorológica", page_icon="🌦️", layout="wide")

st.title("🌦️ Estação Meteorológica")

# ---------- barra lateral ----------
st.sidebar.header("Configurações")
api_url = st.sidebar.text_input("Endereço da API", "http://localhost:8000")
intervalo = st.sidebar.number_input("Atualizar a cada (segundos)", min_value=2, max_value=60, value=5)
auto = st.sidebar.checkbox("Atualizar automaticamente", value=True)

# ---------- histórico guardado na sessão ----------
if "historico" not in st.session_state:
    st.session_state.historico = []


def buscar_ultima_leitura(url):
    resposta = requests.get(url + "/readings/latest", timeout=5)
    resposta.raise_for_status()
    return resposta.json()


def fazer_grafico(df, coluna, titulo):
    fig, ax = plt.subplots(figsize=(6, 2.8))
    ax.plot(df.index, df[coluna], marker="o")
    ax.set_title(titulo)
    ax.grid(True)
    fig.autofmt_xdate()
    st.pyplot(fig)
    plt.close(fig)


# ---------- busca os dados na API ----------
leitura = None
deu_erro = False
try:
    leitura = buscar_ultima_leitura(api_url)
except requests.exceptions.RequestException:
    deu_erro = True
    st.error("Não foi possível conectar na API. Verifique se o uvicorn está rodando e se o endereço está certo.")

if leitura is None and not deu_erro:
    st.info("Ainda não existe nenhuma leitura no banco de dados.")

# só guarda no histórico se for uma leitura nova
if leitura is not None:
    historico = st.session_state.historico
    if len(historico) == 0 or historico[-1]["id"] != leitura["id"]:
        historico.append(leitura)
        if len(historico) > 100:
            historico.pop(0)

# ---------- mostra os dados ----------
if st.session_state.historico:
    atual = st.session_state.historico[-1]

    if len(st.session_state.historico) > 1:
        anterior = st.session_state.historico[-2]
    else:
        anterior = atual

    st.caption("Última leitura: " + atual["recorded_at"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperatura", f"{atual['temperature']:.1f} °C",
                f"{atual['temperature'] - anterior['temperature']:.1f}")
    col2.metric("Umidade", f"{atual['humidity']:.1f} %",
                f"{atual['humidity'] - anterior['humidity']:.1f}")
    col3.metric("Pressão", f"{atual['pressure']:.1f} hPa",
                f"{atual['pressure'] - anterior['pressure']:.1f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Luminosidade", atual["luminosity"],
                int(atual["luminosity"] - anterior["luminosity"]))
    col5.metric("Qualidade do ar", f"{atual['air_quality']:.1f}",
                f"{atual['air_quality'] - anterior['air_quality']:.1f}")
    col6.metric("Chuva", f"{atual['rainfall']:.1f}",
                f"{atual['rainfall'] - anterior['rainfall']:.1f}")

    # ---------- gráficos ----------
    df = pd.DataFrame(st.session_state.historico)
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])
    df = df.set_index("recorded_at")

    st.subheader("Gráficos")
    if len(df) < 2:
        st.info("Aguardando mais leituras para montar os gráficos...")
    else:
        g1, g2 = st.columns(2)
        with g1:
            fazer_grafico(df, "temperature", "Temperatura (°C)")
            fazer_grafico(df, "pressure", "Pressão (hPa)")
            fazer_grafico(df, "luminosity", "Luminosidade")
        with g2:
            fazer_grafico(df, "humidity", "Umidade (%)")
            fazer_grafico(df, "air_quality", "Qualidade do ar")
            fazer_grafico(df, "rainfall", "Chuva")

    # ---------- tabela ----------
    st.subheader("Últimas leituras")
    st.dataframe(df.sort_index(ascending=False).head(10))

# ---------- atualização automática ----------
if auto:
    time.sleep(intervalo)
    st.rerun()
