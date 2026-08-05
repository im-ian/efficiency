# Efficiency

**한국어** | [English](README.en.md)

검증을 약화시키지 않으면서 복잡한 작업을 더 빠르게 처리하는 에이전트 워크플로 모음. `eff` 플러그인 하나로 Claude Code 와 Codex 에 독립 스킬들을 설치합니다.

## 왜 만들었나

기능을 상상해서 채운 모음이 아니라, 매일 에이전트와 작업하면서 반복해서 부딪힌 지점들을 하나씩 스킬로 굳힌 결과입니다.

- **`graph`** — 큰 작업을 매번 즉흥적으로 쪼개다 보니 검증 단계가 빠지거나 순서가 꼬였습니다. 실행 전에 구조를 먼저 확정하려고 만들었습니다.
- **`blitz`** — "파일이 겹쳐서 병렬로 못 합니다"라는 답을 너무 자주 들었습니다. 겹침은 병렬화 차단 사유가 아니라 머지 문제라서, 일단 나누고 나중에 합친 뒤 게이트로 검증하게 했습니다.
- **`toss`** — 오래 걸리는 작업 하나 때문에 세션 전체가 묶여 기다리는 게 아까웠습니다. 백그라운드로 넘기고 메인은 곧바로 다음 일을 하도록 만들었습니다.
- **`update-skills`** — 설치한 스킬이 언제 업데이트됐는지 몰라 오래된 버전을 계속 쓰고 있었습니다. 버전·변경점·토큰 증감을 표로 보고 골라서 올리게 했습니다.
- **`dedupe-skills`** — 스킬을 쌓다 보니 비슷한 스킬끼리 트리거를 뺏거나 서로 모순된 지시로 오동작했습니다. 겹침을 증거와 함께 찾아 정리까지 돕게 했습니다.
- **`prune-skills`** — 설치만 해두고 안 쓰는 스킬들이 매 세션 토큰만 태우고 있었습니다. 실제 사용 기록을 재서 죽은 스킬을 추려내게 했습니다.

## 스킬

| 스킬 | 용도 |
| --- | --- |
| `eff:graph` | 프롬프트 / 루프 / 그래프 실행 중 적합한 방식을 판단하고, 그래프가 필요할 때 에이전트·검증·머지·휴먼 노드로 구성된 검증된 DAG 를 오케스트레이션. |
| `eff:blitz` | 겹치는 작업을 격리된 병렬 슬라이스로 강제 분할하고, 의도 기준으로 머지한 뒤, 필수 검증 게이트를 통과. |
| `eff:toss` | 현재 진행 중인 작업을 백그라운드 서브 에이전트에게 넘기고 메인 세션은 즉시 다른 작업 가능; 종료 시 소요 시간·토큰·작업 요약 리포트. |
| `eff:update-skills` | 설치된 스킬들의 최신 버전을 확인해 변경점·버전·토큰 증감 표로 미리 보여주고, 사용자가 확정한 것만 업데이트. 실패 항목은 원인과 함께 리포트. |
| `eff:dedupe-skills` | 기능 중복·트리거 충돌·상호 모순·토큰 낭비 관점으로 겹치는 스킬을 증거와 함께 추려 제거를 권장하고, 확정된 항목만 정리 (disable 우선). |
| `eff:prune-skills` | 세션 기록에서 실제 사용량을 측정해 안 쓰는 스킬을 근거와 함께 추려내고, 확정된 항목만 정리 (disable 우선). |

스킬들은 설치 네임스페이스만 공유하고 프롬프트, 트리거, 동작 계약은 각각 독립적입니다.

## 설치

### Claude Code

Claude Code 세션에서 실행:

```text
/plugin marketplace add im-ian/efficiency
/plugin install eff@efficiency
```

호출:

```text
/eff:graph <task>
/eff:blitz <task>
/eff:toss <task>
/eff:update-skills
/eff:dedupe-skills
/eff:prune-skills
```

### Codex

터미널에서 실행:

```bash
codex plugin marketplace add im-ian/efficiency
codex plugin add eff@efficiency
```

새 세션 시작 후 호출:

```text
$eff:graph <task>
$eff:blitz <task>
$eff:toss <task>
$eff:update-skills
$eff:dedupe-skills
$eff:prune-skills
```

## 라이선스

MIT
