from ultralytics import YOLO
import os
import glob

# 1. 학습된 모델 경로 (runs 폴더 안에 가장 최신 폴더를 찾으세요)
# 보통 runs/detect/safety_model/weights/best.pt 에 있습니다.
# 만약 safety_model2, 3... 이렇게 늘어났다면 가장 숫자가 높은 걸 쓰세요.
model_path = "runs/detect/safety_model3/weights/best.pt"

# (혹시 경로 못 찾을까봐 안전장치)
if not os.path.exists(model_path):
    # runs/detect 안에서 가장 최근에 수정된 폴더의 best.pt 찾기
    list_of_files = glob.glob('runs/detect/*/weights/best.pt') 
    latest_file = max(list_of_files, key=os.path.getctime)
    model_path = latest_file

print(f"모델 로드 중: {model_path}")
model = YOLO(model_path)

# 2. 테스트할 이미지 찾기 (test 폴더에서 아무거나 하나)
test_images = glob.glob("datasets/Hard-Hat-Universe-1/test/images/*.jpg")
if not test_images:
    # 폴더명이 다를 수 있으니 유연하게 찾기
    test_images = glob.glob("datasets/*/test/images/*.jpg")

target_image = test_images[0] # 첫 번째 사진 선택
print(f"📸 테스트 이미지: {target_image}")

# 3. 예측 실행 (결과 저장)
# conf=0.5 : 확신이 50% 이상인 것만 박스 그리기
results = model.predict(source=target_image, save=True, conf=0.5)

print(f"\n결과 저장 완료!")
print(f"확인 경로: {results[0].save_dir}")
print("위 폴더에 들어가서 .jpg 파일을 열어보세요. 머리에 박스가 쳐져 있나요?")