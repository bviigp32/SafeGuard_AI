# 👷SafeGuard AI: 실시간 안전 장비 감지 시스템
**CCTV 영상 스트림**을 분석하여 작업자의 안전모/조끼 착용 여부를 **실시간으로 탐지**하고, 위반 사항을 기록하는 **End-to-End AI 파이프라인 프로젝트**입니다.
**MSA(Microservices Architecture)** 개념을 적용하여 메시지 브로커, 데이터베이스, 스토리지, AI 모델을 유기적으로 연결했습니다.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![Kafka](https://img.shields.io/badge/Apache%20Kafka-Streaming-231F20?logo=apachekafka) ![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-00FFFF?logo=yolo) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-4169E1?logo=postgresql) ![MinIO](https://img.shields.io/badge/MinIO-Storage-C72C48?logo=minio) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)

## 프로젝트 진행 로그 (5-Day Challenge)
* **Day 1**: 빅데이터 인프라 구축 (Kafka, MinIO, PostgreSQL, Zookeeper)
* **Day 2**: AI 모델 학습 (Roboflow 데이터셋 + YOLOv8 Fine-tuning)
* **Day 3**: 실시간 스트리밍 파이프라인 구축 (Webcam → Kafka Producer → Consumer)
* **Day 4**: 데이터 영구 저장 시스템 구현 (위반 로그 DB 저장 + 증거 사진 MinIO 업로드)
* **Day 5**: 통합 관제 대시보드 개발 (Streamlit 기반 실시간 모니터링 UI)

## 기술 스택 (Tech Stack)
| Category | Technology |
| :--- | :--- |
| **Language** | Python 3.11 |
| **AI / Vision** | YOLOv8 (Ultralytics), OpenCV |
| **Streaming** | Apache Kafka (Event Streaming) |
| **Database** | PostgreSQL (Detection Logs) |
| **Storage** | MinIO (Evidence Snapshots - S3 Compatible) |
| **Frontend** | Streamlit (Admin Dashboard) |
| **Infra / DevOps** | Docker, Docker Compose |
| **Hardware** | Apple Silicon M3 (MPS Acceleration) |

## 프로젝트 구조 (Architecture)
```bash
safeguard-ai/
├── docker-compose.yml   # 인프라 실행 설정 (Kafka, DB, MinIO)
├── producer.py          # [Core] 영상 송신 (Webcam -> Kafka)
├── consumer.py          # [Core] 영상 수신 및 AI 추론 (Kafka -> YOLO -> DB/MinIO)
├── dashboard.py         # [UI] 관제 대시보드 (Streamlit)
├── init_db.py           # DB 테이블 초기화 스크립트
├── check_db.py          # DB 데이터 검증 스크립트
├── train_model.py       # YOLOv8 학습 스크립트
├── test_inference.py    # 모델 추론 테스트 스크립트
├── datasets/            # 학습 데이터 (Hard Hat Universe)
└── runs/                # 학습된 모델 가중치 (best.pt)

```

## 주요 기능 (Key Features)

1. **Kafka 기반 실시간 스트리밍**
* OpenCV로 캡처한 고해상도 웹캠 영상을 압축하여 Kafka Topic(`cctv-stream`)으로 전송
* Producer-Consumer 구조를 통해 **지연 시간(Latency) 최소화** 및 데이터 처리량 증대


2. **AI 안전 장비 탐지 (YOLOv8)**
* 작업자의 **안전모(Helmet)**, **조끼(Vest)** 착용 여부를 실시간으로 판별
* Mac M3 칩의 **MPS(Metal Performance Shaders)** 가속을 활용한 고속 추론


3. **증거 데이터 영구 보존 (Evidence Logging)**
* **PostgreSQL:** 위반 발생 시각, 위반 유형, AI 확신도(Confidence)를 정형 데이터로 저장
* **MinIO:** 위반 순간의 스냅샷(Snapshot) 이미지를 객체 스토리지에 자동 업로드


4. **통합 관제 대시보드**
* **Streamlit**을 활용하여 복잡한 터미널 명령 없이 웹 브라우저에서 현황 파악
* 최근 위반 이력 리스트 확인 및 증거 이미지 클릭 시 확대 보기 기능 제공



## 실행 방법 (How to Run)

**1. 인프라 실행 (Docker)**
Kafka, Zookeeper, DB, MinIO 컨테이너를 실행합니다.

```bash
docker-compose up -d

```

**2. DB 초기화**
PostgreSQL에 로그 테이블을 생성합니다.

```bash
python init_db.py

```

**3. 서비스 가동 (3개의 터미널 필요)**

```bash
# Terminal 1: 영상 송신 (Producer)
python producer.py

# Terminal 2: AI 감지 및 저장 (Consumer)
python consumer.py

# Terminal 3: 대시보드 실행 (Dashboard)
streamlit run dashboard.py

```

**접속 주소:**

* **Dashboard:** http://localhost:8501
* **MinIO Console:** http://localhost:9001 (ID/PW: minioadmin)

## 알려진 이슈 (Known Issues)

* **Dataset Bias:** 현재 학습 데이터셋의 특성상 머리 부분이나 모자를 쓴 경우를 대부분 'Helmet'으로 인식하는 경향이 있습니다. 추후 'No-Helmet' 클래스 데이터를 보강하여 재학습할 예정입니다.

---

*Created by [Kim Kyunghun]*