
import random


def ler_termohigrometros(ambiente=None):
    sensores = {}

    niveis = {
        "superior": 1.5,
        "intermediario": 0.5,
        "inferior": -0.5
    }

    locais = ["A", "B", "C"]

    temperatura_base = (
        ambiente["temperatura"]
        if ambiente else 26.0
    )

    umidade_base = (
        ambiente["umidade"]
        if ambiente else 70.0
    )

    circulacao = (
        ambiente.get("circulacao", False)
        if ambiente else False
    )

    # A circulação reduz a estratificação térmica
    fator_estratificacao = 0.3 if circulacao else 1.0

    for nivel, variacao in niveis.items():
        for local in locais:
            identificador = f"TH_{nivel}_{local}"

            temperatura = (
                temperatura_base
                + variacao * fator_estratificacao
                + random.uniform(-0.2, 0.2)
            )

            umidade = (
                umidade_base
                + random.uniform(-1, 1)
            )

            sensores[identificador] = {
                "temperatura": round(temperatura, 2),
                "umidade": round(umidade, 2)
            }

    return sensores
