
class ControleIluminacao:
    def __init__(self):
        # 100% = totalmente aberto
        # 0% = totalmente fechado
        self.abertura = 100.0
        self.estado_motor = "PARADO"

        self.limite_superior = 35000
        self.limite_inferior = 12000

        # Movimento por ciclo de simulacao
        self.passo = 10.0

    def processar(self, sensores):
        luz_externa = sensores["L1"]
        luz_interna = sensores["L2"]

        # Luz excessiva: fechar sombrite
        if luz_interna > self.limite_superior:
            self.estado_motor = "FECHANDO"

            self.abertura = max(
                0.0,
                self.abertura - self.passo
            )

        # Luz insuficiente: abrir sombrite
        elif luz_interna < self.limite_inferior:
            self.estado_motor = "ABRINDO"

            self.abertura = min(
                100.0,
                self.abertura + self.passo
            )

        else:
            self.estado_motor = "PARADO"

        # Parar ao atingir os limites mecanicos
        if self.abertura == 0 and self.estado_motor == "FECHANDO":
            self.estado_motor = "PARADO"

        if self.abertura == 100 and self.estado_motor == "ABRINDO":
            self.estado_motor = "PARADO"

        return {
            "L1": luz_externa,
            "L2": luz_interna,
            "abertura": round(self.abertura, 1),
            "motor": self.estado_motor
        }
