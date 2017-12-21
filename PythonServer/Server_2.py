import socket
import FindMatch as fm
import Evolution as ev

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
#use the next line when testing locally
ip = "0.0.0.0"
port = 23260

address = (ip, port)
print address

server.bind(address)
server.listen(1)
print "[+] Started listening on ", ip, ":", port

client, addr = server.accept()
print "[+] Got a connection from ", addr[0], ":", addr[1]

while True:
    data = client.recv(1024)
    print "[+] Received ", data, " from the client"
    print "     Processing data"

    fm = fm.FindMatch(data)
    match = fm.main()
    print match

    if data == "disconnect":
        client.send("Closing client")
        client.close()
        break

    else:
        client.send(match)
        print "     Processing done\n[+] Reply sent"




