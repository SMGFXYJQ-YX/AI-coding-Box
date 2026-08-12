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

# 三种功能的 system prompt：决定"模型之上你加的逻辑层"
SYSTEM_PROMPTS = {
    "code": (
        "你是一个专业的编程助手。用户会用自然语言描述需求，"
        "你需要生成对应编程语言的代码，并给出简短必要的说明。"
        "代码请用 markdown 代码块包裹（注明语言），说明尽量简洁。"
        "如果用户的问题与编程无关，请礼貌说明你只处理编程相关请求。"
    ),
    "explain": (
        "你是一个资深代码审查员。用户会粘贴一段代码，"
        "你需要：1）用简洁中文说明这段代码的功能与执行流程；"
        "2）指出潜在的 bug、边界问题或安全隐患；"
        "3）给出具体可操作的优化建议。"
        "请使用 markdown 代码块包裹任何代码片段，说明保持简洁有条理。"
    ),
    "testcase": (
        "你是一个测试工程师。用户会给出一段代码或需求描述，"
        "你需要为它设计单元测试用例：覆盖正常路径、边界条件、异常输入，"
        "并尽量给出可直接运行的测试代码（使用对应语言的常见测试框架，如 Python 的 pytest）。"
        "请用 markdown 代码块包裹测试代码，并简要说明每个用例的意图。"
    ),
}


def build_messages(mode, language, user_input):
    """根据功能模式构造发给大模型的消息。这是"你自己的逻辑层"。"""
    if mode == "explain":
        return [
            {"role": "system", "content": SYSTEM_PROMPTS["explain"]},
            {"role": "user", "content": f"以下是 {language} 代码，请解释并审查：\n\n```{language}\n{user_input}\n```"},
        ]
    if mode == "testcase":
        return [
            {"role": "system", "content": SYSTEM_PROMPTS["testcase"]},
            {"role": "user", "content": f"请为以下 {language} 代码/需求设计测试用例：\n\n```{language}\n{user_input}\n```"},
        ]
    # 默认 code
    return [
        {"role": "system", "content": SYSTEM_PROMPTS["code"]},
        {"role": "user", "content": f"请使用 {language} 实现以下需求：{user_input}"},
    ]


@app.route("/")
def index():
    # 同目录提供前端页面，避免跨域问题
    return send_from_directory(".", "index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    api_key = API_KEY
    if not api_key:
        return jsonify({
            "error": "未配置 SILICONFLOW_API_KEY 环境变量，请在运行前设置后再试。"
        }), 400

    data = request.get_json(silent=True) or {}
    user_input = (data.get("prompt") or "").strip()
    language = (data.get("language") or "Python").strip()
    mode = (data.get("mode") or "code").strip()
    if mode not in SYSTEM_PROMPTS:
        mode = "code"
    if not user_input:
        return jsonify({"error": "请输入内容。"}), 400

    messages = build_messages(mode, language, user_input)

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
