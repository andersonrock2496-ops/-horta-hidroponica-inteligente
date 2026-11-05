
import math


class AmbienteSimulado:
    def __init__(self):
        self.tempo = 0
        self.temperatura = 26.0
        self.umidade = 70.0

    def atualizar(self, motores):
        # Cada ciclo representa 5 minutos simulados
        self.tempo += 5

        # Temperatura externa simulada
        temperatura_externa = (
            27 + 5 * math.sin(2 * math.pi * self.tempo / 1440)
        )

        # Aquecimento pela diferença térmica
        aquecimento = (
            temperatura_externa - self.temperatura
        ) * 0.08

        # Efeito dos equipamentos
        ventilacao_inferior = any(
            motores.get(f"V{i}", False)
            for i in range(1, 4)
        )

        exaustao = any(
            motores.get(f"E{i}", False)
            for i in range(1, 4)
        )

        circulacao = any(
            motores.get(f"C{i}", False)
            for i in range(1, 4)
        )

        resfriamento = 0

        if ventilacao_inferior and exaustao:
            resfriamento = 0.25
        elif ventilacao_inferior or exaustao:
            resfriamento = 0.10

        # Circulação redistribui o ar, sem resfriamento adicional
        self.temperatura += aquecimento - resfriamento

        # Evolução simplificada da umidade
        self.umidade += 0.15

        if exaustao:
            self.umidade -= 0.5

        self.umidade = max(
            40, min(95, self.umidade)
        )

        return {
            "tempo": self.tempo,
            "temperatura": round(self.temperatura, 2),
            "umidade": round(self.umidade, 2),
            "circulacao": circulacao
        }
