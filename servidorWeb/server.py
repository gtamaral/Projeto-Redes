import socket       # importando a biblioteca socket

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

# output
print(f'O cliente enviou: {dadoRecebido}')

# responde o txt pong para o cliente
socket_client.sendall(b'pong')

# encerrando a cnx
socket_client.close()

