# modules/update_gp.py
import subprocess
import os
import getpass
import datetime
from tkinter import messagebox, Toplevel, Label, Entry, Button

def log_atividade(hostname):
    usuario = getpass.getuser()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Cria a pasta 'logs' se não existir
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file_name = os.path.join(log_dir, f"{usuario}Log.txt")

    with open(log_file_name, "a") as log_file:
        log_file.write(f"{usuario} atualizou as políticas do computador {hostname} em {data_hora}\n")

def update_gp_remotely():
    # Cria a janela de entrada do hostname
    gp_window = Toplevel()
    gp_window.title("Atualizar Políticas de Grupo Remotamente")
    gp_window.geometry("350x200")
    gp_window.resizable(False, False)

    Label(gp_window, text="Hostname da Máquina:").pack(pady=10)
    host_entry = Entry(gp_window)
    host_entry.pack(pady=5)

    # Função para executar o gpupdate remotamente
    def run_gpupdate():
        hostname = host_entry.get()

        if not hostname:
            messagebox.showwarning("Aviso", "Por favor, preencha o hostname.")
            return

        # Caminho do PsExec
        psexec_path = r"C:\Windows\System32\psexec.exe"  # Atualize o caminho se necessário

        # Comando para atualizar as políticas de grupo remotamente
        command = f'{psexec_path} \\\\{hostname} -s cmd /c "gpupdate /force"'
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Sucesso", f"Políticas de grupo atualizadas remotamente em {hostname}.")
                log_atividade(hostname)  # Registra a atualização no log
            else:
                messagebox.showerror("Erro", f"Erro ao atualizar as políticas: {result.stderr}")
                log_atividade(f"Erro ao atualizar políticas em {hostname}: {result.stderr}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Erro ao executar o comando remotamente: {e}")
            log_atividade(f"Erro ao executar comando remotamente em {hostname}: {e}")

    Button(gp_window, text="Atualizar Políticas", command=run_gpupdate).pack(pady=20)
