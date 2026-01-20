# SafeGuard AI: 실시간 안전 장비 감지 시스템

CCTV 영상 스트림을 분석하여 작업자의 안전모/조끼 착용 여부를 실시간으로 탐지하고, 위반 사항을 기록하는 AI & Big Data 프로젝트입니다.

## 프로젝트 진행 로그
* **Day 1**: 빅데이터 인프라 구축 (Kafka, MinIO, PostgreSQL, Zookeeper)
* **Day 2**: AI 모델 학습 (YOLOv8)
  * Roboflow에서 'Hard Hat Universe' 데이터셋 수집 및 전처리
  * YOLOv8 Fine-tuning 학습
  * 안전모(Helmet), 조끼(Vest), 사람(Person) 객체 탐지 성능 검증 완료

## 기술 스택
* **Core**: Python 3.11, Kafka, YOLOv8 (Ultralytics)
* **Infra**: Docker Compose, MinIO (Object Storage)
* **Database**: PostgreSQL

## 프로젝트 구조
```bash
safeguard-ai/
├── docker-compose.yml   # 인프라 실행 설정
├── train_model.py       # YOLO 모델 학습 스크립트
├── test_inference.py    # 학습된 모델 테스트 스크립트
├── download_data.py     # 데이터셋 다운로드
└── datasets/            # (Git 제외) 학습 데이터
```