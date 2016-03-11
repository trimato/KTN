import json


class MessageParser:
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
        }

    def parse(self, payload):
        payload = json.loads(payload)
        # decodes the JSON object to a dictionary

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print("The server did not respond correctly, please try again.")
            # Response not valid


    def parse_error(self, payload):
        print(payload['timestamp']+ "Error: "+ payload['content'])


    def parse_info(self, payload):
        print(payload['timestamp']+ "  "+ payload['sender']+ ":"+ "\t"+ payload['content'])


    def parse_message(self, payload):
        print(payload['timestamp']+ "  "+ payload['sender']+ ":"+ "\t" + payload['content'])


    def parse_history(self, payload):
        for i in payload['content']:
            print(payload['sender']+ ":"+ "\t"+ i)