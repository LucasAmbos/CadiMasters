# main.py
import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import subprocess
import getpass
import datetime
from modules.clear_cache import clear_cache
from modules.update_gp import update_gp_remotely
from modules.install_program import install_program_interface
from modules.programas import programas_interface
from modules.instalar_impressora import install_printer_interface

# Caminhos do PsExec e do script BAT local
PSEXEC_PATH = r"C:\Windows\System32\psexec.exe"

# Função para registrar logs
def log_atividade(funcao):
    usuario = getpass.getuser()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file_name = os.path.join(log_dir, f"{usuario}Log.txt")
    
    with open(log_file_name, "a") as log_file:
        log_file.write(f"{usuario} executou {funcao} em {data_hora}\n")

# Definindo o caminho do arquivo BAT na pasta bats
BAT_PATH_LOCAL = os.path.join(os.path.dirname(os.path.abspath(__file__)),'bats', 'perfil.bat')

# Função para executar o bat para renomear perfil
def execute_refazer_perfil(hostname, username):
    #log_atividade("Iniciando renomeação de perfil remoto")
    try:
        remote_bat_path = f"\\\\{hostname}\\C$\\Temp\\perfil.bat"
        
        # Copia o perfil.bat para o caminho remoto
        shutil.copy(BAT_PATH_LOCAL, remote_bat_path)
        
        # Comando para executar o perfil.bat na máquina remota
        command = f'start cmd /k "{PSEXEC_PATH} \\\\{hostname} -s {remote_bat_path} {username}"'
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        messagebox.showinfo("Sucesso", "Comando enviado para o CMD com sucesso.")
        #log_atividade(f"Renomeação de perfil executada em {hostname} para o usuário {username}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar o comando remoto: {e}")
        #log_atividade(f"Erro ao renomear perfil remoto em {hostname}: {e}")
# Função para abrir a janela de renomeação de perfil remoto
def open_rename_profile_window():
    #log_atividade("Abrindo janela de renomeação de perfil remoto")
    rename_window = tk.Toplevel(root)
    rename_window.title("Renomear Perfil Remoto")
    rename_window.geometry("400x200")
    rename_window.resizable(False, False)

    tk.Label(rename_window, text="Hostname da Máquina:").pack()
    host_entry = tk.Entry(rename_window)
    host_entry.pack(pady=5)

    tk.Label(rename_window, text="Nome do Usuário de Rede:").pack()
    user_name_entry = tk.Entry(rename_window)
    user_name_entry.pack(pady=5)

    def rename_remote_profile():
        hostname = host_entry.get()
        username = user_name_entry.get()
        
        if not hostname or not username:
            tk.messagebox.showwarning("Aviso", "Por favor, preencha o hostname e o nome de usuário.")
            #log_atividade("Aviso: hostname ou usuário ausente ao renomear perfil")
            return

        execute_refazer_perfil(hostname, username)

    tk.Button(rename_window, text="Renomear Perfil", command=rename_remote_profile).pack(pady=10)

# Função para transferir arquivos e pastas
def transfer_file_to_remote_machine(path, hostname):
    #log_atividade(f"Iniciando transferência de '{path}' para {hostname}")
    try:
        if os.path.isdir(path):
            remote_path = f"\\\\{hostname}\\D$\\{os.path.basename(path)}"
            shutil.copytree(path, remote_path)
        else:
            remote_path = f"\\\\{hostname}\\D$\\{os.path.basename(path)}"
            shutil.copy2(path, remote_path)
        messagebox.showinfo("Sucesso", f"Transferência de '{path}' para {hostname} concluída.")
        #log_atividade(f"Transferência de '{path}' para {hostname} concluída com sucesso")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao transferir '{path}': {e}")
        #log_atividade(f"Erro na transferência de '{path}' para {hostname}: {e}")

# Função para abrir a janela de transferência de arquivos e pastas
def open_transfer_files_window():
    #log_atividade("Abrindo janela de transferência de arquivos/pastas")
    transfer_window = tk.Toplevel(root)
    transfer_window.title("Transferir Arquivos/Pastas")
    transfer_window.geometry("400x350")
    transfer_window.resizable(False, False)

    def select_files():
        paths = filedialog.askopenfilenames(title="Selecione os arquivos")
        if paths:
            paths_list.extend(paths)
            update_path_display()

    def select_folder():
        path = filedialog.askdirectory(title="Selecione a pasta")
        if path:
            paths_list.append(path)
            update_path_display()

    def update_path_display():
        file_entry.delete(0, tk.END)
        file_entry.insert(0, "; ".join(paths_list))

    def transfer_files_and_folders():
        machine_name = machine_entry.get()
        
        if not paths_list or not machine_name:
            tk.messagebox.showwarning("Aviso", "Por favor, preencha os caminhos e o nome da máquina.")
            #log_atividade("Aviso: Caminho ou hostname ausente ao transferir arquivos/pastas")
            return
        
        for path in paths_list:
            transfer_file_to_remote_machine(path, machine_name)

    paths_list = []

    tk.Label(transfer_window, text="Caminhos dos Arquivos/Pastas:").pack()
    file_entry = tk.Entry(transfer_window, width=50)
    file_entry.pack(pady=5)
    
    tk.Button(transfer_window, text="Selecionar Arquivos", command=select_files).pack(pady=5)
    tk.Button(transfer_window, text="Selecionar Pasta", command=select_folder).pack(pady=5)

    tk.Label(transfer_window, text="Nome da Máquina de Destino:").pack()
    machine_entry = tk.Entry(transfer_window)
    machine_entry.pack(pady=5)

    tk.Button(transfer_window, text="Transferir Arquivos/Pastas", command=transfer_files_and_folders).pack(pady=10)

# Função para abrir a janela de limpeza de CACHE remota
def open_clear_cache_window():
    #log_atividade("Abrindo janela de limpeza de cache remoto")
    clear_window = tk.Toplevel(root)
    clear_window.title("Limpar Cache Remotamente")
    clear_window.geometry("350x300")
    clear_window.resizable(False, False)

    tk.Label(clear_window, text="Hostname da Máquina:").pack(pady=5)
    host_entry = tk.Entry(clear_window)
    host_entry.pack(pady=5)

    tk.Label(clear_window, text="Selecione o Navegador:").pack(pady=10)

    # Combobox para seleção do navegador
    browser_combobox = ttk.Combobox(clear_window, values=["Chrome", "Edge", "Todos"])
    browser_combobox.pack(pady=5)
    browser_combobox.current(0)  # Chrome como padrão

    def clear_cache_remote():
        hostname = host_entry.get()
        browser = browser_combobox.get()

        if not hostname:
            tk.messagebox.showwarning("Aviso", "Por favor, preencha o hostname.")
            #log_atividade("Aviso: hostname ausente ao limpar cache remoto")
            return

        # Passando o hostname e o navegador para a função clear_cache
        clear_cache(hostname, browser)
        tk.messagebox.showinfo("Sucesso", f"Cache do {browser} limpo remotamente.")
        #log_atividade(f"Cache do {browser} limpo remotamente com sucesso")

    tk.Button(clear_window, text="Limpar Cache Remoto", command=clear_cache_remote).pack(pady=10)

# Função para abrir a janela de atualização de políticas de grupo
def open_update_gp_window():
    #log_atividade("Abrindo janela de atualização de políticas de grupo")
    update_gp_remotely()

# Função para abrir a interface de instalação de programas
def open_install_program_window():
    #log_atividade("Abrindo janela de instalação de programa remoto")
    install_program_interface()

# Configuração da Tela Principal
root = tk.Tk()
root.title("CADI Masters")
root.geometry("300x400")
root.resizable(False, False)

title_frame = tk.Frame(root)
title_frame.pack(pady=10)
cadi_label = tk.Label(title_frame, text="CADI", font=("Arial", 16))
cadi_label.pack(side="left")
masters_label = tk.Label(title_frame, text=" Masters", font=("Arial", 16), fg="red")
masters_label.pack(side="left")

# Botões para abrir cada funcionalidade em uma nova janela
tk.Button(root, text="Renomear Perfil Remoto", command=open_rename_profile_window).pack(pady=10)
tk.Button(root, text="Transferir Arquivos/Pastas", command=open_transfer_files_window).pack(pady=10)
# tk.Button(root, text="Limpar Cache Remotamente", command=open_clear_cache_window).pack(pady=10)
tk.Button(root, text="Atualizar Políticas de Grupo", command=open_update_gp_window).pack(pady=10)
tk.Button(root, text="Instalar Programa Remotamente", command=open_install_program_window).pack(pady=10)
tk.Button(root, text="Programas", command=programas_interface).pack(pady=10)
tk.Button(root, text="Instalar Impressora", command=install_printer_interface).pack(pady=10)

# Função para exibir a janela "Desenvolvido por"
def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("Sobre")
    about_window.geometry("300x150")
    about_window.resizable(False, False)
    
    tk.Label(about_window, text="Desenvolvido por:", font=("Arial", 12)).pack(pady=10)
    tk.Label(about_window, text="Hoffmann & Ambos", font=("Arial", 14, "bold")).pack(pady=10)

# Adicionando o botão ao final da tela principal
tk.Button(root, text="Sobre", command=open_about_window).pack(pady=10)


root.mainloop()
