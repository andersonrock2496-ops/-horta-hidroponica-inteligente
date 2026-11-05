
import time

from simuladores.sensores import ler_termohigrometros
from simuladores.ambiente import AmbienteSimulado
from modulos.ventilacao import ControleVentilacao
from configuracao import INTERVALO_LEITURA


ambiente = AmbienteSimulado()
controle = ControleVentilacao()

motores = controle.motores.consultar_estado()

print("=" * 55)
print("HORTA HIDROPONICA INTELIGENTE")
print("SIMULACAO DINAMICA DO AMBIENTE")
print("=" * 55)

try:
    while True:
        # Atualiza o ambiente usando o estado anterior
        # dos equipamentos
        estado_ambiente = ambiente.atualizar(motores)

        # Simula os nove sensores
        leituras = ler_termohigrometros(estado_ambiente)

        # Processa o controle automático
        resultado = controle.processar(leituras)

        motores = resultado["motores"]

        print("\n" + "=" * 55)
        print("TEMPO SIMULADO:",
              estado_ambiente["tempo"], "minutos")

        print("TEMPERATURA EXTERNA/AMBIENTE SIMULADO")
        print("Temperatura interna:",
              estado_ambiente["temperatura"], "°C")
        print("Umidade interna:",
              estado_ambiente["umidade"], "%")

        print("\n--- SENSORES ---")

        for sensor, dados in leituras.items():
            print(
                f"{sensor}: "
                f"{dados['temperatura']} °C | "
                f"{dados['umidade']} %"
            )

        print("\n--- CONTROLE AUTOMATICO ---")

        print(
            "Temperatura média:",
            resultado["temperatura_media"], "°C"
        )

        print(
            "Umidade média:",
            resultado["umidade_media"], "%"
        )

        print(
            "Diferença térmica vertical:",
            resultado["diferenca_vertical"], "°C"
        )

        print("\n--- EQUIPAMENTOS ---")

        for motor, estado in motores.items():
            situacao = "LIGADO" if estado else "DESLIGADO"
            print(motor, ":", situacao)

        time.sleep(INTERVALO_LEITURA)

except KeyboardInterrupt:
    print("\nSimulação encerrada.")
