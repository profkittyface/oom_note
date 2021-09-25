from flask import jsonify

class ResponseGenerator():
    def __init__(self):
        self.response = {'message': None, 'error': None}
    def getResponse(self, message):
        self.response['message'] = message
        return jsonify(self.response)
    def getError(self, message):
        self.response['message'] = message
        self.response['error'] = True
        return jsonify(self.response)
