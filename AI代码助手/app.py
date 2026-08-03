import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# 密钥优先从环境变量读取；本地演示时可放 key.local 文件（已 gitignore，不进仓库）
API_KEY = os.environ.get("SILICONFLOW_API_KEY")
if not API_KEY:
    _key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "key.local")
    if os.path.exists(_key_file):
        with open(_key_file, "r", encoding="utf-8") as _f:
            API_KEY = _f.read().strip()

# SiliconFlow 大模型接口（与 AI 测试项目同一家，复用 Qwen 模型）
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL = "Qwen/Qwen2.5-7B-Instruct"

SYSTEM_PROMPT = (
    "你是一个专业的编程助手。用户会用自然语言描述需求，"
    "你需要生成对应编程语言的代码，并给出简短必要的说明。"
    "代码请用 markdown 代码块包裹（注明语言），说明尽量简洁。"
    "如果用户的问题与编程无关，请礼貌说明你只处理编程相关请求。"
)


@app.route("/")
def index():
    # 同目录提供前端页面，避免跨域问题
    return send_from_directory(".", "index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    # 密钥优先环境变量，其次本地 key.local 文件（安全，不落代码）
    api_key = API_KEY
    if not api_key:
        return jsonify({
            "error": "未配置 SILICONFLOW_API_KEY 环境变量，请在运行前设置后再试。"
        }), 400

    data = request.get_json(silent=True) or {}
    user_prompt = (data.get("prompt") or "").strip()
    language = (data.get("language") or "Python").strip()
    if not user_prompt:
        return jsonify({"error": "请输入需求描述。"}), 400

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"请使用 {language} 实现以下需求：{user_prompt}"},
    ]

    try:
        resp = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 2048,
            },
            timeout=120,
        )
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"]
        return jsonify({"result": content})
    except requests.exceptions.Timeout:
        return jsonify({"error": "请求超时，请稍后重试。"}), 504
    except Exception as e:
        return jsonify({"error": f"调用模型失败：{e}"}), 500


if __name__ == "__main__":
    # 云平台（如 Render）通过环境变量 PORT 指定端口，本地默认 5001（避开沙箱 5000 幽灵端口）
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
