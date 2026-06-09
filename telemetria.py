"""
Módulo 3 — Telemetria Inteligente
Monitoramento simulado e alertas preditivos.
"""

import random

# Histórico de leituras para análise de tendência
_historico_leituras = []


def simular_leitura(ciclo, temperatura_base=22.0, bateria_inicial=100.0):
    """
    Simula uma leitura de telemetria para um ciclo da missão.
    A bateria degrada gradualmente e a temperatura varia com o ciclo orbital.
    """
    degradacao_bateria = ciclo * random.uniform(0.8, 1.4)
    variacao_temp = random.uniform(-3.0, 8.0)
    temperatura = round(temperatura_base + variacao_temp, 1)
    bateria = round(max(0, bateria_inicial - degradacao_bateria), 1)
    energia_gerada = round(random.uniform(1.5, 2.8), 2)
    energia_consumida = round(random.uniform(1.2, 2.5), 2)

    leitura = {
        "ciclo": ciclo,
        "temperatura_c": temperatura,
        "bateria_pct": bateria,
        "energia_gerada_w": energia_gerada,
        "energia_consumida_w": energia_consumida,
    }
    return leitura


def classificar_status(leitura):
    """Classifica o status da missão com base nos limites operacionais."""
    bateria = leitura["bateria_pct"]
    temperatura = leitura["temperatura_c"]

    match True:
        case _ if bateria < 15 or temperatura > 55:
            return "CRITICO"
        case _ if bateria < 30 or temperatura > 45:
            return "ALERTA"
        case _:
            return "NOMINAL"


def analisar_tendencia_bateria(historico, janela=5):
    """
    Analisa a queda média de bateria por ciclo nas últimas leituras.
    Retorna alerta preditivo se a degradação estiver acima do normal.
    """
    if len(historico) < 2:
        return None

    amostra = historico[-janela:] if len(historico) >= janela else historico
    quedas = []
    for i in range(1, len(amostra)):
        queda = amostra[i - 1]["bateria_pct"] - amostra[i]["bateria_pct"]
        quedas.append(queda)

    if not quedas:
        return None

    queda_media = sum(quedas) / len(quedas)
    limite_normal = 1.5

    if queda_media > limite_normal:
        bateria_atual = amostra[-1]["bateria_pct"]
        ciclos_ate_critico = (bateria_atual - 15) / queda_media if queda_media > 0 else 999
        dias_estimados = round(ciclos_ate_critico * 1.5)

        return {
            "tipo": "PREDITIVO",
            "mensagem": (
                f"Bateria caindo {queda_media:.1f}% por ciclo acima do normal "
                f"(limite: {limite_normal}%)"
            ),
            "risco": f"Risco de falha em aproximadamente {dias_estimados} dias",
            "queda_media_pct": round(queda_media, 2),
        }

    return None


def executar_ciclo_telemetria(ciclo):
    """Executa um ciclo de telemetria e retorna leitura com status."""
    global _historico_leituras

    leitura = simular_leitura(ciclo)
    leitura["status"] = classificar_status(leitura)
    _historico_leituras.append(leitura)

    alerta_preditivo = analisar_tendencia_bateria(_historico_leituras)
    if alerta_preditivo:
        leitura["alerta_preditivo"] = alerta_preditivo

    return leitura


def exibir_painel_telemetria(num_ciclos=10):
    """Simula múltiplos ciclos de telemetria e exibe painel."""
    global _historico_leituras
    _historico_leituras = []

    print(f"\n{'=' * 55}")
    print("  TELEMETRIA INTELIGENTE — Monitoramento Simulado")
    print(f"{'=' * 55}")
    print(f"  Simulando {num_ciclos} ciclos orbitais...\n")
    print(f"  {'Ciclo':<6} {'Temp(°C)':<10} {'Bateria':<10} {'Status':<10} {'LED'}")
    print(f"  {'-' * 50}")

    alertas = []

    for ciclo in range(1, num_ciclos + 1):
        leitura = executar_ciclo_telemetria(ciclo)
        led = "VERDE" if leitura["status"] == "NOMINAL" else "VERMELHO"

        print(
            f"  {leitura['ciclo']:<6} "
            f"{leitura['temperatura_c']:<10} "
            f"{leitura['bateria_pct']}%{'':<6} "
            f"{leitura['status']:<10} "
            f"{led}"
        )

        if "alerta_preditivo" in leitura:
            alertas.append(leitura["alerta_preditivo"])

    if alertas:
        print("\n  Alertas preditivos detectados:")
        for alerta in alertas:
            print(f"    [!] {alerta['mensagem']}")
            print(f"      -> {alerta['risco']}")
    else:
        print("\n  Nenhum padrão de degradação anormal detectado.")

    return _historico_leituras
