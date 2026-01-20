from roboflow import Roboflow
import os

# 1. 데이터셋 저장할 폴더 생성
os.makedirs("datasets", exist_ok=True)
os.chdir("datasets")

print("데이터셋 다운로드 중... (약 100MB)")

# [수정할 부분] 아래 "YOUR_API_KEY" 자리에 방금 복사한 진짜 키를 넣으세요!
# 예: rf = Roboflow(api_key="aBcDeFgHiJkLmNoP")
rf = Roboflow(api_key="Ppx8lMffHsfinE2vss0X")
project = rf.workspace("kimdata").project("hard-hat-universe-0dy7t-zl56l")
version = project.version(1)
dataset = version.download("yolov8")

print("\n다운로드 완료! 'datasets/Hard-Hat-Universe-11' 폴더를 확인하세요.")
