from ultralytics import YOLO
import os

def train():
    # 1. 모델 불러오기 (가벼운 Nano 버전 사용)
    # 처음에는 coco 데이터로 학습된 깡통 모델(yolov8n.pt)을 로드합니다.
    model = YOLO('yolov8n.pt')  

    # 2. 데이터셋 경로 설정 (절대 경로 추천)
    # 방금 다운로드한 data.yaml 파일의 위치
    dataset_path = os.path.abspath("datasets/Hard-Hat-Universe-1/data.yaml")

    # 3. 학습 시작 (M3 칩 가속 활용 -> device='mps')
    print("M3 GPU(MPS)를 사용하여 학습을 시작합니다...")
    results = model.train(
        data=dataset_path,
        epochs=10,         # 테스트용이라 10번만 (성능 높이려면 50~100 추천)
        imgsz=640,         # 이미지 크기
        device='mps',      # [중요] Mac M1/M2/M3 가속 활성화
        batch=16,          # 메모리 부족하면 8로 줄이세요
        name='safety_model' # 결과 저장 폴더 이름
    )
    
    print("학습 완료! 결과는 'runs/detect/safety_model' 에 저장되었습니다.")

if __name__ == '__main__':
    train()