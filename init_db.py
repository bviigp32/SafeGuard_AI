import psycopg2

def create_table():
    try:
        # 1. DB 연결 (docker-compose.yml에 설정한 값)
        conn = psycopg2.connect(
            host="localhost",
            port="5433", # 혹은 5433 (포트 확인 필요! docker ps로 확인하세요)
            database="safety_db",
            user="user",
            password="password"
        )
        cur = conn.cursor()

        # 2. 테이블 생성 쿼리
        # log_id, timestamp, violation_type(헬멧 미착용 등), image_url, confidence
        create_query = """
        CREATE TABLE IF NOT EXISTS safety_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            violation_type VARCHAR(50),
            image_url VARCHAR(255),
            confidence FLOAT
        );
        """
        cur.execute(create_query)
        conn.commit()
        print("'safety_logs' 테이블 생성 완료!")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"DB 연결 실패: {e}")
        print("힌트: 'docker-compose up'이 켜져 있는지, 포트가 5432인지 5433인지 확인하세요.")

if __name__ == "__main__":
    create_table()