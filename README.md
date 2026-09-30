# prompt-library

검증된 AI 프롬프트와 사용 맥락, 실패 패턴, 재사용 규칙을 체계적으로 관리하는 개인 프롬프트 라이브러리입니다.

단순히 "잘 나온 프롬프트 모음"이 아니라, **무엇을 바꾸고 무엇을 고정해야 하는지**, **어떤 표현이 실패를 유발했는지**, **어떤 모델/작업에서 검증되었는지**를 함께 기록하는 것을 원칙으로 합니다.

## 빠른 탐색

전체 프롬프트는 [CATALOG.md](CATALOG.md)에서 표 형태로 탐색합니다.

`CATALOG.md`는 각 프롬프트 문서의 metadata를 읽어 자동 생성되므로 직접 수정하지 않습니다.

## 문서 작성 원칙

### 기본 언어

- 설명, 용례, 실패 원인, 사용법 등 **문서 본문은 한글 중심**으로 작성합니다.
- 프롬프트는 원칙적으로 **한글/영문을 병기**합니다.
- 각 프롬프트에는 반드시 **프롬프트 전송 권장 언어**를 표시합니다.
- 권장 언어가 **한글(`ko`)**인 경우에는 영문 프롬프트를 생략할 수 있습니다.
- 권장 언어가 **영문(`en`)**인 경우에는 실제 전송용 영문 프롬프트와 함께 이해/수정용 한글 버전을 제공합니다.
- 권장 언어가 **무관(`any`)**인 경우에도 재사용성을 위해 한글/영문을 함께 관리합니다.

### 검증 상태

- `VERIFIED`: 실제 사용 결과가 좋았고 재사용 가치가 확인됨
- `EXPERIMENTAL`: 아이디어 또는 제한적 성공 단계
- `DEPRECATED`: 더 나은 프롬프트로 대체되었거나 부작용이 확인됨

### 프롬프트 문서에 반드시 기록할 것

- 목적과 적용 범위
- 변경 대상(Variable)
- 고정 대상(Lock / Invariant)
- 권장 전송 언어
- 모델 또는 모델 계열
- 검증일
- 한글 프롬프트
- 영문 프롬프트(필요한 경우)
- 잘 맞는 용례 / 피해야 할 용례
- 알려진 실패 패턴 또는 주의점

## 디렉터리 구조

```text
prompt-library/
├── README.md
├── CATALOG.md
├── image/
│   ├── generation/
│   └── editing/
│       ├── relighting/
│       ├── shading/
│       ├── style-transfer/
│       ├── identity-lock/
│       └── background/
├── music/
├── video/
├── text/
├── agents/
├── cases/                  # 선택 사항: 상세 실험 기록이 필요할 때만
├── templates/
│   └── PROMPT_TEMPLATE.md
├── scripts/
│   └── build_catalog.py
└── .github/
    └── workflows/
        └── build-catalog.yml
```

Repository 자체가 prompt library이므로 최상위에 별도의 `prompts/` 계층은 두지 않습니다.

## Prompt와 Case

### Prompt — 기본 관리 단위

실제 다음 작업에서 바로 재사용할 수 있도록 일반화한 프롬프트입니다.

예:

```text
image/editing/shading/preserve-lighting-anime-shading.md
```

사용법, 실패 패턴, 검증 메모처럼 재사용에 필요한 정보는 가능한 한 **Prompt 문서 하나에 함께 기록**합니다.

### Case — 선택 사항

`cases/`는 필수 단계가 아닙니다.

동일 문제를 반복 실험하거나, 모델별 비교처럼 별도 연구 기록이 가치가 있을 때만 사용합니다. 일반적인 프롬프트 등록을 위해 Case 문서를 추가할 필요는 없습니다.

## 자동 카탈로그

`scripts/build_catalog.py`는 Prompt 문서의 YAML front matter를 읽어 다음을 수행합니다.

1. `CATALOG.md` 자동 생성
2. ID 중복 검사
3. 필수 metadata 검사
4. status / 권장 언어 값 검증
5. 저장소의 한글·영문 병기 정책 검사
6. `VERIFIED` 문서의 검증일·모델 정보 검사

### 로컬 실행

```bash
python scripts/build_catalog.py
```

카탈로그를 수정하지 않고 최신 여부만 검사하려면:

```bash
python scripts/build_catalog.py --check
```

외부 Python 패키지는 필요하지 않습니다.

### GitHub Actions

`main` 브랜치의 Markdown 프롬프트 또는 카탈로그 생성 코드가 변경되면 GitHub Actions가 자동으로:

```text
Prompt 추가/수정
        ↓
metadata 검증
        ↓
CATALOG.md 재생성
        ↓
변경이 있으면 자동 commit
```

합니다.

따라서 새 프롬프트 등록 시 `CATALOG.md`를 사람이 직접 편집할 필요가 없습니다.

## Metadata

기본 예시는 `templates/PROMPT_TEMPLATE.md`를 사용합니다.

주요 필드:

- `id`: 프롬프트 고유 ID
- `title`: 한글 중심 제목
- `status`: `VERIFIED | EXPERIMENTAL | DEPRECATED`
- `domain`: 선택 사항. 생략하면 최상위 디렉터리명에서 자동 추론
- `category`: 작업 카테고리
- `task`: 세부 작업 유형
- `model_family`: 검증 모델/계열
- `verified_at`: 검증일
- `recommended_prompt_language`: `ko | en | any`
- `prompt_languages`: 실제 관리하는 프롬프트 언어 목록
- `tags`: 검색용 태그(선택)

## 핵심 설계 원칙

이미지 편집 프롬프트에서는 가능한 한 작업을 다음 두 요소로 분리합니다.

1. **Variable** — 이번 편집에서 실제로 바꿀 요소
2. **Invariant / Lock** — 절대로 바꾸면 안 되는 요소

특히 한 요소만 변경하는 작업에서는 모델이 주변 요소를 재해석하지 못하도록 변경 범위를 명시적으로 좁힙니다.

## ID 권장 형식

파일 경로가 주 taxonomy 역할을 하므로 ID는 짧고 안정적으로 유지합니다.

- `IMG-EDIT-001`
- `IMG-GEN-001`
- `MUS-SUNO-001`
- `VID-LOOP-001`

세부 분류는 디렉터리와 metadata를 사용합니다.
