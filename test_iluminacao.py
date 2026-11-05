import unittest
from modulos.iluminacao import ControleIluminacao


class TestIluminacao(unittest.TestCase):
    def test_fecha_com_luminosidade_alta(self):
        controle = ControleIluminacao()
        resultado = controle.processar({"L1": 45000, "L2": 36000})
        self.assertEqual(resultado["abertura"], 90.0)
        self.assertEqual(resultado["motor"], "FECHANDO")

    def test_abre_com_luminosidade_baixa(self):
        controle = ControleIluminacao()
        controle.abertura = 50.0
        resultado = controle.processar({"L1": 9000, "L2": 8000})
        self.assertEqual(resultado["abertura"], 60.0)
        self.assertEqual(resultado["motor"], "ABRINDO")

    def test_permanece_parado_na_faixa(self):
        controle = ControleIluminacao()
        resultado = controle.processar({"L1": 30000, "L2": 20000})
        self.assertEqual(resultado["abertura"], 100.0)
        self.assertEqual(resultado["motor"], "PARADO")

    def test_respeita_limites_mecanicos(self):
        controle = ControleIluminacao()
        controle.abertura = 5.0
        resultado = controle.processar({"L1": 50000, "L2": 40000})
        self.assertEqual(resultado["abertura"], 0.0)
        self.assertEqual(resultado["motor"], "PARADO")


if __name__ == "__main__":
    unittest.main()
