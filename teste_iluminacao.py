
from simuladores.luminosidade import SimuladorLuminosidade
from modulos.iluminacao import ControleIluminacao


simulador = SimuladorLuminosidade()
controle = ControleIluminacao()

print("=" * 60)
print("SIMULACAO DO SOMBRITE AUTOMATICO")
print("=" * 60)

# Simular 24 horas, com intervalos de 5 minutos
for tempo in range(0, 1440, 5):

    sensores = simulador.atualizar(
        tempo,
        controle.abertura
    )

    resultado = controle.processar(sensores)

    hora = tempo // 60
    minuto = tempo % 60

    print(
        f"{hora:02d}:{minuto:02d} | "
        f"L1: {resultado['L1']:.0f} lux | "
        f"L2: {resultado['L2']:.0f} lux | "
        f"Sombrite: {resultado['abertura']:.0f}% aberto | "
        f"Motor: {resultado['motor']}"
    )
