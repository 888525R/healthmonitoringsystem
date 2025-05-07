from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        conversation_history.append({"role": "user", "content": user_message})

        response = ollama.chat(model="llama3.2", messages=conversation_history)
        ai_reply = response['message']['content']

        conversation_history.append({"role": "assistant", "content": ai_reply})

        return jsonify({'reply': ai_reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/affirmation')
def affirmation():
    try:
        prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        return jsonify({'affirmation': response['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/meditation')
def meditation():
    try:
        prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        return jsonify({'meditation': response['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'Conversation history cleared'})

if __name__ == "__main__":
    app.run(debug=True)