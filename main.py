"""
1. install inquirer
    pip install inquirer

2. install whisper
    pip install openai-whisper
x
3. Install FFmpeg
    # on Ubuntu or Debian
    sudo apt update && sudo apt install ffmpeg
    # on Arch Linux
    sudo pacman -S ffmpeg
    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg
    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg
    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
"""
import os
import inquirer
import whisper
import datetime
from tqdm import tqdm

def STT(path):
    model = whisper.load_model("turbo")
    result = model.transcribe(path, verbose=False)
    segments = result["segments"]

    # result에 "duration" 키가 없으면 마지막 세그먼트의 end 값을 총 길이로 사용
    total_duration = result.get("duration", segments[-1]["end"] if segments else 0)

    text = ""
    pbar = tqdm(total=total_duration, desc="Transcribing", ncols=100, unit="sec")
    last_progress = 0
    for segment in segments:
        current_progress = segment['start']
        pbar.update(current_progress - last_progress)
        last_progress = current_progress

        minutes, seconds = divmod(segment['start'], 60)
        hours, minutes = divmod(minutes, 60)
        start = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        minutes, seconds = divmod(segment['end'], 60)
        hours, minutes = divmod(minutes, 60)
        end = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        text += f"[{start} ~ {end}] {segment['text']}\n"
    
    # 최종 진행률 보정
    if pbar.n < total_duration:
        pbar.update(total_duration - pbar.n)
    pbar.close()

    return text

def save(text, output_dir):
    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d_%H%M%S") + "_" + os.path.basename(path).replace('.', '_') + ".txt"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(text)
    
    path = output_dir + "/" + filename

    return path

def run():

    menu = ["음성&영상 → txt", "Gemini로 자연스럽게", "Gemini로 요약"]
    question1 = [
        inquirer.List("choice", message="텍스트로 변환할 파일을 선택하세요", choices=menu)
    ]
    choice1 = inquirer.prompt(question1)['choice']
    
    if choice1 == "음성&영상 → txt": 
        files = os.listdir("resources")
        question2 = [
            inquirer.List("choice", message="텍스트로 변환할 파일을 선택하세요", choices=files)
        ]
        choice2 = inquirer.prompt(question2)['choice']
        text = STT(f"resources/{choice2}")
        print("추출중...")
        save(text, "out/stt")
        print("저장완료: out/stt/{out}로 변환완료.")
    
    elif choice2 == "Gemini로 자연스럽게":
        print("개발중...")
    
    elif choice2 == "Gemini로 요약":
        print("개발중...")
        
    

if __name__ == "__main__":
    run()

    main()    # 