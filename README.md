# 🌱 Horta Hidropônica Inteligente

### Supervisório de automação e simulação de cultivo hidropônico

Projeto desenvolvido em **Python e Streamlit**, com foco na simulação de processos agrícolas automatizados, monitoramento de variáveis ambientais e controle de atuadores.

O sistema integra três subsistemas operacionais em um único supervisório, permitindo acompanhar sensores, decisões de controle, estados dos equipamentos e históricos de funcionamento.

## Demonstração do supervisório

![Supervisório integrado](docs/imagens/01-visao-geral.png)

O sistema integra climatização, controle de
luminosidade e monitoramento da solução
nutritiva em uma interface Streamlit.

### Resultados do teste de dosagem de 24 horas

| Indicador | Resultado |
|---|---|
| pH inicial | 6,45 |
| pH final | 6,15 |
| EC inicial | 1,05 mS/cm |
| EC final | 1,448 mS/cm |
| Pulsos D1 (pH Down) | 17 |
| Pulsos D3 (Nutriente A) | 3 |
| Pulsos D4 (Nutriente B) | 3 |
| Total de pulsos | 23 |
| Alarmes ativos ao final | 0 |

Os resultados foram obtidos em ambiente
simulado, sem equipamentos físicos conectados.

[Ver demonstração completa](docs/demonstracao.md)

[Consultar log de execução](logs/simulacao_24h.log)


## Funcionalidades implementadas

### 1. Controle climático

- Simulação de nove termohigrômetros distribuídos em diferentes alturas.
- Monitoramento de temperatura e umidade relativa.
- Controle de insuflação, circulação e exaustão.
- Acionamento automático com histerese.
- Monitoramento da diferença térmica vertical.

### 2. Controle de luminosidade

- Simulação de luminosidade externa e interna.
- Controle automático de sombrite retrátil.
- Monitoramento do percentual de abertura.
- Registro histórico da luminosidade e da posição do sombrite.

### 3. Controle da solução nutritiva

- Monitoramento de pH, condutividade elétrica (EC), temperatura, nível e vazão.
- Controle de bomba de circulação e reposição de água.
- Controle térmico por chiller.
- Simulação de dosagem de corretivos de pH.
- Simulação de dosagem de nutrientes A/B.
- Máquina de estados para dosagem e homogeneização.
- Alarmes e intertravamentos de segurança simulados.

## Tecnologias

- Python
- Streamlit
- Pandas
- Plotly
- Git e GitHub

## Arquitetura

O projeto foi organizado em módulos independentes:

- `simuladores/`: modelos de ambiente, sensores e processos físicos simulados.
- `modulos/`: lógica de controle dos subsistemas.
- `interface.py`: supervisório gráfico em Streamlit.
- `testes/` e arquivos `teste_*.py`: rotinas de validação.
- `configuracao.py`: parâmetros de referência.

## Como executar

Clone o repositório e acesse a pasta do projeto.

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o supervisório:

```bash
python -m streamlit run interface.py
```

Para executar o teste de dosagem:

```bash
python teste_dosagem.py
```

## Estado do projeto

**Protótipo funcional em simulação.**

Os sensores, atuadores, processos químicos e processos térmicos são representados por modelos computacionais simplificados. O sistema ainda não foi validado para operação autônoma em uma instalação hidropônica real.

As doses simuladas não representam volumes reais de produtos químicos.

## Próximas etapas

- Integração com ESP32 para aquisição de dados e controle.
- Raspberry Pi como unidade supervisória.
- Comunicação entre dispositivos.
- Persistência de dados em banco de dados.
- Calibração de sensores e bombas dosadoras.
- Aprimoramento dos modelos físicos e químicos.
- Testes de falhas e intertravamentos.
- Implantação piloto em ambiente real.

## Objetivo

Desenvolver uma plataforma modular de agricultura de precisão, integrando conhecimentos de automação industrial, programação, instrumentação, IoT e agronomia.

**Área:** AgriTech | Automação | IoT | Sistemas Supervisórios