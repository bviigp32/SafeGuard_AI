import cv2
import numpy as np
from kafka import KafkaConsumer
from ultralytics import YOLO
import os

# 1. Kafka Consumer 설정
TOPIC_NAME = 'cctv-stream'
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest' # 가장 최신 데이터부터 읽기 (실시간성 중요)
)

# 2. YOLO 모델 로드 (어제 만든 best.pt 경로 확인 필수!)
# 예: runs/detect/safety_model/weights/best.pt
model_path = "runs/detect/safety_model/weights/best.pt" 

# (경로 못 찾을까봐 안전장치 - 어제 코드 재활용)
if not os.path.exists(model_path):
    import glob
    list_of_files = glob.glob('runs/detect/*/weights/best.pt') 
    if list_of_files:
        model_path = max(list_of_files, key=os.path.getctime)
    else:
        print("모델 파일(best.pt)을 찾을 수 없습니다! 경로를 확인하세요.")
        exit()

print(f"모델 로드 중: {model_path}")
model = YOLO(model_path)

print("Kafka에서 영상을 받아오는 중... (화면이 뜰 때까지 기다리세요)")

try:
    for msg in consumer:
        # 3. Kafka 메시지(bytes) -> 이미지(numpy array)로 복구
        # byte array를 numpy로 변환
        nparr = np.frombuffer(msg.value, np.uint8)
        # 이미지 디코딩
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            continue

        # 4. YOLO 추론 (Inference)
        results = model(frame, conf=0.7, verbose=False)
        
        # 5. 결과 시각화 (박스 그리기)
        annotated_frame = results[0].plot()

        # 6. 화면 출력
        cv2.imshow("SafeGuard AI - Realtime Monitor", annotated_frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n모니터링 중단")
finally:
    cv2.destroyAllWindows()
    consumer.close()