
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from simuladores.ambiente import AmbienteSimulado
from simuladores.sensores import ler_termohigrometros
from simuladores.luminosidade import SimuladorLuminosidade
from simuladores.solucao_nutritiva import SimuladorSolucaoNutritiva

from modulos.ventilacao import ControleVentilacao
from modulos.iluminacao import ControleIluminacao
from modulos.nutrientes import ControleNutrientes


# ==========================================
# CONFIGURACAO
# ==========================================

st.set_page_config(
    page_title="Horta Hidroponica Inteligente",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0e1726;
    color: #f1f5f9;
}

div[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

div[data-testid="stMetric"] * {
    color: #17263b !important;
    opacity: 1 !important;
}

h1, h2, h3 {
    color: #6ee7b7 !important;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# INICIALIZACAO
# ==========================================

def inicializar():
    st.session_state.ambiente = AmbienteSimulado()
    st.session_state.ventilacao = ControleVentilacao()

    st.session_state.luminosidade = (
        SimuladorLuminosidade()
    )
    st.session_state.iluminacao = ControleIluminacao()

    st.session_state.reservatorio = (
        SimuladorSolucaoNutritiva()
    )
    st.session_state.nutrientes = ControleNutrientes()

    st.session_state.historico = []


if "ambiente" not in st.session_state:
    inicializar()

if "reservatorio" not in st.session_state:
    inicializar()


# ==========================================
# CABECALHO E CONTROLES
# ==========================================

st.title("🌱 HORTA HIDROPONICA INTELIGENTE")
st.caption(
    "Supervisório integrado | Clima + Luz + Nutrientes "
    "| Raspberry Pi + ESP32 | SIMULAÇÃO"
)

with st.sidebar:
    st.header("⚙️ Supervisório")
    st.success("Modo: SIMULAÇÃO")

    st.write("Atualização: 2 segundos")
    st.write("Avanço: 5 minutos/ciclo")

    if st.button("🔄 Reiniciar simulação"):
        inicializar()
        st.rerun()

    st.divider()
    st.write("**Subsistemas**")
    st.write("🌡️ Climatização")
    st.write("☀️ Sombrite")
    st.write("💧 Solução nutritiva")
    st.divider()
    st.caption("Nenhum equipamento físico conectado.")


# ==========================================
# GRAFICOS
# ==========================================

def grafico_linhas(df, colunas, titulo, cores,
                   limites=None):
    fig = go.Figure()

    for coluna, cor in zip(colunas, cores):
        fig.add_trace(
            go.Scatter(
                x=df["Tempo"],
                y=df[coluna],
                mode="lines",
                name=coluna,
                line=dict(color=cor, width=2)
            )
        )

    if limites:
        for valor, texto in limites:
            fig.add_hline(
                y=valor,
                line_dash="dash",
                line_color="#ef4444",
                annotation_text=texto
            )

    fig.update_layout(
        title=titulo,
        xaxis_title="Tempo simulado (min)",
        template="plotly_dark",
        height=330,
        margin=dict(l=25, r=20, t=55, b=35)
    )

    return fig


def mostrar_atuador(nome, ligado):
    if ligado:
        st.success(f"🟢 {nome} - LIGADO")
    else:
        st.info(f"⚪ {nome} - DESLIGADO")


# ==========================================
# SUPERVISORIO
# ==========================================

@st.fragment(run_every="2s")
def atualizar_painel():

    ambiente = st.session_state.ambiente
    ventilacao = st.session_state.ventilacao
    simulador_luz = st.session_state.luminosidade
    iluminacao = st.session_state.iluminacao
    reservatorio = st.session_state.reservatorio
    nutrientes = st.session_state.nutrientes

    # --------------------------------------
    # BLOCO CLIMATICO
    # --------------------------------------

    motores_anteriores = (
        ventilacao.motores.consultar_estado()
    )

    estado_ambiente = ambiente.atualizar(
        motores_anteriores
    )

    tempo = estado_ambiente["tempo"]

    leituras = ler_termohigrometros(
        estado_ambiente
    )

    clima = ventilacao.processar(leituras)

    temperatura = clima["temperatura_media"]
    umidade = clima["umidade_media"]
    diferenca = clima["diferenca_vertical"]
    motores = clima["motores"]

    # --------------------------------------
    # BLOCO LUMINOSIDADE
    # --------------------------------------

    sensores_luz = simulador_luz.atualizar(
        tempo,
        iluminacao.abertura
    )

    luz = iluminacao.processar(sensores_luz)

    # --------------------------------------
    # BLOCO A - SOLUCAO NUTRITIVA
    # --------------------------------------

    atuadores_anteriores = (
        nutrientes.atuadores.copy()
    )

    sensores_nutrientes = reservatorio.atualizar(
        atuadores_anteriores,
        minutos=5
    )

    resultado_nutrientes = nutrientes.processar(
        sensores_nutrientes
    )

    atuadores = resultado_nutrientes["atuadores"]
    alarmes = resultado_nutrientes["alarmes"]


    # Aplicar pulsos dosadores no simulador
    dose_aplicada = "-"

    for bomba in ("D1", "D2", "D3", "D4"):
        if atuadores[bomba]:
            sucesso = reservatorio.aplicar_dose(bomba)

            if sucesso:
                dose_aplicada = bomba
            else:
                alarmes.append(
                    f"Estoque simulado vazio: {bomba}"
                )

    # --------------------------------------
    # HISTORICO
    # --------------------------------------

    registro = {
        "Tempo": tempo,
        "Temperatura": temperatura,
        "Umidade": umidade,
        "Diferenca": diferenca,

        "L1": luz["L1"],
        "L2": luz["L2"],
        "Sombrite": luz["abertura"],
        "Motor_sombrite": luz["motor"],

        "pH": sensores_nutrientes["ph"],
        "EC": sensores_nutrientes["ec"],
        "Temperatura_solucao":
            sensores_nutrientes["temperatura"],
        "Volume":
            sensores_nutrientes["volume"],
        "Nivel":
            sensores_nutrientes["nivel_percentual"],
        "Vazao":
            sensores_nutrientes["vazao"],

        "B1": atuadores["B1"],
        "B2": atuadores["B2"],
        "CH1": atuadores["CH1"],
        
        "D1": atuadores["D1"],
        "D2": atuadores["D2"],
        "D3": atuadores["D3"],
        "D4": atuadores["D4"],
        "Dose_aplicada": dose_aplicada,
        "Estado_dosagem":
            resultado_nutrientes["estado_dosagem"],
        "Mistura_restante":
            resultado_nutrientes["mistura_restante"],
        "Total_pulsos":
            nutrientes.total_pulsos,

        "Alarmes": " | ".join(alarmes),

        **motores
    }

    st.session_state.historico.append(registro)
    st.session_state.historico = (
        st.session_state.historico[-288:]
    )

    df = pd.DataFrame(st.session_state.historico)

    # --------------------------------------
    # RESUMO GERAL
    # --------------------------------------

    st.subheader("📊 Visão geral")

    r1, r2, r3, r4 = st.columns(4)

    r1.metric("Tempo simulado", f"{tempo} min")
    r2.metric("Temperatura", f"{temperatura:.2f} °C")
    r3.metric("pH", f"{sensores_nutrientes['ph']:.2f}")
    r4.metric(
        "Nível reservatório",
        f"{sensores_nutrientes['nivel_percentual']:.1f}%"
    )

    if alarmes:
        st.error(
            "⚠️ ALARMES ATIVOS: " + " | ".join(alarmes)
        )
    else:
        st.success("Sistema sem alarmes ativos")

    # ======================================
    # ABA 1 - CLIMA
    # ======================================

    aba_clima, aba_luz, aba_nutrientes, aba_dados = (
        st.tabs([
            "🌡️ Clima",
            "☀️ Luminosidade",
            "💧 Solução nutritiva",
            "📋 Histórico"
        ])
    )

    with aba_clima:
        st.subheader("Controle climático")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Temperatura média",
            f"{temperatura:.2f} °C"
        )
        c2.metric(
            "Umidade média",
            f"{umidade:.2f}%"
        )
        c3.metric(
            "Diferença vertical",
            f"{diferenca:.2f} °C"
        )

        g1, g2 = st.columns(2)

        with g1:
            st.plotly_chart(
                grafico_linhas(
                    df,
                    ["Temperatura"],
                    "Temperatura interna",
                    ["#ff7043"],
                    [(29, "Limite")]
                ),
                width="stretch"
            )

        with g2:
            st.plotly_chart(
                grafico_linhas(
                    df,
                    ["Umidade"],
                    "Umidade relativa",
                    ["#38bdf8"],
                    [(80, "Limite")]
                ),
                use_container_width=True
            )

        st.subheader("Ventilação")

        grupos = {
            "Insuflação inferior": ["V1", "V2", "V3"],
            "Circulação superior": ["C1", "C2", "C3"],
            "Exaustão superior": ["E1", "E2", "E3"]
        }

        for grupo, equipamentos in grupos.items():
            st.markdown(f"**{grupo}**")
            colunas = st.columns(3)

            for coluna, nome in zip(
                colunas, equipamentos
            ):
                with coluna:
                    mostrar_atuador(
                        nome, motores[nome]
                    )

        st.subheader("Termohigrômetros")

        tabela_sensores = []

        for nome, dados in leituras.items():
            tabela_sensores.append({
                "Sensor": nome,
                "Temperatura (°C)":
                    dados["temperatura"],
                "Umidade (%)":
                    dados["umidade"]
            })

        st.dataframe(
            pd.DataFrame(tabela_sensores),
            use_container_width=True,
            hide_index=True
        )

    # ======================================
    # ABA 2 - LUMINOSIDADE
    # ======================================

    with aba_luz:
        st.subheader("Controle do sombrite")

        l1, l2, l3 = st.columns(3)

        l1.metric(
            "L1 - Externa",
            f"{luz['L1']:,.0f} lux"
        )
        l2.metric(
            "L2 - Interna",
            f"{luz['L2']:,.0f} lux"
        )
        l3.metric(
            "Sombrite aberto",
            f"{luz['abertura']:.0f}%"
        )

        st.progress(
            int(luz["abertura"]),
            text="Percentual de abertura"
        )

        if luz["motor"] == "ABRINDO":
            st.info("Motor: ABRINDO")
        elif luz["motor"] == "FECHANDO":
            st.warning("Motor: FECHANDO")
        else:
            st.success("Motor: PARADO")

        st.plotly_chart(
            grafico_linhas(
                df,
                ["L1", "L2"],
                "Luminosidade externa e interna",
                ["#facc15", "#38bdf8"],
                [(35000, "Limite L2")]
            ),
            use_container_width=True
        )

        st.plotly_chart(
            grafico_linhas(
                df,
                ["Sombrite"],
                "Abertura do sombrite (%)",
                ["#22c55e"]
            ),
            use_container_width=True
        )

        st.caption(
            "L2 é medida antes do movimento "
            "do sombrite neste ciclo."
        )

    # ======================================
    # ABA 3 - SOLUCAO NUTRITIVA
    # ======================================

    with aba_nutrientes:
        st.subheader(
            "💧 Bloco A - Solução nutritiva"
        )

        n1, n2, n3 = st.columns(3)

        n1.metric(
            "pH",
            f"{sensores_nutrientes['ph']:.3f}"
        )
        n2.metric(
            "EC",
            f"{sensores_nutrientes['ec']:.3f} mS/cm"
        )
        n3.metric(
            "Temperatura",
            f"{sensores_nutrientes['temperatura']:.2f} °C"
        )

        n4, n5, n6 = st.columns(3)

        n4.metric(
            "Volume",
            f"{sensores_nutrientes['volume']:.1f} L"
        )
        n5.metric(
            "Nível",
            f"{sensores_nutrientes['nivel_percentual']:.1f}%"
        )
        n6.metric(
            "Vazão",
            f"{sensores_nutrientes['vazao']:.1f} L/min"
        )

        st.progress(
            int(sensores_nutrientes["nivel_percentual"]),
            text="Nível do reservatório"
        )

        st.subheader("Bombas e equipamentos")

        b1, b2, b3 = st.columns(3)

        with b1:
            mostrar_atuador(
                "B1 - Circulação",
                atuadores["B1"]
            )
        with b2:
            mostrar_atuador(
                "B2 - Reposição",
                atuadores["B2"]
            )
        with b3:
            mostrar_atuador(
                "CH1 - Chiller",
                atuadores["CH1"]
            )

        st.subheader("Histórico químico")

        gp1, gp2 = st.columns(2)

        with gp1:
            st.plotly_chart(
                grafico_linhas(
                    df,
                    ["pH"],
                    "Evolução do pH",
                    ["#a78bfa"],
                    [
                        (5.5, "Mínimo"),
                        (6.2, "Máximo")
                    ]
                ),
                use_container_width=True
            )

        with gp2:
            st.plotly_chart(
                grafico_linhas(
                    df,
                    ["EC"],
                    "Condutividade elétrica",
                    ["#facc15"],
                    [
                        (1.2, "Mínimo"),
                        (1.8, "Máximo")
                    ]
                ),
                use_container_width=True
            )

        st.subheader("Controle hidráulico e térmico")

        gh1, gh2 = st.columns(2)

        with gh1:
            st.plotly_chart(
                grafico_linhas(
                    df,
                    ["Nivel"],
                    "Nível do reservatório (%)",
                    ["#38bdf8"]
                ),
                use_container_width=True
            )

        with gh2:
            st.plotly_chart(
                grafico_linhas(
                    df,
                    ["Temperatura_solucao"],
                    "Temperatura da solução",
                    ["#fb923c"],
                    [(24, "Acionamento CH1")]
                ),
                use_container_width=True
            )

        st.subheader("Alarmes da solução")
        
        st.subheader("Dosagem inteligente")

        st.metric(
            "Estado do controlador",
            resultado_nutrientes["estado_dosagem"]
        )

        st.metric(
            "Tempo de mistura restante",
            f"{resultado_nutrientes['mistura_restante']} min"
        )

        st.write(
            "Último evento:",
            resultado_nutrientes["ultimo_evento"]
        )

        st.write(
            "Pulsos realizados:",
            nutrientes.total_pulsos
        )

        colunas_dose = st.columns(4)

        for coluna, bomba, descricao in zip(
            colunas_dose,
            ("D1", "D2", "D3", "D4"),
            (
                "pH Down",
                "pH Up",
                "Nutriente A",
                "Nutriente B"
            )
        ):
            with coluna:
                mostrar_atuador(
                    f"{bomba} - {descricao}",
                    atuadores[bomba]
                )
                st.caption(
                    f"Pulsos: "
                    f"{nutrientes.pulsos_realizados[bomba]}"
                )

        st.plotly_chart(
            grafico_linhas(
                df,
                ["Total_pulsos"],
                "Histórico acumulado de dosagem",
                ["#22c55e"]
            ),
            use_container_width=True
        )


        if alarmes:
            for alarme in alarmes:
                st.error(alarme)
        else:
            st.success(
                "Parâmetros monitorados sem alarmes"
            )

        st.caption(
            "Dosagem de nutrientes e correção "
            "de pH ainda não implementadas."
        )

    # ======================================
    # ABA 4 - HISTORICO
    # ======================================

    with aba_dados:
        st.subheader("Histórico integrado")

        st.dataframe(
            df.tail(30),
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Baixar histórico completo CSV",
            data=csv,
            file_name="historico_horta_3_blocos.csv",
            mime="text/csv",
            key="download_tres_blocos"
        )

        st.caption(
            "Histórico em memória limitado aos "
            "últimos 288 ciclos (24 horas simuladas)."
        )


# ==========================================
# EXECUCAO
# ==========================================

atualizar_painel()
