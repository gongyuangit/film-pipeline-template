# PRODUCTION

- 目前无其它制片约束。

## DaVinci Editing Bridge Notes

- DaVinci 时间线起点为 `01:00:00:00`，planning SRT (`_artifacts/shot_map_v1.srt`) 以此为基础输出，并在 `00_human/INBOX.md` 中标记需要人工确认。
- 所有素材重命名/路径调整/时间线重连动作，必须同速生成 `rename_plan_v1.yaml`、`timeline_updated.xml` 与 `asset_manifest_v1.yaml`，以明确旧镜头与新素材之间的对应关系。
- 镜头与素材的多对多关系是允许的；真相以 XML 时间线为准，命名仅为整理标签；如需策略性调整，可在 `_artifacts/editing_bridge/notes.md` 记录辅助决策。
