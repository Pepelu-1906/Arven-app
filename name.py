import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Configuración estética
st.set_page_config(page_title="Arven Invest", layout="wide")

st.title("🛡️ Arven: Terminal de Inversión")

ticker = st.text_input("Escribe el Ticker aquí y pulsa la lupa del teclado", "MSFT").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1y")

        # --- MÉTRICAS TOP ---
        col1, col2, col3 = st.columns(3)
        
        # Cálculo de ROIC estimado
        ebit = info.get('ebitda', 0) - info.get('amortization', 0)
        cap_empleado = info.get('totalStockholderEquity', 0) + info.get('totalDebt', 0)
        roic = (ebit / cap_empleado * 100) if cap_empleado > 0 else 0
        
        col1.metric("ROIC", f"{roic:.1f}%", help="Retorno sobre el Capital Invertido")
        col2.metric("PER", info.get('trailingPE', 'N/A'))
        col3.metric("Div. Yield", f"{info.get('dividendYield', 0)*100:.2f}%")

        # --- ANÁLISIS DE CALIDAD ---
        with st.expander("📊 Análisis de Calidad y Crecimiento", expanded=True):
            st.write(f"**Empresa:** {info.get('longName')}")
            st.write(f"**Sector:** {info.get('sector')}")
            
            # Semáforo de Riesgo
            caja = info.get('totalCash', 0)
            deuda = info.get('totalDebt', 1)
            if caja > deuda:
                st.success("✅ Balance Sólido: Más caja que deuda.")
            else:
                st.warning("⚠️ Atención: La deuda supera a la caja disponible.")

        # --- GRÁFICO TÉCNICO ---
        st.subheader("📈 Análisis Técnico (Velas)")
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index, open=hist['Open'], high=hist['High'],
            low=hist['Low'], close=hist['Close']
        )])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=400)
        st.plotly_chart(fig, use_container_width=True)

    except:
        st.error("No se pudo encontrar el ticker. Prueba con uno común como AAPL.")
      
