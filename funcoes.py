from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

# Função para criptografar dados usando AES
def encrypt_aes(nome_pasta, key):
    conteudo = []
    nomes_arq = []
    caminho_pasta = os.path.join(os.getcwd(), nome_pasta)
    
    # Verifica se a pasta existe
    if os.path.isdir(caminho_pasta):
        # Lista todos os arquivos .txt
        for arquivo in os.listdir(caminho_pasta):
            if arquivo.endswith('.txt'):
                nomes_arq.append(arquivo)
                caminho_arquivo = os.path.join(caminho_pasta, arquivo)

                # Lê o conteúdo do arquivo
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    resultado = f.read()
                    conteudo.append(resultado)
    
    i = 0    
    for data in conteudo:
        # Gera um IV (Initialization Vector) aleatório de 16 bytes para cada arquivo
        iv = get_random_bytes(16)
        
        # Inicializa o cifrador AES em modo CBC
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Padding do dado para garantir que o tamanho seja múltiplo de 16 bytes
        padded_data = pad(data.encode('utf-8'), AES.block_size)
        
        # Criptografa os dados
        ciphertext = cipher.encrypt(padded_data)
        
        # Salva o arquivo criptografado concatenando o IV e o ciphertext na mesma pasta
        with open(os.path.join(caminho_pasta, f'{nomes_arq[i]}.enc'), 'wb') as f:
            f.write(iv + ciphertext)

        # Remove o arquivo original após a criptografia
        os.remove(os.path.join(caminho_pasta, nomes_arq[i]))
        print(f"Arquivo '{nomes_arq[i]}' criptografado e removido com sucesso!")
        
        i += 1
    
    # Salva a chave usada para criptografia em um arquivo separado
    with open(os.path.join(caminho_pasta, 'key.rans'), 'wb') as chave_file:
        chave_file.write(key)
    
    print("Criptografia concluída com sucesso!")


# Função para descriptografar dados usando AES e excluir arquivos criptografados
def decrypt_aes(nome_pasta, key):
    caminho_pasta = os.path.join(os.getcwd(), nome_pasta)
    
    # Verifica se a pasta existe
    if os.path.isdir(caminho_pasta):
        # Lista todos os arquivos .enc na pasta
        for arquivo in os.listdir(caminho_pasta):
            if not arquivo.endswith('.enc'):
                continue

            caminho_arquivo = os.path.join(caminho_pasta, arquivo)

            # Abre o arquivo criptografado em modo binário
            with open(caminho_arquivo, 'rb') as f:
                conteudo = f.read()
                
            # O IV está nos primeiros 16 bytes do dado criptografado
            iv = conteudo[:16]
            
            # O texto criptografado começa após o IV
            ciphertext = conteudo[16:]
            
            try:
                # Inicializa o decifrador AES em modo CBC com o mesmo IV
                cipher = AES.new(key, AES.MODE_CBC, iv)
                
                # Descriptografa e remove o padding
                original_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
                
                # Remove a extensão .enc para salvar o arquivo descriptografado
                arquivo_descriptografado = arquivo.replace('.enc', '')
                
                # Escreve o arquivo descriptografado no modo texto
                with open(os.path.join(caminho_pasta, arquivo_descriptografado), 'w', encoding='utf-8') as f_out:
                    f_out.write(original_data.decode('utf-8'))
                
                print(f"Arquivo '{arquivo_descriptografado}' descriptografado com sucesso!")

                # Fechar o arquivo antes de excluí-lo
                f_out.close()
                
                # Remove o arquivo criptografado após a descriptografia
                os.remove(caminho_arquivo)
                print(f"Arquivo criptografado '{arquivo}' removido.")
            except (ValueError, KeyError) as e:
                print(f"Erro de descriptografia: {str(e)}")
                raise

    print("Descriptografia concluída com sucesso!")
