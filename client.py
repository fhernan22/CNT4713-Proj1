import socket
import sys
import os

def main():
    try:
        SERVER = sys.argv[1]

    except IndexError:
        sys.stderr.write('ERROR: Server name or IP address must be provided.\n')
        sys.exit(1)

    PORT = 21

    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        sock.connect((SERVER,PORT))
        response = sock.recv(1024)
        print(response)

        userName = raw_input("Please enter username: ")
        password = raw_input("Please enter password: ")

        sock.send(('USER ' + userName + '\r\n'))
        response = sock.recv(1024) 
        sock.send(('PASS ' + password + '\r\n'))
        response = sock.recv(1024) 
        print(response)

        if int(response[0:3]) >= 300:
            sys.exit(1)

    except socket.error as e:
        sys.stderr.write('ERROR: {}\n'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()