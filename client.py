# client.py
import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'  # The server's IP address
PORT = 12783        # The port we're connecting to

# Connect to the host
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("\nConnected to the server!")

# Set up the game
player_o = TicTacToe("O")

while True:
    print("\n\n T I C - T A C - T O E ")
    while not player_o.did_win("O") and not player_o.did_win("X") and not player_o.is_draw():
        player_o.draw_grid()

        # Wait to receive the symbol list and update it
        print("Waiting for other player...")
        try:
            x_symbol_list = s.recv(1024)
            if not x_symbol_list:
                print("Server disconnected.")
                break
            x_symbol_list = pickle.loads(x_symbol_list)
            player_o.update_symbol_list(x_symbol_list)
        except Exception as e:
            print(f"Error receiving data from server: {e}")
            break

        if player_o.did_win("X") or player_o.is_draw():
            break

        # Draw grid and ask for coordinate
        player_o.draw_grid()
        player_coord = input("Enter coordinate (e.g., A1): ").strip()
        while not player_o.edit_square(player_coord):
            player_coord = input("Enter a valid coordinate (e.g., A1): ").strip()

        # Pickle the symbol list and send it
        o_symbol_list = pickle.dumps(player_o.symbol_list)
        s.send(o_symbol_list)

    # End game messages
    player_o.draw_grid()
    if player_o.did_win("O"):
        print("Congrats, you won!")
    elif player_o.is_draw():
        print("It's a draw!")
    else:
        print("Sorry, the server won.")

    # Wait for server's rematch response
    try:
        rematch = s.recv(1024)
        if not rematch:
            print("Server disconnected.")
            break
        rematch = pickle.loads(rematch)
    except Exception as e:
        print(f"Error receiving rematch response: {e}")
        break

    if rematch == "N":
        break
    player_o.restart()

s.close()
print("Game over!")
