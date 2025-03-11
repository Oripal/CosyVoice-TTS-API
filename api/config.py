# Author: Richard Sun

import os

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
AUDIO_OUTPUT_DIR = os.path.join(BASE_DIR, "audio")

# 确保目录存在
os.makedirs(PROMPTS_DIR, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

# 服务器配置
HOST = "0.0.0.0"
PORT = 3005

# 音频处理参数
MAX_VAL = 0.8
PROMPT_SR = 16000
DEFAULT_VOICE = "李达康"  # 默认声音

# 模型路径
MODEL_PATH = "pretrained_models/CosyVoice2-0.5B"
LOAD_JIT = True

# 后处理参数
TOP_DB = 60
HOP_LENGTH = 220
WIN_LENGTH = 440

# API密钥配置
API_KEYS = ["your-existing-keys", "cosyvoice-api-demo"]

# 不需要API密钥验证的路径
NO_AUTH_PATHS = ["/docs", "/redoc", "/openapi.json", "/health", "/"]

# 是否启用API认证（默认启用）
ENABLE_API_AUTH = os.environ.get("ENABLE_API_AUTH", "True").lower() in ("true", "1", "yes")


# 添加允许所有源的CORS配置
CORS_ORIGINS = ["*"]  # 或更严格地：["http://localhost:8000"]
