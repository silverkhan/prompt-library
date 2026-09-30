# Prompt Catalog

> 이 파일은 `scripts/build_catalog.py`가 자동 생성합니다. 직접 수정하지 마십시오.

## 요약

- 총 프롬프트: **1**
- VERIFIED: **1**
- EXPERIMENTAL: **0**
- DEPRECATED: **0**

### 분야별

- 이미지: **1**

## 카탈로그

| ID | 분야 | 카테고리 | 작업 | 제목 | 상태 | 권장 언어 | 검증 모델 | 태그 |
|---|---|---|---|---|---|---|---|---|
| IMG-EDIT-001 | 이미지 | image-editing | shading-style-transfer | [광원 유지 + 애니메이션 음영 스타일 변환](image/editing/shading/preserve-lighting-anime-shading.md) | VERIFIED | 영문 | chatgpt-image | - |

## 메타데이터 규칙

- `status`: `VERIFIED`, `EXPERIMENTAL`, `DEPRECATED` 중 하나
- `recommended_prompt_language`: `ko`, `en`, `any` 중 하나
- `VERIFIED`는 `verified_at`과 `model_family` 필수
- 권장 언어가 `en` 또는 `any`이면 한글/영문 프롬프트를 모두 포함
- 권장 언어가 `ko`이면 영문 프롬프트 생략 가능
