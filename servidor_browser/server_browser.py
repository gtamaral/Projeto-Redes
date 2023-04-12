import socket      # importando a biblioteca socket
import sys

enderecoServer = '0.0.0.0'
portaServer = 8000

socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# cria um objeto socket e passa como para parametro 02 argumentos
# AFINET = IP // socket_stream = tcp ===> tcp/ip

 # solicita ao windows para que escute na porta 8000 atraves do metodo "BIND"
socket_servidor.bind((enderecoServer, portaServer))    # o primeiro argumento serve para ouvir em todas as placas de redes disponiveis
socket_servidor.listen()

# aguardo uma conexao com o client
print(f'servidor ouvindo em {enderecoServer} : {portaServer} pronto para receber as conexoes')    # ouput
socket_client, client_addr = socket_servidor.accept()
# a funcao accept retorna o endereco ipv4 e a porta de origigem do mesmo

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

# abrir o arquivo
try:
    file = open(arquivo_solicitado, 'r', encoding = 'utf-8')
    conteudo_arquivo = file.read()

except FileNotFoundError:
    print(f'Arquivo não existe {arquivo_solicitado}')
    socket_client.sendall(b'HTTP/1.1 404 File not found\r\n\r\nFile not found')
    socket_client.close()
    sys.exit(1)

# enviar o conteúdo do arquivo para o browser
arquivo_solicitado

# resposta ao browser
cabecalho_resposta = f'HTTP/1.1 200 OK\r\n\r\n'
corpo_resposta = arquivo_solicitado

resposta_final = cabecalho_resposta + corpo_resposta

# responde para o cliente
socket_client.sendall(resposta_final.encode('utf-8'))

# encerrando a cnx
socket_client.close()

