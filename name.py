import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configuración Pro
st.set_page_config(page_title="Arven Ultimate", layout="wide")

st.title("🛡️ Arven: Inteligencia Financiera Avanzada")

ticker = st.text_input("Introduce el Ticker oficial (ej: MSFT, AAPL, NVDA)", "MSFT").upper()

if st.button('🔍 Realizar Análisis Profundo'):
    try:
        stock = yf.Ticker(ticker)
        # Forzamos la descarga de datos profundos
        info = stock.info
        df_finanzas = stock.financials
        df_cashflow = stock.cashflow
        df_balance = stock.balance_sheet
        
        # --- CABECERA RESUMEN ---
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            precio = info.get('currentPrice', 0)
            st.metric("Precio", f"${precio}")
        with col2:
            eps = round(info.get('trailingEps', 0), 2)
            st.metric("EPS (Bº por acción)", f"{eps}")
        with col3:
            per = round(precio/eps, 2) if eps else "N/A"
            st.metric("PER Actual", f"{per}x")
        with col4:
            yield_div = round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0
            st.metric("Div. Yield", f"{yield_div}%")

        # --- SECCIONES DE INTELIGENCIA ---
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Flujos de Caja (FCF/Capex)", "👔 Insiders & Dataroma", "📄 SEC Filings & Earnings", "🚩 Red Flags & Competencia"])

        with tab1:
            st.subheader("Análisis de Generación de Valor")
            # Extraemos Capex y FCF de los estados financieros reales
            try:
                capex = abs(df_cashflow.loc['Capital Expenditures'].iloc[0])
                fcf = df_cashflow.loc['Free Cash Flow'].iloc[0]
                st.write(f"**Capex (Inversión en el negocio):** ${capex:,.0f}")
                st.write(f"**Free Cash Flow (Caja Libre):** ${fcf:,.0f}")
                st.progress(min(max(fcf/capex if capex != 0 else 0, 0.0), 1.0))
                st.caption("Relación FCF vs Capex (Capacidad de autofinanciación)")
            except:
                st.warning("Datos de flujo de caja no disponibles para este ticker en este momento.")

        with tab2:
            st.subheader("Movimientos de Directivos (Insiders)")
            st.info("Nota: Los datos de Dataroma son privados. Aquí mostramos los reportes oficiales de la empresa.")
            insiders = stock.insider_transactions
            if insiders is not None and not insiders.empty:
                st.dataframe(insiders.head(10))
            else:
                st.write("No hay transacciones de insiders reportadas recientemente.")
            st.markdown(f"[🔗 Ver perfil completo en Dataroma](https://www.dataroma.com/m/stock.php?sym={ticker})")

        with tab3:
            st.subheader("Documentación Oficial (SEC)")
            st.write("Accede a los reportes 10-K (Anual) y 10-Q (Trimestral) directamente:")
            st.markdown(f"👉 [Buscador EDGAR de la SEC para {ticker}](https://www.sec.gov/edgar/browse/?CIK={ticker})")
            st.write("---")
            st.subheader("Earnings Calls")
            st.write("Consulta las últimas conferencias de resultados:")
            st.markdown(f"[🎧 Transcripciones de Earnings en Seeking Alpha](https://seekingalpha.com/symbol/{ticker}/earnings/transcripts)")

        with tab4:
            st.subheader("Análisis de Riesgos (Red Flags)")
            deuda = info.get('debtToEquity', 0)
            margin = info.get('profitMargins', 0) * 100
            
            col_a, col_b = st.columns(2)
            if deuda > 100:
                col_a.error(f"❌ Deuda elevada: {round(deuda, 2)}%")
            else:
                col_a.success(f"✅ Deuda controlada: {round(deuda, 2)}%")
                
            if margin < 10:
                col_b.warning(f"⚠️ Márgenes estrechos: {round(margin, 2)}%")
            else:
                col_b.success(f"✅ Márgenes sólidos: {round(margin, 2)}%")

        # Gráfico de apoyo
        st.subheader("Gráfico de Cotización")
        hist = stock.history(period="1y")
        st.line_chart(hist['Close'])

    except Exception as e:
        st.error(f"Error de conexión: {e}. Yahoo Finance ha limitado las peticiones. Espera 15 min.")

st.sidebar.write("Arven v2.0 - IA de Inversión")
