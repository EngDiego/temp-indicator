# temp-indicator
Indicador de Temperatura


### Passos para testar cloudfunction local

0. sudo apt install python3.12-venv
    - sudo apt update
    - sudo apt install python3-tk -y
1. acessar pasta_function com cd /temp-indicator
2. python3.12 -m venv .venv
3. source .venv/bin/activate
4. pip install -r requirements.txt
5. python3 main.py
6. watch -n 1 'python3 main.py'
7. pip freeze > requirements.txt
8. deactivate


### Passos para zipar cloudfunction

1. cd temp-indicator/
2. rm -f temp-indicator.zip && zip -r temp-indicator.zip . -x "." -x "/_pycache/" -x "/pycache" -x "pycache/*" -x "pycache_"
3. Dentro da cloudfunction, apertar em editar e depois upload de arquivo zip
