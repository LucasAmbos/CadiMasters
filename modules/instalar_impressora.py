import os
import shutil
import subprocess
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, messagebox, Frame, Toplevel

# Importa a função para capturar o ID da sessão
from modules.capturar_id import capture_session_id

def install_printer_interface():
    window = Tk()
    window.title("Instalar Impressora Remotamente")
    window.geometry("300x300")

    Label(window, text="Hostname da Máquina:").place(x=10, y=10)
    host_entry = Entry(window)
    host_entry.place(x=10, y=40, width=280)

    model_type = StringVar(window)
    model_type.set("Kyocera")  # Padrão é Kyocera
    Label(window, text="Modelo da Impressora:").place(x=10, y=80)
    model_type_menu = OptionMenu(window, model_type, "Kyocera", "Epson", command=lambda _: toggle_printer_type())
    model_type_menu.place(x=10, y=110, width=280)

    type_frame = Frame(window)
    type_frame.place(x=10, y=140)

    printer_type = StringVar(window)
    printer_type.set("3655 Mono")  # Padrão é 3655
    Label(type_frame, text="Tipo de Impressora:").pack(side="left")
    printer_type_menu = OptionMenu(type_frame, printer_type, "3655 Mono", "308 Color")
    printer_type_menu.pack(side="left")

    Label(window, text="Nome da Impressora:").place(x=10, y=180)
    printer_name_entry = Entry(window)
    printer_name_entry.place(x=10, y=210, width=280)

    def open_credentials_window():
        # Nova janela para solicitar as credenciais de usuário
        cred_window = Toplevel(window)
        cred_window.title("Credenciais do Usuário")
        cred_window.geometry("300x150")

        Label(cred_window, text="Usuário:").place(x=10, y=10)
        user_entry = Entry(cred_window)
        user_entry.place(x=10, y=40, width=280)

        Label(cred_window, text="Senha:").place(x=10, y=70)
        password_entry = Entry(cred_window, show="*")
        password_entry.place(x=10, y=100, width=280)

        def submit_credentials():
            username = user_entry.get()
            password = password_entry.get()
            if not username or not password:
                messagebox.showwarning("Aviso", "Por favor, informe o usuário e a senha.")
            else:
                cred_window.destroy()  # Fecha a janela de credenciais
                install_printer(username, password)  # Chama a função com as credenciais

        Button(cred_window, text="Enviar", command=submit_credentials).place(x=10, y=130, width=280)

    def install_printer(username, password):
        hostname = host_entry.get()
        printer_name = printer_name_entry.get()

        if not hostname or not printer_name:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        session_id = capture_session_id(hostname)
        if session_id is None:
            messagebox.showwarning("Aviso", "Não foi possível capturar o ID da sessão.")
            return

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Install_printer'))
        bats_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bats'))

        kyocera_path = os.path.join(base_dir, 'kyocera.exe')
        epson_path = os.path.join(base_dir, 'install_epson.exe')
        epson_exe_path = os.path.join(base_dir, 'epson.exe')
        config_path = os.path.join(base_dir, 'config.txt')
        epconfig_path = os.path.join(base_dir, 'epconfig.txt')
        impressora_path = os.path.join(base_dir, 'impressora.exe')

        startky_path = os.path.join(bats_dir, 'startky.bat')
        startep_path = os.path.join(bats_dir, 'startep.vbs')

        remote_temp_dir = f"\\\\{hostname}\\C$\\Temp"

        if model_type.get() == "Kyocera":
            printer_type_value = printer_type.get().split()[0]
            with open(config_path, 'w') as config_file:
                config_file.write(f"{printer_type_value}\n{printer_name}")

            remote_paths = {
                "exe": os.path.join(remote_temp_dir, 'kyocera.exe'),
                "config": os.path.join(remote_temp_dir, 'config.txt'),
                "impressora": os.path.join(remote_temp_dir, 'impressora.exe'),
                "bat": os.path.join(remote_temp_dir, 'startky.bat')
            }

            try:
                shutil.copy(kyocera_path, remote_paths["exe"])
                shutil.copy(config_path, remote_paths["config"])
                shutil.copy(impressora_path, remote_paths["impressora"])
                shutil.copy(startky_path, remote_paths["bat"])
                messagebox.showinfo("Sucesso", "Arquivos transferidos com sucesso.")
            except Exception as e:
                print(f"Erro ao transferir arquivos Kyocera: {e}")
                messagebox.showerror("Erro", f"Erro ao transferir arquivos: {e}")
                return

            psexec_command = f'psexec \\\\{hostname} -u {username} -p {password} -i {session_id} "C:\\temp\\startky.bat"'

            try:
                subprocess.run(psexec_command, shell=True, check=True)
                messagebox.showinfo("Sucesso", "Instalação da impressora iniciada.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Erro", f"Erro ao executar o instalador: {e}")

        elif model_type.get() == "Epson":
            printer_type_value = printer_type.get().split()[0]
            with open(epconfig_path, 'w') as epconfig_file:
                epconfig_file.write(f"{printer_name}")

            remote_paths = {
                "install": os.path.join(remote_temp_dir, 'install_epson.exe'),
                "exe": os.path.join(remote_temp_dir, 'epson.exe'),
                "epconfig": os.path.join(remote_temp_dir, 'epconfig.txt'),
                "vbs": os.path.join(remote_temp_dir, 'startep.vbs')
            }

            try:
                shutil.copy(epson_path, remote_paths["install"])
                shutil.copy(epconfig_path, remote_paths["epconfig"])
                shutil.copy(epson_exe_path, remote_paths["exe"])
                shutil.copy(startep_path, remote_paths["vbs"])
                messagebox.showinfo("Sucesso", "Arquivos transferidos com sucesso.")
            except Exception as e:
                print(f"Erro ao transferir arquivos Epson: {e}")
                messagebox.showerror("Erro", f"Erro ao transferir arquivos: {e}")
                return

            psexec_command = f'psexec \\\\{hostname} -u {username} -p {password} -i {session_id} cmd /c "C:\\temp\\install_epson.exe"'

            try:
                subprocess.run(psexec_command, shell=True, check=True)
                messagebox.showinfo("Sucesso", "Instalação da impressora iniciada.")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar psexec: {e}")
                messagebox.showerror("Erro", f"Erro ao executar o instalador: {e}")

    install_button = Button(window, text="Instalar Impressora", command=open_credentials_window)
    install_button.place(x=10, y=240, width=280)

    def toggle_printer_type():
        if model_type.get() == "Epson":
            type_frame.place_forget()
        else:
            type_frame.place(x=10, y=140)

    window.mainloop()

# Para testar, você pode descomentar a linha abaixo.
# install_printer_interface()
