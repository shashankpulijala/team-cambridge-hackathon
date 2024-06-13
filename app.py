from flask import Flask, jsonify, render_template
from flask_cors import CORS
from uagents.query import query
from uagents import Model
import json
import logging

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enables CORS for all domains on all routes

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the address for the parser agent
parser_address = 'agent1qgtvev96vtf05f9jlhn7mu94vku9l7ncleuacmyef8fljrg5jwt0qs7sgll'

# Define Request and Response Models for Parsing
class Message(Model):
    message: str

class Response(Model):
    response: str

class ErrorMessage(Model):
    error: str

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for parsing a file
@app.route('/api/parse/<string:file_name>', methods=['GET'])
async def parse_file(file_name):
    # try:
    response = await query(destination=parser_address, message=Message(message=file_name), timeout=15.0)

    if response is None:
        logging.error("No response received from the parser agent.")
        return jsonify( "You can opt for the basic pension plan."), 500
    else:
        return (response)


        # if isinstance(response, ErrorMessage):
        #     logging.error(f"Error message received: {response.error}")
        #     return jsonify({"error": response.error}), 500
        #
        # parsed_data = json.loads(response.decode_payload())
        # logging.info(parsed_data)
        # logging.info(parsed_data['response'])
        # return jsonify({"message": parsed_data['response']})

    # except Exception as e:
    #     logging.error(f"An error occurred: {e}")
    #     return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
