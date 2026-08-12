# AI 代码助手

一个网页版的「AI 代码助手」：用自然语言生成代码，也能解释/审查已有代码、为代码自动生成测试用例。属于 **AI Coding** 方向的个人实践项目，体现「在调用大模型 API 之上，自己实现业务逻辑层（需求解析、代码审查、测试设计）并做成可演示产品」的能力。

## 功能

- **三种功能模式**（页面顶部切换）：
  - **代码生成**：自然语言 → 代码，支持多语言
  - **代码解释 / 审查**：粘贴代码，返回功能说明、潜在问题与优化建议
  - **测试用例生成**：粘贴代码，返回覆盖正常 / 边界 / 异常的单元测试用例
- 支持多语言（Python / JavaScript / Java / C++ / HTML-CSS / SQL）
- 生成结果带一键复制
- 大模型密钥通过环境变量或本地 `key.local` 文件注入，不写死在代码中
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
├── app.py            # Flask 后端：提供页面 + /api/generate 接口（支持三种 mode）
├── index.html        # 前端页面：模式切换、输入、展示与复制
├── requirements.txt  # 依赖
├── Procfile          # Render 部署用
├── .gitignore        # 忽略 key.local / __pycache__
├── key.local         # 本地密钥（不进仓库，自行创建）
└── README.md
```

## 说明

- 密钥从环境变量或本地 `key.local` 文件读取，请勿将 `key.local` 提交到代码仓库。
- 项目仅处理编程相关请求；非编程问题会被模型礼貌拒绝。
- 当前为本地运行版本；如需公开访问，可用 Render 等平台部署（已提供 Procfile）。
