import subprocess 
from tkinter import messagebox
import os
import shutil

def clear_cache(hostname, browser):
    """
    Limpa os arquivos temporários na máquina remota.

    Parâmetros:
    hostname (str): Nome do host ou IP da máquina remota.
    browser (str): Navegador para limpar o cache.
    """
    # Defina o caminho do diretório onde os arquivos .bat estão localizados
    bats_directory = 'bats'  # ou o caminho completo, se necessário

    # Escolha o arquivo .bat com base no navegador selecionado
    if browser == "Chrome":
        batch_file = os.path.join(bats_directory, 'chrome.bat')
    elif browser == "Edge":
        batch_file = os.path.join(bats_directory, 'edge.bat')
    else:
        messagebox.showwarning("Aviso", "Navegador não suportado.")
        return

    # Enviar o arquivo .bat para a máquina remota
    try:
        shutil.copy(batch_file, f'\\\\{hostname}\\C$\\Users\\Public\\{os.path.basename(batch_file)}')
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao copiar o arquivo: {e}")
        return

    # Comando para executar o arquivo .bat no host remoto
    remote_batch_file = f'C:\\Users\\Public\\{os.path.basename(batch_file)}'
    psexec_command = f'psexec \\\\{hostname} {remote_batch_file}'

    try:
        subprocess.run(psexec_command, shell=True, check=True)
        messagebox.showinfo("Sucesso", f"Cache do {browser} limpo remotamente no computador {hostname}.")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao limpar o cache: {e}")
