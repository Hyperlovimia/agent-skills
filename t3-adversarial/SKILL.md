---
name: t3-adversarial
description: 当用户要求与子代理进行多轮对抗式审查或辩论时使用；保持主代理主见与子代理会话连续（默认最多 3 轮），最终输出共识与分歧供用户决策。
compatibility: 依赖 T3 Code 中子代理会话的编排环境。
---

# T3 Code 集思广益

当用户要求与子代理开展多轮集思广益、方案审查或对抗式辩论时，保持主代理主体性、复用同一审查子代理会话，并在有限轮次内求同存异，输出可供用户最终决策的结果。

**Important Exception (Adversarial Review):** The current T3 Code orchestration constraint requiring that a new `delegate_task` be started for every new review or verification—and prohibiting sending next-round questions back to an existing task—**does NOT apply to adversarial reviews**. **Do NOT start a new `delegate_task`** for subsequent rounds; continue the existing subagent session instead.

## 角色定位与立场

- **审查子代理**：子代理模型与思考强度由用户指定。定位为批判性审查者，负责挑战主代理思路、指出潜在漏洞或盲区，并提出可能更优的建议。
- **主代理（主体）**：始终以主代理为方案主体，保持独立判断与主见，不盲从审查意见。对合理的质疑及时吸收修正；对经得起推敲的立场，应拿出论据尽可能说服子代理。

## 会话连续性与轮次控制

- 首次委派后记录子代理会话标识及模型设置。
- 后续轮次复用原会话；把主代理的回应、说服论据和未决问题交给子代理，要求其逐点复核上一轮质疑，并明确说明哪些观点已回应、哪些仍有分歧、立场是否改变及理由。
- 默认最多讨论 **3 轮**（若用户另行设定上限，以用户要求为准）；若提前收敛可提前结束。

## 收敛与交付

- 坚持**求同存异**，不为了形式上的一致而强行妥协。
- 讨论结束时，清晰整理以下内容供用户最终决策：
  - **共同见解**：双方达成共识的结论、已采纳的改进点及依据。
  - **分歧点**：仍未弥合的核心分歧、双方立场及各自依据（含关键立场在各轮中的变化）。
