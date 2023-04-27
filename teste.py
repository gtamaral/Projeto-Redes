import socket      # importando a biblioteca socket
import sys
from threading import Thread
import subprocess

enderecoServer = '0.0.0.0'
portaServer = 8000

type_arquivoBinario = ['png', 'jpeg', 'bmp']
type_arquivoTexto = ['html', 'css', 'js']
type_arquivoExecutavel = ['php', 'py', 'pl']

def processa_solicitacao(socket_client, client_addr):
    # output
    print(f'cliente se conextou com exito. {client_addr[0]}: {client_addr[1]}')

    # receber dados do cliente
    dadoRecebido = socket_client.recv(1024)     #recebe ate 1024btes
    dadoRecebido = dadoRecebido.decode()        #decodifica o byte p str

    # parcing do cabeçalho
    headers = dadoRecebido.split('\r\n')
    header_get = headers[0] # isolando a primeira linha do cabeçalho

    # obtendo o arquivo solicitado
    arquivo_solicitado = header_get.split(' ') [1] [1:] # transformando a primeira linha em um array, pegando o segundo elemento e eliminando o primeiro caracter que seria "/"
    print (f'Arquivo solicitado: {arquivo_solicitado}')

    # obtendo extensao do arquivo
    extensao = arquivo_solicitado.split('.')[-1]
    
    arquivoBinario = False
    arquivoExecutavel = False
    
    if extensao in ['py']:
        arquivoExecutavel = True
    if extensao in type_arquivoBinario:
        arquivoBinario = True

    # abrir o arquivo
    try:
        if arquivoExecutavel:
            processo = subprocess.run(['python', arquivo_solicitado], stdout=subprocess.PIPE, text = True)
            stdout = processo.stdout
            headers = f'HTTP/1.1 200 OK\r\n\r\n'
            answer = headers + stdout
            socket_client.sendall(answer.encode('utf-8'))
            return True
        elif arquivoBinario:
            file = open(arquivo_solicitado, 'rb')
            bloco = file.read(1024)  # ler em blocos de 1024 bytes
            while bloco:
                socket_client.send(bloco)
                bloco = file.read(1024)
            file.close()
        else:
            file = open(arquivo_solicitado, 'r', encoding = 'utf-8')
            bloco = file.read(1024)  # ler em blocos de 1024 bytes
            while bloco:
                socket_client.send(bloco.encode('utf-8'))
                bloco = file.read(1024)
            file.close()

    # quando o arquivo nao é encontrado == error404
    except FileNotFoundError:
        print(f'Arquivo não existe {arquivo_solicitado}')
        socket_client.sendall(b'HTTP/1.1 404 File not found\r\n\r\nFile