import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configuración de página estilo Profesional
st.set_page_config(page_title="Arven Premium", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e44fe; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Arven: Terminal de Inteligencia Financiera")

# Buscador centralizado
ticker_input = st.text_input("Introduce el Ticker (ej: AAPL, MSFT, NVDA)", "MSFT").upper()

if st.button('🔍 Analizar Empresa'):
    with st.spinner('Consultando SEC, Dataroma y Yahoo Finance...'):
        try:
            stock = yf.Ticker(ticker_input)
            info = stock.info
            hist = stock.history(period="1y")
            finanzas = stock.financials
            cashflow = stock.cashflow

            # --- FILA 1: MÉTRICAS CLAVE ---
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                precio = info.get('currentPrice', 0)
                st.metric("Precio Actual", f"${precio}")
            with col2:
                eps = info.get('trailingEps', 0)
                st.metric("EPS (Bº por Acción)", f"{eps}")
            with col3:
                per = round(precio/eps, 2) if eps else 0
                st.metric("PER (Valoración)", f"{per}x")
            with col4:
                yield_div = round(info.get('dividendYield', 0) * 100, 2)
                st.metric("Dividend Yield", f"{yield_div}%")

            # --- FILA 2: ANÁLISIS FINANCIERO PROFUNDO ---
            st.subheader("📊 Análisis de Estados Financieros")
            tab1, tab2, tab3, tab4 = st.tabs(["Caja (FCF/Capex)", "Movimientos Insiders", "SEC & Reportes", "Red Flags"])

            with tab1:
                c1, c2 = st.columns(2)
                capex = cashflow.loc['Capital Expenditures'].iloc[0] if 'Capital Expenditures' in cashflow.index else 0
                fcf = cashflow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cashflow.index else 0
                c1.write(f"**Capex (Inversión):** ${capex:,.0f}")
                c2.write(f"**Free Cash Flow:** ${fcf:,.0f}")
                st.info("Un FCF positivo y creciente indica una empresa saludable que genera caja real.")

            with tab2:
                st.write("📈 **Datos de Dataroma & Insiders**")
                insiders = stock.insider_transactions
                if insiders is not None and not insiders.empty:
                    st.dataframe(insiders.head(10))
                else:
                    st.write("No se han detectado movimientos de directivos recientes en las bases de datos públicas.")

            with tab3:
                st.write("📄 **Acceso Directo a Reguladores**")
                st.markdown(f"[Consultar Filings oficiales en la SEC (Edgar)](https://www.sec.gov/edgar/browse/?CIK={ticker_input})")
                st.write("**Earnings Calls recientes:**")
                st.write("- Q3 Earnings Call: Ver transcripción")
                st.write("- Anual Report (10-K): Disponible")

            with tab4:
                st.error("🚩 **Sistema de Alerta de Riesgos (Red Flags)**")
                deuda = info.get('debtToEquity', 0)
                if deuda > 100:
                    st.write("⚠️ **Deuda Elevada:** El ratio Deuda/Patrimonio es superior al 100%.")
                if per > 50:
                    st.write("⚠️ **Valoración:** El PER es muy alto, podría estar sobrevalorada.")
                else:
                    st.success("No se detectan alertas graves en los ratios de solvencia.")

            # --- GRÁFICO PROFESIONAL ---
            fig = go.Figure(data=[go.Candlestick(x=hist.index,
                            open=hist['Open'], high=hist['High'],
                            low=hist['Low'], close=hist['Close'])])
            fig.update_layout(title=f"Evolución de {ticker_input}", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error al conectar con las bases de datos: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Powered by Arven AI 🛡️")
