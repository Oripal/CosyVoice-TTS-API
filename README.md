# CosyVoice TTS API

[中文](#cosyvoice-tts-api-中文) | [English](#cosyvoice-tts-api-english)

---

## CosyVoice TTS API (中文)

**CosyVoice TTS API** 是一个基于 [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) 开源项目的扩展，提供了文本转语音（Text-to-Speech）的 RESTful API 接口，支持多种声音选择、语速调整和随机种子控制，并通过流式音频输出实现高效的语音生成。本项目包括 FastAPI 后端服务和一个 HTML 前端测试页面，适用于测试和集成。

### 功能特性

- **后端 API**：
  - 获取可用声音列表 (`/api/voices`)。
  - 生成流式 PCM 音频 (`/api/tts`)，支持零样本语音复刻。
  - 支持动态添加声音（通过 `prompts/` 目录）。
  - API 密钥认证和 CORS 支持。
- **前端测试页面**：
  - 输入文本、选择声音、调整语速和随机种子。
  - 点击“随机”按钮生成随机种子。
  - 实时生成并播放语音。
- **音频格式**：
  - 输出：24 kHz 单声道 PCM。
  - 前端自动转换为 WAV 播放。

### 项目背景

本项目基于 [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) 开源项目开发，在其基础上扩展了 API 接口，增强了服务端功能和用户交互体验。CosyVoice 提供了强大的 TTS 模型支持，而 CosyVoice TTS API 则将其封装为易用的 Web 服务。

### 项目结构

```text
CosyVoice/
├── api/
│   ├── __init__.py       # 空文件，避免循环导入
│   ├── config.py        # 配置项（路径、密钥、服务器设置）
│   ├── main.py          # FastAPI 应用，定义 API 端点
│   ├── service.py       # TTS 服务逻辑，模型加载和语音生成
│   ├── prompts/         # 提示文件目录（例如 aaa.wav、aaa.txt）
│   └── audio/           # 音频输出目录（自动创建）
├── run-apy.py           # 启动脚本
├── test_config.py       # 测试配置脚本
├── CosyVoice-API-Test.html # 前端测试页面
└── README.md            # 项目说明文档
```



### 安装

#### 前置条件

- CosyVoice
- Git
- 浏览器（推荐 Chrome 或 Firefox）

#### 安装步骤

1. CosyVoice 依赖：需要从官方仓库安装:
   https://github.com/FunAudioLLM/CosyVoice.git

   确保 pretrained_models/CosyVoice2-0.5B 模型文件已下载并放置在项目根目录下的 pretrained_models/ 文件夹中。参考 [CosyVoice 安装指南](https://github.com/FunAudioLLM/CosyVoice#installation)。

   

2. 在CosyVoice主目录下

   ```bash
   pip install fastapi uvicorn torch librosa numpy pydantic
   git clone https://github.com/Oripal/CosyVoice-TTS-API.git
   ```

   

3. 准备提示文件：

   - 在 api/prompts/ 目录下添加声音文件对，例如：

     ```text
     api/prompts/
     ├── aaaaa.wav
     ├── aaaaa.txt
     ├── bbbbb.wav
     ├── bbbbb.txt
     ```

#### 使用方法

启动后端服务

1. 运行服务：

   ```bash
   python run.py
   ```

   - 默认监听 http://0.0.0.0:3005。

2. 验证服务：

   - 打开浏览器，访问 CosyVoice-API-Test.html。

   - 使用 curl 测试：

     ```bash
     curl http://localhost:3005/api/voices
     curl -X POST "http://localhost:3005/api/tts" -H "X-API-Key: cosyvoice-api-demo" -H "Content-Type: application/json" -d '{"text": "Hello World", "voice_id": "aaaaa"}' > output.pcm
     ```



#### API 端点

- GET /api/voices

  - 返回可用声音列表。

  - 示例响应：

    json

    ```json
    [{"id": "aaaaa", "name": "aaaaa"}, {"id": "bbbbb", "name": "bbbbb"}]
    ```

- POST /api/tts

  - 请求体：

    ```json
    {
      "text": "你好，这是一段测试语音",
      "voice_id": "aaaaa",
      "seed": 42 Leaderboard,
      "speed": 1.0,
      "stream": true
    }
    ```

  - 响应：PCM 音频流（24 kHz，单声道）。

### 配置

- 环境变量：
  - COSYVOICE_API_KEY：自定义 API 密钥。
  - COSYVOICE_HOST 和 COSYVOICE_PORT：服务器地址和端口。
- 修改 api/config.py：
  - 更新 API_KEYS、MODEL_PATH 或 PROMPTS_DIR。

### 贡献

欢迎为 CosyVoice TTS API 贡献代码！请遵循以下步骤：

1. Fork 仓库。

2. 创建新分支：

   ```bash
   git checkout -b feature/your-feature
   ```

3. 提交更改：

   ```bash
   git commit -m "Add your feature"
   ```

4. 推送并创建 Pull Request：

   ```bash
   git push origin feature/your-feature
   ```

### 许可

本项目遵循 [CosyVoice 的许可](https://github.com/FunAudioLLM/CosyVoice/blob/main/LICENSE)（Apache 2.0）。扩展部分的代码采用 MIT 许可证 (LICENSE)。

### 致谢

- 感谢 [FunAudioLLM](https://github.com/FunAudioLLM) 提供的 [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) 项目和模型支持。
- 感谢所有参与调试和测试的贡献者！



## CosyVoice TTS API (English)

CosyVoice TTS API (English)

CosyVoice TTS API is an extension of the [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) open-source project, providing a RESTful API interface for Text-to-Speech (TTS). It supports multiple voice options, speed adjustment, and random seed control, delivering efficient speech generation via streaming audio output. The project includes a FastAPI backend service and an HTML frontend testing page, suitable for testing and integration.

### Features

- Backend API:
  - Retrieve available voices (/api/voices).
  - Generate streaming PCM audio (/api/tts), supporting zero-shot voice cloning.
  - Dynamically add voices (via the prompts/ directory).
  - API key authentication and CORS support.
- Frontend Testing Page:
  - Input text, select voices, adjust speed and random seed.
  - Click the "Random" button to generate a random seed.
  - Generate and play speech in real-time.
- Audio Format:
  - Output: 24 kHz mono PCM.
  - Frontend automatically converts to WAV for playback.

### Project Background

This project is built upon the [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) open-source project, extending it with an API interface to enhance server-side functionality and user interaction. CosyVoice provides robust TTS model support, while CosyVoice TTS API encapsulates it into an easy-to-use web service.

Project Structure

text

```text
CosyVoice/
├── api/
│   ├── __init__.py       # Empty file to prevent import loops
│   ├── config.py        # Configuration (paths, keys, server settings)
│   ├── main.py          # FastAPI app defining API endpoints
│   ├── service.py       # TTS service logic, model loading, and speech generation
│   ├── prompts/         # Prompt files directory (e.g., aaa.wav, aaa.txt)
│   └── audio/           # Audio output directory (auto-created)
├── run-apy.py           # Startup script
├── test_config.py       # Configuration test script
├── CosyVoice-API-Test.html # Frontend testing page
└── README.md            # Project documentation
```

### Installation

Prerequisites

- CosyVoice
- Git
- Browser (Chrome or Firefox recommended)

Installation Steps

1. CosyVoice Dependency:

   - Install from the official repository:

     ```text
     https://github.com/FunAudioLLM/CosyVoice.git
     ```

   - Ensure the pretrained_models/CosyVoice2-0.5B model files are downloaded and placed in the pretrained_models/ folder in the project root. Refer to the [CosyVoice Installation Guide](https://github.com/FunAudioLLM/CosyVoice#installation).

2. In the CosyVoice Root Directory:

   ```bash
   pip install fastapi uvicorn torch librosa numpy pydantic
   git clone https://github.com/Oripal/CosyVoice-TTS-API.git
   ```

3. Prepare Prompt Files:

   - Add voice file pairs in the api/prompts/ directory, e.g.:

     ```text
     api/prompts/
     ├── aaaaa.wav
     ├── aaaaa.txt
     ├── bbbbb.wav
     ├── bbbbb.txt
     ```

### Usage

Starting the Backend Service

1. Run the service:

   ```bash
   python run.py
   ```

   - Default listening address: http://0.0.0.0:3005.

2. Verify the service:

   - Open a browser and visit CosyVoice-API-Test.html.

   - Test with curl:

     ```bash
     curl http://localhost:3005/api/voices
     curl -X POST "http://localhost:3005/api/tts" -H "X-API-Key: cosyvoice-api-demo" -H "Content-Type: application/json" -d '{"text": "Hello World", "voice_id": "aaaaa"}' > output.pcm
     ```

API Endpoints

- GET /api/voices

  - Returns the list of available voices.

  - Example response:

    ```json
    [{"id": "aaaaa", "name": "aaaaa"}, {"id": "bbbbb", "name": "bbbbb"}]
    ```

- POST /api/tts

  - Request body:

    ```json
    {
      "text": "Hello, this is a test speech",
      "voice_id": "aaaaa",
      "seed": 42,
      "speed": 1.0,
      "stream": true
    }
    ```

  - Response: PCM audio stream (24 kHz, mono).

Configuration

- Environment Variables:
  - COSYVOICE_API_KEY: Custom API key.
  - COSYVOICE_HOST and COSYVOICE_PORT: Server address and port.
- Modify api/config.py:
  - Update API_KEYS, MODEL_PATH, or PROMPTS_DIR.

### Contributing

Contributions to CosyVoice TTS API are welcome! Follow these steps:

1. Fork the repository.

2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit changes:

   ```bash
   git commit -m "Add your feature"
   ```

4. Push and create a Pull Request:

   ```bash
   git push origin feature/your-feature
   ```

### License

This project adheres to the [CosyVoice License](https://github.com/FunAudioLLM/CosyVoice/blob/main/LICENSE) (Apache 2.0). The extended API code is licensed under the MIT License (LICENSE).

Acknowledgments

- Thanks to [FunAudioLLM](https://github.com/FunAudioLLM) for the [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) project and model support.
- Gratitude to all contributors who assisted in debugging and testing!