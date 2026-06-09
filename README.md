# ORION Mission OS — Python

Plataforma de inteligencia de missoes espaciais para planejamento e validacao de CubeSats.

**Disciplina:** Computational Thinking with Python — FIAP · Global Solution 2026

## Sobre o Projeto

O ORION Mission OS democratiza o planejamento de CubeSats com quatro modulos integrados: montagem virtual, matching orbital, telemetria simulada e digital twin. Tudo executado via terminal em Python puro.

## Equipe

| Nome | RM |
|------|-----|
| Luiz Ademario | 571182 |
| Gustavo Noleto | 569592 |
| Lucas Gaspar | 568616 |

## Estrutura de Pastas

```
DISCIPLINA PYTHON/
├── main.py
├── dados.py
├── autolaunch.py
├── orbitshare.py
├── telemetria.py
├── digital_twin.py
├── relatorios.py
└── README.md
```

## Menu Principal

| Opcao | Funcionalidade |
|-------|----------------|
| 1 | AutoLaunch Optimizer — montar e analisar CubeSat |
| 2 | OrbitShare — buscar parceiros de lancamento |
| 3 | Telemetria Inteligente — monitoramento simulado |
| 4 | Digital Twin Orbital — simulacao temporal |
| 5 | Jornada completa (todos os modulos + relatorio) |
| 6 | Descricao da solucao (max. 5 linhas) |
| 7 | Ver equipe do projeto |
| 0 | Sair |

## Como Executar

**Requisitos:** Python 3.10 ou superior. Nao exige bibliotecas externas para rodar o sistema.

```bash
cd "DISCIPLINA PYTHON"
python main.py
```

**Exemplo de componentes (opcao 1):**

```
painel_solar_b,bateria_li_b,sensor_temp,antena_uhf,radio_uhf,obc_basico
```

Ao final da jornada completa (opcao 5), e possivel salvar um relatorio em `.txt`.

## Modulos

- **autolaunch.py** — Mission Readiness Score, metricas e sugestoes de otimizacao
- **orbitshare.py** — compatibilidade orbital e custo compartilhado (rideshare)
- **telemetria.py** — leituras simuladas, status e alertas preditivos
- **digital_twin.py** — degradacao exponencial de bateria e paineis solares
- **relatorios.py** — geracao e salvamento de relatorios formatados
- **dados.py** — catalogo de componentes, missoes e integrantes

## Tecnologias

- Python 3.10+
- Listas, dicionarios, funcoes, if/elif, while, for

## Licenca

Projeto academico — FIAP 2026.
