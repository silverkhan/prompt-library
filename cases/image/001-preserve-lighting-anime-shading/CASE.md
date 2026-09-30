---
case_id: CASE-IMG-001
status: VERIFIED
related_prompt: IMG-EDIT-001
verified_at: 2026-09-30
model_family: chatgpt-image
---

# Case 001 — 광원은 유지하고 음영 표현만 애니메이션풍으로 전환

## 배경

엘프 여성 캐릭터의 초상 이미지에서 원하는 광원의 방향을 먼저 확정한 뒤, 결과를 검토하자 음영 표현이 지나치게 실사적으로 변한 문제가 발생했습니다.

목표는 이미 확정된 **빛의 방향과 그림자 위치를 그대로 유지하면서**, 음영의 렌더링 언어만 기존의 고급 애니메이션 일러스트 계열로 되돌리는 것이었습니다.

## 최종 목표

### 유지해야 하는 것

- 동일 캐릭터
- 얼굴 identity
- 동일한 포즈와 구도
- 동일한 헤어
- 동일한 의상 및 장신구
- 동일한 배경
- 동일한 광원 방향
- 동일한 밝은 면 / 어두운 면
- 동일한 하이라이트 위치
- 동일한 그림자 위치

### 변경해야 하는 것

오직:

- 음영 표현 방식
- 피부의 tonal transition
- 얼굴 면의 렌더링 언어

반실사/실사적 shading을 하이엔드 애니메이션 illustration shading으로 변경합니다.

## 시행착오

### 실패 1 — 광원 방향 변경과 스타일 변경을 동시에 수행

광원의 방향과 그림체를 한 번에 수정하도록 하자 모델이 캐릭터와 렌더링을 넓게 재해석했습니다.

**교훈**

광원 수정과 스타일 수정은 가능한 한 별도 단계로 분리합니다.

---

### 실패 2 — "정면광"을 강하게 강조

정면광을 요구하는 과정에서 모델이 이를 frontal fill / beauty lighting에 가깝게 해석하여 기존 form shadow가 거의 사라졌습니다.

**교훈**

카메라 방향에서 들어오는 directional key light와 fill light는 분리해서 기술해야 합니다.

광원을 바꾸는 작업에서는:

- ambient/fill 증가 금지
- form shadow 유지
- surface orientation에 따른 밝기 차이 유지

를 함께 명시해야 합니다.

---

### 실패 3 — 광원은 맞았지만 음영이 실사화됨

카메라 축 방향의 광원은 원하는 위치에 도달했지만, 그림자의 경계와 피부 면 모델링이 실사/반실사 렌더링처럼 바뀌었습니다.

이 시점부터 작업 목표가 달라졌습니다.

더 이상 relighting 작업이 아니라:

> **광원과 shadow topology를 lock하고 shading language만 변경**

하는 작업이 되었습니다.

---

### 성공 — Relighting을 명시적으로 금지하고 shading만 Variable로 지정

성공 프롬프트의 가장 중요한 문장은 다음입니다.

```text
This is NOT a relighting task.
```

그리고 다음 요소를 명시적으로 고정했습니다.

```text
Do NOT change the light direction.
Do NOT change the placement of highlights.
Do NOT change the placement of shadows.
Do NOT recalculate the lighting.
```

변경 범위는 하나로 제한했습니다.

```text
Change ONLY the shading/rendering style.
```

이 조합을 통해 광원 방향과 그림자 배치는 유지되면서 음영 표현 방식만 하이엔드 애니메이션풍으로 전환된 만족스러운 결과를 얻었습니다.

## 왜 성공했는가

이 사례의 핵심은 프롬프트를 "원하는 스타일 설명" 중심으로 작성하지 않고 **Variable과 Invariant를 분리한 것**입니다.

### Invariant

- lighting
- highlight placement
- shadow placement
- identity
- composition
- color
- design

### Variable

- shading/rendering style

모델이 변경할 수 있는 자유도를 한 요소로 제한한 것이 성공에 크게 기여한 것으로 판단합니다.

## 재사용 지침

다음과 같은 요청에 우선 적용합니다.

> "지금 빛과 그림자는 좋은데 피부가 너무 실사 같다."

> "광원은 절대 건드리지 말고 애니메이션처럼 음영만 정리해라."

> "얼굴과 구도는 그대로 두고 렌더링만 반실사에서 애니풍으로."

반대로 사용자가 광원 자체를 변경하려는 경우에는 이 프롬프트를 사용하지 않고 relighting 전용 프롬프트를 사용합니다.

## 검증 프롬프트

- `image/editing/shading/preserve-lighting-anime-shading.md`
