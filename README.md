# Conversor de Arquivos SAMSON para AERMOD

Este projeto permite obter dados meteorológicos da API Open-Meteo, processá-los e convertê-los para o formato compatível com o software de modelagem de dispersão atmosférica **AERMOD**.

## Funcionalidades

- Interface gráfica para entrada de dados.
- Coleta de dados meteorológicos passados e futuros.
- Processamento e armazenamento dos dados em um arquivo Excel (.xlsx).
- Conversão automática do arquivo para o formato SAM compatível com o AERMOD.
- Suporte a execução via arquivo executável (.exe).

## Tecnologias Utilizadas

- **Python**
- **Tkinter** (Interface gráfica)
- **Pandas** (Manipulação de dados)
- **Open-Meteo API** (Obtenção de dados meteorológicos)
- **requests-cache** (Cache de requisições para otimização)
- **retry-requests** (Requisições com tentativas automáticas)
- **openpyxl** (Manipulação de arquivos Excel)
- **PyInstaller** (Geração do executável)

---

## Como Executar o Projeto

### 1. Criar e Ativar um Ambiente Virtual

#### No Windows (cmd ou PowerShell):

```sh
python -m venv venv
venv\Scripts\activate
```

#### No Linux/macOS:

```sh
python3 -m venv venv
source venv/bin/activate
```

---

### 2. Instalar as Dependências

```sh
pip install requests-cache retry-requests pandas openpyxl openmeteo_requests pyinstaller
```

---

### 3. Executar o Script

```sh
python main.py
```

---

## Gerando o Executável (.exe)

Caso deseje criar um executável para rodar o projeto sem a necessidade de um ambiente Python instalado:

```sh
pyinstaller --onefile --windowed main.py
```

Isso gerará um executável dentro da pasta `dist/`.

---

## Estrutura do Projeto

```
📂 Projeto
├── 📂 arquivos/              # Pasta onde os arquivos convertidos serão salvos
├── 📜 main.py                # Script principal
├── 📜 requirements.txt       # Lista de dependências (caso precise criar)
├── 📜 README.md              # Documentação do projeto
└── 📂 venv/                  # Ambiente virtual (não precisa versionar)
```

---

## Notas

- Certifique-se de ter acesso à internet para realizar as requisições à API Open-Meteo.
- O script cria automaticamente a pasta `arquivos/` para salvar os arquivos convertidos.
- Utilize o ambiente virtual para evitar conflitos de dependências.

**Desenvolvido para facilitar a conversão de dados meteorológicos para o AERMOD!** 🚀

