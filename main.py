"""
ORION Mission OS — Sistema principal (menu interativo via terminal)
Global Solution 2026 · FIAP · Computational Thinking with Python
"""

from autolaunch import (
    buscar_componente,
    exibir_analise_missao,
    listar_componentes,
)
from dados import INTEGRANTES, LIMITE_PESO_GRAMAS
from digital_twin import exibir_digital_twin
from orbitshare import exibir_matching
from relatorios import gerar_relatorio_missao, salvar_relatorio
from telemetria import exibir_painel_telemetria


def exibir_cabecalho():
    print("\n" + "=" * 55)
    print("       ORION MISSION OS — Mission Intelligence Layer")
    print("       Do componente ao espaço. Sem desperdício.")
    print("=" * 55)


def exibir_equipe():
    print("\n--- Equipe do Projeto ---")
    for integrante in INTEGRANTES:
        print(f"  {integrante['nome']} (RM {integrante['rm']})")


def exibir_descricao_solucao():
    """Descrição textual da solução (máximo 5 linhas)."""
    print("\n--- Descrição da Solução ---")
    print("ORION Mission OS valida CubeSats antes do lançamento orbital.")
    print("Integra montagem virtual, matching orbital e telemetria simulada.")
    print("Simula degradação energética e gera relatórios no terminal.")
    print("Democratiza o acesso ao espaço para universidades e startups.")
    print("Desenvolvido em Python com funções, listas e estruturas de decisão.")


def montar_missao_interativa():
    """Fluxo interativo de montagem de CubeSat no AutoLaunch Optimizer."""
    listar_componentes()
    print(f"\nLimite de peso CubeSat 1U: {LIMITE_PESO_GRAMAS} g")
    print("Digite os IDs dos componentes separados por vírgula.")
    print("Exemplo: painel_solar_b,bateria_li_b,sensor_temp,antena_uhf,radio_uhf,obc_basico")

    entrada = input("\nIDs dos componentes: ").strip()
    if not entrada:
        print("Nenhum componente informado.")
        return None, None

    ids = [item.strip() for item in entrada.split(",")]
    componentes = []
    for componente_id in ids:
        componente = buscar_componente(componente_id)
        if componente:
            componentes.append(componente)
        else:
            print(f"  Aviso: componente '{componente_id}' não encontrado.")

    if not componentes:
        print("Montagem inválida.")
        return None, None

    nome = input("Nome da missão: ").strip() or "Missão FIAP CubeSat"
    analise = exibir_analise_missao(componentes, nome)
    return nome, analise


def configurar_orbitshare(analise):
    """Configura missão do usuário para busca de parceiros no OrbitShare."""
    if not analise:
        print("Execute primeiro o AutoLaunch Optimizer.")
        return None, None

    print("\n--- Configurar missão para OrbitShare ---")
    orbita = input("Órbita alvo (ex: SSO 500km): ").strip() or "SSO 500km"

    inclinacao_texto = input("Inclinação em graus (ex: 97.4): ").strip()
    if inclinacao_texto:
        try:
            inclinacao = float(inclinacao_texto.replace(",", "."))
        except ValueError:
            print("Inclinação inválida. Usando valor padrão: 97.4")
            inclinacao = 97.4
    else:
        inclinacao = 97.4

    janela = input("Janela de lançamento (ex: 2026-Q3): ").strip() or "2026-Q3"

    missao_usuario = {
        "id": "mis_usuario",
        "equipe": "Sua equipe",
        "orbita_alvo": orbita,
        "inclinacao_graus": inclinacao,
        "janela_lancamento": janela,
    }

    massa_kg = analise["metricas"]["peso_kg"]
    custo_lancamento = analise["metricas"]["custo_lancamento_usd"]
    parceiros = exibir_matching(missao_usuario, massa_kg, custo_lancamento)
    return missao_usuario, parceiros


def executar_jornada_completa():
    """Demonstra o fluxo integrado dos quatro módulos."""
    print("\n>>> JORNADA COMPLETA: AutoLaunch -> OrbitShare -> Telemetria -> Digital Twin")

    nome, analise = montar_missao_interativa()
    if not analise:
        return

    _, parceiros = configurar_orbitshare(analise)
    exibir_painel_telemetria(8)
    timeline = exibir_digital_twin(analise["metricas"], duracao_meses=12)

    relatorio = gerar_relatorio_missao(nome, analise, parceiros, timeline)
    print("\n" + relatorio)

    salvar = input("\nSalvar relatório em arquivo? (s/n): ").strip().lower()
    if salvar == "s":
        arquivo = salvar_relatorio(relatorio)
        print(f"Relatório salvo em: {arquivo}")


def exibir_menu():
    print("\n--- Menu Principal ---")
    print("  Aviso: use a opção 1 antes das opções 2 e 4.")
    print("  Sem montar a missão na opção 1, as próximas etapas não funcionam.")
    print("  A opção 5 executa todo o fluxo automaticamente (1 -> 2 -> 3 -> 4).")
    print("  1. AutoLaunch Optimizer (montar e analisar CubeSat)")
    print("  2. OrbitShare (buscar parceiros de lançamento)")
    print("  3. Telemetria Inteligente (monitoramento simulado)")
    print("  4. Digital Twin Orbital (simulação temporal)")
    print("  5. Jornada completa (todos os módulos)")
    print("  6. Descrição da solução")
    print("  7. Ver equipe do projeto")
    print("  0. Sair")


def main():
    analise_atual = None
    nome_missao_atual = "Missão FIAP CubeSat"

    exibir_cabecalho()

    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        match opcao:
            case "1":
                nome, analise = montar_missao_interativa()
                if analise:
                    analise_atual = analise
                    nome_missao_atual = nome

            case "2":
                configurar_orbitshare(analise_atual)

            case "3":
                ciclos_texto = input("Quantos ciclos simular? (padrão 10): ").strip()
                ciclos = int(ciclos_texto) if ciclos_texto.isdigit() else 10
                exibir_painel_telemetria(ciclos)

            case "4":
                if not analise_atual:
                    print("\nMonte uma missão primeiro (opção 1) ou use a demonstração padrão.")
                    from autolaunch import calcular_metricas, buscar_componente as bc

                    demo = [
                        bc("painel_solar_b"),
                        bc("bateria_li_a"),
                        bc("sensor_temp"),
                        bc("antena_uhf"),
                        bc("radio_uhf"),
                        bc("obc_basico"),
                    ]
                    analise_atual = {"metricas": calcular_metricas(demo)}

                meses_texto = input("Duração em meses (padrão 12): ").strip()
                meses = int(meses_texto) if meses_texto.isdigit() else 12
                exibir_digital_twin(analise_atual["metricas"], duracao_meses=meses)

            case "5":
                executar_jornada_completa()

            case "6":
                exibir_descricao_solucao()

            case "7":
                exibir_equipe()

            case "0":
                print("\nEncerrando ORION Mission OS. Boa missão!")
                break

            case _:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
