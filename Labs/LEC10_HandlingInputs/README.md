# DRILL #9: 소년 상하좌우 이동 및 방향 바꾸기

최종 실행 파일: `Drill-09.py`

## 실행

저장소 루트에서:

```sh
python Labs/LEC10_HandlingInputs/Drill-09.py
```

Pico2D 1.5.1이 필요합니다. 현재 macOS 수업 환경에서는 `.venv/bin/python`을 사용하며 필요시 `SDL_RENDER_DRIVER=software`를 지정합니다.

## 조작과 구현

- 방향키를 누르는 동안 상하좌우로 계속 이동, 떼면 멈춤
- 좌우 방향에 맞는 Run 및 Idle 애니메이션, 상하 이동 시 마지막 좌우 방향 유지
- 화면 중앙 (400, 300)에서 시작
- 100×100 스프라이트 전체가 800×600 화면 안에 머물도록 x=50~750, y=50~550 제한
- 키 상태를 집합으로 관리하여 키 자동 반복 및 동시 입력 처리
- 대각선 이동 속도 정규화, 프레임 시간 기반 이동과 8프레임 애니메이션
- ESC 또는 창 닫기로 종료
- 수업 저장소의 LEC10 예제 이미지 사용

## 자동 테스트

```sh
python -m unittest discover -s Labs/LEC10_HandlingInputs -p 'test_drill_09.py' -v
```

## 개발 기록

`drill-09` 브랜치에서 중앙 시작 → 방향키 이동 → 방향별 애니메이션 → 경계 제한 → 테스트 순으로 점진적으로 구현했습니다.
