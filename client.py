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
        addr, dataPort = sock.getsockname()
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

        while True:
            command = raw_input('myftp> ')

            if command.upper() == 'LS':
                dataPort += 1

                isPortAvailable = False 

                while isPortAvailable == False:
                    try:
                        dataSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
                        dataSocket.bind(('',dataPort))
                        isPortAvailable = True

                    except socket.error:
                        dataPort += 1

                splitAddress = str.split(addr, ".")
                dataPortOne = str(int(hex(dataPort)[2:4], 16))
                dataPortTwo = str(int(hex(dataPort)[4:6], 16))

                message = 'PORT ' + splitAddress[0] \
                                + "," + splitAddress[1] + "," + splitAddress[2] \
                                + "," + splitAddress[3] + "," \
                                + dataPortOne + ',' + dataPortTwo + '\r\n'

                sock.send(message)
                response = sock.recv(1024)
                print(response)

                message = 'NLST\r\n'
                sock.send(message)

                dataSocket.listen(1)
                dataConn = dataSocket.accept()[0]

                response = sock.recv(1024)
                print(response)

                listing = dataConn.recv(1024)
                print(listing)
                dataConn.close()

                response = sock.recv(1024)
                print(response)
                dataSocket.close()

            elif command[0:3].upper() == 'PUT':
                dataPort += 1

                isPortAvailable = False 

                while isPortAvailable == False:
                    try:
                        dataSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
                        dataSocket.bind(('',dataPort))
                        isPortAvailable = True

                    except socket.error:
                        dataPort += 1

                splitAddress = str.split(addr, ".")
                dataPortOne = str(int(hex(dataPort)[2:4], 16))
                dataPortTwo = str(int(hex(dataPort)[4:6], 16))

                message = 'PORT ' + splitAddress[0] \
                                + "," + splitAddress[1] + "," + splitAddress[2] \
                                + "," + splitAddress[3] + "," \
                                + dataPortOne + ',' + dataPortTwo + '\r\n'

                sock.send(message)
                response = sock.recv(1024)
                print(response)

                message = 'STOR ' + command[4:] + '\r\n'
                sock.send(message)

                dataSocket.listen(1)
                dataConn = dataSocket.accept()[0]

                response = sock.recv(1024)
                print(response)

                with open(command[4:], 'rb') as file:
                    segment = file.read(1024)

                    while segment: 
                        dataConn.send(segment) 
                        segment = file.read(1024)

                dataConn.close()
                response = sock.recv(1024)
                print(response)
                dataSocket.close()

            elif command[0:3].upper() == 'GET':
                dataPort += 1

                isPortAvailable = False 

                while isPortAvailable == False:
                    try:
                        dataSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
                        dataSocket.bind(('',dataPort))
                        isPortAvailable = True

                    except socket.error:
                        dataPort += 1

                splitAddress = str.split(addr, ".")
                dataPortOne = str(int(hex(dataPort)[2:4], 16))
                dataPortTwo = str(int(hex(dataPort)[4:6], 16))

                message = 'PORT ' + splitAddress[0] \
                                + "," + splitAddress[1] + "," + splitAddress[2] \
                                + "," + splitAddress[3] + "," \
                                + dataPortOne + ',' + dataPortTwo + '\r\n'

                sock.send(message)
                response = sock.recv(1024)
                print(response)

                message = 'RETR ' + command[4:] + '\r\n'
                sock.send(message)

                dataSocket.listen(1)
                dataConn = dataSocket.accept()[0]

                response = sock.recv(1024)
                print(response)

                incomingFile = dataConn.recv(1024)
                print(incomingFile)

                with open(command[4:], 'wb') as file:
                    for line in incomingFile:
                        file.write(line)

                dataConn.close()
                response = sock.recv(1024)
                print(response)
                dataSocket.close()

            elif command[0:6].upper() == 'DELETE':
                message = 'DELE ' + command[7:] + '\r\n'

                sock.send(message)
                
                response = sock.recv(1024)
                print(response)

            elif command[0:2].upper() == 'CD':
                message = 'CWD ' + command[3:] + '\r\n'

                sock.send(message)
                
                response = sock.recv(1024)
                print(response)

            elif command.upper() == 'QUIT':
                sock.send('QUIT\r\n')
                response = sock.recv(1024)
                print(response)
                sock.close()
                quit()

            else:
                print("Command not available. Please try again")
                

    except socket.error as e:
        sys.stderr.write('ERROR: {}\n'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()