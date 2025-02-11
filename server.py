# server.py
import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'  # Local host
PORT = 12784        # Port to listen on for clients

# Set up the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print("\nWaiting for a connection...")
client_socket, client_address = s.accept()
print(f"Connected to {client_address}!")

# Set up the game
player_x = TicTacToe("X")

while True:
    print("\n\n T I C - T A C - T O E ")
    while not player_x.did_win("X") and not player_x.did_win("O") and not player_x.is_draw():
        player_x.draw_grid()
        player_coord = input("Enter coordinate (e.g., A1): ").strip()
        while not player_x.edit_square(player_coord):
            player_coord = input("Enter a valid coordinate (e.g., A1): ").strip()

        # Pickle the symbol list and send it
        x_symbol_list = pickle.dumps(player_x.symbol_list)
        client_socket.send(x_symbol_list)

        if player_x.did_win("X") or player_x.is_draw():
            break

        # Wait to receive the symbol list and update it
        print("Waiting for other player...")
        try:
            o_symbol_list = client_socket.recv(1024)
            if not o_symbol_list:
                print("Client disconnected.")
                break
            o_symbol_list = pickle.loads(o_symbol_list)
            player_x.update_symbol_list(o_symbol_list)
        except Exception as e:
            print(f"Error receiving data from client: {e}")
            break

    # End game messages
    player_x.draw_grid()
    if player_x.did_win("X"):
        print("Congrats, you won!")
    elif player_x.is_draw():
        print("It's a draw!")
    else:
        print("Sorry, the client won.")

    # Ask for a rematch
    rematch = input("Rematch? (Y/N): ").strip().upper()
    client_socket.send(pickle.dumps(rematch))

    if rematch == "N":
        break
    player_x.restart()

client_socket.close()
s.close()
print("Game over!")
