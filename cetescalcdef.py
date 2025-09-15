import streamlit as st
import pandas as pd

# Función de cálculo CETES
def calculadora_cetes(monto, tasa, dt, plazo):
    VN = 10.0
    base = 360.0

    # Convertir porcentaje a decimal si es necesario
    if tasa > 1:
        tasa = tasa / 100.0

    # Validaciones
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

    # Número de plazos equivalentes en un año (usando los días restantes)
    P = base / Dv

    # Monto final anual
    Mf_anual = monto * (1 + T_plazo) ** P

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
        "Monto final anual": Mf_anual,
        "Valor nominal al vencimiento": VN_total,
        "Ganancia neta": ganancia
    }

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
    
    # Preparar tabla para mostrar resultados
    display_data = {
        "Concepto": [
            "Plazo (días)",
            "Precio de compra",
            "Títulos adquiridos",
            "Días a vencimiento",
            "Precio ajustado a los días transcurridos",
            "Monto final al de los días transcurridos",
            "Tasa efectiva del plazo",
            "Monto final anual",
            "Valor nominal al vencimiento",
            "Ganancia neta"
        ],
        "Valor": [
            resultados["Plazo (días)"],
            f"${resultados['Precio de compra']:.2f}",
            f"{resultados['Títulos adquiridos']:.2f}",
            resultados["Días a vencimiento"],
            f"${resultados['Precio ajustado a los días transcurridos']:.2f}",
            f"${resultados['Monto final al de los días transcurridos']:.2f}",
            f"{resultados['Tasa efectiva del plazo']*100:.4f}%",
            f"${resultados['Monto final anual']:.2f}",
            f"${resultados['Valor nominal al vencimiento']:.2f}",
            f"${resultados['Ganancia neta']:.2f}"
        ]
    }

    df = pd.DataFrame(display_data)
    
    st.subheader(f"Resultados CETES {plazo} días")
    st.table(df)

    # Resaltar ganancia o pérdida
    if resultados["Ganancia neta"] >= 0:
        st.success(f"✅ Ganancia neta después de los días transcurridos: ${resultados['Ganancia neta']:.2f}")
    else:
        st.error(f"⚠️ Pérdida neta después de los días transcurridos: ${resultados['Ganancia neta']:.2f}")
