import streamlit as st
import pandas as pd

# Función de cálculo CETES
def calculadora_cetes(monto, tasa, dt, plazo):
    VN = 10.0
    base = 360.0

    if tasa > 1:
        tasa = tasa / 100.0

    dt = max(0, min(dt, plazo))  # DT entre 0 y plazo

    # Precio de compra
    Pc = VN / (1 + tasa * (plazo / base))

    # Títulos adquiridos
    titulos = monto / Pc

    # Días a vencimiento
    Dv = plazo - dt

    # Precio ajustado a los días transcurridos
    Pr = VN / (1 + tasa * (Dv / base))

    # Monto final al de los días transcurridos
    Mf_plazo = titulos * Pr

    # Tasa efectiva del plazo
    T_plazo = (Mf_plazo / monto) - 1 if monto != 0 else 0

    # Valor nominal al vencimiento
    VN_total = titulos * VN

    # Ganancia neta
    ganancia = Mf_plazo - monto

    return {
        "Plazo (días)": plazo,
        "Precio de compra": Pc,
        "Títulos adquiridos": titulos,
        "Días a vencimiento": Dv,
        "Precio ajustado a los días transcurridos": Pr,
        "Monto final al de los días transcurridos": Mf_plazo,
        "Tasa efectiva del plazo": T_plazo,
        "Valor nominal al vencimiento": VN_total,
        "Ganancia neta": ganancia
    }

# Estilo azul oscuro
st.markdown(
    """
    <style>
    .main {
        background-color: #001f3f;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #0074D9;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit App
st.set_page_config(page_title="Calculadora CETES", layout="wide")
st.title("Calculadora CETES 😈🙏")

# Sidebar inputs
st.sidebar.header("Datos de inversión")
monto = st.sidebar.number_input("Monto a invertir", min_value=0.0, value=3000.0, step=100.0)
tasa = st.sidebar.number_input("Tasa anual (%)", min_value=0.0, value=7.69, step=0.01)
dt = st.sidebar.number_input("Días transcurridos (DT)", min_value=0, value=28, step=1)
plazo = st.sidebar.selectbox("Plazo (días)", [28, 91, 182, 364, 728])

# Botón de cálculo
if st.sidebar.button("Calcular"):
    resultados = calculadora_cetes(monto, tasa, dt, plazo)
    
    # Preparar tabla para mostrar resultados (sin Monto final anual)
    display_data = {
        "Concepto": [
            "Plazo (días)",
            "Precio de compra",
            "Títulos adquiridos",
            "Días a vencimiento",
            "Precio ajustado a los días transcurridos",
            "Monto final al de los días transcurridos",
            "Tasa efectiva del plazo",
            "Valor nominal al vencimiento",
            "Ganancia neta"
        ],
        "Valor": [
            f"{resultados['Plazo (días)']:,}",
            f"${resultados['Precio de compra']:,.2f}",
            f"{resultados['Títulos adquiridos']:,.2f}",
            f"{resultados['Días a vencimiento']:,}",
            f"${resultados['Precio ajustado a los días transcurridos']:,.2f}",
            f"${resultados['Monto final al de los días transcurridos']:,.2f}",
            f"{resultados['Tasa efectiva del plazo']*100:.4f}%",
            f"${resultados['Valor nominal al vencimiento']:,.2f}",
            f"${resultados['Ganancia neta']:,.2f}"
        ]
    }

    df = pd.DataFrame(display_data)
    
    st.subheader(f"Resultados CETES {plazo} días")
    st.table(df)

    # Resaltar ganancia o pérdida
    if resultados["Ganancia neta"] >= 0:
        st.success(f"✅ Ganancia neta después de los días transcurridos: ${resultados['Ganancia neta']:,.2f}")
    else:
        st.error(f"⚠️ Pérdida neta después de los días transcurridos: ${resultados['Ganancia neta']:,.2f}")
