import os
from flask import Flask
import requests
import time

app = Flask(__name__)

# 환경 변수에서 Hugging Face API 토큰 읽기
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not API_TOKEN:
    raise ValueError("HUGGINGFACE_API_TOKEN 환경 변수가 설정되지 않았습니다.")

# Hugging Face API 설정
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 50, "num_return_sequences": 1}
    }
    for _ in range(3):  # 최대 3번 재시도
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
            result = response.json()
            # API 응답이 리스트인지 확인
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result
            elif isinstance(result, dict) and "error" in result:
                if "loading" in result["error"].lower():
                    time.sleep(5)  # 모델 로딩 대기
                    continue
                return {"error": result["error"]}
            return {"error": "Unexpected response format"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    return {"error": "Model loading timeout after retries"}

@app.route('/conversation')
def conversation():
    # AI 대화 예시
    prompt = "안녕, 오늘의 주제를 정하자."
    ai1_response = query_huggingface(prompt)
    
    if "error" in ai1_response:
        ai1_text = f"AI1 응답 실패: {ai1_response['error']}"
    else:
        ai1_text = ai1_response[0]["generated_text"]

    prompt = f"{ai1_text} AI2: 좋아, 어떤 주제로 할까?"
    ai2_response = query_huggingface(prompt)
    
    if "error" in ai2_response:
        ai2_text = f"AI2 응답 실패: {ai2_response['error']}"
    else:
        ai2_text = ai2_response[0]["generated_text"]

    return f"AI1: {ai1_text}<br>AI2: {ai2_text}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)