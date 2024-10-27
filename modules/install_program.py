import shutil
import subprocess
from tkinter import messagebox, filedialog, Toplevel, Label, Entry, Button, Checkbutton, IntVar, StringVar, OptionMenu
import os
from modules.capturar_id import capture_session_id, get_captured_session_id  # Importa as funções do módulo capturar_id
import getpass 
import datetime

def install_program_interface():
    # Cria a janela da interface de instalação remota
    install_window = Toplevel()
    install_window.title("Instalar Programa Remotamente")
    install_window.geometry("350x400")

    # Campo para o hostname
    Label(install_window, text="Hostname da Máquina:").pack(pady=5)
    host_entry = Entry(install_window)
    host_entry.pack(pady=5)

    # Variável para o tipo de instalação
    silent_install = IntVar(value=1)  # Marcado por padrão

    # Função para selecionar o arquivo do instalador
    def select_installer():
        installer_path = filedialog.askopenfilename(title="Selecione o Instalador")
        installer_entry.delete(0, 'end')
        installer_entry.insert(0, installer_path)
        detect_install_type(installer_path)  # Detecta o tipo de instalador

    # Função para detectar o tipo de instalador
    def detect_install_type(installer_path):
        _, ext = os.path.splitext(installer_path)
        if ext.lower() == ".msi":
            install_type.set("msiexec")
        elif ext.lower() in [".exe"]:  # Você pode adicionar mais extensões conforme necessário
            if "setup" in os.path.basename(installer_path).lower():
                install_type.set("Inno Setup")  # Exemplo
            else:
                install_type.set("InstallShield")  # Exemplo genérico
        else:
            install_type.set("msiexec")  # Valor padrão se não for reconhecido

    # Botão para selecionar o instalador
    Button(install_window, text="Selecionar Instalador", command=select_installer).pack(pady=5)

    # Campo para mostrar o caminho do instalador selecionado
    installer_entry = Entry(install_window, width=40)
    installer_entry.pack(pady=5)

    # Menu para selecionar o tipo de instalador
    install_type = StringVar(value="msiexec")
    Label(install_window, text="Tipo de Instalador:").pack(pady=5)
    install_options = ["msiexec", "InstallShield", "Inno Setup"]
    OptionMenu(install_window, install_type, *install_options).pack(pady=5)

    # Checkbox para instalação silenciosa
    Checkbutton(install_window, text="Instalação silenciosa", variable=silent_install).pack(pady=5)

    # Função para criar o arquivo .bat e executar
    def install_program():
        hostname = host_entry.get()
        installer_path = installer_entry.get()
        method = install_type.get()

        if not hostname or not installer_path:
            messagebox.showwarning("Aviso", "Por favor, preencha o hostname e selecione o instalador.")
            return

        # Captura o ID da sessão
        session_id = capture_session_id(hostname)
        if not session_id:
            messagebox.showwarning("Aviso", "Não foi possível capturar o ID da sessão.")
            return

        # Caminho do .bat a ser criado
        bat_path = "D:\\install_program.bat"
        remote_installer_path = f"\\\\{hostname}\\C$\\Temp\\{os.path.basename(installer_path)}"
        remote_bat_path = f"\\\\{hostname}\\C$\\Temp\\install_program.bat"

        # Transfere o instalador para a máquina remota
        try:
            shutil.copy(installer_path, remote_installer_path)
            messagebox.showinfo("Sucesso", f"Instalador transferido para {remote_installer_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao transferir o instalador: {e}")
            return

        # Gera o conteúdo do .bat com base na seleção
        with open(bat_path, "w") as bat_file:
            if method == "msiexec":
                bat_file.write(f'msiexec /i "{remote_installer_path}" ')
                if silent_install.get() == 1:
                    bat_file.write("/qn\n")
            elif method == "InstallShield":
                bat_file.write(f'"{remote_installer_path}" ')
                if silent_install.get() == 1:
                    bat_file.write("/S /silent\n")
            elif method == "Inno Setup":
                bat_file.write(f'"{remote_installer_path}" ')
                if silent_install.get() == 1:
                    bat_file.write("/VERYSILENT /SUPPRESSMSGBOXES\n")
            else:
                bat_file.write(f'"{remote_installer_path}"\n')

        # Transfere o .bat para a máquina remota
        try:
            shutil.copy(bat_path, remote_bat_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao transferir o arquivo .bat: {e}")
            return

        # Executa o .bat na máquina remota
        try:
            if silent_install.get() == 1:
                psexec_command = f'psexec \\\\{hostname} -s -i cmd /c {remote_bat_path}'
            else:
                psexec_command = f'psexec \\\\{hostname} -s -i {session_id} cmd /c {remote_bat_path}'

            subprocess.run(psexec_command, shell=True, check=True)
            messagebox.showinfo("Sucesso", "Instalação finalizada remotamente.")
            
            # Registra a instalação
            log_instalacao(os.path.basename(installer_path), hostname)  # Passa apenas o nome do arquivo
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Erro ao iniciar a instalação: {e}")

    # Função para registrar logs
    def log_instalacao(caminho_programa, hostname_informado):
        usuario = getpass.getuser()
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Obtém o caminho do diretório de logs
        log_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs'))
        os.makedirs(log_dir, exist_ok=True)

        log_file_name = os.path.join(log_dir, f"{usuario}Log.txt")

        with open(log_file_name, "a") as log_file:
            log_file.write(f"{usuario} instalou o programa {caminho_programa} na máquina {hostname_informado} em {data_hora}\n")

    # Botão para iniciar a instalação
    Button(install_window, text="Instalar Programa", command=install_program).pack(pady=10)
