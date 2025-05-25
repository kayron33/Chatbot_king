from flask import Flask, request, jsonify
import json
import difflib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Carrega o banco de perguntas e respostas
with open('dados.json', 'r', encoding='utf-8') as f:
    base_conhecimento = json.load(f)

# Mensagem inicial com perguntas frequentes
mensagem_inicial = (
    "Olá! Sou o assistente virtual da King Sites Work. "
    "Aqui estão algumas perguntas que você pode me fazer:\n"
    "- Quais formas de pagamento vocês aceitam?\n"
    "- Qual é o horário de atendimento?\n"
    "- Vocês criam sites profissionais?\n"
    "Digite sua pergunta abaixo:"
)

@app.route("/responder", methods=["POST"])
def responder():
    data = request.get_json()
    pergunta_usuario = data.get("pergunta", "").lower()

    # Verifica pergunta mais parecida
    perguntas_cadastradas = [item["pergunta"] for item in base_conhecimento]
    parecida = difflib.get_close_matches(pergunta_usuario, perguntas_cadastradas, n=1, cutoff=0.5)

    if parecida:
        for item in base_conhecimento:
            if item["pergunta"] == parecida[0]:
                return jsonify({"resposta": item["resposta"]})

    return jsonify({"resposta": "Desculpe, não entendi. Pode reformular sua pergunta?"})

@app.route("/mensagem_inicial", methods=["GET"])
def mensagem_inicial_route():
    return jsonify({"resposta": mensagem_inicial})

if __name__ == "__main__":
    app.run(debug=True)
