"""
Módulo 2 — OrbitShare
Matching orbital com índice de compatibilidade entre missões.
"""

from dados import MISSOES_EXEMPLO

JANELAS_COMPATIVEIS = {
    "2026-Q3": ["2026-Q3", "2026-Q4"],
    "2026-Q4": ["2026-Q3", "2026-Q4", "2027-Q1"],
    "2027-Q1": ["2026-Q4", "2027-Q1"],
}


def extrair_tipo_orbita(orbita_alvo):
    """Extrai o tipo orbital (SSO, LEO, etc.) da string de órbita."""
    return orbita_alvo.split()[0].upper()


def extrair_altitude(orbita_alvo):
    """Extrai altitude em km da string de órbita."""
    for parte in orbita_alvo.split():
        if parte.endswith("km"):
            return int(parte.replace("km", ""))
    return 500


def calcular_compatibilidade(missao_usuario, missao_cadastrada, massa_usuario_kg):
    """
    Calcula percentual de compatibilidade entre duas missões.
    Considera órbita, inclinação, janela de lançamento e capacidade de massa.
    """
    if missao_usuario["id"] == missao_cadastrada["id"]:
        return 0

    score = 0

    # Compatibilidade orbital (40%)
    tipo_usuario = extrair_tipo_orbita(missao_usuario["orbita_alvo"])
    tipo_parceiro = extrair_tipo_orbita(missao_cadastrada["orbita_alvo"])
    if tipo_usuario == tipo_parceiro:
        alt_usuario = extrair_altitude(missao_usuario["orbita_alvo"])
        alt_parceiro = extrair_altitude(missao_cadastrada["orbita_alvo"])
        diff_alt = abs(alt_usuario - alt_parceiro)
        if diff_alt <= 50:
            score += 40
        elif diff_alt <= 150:
            score += 25
        else:
            score += 10

    # Inclinação orbital (25%)
    diff_incl = abs(
        missao_usuario["inclinacao_graus"] - missao_cadastrada["inclinacao_graus"]
    )
    if diff_incl <= 1:
        score += 25
    elif diff_incl <= 3:
        score += 18
    elif diff_incl <= 5:
        score += 10

    # Janela de lançamento (20%)
    janela_usuario = missao_usuario["janela_lancamento"]
    janela_parceiro = missao_cadastrada["janela_lancamento"]
    janelas_ok = JANELAS_COMPATIVEIS.get(janela_usuario, [janela_usuario])
    if janela_parceiro in janelas_ok:
        score += 20
    elif janela_parceiro in JANELAS_COMPATIVEIS.get(janela_parceiro, []):
        score += 10

    # Capacidade de massa no veículo (15%)
    if massa_usuario_kg <= missao_cadastrada["capacidade_disponivel_kg"]:
        score += 15
    elif massa_usuario_kg <= missao_cadastrada["capacidade_disponivel_kg"] * 1.2:
        score += 8

    return round(min(score, 100), 1)


def calcular_custo_compartilhado(custo_total_lancamento, numero_participantes):
    """Divide o custo do lançamento entre os participantes do rideshare."""
    if numero_participantes <= 0:
        return custo_total_lancamento
    return round(custo_total_lancamento / numero_participantes, 2)


def buscar_parceiros(missao_usuario, massa_usuario_kg, banco_missões=None):
    """
    Retorna lista de missões compatíveis ordenadas por índice de compatibilidade.
    """
    if banco_missões is None:
        banco_missões = MISSOES_EXEMPLO

    resultados = []
    for missao in banco_missões:
        compatibilidade = calcular_compatibilidade(missao_usuario, missao, massa_usuario_kg)
        if compatibilidade >= 40:
            resultados.append(
                {
                    "missao": missao,
                    "compatibilidade": compatibilidade,
                }
            )

    return sorted(resultados, key=lambda r: r["compatibilidade"], reverse=True)


def exibir_matching(missao_usuario, massa_usuario_kg, custo_lancamento_usd):
    """Exibe resultados do algoritmo de matching orbital."""
    parceiros = buscar_parceiros(missao_usuario, massa_usuario_kg)

    print(f"\n{'=' * 55}")
    print("  ORBITSHARE — Matching Orbital")
    print(f"{'=' * 55}")
    print(f"  Sua missão:     {missao_usuario.get('equipe', 'Sua equipe')}")
    print(f"  Órbita alvo:    {missao_usuario['orbita_alvo']}")
    print(f"  Inclinação:     {missao_usuario['inclinacao_graus']}°")
    print(f"  Janela:         {missao_usuario['janela_lancamento']}")
    print(f"  Massa:          {massa_usuario_kg} kg")
    print(f"  Custo lançamento (individual): US$ {custo_lancamento_usd}")

    if not parceiros:
        print("\n  Nenhum parceiro compatível encontrado no banco de missões.")
        return []

    print(f"\n  {len(parceiros)} parceiro(s) compatível(is) encontrado(s):\n")

    for i, resultado in enumerate(parceiros, 1):
        missao = resultado["missao"]
        compat = resultado["compatibilidade"]
        participantes = 2
        custo_dividido = calcular_custo_compartilhado(custo_lancamento_usd, participantes)
        economia = custo_lancamento_usd - custo_dividido

        print(f"  {i}. {missao['equipe']} — Compatibilidade: {compat}%")
        print(f"     Órbita: {missao['orbita_alvo']} | Janela: {missao['janela_lancamento']}")
        print(f"     Capacidade disponível: {missao['capacidade_disponivel_kg']} kg")
        print(f"     Custo compartilhado (2 equipes): US$ {custo_dividido}")
        print(f"     Economia estimada: US$ {economia} ({round(economia/custo_lancamento_usd*100, 1)}%)")
        print()

    return parceiros
