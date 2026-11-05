
class ControleNutrientes:
    def __init__(self):
        self.atuadores = {
            "B1": False,
            "B2": False,
            "CH1": False,
            "D1": False,
            "D2": False,
            "D3": False,
            "D4": False
        }

        self.alarmes = []
        self.estado_dosagem = "MONITORANDO"
        self.mistura_restante = 0

        self.fila_doses = []
        self.pulsos_realizados = {
            "D1": 0, "D2": 0,
            "D3": 0, "D4": 0
        }

        self.ciclos_sem_vazao = 0
        self.falha_vazao_travada = False

        self.limite_pulsos = 30
        self.total_pulsos = 0
        self.ultimo_evento = "Inicializado"

    def processar(self, sensores, minutos=5):
        self.alarmes = []

        ph = sensores["ph"]
        ec = sensores["ec"]
        temperatura = sensores["temperatura"]
        nivel = sensores["nivel_percentual"]
        vazao = sensores["vazao"]

        b1_anterior = self.atuadores["B1"]

        # Todos os dosadores desligados por padrao
        for bomba in ("D1", "D2", "D3", "D4"):
            self.atuadores[bomba] = False

        # Reposicao de agua
        if nivel < 80:
            self.atuadores["B2"] = True
        elif nivel >= 95:
            self.atuadores["B2"] = False

        # Circulacao
        if nivel <= 10 or self.falha_vazao_travada:
            self.atuadores["B1"] = False
        else:
            self.atuadores["B1"] = True

        # Falha persistente de vazao
        if b1_anterior and vazao < 0.5:
            self.ciclos_sem_vazao += 1
        else:
            self.ciclos_sem_vazao = 0

        if self.ciclos_sem_vazao >= 2:
            self.falha_vazao_travada = True
            self.atuadores["B1"] = False

        if self.falha_vazao_travada:
            self.alarmes.append(
                "Falha de vazao: rearme necessario"
            )

        # Chiller
        if nivel <= 10:
            self.atuadores["CH1"] = False
        elif temperatura >= 24:
            self.atuadores["CH1"] = True
        elif temperatura <= 21:
            self.atuadores["CH1"] = False

        # Monitoramento
        if not 5.5 <= ph <= 6.2:
            self.alarmes.append(
                f"pH fora da faixa: {ph:.3f}"
            )

        if not 1.2 <= ec <= 1.8:
            self.alarmes.append(
                f"EC fora da faixa: {ec:.3f}"
            )

        if nivel <= 10:
            self.alarmes.append(
                "Nivel critico do reservatorio"
            )

        if self.total_pulsos >= self.limite_pulsos:
            self.alarmes.append(
                "Limite de dosagem atingido"
            )

        # Intertravamentos para dosagem
        permissao = (
            nivel >= 20
            and vazao >= 0.5
            and b1_anterior
            and self.atuadores["B1"]
            and not self.atuadores["B2"]
            and not self.falha_vazao_travada
            and self.total_pulsos < self.limite_pulsos
        )

        if not permissao:
            self.estado_dosagem = "BLOQUEADO"
            self.fila_doses = []
            self.mistura_restante = 0

            return self.resultado()

        # Esperar mistura
        if self.mistura_restante > 0:
            self.mistura_restante = max(
                0, self.mistura_restante - minutos
            )
            self.estado_dosagem = "MISTURANDO"
            return self.resultado()

        # Executar proximo pulso pendente
        if self.fila_doses:
            bomba = self.fila_doses.pop(0)
            self.atuadores[bomba] = True
            self.estado_dosagem = "DOSANDO"
            self.mistura_restante = 15

            self.pulsos_realizados[bomba] += 1
            self.total_pulsos += 1
            self.ultimo_evento = f"Pulso {bomba}"

            return self.resultado()

        # Prioridade 1: corrigir pH
        if ph > 6.2:
            self.fila_doses = ["D1"]

        elif ph < 5.5:
            self.fila_doses = ["D2"]

        # Prioridade 2: corrigir EC baixa
        elif ec < 1.2:
            self.fila_doses = ["D3", "D4"]

        else:
            self.estado_dosagem = "MONITORANDO"
            return self.resultado()

        # Primeiro pulso do novo ciclo
        bomba = self.fila_doses.pop(0)
        self.atuadores[bomba] = True
        self.estado_dosagem = "DOSANDO"
        self.mistura_restante = 15

        self.pulsos_realizados[bomba] += 1
        self.total_pulsos += 1
        self.ultimo_evento = f"Pulso {bomba}"

        return self.resultado()

    def resultado(self):
        return {
            "atuadores": self.atuadores.copy(),
            "alarmes": self.alarmes.copy(),
            "estado_dosagem": self.estado_dosagem,
            "mistura_restante": self.mistura_restante,
            "pulsos": self.pulsos_realizados.copy(),
            "ultimo_evento": self.ultimo_evento
        }
