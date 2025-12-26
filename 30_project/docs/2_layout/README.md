# Layout Phase Directory

`_artifacts/` 是 layout 阶段产出与归档的唯一区域，所有 cinematic intent / prompt pack / Blender token 文件都必须保存在此处，子目录 `_artifacts/reports/` 用于留存分析与检查报表。

`CURRENT.yaml` 记录被批准的 cinematic intent 版本路径与编号，任何下游生成目标必须以该指针为起点，并通过 `APPROVALS.md` 中的 gate 才能继续。
