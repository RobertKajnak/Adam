import socket
import json
import requests
#import FindMatch as fm
#import Evolution as ev

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
ip = "0.0.0.0"
print ip
port = 23260

address = (ip, port)

server.bind(address)
server.listen(1)
print "[+] Started listening ", ip, ":", port

client, addr = server.accept()
print "[+] Got a connection from ", addr[0], ":", addr[1]

while True:
    data = client.recv(1024)
    #print "[+] Received ", data, " from the client"
    decr = json.loads(data)
    print decr['token']
    print "     Processing data"
    
    r = requests.get("https://graph.facebook.com/v2.11/me/posts?access_token=" + decr['token'])

    print r.content
    
    dataToDbObject = json.loads(r.content)

    if data != " ":
        client.send("Closing client")
        client.close()
        break

    else:
        print "Client sent ", data
        print "     Processing done\n[+] Reply sent"


''' sample token:
    EAAXckKsm7pQBACnaXqAFUb7UCoEuR8IvSobbyZBKRBcsqW0ZB7tvOJxcPymtXLZAh1Vk0S1qeCXx1XZCXcrZBTJfieReYB9IWNebWmZBY5p5GzvhqBHW3YMGsiAYhhHSy4imZA4R9CtOfgqbKgBd6y1MRF7V4ZALMRoa31H12CJztoKZCJZAlutMEsBX1x7HHItak3Svn7aj1s5gZDZD
'''

