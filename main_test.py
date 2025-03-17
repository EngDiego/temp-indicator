import subprocess

def run_powershell_command(command):
    """Executa um comando PowerShell a partir do WSL e retorna a saída"""
    result = subprocess.run(["powershell.exe", command], capture_output=True, text=True)
    return result.stdout

# Exemplo de comando para obter a temperatura da CPU
command = "Get-WmiObject -Class Win32_Processor | Select-Object -ExpandProperty LoadPercentage"
output = run_powershell_command(command)
print(f"Saída do PowerShell: {output}")


command = "Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace root/wmi | Select-Object -ExpandProperty CurrentTemperature"
output = run_powershell_command(command)
print(f"Temperatura do CPU: {output}")

temperatura_celsius = (int(output.strip()) / 10) - 273.15
print(f"Temperatura da CPU: {temperatura_celsius:.2f}°C")


