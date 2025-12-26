# 0-source 碎片事实仓库

- 目录聚焦零散事实输入，用于 Source Synthesis 阶段。
- `raw/` 是人类提供碎片事实（文本、表格、截图说明）的唯一入口；不要直接把碎片丢到其他目录。
  - `raw/structured/` 存放人工整理的高质量 source 片段（原 0_source 目录下的 0-*.yaml），Stage S 应优先解析与引用。
  - `parsed/` 存放每个碎片解析后的标准文本，供下游复用。
  - `registry.yaml` 记录每个碎片的 fingerprint 与解析输出，控制增量解析与复用。
