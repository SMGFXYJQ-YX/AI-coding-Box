# AI 代码助手

一个网页版的「AI 代码助手」：用自然语言描述需求，调用 Qwen 大模型生成对应编程语言的代码。属于 **AI Coding** 方向的个人实践项目，体现「用 AI 辅助编程并做成可演示产品」的能力。
可以用其它模型的key替代， Qwen 模型真的不太行

## 功能

- 支持多语言（Python / JavaScript / Java / C++ / HTML-CSS / SQL）
- 自然语言 → 代码生成，结果带一键复制
- 大模型密钥通过环境变量注入，不写死在代码中
- 后端统一提供前端页面，避免跨域问题

## 技术栈

- 后端：Python + Flask + requests
- 前端：HTML + CSS + JavaScript（原生，无框架）
- 模型：SiliconFlow 平台的 Qwen/Qwen2.5-7B-Instruct

## 运行方式

1. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

2. 设置 API 密钥（从 SiliconFlow 控制台获取）：

   - Windows（PowerShell）：
     ```powershell
     $env:SILICONFLOW_API_KEY="你的密钥"
     ```
   - Linux / macOS：
     ```bash
     export SILICONFLOW_API_KEY="你的密钥"
     ```

3. 启动服务：

   ```bash
   python app.py
   ```

4. 浏览器打开 `http://localhost:5001/`，输入需求即可生成代码。

## 项目结构

```
AI代码助手/
├── app.py            # Flask 后端：提供页面 + /api/generate 接口
├── index.html        # 前端页面：输入需求、展示与复制代码
├── requirements.txt  # 依赖
└── README.md
```

## 说明

- 密钥仅从环境变量读取，请勿将其提交到代码仓库。
- 项目仅处理编程相关请求；非编程问题会被模型礼貌拒绝。
