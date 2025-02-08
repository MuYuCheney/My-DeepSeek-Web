from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio
from fastapi.responses import StreamingResponse

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(message: ChatMessage):
    # 这里实现你的聊天逻辑
    return {"response": f"你说的是: {message.message}"}

@app.get("/api/chat/stream")
async def chat(prompt: str = "什么是深度学习", model_tag: str = "openai"):
    """聊天接口 - EventSource"""
    request = ChatRequest(
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=True,
        model_tag=model_tag
    )

    async def generate():
        try:
            # 立即发送一个初始化消息，启动流
            yield b"data: {}\n\n"
            
            # 不要等待所有 token 生成完，立即开始发送
            async for chunk in chat_service.generate_stream_response(request):
                if chunk.done:
                    yield b"data: [DONE]\n\n"
                    break
                else:
                    # 每个 token 生成后立即发送，不等待下一个
                    data = json.dumps({"content": chunk.content}, ensure_ascii=False)
                    yield f"data: {data}\n\n".encode('utf-8')
                    # 强制刷新缓冲区
                    await asyncio.sleep(0)

        except Exception as e:
            print(f"Error: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n".encode('utf-8')

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Transfer-Encoding": "chunked"  # 添加分块传输编码
        }
    ) 