# Layout Phase Directory

`_artifacts/` 是 layout 阶段产出与归档的唯一区域，所有 cinematic intent / prompt pack / Blender token 文件都必须保存在 `_artifacts/inputs/`、`_artifacts/prompt_packs/`、`_artifacts/reports/` 等子目录中；`reports/` 用于留存分析与检查报表。

`CURRENT.yaml` 记录被批准的 cinematic intent 版本路径与编号（现在指向 `_artifacts/inputs/2-1_cinematic_intent_v1.yaml`），任何下游生成目标必须以该指针为起点，并通过 `APPROVALS.md` 中的 gate 才能继续。

## DaVinci Editing Bridge Rules

### 硬约束（必须遵守）
- DaVinci 时间线起点固定为 `01:00:00:00`；`_artifacts/editing_bridge/shot_map_v1.srt` 和 `_artifacts/editing_bridge/timeline_plan_v1.xml` 均以该时码为基准输出，内部可用帧 0 进行计算（fps 默认 24）。
- 编辑/素材重命名或路径变更，必须同时生成下列 `_artifacts/editing_bridge/` 产物：
  - `rename_plan_v1.yaml`：记录旧路径 → 新路径映射。
  - `timeline_updated.xml`：可被 DaVinci 重新导入的更新后的 XML。
  - `asset_manifest_v1.yaml`：映射镜头区间（shot id / TC）到实际素材使用情况。
- 真相以最新的 XML 时间线为准；文件名仅是标签或整理工具，不能替代时间线事实。

### 策略项（可选方式）
- 镜头与素材可呈多对多关系；素材命名与镜头可能错位，只要有对应说明，不阻塞流程。
- `timeline_in.xml` 用作当前素材接管的参考，`notes.md` 记录对接过程中的辅助提示或异常说明。
- 如果对素材归档进行版本化，可在 `editing_bridge/` 增加版本化文件，但必须同步更新 manifest 与 approvals。

### 轨道映射约定
- Layout 轨道：`V4` = layout_master，`V1/V2/V3` = layout_candidates。
- Lookdev 轨道：`V8` = lookdev_master，`V5/V6/V7` = lookdev_candidates。
- 轨道可以多对多：一个镜头可覆盖多个素材、一个素材可跨多个镜头；允许镜头为空，轨道上的素材可以是视频或静态图。

`_artifacts/editing_bridge/` 中的所有文件都属于 layout 产物；更新它们须同步更新 `CINEMATIC_INTENT_APPROVED` 及 `SHOT_MAP_SRT_XML_APPROVED` 之类的 gates，保持 stop→go→stop 的节奏。

## Lookdev Prompt Guidance

- Lookdev prompt packs, reviews, and exports now live under `30_project/docs/3_lookdev/_artifacts/`; this layout README covers the remaining layout prompt packs only.

- Layout prompt pack（如 `_artifacts/prompt_packs/branch1_segment_prompt_pack_v1.yaml` / `_artifacts/prompt_packs/branch2_shot_prompt_pack_v1.yaml`）聚焦镜头逻辑、镜头语言与叙事节奏，源自 cinematic intent 与 layout freeze 输出；它们的逻辑是“如何用镜头呈现叙事”。
- Lookdev shot prompt pack (`_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml`) 则侧重镜头画面风格、材质与灯光预期，其信息源必须包含 cinematic intent 与 `reports/layout_review_v1.md` 中的验收反馈（问题清单 + 通用教训 + lookdev 补丁），目的是帮助 lookdev 团队在镜头构图基础上决策材质调性。

### Lookdev Review Requirement

- Lookdev 阶段完成镜头提示词后，必须生成 `reports/lookdev_review_v1.md` 验收报告，并将其作为后续 execution / render 参考；未获得 `LOOKDEV_REVIEW_APPROVED`，不得开始执行计划或 render 相关流程。
- `lookdev_review_v1.md` 同样按镜头列出问题、教训与执行建议，它与 cinematic intent + layout review 等资料共同构成 downstream 的输入集合，用于排查材质、色彩、光照等一致性问题。
- Lookdev Review 的评估标准来自 `10_codex/STANDARDS_LOOKDEV.md`，每条登记需对应材质/光照/色彩一致性之一并说明严重度与建议，报告中的问题清单必须覆盖这三个维度。

## Prompt Pack Convention

- 所有 prompt pack 必须包含 `globals.negative`（全局负向提示词）与 `shots[]`（正向/负向提示词按镜头分组），其中 `shots[].positive` 构成镜头正向提示，`shots[].negative` 用以添加该镜头特有的负向提示；整体生效的负向提示可以理解为 `negative_effective = globals.negative + shots[].negative`。
- `globals.negative` 适合覆盖项目级别的“不要做”，例如“避免logos/文字/低分辨率”。每个镜头的 `shots[].negative` 用于针对特定镜头的约束，例如“远景不加特写光”，也可以保持空列表，如果镜头没有额外负向需求。
- Lookdev prompt pack 的结构与 Layout prompt pack 一致，但它的 `shots[].positive` 会进一步聚焦材质、灯光、色彩，而不是叙事逻辑，必须以 layout review 的反馈为支撑。
- `exports/` 目录（如 `_artifacts/exports/layout_markers_v1.yaml`）用于把需要 deliver 的镜头/时间码写成 marker 清单，供达芬奇编辑/调色参考，也便于将信息写回 XML。
