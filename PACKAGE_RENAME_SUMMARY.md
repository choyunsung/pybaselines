# 패키지 이름 변경 요약: pybaselines → amcg-pybaselines

## 변경 개요

패키지 이름을 `pybaselines`에서 `amcg-pybaselines`로 변경했습니다.

## 주요 변경 사항

### 1. 패키지 디렉토리 변경
- `pybaselines/` → `amcg_pybaselines/`
- Python 패키지명은 하이픈을 사용할 수 없으므로 밑줄 사용

### 2. 설정 파일 업데이트

#### pyproject.toml
- `name = "amcg-pybaselines"`
- `version-file = "amcg_pybaselines/_version.py"`
- URLs 및 의존성 참조 업데이트

#### CITATION.cff
- 모든 URL과 제목에서 패키지명 변경
- 저장소 URL과 PyPI URL 업데이트

### 3. Python 코드 업데이트

#### Import 문 변경
```python
# 이전
from pybaselines import Baseline
from pybaselines.whittaker import aspls

# 변경 후
from amcg_pybaselines import Baseline
from amcg_pybaselines.whittaker import aspls
```

#### 영향받은 파일들
- 모든 패키지 내부 Python 파일
- 테스트 파일들 (`tests/`)
- 문서 예제들 (`docs/examples/`)
- 도구들 (`tools/`)
- 최적화 검증 스크립트들

### 4. 문서 업데이트

#### README.rst
- 패키지명, URL, 설치 명령어 모두 변경
- `pip install amcg-pybaselines`

#### 최적화 관련 문서들
- `aspls_optimization_plan.md`
- `aspls_optimization_summary.md`
- `ASPLS_OPTIMIZATION_README.md`

### 5. 빌드 및 검증 도구 업데이트

#### Makefile
- 모든 경로와 명령어에서 패키지명 변경
- 백업/복원 경로 업데이트

## 설치 및 사용법 변경

### 설치
```bash
# 이전
pip install pybaselines

# 변경 후
pip install amcg-pybaselines
```

### 사용법
```python
# 이전
import pybaselines
from pybaselines import Baseline

# 변경 후
import amcg_pybaselines
from amcg_pybaselines import Baseline
```

## 검증

### 문법 검사 완료
- ✓ `amcg_pybaselines/whittaker.py`
- ✓ `amcg_pybaselines/__init__.py`
- ✓ `benchmark_aspls.py`
- ✓ `test_aspls_optimized.py`

### 빌드 설정 확인
- ✓ pyproject.toml 업데이트
- ✓ CITATION.cff 업데이트
- ✓ README.rst 업데이트

## 마이그레이션 가이드

### 기존 사용자를 위한 변경사항

1. **설치명 변경**
   ```bash
   pip uninstall pybaselines
   pip install amcg-pybaselines
   ```

2. **코드 수정**
   ```python
   # 모든 import 문 변경
   from pybaselines import Baseline  # 이전
   from amcg_pybaselines import Baseline  # 변경 후
   ```

3. **API는 동일**
   - 모든 클래스, 메서드, 함수 이름은 그대로 유지
   - 사용 방법은 import 문만 변경하면 됨

## 주의사항

1. **Python import 규칙**
   - 패키지명(PyPI): `amcg-pybaselines` (하이픈 사용)
   - Python import: `amcg_pybaselines` (밑줄 사용)

2. **하위 호환성**
   - 기존 `pybaselines` 패키지와는 별도 패키지
   - 동시 설치 가능하지만 권장하지 않음

3. **URL 변경**
   - GitHub: `https://github.com/derb12/amcg-pybaselines`
   - Documentation: `https://amcg-pybaselines.readthedocs.io`
   - PyPI: `https://pypi.org/project/amcg-pybaselines`

## 완료 상태

✅ 모든 패키지 이름 변경 완료  
✅ 설정 파일 업데이트 완료  
✅ Python 코드 import 문 업데이트 완료  
✅ 문서 업데이트 완료  
✅ 빌드 도구 업데이트 완료  
✅ 문법 검사 통과  

패키지는 이제 `amcg-pybaselines`로 완전히 변경되었습니다.