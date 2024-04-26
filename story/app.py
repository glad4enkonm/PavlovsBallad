from flask import Flask, request, jsonify
from main import run
app = Flask(__name__)


@app.route('/letitrun', methods=['PUT'])
def telegraph():
    data = request.get_json()
    if data:
        idToStart = run(data["age"], data["interest"])
        if idToStart != "":
            return jsonify({'status': 'success', 'response': idToStart})    
    return jsonify({'status': 'error', 'message': 'No message provided'})

if __name__ == '__main__':
    app.run()
