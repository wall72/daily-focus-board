# 저장소 작업 안내

## 프로젝트 개요

Daily Focus Board는 FastAPI, Jinja2, SQLite로 만든 서버 렌더링 할 일 관리 앱입니다. 구현을 간결하게 유지하고 `main.py`, `templates/`, `static/` 구조를 따릅니다.

## 개발 환경

- Python 명령은 저장소의 `.venv` 가상환경을 사용합니다.
- 의존성은 `.venv/bin/pip install -r requirements.txt`로 설치합니다.
- 저장소 루트에서 `.venv/bin/uvicorn main:app --reload`로 앱을 실행합니다.
- FastAPI 앱이 시작될 때 프로젝트 루트에 `focus.db`와 `tasks` 테이블을 생성합니다. 데이터베이스는 로컬 실행 데이터이므로 커밋하지 않습니다.

## 구현 규칙

- HTTP 라우트, SQLite 접근, 할 일 관련 계산은 `main.py`에 둡니다.
- 화면 마크업은 `templates/index.html`, 표현 스타일은 `static/style.css`에 둡니다.
- SQL 값에는 매개변수 바인딩을 사용하고, 할 일 추가 전에 중요도가 `High`, `Medium`, `Low` 중 하나인지 확인합니다.
- 폼은 URL 인코딩 요청 본문을 사용하며, 변경 작업 후 `/`로 이동합니다.
- 화면을 수정할 때 한국어 UI, 반응형 레이아웃, 접근성 라벨, 완료 항목 스타일, 진행률 표시, 전체 완료 메시지를 유지합니다.
- 런타임 의존성은 `requirements.txt`에 추가합니다. 특별한 이유가 없다면 프런트엔드 프레임워크를 도입하지 않습니다.

## 저장소 관리

- `.venv/`, Python 캐시 파일, `focus.db`는 커밋하지 않습니다. 해당 항목은 `.gitignore`에서 제외합니다.
- 문서와 소스 변경은 요청된 기능에 맞게 간결하게 유지합니다.
