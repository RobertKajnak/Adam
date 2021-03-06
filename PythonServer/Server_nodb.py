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
    f = open('log.txt', 'w')
    data = client.recv(1024)
    f.write('data as recieved:\n')
    f.write(data)
    #print "[+] Received ", data, " from the client"
    decr = json.loads(data)
    f.write('\n\nJSON deserialized(py object form):\n')
    f.write(decr.__str__())
    
    f.write('\n\nToken only:\n')
    f.write(decr['token'].__str__())
    print decr['token']
    print "     Processing data"
    
    r = requests.get("https://graph.facebook.com/v2.11/me/posts?access_token=" + decr['token'])

    f.write('\n\nResponse to the request:\n')
    f.write(r.__str__())
    print r.content
    
    f.write('\n\nActual request content:\n' )
    f.write(r.content)

    dataToDbObject = json.loads(r.content)
    f.write('\n\nDeserialized:\n')
    f.write(dataToDbObject.__str__())

    f.close()
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

