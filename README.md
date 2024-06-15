# Insurance Quote Processing Agents

This repository contains three agents that work together to process insurance documents, extract relevant information, and generate insurance quotes based on predefined rules. The agents are implemented using the `uagents` library and OpenAI's GPT-3.5 model.

## Agents Overview

### Agent 2: Parser

The Parser agent is responsible for parsing the text from insurance documents, converting tables to text, and generating a mapping of key fields required for an insurance quote.

- **Port**: 5001
- **Seed**: `jkhgfdsa`
- **Endpoint**: `http://localhost:5001/submit`

### Agent 3: Rules

The Rules agent processes the parsed document text received from the Parser agent. It generates condition statements and converts them into if-else statements in Python.

- **Port**: 5002
- **Seed**: `khljghfgfd`
- **Endpoint**: `http://localhost:5002/submit`

### Agent 4: Premium

The Premium agent applies the generated if-else statements to a dataset to evaluate insurance quotes and send the final quotes back to the Parser agent.

- **Port**: 5003
- **Seed**: `khasdljghfgfd`
- **Endpoint**: `http://localhost:5003/submit`

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/insurance-quote-processing.git
    cd insurance-quote-processing
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set OpenAI API Key**:
    Replace the placeholder `###` in the code with your actual OpenAI API key.

## Running the Agents

To run the agents, execute the following commands in separate terminal windows:

1. **Start the Parser agent**:
    ```bash
    python agent2.py
    ```

2. **Start the Rules agent**:
    ```bash
    python agent3.py
    ```

3. **Start the Premium agent**:
    ```bash
    python agent4.py
    ```

## Usage

1. **Parser Agent**:
    - Parses the text from insurance documents and generates a mapping file.
    - Sends the mapped fields to the Rules agent for further processing.

2. **Rules Agent**:
    - Receives the mapped fields from the Parser agent.
    - Generates condition statements and converts them into if-else statements.
    - Sends the if-else statements to the Premium agent for evaluation.

3. **Premium Agent**:
    - Receives the if-else statements from the Rules agent.
    - Applies the conditions to a predefined dataset to generate insurance quotes.
    - Sends the final insurance quotes back to the Parser agent.

## Configuration

- **Agent Addresses**: Ensure the addresses in the code match the actual addresses of your agents.
- **OpenAI API Key**: Replace the placeholder `###` in the code with your actual OpenAI API key.

## Example

Below is an example of how to interact with the agents:

1. **Send a document to the Parser agent**:
    ```python
    import requests
    from uagents import Model

    class Message(Model):
        message: str

    response = requests.post(
        'http://localhost:5001/submit',
        json=Message(message='path_to_document.docx').dict()
    )
    print(response.json())
    ```

2. **Parser agent processes the document and sends mapped fields to the Rules agent**.

3. **Rules agent generates if-else statements and sends them to the Premium agent**.

4. **Premium agent evaluates the conditions and sends the final quote back to the Parser agent**.

## Contributing

Contributions are welcome! Please create an issue or submit a pull request for any improvements or new features.
