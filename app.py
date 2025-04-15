from flask import Flask, request, jsonify
from flask_cors import CORS
from translatepy import Translator
import requests

app = Flask(__name__)
CORS(app)

translator = Translator()

@app.route("/traduzir", methods=["POST"])
def traduzir():
    data = request.get_json()
    texto = data.get("texto", "")
    idioma = data.get("idioma", "en")  # padrão: inglês

    if not texto.strip():
        return jsonify({"error": "Texto vazio."}), 400

    linhas = texto.split("\n")
    traducoes = []

    for linha in linhas:
        if linha.strip() == "":
            traducoes.append("")
            continue

        try:
            traducao = translator.translate(linha, idioma)
            traducoes.append(traducao.result)
        except Exception as e:
            traducoes.append(f"[Erro: {str(e)}]")

    return jsonify({
        "original": linhas,
        "traduzido": traducoes
    })

@app.route("/corrigir", methods=["POST"])
def corrigir_texto():
    data = request.get_json()
    texto = data.get("texto", "")

    if not texto.strip():
        return jsonify({"erro": "Texto vazio"}), 400

    response = requests.post(
        "https://api.languagetool.org/v2/check",
        data={
            "text": texto,
            "language": "pt-BR"
        }
    )

    if response.status_code != 200:
        return jsonify({"erro": "Erro ao se conectar ao LanguageTool"}), 500

    resultado = response.json()
    texto_corrigido = texto
    offset_correction = 0

    for match in sorted(resultado["matches"], key=lambda x: x["offset"]):
        if "replacements" in match and match["replacements"]:
            start = match["offset"] + offset_correction
            end = start + match["length"]
            replacement = match["replacements"][0]["value"]
            texto_corrigido = (
                texto_corrigido[:start] +
                replacement +
                texto_corrigido[end:]
            )
            offset_correction += len(replacement) - match["length"]

    return jsonify({"corrigido": texto_corrigido})

if __name__ == "__main__":
    app.run(debug=True)
