import socket

# Configuração do cliente
HOST = '127.0.0.1'  # endereço IP do servidor
PORT = 5555  # porta do servidor

# Inicialização do socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Loop principal do cliente
while True:
    # Aguarda a entrada do usuário para enviar uma mensagem para o servidor
    message = input('Digite uma mensagem para enviar ao servidor: ')

    # Envia a mensagem para o servidor
    client_socket.sendall(message.encode())

    # Recebe a mensagem do servidor
    server_message = client_socket.recv(1024).decode()

    # Exibe a mensagem recebida do servidor
    print('Mensagem recebida do servidor:', server_message)

# Encerra a conexão com o servidor
client_socket.close()
