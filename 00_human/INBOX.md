# INBOX
| ID | Status | Description | 备注 |
| -- | -- | -- | -- |
| 1 | pending | 请确认 `00_human/` 现在是唯一面向人工的入口点，再继续非交互式工作。 |  |
| 2 | pending | 项目核心移至 `30_project/`；生成内容前需要一个项目入口（如 `30_project/inputs/index.yaml` 或类似的清单），包含项目名称、所需文档与约束。 |  |

## 【素材检测 / 启动前状态】
<!-- inputs-detection:start -->
**状态**：pending  
**说明**：尚未检测到 `30_project/inputs/` 下的素材，请在以下路径添加相应内容后重新运行 `make check-inputs`。`index.yaml` 可选但不再作为启动阻塞。

| 内容名称 | 是否必需 | 放置路径 | 简短备注 |
| 剧本/脚本 | 必需 | `30_project/inputs/script/` | 提供完整脚本或文本（如 `script.pdf`, `剧本.md`），包含镜头/对白/节奏 |
| 分镜/故事板 | 必需 | `30_project/inputs/storyboard/` | 提供分镜或视觉概念文件，标注镜头编号与时长参考 |
| 拍摄/视觉参考 | 必需 | `30_project/inputs/reference/` | 放置关键参考图、参考片段说明（支持 `.jpg`, `.png`, `.txt` 等） |
| 素材/已有镜头 | 可选 | `30_project/inputs/assets/` | 若已有素材片段，可放入此目录并保持可读格式（如 `mp4`, `mov`） |
<!-- inputs-detection:end -->
