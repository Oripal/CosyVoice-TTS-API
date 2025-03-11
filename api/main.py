import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.routing import APIRoute


from . import config
from .service import TTSService, get_available_voices

# 创建自定义路由类来处理OPTIONS请求
class CORSRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()
        
        async def custom_route_handler(request: Request):
            if request.method == "OPTIONS":
                return JSONResponse(
                    status_code=200,
                    content={"message": "OK"},
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "*",
                        "Access-Control-Allow-Headers": "*",
                    },
                )
            return await original_route_handler(request)
            
        return custom_route_handler

# 初始化FastAPI应用
app = FastAPI(
    title="CosyVoice API", 
    description="CosyVoice文本转语音API",
    version="1.0.0",
    route_class=CORSRoute,  # 使用自定义路由类
)

# 添加CORS中间件（放在最高优先级）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 初始化TTS服务
tts_service = TTSService()

# 数据模型
class TTSRequest(BaseModel):
    text: str = Field(..., description="需要转换为语音的文本")
    voice_id: Optional[str] = Field(None, description="声音ID，不指定时使用默认声音")
    seed: Optional[int] = Field(42, description="随机种子，影响生成的语音特征")
    stream: bool = Field(True, description="是否使用流式输出")
    speed: Optional[float] = Field(1.0, ge=0.5, le=2.0, description="语速，范围0.5-2.0")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "你好，这是一段测试语音",
                "voice_id": "李达康",
                "seed": 42,
                "stream": True,
                "speed": 1.0
            }
        }

class VoiceInfo(BaseModel):
    id: str
    name: str

# 添加专用OPTIONS处理器，确保CORS预检请求能成功
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
    )

# API路由
@app.get("/")
async def root():
    """API根路径"""
    return {"status": "ok", "message": "CosyVoice TTS API正在运行"}

@app.get("/api/voices", response_model=List[VoiceInfo])
async def list_voices():
    """获取所有可用声音列表"""
    voices = get_available_voices()
    return voices

@app.post("/api/tts")
async def generate_tts(request: TTSRequest):
    """文本转语音"""
    if not request.text:
        raise HTTPException(status_code=400, detail="文本不能为空")
    
    headers = {
        "Content-Type": "audio/pcm",
        "X-Sample-Rate": "24000",
        "X-Channel-Count": "1"
    }
    
    async def generate():
        try:
            generator = tts_service.generate_speech(
                text=request.text,
                voice_id=request.voice_id,
                stream=request.stream,
                seed=request.seed,
                speed=request.speed
            )
            
            for i, out in enumerate(generator):
                raw = (out['tts_speech'].numpy() * 32767).astype(np.int16).flatten()
                yield raw.tobytes()
        except ValueError as e:
            # 处理已知错误类型
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # 处理其他错误
            raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")
    
    return StreamingResponse(generate(), media_type="audio/pcm", headers=headers)

# 为了向后兼容，保留原始路径
@app.post("/cosyvoice")
async def cosyvoice_compat(request: TTSRequest):
    """向后兼容原始API"""
    return await generate_tts(request)

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "version": "1.0.0"}

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    # 允许所有OPTIONS请求通过（CORS预检请求）
    if request.method == "OPTIONS":
        return await call_next(request)
        
    # 检查路径是否需要验证
    if request.url.path in config.NO_AUTH_PATHS or any(
        request.url.path.startswith(f"{path}/") for path in config.NO_AUTH_PATHS if path != "/"
    ):
        return await call_next(request)
    
    # 获取API密钥
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "未提供API密钥"}
        )
    
    # 验证API密钥
    if api_key not in config.API_KEYS:
        return JSONResponse(
            status_code=401,
            content={"detail": "无效的API密钥"}
        )
    
    # 继续处理请求
    return await call_next(request)

# 启动服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("api.main:app", host=config.HOST, port=config.PORT, reload=True)