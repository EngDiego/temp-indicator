# Temp Indicator

## Sobre
O **Temp Indicator** é um indicador de temperatura da CPU e GPU para Windows e Linux, utilizando o Open Hardware Monitor para leitura dos sensores.

---

## Instalação no Windows (usando Bash)

1. Instale o **Python 3.12** ou superior a partir do site oficial: [Python Downloads](https://www.python.org/downloads/)
2. Execute o script **`windows_install_and_run.bat`**
3. Autorize a leitura dos sensores do sistema quando solicitado
4. Aguarde a abertura do indicador de temperatura na parte superior esquerda da tela
5. Para fechar, clique no **X** no canto da interface

---

## Testando o programa localmente (Linux & Windows)

### **Pré-requisitos**
Para Linux:
```sh
sudo apt update && sudo apt install python3-venv python3-tk -y
```

Para Windows, abra o PowerShell como Administrador e execute:
```powershell
Set-ExecutionPolicy Unrestricted -Scope Process
```

### **Passos para executar**
1. Acesse a pasta do projeto:
   ```sh
   cd temp-indicator
   ```
2. Crie um ambiente virtual:
   ```sh
   python -m venv .venv
   ```
3. Ative o ambiente virtual:
   - **Linux/macOS:**
     ```sh
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate
     python.exe -m pip install --upgrade pip
     ```
4. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
5. Execute o programa:
   ```sh
   python main.py
   ```
6. Para atualizar o arquivo de dependências:
   ```sh
   pip freeze > requirements.txt
   ```
7. Para sair do ambiente virtual:
   ```sh
   deactivate
   ```

---

## Criando um arquivo ZIP do projeto
Para compactar o projeto sem incluir arquivos desnecessários:
```sh
cd temp-indicator/
rm -f temp-indicator.zip && zip -r temp-indicator.zip . -x "./.git*" -x "__pycache__/*"
```
Depois, basta fazer o **upload do arquivo ZIP** onde for necessário.


## Contribuição
Caso tenha sugestões ou melhorias, sinta-se à vontade para abrir um **Pull Request** ou relatar problemas na aba **Issues**.

---

### 📌 Observação
- Para garantir que o Open Hardware Monitor funcione corretamente, é necessário rodá-lo como Administrador.
- Algumas funcionalidades podem exigir permissões especiais para acessar sensores do hardware.

