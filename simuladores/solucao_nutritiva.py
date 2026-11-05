
class SimuladorSolucaoNutritiva:
    def __init__(self):
        self.capacidade = 200.0
        self.volume = 180.0
        self.ph = 5.8
        self.ec = 1.5
        self.temperatura = 22.0
        self.vazao_nominal = 2.0

        # Estoques abstratos, apenas para simulacao
        self.estoques = {
            "D1": 100,
            "D2": 100,
            "D3": 100,
            "D4": 100
        }

    def atualizar(self, atuadores, minutos=5):
        circulacao = atuadores.get("B1", False)
        reposicao = atuadores.get("B2", False)
        chiller = atuadores.get("CH1", False)

        # Balanco hidrico simplificado
        self.volume -= 0.015 * minutos

        if reposicao:
            self.volume += 0.8 * minutos

        self.volume = max(
            0.0, min(self.capacidade, self.volume)
        )

        # Balanco termico simplificado
        self.temperatura += 0.015 * minutos

        if chiller:
            self.temperatura -= 0.05 * minutos

        # Derivas naturais simuladas
        self.ph += 0.0005 * minutos
        self.ec += 0.0002 * minutos

        if reposicao:
            self.ec -= 0.001 * minutos

        self.ph = max(0.0, min(14.0, self.ph))
        self.ec = max(0.0, self.ec)

        vazao = (
            self.vazao_nominal
            if circulacao and self.volume > 5
            else 0.0
        )

        return {
            "ph": round(self.ph, 3),
            "ec": round(self.ec, 3),
            "temperatura": round(
                self.temperatura, 2
            ),
            "volume": round(self.volume, 2),
            "nivel_percentual": round(
                self.volume / self.capacidade * 100, 2
            ),
            "vazao": round(vazao, 2)
        }

    def aplicar_dose(self, bomba):
        """
        Aplica UM pulso abstrato de dosagem.

        Nao representa ml, concentracao quimica
        nem recomendacao para uso fisico.
        """

        if bomba not in self.estoques:
            raise ValueError("Bomba desconhecida")

        if self.estoques[bomba] <= 0:
            return False

        if bomba == "D1":
            self.ph -= 0.06

        elif bomba == "D2":
            self.ph += 0.06

        elif bomba == "D3":
            self.ec += 0.025

        elif bomba == "D4":
            self.ec += 0.025

        self.ph = max(0.0, min(14.0, self.ph))
        self.ec = max(0.0, self.ec)

        self.estoques[bomba] -= 1

        return True
