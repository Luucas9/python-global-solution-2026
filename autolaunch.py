"""
Módulo 1 — AutoLaunch Optimizer
Montagem virtual, cálculos e Mission Readiness Score.
"""

from dados import (
    CATALOGO_COMPONENTES,
    CUSTO_LANCAMENTO_POR_KG,
    LIMITE_PESO_GRAMAS,
    ORCAMENTO_PADRAO_USD,
)


def buscar_componente(componente_id):
    """Retorna um componente do catálogo pelo identificador."""
    for componente in CATALOGO_COMPONENTES:
        if componente["id"] == componente_id:
            return componente
    return None


def listar_componentes():
    """Exibe o catálogo de componentes disponíveis."""
    print("\n--- Catálogo de Componentes ---")
    for componente in CATALOGO_COMPONENTES:
        sinal_energia = "gera" if componente["consumo_w"] < 0 else "consome"
        energia = abs(componente["consumo_w"])
        print(
            f"[{componente['id']}] {componente['nome']} | "
            f"{componente['peso_g']}g | {sinal_energia} {energia:.2f}W | "
            f"US$ {componente['custo_usd']}"
        )


def calcular_metricas(componentes_selecionados):
    """
    Calcula peso total, balanço energético e custo da missão.
    Valores negativos em consumo_w representam geração de energia.
    """
    peso_total = 0
    geracao_w = 0
    consumo_w = 0
    custo_componentes = 0
    vida_util_minima = 999

    for componente in componentes_selecionados:
        peso_total += componente["peso_g"]
        if componente["consumo_w"] < 0:
            geracao_w += abs(componente["consumo_w"])
        else:
            consumo_w += componente["consumo_w"]
        custo_componentes += componente["custo_usd"]
        vida_util_minima = min(vida_util_minima, componente["vida_util_meses"])

    margem_energetica = geracao_w - consumo_w
    peso_kg = peso_total / 1000
    custo_lancamento = peso_kg * CUSTO_LANCAMENTO_POR_KG
    custo_total = custo_componentes + custo_lancamento

    return {
        "peso_total_g": peso_total,
        "peso_kg": round(peso_kg, 3),
        "geracao_w": round(geracao_w, 2),
        "consumo_w": round(consumo_w, 2),
        "margem_energetica_w": round(margem_energetica, 2),
        "custo_componentes_usd": custo_componentes,
        "custo_lancamento_usd": round(custo_lancamento, 2),
        "custo_total_usd": round(custo_total, 2),
        "vida_util_minima_meses": vida_util_minima,
    }


def calcular_mission_readiness_score(metricas, orcamento=ORCAMENTO_PADRAO_USD):
    """
    Gera um índice de 0 a 100 ponderando peso, energia, custo e vida útil.
    """
    # Peso: quanto mais abaixo do limite, melhor
    if metricas["peso_total_g"] <= LIMITE_PESO_GRAMAS:
        folga_peso = LIMITE_PESO_GRAMAS - metricas["peso_total_g"]
        score_peso = min(100, 60 + (folga_peso / LIMITE_PESO_GRAMAS) * 40)
    else:
        excesso = metricas["peso_total_g"] - LIMITE_PESO_GRAMAS
        score_peso = max(0, 60 - (excesso / LIMITE_PESO_GRAMAS) * 120)

    # Energia: margem positiva é essencial
    if metricas["margem_energetica_w"] >= 0.5:
        score_energia = min(100, 70 + metricas["margem_energetica_w"] * 10)
    elif metricas["margem_energetica_w"] >= 0:
        score_energia = 50 + metricas["margem_energetica_w"] * 40
    else:
        score_energia = max(0, 50 + metricas["margem_energetica_w"] * 50)

    # Custo: compara com orçamento disponível
    if metricas["custo_total_usd"] <= orcamento:
        economia = orcamento - metricas["custo_total_usd"]
        score_custo = min(100, 65 + (economia / orcamento) * 35)
    else:
        estouro = metricas["custo_total_usd"] - orcamento
        score_custo = max(0, 65 - (estouro / orcamento) * 80)

    # Vida útil mínima dos componentes
    score_vida = min(100, (metricas["vida_util_minima_meses"] / 36) * 100)

    score_final = (
        score_peso * 0.35
        + score_energia * 0.30
        + score_custo * 0.20
        + score_vida * 0.15
    )
    return round(score_final, 1)


def sugerir_substituicoes(componentes_selecionados, metricas):
    """
    Sugere trocas de componentes para melhorar peso, energia ou custo.
    """
    sugestoes = []

    if metricas["peso_total_g"] > LIMITE_PESO_GRAMAS:
        excesso = metricas["peso_total_g"] - LIMITE_PESO_GRAMAS
        candidatos = sorted(
            [c for c in CATALOGO_COMPONENTES if c not in componentes_selecionados],
            key=lambda c: c["peso_g"],
        )
        for atual in sorted(componentes_selecionados, key=lambda c: c["peso_g"], reverse=True):
            for candidato in candidatos:
                if candidato["categoria"] == atual["categoria"] and candidato["peso_g"] < atual["peso_g"]:
                    reducao = atual["peso_g"] - candidato["peso_g"]
                    sugestoes.append(
                        {
                            "tipo": "peso",
                            "de": atual["nome"],
                            "para": candidato["nome"],
                            "beneficio": f"reduz {reducao}g (excesso atual: {excesso}g)",
                        }
                    )
                    break

    if metricas["margem_energetica_w"] < 0.3:
        for atual in componentes_selecionados:
            if atual["consumo_w"] > 0:
                alternativas = [
                    c
                    for c in CATALOGO_COMPONENTES
                    if c["categoria"] == atual["categoria"]
                    and c["consumo_w"] < atual["consumo_w"]
                    and c not in componentes_selecionados
                ]
                if alternativas:
                    melhor = min(alternativas, key=lambda c: c["consumo_w"])
                    sugestoes.append(
                        {
                            "tipo": "energia",
                            "de": atual["nome"],
                            "para": melhor["nome"],
                            "beneficio": (
                                f"reduz consumo em "
                                f"{atual['consumo_w'] - melhor['consumo_w']:.2f}W"
                            ),
                        }
                    )

    if metricas["custo_total_usd"] > ORCAMENTO_PADRAO_USD:
        for atual in sorted(componentes_selecionados, key=lambda c: c["custo_usd"], reverse=True):
            alternativas = [
                c
                for c in CATALOGO_COMPONENTES
                if c["categoria"] == atual["categoria"]
                and c["custo_usd"] < atual["custo_usd"]
                and c not in componentes_selecionados
            ]
            if alternativas:
                mais_barato = min(alternativas, key=lambda c: c["custo_usd"])
                economia = atual["custo_usd"] - mais_barato["custo_usd"]
                sugestoes.append(
                    {
                        "tipo": "custo",
                        "de": atual["nome"],
                        "para": mais_barato["nome"],
                        "beneficio": f"economiza US$ {economia}",
                    }
                )

    return sugestoes[:5]


def exibir_analise_missao(componentes_selecionados, nome_missao="Missão sem nome"):
    """Exibe relatório completo da análise AutoLaunch."""
    metricas = calcular_metricas(componentes_selecionados)
    score = calcular_mission_readiness_score(metricas)
    sugestoes = sugerir_substituicoes(componentes_selecionados, metricas)

    print(f"\n{'=' * 55}")
    print(f"  AUTOLAUNCH OPTIMIZER — {nome_missao}")
    print(f"{'=' * 55}")
    print(f"  Componentes selecionados: {len(componentes_selecionados)}")
    print(f"  Peso total:             {metricas['peso_total_g']} g ({metricas['peso_kg']} kg)")
    print(f"  Limite CubeSat 1U:      {LIMITE_PESO_GRAMAS} g")
    print(f"  Geração de energia:     {metricas['geracao_w']} W")
    print(f"  Consumo de energia:     {metricas['consumo_w']} W")
    print(f"  Margem energética:      {metricas['margem_energetica_w']} W")
    print(f"  Custo componentes:      US$ {metricas['custo_componentes_usd']}")
    print(f"  Custo lançamento:       US$ {metricas['custo_lancamento_usd']}")
    print(f"  Custo total estimado:   US$ {metricas['custo_total_usd']}")
    print(f"  Vida útil mínima:       {metricas['vida_util_minima_meses']} meses")
    print(f"  MISSION READINESS SCORE: {score}/100")

    status = "APTA" if score >= 70 else "ATENÇÃO" if score >= 50 else "CRÍTICA"
    print(f"  Status da missão:       {status}")

    if sugestoes:
        print("\n  Sugestões de otimização:")
        for i, sug in enumerate(sugestoes, 1):
            print(f"    {i}. [{sug['tipo'].upper()}] Trocar '{sug['de']}' por '{sug['para']}'")
            print(f"       -> {sug['beneficio']}")
    else:
        print("\n  Nenhuma substituição crítica sugerida. Configuração equilibrada.")

    return {"metricas": metricas, "score": score, "sugestoes": sugestoes}
