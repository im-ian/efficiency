# Graph Engineering Skill (`ge`)

태스크를 받아 **prompt → loop → graph** 계층을 판단하고, 그래프가 필요하면 agent / validator / merge / human 노드로 구성된 work graph(DAG)를 설계·실행하는 오케스트레이터 프롬프트입니다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| `PROMPT.md` | 핵심 프롬프트 (단일 소스). 그래프 스펙 계약 + 실행 프로토콜 |
| `SKILL.md` | Claude Code / Codex 공용 스킬 래퍼 (PROMPT.md 를 읽어 적용) |
| `scripts/test.py` | 그래프 JSON 검증기 (스키마·DAG·artifact 전달·entry/exit 체크) |

## 설치

이 폴더를 양쪽 스킬 디렉토리에 symlink 하면 끝. 원본 하나만 수정하면 양쪽에 반영됩니다.

```bash
git clone https://github.com/im-ian/graph-engineering.git
cd graph-engineering

# Claude Code → /ge
ln -s "$PWD" ~/.claude/skills/ge

# Codex → $ge
ln -s "$PWD" ~/.codex/skills/ge
```

설치 후 **새 세션**에서 스킬이 인식됩니다.

## 사용법

```
# Claude Code
/ge 경쟁사 5곳 리서치하고, IA 설계해서 내 승인 받은 뒤, SEO 통과하는 포스트 3개 써줘

# Codex
$ge 경쟁사 5곳 리서치하고, IA 설계해서 내 승인 받은 뒤, SEO 통과하는 포스트 3개 써줘
```

- 태스크에 `PLAN ONLY` 를 포함하면 그래프 설계(JSON + mermaid)까지만 하고 실행하지 않습니다.
- 단순한 태스크는 그래프를 만들지 않고 `LAYER: prompt` 또는 `LAYER: loop` 로 바로 처리합니다.
- 명시적 호출(`/ge`, `$ge`) 외에 자연어로도 트리거됩니다: "그래프로 설계해줘", "에이전트 병렬로 나눠서", "역할 나눠서 병렬 진행", "검증 게이트 넣어서", "orchestrate this as a graph", "split into parallel agents" 등.

## 그래프 검증 (수동)

에이전트가 출력한 그래프 JSON 을 직접 검증하려면:

```bash
python3 scripts/test.py graph.json    # 또는 에이전트 출력 전체를 stdin 으로 파이프
```

체크 항목: 노드 id 중복, 노드 타입, validator 의 `on_fail`, 엣지가 실어 나르는 artifact 가 from-노드 outputs 에 존재하는지, entry/exit 정합성, 사이클(DAG) 여부.

## 동작 개요

1. **계층 판단** — 모델 호출 1번이면 prompt, 단일 에이전트 루프면 loop, 병렬 브랜치·역할 분리·검증 게이트·human 승인 필요하면 graph.
2. **그래프 설계** — 노드(id/type/role/prompt/outputs) + 엣지(from/to/carries/when) JSON. 컨텍스트는 엣지가 실어 나르는 artifact 로만 노드 경계를 넘음.
3. **실행** — ready 노드 병렬 실행, `RUN:` 로그, validator 실패 시 critique 붙여 producer 재실행(최대 retry 후 escalate/abort), 필요 시 `GRAPH-EDIT:` 로 노드 추가/제거, 완료 시 RUN LOG + `FINAL:` artifact 출력.
