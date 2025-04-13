import os
from flask import Flask
import requests

app = Flask(__name__)

# 환경 변수에서 Hugging Face API 토큰 읽기
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not API_TOKEN:
    raise ValueError("HUGGINGFACE_API_TOKEN 환경 변수가 설정되지 않았습니다.")

# Hugging Face API 설정
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # 예시 모델
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 50, "num_return_sequences": 1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route('/conversation')
def conversation():
    # AI 대화 예시
    prompt = "안녕, 오늘의 주제를 정하자."
    ai1_response = query_huggingface(prompt)
    ai1_text = ai1_response[0]["generated_text"] if ai1_response else "AI1 응답 실패"
    
    prompt = f"{ai1_text} AI2: 좋아, 어떤 주제로 할까?"
    ai2_response = query_huggingface(prompt)
    ai2_text = ai2_response[0]["generated_text"] if ai2_response else "AI2 응답 실패"
    
    return f"AI1: {ai1_text}<br>AI2: {ai2_text}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)