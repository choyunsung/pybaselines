# AMCG-Pybaselines ASPLS 최적화 검증 가이드

이 문서는 aspls 알고리즘 최적화의 검증 방법을 설명합니다.

## 빠른 시작

```bash
# 전체 검증 실행
make verify

# 성능 벤치마크 실행
make benchmark
```

## Makefile 타겟

### 기본 명령어

- `make help` - 사용 가능한 모든 명령어 표시
- `make verify` - 모든 검증 테스트 실행 (기본 타겟)
- `make test` - 기본 기능 테스트 실행
- `make benchmark` - 성능 벤치마크 실행

### 백업 및 복원

- `make backup` - 원본 파일 백업 생성
- `make restore` - 백업에서 원본 복원

### 검증 단계별 실행

1. `make check-syntax` - Python 문법 검사
2. `make verify-simple` - 간단한 동작 검증
3. `make verify-behavior` - 상세 동작 비교 검증

### 유틸리티

- `make clean` - 생성된 파일 정리
- `make install-deps` - 필요한 의존성 설치
- `make report` - 검증 보고서 생성

## 전체 검증 워크플로우

```bash
# 1. 백업 생성
make backup

# 2. 전체 검증 실행
make full-verify

# 3. 검증 보고서 생성
make report
```

## 검증 항목

### 1. 문법 검사
- 모든 Python 파일의 문법 오류 검사
- import 가능 여부 확인

### 2. 동작 검증
- 동일 입력에 대한 동일 출력 확인
- weights와 alpha 값의 수치적 일치성 (오차 < 1e-10)
- 엣지 케이스 처리 (작은 데이터셋, 상수 데이터 등)

### 3. 성능 검증
- 다양한 데이터 크기에서 실행 시간 측정
- 웜 스타트 효과 검증
- 메모리 사용량 비교

## 검증 결과 해석

### ✓ 성공 표시
- 문법 검사 통과
- 결과값 일치 (수치 오차 범위 내)
- 성능 향상 확인

### ✗ 실패 표시
- 문법 오류 발생
- 결과값 불일치
- 예외 발생

## 문제 해결

### Python 모듈을 찾을 수 없는 경우
```bash
make install-deps
# 또는
pip install numpy scipy
```

### 백업이 이미 존재하는 경우
```bash
# 기존 백업 확인
ls pybaselines/whittaker_backup.py

# 필요시 수동으로 백업 관리
mv pybaselines/whittaker_backup.py pybaselines/whittaker_backup_old.py
make backup
```

### 검증 실패 시
1. `make restore`로 원본 복원
2. 최적화 코드 검토 및 수정
3. 다시 검증 실행

## CI/CD 통합

```bash
# CI 환경에서 빠른 테스트
make ci-test

# 전체 검증 (백업 포함)
make full-verify
```

## 검증 보고서

`make report` 실행 시 `verification_report.md` 파일이 생성되며, 다음 내용을 포함합니다:
- 실행 날짜 및 시간
- 문법 검사 결과
- 각 검증 테스트 결과
- 성능 측정 결과

## 요약

이 Makefile은 aspls 최적화가 올바르게 동작하는지 체계적으로 검증할 수 있도록 합니다. 모든 테스트가 통과하면 최적화된 구현이 원본과 동일한 결과를 생성하면서도 더 나은 성능을 제공함을 확신할 수 있습니다.