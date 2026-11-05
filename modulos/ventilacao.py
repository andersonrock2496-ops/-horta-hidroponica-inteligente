
from simuladores.motores import SistemaVentilacao

from configuracao import (
    TEMPERATURA_MAXIMA,
    TEMPERATURA_DESLIGAMENTO,
    UMIDADE_MAXIMA,
    UMIDADE_DESLIGAMENTO,
    DIFERENCA_VERTICAL_LIGAR,
    DIFERENCA_VERTICAL_DESLIGAR
)


class ControleVentilacao:
    def __init__(self):
        self.motores = SistemaVentilacao()

        self.alerta_temperatura = False
        self.alerta_umidade = False
        self.alerta_estratificacao = False

    def processar(self, leituras):
        temperaturas = [
            sensor["temperatura"]
            for sensor in leituras.values()
        ]

        umidades = [
            sensor["umidade"]
            for sensor in leituras.values()
        ]

        media_temperatura = sum(temperaturas) / len(temperaturas)
        media_umidade = sum(umidades) / len(umidades)

        superior = sum(
            leituras[f"TH_superior_{local}"]["temperatura"]
            for local in ["A", "B", "C"]
        ) / 3

        inferior = sum(
            leituras[f"TH_inferior_{local}"]["temperatura"]
            for local in ["A", "B", "C"]
        ) / 3

        diferenca_vertical = superior - inferior

        # Histerese da temperatura
        if media_temperatura >= TEMPERATURA_MAXIMA:
            self.alerta_temperatura = True
        elif media_temperatura <= TEMPERATURA_DESLIGAMENTO:
            self.alerta_temperatura = False

        # Histerese da umidade
        if media_umidade >= UMIDADE_MAXIMA:
            self.alerta_umidade = True
        elif media_umidade <= UMIDADE_DESLIGAMENTO:
            self.alerta_umidade = False

        # Histerese da estratificação térmica
        if diferenca_vertical >= DIFERENCA_VERTICAL_LIGAR:
            self.alerta_estratificacao = True
        elif diferenca_vertical <= DIFERENCA_VERTICAL_DESLIGAR:
            self.alerta_estratificacao = False

        # Insuflação e exaustão
        ventilacao_ativa = (
            self.alerta_temperatura
            or self.alerta_umidade
        )

        self.motores.acionar_inferiores(ventilacao_ativa)
        self.motores.acionar_exaustores(ventilacao_ativa)

        # Circulação superior
        circulacao_ativa = (
            self.alerta_estratificacao
            or self.alerta_temperatura
        )

        self.motores.acionar_superiores(circulacao_ativa)

        return {
            "temperatura_media": round(media_temperatura, 2),
            "umidade_media": round(media_umidade, 2),
            "diferenca_vertical": round(diferenca_vertical, 2),
            "motores": self.motores.consultar_estado()
        }
