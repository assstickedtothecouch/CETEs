import streamlit as st
import pandas as pd

def calculadora_cetes(monto, tasa, dt, plazo):
    VN = 10.0
    base = 360.0

    if tasa > 1:
        tasa = tasa / 100.0

    if dt < 0:
        dt = 0

    # Precio de compra
    Pc = VN / (1 + tasa * (plazo / base))

    # Títulos adquiridos
    titulos = monto / Pc

    # Días a vencimiento ajustados
    Dv = max(plazo - dt, 0)

    # Precio ajustado
    Pr = VN / (1 + tasa * (Dv / base))

    # Monto final al plazo
    Mf_plazo = titulos * Pr

    # Tasa efectiva del plazo
    T_plazo = (Mf_plazo / monto) - 1 if monto != 0 else 0

    # Número de plazos equivalentes en un año
    P = base / plazo

    # Monto final anual correctamente
    Mf_anual = monto * (1 + T_plazo) ** P

    # Ganancia neta en el plazo
    ganancia = Mf_plazo - monto

    return {
        "Plazo (días)": plazo,
        "Precio de compra": Pc,
        "Títulos adquiridos": titulos,
        "Días a vencimiento": Dv,
        "Precio ajustado": Pr,
        "Monto final al plazo": Mf_plazo,
        "Tasa efectiva del plazo": T_plazo,
        "Monto final anual": Mf_anual,
        "Ganancia neta": ganancia
    }

# Streamlit App
st.set_page_config(page_title="Calculadora CETES", layout="wide")
st.title("💰 Calculadora CETES")

# Entradas
st.sidebar.header("Datos de inversión")
monto = st.sidebar.number_input("Monto a invertir", min_value=0.0, value=3000.0)
tasa = st.sidebar.number_input("Tasa anual (%)", min_value=0.0, value=7.69)
dt = st.sidebar.number_input("Días transcurridos (DT)", min_value=0, value=0)
plazo = st.sidebar.selectbox("Plazo (días)", [28, 91, 182, 364, 728])

if st.sidebar.button("Calcular"):
    resultados = calculadora_cetes(monto, tasa, dt, plazo)
    
    display_data = {
        "Concepto": [
            "Plazo (días)",
            "Precio de compra",
            "Títulos adquiridos",
            "Días a vencimiento",
            "Precio ajustado",
            "Monto final al plazo",
            "Tasa efectiva del plazo",
            "Monto final anual",
            "Ganancia neta"
        ],
        "Valor": [
            resultados["Plazo (días)"],
            f"${resultados['Precio de compra']:.2f}",
            f"{resultados['Títulos adquiridos']:.2f}",
            resultados["Días a vencimiento"],
            f"${resultados['Precio ajustado']:.2f}",
            f"${resultados['Monto final al plazo']:.2f}",
            f"{resultados['Tasa efectiva del plazo']*100:.4f}%",
            f"${resultados['Monto final anual']:.2f}",
            f"${resultados['Ganancia neta']:.2f}"
        ]
    }

    df = pd.DataFrame(display_data)
    st.subheader(f"Resultados CETES {plazo} días")
    st.table(df)

    if resultados["Ganancia neta"] >= 0:
        st.success(f"✅ Ganancia neta: ${resultados['Ganancia neta']:.2f}")
    else:
        st.error(f"⚠️ Pérdida neta: ${resultados['Ganancia neta']:.2f}")
