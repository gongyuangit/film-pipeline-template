# Template Structure Index

## A. Directory tree (depth ≤3)
- `00_human`
- `10_codex`
  - `10_codex/tools`
    - `10_codex/tools/__pycache__`
- `30_project/docs`
  - `30_project/docs/0-source`
    - `30_project/docs/0-source/parsed`
    - `30_project/docs/0-source/raw`
  - `30_project/docs/1_story`
  - `30_project/docs/2_audio`
    - `30_project/docs/2_audio/_artifacts`
  - `30_project/docs/2_layout`
    - `30_project/docs/2_layout/_artifacts`
  - `30_project/docs/3_lookdev`
    - `30_project/docs/3_lookdev/_artifacts`
  - `30_project/docs/4_edit`
    - `30_project/docs/4_edit/_artifacts`
  - `30_project/docs/5_color`
    - `30_project/docs/5_color/_artifacts`
  - `30_project/docs/meta`
- `20_runtime`
  - `20_runtime/exec`
  - `20_runtime/final`
  - `20_runtime/plan`
  - `20_runtime/tests`
    - `20_runtime/tests/segment_story`

## B. Purpose table

| Path | Owner | Purpose | Lifecycle | Notes |
| -- | -- | -- | -- | -- |
| 00_human/INBOX.md | Human | All-gate board | Regenerated via preflight | Shows each stage in PIPELINE_STAGES |
| 00_human/NOW.md | Human | Actionable gate list | Regenerated via preflight | Empty in template mode |
| 00_human/APPROVALS.md | Human | Approvals unlock gates | Manual edits only | Approvals are sole source of approved status |
| 10_codex/PIPELINE_STAGES.yaml | Codex | Defines gate order/prereqs/products | Updated with new stages | Drives dashboards |
| 10_codex/TEMPLATE_MANIFEST.yaml | Codex | Structure manifest | Preflight enforces listed entries | Includes placeholders |
| 10_codex/tools/preflight.py | Codex | Preflight / dashboards | Run before other flow | Loads manifest/stages and checks template index |
| 30_project/inputs/index.yaml | Human | project_mode switch | Default template, change to project | Keeps NOW empty until project mode |
| 30_project/docs/0-source/ | Codex | Source fragments + registry | Feeds Stage S | raw/ -> structured shards |
| 30_project/docs/1_story/script_breakdown_v1.yaml | Codex | Script breakdown | Feeds layout/audio | Placeholder until populated |
| 30_project/docs/2_layout/_artifacts/ | Codex | Layout/lookdev artifacts | All layout outputs live here | Includes editing_bridge + CURRENT pointer |
| 30_project/docs/3_lookdev/_artifacts/ | Codex | Lookdev prompt pack + reports | Feeding lookdev gates | Hosts prompt pack + lookdev review |
| 30_project/docs/2_audio/_artifacts/ | Codex | Audio planning + prompts + review | Parallel to layout | Shares editing_bridge facts |
| 30_project/docs/5_color/_artifacts/ | Codex | Color QC + review | After exec plan | Editing bridge anchors XML/SRT |
| 20_runtime/ | Codex | Runtime/cache skeleton | Cache only, never committed outputs | Holds plan/exec/tests/final folders with `.gitkeep` placeholders |

## C. Key rules
- Approvals only come from `00_human/APPROVALS.md`; artifacts never auto-approve.
- In `project_mode: template`, artifact_ready is forced false (outside whitelist) and NOW shows a reminder.
- `TEMPLATE_PLACEHOLDER: true` + `content_nontrivial` heuristics guard readiness for YAML/MD/SRT/XML/JSON inputs.
- XML/SRT files represent timeline facts; trust track IDs and durations, not track names, and keep them under `_artifacts/editing_bridge/`.
- Every generated product must live inside the stage’s `_artifacts/` directory; layout uses `CURRENT.yaml` as the pointer.
- Lookdev prompt packs and reports live under `30_project/docs/3_lookdev/_artifacts/` to keep the stage boundaries explicit.
- `20_runtime/` is an ephemeral cache (plan/exec/tests/final); files inside are regenerated and may be cleared at will.

## D. No-drift rules
- New stages must sync `PIPELINE_STAGES.yaml`, `TEMPLATE_MANIFEST.yaml`, dashboards (INBOX/NOW), and `preflight.py` gating logic.
- Every required file/directory must be listed in `TEMPLATE_MANIFEST.yaml`; preflight recreates placeholders when missing.
- Any structural change must document updates in `10_codex/TEMPLATE_INDEX.md` and, if archiving content, record it in the migration log.
