from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np

app2 = Flask(__name__)  # Agora o app se chama 'app2'

# Cria o leitor EasyOCR (Português)
reader = easyocr.Reader(['pt'])

# Endpoint para acordar o servidor (ping)
@app2.route('/ping', methods=['GET'])
def ping():
    return 'pong', 200

# Endpoint principal para OCR
@app2.route('/ocr', methods=['POST'])
def ocr_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado!'}), 400

    file = request.files['file']
    in_memory_file = file.read()
    npimg = np.frombuffer(in_memory_file, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Faz OCR na imagem
    resultados = reader.readtext(image)

    # Extrai apenas o texto (sem coordenadas ou confiança)
    textos_detectados = [texto for (_, texto, _) in resultados]

    # Junta os textos em uma única string separada por quebras de linha
    texto_final = "\n".join(textos_detectados)

    return jsonify({'texto_extraido': texto_final})
