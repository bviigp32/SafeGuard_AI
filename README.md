# SafeGuard AI: 실시간 안전 장비 감지 시스템

CCTV 영상 스트림을 분석하여 작업자의 안전모/조끼 착용 여부를 실시간으로 탐지하고, 위반 사항을 기록하는 AI & Big Data 프로젝트입니다.

## 프로젝트 진행 로그
* **Day 1**: 빅데이터 인프라 구축 (Kafka, MinIO, PostgreSQL, Zookeeper)
* **Day 2**: AI 모델 학습 (YOLOv8)
  * Roboflow에서 'Hard Hat Universe' 데이터셋 수집 및 전처리
  * Mac M3 (MPS) 가속을 활용한 YOLOv8 Fine-tuning 학습
  * 안전모(Helmet), 조끼(Vest), 사람(Person) 객체 탐지 성능 검증 완료
* **Day 3**: 실시간 스트리밍 파이프라인 구축 (Kafka Producer/Consumer)
  * **Producer**: OpenCV로 웹캠 영상을 캡처하여 Kafka Topic(`cctv-stream`)으로 실시간 전송
  * **Consumer**: Kafka에서 스트림 데이터를 수신하여 이미지로 복원
  * **Inference**: YOLOv8 모델을 통해 실시간 객체 탐지 및 모니터링 화면 출력
* **Day 4**: 데이터 영구 저장 시스템 구축 (DB & Storage)
  * **PostgreSQL**: `safety_logs` 테이블 설계 및 탐지 로그(위반 유형, 시간, 확신도) 저장 구현 (Port 5433)
  * **MinIO**: 객체 탐지 시점의 스냅샷 이미지를 클라우드 스토리지(Bucket: `cctv-images`)에 자동 업로드
  * **Backend**: Consumer 로직을 확장하여 AI 추론 결과를 DB/Storage로 라우팅
  * *Note: 현재 모델은 데이터 편향으로 인해 대부분의 객체를 Helmet으로 인식하는 경향이 있음 (추후 개선 예정)*

## 기술 스택
* **Core**: Python 3.11, Kafka, YOLOv8 (Ultralytics)
* **Infra**: Docker Compose, MinIO (Object Storage)
* **Database**: PostgreSQL
* **Hardware**: Apple Silicon (M3)

## 프로젝트 구조
```bash
safeguard-ai/
├── docker-compose.yml   # 인프라 실행 설정 (Kafka, DB, MinIO)
├── download_data.py     # 데이터셋 다운로드
├── fix_dataset.py       # 데이터셋 경로 수정 유틸
├── train_model.py       # YOLO 모델 학습 스크립트
├── test_inference.py    # 학습된 모델 테스트 스크립트
├── producer.py          # [Day 3] Webcam 영상 송신 (Producer)
├── consumer.py          # [Day 3] 영상 수신 및 AI 추론 (Consumer)
├── datasets/            # (Git 제외) 학습 데이터
└── runs/                # (Git 제외) 학습 결과 및 모델(best.pt)
├── init_db.py           # [Day 4] DB 테이블 초기화 스크립트
```