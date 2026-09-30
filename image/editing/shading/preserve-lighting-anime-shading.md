---
id: IMG-EDIT-001
title: 광원 유지 + 애니메이션 음영 스타일 변환
status: VERIFIED
category: image-editing
task: shading-style-transfer
model_family: chatgpt-image
verified_at: 2026-09-30
recommended_prompt_language: en
prompt_languages:
  - ko
  - en

locks:
  identity: true
  composition: true
  lighting: true
  shadow_placement: true
  highlight_placement: true
  colors: true

variables:
  - shading_rendering_style
---

# 광원 유지 + 애니메이션 음영 스타일 변환

기존 이미지의 캐릭터, 구도, 광원 벡터, 하이라이트 및 그림자의 **위치**는 그대로 유지하면서, 음영을 표현하는 **렌더링 언어만** 반실사/실사풍에서 하이엔드 애니메이션 일러스트풍으로 바꾸기 위한 프롬프트입니다.

## 핵심 개념

이 작업은 **Relighting이 아닙니다.**

바뀌는 것은:

- 그림자의 위치가 아니라 그림자를 표현하는 방식
- 광원의 방향이 아니라 톤과 면을 정리하는 방식
- 얼굴 구조가 아니라 렌더링 언어

즉:

> **Lighting topology는 고정하고 shading language만 변경한다.**

## 적용 범위

### 잘 맞는 용례

- 반실사 캐릭터의 음영만 애니메이션풍으로 정리
- 이미 만족스러운 광원 방향을 그대로 보존
- 얼굴/의상/배경을 재디자인하지 않고 렌더링 감각만 변경
- 기존 이미지의 3차원 볼륨을 유지하면서 피부의 실사적 모델링을 줄이는 작업

### 피해야 할 용례

- 광원의 방향 자체를 바꾸려는 작업
- 그림자 위치를 새로 계산해야 하는 작업
- 캐릭터 디자인 변경
- 구도/포즈 변경
- 완전히 다른 화풍으로 대규모 스타일 전환

이 경우 각각 별도의 전용 프롬프트를 사용해야 합니다.

## 변경 대상

**오직 다음 요소만 변경합니다.**

- shading / rendering style
- tonal transition의 표현 방식
- facial plane의 스타일화 정도
- 실사적 피부 모델링의 강도

## 고정 대상

- Character identity
- 얼굴형과 이목구비
- 헤어스타일과 머리카락 흐름
- 의상과 장신구
- 배경
- 구도와 크롭
- 색상
- 광원의 방향
- 밝은 면 / 어두운 면의 위치
- 하이라이트 위치
- 그림자 위치

## 프롬프트 전송 권장 언어

**권장: 영문**

현재 검증된 성공 사례가 영문 프롬프트를 직접 전송했을 때 얻어진 결과이므로, 재현성을 우선할 경우 아래 영문 버전 사용을 권장합니다.

한글 버전은 의미 확인, 수정 및 파생 프롬프트 작성용으로 함께 관리합니다.

## 프롬프트 — 한글

```text
첨부한 이미지를 직접 편집하라.

이 작업은 리라이팅 작업이 아니다.
빛의 방향을 바꾸지 마라.
하이라이트의 위치를 바꾸지 마라.
그림자의 위치를 바꾸지 마라.
조명을 다시 계산하지 마라.

다음 요소를 정확히 유지하라:
- 현재의 광원 방향
- 현재의 그림자 구조
- 현재의 하이라이트 위치
- 캐릭터 정체성
- 얼굴, 눈, 코, 입술, 귀
- 헤어스타일과 머리카락 흐름
- 의상, 장신구, 배경
- 구도, 크롭, 색상 및 전체 디자인

오직 음영/렌더링 스타일만 변경하라.

목표:
동일한 조명 설정과 동일한 그림자 패턴을 유지하면서,
현재의 반실사적/실사적 모델링 방식만
하이엔드 애니메이션 일러스트 스타일로 변환한다.

음영 스타일 방향:
- 보다 애니메이션적인 톤 처리
- 더 깨끗하고 의도적으로 설계된 그림자 형태
- 사진 같은 피부 렌더링보다 부드러운 페인터리 애니메이션 렌더링
- 형태 전환을 약간 단순화
- 우아하게 스타일화된 얼굴 면
- 깊이감은 유지하되 실사적인 피부 모델링은 감소
- 프리미엄하고 정제되며 시네마틱한 인상 유지
- 입체감은 유지하되 애니메이션 일러스트의 시각 언어로 표현

중요:
- 같은 광원 벡터와 같은 그림자 방향을 유지하라
- 얼굴의 밝은 면과 어두운 면을 그대로 유지하라
- 빛을 받는 면과 그림자 면의 위치를 그대로 유지하라
- 얼굴을 평면적으로 만들지 마라
- 그림자를 제거하지 마라
- 그림자를 이동시키지 마라
- 새로운 림라이트나 새로운 정면광을 추가하지 마라
- 실사처럼 보이게 만들지 마라
- 캐릭터를 재디자인하지 마라
- 구도를 변경하지 마라

최종 이미지는 캐릭터, 포즈, 구도, 광원 방향 면에서 원본과 거의 동일해야 하며,
음영 표현 방식만 실사적 렌더링이 아니라 정제된 하이엔드 애니메이션 일러스트처럼 느껴져야 한다.
```

## Prompt — English

```text
EDIT THE ATTACHED IMAGE DIRECTLY.

This is NOT a relighting task.
Do NOT change the light direction.
Do NOT change the placement of highlights.
Do NOT change the placement of shadows.
Do NOT recalculate the lighting.

Preserve exactly:
- the current direction of light,
- the current shadow structure,
- the current highlight locations,
- the character identity,
- face, eyes, nose, lips, ears,
- hairstyle and hair flow,
- costume, jewelry, background,
- composition, crop, colors, and overall design.

Change ONLY the shading/rendering style.

Goal:
Keep the same lighting setup and the same shadow pattern,
but convert the current shading treatment from semi-realistic / realistic modeling
into a high-end animation illustration style.

Shading style direction:
- more animation-style tonal treatment
- cleaner and more designed shadow shapes
- softer painterly anime rendering rather than photographic skin rendering
- slightly simplified form transitions
- elegant stylized facial planes
- preserve depth, but reduce realistic skin-like modeling
- keep the image premium, refined, and cinematic
- maintain dimensionality, but express it in anime illustration language

Important:
- Keep the same light vector and same shadow direction
- Keep the same bright side and dark side of the face
- Keep the same illuminated planes and shadowed planes
- Do NOT flatten the face
- Do NOT remove shadows
- Do NOT move shadows
- Do NOT introduce a new rim light or new frontal light
- Do NOT make it look photorealistic
- Do NOT redesign the character
- Do NOT alter the composition

Result:
The final image should look almost identical in character, pose, composition,
and lighting direction, but the shading should feel like a refined high-end
anime illustration rather than realistic rendering.
```

## 사용 방법

1. 이미 광원 방향과 명암 배치가 만족스러운 원본 이미지를 첨부합니다.
2. 위 프롬프트를 이미지 편집 요청으로 사용합니다.
3. 결과에서 먼저 광원 방향과 그림자의 위치가 유지되었는지 확인합니다.
4. 그 다음 피부/얼굴/머리카락의 음영이 실사적 모델링에서 애니메이션적 렌더링으로 바뀌었는지 확인합니다.
5. 광원이 바뀌었다면 스타일 세부 조정보다 먼저 해당 결과를 실패로 판단합니다.

## 성공 판정 기준

- 광원 방향이 원본과 동일함
- 밝은 면과 어두운 면이 뒤집히지 않음
- 주요 그림자 위치가 유지됨
- 캐릭터 얼굴 identity가 유지됨
- 구도/의상/장신구가 실질적으로 동일함
- 음영의 면 정리와 tonal transition만 애니메이션풍으로 바뀜
- 실사 피부처럼 보이지 않으면서 입체감은 남아 있음

## 알려진 실패 패턴

### "Anime style"만 지시

스타일 변경 범위가 너무 넓어 얼굴, 헤어, 조명까지 다시 디자인될 수 있습니다.

### Relighting 지시가 동시에 존재

음영 스타일을 바꾸면서 광원 관련 지시까지 포함하면 모델이 light vector까지 다시 계산할 수 있습니다.

### 그림자 제거

"정면광", "soft beauty lighting", "even lighting" 같은 표현이 섞이면 form shadow가 사라지거나 얼굴이 평면화될 수 있습니다.

