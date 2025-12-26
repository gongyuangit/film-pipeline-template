# PRODUCTION

- 目前无其它制片约束。

## DaVinci Editing Bridge Notes

- DaVinci 时间线起点为 `01:00:00:00`，planning SRT (`_artifacts/editing_bridge/shot_map_v1.srt`) 与规划 XML (`_artifacts/editing_bridge/timeline_plan_v1.xml`) 以此为基础输出，并在 `00_human/INBOX.md` 中标记需要人工确认。
- 所有素材重命名/路径调整/时间线重连动作，必须同速生成 `rename_plan_v1.yaml`、`timeline_updated.xml` 与 `asset_manifest_v1.yaml`，以明确旧镜头与新素材之间的对应关系。
- 镜头与素材的多对多关系是允许的；真相以 XML 时间线为准，命名仅为整理标签；如需策略性调整，可在 `_artifacts/editing_bridge/notes.md` 记录辅助决策。
- Layout 轨道：`V4` = layout_master，`V1/V2/V3` = layout_candidates；Lookdev 轨道：`V8` = lookdev_master，`V5/V6/V7` = lookdev_candidates。
- Track 上的素材（视频或图片）与镜头之间允许多对多与错位，只要 XML 时间线能说明事实即可；`timeline_plan_v1.xml` 是规划版骨架，`shot_map_v1.srt` 的镜头顺序必须对应 XML 轨道 marker。
- Layout prompts（segment/shot prompt pack）依赖 cinematic intent + layout freeze 输出，关注结构、节奏与镜头逻辑；Lookdev prompts 则必须额外依赖 `reports/layout_review_v1.md` 中的验收反馈（按镜头问题清单 + 通用教训 + lookdev 输入补丁），用于指导材质、光效、细节层面的设计决策。
- Lookdev 阶段的最后一步必须生成 `reports/lookdev_review_v1.md` 验收报告，未获得 `LOOKDEV_REVIEW_APPROVED` 不得启动执行计划或向渲染/后期交付环节递交素材。
- 音频流水线平行运行，依赖同一 shot_map + timeline（`30_project/docs/2_layout/_artifacts/editing_bridge/shot_map_v1.srt` 与 `timeline_plan_v1.xml`），但拥有独立的 stop→go→stop gate。音频的素材/重命名操作亦需同步产生 `audio_asset_manifest_v1.yaml` / `rename_plan_v1.yaml` / `timeline_updated.xml`，并在 `00_human/INBOX.md` 发起对应 pending 请求。
- 调色阶段由机器执行可量化 QC（`color_qc_v1.md`），随后生成 `color_review_v1.md` 用于决定是否允许最终交付；`COLOR_REVIEW_APPROVED` 是所有最终交付（如 deliverables）前必过的闸门。
