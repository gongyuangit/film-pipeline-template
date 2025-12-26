# Audio Phase Directory

`_artifacts/` 是音频阶段的产物区，所有规划、提示词和验收文件都必须保存在此处，目录内结构与视觉 layout 平行。音频阶段依赖 `30_project/docs/2_layout/_artifacts/editing_bridge/shot_map_v1.srt` 与 `timeline_plan_v1.xml` 共享镜头容器/时间线真相。

## Stop→Go→Stop
- Audio Plan/Prompts/Review 同样遵守 stop→go→stop 节奏，每个阶段完成后都必须在 `00_human/INBOX.md` 记录 pending 并等待对应审批（`AUDIO_PLAN_APPROVED` / `AUDIO_PROMPTS_APPROVED` / `AUDIO_REVIEW_APPROVED`）。
- 这些审批不会阻塞视觉流水线，视觉审批也不会阻塞音频阶段。

## Prompt Packs
- 所有音频 prompt pack（dialogue VO / SFX / Music）必须包含 `globals.negative` 与 `items[]`（正向/负向提示），并按以下合成方式生效：`negative_effective = globals.negative + items[].negative`。
- Dialogue VO 与 SFX pack 按 shot_id 列表组织，Music pack 按 segment/scene/beat id 组织。

## DaVinci 音轨约定
- DaVinci timecode 起点为 `01:00:00:00`，fps 默认 24。音频资产以 `timeline_plan_v1.xml` + `timeline_updated.xml` 为事实依据，允许多对多（一个镜头多个片段 / 一个片段跨多个镜头 / 镜头可为空）。
- 重命名、素材移动或时间线重连必须同时产出 `timeline_updated.xml`、`rename_plan_v1.yaml`、`audio_asset_manifest_v1.yaml`。
- 轨道编号约定（仅编号）：Dialogue/VO → master `A4`（候选 `A1-A3`），SFX → master `A8`（候选 `A5-A7`），Music → master `A12`（候选 `A9-A11`）。
- 不依赖轨道名，仅依赖编号 + SRT 时间段 + XML 片段段落。
