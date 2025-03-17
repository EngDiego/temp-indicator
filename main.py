import tkinter as tk
import threading
import time
import wmi
import os
import subprocess
import pythoncom  # Importar pythoncom para inicializar o COM
import psutil

# Caminho do Open Hardware Monitor relativo ao diretório onde o script está rodando
script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório onde o script está
OHM_PATH = os.path.join(script_dir, 'OpenHardwareMonitor', 'OpenHardwareMonitor.exe')  # Constrói o caminho

class MonitorTemperatura:
    def __init__(self):
        # Inicializa o Open Hardware Monitor se não estiver rodando
        self.iniciar_ohm()

        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove bordas
        self.root.attributes("-topmost", True)  # Sempre no topo
        self.root.wm_attributes("-transparentcolor", "black")  # Fundo transparente
        self.root.configure(bg="black")

        # Criar rótulo de temperatura
        self.label_temp = tk.Label(
            self.root,
            text="CPU: --°C",
            font=("Impact", 24, "bold"),
            fg="yellow",
            bg="black"
        )
        self.label_temp.pack(padx=10, pady=5)

        # Botão de fechar menor
        self.close_button = tk.Button(
            self.root, text="X", command=self.fechar_programa,
            font=("Arial", 7),  # Reduzindo a fonte
            bg="red", fg="white",
            width=2, height=1,  # Definindo tamanho fixo
            padx=0, pady=0,  # Removendo padding interno
            bd=1  # Reduzindo a borda
        )
        self.close_button.place(x=0, y=0)

        # Permitir arrastar a interface
        self.root.bind("<Button-1>", self.iniciar_arrasto)
        self.root.bind("<B1-Motion>", self.mover_janela)

        # Iniciar a atualização da temperatura
        self.executando = True
        threading.Thread(target=self.atualizar_temperatura, daemon=True).start()

    def iniciar_ohm(self):
        """Inicia o Open Hardware Monitor se ele não estiver rodando"""
        if not any("OpenHardwareMonitor.exe" in p for p in os.popen('tasklist').read().splitlines()):
            print("Iniciando Open Hardware Monitor...")
            self.process_ohm = subprocess.Popen(OHM_PATH, shell=True)
            time.sleep(10)  # Give OHM a *very* generous time to initialize
    
    def fechar_ohm(self):
        """Força o fechamento do Open Hardware Monitor"""
        try:
            print("Fechando Open Hardware Monitor...")
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == "OpenHardwareMonitor.exe":
                    try:
                        proc.kill()
                        print(f"Processo OpenHardwareMonitor.exe (PID {proc.info['pid']}) finalizado.")
                    except psutil.AccessDenied:
                        print(f"Acesso negado ao finalizar o processo OpenHardwareMonitor.exe (PID {proc.info['pid']}). Execute o script como administrador.")
                    except Exception as e:
                        print(f"Erro ao finalizar o processo OpenHardwareMonitor.exe (PID {proc.info['pid']}): {e}")
                    return  # Exit after killing the process

            print("OpenHardwareMonitor.exe não encontrado.")

        except Exception as e:
            print(f"Erro ao tentar fechar o Open Hardware Monitor: {e}")
    
    def atualizar_temperatura(self):
        """Thread que atualiza a temperatura na interface"""
        pythoncom.CoInitialize()  # Inicializar o COM no thread
        while self.executando:
            # Create WMI connection *within* the thread
            try:
                w = wmi.WMI(namespace=r"root\OpenHardwareMonitor")
            except Exception as e:
                print(f"Thread failed to connect to WMI: {e}")
                time.sleep(5)  # Wait and retry
                continue  # Skip to the next iteration

            temperatura_cpu, temperatura_gpu = self.obter_temperaturas(w)  # Pass the WMI object

            # Criar a string de temperatura para o rótulo
            text = ""
            if temperatura_cpu is not None:
                text += f"CPU: {int(temperatura_cpu)}°C"
            if temperatura_gpu is not None:
                if text:  # Adiciona um espaço entre as temperaturas
                    text += "   "
                text += f"GPU: {int(temperatura_gpu)}°C"

            # Atualiza o rótulo de temperatura
            self.root.after(0, lambda: self.label_temp.config(text=text))

            time.sleep(2)
        pythoncom.CoUninitialize()  # Finalizar o COM no final do thread

    def obter_temperaturas(self, w):  # Pass the WMI object as an argument
        """Obtém as temperaturas dos sensores de CPU e GPU"""

        max_retries = 3
        retry_delay = 0.5

        for attempt in range(max_retries):
            try:
                 temperatura_cpu = None
                 temperatura_gpu = None

                 # Obter todos os sensores
                 sensores = w.Sensor()
                 # Iterar sobre os sensores e filtrar apenas os sensores de temperatura
                 for sensor in sensores:
                     if sensor.SensorType == "Temperature":
                             if "CPU" in sensor.Name:
                                 # Se for um sensor de temperatura da CPU
                                 temperatura_cpu = sensor.Value
                             elif "GPU" in sensor.Name:
                                 # Se for um sensor de temperatura da GPU
                                 temperatura_gpu = sensor.Value
                 return temperatura_cpu, temperatura_gpu  # Return both CPU and GPU temps

            except Exception as e:
                print(f"Erro ao acessar sensores: {e}")
                time.sleep(retry_delay)
                continue

        return None, None  # Failed getting the values

    def iniciar_arrasto(self, event):
        self.x = event.x
        self.y = event.y

    def mover_janela(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def fechar_programa(self):
        """Fecha o programa e o Open Hardware Monitor"""
        self.executando = False
        self.fechar_ohm()  # Fecha o Open Hardware Monitor
        self.root.quit()

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MonitorTemperatura()
    app.iniciar()
