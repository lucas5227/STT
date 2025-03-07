# STT
OpenAI Whisper를 활용한 Speech-to-Text application 입니다.
2025.03.06~2025.03.

by https://github.com/lucas5227

## Requirements

* Python 3.9 ~ 3.11 (3.11에서 재작)
* [Pip](https://pip.pypa.io/en/stable/installing/)
* [FFmpeg](https://ffmpeg.org/download.html)
    * on Ubuntu or Debian: `sudo apt update && sudo apt install ffmpeg`
    * on Arch Linux: `sudo pacman -S ffmpeg`
    * on MacOS using Homebrew (https://brew.sh/): `brew install ffmpeg`
    * on Windows using Chocolatey (https://chocolatey.org/): `choco install ffmpeg`
    * on Windows using Scoop (https://scoop.sh/): `scoop install ffmpeg`

## Installation

```bash
pip install -r requirements.txt
```

# .env 

```text
touch .env
echo "OPENAI_API_KEY=your-openai-api-key" >> .env
```

# 파일 위치
- `in/`: 입력 파일 위치
- `out/`: 출력 파일 위치

# Run

```bash
python .
```