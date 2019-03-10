import socket

# 主要負責將判斷結果傳回去
def main(entitys):

	return entitys + 'hi'

if __name__ == '__main__':
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
	host = "140.116.245.146" # Get local machine name
	port = 1994 # Reserve a port for your service.
	soc.bind((host, port))   # Bind to the port
	soc.listen(5) # Now wait for client connection.
	print("server running..")
	while True:
		conn, addr = soc.accept() # Establish connection with client.
		print ("Got connection from", addr)
		questions = conn.recv(1024)
		answers = main(questions.decode("utf-8"))
		conn.send((answers + "\n").encode('utf-8'))