
from simuladores.solucao_nutritiva import (
    SimuladorSolucaoNutritiva
)
from modulos.nutrientes import ControleNutrientes

reservatorio = SimuladorSolucaoNutritiva()
controle = ControleNutrientes()

# Cenario de teste: pH alto e EC baixa
reservatorio.ph = 6.45
reservatorio.ec = 1.05

print("TESTE ACELERADO - DOSAGEM INTELIGENTE")
print("=" * 90)

for tempo in range(0, 1440, 5):
    sensores = reservatorio.atualizar(
        controle.atuadores.copy(),
        minutos=5
    )

    resultado = controle.processar(
        sensores,
        minutos=5
    )

    dose = "-"

    for bomba in ("D1", "D2", "D3", "D4"):
        if resultado["atuadores"][bomba]:
            if reservatorio.aplicar_dose(bomba):
                dose = bomba

    if tempo % 30 == 0 or dose != "-":
        hora, minuto = divmod(tempo, 60)

        print(
            f"{hora:02d}:{minuto:02d} | "
            f"pH={sensores['ph']:.3f} | "
            f"EC={sensores['ec']:.3f} | "
            f"Nivel={sensores['nivel_percentual']:.1f}% | "
            f"Estado={resultado['estado_dosagem']} | "
            f"Dose={dose} | "
            f"Mistura={resultado['mistura_restante']} min"
        )

print("\nRESUMO")
print("pH final:", round(reservatorio.ph, 3))
print("EC final:", round(reservatorio.ec, 3))
print("Pulsos:", controle.pulsos_realizados)
print("Estado:", controle.estado_dosagem)
print("Alarmes:", controle.alarmes)
