# Author: Richard Sun

import io
import os
import sys
import torch
import librosa
import numpy as np
import logging
from typing import Dict, List, Generator, Optional

from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav
from cosyvoice.utils.common import set_all_random_seed

from . import config

# 确保Matcha-TTS可以导入
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'third_party/Matcha-TTS'))

try:
    import matcha
    logging.info("Matcha-TTS module found")
except ImportError:
    logging.error("Matcha-TTS module not found")
    sys.exit(1)

# 设置日志
# logging.basicConfig(level=logging.DEBUG)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def postprocess(speech, top_db=config.TOP_DB, hop_length=config.HOP_LENGTH, win_length=config.WIN_LENGTH):
    """处理生成的语音信号"""
    speech, _ = librosa.effects.trim(speech, top_db=top_db, frame_length=win_length, hop_length=hop_length)
    if speech.abs().max() > config.MAX_VAL:
        speech = speech / speech.abs().max() * config.MAX_VAL
    speech = torch.concat([speech, torch.zeros(1, int(24000 * 0.2))], dim=1)  # 添加0.2秒的静音
    return speech

def get_available_voices() -> List[Dict[str, str]]:
    """扫描prompts目录，返回所有可用的声音列表"""
    voices = []
    for filename in os.listdir(config.PROMPTS_DIR):
        if filename.endswith('.wav'):
            voice_name = os.path.splitext(filename)[0]
            # 检查对应的文本文件是否存在
            if os.path.exists(os.path.join(config.PROMPTS_DIR, f"{voice_name}.txt")):
                voices.append({
                    "id": voice_name,
                    "name": voice_name
                })
    
    # 如果没有找到任何声音，检查旧版路径
    if not voices and os.path.exists(config.LEGACY_PROMPT_VOICE) and os.path.exists(config.LEGACY_PROMPT_TEXT_FILE):
        voices.append({
            "id": "default",
            "name": "默认声音"
        })
    
    return voices

def get_voice_path(voice_id: str) -> Dict[str, str]:
    """获取指定声音的路径信息"""
    # 检查是否是旧版默认声音
    if voice_id == "default" and os.path.exists(config.LEGACY_PROMPT_VOICE):
        return {
            "wav_path": config.LEGACY_PROMPT_VOICE,
            "txt_path": config.LEGACY_PROMPT_TEXT_FILE
        }
    
    # 新版声音路径
    wav_path = os.path.join(config.PROMPTS_DIR, f"{voice_id}.wav")
    txt_path = os.path.join(config.PROMPTS_DIR, f"{voice_id}.txt")
    
    if not os.path.exists(wav_path) or not os.path.exists(txt_path):
        raise ValueError(f"声音 '{voice_id}' 的提示文件不完整")
    
    return {
        "wav_path": wav_path,
        "txt_path": txt_path
    }

class TTSService:
    def __init__(self):
        # 初始化模型
        try:
            self.model = CosyVoice2(config.MODEL_PATH, load_jit=config.LOAD_JIT)
            self.sample_rate = self.model.sample_rate
            logger.info("CosyVoice2 模型加载成功")
        except Exception as e:
            logger.error(f"加载CosyVoice2失败: {str(e)}")
            raise
    
    def get_prompt_text(self, voice_id: str) -> str:
        """获取提示文本"""
        voice_paths = get_voice_path(voice_id)
        with open(voice_paths["txt_path"], 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def get_prompt_speech(self, voice_id: str) -> torch.Tensor:
        """获取提示语音"""
        voice_paths = get_voice_path(voice_id)
        return postprocess(load_wav(voice_paths["wav_path"], config.PROMPT_SR))
    
    def generate_speech(self, 
                        text: str, 
                        voice_id: Optional[str] = None, 
                        stream: bool = True, 
                        seed: int = 42, 
                        speed: float = 1.0) -> Generator:
        """生成语音"""
        if not voice_id:
            # 尝试使用默认声音，如果没有可用声音则使用第一个
            available_voices = get_available_voices()
            if available_voices:
                voice_id = available_voices[0]["id"]
            else:
                raise ValueError("没有可用的声音模型")
        
        try:
            prompt_text = self.get_prompt_text(voice_id)
            prompt_speech_16k = self.get_prompt_speech(voice_id)
            
            set_all_random_seed(seed)
            
            logger.debug(f"开始zero-shot推理，文本: {text}, 声音: {voice_id}")
            
            return self.model.inference_zero_shot(
                tts_text=text,
                prompt_text=prompt_text,
                prompt_speech_16k=prompt_speech_16k,
                stream=stream,
                speed=speed
            )
        except Exception as e:
            logger.error(f"语音生成失败: {str(e)}")
            raise