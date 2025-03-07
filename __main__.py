import os
import inquirer
import datetime
from tqdm import tqdm
import Gemini
G = Gemini.Gemini()

def cmd_select(question, selects):
    selects.append("종료")
    question1 = [
        inquirer.List("choice", message=question, choices=selects)
    ]
    choice = inquirer.prompt(question1)['choice']
    if choice == "종료":
        exit()

    return choice

def STT(path):
    import whisper
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

def save(text, output_dir, og_filename):
    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d_%H%M%S") + "_" + og_filename.replace('.', '_') + ".txt"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(text)
    
    return output_dir + "/" + filename

def run():
    menus = ["음성&영상 → txt", "Gemini로 요약"]
    question = "작업을 선택하세요"
    choice1 = cmd_select(question, menus)
    
    if choice1 == "음성&영상 → txt": 
        files = os.listdir("in")
        choice2 = cmd_select("텍스트로 변환할 파일을 선택하세요", files)
        print("추출중...")
        text = STT(f"in/{choice2}")
        save(text, "out/stt", choice2)
        print("저장완료: out/stt/{out}로 변환완료.")
    
    elif choice1 == "Gemini로 요약":
        source_path = "out/stt"
        files = os.listdir(source_path)
        choice2 = cmd_select("Gemini로 교정할 파일을 선택하세요", files)
        result = G.summary(f"{source_path}/{choice2}")
        save(result, "out/summery", choice2)

while True:
    run()