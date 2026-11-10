
# 🌦️ Estação Meteorológica com ESP32

Sistema de monitoramento meteorológico desenvolvido com ESP32, MicroPython, FastAPI e SQLite. O projeto realiza a coleta de dados ambientais por meio de sensores físicos, transmite as medições via Wi-Fi para uma API e disponibiliza os dados para visualização em um dashboard web.

## 📌 Sobre o projeto

O objetivo é desenvolver uma estação meteorológica capaz de monitorar diferentes condições ambientais, coletando informações como:

- Temperatura ambiente.
- Umidade relativa do ar.
- Pressão atmosférica.
- Luminosidade.
- Qualidade do ar.
- Volume de chuva acumulado.

A comunicação entre o hardware e o backend acontece pela rede Wi-Fi, utilizando requisições HTTP.

## 🏗️ Arquitetura do sistema

O projeto é dividido em quatro partes principais:

1. **Hardware:** ESP32 e sensores responsáveis pela coleta das informações ambientais.
2. **Firmware:** código MicroPython executado no ESP32, responsável por ler os sensores e transmitir os dados.
3. **Backend:** API desenvolvida com FastAPI, responsável por receber e armazenar as medições.
4. **Banco de dados e Front-end:** SQLite para persistência dos dados e dashboard para visualização das informações.

### Fluxo de funcionamento

```text
Sensores
   |
   v
ESP32 (MicroPython)
   |
   | Wi-Fi / HTTP POST
   v
FastAPI
   |
   v
SQLite
   |
   v
Dashboard Web
```

## 🔧 Componentes utilizados

| Componente | Função |
|---|---|
| ESP32 DevKit | Unidade de processamento e comunicação Wi-Fi |
| DHT22 | Medição de temperatura e umidade |
| BMP280 | Medição de pressão atmosférica |
| LDR | Medição de luminosidade |
| MQ-135 | Monitoramento da qualidade do ar |
| Reed Switch | Detecção dos acionamentos do pluviômetro |
| Pluviômetro de báscula | Medição do volume de chuva |
| Resistores de 10 kΩ | Divisores de tensão e circuitos auxiliares |

## 🔌 Ligações dos componentes

| Sensor / Componente | Pino ESP32 |
|---|---|
| DHT22 — DATA | GPIO 4 |
| BMP280 — SDA | GPIO 21 |
| BMP280 — SCL | GPIO 22 |
| LDR — saída analógica | GPIO 35 |
| MQ-135 — saída AO | GPIO 34 |
| Reed Switch | GPIO 27 |

### Observações sobre as ligações

- O BMP280 utiliza comunicação I²C e endereço esperado `0x76`.
- O MQ-135 é alimentado pela saída VIN de 5 V, com divisor de tensão na saída analógica para proteger a entrada do ESP32.
- O LDR utiliza uma entrada analógica.
- O Reed Switch é conectado com resistor interno de pull-up.
- Todos os componentes devem compartilhar o GND.

## 💻 Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| MicroPython | Programação do ESP32 |
| Python | Desenvolvimento do backend |
| FastAPI | Construção da API REST |
| SQLAlchemy | ORM e comunicação com o banco |
| SQLite | Armazenamento das medições |
| HTTP | Comunicação entre ESP32 e backend |

## 🌐 Configuração de rede e conexão Wi-Fi

A comunicação entre o ESP32, o backend e o front-end acontece pela rede local.

O computador que executa o FastAPI e o ESP32 precisam estar conectados à mesma rede Wi-Fi para que a transmissão funcione.

### 1. Configurar a rede no ESP32

No arquivo `esp32/main.py`, existe uma seção de configuração com as informações da rede e do servidor:

```python
WIFI_SSID = "NOME_DA_REDE"
WIFI_PASSWORD = "SENHA_DA_REDE"

API_HOST = "192.168.0.224"
API_PORT = 8000
API_PATH = "/readings/"
```

Configure os seguintes parâmetros:

- `WIFI_SSID`: nome da rede Wi-Fi.
- `WIFI_PASSWORD`: senha da rede Wi-Fi.
- `API_HOST`: endereço IPv4 do computador que está executando o backend.
- `API_PORT`: porta utilizada pelo FastAPI.
- `API_PATH`: endpoint responsável por receber as medições.

### 2. Como trocar a rede de internet

Quando a estação for utilizada em outra rede, será necessário atualizar as configurações do ESP32.

Por exemplo, ao sair da rede doméstica e utilizar o hotspot de um celular:

1. Conecte o computador ao hotspot do celular.
2. Conecte o ESP32 à mesma rede, utilizando o nome e a senha do hotspot.
3. Descubra o novo endereço IPv4 do computador.
4. Atualize `WIFI_SSID` e `WIFI_PASSWORD` no arquivo `main.py`.
5. Atualize `API_HOST` com o novo endereço IP do computador.
6. Reinicie o ESP32.

**Importante:** o endereço IP pode mudar dependendo da rede utilizada. Portanto, sempre verifique o IPv4 do computador antes de iniciar a comunicação.

Não é necessário alterar a lógica de funcionamento dos sensores ou da API. Apenas as configurações de conexão precisam ser atualizadas.

### 3. Como descobrir o endereço IP do computador

No Windows:

1. Abra o Prompt de Comando (CMD).
2. Execute:

```bash
ipconfig
```

3. Localize o adaptador de rede conectado à internet.
4. Procure o campo `Endereço IPv4`.

Exemplo:

```text
Endereço IPv4: 192.168.0.224
```

Utilize esse endereço na variável `API_HOST`.

**Não utilize `localhost` ou `127.0.0.1` no ESP32 ou no front-end quando estiverem acessando o backend por meio da rede.** Esses endereços representam o próprio dispositivo que está realizando a conexão, e não o computador onde o FastAPI está executando.

### 4. Executar o backend

Inicie o FastAPI permitindo conexões externas à máquina:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

O parâmetro `--host 0.0.0.0` permite que outros dispositivos da mesma rede acessem a API.

O endereço de acesso será:

```text
http://IP_DO_COMPUTADOR:8000
```

Exemplo:

```text
http://192.168.0.224:8000/docs
```

**Importante:** `0.0.0.0` é utilizado somente para iniciar o servidor. Para acessar a API, utilize o IPv4 real do computador.

### 5. Configuração do front-end

O front-end também deve utilizar o endereço IP do computador que executa o backend, e não `localhost`, caso seja acessado por outro dispositivo.

Exemplo de endereço da API:

```text
http://192.168.0.224:8000
```

Quando a rede mudar e o IP do computador for alterado, atualize também o endereço configurado no front-end.

### 6. Requisitos para a comunicação

Para que o sistema funcione corretamente:

- Computador e ESP32 devem estar na mesma rede.
- O FastAPI deve estar em execução.
- O backend deve aceitar conexões externas com `--host 0.0.0.0`.
- O ESP32 deve utilizar o IP atual do computador.
- O front-end deve apontar para o mesmo IP e porta do backend.
- O firewall do Windows deve permitir conexões na porta 8000.

### Exemplo de funcionamento

```text
Hotspot do celular
       |
       |------------------|
       |                  |
       v                  v
    Computador          ESP32
    IP: 192.168.43.10   IP: 192.168.43.20
       |
       v
    FastAPI
    Porta 8000
       |
       v
    SQLite
       |
       v
    Front-end
```

A cada mudança de rede, basta atualizar as configurações de conexão e os endereços IP. O restante do código e a lógica de funcionamento da estação permanecem iguais.

## 📡 Comunicação com a API

O ESP32 envia periodicamente os dados coletados para o backend por meio de uma requisição HTTP POST.

### Endpoint de envio

```http
POST /readings/
```

### Exemplo de estrutura JSON

```json
{
  "temperature": 25.5,
  "humidity": 65.0,
  "pressure": 1013.2,
  "luminosity": 450,
  "air_quality": 125,
  "rainfall": 2.0
}
```

Os valores acima são apenas ilustrativos.

### Endpoint para consultar a última medição

```http
GET /readings/latest
```

A API retorna os dados mais recentes armazenados no banco de dados.

## ⚙️ Configuração e execução

### 1. Backend

Instale as dependências necessárias no ambiente virtual Python do backend:

```bash
pip install fastapi uvicorn sqlalchemy
```

Execute a API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

A documentação interativa estará disponível em:

```text
http://IP_DO_COMPUTADOR:8000/docs
```

### 2. ESP32

O firmware deve ser executado no ESP32 utilizando MicroPython.

Antes de iniciar:

1. Configure o nome da rede Wi-Fi.
2. Configure a senha da rede.
3. Configure o IP do computador que executa o backend.
4. Verifique se o FastAPI está em execução.
5. Execute o arquivo `main.py` no ESP32.

O firmware realiza as leituras dos sensores e envia os dados automaticamente para a API.

### 3. Front-end

Com o backend em execução, o dashboard pode consultar os endpoints da API para apresentar as medições.

O endereço utilizado pelo front-end deve apontar para o IP do computador que executa o backend.

## 📊 Dados monitorados

| Campo | Descrição | Unidade |
|---|---|---|
| temperature | Temperatura ambiente | °C |
| humidity | Umidade relativa do ar | % |
| pressure | Pressão atmosférica | hPa |
| luminosity | Leitura analógica do LDR | ADC |
| air_quality | Leitura analógica do MQ-135 | ADC |
| rainfall | Chuva acumulada | mm |
| recorded_at | Data e hora do registro | Data/Hora |

### Observações sobre as medições

- O MQ-135 envia a leitura analógica bruta do sensor. Ela não representa diretamente uma concentração em ppm.
- A luminosidade é representada pela leitura ADC do circuito com LDR.
- O pluviômetro utiliza um Reed Switch para identificar cada basculamento. A conversão para milímetros depende da calibração física do equipamento.
- A leitura de pressão depende do funcionamento correto do BMP280.

## 🔄 Intervalo de coleta

O intervalo de envio atualmente configurado no firmware é de **10 segundos**.

O backend armazena cada medição recebida, permitindo consultar o histórico e a leitura mais recente.

## 🚀 Funcionalidades

- Coleta de dados ambientais utilizando sensores físicos.
- Comunicação sem fio via Wi-Fi.
- Transmissão de medições por HTTP.
- API REST desenvolvida com FastAPI.
- Persistência dos dados em SQLite.
- Consulta da última medição registrada.
- Visualização das informações em dashboard web.
- Monitoramento de temperatura, umidade, luminosidade, qualidade do ar e chuva.

## 📁 Organização do projeto

A organização abaixo é uma referência e deve ser ajustada à estrutura real do repositório:

```text
estacao-meteorologica/
│
├── esp32/
│   └── main.py
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── frontend/
│   └── ...
│
└── README.md
```

## 🎓 Objetivo acadêmico

O projeto foi desenvolvido com o propósito de aplicar conhecimentos de eletrônica, programação de sistemas embarcados, comunicação entre dispositivos, desenvolvimento de APIs e armazenamento de dados.

A integração entre hardware e software permite construir uma solução de monitoramento ambiental, conectando sensores físicos a uma aplicação web.

---

**Projeto de Estação Meteorológica — ESP32 + MicroPython + FastAPI + SQLite.**
