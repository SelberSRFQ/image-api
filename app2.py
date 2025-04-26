import os
from flask import Flask, request, jsonify
import cv2
import pytesseract
import numpy as np

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong', 200

@app.route('/ocr', methods=['POST'])
def ocr_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado!'}), 400

        file = request.files['file']
        in_memory_file = file.read()
        npimg = np.frombuffer(in_memory_file, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({'error': 'Arquivo inválido ou formato não suportado!'}), 400

        texto = pytesseract.image_to_string(image, lang='por')

        return jsonify({'texto_extraido': texto})
    
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

