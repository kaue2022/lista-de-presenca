import customtkinter as ctk
from datetime import datetime
import csv
import os

# Função para cadastrar a presença
def cadastrar():
    nome = registro_nome.get().strip()
    email = registro_email.get().strip()
    hora = datetime.now().strftime('%H:%M')

    if nome == '' or email == '' or '@' not in email:
        resultado.configure(text='Preencha todos os campos corretamente!', text_color='red')
        return

    try:
        # Salvando os dados no arquivo CSV
        with open('presencas.csv', 'a', encoding='utf-8', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([nome, email, hora])
        
        resultado.configure(text='Presença registrada com sucesso!', text_color='green')
    except Exception as e:
        resultado.configure(text=f'Erro ao salvar: {e}', text_color='red')
    
    # Chama a função que abre a nova janela e lista as presenças
    lista_atualizada()

# Função para abrir a janela com a lista de presenças
def lista_atualizada():
    tela2 = ctk.CTkToplevel(tela1)
    tela2.geometry("500x500")
    tela2.title('Lista de presenças atualizada')
    tela2.grab_set()  # Impede de clicar na tela principal enquanto a nova estiver aberta

    # Mensagem inicial
    msg = ctk.CTkLabel(tela2, text="Bem-vindo! Sua presença está confirmada",
                       font=('Arial', 14, 'bold'), text_color='white')
    msg.pack(pady=10)

    # Caixa de texto para mostrar os dados do CSV
    caixa = ctk.CTkTextbox(tela2, width=460, height=350)
    caixa.pack(pady=10)

    try:
        # Lendo o CSV e mostrando na caixa de texto
        with open('presencas.csv', 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                if len(linha) >= 3:
                    nome, email, hora = linha
                    caixa.insert("end", f"Nome:{nome} | Email:{email} | Hora:{hora}\n")
    except FileNotFoundError:
        caixa.insert("end", "Nenhum registro encontrado ainda.")

# Criando a janela principal
tela1 = ctk.CTk()
tela1.title("Registro lista de presença")
tela1.geometry('500x500')

# Descrição acima do campo de preenchimento do nome
label_nome = ctk.CTkLabel(tela1, text="Nome", font=('Arial', 14, 'bold'), width=200)
label_nome.pack(pady=10)

# Entrada de nome do usuário
registro_nome = ctk.CTkEntry(tela1, placeholder_text="seu nome...", width=200)
registro_nome.pack(padx=10)

# Descrição acima do campo de e-mail
label_email = ctk.CTkLabel(tela1, text='Email', font=('Arial', 14, 'bold'), width=200)
label_email.pack(pady=10)

# Entrada de e-mail do usuário
registro_email = ctk.CTkEntry(tela1, placeholder_text="seu email...", width=200)
registro_email.pack(pady=10)

# Botão para registrar a presença
registrar = ctk.CTkButton(tela1, text='Registrar presença', command=cadastrar)
registrar.pack(pady=10)

# Campo para exibir o resultado (sucesso ou erro)
resultado = ctk.CTkLabel(tela1, text="", font=('Arial', 14, 'bold'))
resultado.pack(pady=10)

# Rodando a janela principal
tela1.mainloop()
