import os
import tkinter as tk
from tkinter import ttk, messagebox

class GerenciadorTarefas:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("✨ Gerenciador de Tarefas")
        self.janela.geometry("500x600")
        self.janela.configure(bg='#f0f0f0')
        
        self.criar_widgets()
        self.carregar_tarefas()
        self.configurar_atalhos()
        
    def criar_widgets(self):
        # Frame principal
        self.frame_principal = ttk.Frame(self.janela)
        self.frame_principal.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(self.frame_principal, 
                          text="Minhas Tarefas", 
                          font=('Helvetica', 16, 'bold'))
        titulo.pack(pady=10)
        
        # Frame de entrada
        frame_entrada = ttk.Frame(self.frame_principal)
        frame_entrada.pack(fill='x', pady=10)
        
        self.entrada = ttk.Entry(frame_entrada, width=40, font=('Helvetica', 10))
        self.entrada.pack(side='left', padx=5)
        
        # Frame de botões
        frame_botoes = ttk.Frame(self.frame_principal)
        frame_botoes.pack(pady=10)
        
        estilo = ttk.Style()
        estilo.configure('Acento.TButton', padding=5)
        
        self.botao_adicionar = ttk.Button(frame_botoes, 
                                        text=" Adicionar",
                                        command=self.adicionar_tarefa,
                                        style='Acento.TButton')
        self.botao_adicionar.pack(side='left', padx=5)
        
        self.botao_remover = ttk.Button(frame_botoes,
                                      text=" Remover",
                                      command=self.remover_tarefa,
                                      style='Acento.TButton')
        self.botao_remover.pack(side='left', padx=5)
        
        self.botao_concluir = ttk.Button(frame_botoes,
                                       text=" Concluir",
                                       command=self.concluir_tarefa,
                                       style='Acento.TButton')
        self.botao_concluir.pack(side='left', padx=5)
        
        # Lista de tarefas
        self.lista_tarefas = tk.Listbox(self.frame_principal,
                                      width=50,
                                      height=15,
                                      font=('Helvetica', 10),
                                      selectmode=tk.SINGLE,
                                      bg='white',
                                      selectbackground='#0078d7')
        self.lista_tarefas.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.lista_tarefas)
        scrollbar.pack(side='right', fill='y')
        self.lista_tarefas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lista_tarefas.yview)

    def carregar_tarefas(self):
        """Carrega as tarefas do arquivo (se existir)."""
        if os.path.exists("tarefas.txt"):
            with open("tarefas.txt", "r", encoding='utf-8') as f:
                for linha in f:
                    self.lista_tarefas.insert(tk.END, linha.strip())

    def salvar_tarefas(self):
        """Salva as tarefas no arquivo antes de fechar o app."""
        with open("tarefas.txt", "w", encoding='utf-8') as f:
            tarefas = self.lista_tarefas.get(0, tk.END)
            for tarefa in tarefas:
                f.write(f"{tarefa}\n")

    def adicionar_tarefa(self):
        tarefa = self.entrada.get().strip()
        if tarefa:
            self.lista_tarefas.insert(tk.END, tarefa)
            self.entrada.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Digite uma tarefa antes de adicionar!")

    def remover_tarefa(self):
        try:
            indice = self.lista_tarefas.curselection()[0]
            self.lista_tarefas.delete(indice)
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")

    def concluir_tarefa(self):
        try:
            indice = self.lista_tarefas.curselection()[0]
            tarefa = self.lista_tarefas.get(indice)
            if not tarefa.startswith("✔️"):
                self.lista_tarefas.delete(indice)
                self.lista_tarefas.insert(indice, f"✔️ {tarefa}")
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para marcar!")

    def configurar_atalhos(self):
        self.janela.bind('<Return>', lambda e: self.adicionar_tarefa())
        self.janela.bind('<Delete>', lambda e: self.remover_tarefa())
        self.janela.bind('<space>', lambda e: self.concluir_tarefa())
        self.janela.protocol("WM_DELETE_WINDOW", 
                           lambda: [self.salvar_tarefas(), self.janela.destroy()])

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = GerenciadorTarefas()
    app.iniciar()