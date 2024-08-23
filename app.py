from flask import Flask, request, jsonify, send_from_directory
import together
import argparse 

app = Flask(__name__)

# Add named commandline arg for together API key
parser = argparse.ArgumentParser()
parser.add_argument("--together_api_key", help="Together AI API key")
args = parser.parse_args()

# Replace with your Together AI API key
together.api_key = args.together_api_key

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get_suggestion', methods=['POST'])
def get_suggestion():
    data = request.json
    text = data['text']
    print("Suggestion:", text)
    # Call Together AI API for text completion
    response = together.Complete.create(
        prompt=f"{text}",
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        max_tokens=50,
        temperature=0.3,
        repetition_penalty=1
    )
    print(response) 
    suggestion = response['choices'][0]['text'].strip()

    return jsonify({'suggestion': suggestion})

if __name__ == '__main__':
    app.run(debug=True)