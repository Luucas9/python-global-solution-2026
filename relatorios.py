"""
Geração de relatórios formatados da missão.
"""

from datetime import datetime


def gerar_relatorio_missao(nome_missao, analise, parceiros=None, timeline=None):
    """Gera relatório textual completo da missão."""
    metricas = analise["metricas"]
    score = analise["score"]
    sugestoes = analise["sugestoes"]
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    linhas = [
        "=" * 60,
        "  ORION MISSION OS — Relatório de Missão",
        "=" * 60,
        f"  Missão: {nome_missao}",
        f"  Gerado em: {agora}",
        "",
        "  RESUMO EXECUTIVO",
        f"  Mission Readiness Score: {score}/100",
        f"  Peso total: {metricas['peso_total_g']} g",
        f"  Margem energética: {metricas['margem_energetica_w']} W",
        f"  Custo total: US$ {metricas['custo_total_usd']}",
        "",
        "  DETALHAMENTO DE CUSTOS",
        f"  Componentes: US$ {metricas['custo_componentes_usd']}",
        f"  Lançamento:  US$ {metricas['custo_lancamento_usd']}",
        "",
        "  BALANÇO ENERGÉTICO",
        f"  Geração: {metricas['geracao_w']} W",
        f"  Consumo: {metricas['consumo_w']} W",
        f"  Margem:  {metricas['margem_energetica_w']} W",
        "",
    ]

    if sugestoes:
        linhas.append("  SUGESTÕES DE OTIMIZAÇÃO")
        for i, sug in enumerate(sugestoes, 1):
            linhas.append(f"  {i}. [{sug['tipo'].upper()}] {sug['de']} -> {sug['para']}")
            linhas.append(f"     {sug['beneficio']}")
        linhas.append("")
    else:
        linhas.append("  Configuração sem sugestões críticas de otimização.")
        linhas.append("")

    if parceiros:
        linhas.append("  ORBITSHARE — Parceiros Compatíveis")
        for i, p in enumerate(parceiros[:3], 1):
            missao = p["missao"]
            linhas.append(
                f"  {i}. {missao['equipe']} — {p['compatibilidade']}% compatível"
            )
        linhas.append("")

    if timeline:
        final = timeline[-1]
        linhas.append("  DIGITAL TWIN — Projeção Final")
        linhas.append(f"  Bateria residual: {final['capacidade_bateria_wh']} Wh")
        linhas.append(f"  Geração residual: {final['geracao_painel_w']} W")
        linhas.append(f"  Status: {final['status']}")
        linhas.append("")

    linhas.append("=" * 60)
    return "\n".join(linhas)


def salvar_relatorio(conteudo, nome_arquivo="relatorio_missao.txt"):
    """Salva relatório em arquivo de texto."""
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    return nome_arquivo
