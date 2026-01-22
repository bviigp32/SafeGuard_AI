import cv2
import numpy as np
import time
import io
import os
from kafka import KafkaConsumer
from ultralytics import YOLO
from minio import Minio
import psycopg2
from datetime import datetime

# --- 설정 구간 ---
TOPIC_NAME = 'cctv-stream'
MODEL_PATH = "runs/detect/safety_model/weights/best.pt" # 경로 확인!

# MinIO 설정 (사진 저장소)
minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)
BUCKET_NAME = "cctv-images"

# DB 설정 (로그 저장소)
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5433", # 포트 확인!
        database="safety_db",
        user="user",
        password="password"
    )

# --- 메인 로직 ---
def run_consumer():
    # 1. 리소스 준비
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers='localhost:9092', auto_offset_reset='latest')
    
    # 모델 로드 (없으면 자동 찾기)
    if not os.path.exists(MODEL_PATH):
        import glob
        files = glob.glob('runs/detect/*/weights/best.pt')
        model_path = max(files, key=os.path.getctime) if files else MODEL_PATH
    else:
        model_path = MODEL_PATH
    
    print(f"AI 모델 로드: {model_path}")
    model = YOLO(model_path)
    
    # MinIO 버킷 확인
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)
        print(f"MinIO 버킷 생성: {BUCKET_NAME}")

    print("감시 시스템 가동 시작...")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        for msg in consumer:
            # 이미지 복원
            nparr = np.frombuffer(msg.value, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is None: continue

            # AI 추론 (conf=0.6 이상만)
            results = model(frame, conf=0.8, verbose=False)
            annotated_frame = results[0].plot()

            # --- [핵심] 저장 로직 ---
            # 탐지된 객체가 있을 때만 저장 (용량 절약)
            if len(results[0].boxes) > 0:
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = model.names[cls_id] # helmet, head, person 등
                    
                    # 예: 'head'(안전모 미착용)만 골라서 저장하려면?
                    # if label == 'head': ... 로직 추가 가능
                    
                    # 1. 이미지 MinIO 업로드
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    filename = f"{label}_{timestamp}.jpg"
                    
                    # 메모리에서 바로 업로드 (디스크 저장 X)
                    _, img_encoded = cv2.imencode('.jpg', annotated_frame)
                    img_bytes = io.BytesIO(img_encoded)
                    
                    minio_client.put_object(
                        BUCKET_NAME, filename, img_bytes, len(img_encoded), content_type="image/jpeg"
                    )
                    
                    # 2. DB 로그 저장
                    image_url = f"http://localhost:9000/{BUCKET_NAME}/{filename}"
                    insert_query = """
                        INSERT INTO safety_logs (violation_type, image_url, confidence)
                        VALUES (%s, %s, %s)
                    """
                    cur.execute(insert_query, (label, image_url, conf))
                    conn.commit()
                    
                    print(f"📸 저장 완료: {label} ({conf:.2f}) -> DB & MinIO")

            # 화면 출력
            cv2.imshow("SafeGuard AI - Recording...", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        cv2.destroyAllWindows()
        consumer.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    run_consumer()