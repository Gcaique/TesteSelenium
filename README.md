## Como rodar (Passos para iniciar o projeto)

python -m venv .venv 

.\.venv\Scripts\activate 

pip install -r requirements.txt

pytest -q

--------------------------------------------------------------
## MOBILE

### Android padrão (Chrome):

pytest -m mobile --ambiente mobile

### Android Firefox:

pytest -m mobile --ambiente mobile --navegador firefox

### iOS Safari:

pytest -m mobile --ambiente mobile --so ios --navegador safari

### iOS com device específico:

pytest -m mobile --ambiente mobile --so ios --device "iPhone 15 Pro"


