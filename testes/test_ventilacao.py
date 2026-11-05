import unittest
from modulos.ventilacao import ControleVentilacao


def leituras(temperatura=26.0, umidade=70.0, diferenca=0.0):
    resultado = {}
    for nivel, desvio in (("superior", diferenca / 2),
                          ("intermediario", 0),
                          ("inferior", -diferenca / 2)):
        for local in "ABC":
            resultado[f"TH_{nivel}_{local}"] = {
                "temperatura": temperatura + desvio,
                "umidade": umidade,
            }
    return resultado


class TestVentilacao(unittest.TestCase):
    def test_temperatura_alta_aciona_todos_os_motores(self):
        controle = ControleVentilacao()
        estado = controle.processar(leituras(temperatura=30))["motores"]
        self.assertTrue(all(estado.values()))

    def test_umidade_alta_aciona_insuflacao_e_exaustao(self):
        controle = ControleVentilacao()
        estado = controle.processar(leituras(umidade=85))["motores"]
        self.assertTrue(all(estado[f"V{i}"] and estado[f"E{i}"] for i in (1, 2, 3)))
        self.assertFalse(any(estado[f"C{i}"] for i in (1, 2, 3)))

    def test_estratificacao_aciona_apenas_circulacao(self):
        controle = ControleVentilacao()
        estado = controle.processar(leituras(diferenca=2))["motores"]
        self.assertTrue(all(estado[f"C{i}"] for i in (1, 2, 3)))
        self.assertFalse(any(estado[f"V{i}"] or estado[f"E{i}"] for i in (1, 2, 3)))

    def test_histerese_da_temperatura(self):
        controle = ControleVentilacao()
        controle.processar(leituras(temperatura=30))
        estado = controle.processar(leituras(temperatura=28))["motores"]
        self.assertTrue(estado["V1"])
        estado = controle.processar(leituras(temperatura=26))["motores"]
        self.assertFalse(any(estado.values()))


if __name__ == "__main__":
    unittest.main()
