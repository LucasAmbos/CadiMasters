# modules/transfer_files.py
import shutil
import os
from tkinter import messagebox
import getpass
import datetime

def log_transferencia(nome_arquivo, machine_name):
    usuario = getpass.getuser()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Obtém o caminho do diretório de logs
    log_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs'))
    os.makedirs(log_dir, exist_ok=True)

    log_file_name = os.path.join(log_dir, f"{usuario}Log.txt")

    with open(log_file_name, "a") as log_file:
        log_file.write(f"{usuario} transferiu o {nome_arquivo} para a máquina {machine_name} em {data_hora}\n")

def transfer_file_to_remote_machine(file_path, machine_name):
    """
    Transfere um arquivo para o diretório D$ na máquina remota.

    Parâmetros:
    file_path (str): Caminho local do arquivo a ser transferido.
    machine_name (str): Nome do host ou IP da máquina remota.
    """
    if not os.path.exists(file_path):
        messagebox.showerror("Erro", "Arquivo de origem não encontrado.")
        return
    
    # Caminho de destino na máquina remota (Drive D)
    destination_path = f"\\\\{machine_name}\\D$\\{os.path.basename(file_path)}"
    
    try:
        shutil.copy(file_path, destination_path)
        messagebox.showinfo("Sucesso", f"Arquivo copiado para {destination_path}")

        # Registra a transferência no log
        log_transferencia(os.path.basename(file_path), machine_name)
        
    except PermissionError:
        messagebox.showerror("Erro", "Permissão negada. Verifique as credenciais de rede.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao copiar o arquivo: {e}")
