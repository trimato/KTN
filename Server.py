# -*- coding: utf-8 -*-
import SocketServer
import time
import json
import datetime
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

# Dictionary of connected clients [keys] = connection, [values] = name
connectedClients = {}

# List of chat history
history = []

# Regular expression allowed characters for names
viableCharacters = re.compile("^[a-zA-Z0-9]+$")

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.client = ''
        self.login_flag = False

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            if not received_string:
                continue
            print("<-- [", self.ip, "]:", received_string) # TODO: REMOVE DEBUG
            received_string = json.loads(received_string)
            request = received_string['request']
            content = received_string['content']

            # Handling login request
            if request == 'login' and content != None:
                if not self.isValidName(content):
                    self.respond('error', 'Invalid name!')
                else:
                    self.client = content
                    if self.client not in connectedClients:
                        connectedClients.setdefault(self.connection, []).append(self.client)
                        self.respond('info', "Login successful!")
                        self.login_flag = True
                        self.respond('history', history)
                    else:
                        self.respond('error', 'Already logged in!')

            # Handling help request
            elif request == 'help':
                if self.login_flag:
                    self.respond('info', 'Supported requests is login, logout, history, msg and names! ')
                else:
                    self.respond('info', 'Supported request is login! ')

            # Ensures that only logged in clients can access the server's main functionality
            if self.login_flag:

                # Handling logout request
                if request == 'logout':
                    self.client = content
                    if self.client in connectedClients and content == None:
                        del connectedClients[self.connection]
                        self.login_flag = False
                    else:
                        self.respond('error', 'You are not logged in!')

                # Handling msg request
                elif request == 'msg':
                    connections = connectedClients.keys()
                    message = self.generateMessage('message', content)
                    for client in connections:
                        client.send(message)
                    history.append(message)

                # Handling history request
                elif request == 'history':
                    self.respond('history', history)

                # Handling names request
                elif request == 'names':
                    names = connectedClients.values()
                    names = ','.join(names)
                    self.respond('info', names)
                else:
                    pass

            else:
                pass

    def respond(self, response, content):
        response = json.dumps(
            {
                'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'sender': self.client,
                'response': response,
                'content': content,
            }
        )
        if response == 'message':
            history.append(response)
        self.connection.send(response)
        print("--> [", self.ip, "]:", response) # TODO: REMOVE DEBUG

    def generateMessage(self, response, content):
        message = json.dumps(
            {
                'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'sender': self.client,
                'response': response,
                'content': content,
            }
        )
        return message

        # TODO: Add handling of received payload from client

    def isValidName (self, name):
        return viableCharacters.match(name)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()