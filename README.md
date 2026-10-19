# Daily Focus Board

오늘 해야 할 일을 중요도와 함께 정리하고 진행 상황을 한눈에 확인하는 간단한 웹 앱입니다.

## 주요 기능

- 할 일 추가 및 중요도 선택 (High, Medium, Low)
- 할 일 완료 표시 및 삭제
- 완료율을 보여주는 진행률 바
- 모든 할 일을 완료하면 축하 메시지 표시
- 카드형 화면, 마우스 오버 효과, 완료한 항목의 취소선, 모바일 반응형 레이아웃
- SQLite를 이용한 데이터 저장

## 실행 방법

저장소 루트에서 가상환경을 만들고 의존성을 설치합니다.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

개발 서버를 실행합니다.

```bash
.venv/bin/uvicorn main:app --reload
```

브라우저에서 [http://127.0.0.1:8000](http://127.0.0.1:8000)을 엽니다. 서버를 종료하려면 터미널에서 `Ctrl+C`를 누릅니다.

## 데이터 저장

앱을 시작하면 저장소 루트에 `focus.db`와 `tasks` 테이블이 자동으로 생성됩니다. 데이터베이스 파일은 로컬 실행 데이터이며 Git에서 제외됩니다.

## 프로젝트 구조

```text
.
├── main.py              # FastAPI 라우트, SQLite 초기화 및 데이터 처리
├── requirements.txt     # Python 의존성 목록
├── templates/
│   └── index.html       # 한국어 메인 화면
└── static/
    └── style.css        # 반응형 화면 스타일
```
