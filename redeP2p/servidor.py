import socket

# Configuração do servidor
HOST = '0.0.0.0'  # endereço IP do servidor
PORT = 5555  # porta do servidor

# Inicialização do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # o servidor aguardará apenas 1 conexão

# Aguardar conexão
print('Aguardando conexão...')
client_socket, address = server_socket.accept()
print('Conexão estabelecida com', address)

# Loop principal do servidor
while True:
    # Recebe a mensagem do cliente
    message = client_socket.recv(1024).decode()

    # Verifica se a mensagem está vazia (isso pode ocorrer caso o cliente seja desconectado)
    if not message:
        break

    # Exibe a mensagem recebida
    print('Mensagem recebida:', message)

    # Aguarda a entrada do usuário para enviar uma mensagem para o cliente
    server_message = input('Digite uma mensagem para enviar ao cliente: ')

    # Envia a mensagem para o cliente
    client_socket.sendall(server_message.encode())

# Encerra a conexão com o cliente
client_socket.close()

# Encerra o socket do servidor
server_socket.close()
