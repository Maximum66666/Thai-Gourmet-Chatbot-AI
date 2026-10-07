import os
import json
import base64
import requests
from flask import Flask, render_template, request, jsonify
from health_checker import analyze_health_warnings

app = Flask(__name__)
# Limit upload size to 2 MB as specified by API docs
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

API_URL = "https://api.aiforthai.in.th/thaifood"
DEFAULT_API_KEY = os.environ.get("AIFORTHAI_API_KEY", "PVNKXPuEyOEnoIWTctJs6czMeqZ3sYqB")

# ThaiLLM Chatbot Configuration
THAILLM_API_URL = "http://thaillm.or.th/api/v1/chat/completions"
DEFAULT_THAILLM_API_KEY = os.environ.get("THAILLM_API_KEY", "hbyF************************fHd6")
DEFAULT_THAILLM_MODEL = "pathumma-thaillm-qwen3-8b-think-3.0.0"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'กรุณาเลือกไฟล์ภาพ'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'ไม่ได้เลือกไฟล์ภาพ'}), 400

    api_key = request.form.get('api_key', '').strip() or DEFAULT_API_KEY
    
    # Retrieve allergies and health restrictions from user
    allergies_raw = request.form.get('allergies', '[]')
    conditions_raw = request.form.get('health_conditions', '[]')
    custom_restrictions = request.form.get('custom_restrictions', '').strip()

    try:
        allergies = json.loads(allergies_raw) if allergies_raw else []
        conditions = json.loads(conditions_raw) if conditions_raw else []
    except Exception:
        allergies = []
        conditions = []

    try:
        image_bytes = file.read()
        
        # Check size (<= 2MB)
        if len(image_bytes) > 2 * 1024 * 1024:
            return jsonify({'success': False, 'error': 'ขนาดไฟล์ภาพเกิน 2 MB'}), 400

        # Encode to Base64
        b64_str = base64.b64encode(image_bytes).decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'Apikey': api_key
        }
        payload = {
            'file': b64_str
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)

        if response.status_code != 200:
            return jsonify({
                'success': False, 
                'error': f'API ตอบกลับข้อผิดพลาด (Status Code: {response.status_code}): {response.text}'
            }), 502

        res_data = response.json()

        # Perform health and allergy safety check on the top predicted foods
        health_warnings = []
        objects = res_data.get('objects', [])
        if objects:
            top_food_name = objects[0].get('result', '')
            health_warnings = analyze_health_warnings(
                food_name=top_food_name,
                selected_allergies=allergies,
                selected_health_conditions=conditions,
                custom_restrictions=custom_restrictions
            )

        return jsonify({
            'success': True, 
            'data': res_data,
            'health_warnings': health_warnings,
            'user_profile': {
                'allergies': allergies,
                'health_conditions': conditions,
                'custom_restrictions': custom_restrictions
            }
        })

    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'error': 'การเชื่อมต่อไปยัง API หมดเวลา (Timeout)'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'เกิดข้อผิดพลาดในการเชื่อมต่อเครือข่าย: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'เกิดข้อผิดพลาด: {str(e)}'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get('messages', [])
    if not messages or not isinstance(messages, list):
        return jsonify({'success': False, 'error': 'กรุณาระบุข้อความสนทนา (messages)'}), 400

    api_key = data.get('api_key', '').strip() or DEFAULT_THAILLM_API_KEY
    model = data.get('model', '').strip() or DEFAULT_THAILLM_MODEL
    try:
        temperature = float(data.get('temperature', 0.3))
    except (ValueError, TypeError):
        temperature = 0.3
    try:
        max_tokens = int(data.get('max_tokens', 2048))
    except (ValueError, TypeError):
        max_tokens = 2048

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {
        'model': model,
        'messages': messages,
        'max_tokens': max_tokens,
        'temperature': temperature
    }

    try:
        response = requests.post(THAILLM_API_URL, headers=headers, json=payload, timeout=90)

        if response.status_code == 401:
            return jsonify({
                'success': False,
                'error': 'การยืนยันตัวตนล้มเหลว (401 Unauthorized): กรุณาตรวจสอบและกรอก ThaiLLM Bearer Token (API Key) ที่ถูกต้องในการตั้งค่า'
            }), 401

        if response.status_code != 200:
            return jsonify({
                'success': False,
                'error': f'ThaiLLM API แจ้งข้อผิดพลาด (Status {response.status_code}): {response.text}'
            }), response.status_code

        res_data = response.json()
        choices = res_data.get('choices', [])
        reply_content = ''
        if choices and 'message' in choices[0]:
            reply_content = choices[0]['message'].get('content', '')

        return jsonify({
            'success': True,
            'reply': reply_content,
            'raw': res_data
        })
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'error': 'การเชื่อมต่อไปยัง ThaiLLM API หมดเวลา (Timeout - เกิน 90 วินาที)'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'เกิดข้อผิดพลาดในการเชื่อมต่อเครือข่าย ThaiLLM: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'เกิดข้อผิดพลาด: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
