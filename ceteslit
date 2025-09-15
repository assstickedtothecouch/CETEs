import streamlit as st

# Función de cálculo CETES
def calculadora_cetes(monto, tasa, dt, plazo):
    VN = 10.0
    base = 360.0

    if tasa > 1:
        tasa = tasa / 100.0

    if dt < 0:
        dt = 0

    Pc = VN / (1 + tasa * (plazo / base))
    titulos = monto / Pc
    plazos_equivalentes = base / plazo
    VN_total = titulos * VN
    Dv = max(plazo - dt, 0)
    Pr = VN / (1 + tasa * (Dv / base))
    Mf_plazo = (VN_total / VN) * Pr
    tasa_plazo = (Mf_plazo / monto) - 1 if monto != 0 else 0
    Mf_anual = monto * (1 + tasa_plazo) ** plazos_equivalentes
    ganancia = Mf_plazo - monto

    return {
        "Plazo (días)": int(plazo),
        "Precio de compra (Pc)": Pc,
        "Títulos adquiridos": titulos,
        "Plazos equivalentes (360/P)": plazos_equivalentes,
        "Valor Nominal Total (VN_total)": VN_total,
        "Días a vencimiento (Dv)": int(Dv),
        "Precio ajustado (Pr)": Pr,
        "Monto final al plazo (Mf_plazo)": Mf_plazo,
        "Tasa efectiva del plazo": tasa_plazo,
        "Monto final anual (M*(1+T_plazo)^P)": Mf_anual,
        "Ganancia neta en el plazo": ganancia
    }

# Streamlit App
st.title("Calculadora CETES")

# Entradas
monto = st.number_input("Monto a invertir", min_value=0.0, value=10000.0)
tasa = st.number_input("Tasa anual (%)", min_value=0.0, value=7.35)
dt = st.number_input("Días transcurridos (DT)", min_value=0, value=0)
plazo = st.selectbox("Plazo (días)", [28, 91, 182, 364, 728])

# Botón de cálculo
if st.button("Calcular"):
    resultados = calculadora_cetes(monto, tasa, dt, plazo)
    st.subheader(f"Resultados CETES {plazo} días")
    for k, v in resultados.items():
        if isinstance(v, float):
            st.write(f"{k}: {v:,.2f}")
        else:
            st.write(f"{k}: {v}")
