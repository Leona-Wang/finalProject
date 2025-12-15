from flask import Flask, render_template, request, jsonify
import os
import aisuite as ai
import json

api_key = "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"
os.environ['GROQ_API_KEY'] = api_key

model = "groq:openai/gpt-oss-120b"
client = ai.Client()

with open("persona.json", "r", encoding="utf-8") as f:
    persona = json.load(f)

system_prompt = f"""
你是 Leona 的個人化 AI 聊天助理。
以下是你的個人設定：
{json.dumps(persona, ensure_ascii=False, indent=2)}
請回答要像 Leona 本人會說的話，
親切、自然、有台灣口吻。
"""

chat_history = []

app = Flask(__name__)


def chat_with_persona(user_input):
    global chat_history

    final_prompt = f"使用者問題：{user_input}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": final_prompt
            },
        ]
    )

    answer = response.choices[0].message.content
    chat_history.append((user_input, answer))
    return answer


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    userMessage = request.json.get("message")
    try:
        reply = chat_with_persona(userMessage)
    except Exception as e:
        print("LLM error:", str(e))
        reply = "模型暫時無法回應，請稍後再試"
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
