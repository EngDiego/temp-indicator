import os
import time
import psutil
import tkinter as tk
from tkinter import messagebox


def get_cpu_temperature():
    """
    Obtém a temperatura do CPU. No Raspberry Pi, usa 'vcgencmd'.
    No WSL e Linux, usa 'psutil.sensors_temperatures()'.
    """
    if "microsoft" in os.uname().release.lower():
        print("⚠️ Monitoramento de temperatura pode não funcionar no WSL.")
        return None

    temps = psutil.sensors_temperatures()
    if "coretemp" in temps:
        return temps["coretemp"][0].current
    return None


def show_alert(temp):
    """
    Exibe um alerta pop-up na tela se a temperatura for alta.
    """
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(
        "🔥 ALERTA DE TEMPERATURA!",
        f"A temperatura do CPU está em {temp:.1f}°C!\nVerifique a refrigeração."
    )
    root.destroy()


def main():
    """
    Loop de monitoramento da temperatura do CPU.
    Exibe um alerta se a temperatura ultrapassar o limite.
    """
    temperatura_limite = 70.0

    while True:
        temperatura = get_cpu_temperature()

        if temperatura and temperatura > temperatura_limite:
            show_alert(temperatura)
        elif temperatura is None:
            print("❌ Não foi possível obter a temperatura do CPU no WSL.")
            break  # Sai do loop se não for possível medir a temperatura

        time.sleep(10)


if __name__ == "__main__":
    main()
