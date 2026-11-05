
from simuladores.solucao_nutritiva import (
    SimuladorSolucaoNutritiva
)
from modulos.nutrientes import ControleNutrientes


reservatorio = SimuladorSolucaoNutritiva()
controle = ControleNutrientes()

print("=" * 60)
print("BLOCO A - CONTROLE DA SOLUCAO NUTRITIVA")
print("=" * 60)

# Simular 24 horas
for tempo in range(0, 1440, 5):

    # Estado dos atuadores no ciclo anterior
    atuadores_anteriores = controle.atuadores.copy()

    # Atualizar reservatorio
    sensores = reservatorio.atualizar(
        atuadores_anteriores,
        minutos=5
    )

    # Processar controle
    resultado = controle.processar(sensores)

    hora = tempo // 60
    minuto = tempo % 60

    print(
        f"{hora:02d}:{minuto:02d} | "
        f"pH: {sensores['ph']:.2f} | "
        f"EC: {sensores['ec']:.2f} | "
        f"T: {sensores['temperatura']:.2f} C | "
        f"Nivel: {sensores['nivel_percentual']:.1f}% | "
        f"Vazao: {sensores['vazao']:.1f} L/min | "
        f"B1: {resultado['atuadores']['B1']} | "
        f"B2: {resultado['atuadores']['B2']} | "
        f"CH1: {resultado['atuadores']['CH1']}"
    )

    for alarme in resultado["alarmes"]:
        print("  ALERTA:", alarme)
