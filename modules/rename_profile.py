import os
from tkinter import messagebox
import getpass
import datetime

def log_renomeacao(hostname, username):
    usuario = getpass.getuser()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Cria a pasta 'logs' se não existir
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file_name = os.path.join(log_dir, f"{usuario}Log.txt")

    with open(log_file_name, "a") as log_file:
        log_file.write(f"{usuario} refez o perfil do {username} no computador {hostname} em {data_hora}\n")

def execute_refazer_perfil(hostname, username):
    """
    Função para renomear o perfil de usuário na máquina remota.
    Ela renomeia a pasta do perfil diretamente na máquina remota via rede.
    """
    try:
        # Caminho da pasta do usuário na máquina remota
        remote_path = f"\\\\{hostname}\\C$\\Users\\{username}"
        new_remote_path = f"\\\\{hostname}\\C$\\Users\\old.{username}"

        # Verifica se o caminho remoto existe
        if not os.path.exists(remote_path):
            messagebox.showerror("Erro", f"O perfil {username} não foi encontrado no computador {hostname}.")
            return

        # Renomeia o perfil do usuário
        os.rename(remote_path, new_remote_path)

        # Log da renomeação
        log_renomeacao(hostname, username)

        # Mensagem de sucesso
        messagebox.showinfo("Sucesso", f"O perfil {username} foi renomeado para old.{username} no computador {hostname}.")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao renomear o perfil: {e}")
