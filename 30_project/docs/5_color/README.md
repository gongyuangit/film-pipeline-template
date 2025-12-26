# Color QC/Review Workbench

该阶段不生产素材，仅对已合成镜头进行机器可量化的颜色一致性/QC 判断与报告。它共享视觉的 shot_map 与 timeline 事实（`30_project/docs/2_layout/_artifacts/editing_bridge/shot_map_v1.srt`, `timeline_plan_v1.xml`），并在完成后向 `final_picture_path.txt` / `markers_plan_v1.yaml` 提供清单以供后续交付。

## 输入
- `final_picture_path.txt` 用于记录当前的最终合成路径或镜头序列说明，可为空。
- 可选的 `reference_frames/` 目录存放参考截图或色卡。

## 输出
- `_artifacts/reports/color_qc_v1.md`：包含曝光/色温/饱和度/噪点等可量化 QC 清单与建议动作（P0/P1/P2）。
- `_artifacts/reports/color_review_v1.md`：汇总 QC 结论并说明哪些镜头需返工，必须通过 `COLOR_REVIEW_APPROVED` 才能进入最终交付/导出阶段。
- `_artifacts/exports/markers_plan_v1.yaml`：记录需要调色的镜头/时间码供 XML 反写。

## Gate
- 所有 color 产出遵守 stop→go→stop：每阶段结束后在 `00_human/INBOX.md` 写 pending，等待 `COLOR_QC_APPROVED` / `COLOR_REVIEW_APPROVED`。
- 该阶段尽量不阻塞视觉/音频并行工作，但任何最终交付都必须等待 `COLOR_REVIEW_APPROVED`。
