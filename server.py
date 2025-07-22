from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

BASE_CONTEXT = """
Respondé solo como un asistente del juego 'Ecos de Xoria'.
Este juego es un RPG medieval con encantamientos de armas, monstruos, bosses y ciudades.
Hay 4 niveles de encantamientos: Común (blanco), Verde, Azul, Morado y Dorado.
Las armas tier 3 tienen efectos únicos como Toxified (veneno), Hurricane (velocidad), Cursed (robo de vida y objetos).
Los jugadores pueden explorar zonas como Bosque Oscuro, Ciudad nevada, Templo Ruinoso.
Respondé con datos del juego y no inventes nada fuera de este mundo.
"""

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    prompt = BASE_CONTEXT + "\nPregunta del jugador: " + question + "\nRespuesta del asistente:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": BASE_CONTEXT},
            {"role": "user", "content": question}
        ],
        temperature=0.7
    )

    answer = response.choices[0].message["content"]
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)