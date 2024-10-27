import subprocess
from tkinter import messagebox

# Variável global para armazenar o ID da sessão
captured_session_id = None

def capture_session_id(hostname):
    global captured_session_id

    if not hostname:
        messagebox.showwarning("Aviso", "Por favor, preencha o hostname.")
        return None

    try:
        # Comando para capturar a sessão
        session_command = f'psexec \\\\{hostname} cmd /c "query user"'
        result = subprocess.run(session_command, shell=True, capture_output=True, text=True)
        output = result.stdout

        # Verifica se a saída contém o ID da sessão, independentemente do retorno do comando
        if " Ativo " in output or " Active " in output:
            for line in output.splitlines():
                if " Ativo " in line or " Active " in line:
                    captured_session_id = line.split()[2]
                    messagebox.showinfo("Sessão Capturada", f"ID da sessão ativa capturada: {captured_session_id}")
                    return captured_session_id  # Retorna o ID da sessão capturada
        else:
            messagebox.showerror("Erro", "ID da sessão ativa não encontrada.")
            return None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao capturar a sessão: {e}")
        return None

def get_captured_session_id():
    return captured_session_id
