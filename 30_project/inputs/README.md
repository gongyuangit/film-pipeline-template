# Inputs Index

- `index.yaml` 控制当前仓库运行模式：
  - `template`: 模板库模式（默认）—Codex 只能展示 gate、不会推动任何 stage；
  - `project`: 正式项目模式—复制模板后设为 `project`，才允许 `NOW.md` 显示可行动的 gate。
- 复制本模板到新项目后请务必修改 `project_mode` 才能进入生产流程。

其它 `30_project/inputs/` 下的目录保持可选，可按需要补充 `script/`、`storyboard/` 等素材。
