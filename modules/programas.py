import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

# Caminho do arquivo onde os programas serão armazenados
programs_file = 'programas.json'

# Função para carregar a lista de programas do arquivo
def carregar_programas():
    if os.path.exists(programs_file):
        with open(programs_file, 'r') as file:
            return json.load(file)
    return []

# Função para salvar a lista de programas no arquivo
def salvar_programas():
    with open(programs_file, 'w') as file:
        json.dump(program_paths, file)

# Variável global para armazenar a lista de programas
program_paths = carregar_programas()

# Função para abrir um programa com base no caminho fornecido
def abrir_programa(program_path):
    try:
        subprocess.Popen(program_path, shell=True)
        messagebox.showinfo("Sucesso", f"Programa '{program_path}' aberto com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir o programa: {e}")

# Função para remover um programa da lista
def remover_programa(program_path):
    try:
        program_paths.remove(program_path)
        salvar_programas()  # Salva a lista após a remoção
        atualizar_lista_programas()
        messagebox.showinfo("Removido", f"Programa '{program_path}' removido da lista.")
    except ValueError:
        messagebox.showerror("Erro", f"Erro ao remover o programa: '{program_path}' não está na lista.")

# Função para atualizar a interface com os programas adicionados
def atualizar_lista_programas():
    # Limpa os widgets anteriores
    for widget in programas_list_frame.winfo_children():
        widget.destroy()

    # Adiciona cada programa à interface com botões de Abrir e Remover
    for program_path in program_paths:
        frame = tk.Frame(programas_list_frame)
        frame.pack(pady=5, fill="x")

        label = tk.Label(frame, text=program_path)
        label.pack(side="left", padx=5)

        abrir_button = tk.Button(frame, text="Abrir", command=lambda p=program_path: abrir_programa(p))
        abrir_button.pack(side="right", padx=5)

        remover_button = tk.Button(frame, text="Remover", command=lambda p=program_path: remover_programa(p))
        remover_button.pack(side="right", padx=5)

# Função para criar a interface "Programas"
def programas_interface():
    global programas_list_frame

    programas_window = tk.Toplevel()
    programas_window.title("Programas")
    programas_window.geometry("500x300")
    programas_window.resizable(False, False)

    # Função para selecionar um programa e adicionar à lista
    def adicionar_programa():
        program_path = filedialog.askopenfilename(title="Selecione o Programa")
        if program_path:
            program_paths.append(program_path)
            salvar_programas()  # Salva a lista de programas após adicionar
            atualizar_lista_programas()

    # Frame para listar os programas
    programas_list_frame = tk.Frame(programas_window)
    programas_list_frame.pack(pady=10, fill="both", expand=True)

    # Botão para adicionar programas
    tk.Button(programas_window, text="Adicionar Programa", command=adicionar_programa).pack(pady=10)

    # Atualiza a lista ao iniciar
    atualizar_lista_programas()
