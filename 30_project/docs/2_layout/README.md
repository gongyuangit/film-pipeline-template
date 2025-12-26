# Layout Phase Directory

`_artifacts/` 是 layout 阶段产出与归档的唯一区域，所有 cinematic intent / prompt pack / Blender token 文件都必须保存在此处，子目录 `_artifacts/reports/` 用于留存分析与检查报表。

`CURRENT.yaml` 记录被批准的 cinematic intent 版本路径与编号，任何下游生成目标必须以该指针为起点，并通过 `APPROVALS.md` 中的 gate 才能继续。

## DaVinci Editing Bridge Rules

### 硬约束（必须遵守）
- DaVinci 时间线起点固定为 `01:00:00:00`；`_artifacts/shot_map_v1.srt` 需以该时码为基准输出，内部可使用帧 0 进行计算。
- 编辑/素材重命名或路径变更，必须伴随以下 `_artifacts/editing_bridge/` 产物：
  - `rename_plan_v1.yaml`：记录旧路径 → 新路径映射。
  - `timeline_updated.xml`：可被 DaVinci 重新导入的更新后的 XML。
  - `asset_manifest_v1.yaml`：映射镜头区间（shot id / TC）到实际素材使用情况。
- 真相以最新的 XML 时间线为准；文件名仅为便捷标签，不能替代时间线中的事实。

### 策略项（可选方式）
- 镜头与素材可呈多对多关系；素材命名与镜头可能错位，只要有对应说明，不阻塞流程。
- `timeline_in.xml` 用作当前素材接管的参考，`notes.md` 记录对接过程中的辅助提示或异常说明。
- 如果素材归档中出现更多版本，可在 `editing_bridge/` 增加版本化文件，但必须在 manifest 与 approvals 同步更新。

`_artifacts/editing_bridge/` 中的所有文件都属于 layout 产物；更新它们须同步更新 `CINEMATIC_INTENT_APPROVED` 及 `SHOT_MAP_SRT_APPROVED` 之类的 gates，保持 stop→go→stop 的节奏。
