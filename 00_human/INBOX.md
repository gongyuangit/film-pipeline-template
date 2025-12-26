# INBOX
| ID | Status | Description | 备注 |
| -- | -- | -- | -- |
| 1 | pending | 请确认 `00_human/` 现在是唯一面向人工的入口点，再继续非交互式工作。 |  |
| 2 | pending | 项目核心移至 `30_project/`；生成内容前需要一个项目入口（如 `30_project/inputs/index.yaml` 或类似的清单），包含项目名称、所需文档与约束。 |  |
| 3 | pending | 已依据现有剧本文本生成 `30_project/docs/1_story/script_breakdown_v1.yaml` 的第一版骨架，必须人工确认后方可进入 Stage C；分镜/参考只是建议，可选。 |  |
| 4 | done | `30_project/docs/1_story/` 已清理为仅保留 `script_breakdown_v1.yaml` 与 `1-2_segment_structure.yaml`，其余原始脚本/拆解文件移除。 |  |
| 5 | done | `script_breakdown_v1.yaml` 已补齐场次与镜头层（segment→beat→shot），成为 Stage B 的唯一主产物。 |  |

## 【素材检测 / 启动前状态】
<!-- inputs-detection:start -->
**状态**：pending  
**说明**：尚未检测到 `30_project/inputs/` 下的素材，请在以下路径添加相应内容后重新运行 `make check-inputs`。`index.yaml` 可选但不再作为启动阻塞。

| 内容名称 | 是否必需 | 放置路径 | 简短备注 |
| 剧本/脚本 | 必需 | `30_project/inputs/script/` | 提供完整脚本或文本（如 `script.pdf`, `剧本.md`），包含镜头/对白/节奏 |
| 分镜/故事板 | 可选（建议） | `30_project/inputs/storyboard/` | 可补充已有分镜或视觉概念，但非阻塞 |
| 拍摄/视觉参考 | 可选（建议） | `30_project/inputs/reference/` | 提供参考图或片段说明，可增视觉灵感 |
| 素材/已有镜头 | 可选 | `30_project/inputs/assets/` | 若已有素材片段，可放入此目录并保持可读格式（如 `mp4`, `mov`） |
<!-- inputs-detection:end -->

## 【可选素材建议】
- 当前流程可仅依赖剧本发起，分镜与参考均为可选补充，若有现成可直接放入上述路径供参考。
- 若暂未提供分镜或参考，可在 `00_human/INBOX.md` 中以 `Status: pending` 形式记录“建议”信息，待人类反馈再决定是否需要加入。
