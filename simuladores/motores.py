
class SistemaVentilacao:

    def __init__(self):

        self.ventiladores_inferiores = {
            "V1": False,
            "V2": False,
            "V3": False
        }

        self.ventiladores_superiores = {
            "C1": False,
            "C2": False,
            "C3": False
        }

        self.exaustores = {
            "E1": False,
            "E2": False,
            "E3": False
        }

    def acionar_inferiores(self, estado):
        for motor in self.ventiladores_inferiores:
            self.ventiladores_inferiores[motor] = estado

    def acionar_superiores(self, estado):
        for motor in self.ventiladores_superiores:
            self.ventiladores_superiores[motor] = estado

    def acionar_exaustores(self, estado):
        for motor in self.exaustores:
            self.exaustores[motor] = estado

    def consultar_estado(self):

        return {
            **self.ventiladores_inferiores,
            **self.ventiladores_superiores,
            **self.exaustores
        }
