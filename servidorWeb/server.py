import socket      # importando a biblioteca socket
import sys
from threading import Thread


enderecoServer = '0.0.0.0'
portaServer = 8000

type_arquivoBinario = ['png', 'jpeg', 'bmp']
type_arquivoTexto = ['html', 'css', 'js']

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

    # Verifica se o arquivo solicitado é o arquivo bloqueado
    if arquivo_solicitado == 'arquivo_bloqueado.html':
        print(f'Acesso negado ao arquivo {arquivo_solicitado}')
        socket_client.sendall(b'HTTP/1.1 403 Forbidden\r\n\r\nForbidden')
        socket_client.close()
        return

    # obtendo extensao do arquivo
    extensao = arquivo_solicitado.split('.')[-1]
    
    arquivoBinario = False
    if extensao in type_arquivoBinario:
        arquivoBinario = True

    # abrir o arquivo
    try:
        if arquivoBinario:
            file = open(arquivo_solicitado, 'rb')
        else:
            file = open(arquivo_solicitado, 'r', encoding = 'utf-8')    
        conteudo_arquivo = file.read()

    # quando o arquivo nao é encontrado == error404
    except FileNotFoundError:
        print(f'Arquivo não existe {arquivo_solicitado}')
        socket_client.sendall(b'HTTP/1.1 404 File not found\r\n\r\nFile not found')
        socket_client.close()
        return
    
    except:
        print(f'Erro na requisição {arquivo_solicitado}')
        socket_client.sendall(b'HTTP/1.1 400 Bad Request\r\n\r\nBad Request')
        socket_client.close()
        return

    # Verifica se o arquivo possui permissão de leitura
    if not file.readable():
        print(f'Erro de permissão na leitura do arquivo {arquivo_solicitado}')
        socket_client.sendall(b'HTTP/1.1 403 Forbidden\r\n\r\nForbidden')
        socket_client.close()
        return
    file.close()

    # resposta ao browser
    cabecalho_resposta = f'HTTP/1.1 200 OK\r\n\r\n'
    corpo_resposta = conteudo_arquivo

    if arquivoBinario:
        resposta_final = bytes(cabecalho_resposta, 'utf-8') + corpo_resposta
        socket_client.sendall(resposta_final)   #responde p o cliente
    else:
        if cabecalho_resposta.startswith('HTTP/1.0'):
            print(f'Versão HTTP não suportada: {cabecalho_resposta}')
            socket_client.sendall(b'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\nHTTP Version Not Supported')
            socket_client.close()
            return
        resposta_final = cabecalho_resposta + corpo_resposta
        socket_client.sendall(resposta_final.encode('utf-8'))   #responde p o cliente
   
    # encerrando a cnx
    socket_client.close()


socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# cria um objeto socket e passa como para parametro 02 argumentos
# AFINET = IP // socket_stream = tcp ===> tcp/ip

 # solicita ao windows para que escute na porta 8000 atraves do metodo "BIND"
socket_servidor.bind((enderecoServer, portaServer))    # o primeiro argumento serve para ouvir em todas as placas de redes disponiveis
socket_servidor.listen(10)

while True:  
    # aguardo uma conexao com o client
    print(f'servidor ouvindo em {enderecoServer} : {portaServer} pronto para receber as conexoes')    # ouput
    socket_client, client_addr = socket_servidor.accept()
    # a funcao accept retorna o endereco ipv4 e a porta de origigem do mesmo

    #  enviando a requisicao para a thread processa-la
    Thread(target=processa_solicitacao, args=(socket_client, client_addr)).start()


socket_servidor.close()
#testeteste