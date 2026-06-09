"""
Módulo 4 — Digital Twin Orbital
Simulação temporal de degradação de bateria e painéis solares.
"""

import math


def calcular_degradacao_exponencial(valor_inicial, taxa_mensal, meses):
    """
    Aplica decaimento exponencial: V(t) = V0 * e^(-λ * t)
    taxa_mensal: fração de degradação por mês (ex: 0.02 = 2%)
    """
    return valor_inicial * math.exp(-taxa_mensal * meses)


def simular_missao_temporal(metricas, duracao_meses=12):
    """
    Simula a evolução da missão ao longo dos meses.
    Retorna lista com estado mensal do satélite virtual.
    """
    bateria_inicial_wh = 10.0
    painel_inicial_w = metricas["geracao_w"]
    consumo_w = metricas["consumo_w"]

    taxa_bateria = 0.025
    taxa_painel = 0.008

    timeline = []

    for mes in range(duracao_meses + 1):
        capacidade_bateria = calcular_degradacao_exponencial(
            bateria_inicial_wh, taxa_bateria, mes
        )
        geracao_painel = calcular_degradacao_exponencial(
            painel_inicial_w, taxa_painel, mes
        )
        margem = geracao_painel - consumo_w

        horas_autonomia = 0
        if consumo_w > 0 and capacidade_bateria > 0:
            horas_autonomia = round((capacidade_bateria / consumo_w) * 0.8, 1)

        if margem < 0:
            status = "FALHA_ENERGETICA"
        elif margem < 0.3:
            status = "DEGRADADO"
        elif mes > metricas.get("vida_util_minima_meses", 24):
            status = "FIM_VIDA_UTIL"
        else:
            status = "OPERACIONAL"

        timeline.append(
            {
                "mes": mes,
                "capacidade_bateria_wh": round(capacidade_bateria, 2),
                "geracao_painel_w": round(geracao_painel, 2),
                "consumo_w": consumo_w,
                "margem_energetica_w": round(margem, 2),
                "autonomia_horas": horas_autonomia,
                "status": status,
            }
        )

    return timeline


def comparar_configuracoes(metricas_a, metricas_b, duracao_meses=12):
    """Compara duas configurações de satélite no Digital Twin."""
    timeline_a = simular_missao_temporal(metricas_a, duracao_meses)
    timeline_b = simular_missao_temporal(metricas_b, duracao_meses)

    final_a = timeline_a[-1]
    final_b = timeline_b[-1]

    return {
        "config_a": final_a,
        "config_b": final_b,
        "melhor_autonomia": "A" if final_a["autonomia_horas"] >= final_b["autonomia_horas"] else "B",
        "melhor_margem": "A" if final_a["margem_energetica_w"] >= final_b["margem_energetica_w"] else "B",
    }


def exibir_digital_twin(metricas, duracao_meses=12):
    """Exibe simulação gráfica em texto do Digital Twin."""
    timeline = simular_missao_temporal(metricas, duracao_meses)

    print(f"\n{'=' * 55}")
    print("  DIGITAL TWIN ORBITAL — Simulação Temporal")
    print(f"{'=' * 55}")
    print(f"  Duração simulada: {duracao_meses} meses")
    print(f"  Geração inicial:  {metricas['geracao_w']} W")
    print(f"  Consumo fixo:     {metricas['consumo_w']} W\n")

    print(f"  {'Mês':<5} {'Bateria':<10} {'Painel':<10} {'Margem':<10} {'Autonomia':<12} {'Status'}")
    print(f"  {'-' * 60}")

    for estado in timeline:
        barra_bateria = "█" * int(estado["capacidade_bateria_wh"]) + "░" * (10 - int(estado["capacidade_bateria_wh"]))
        print(
            f"  {estado['mes']:<5} "
            f"{estado['capacidade_bateria_wh']:.1f}Wh{'':<3} "
            f"{estado['geracao_painel_w']:.2f}W{'':<4} "
            f"{estado['margem_energetica_w']:+.2f}W{'':<3} "
            f"{estado['autonomia_horas']:.1f}h{'':<6} "
            f"{estado['status']}"
        )

    meses_operacionais = sum(1 for e in timeline if e["status"] == "OPERACIONAL")
    print(f"\n  Meses em operação nominal: {meses_operacionais}/{duracao_meses}")
    print(f"  Estado final (mês {duracao_meses}): {timeline[-1]['status']}")

    return timeline
