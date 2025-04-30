from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY", "SUA_CHAVE_GOOGLE")
CX = os.getenv("GOOGLE_CX", "SEU_CX_GOOGLE")


def buscar_no_google(pergunta):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={pergunta}&key={API_KEY}&cx={CX}"
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()
            if "items" in dados and len(dados["items"]) > 0:
                return dados["items"][0]["snippet"]
            else:
                return "Nenhuma resposta encontrada no Google."
        else:
            return f"Erro ao buscar: {resposta.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/perguntar", methods=["POST"])
def perguntar():
    try:
        data = request.get_json()
        if not data or "pergunta" not in data:
            return jsonify({"resposta": "Dados não recebidos corretamente."}), 400

        pergunta = data["pergunta"]
        if not pergunta:
            return jsonify({"resposta": "Por favor, insira uma pergunta."}), 400

        resposta = buscar_no_google(pergunta)
        return jsonify({"resposta": resposta})

    except Exception as e:
        return jsonify({"resposta": f"Erro ao processar a requisição: {str(e)}"}), 400


if __name__ == "__main__":
    app.run(debug=True)
