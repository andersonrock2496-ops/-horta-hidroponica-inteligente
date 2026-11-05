
# Firmware — Horta Hidropônica Inteligente

## Visão geral

Este diretório é destinado ao desenvolvimento dos
firmwares dos microcontroladores utilizados no projeto
Horta Hidropônica Inteligente.

O objetivo é integrar sensores e atuadores físicos ao
sistema supervisório desenvolvido em Python e Streamlit.

**Status atual: planejamento da integração IoT.**

Nesta versão, os sensores e equipamentos são simulados
por software. Ainda não há firmware operacional validado
em hardware.

## Arquitetura planejada

A arquitetura será dividida em dois níveis:

### ESP32 — Aquisição e controle local

Responsável futuramente por:

- Leitura de sensores de temperatura e umidade.
- Leitura dos sensores de luminosidade.
- Aquisição de pH e condutividade elétrica (EC).
- Monitoramento de nível e vazão.
- Acionamento de ventiladores e exaustores.
- Controle do motor do sombrite.
- Acionamento das bombas de circulação e reposição.
- Controle do chiller.
- Controle das bombas dosadoras D1, D2, D3 e D4.
- Execução de intertravamentos locais de segurança.

### Raspberry Pi — Supervisão

Responsável futuramente por:

- Execução do supervisório.
- Visualização de sensores e atuadores.
- Registro de dados operacionais.
- Histórico de alarmes e eventos.
- Comunicação com os controladores ESP32.
- Gerenciamento de parâmetros operacionais.

## Comunicação planejada

A comunicação entre o Raspberry Pi e os ESP32 poderá
utilizar MQTT ou outro protocolo adequado aos requisitos
de confiabilidade, latência e segurança.

O protocolo definitivo ainda não foi selecionado.

## Estrutura futura

```text
firmware/
├── README.md
├── esp32_climatizacao/
├── esp32_luminosidade/
└── esp32_solucao_nutritiva/
```

As pastas acima representam uma proposta de organização
e ainda não constituem módulos implementados.

## Segurança operacional

Antes de utilizar equipamentos físicos, serão
necessários:

- Validação e calibração dos sensores.
- Proteções elétricas dos circuitos de potência.
- Intertravamentos independentes do supervisório.
- Estados seguros em caso de perda de comunicação.
- Proteção contra funcionamento a seco.
- Limites de dosagem e prevenção de sobredosagem.
- Testes de falhas e procedimentos de recuperação.
- Validação experimental dos processos.

## Etapas futuras

1. Definir sensores, atuadores e interfaces elétricas.
2. Desenvolver firmware básico de aquisição.
3. Implementar comunicação com o supervisório.
4. Validar comandos e telemetria.
5. Implementar proteções locais.
6. Executar testes em bancada.
7. Integrar os subsistemas à instalação piloto.

## Observação

Este diretório documenta uma etapa futura do projeto.
O funcionamento atualmente demonstrado no repositório
é realizado em ambiente de simulação.
```
