import streamlit as st
import psycopg2
import pandas as pd
from minio import Minio
from PIL import Image
import io
import time

# --- 설정 (Day 4와 동일) ---
DB_CONFIG = {
    "host": "localhost",
    "port": "5433",  # 포트 5433 확인!
    "database": "safety_db",
    "user": "user",
    "password": "password"
}

MINIO_CONF = {
    "endpoint": "localhost:9000",
    "access_key": "minioadmin",
    "secret_key": "minioadmin",
    "bucket": "cctv-images"
}

# --- 함수 정의 ---

# 1. DB에서 로그 가져오기
def fetch_logs():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # 최신순으로 50개만 가져오기
        query = "SELECT * FROM safety_logs ORDER BY id DESC LIMIT 50"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"DB 연결 실패: {e}")
        return pd.DataFrame()

# 2. MinIO에서 이미지 가져오기
def fetch_image_from_minio(image_url):
    try:
        client = Minio(
            MINIO_CONF["endpoint"],
            access_key=MINIO_CONF["access_key"],
            secret_key=MINIO_CONF["secret_key"],
            secure=False
        )
        # DB에 저장된 URL에서 파일명만 추출 (예: http://.../helmet_123.jpg -> helmet_123.jpg)
        filename = image_url.split("/")[-1]
        
        # MinIO에서 파일 데이터 읽기
        response = client.get_object(MINIO_CONF["bucket"], filename)
        img_data = response.read()
        response.close()
        
        return Image.open(io.BytesIO(img_data))
    except Exception as e:
        st.warning(f"이미지를 불러올 수 없습니다: {e}")
        return None

# --- 메인 화면 (UI) ---
st.set_page_config(page_title="SafeGuard AI 관제 시스템", layout="wide")

st.title("🚧 SafeGuard AI 실시간 관제 대시보드")
st.markdown("CCTV에서 감지된 **안전 장비 위반 사항**을 실시간으로 모니터링합니다.")

# 상단: 실시간 통계
col1, col2, col3 = st.columns(3)
df = fetch_logs()

if not df.empty:
    total_alerts = len(df)
    last_alert_time = df.iloc[0]['timestamp']
    most_common_violation = df['violation_type'].mode()[0]
else:
    total_alerts = 0
    last_alert_time = "-"
    most_common_violation = "-"

col1.metric("최근 감지 건수", f"{total_alerts}건")
col2.metric("마지막 감지 시간", str(last_alert_time))
col3.metric("최다 위반 유형", most_common_violation)

st.divider()

# 하단: 데이터 테이블 & 이미지 뷰어
col_table, col_img = st.columns([1.5, 1]) # 왼쪽이 좀 더 넓게

with col_table:
    st.subheader("위반 감지 로그 (최근 50건)")
    # 데이터프레임 보여주기
    st.dataframe(df, use_container_width=True)
    
    if st.button("새로고침"):
        st.rerun()

with col_img:
    st.subheader("증거 사진 확인")
    
    if not df.empty:
        # 사용자가 선택할 수 있는 셀렉트박스 (ID와 위반유형 표시)
        selected_id = st.selectbox(
            "확인할 로그 ID를 선택하세요:",
            df['id'].values,
            format_func=lambda x: f"ID {x} - {df[df['id']==x]['violation_type'].values[0]}"
        )
        
        # 선택된 행의 이미지 URL 찾기
        selected_row = df[df['id'] == selected_id]
        if not selected_row.empty:
            image_url = selected_row.iloc[0]['image_url']
            violation = selected_row.iloc[0]['violation_type']
            conf = selected_row.iloc[0]['confidence']
            
            # 이미지 가져와서 보여주기
            image = fetch_image_from_minio(image_url)
            if image:
                st.image(image, caption=f"{violation} (확신도: {conf:.2f})", use_container_width=True)
    else:
        st.info("아직 데이터가 없습니다.")

# 자동 리프레시 (선택 사항: 5초마다 새로고침)
# time.sleep(5)
# st.rerun()