import unittest

from simuladores.motores import SistemaVentilacao
from modulos.nutrientes import ControleNutrientes


class TestCirculacao(unittest.TestCase):
    def test_ventiladores_superiores_ligam_e_desligam(self):
        motores = SistemaVentilacao()
        motores.acionar_superiores(True)
        self.assertTrue(all(motores.consultar_estado()[f"C{i}"] for i in (1, 2, 3)))
        motores.acionar_superiores(False)
        self.assertFalse(any(motores.consultar_estado()[f"C{i}"] for i in (1, 2, 3)))

    def test_bomba_circulacao_bloqueada_por_nivel_critico(self):
        controle = ControleNutrientes()
        sensores = {"ph": 5.8, "ec": 1.5, "temperatura": 22,
                   "nivel_percentual": 9, "vazao": 0}
        resultado = controle.processar(sensores)
        self.assertFalse(resultado["atuadores"]["B1"])
        self.assertIn("Nivel critico do reservatorio", resultado["alarmes"])

    def test_bomba_circulacao_liga_com_nivel_seguro(self):
        controle = ControleNutrientes()
        sensores = {"ph": 5.8, "ec": 1.5, "temperatura": 22,
                   "nivel_percentual": 90, "vazao": 0}
        resultado = controle.processar(sensores)
        self.assertTrue(resultado["atuadores"]["B1"])


if __name__ == "__main__":
    unittest.main()
