
import math
import random


class SimuladorLuminosidade:
    def __init__(self):
        self.tempo = 0

    def atualizar(self, tempo_minutos, abertura_sombrite):
        self.tempo = tempo_minutos

        # Dia simulado: 06:00 ate 18:00
        hora = (tempo_minutos % 1440) / 60

        if 6 <= hora <= 18:
            fator_solar = math.sin(
                math.pi * (hora - 6) / 12
            )
        else:
            fator_solar = 0.0

        # Luz externa, com pequena variacao
        luz_externa = max(
            0,
            60000 * fator_solar
            + random.uniform(-500, 500)
        )

        # Abertura 100% = sombrite recolhido
        # Abertura 0% = sombrite totalmente estendido
        transmissao = 0.30 + 0.60 * (
            abertura_sombrite / 100
        )

        luz_interna = luz_externa * transmissao

        return {
            "hora": round(hora, 2),
            "L1": round(luz_externa, 2),
            "L2": round(luz_interna, 2),
            "abertura": abertura_sombrite
        }
