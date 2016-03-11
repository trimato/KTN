# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = 9998
        self.host = 'localhost'
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        MessageReceiver(self, self.connection)

        login_username = raw_input("Login username: ")
        self.login(login_username)

        while True:
            message = raw_input("> ")
            self.send_message(message)


    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        #print("<-- " + message) # TODO: REMOVE DEBUG
        parser = MessageParser()
        parser.parse(message)
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload

        data = json.dumps(data)

        self.connection.send(data)
        #print("--> " + data) # TODO: REMOVE DEBUG

        # More methods may be needed!

    def help(self):
        self.create_request('help')

    def login(self, username):
        self.create_request('login', username)
        self.username = username

    def logout(self):
        self.create_request('logout', self.username)

    def send_message(self, message):
        self.create_request('msg', message)

    def create_request(self, request, content):
        if not content:
            content = ''
        payload = {
            'request': request,
            'content': content,
        }
        self.send_payload(payload)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)