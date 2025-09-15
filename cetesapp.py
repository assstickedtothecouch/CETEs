def calculadora_cetes(monto, tasa, dt, plazo):
    """
    Calculadora CETES para plazos: 28, 91, 182, 364, 728 (base 360).
    monto: monto a invertir (float)
    tasa: tasa anual (puede ingresarse como 0.0735 o 7.35)
    dt: días transcurridos (DT) (int)
    plazo: plazo en días (int) - uno de 28,91,182,364,728
    """
    # Constantes
    VN = 10.0
    base = 360.0

    # Ajuste si el usuario mete porcentaje en lugar de decimal
    if tasa > 1:
        tasa = tasa / 100.0

    # No permitir días negativos
    if dt < 0:
        dt = 0

    # Precio de compra
    Pc = VN / (1 + tasa * (plazo / base))

    # Títulos adquiridos
    titulos = monto / Pc

    # Plazos equivalentes en un año
    plazos_equivalentes = base / plazo

    # Valor nominal total al vencimiento
    VN_total = titulos * VN

    # Días a vencimiento ajustados
    Dv = max(plazo - dt, 0)

    # Precio ajustado
    Pr = VN / (1 + tasa * (Dv / base))

    # Monto final al plazo
    Mf_plazo = (VN_total / VN) * Pr

    # Tasa efectiva del plazo
    tasa_plazo = (Mf_plazo / monto) - 1 if monto != 0 else 0

    # ✅ Fórmula corregida: Monto final anual = M*(1+T_plazo)^P
    Mf_anual = monto * (1 + tasa_plazo) ** plazos_equivalentes

    # Ganancia neta
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


def menu():
    plazos = {
        1: 28,
        2: 91,
        3: 182,
        4: 364,
        5: 728
    }

    print("=== Calculadora CETES ===")
    print("1) CETES 28 días")
    print("2) CETES 91 días")
    print("3) CETES 182 días")
    print("4) CETES 364 días")
    print("5) CETES 728 días")

    try:
        opcion = int(input("Elige una opción (1-5): ").strip())
    except ValueError:
        print("Opción inválida.")
        return

    if opcion not in plazos:
        print("Opción inválida.")
        return

    try:
        monto = float(input("Monto a invertir: ").replace(",", "").strip())
        tasa = float(input("Tasa anual (ej. 0.0735 o 7.35): ").strip())
        dt = int(input("Días transcurridos (DT): ").strip())
    except ValueError:
        print("Entrada inválida. Asegúrate de introducir números válidos.")
        return

    plazo = plazos[opcion]
    resultados = calculadora_cetes(monto, tasa, dt, plazo)

    print(f"\n--- Resultados CETES {plazo} días ---")
    for k, v in resultados.items():
        if isinstance(v, float):
            print(f"{k}: {v:,.2f}")
        else:
            print(f"{k}: {v}")


if __name__ == "__main__":
    menu()