import socket 

enderecoServer = 'localhost'
portaServer = 8000

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# cria um objeto socket e passa como para parametro 02 argumentos
# AFINET = IP // socket_stream = tcp ===> tcp/ip

# conecta no servidor
socket_client.bind(('localhost', 8000))

# envia ping para o server
socket_client.sendall(b'ping!')

# aguarda o server responder
dado = socket_client.recv(1024)
dado = dado.decode()
# output
print(f'recebido do servidor: {dado}')

# output
print(f'conexao deu certo.')

# finaliza a conexao
socket_client.close()