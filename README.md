# My-DeepSeek 智能对话助手

一个基于 Vue 3 + FastAPI 的智能对话助手，支持深度思考、联网搜索等功能。

## 环境要求

- Node.js 16+ 
- Python 3.8+
- npm 或 yarn

## 快速开始

### 1. 克隆项目

```bash
git clone <你的项目地址>
cd AutoGenProjectWeb
```

### 2. 前端设置

安装依赖：
```bash
npm install
# 或
yarn install
```

启动开发服务器：
```bash
npm run dev
# 或
yarn dev
```

### 3. 后端设置

创建虚拟环境（推荐）：
```bash
python -m venv venv

# Windows激活虚拟环境
.\venv\Scripts\activate

# Linux/Mac激活虚拟环境
source venv/bin/activate
```

安装依赖：
```bash
pip install fastapi uvicorn python-dotenv
```

启动后端服务器：
```bash
python main.py
```

### 4. 访问应用

打开浏览器访问：`http://localhost:3000`

## 项目结构

```
my-vue-app/
├── src/                # 前端源代码
│   ├── api/           # API 请求
│   ├── views/         # 页面组件
│   └── router/        # 路由配置
├── main.py            # 后端入口
└── README.md          # 项目说明
```

## 功能特性

- 💬 智能对话
- 🤔 深度思考模式
- 🌐 联网搜索能力
- 📝 Markdown 支持
- 📜 聊天历史记录
- 🎨 现代化 UI 界面

## 常见问题

1. 如果遇到 "端口被占用" 错误：
   - 前端：修改 `vite.config.ts` 中的端口号
   - 后端：修改 `main.py` 中的端口号

2. 如果后端连接失败：
   - 确保后端服务器正在运行
   - 检查 `src/api/index.ts` 中的 API 地址配置

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

[MIT License](LICENSE) 