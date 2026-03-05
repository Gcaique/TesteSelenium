### Preparação de ambiente

Criar ambiente - O comando `python -m venv .venv` cria o ambiente virtual isolado para não conflitar com outras versões do Python.

Ativar ambiente - O comando `.\.venv\Scripts\activate` ativa o ambiente virtual. O ambiente estará ativado quando apresentar **(.venv)** no início do terminal.

Instalar dependências - O comando `pip install -r requirements.txt` instala todas as dependências do arquivo **requirements.txt**.

Desativar ambiente - O comando `deactivate` desativa o ambiente virtual. O ambiente estará desativado quando remover o **(.venv)** no início do terminal.

---
### Execução dos testes

Teste sequencial - O comando `pytest -q` executa todos os testes em ordem sequencial.

Teste específico - O comando `pytest -q -k nomedoteste.py` executa um teste em específico. **Exemplo do comando:** `-k userDeslogado.py`

Teste marcado - O comando `pytest -q -m nomedomarker` executa todos os testes que contém a marca. **Exemplo do comando:** `-m deslogado`

---

### Execução customizada dos testes


Customização de ambiente - O comando `--ambiente` define a execução dos testes em mobile ou desktop. **Exemplo do comando:** `--ambiente mobile`

Customização de navegador - O comando `--navegador` define o navegador utilizado na execução dos testes. **Exemplo do comando:** `--navegador firefox`

Customização de sistema operacional - O comando `--so` define o sistema operacional utilizado na execução dos testes. **Exemplo do comando:** `--so android`

Customização de device - O comando `--device` define o modelo do device que será utilizado na execução dos testes. **Exemplo do comando:** `--device iPhone 14`

Customização de serviço - O comando `--grid` define o destino (Maquina local ou virtual) que será utilizado na execução dos testes. **Exemplo do comando:** `--grid lt`

> **Exemplo de comandos combinados**
> 
>`pytest -q -m mobile --ambiente mobile --grid lt --so ios --navegador safari --device iPhone 14`
> 
> **OBS:** Alguns padrões foram definidos caso não passe a flag `--`. Verificar no arquivo **conftest.py** como está configurado.





