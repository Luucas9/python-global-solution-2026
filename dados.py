"""
Dados base do ORION Mission OS.
Parâmetros inspirados em especificações reais de CubeSat 1U.
"""

INTEGRANTES = [
    {
        "nome": "Luiz Ademario",
        "rm": "571182",
    },
    {
        "nome": "Gustavo Noleto",
        "rm": "569592",
    },
    {
        "nome": "Lucas Gaspar",
        "rm": "568616",
    },
]

# Limites de referência para CubeSat 1U
LIMITE_PESO_GRAMAS = 1200
CUSTO_LANCAMENTO_POR_KG = 10000  # USD — média entre US$ 5k e US$ 15k
ORCAMENTO_PADRAO_USD = 50000

# Catálogo de componentes disponíveis para montagem virtual
CATALOGO_COMPONENTES = [
    {
        "id": "painel_solar_a",
        "nome": "Painel Solar Compacto",
        "categoria": "energia",
        "peso_g": 45,
        "consumo_w": -1.8,
        "custo_usd": 1200,
        "vida_util_meses": 24,
    },
    {
        "id": "painel_solar_b",
        "nome": "Painel Solar Alta Eficiência",
        "categoria": "energia",
        "peso_g": 62,
        "consumo_w": -2.4,
        "custo_usd": 2100,
        "vida_util_meses": 36,
    },
    {
        "id": "bateria_li_a",
        "nome": "Bateria Li-ion 2.5Ah",
        "categoria": "energia",
        "peso_g": 95,
        "consumo_w": 0.0,
        "custo_usd": 800,
        "vida_util_meses": 18,
    },
    {
        "id": "bateria_li_b",
        "nome": "Bateria Li-ion 4.0Ah",
        "categoria": "energia",
        "peso_g": 140,
        "consumo_w": 0.0,
        "custo_usd": 1350,
        "vida_util_meses": 24,
    },
    {
        "id": "sensor_temp",
        "nome": "Sensor de Temperatura DHT",
        "categoria": "sensor",
        "peso_g": 12,
        "consumo_w": 0.05,
        "custo_usd": 45,
        "vida_util_meses": 36,
    },
    {
        "id": "sensor_gyro",
        "nome": "Sensor Giroscópio 3-eixos",
        "categoria": "sensor",
        "peso_g": 18,
        "consumo_w": 0.12,
        "custo_usd": 320,
        "vida_util_meses": 30,
    },
    {
        "id": "antena_uhf",
        "nome": "Antena UHF Dipolo",
        "categoria": "comunicacao",
        "peso_g": 28,
        "consumo_w": 0.0,
        "custo_usd": 180,
        "vida_util_meses": 48,
    },
    {
        "id": "radio_uhf",
        "nome": "Rádio UHF 1W",
        "categoria": "comunicacao",
        "peso_g": 55,
        "consumo_w": 1.1,
        "custo_usd": 950,
        "vida_util_meses": 36,
    },
    {
        "id": "obc_basico",
        "nome": "Computador de Bordo Básico",
        "categoria": "computacao",
        "peso_g": 40,
        "consumo_w": 0.35,
        "custo_usd": 600,
        "vida_util_meses": 48,
    },
    {
        "id": "obc_avancado",
        "nome": "Computador de Bordo Avançado",
        "categoria": "computacao",
        "peso_g": 58,
        "consumo_w": 0.55,
        "custo_usd": 1100,
        "vida_util_meses": 48,
    },
]

# Missões de exemplo para o módulo OrbitShare
MISSOES_EXEMPLO = [
    {
        "id": "mis_001",
        "equipe": "UFABC Space Lab",
        "orbita_alvo": "SSO 500km",
        "inclinacao_graus": 97.4,
        "janela_lancamento": "2026-Q3",
        "massa_kg": 1.1,
        "capacidade_disponivel_kg": 0.4,
    },
    {
        "id": "mis_002",
        "equipe": "INPE NanoSat",
        "orbita_alvo": "SSO 550km",
        "inclinacao_graus": 97.8,
        "janela_lancamento": "2026-Q3",
        "massa_kg": 0.9,
        "capacidade_disponivel_kg": 0.6,
    },
    {
        "id": "mis_003",
        "equipe": "TechStars Orbital",
        "orbita_alvo": "LEO 400km",
        "inclinacao_graus": 51.6,
        "janela_lancamento": "2026-Q4",
        "massa_kg": 1.2,
        "capacidade_disponivel_kg": 0.2,
    },
    {
        "id": "mis_004",
        "equipe": "MIT CubeSat Club",
        "orbita_alvo": "SSO 500km",
        "inclinacao_graus": 97.5,
        "janela_lancamento": "2027-Q1",
        "massa_kg": 1.0,
        "capacidade_disponivel_kg": 0.5,
    },
]
