import cv2
import time
from kafka import KafkaProducer

# 1. Kafka Producer 설정
# bootstrap_servers: Kafka 주소 (localhost:9092)
producer = KafkaProducer(bootstrap_servers='localhost:9092')
TOPIC_NAME = 'cctv-stream'

# 2. 웹캠 연결 (0번은 보통 내장 카메라)
print("웹캠을 시작합니다...")
cap = cv2.VideoCapture(0)

# 해상도나 FPS 설정 (선택사항)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

if not cap.isOpened():
    print("웹캠을 열 수 없습니다. 권한을 확인하세요.")
    exit()

try:
    print(f"'{TOPIC_NAME}' 토픽으로 영상 전송 시작! (멈추려면 Ctrl+C)")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 3. 이미지 전처리 (Resize -> JPEG Encoding)
        # 데이터를 줄여서 보내야 Kafka가 안 체합니다. (640x640 권장)
        frame = cv2.resize(frame, (640, 640))
        
        # 이미지를 바이트(bytes)로 변환
        ret, buffer = cv2.imencode('.jpg', frame)
        
        if ret:
            # 4. Kafka로 전송 (bytes 전송)
            producer.send(TOPIC_NAME, buffer.tobytes())
            
            # 너무 빠르면 데이터가 밀릴 수 있으니 약간의 딜레이 (0.03초 = 약 30FPS)
            time.sleep(0.03)

except KeyboardInterrupt:
    print("\n전송 중단")
finally:
    cap.release()
    producer.close()