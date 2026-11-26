# Agent Skills

个人维护的 AI Agent Skills 与配套提示词集合，包含 **T3 Code 多代理协作协议**、**可视化表达规范**以及 **Codex 全局 `AGENTS.md`**。其中 Skills 支持通过 [CC Switch](https://github.com/farion1231/cc-switch) 直接导入与一键更新。

> **说明**：CC Switch 仅负责安装与同步 Skill 文件；各 Skill 所需的运行时工具（如线程编排、定时任务、HTML 渲染等）由对应的宿主客户端提供。

## 包含的 Skills

| Skill | 简介 | 运行环境要求 |
| :--- | :--- | :--- |
| [`t3-adversarial`](t3-adversarial/SKILL.md) | **T3 Code 集思广益**：与子代理进行多轮对抗式方案审查或辩论，保持主代理主见与子代理会话连续（默认最多 3 轮），最终输出共同见解与分歧点供用户决策。 | 依赖 T3 Code 中支持复用子代理会话的编排环境 |
| [`t3-secretary`](t3-secretary/SKILL.md) | **T3 Code 秘书模式**：双角色（秘书 + 项目经理）异步协作协议，按角色分流读取 SOP，涵盖需求对齐、派单、6 小时定时汇报、阻塞介入、完工验收与定时任务清理。 | 依赖 T3 Code 的线程与定时任务工具（`t3_thread_configure`、`t3_thread_launch`、`t3_thread_send`、`schedule_task`、`delete_scheduled_task` 等） |
| [`visualize`](visualize/SKILL.md) | **可视化表达（丰富图谱模式）**：使用内嵌 HTML 图谱与排版组件结构化呈现复杂逻辑、横向对比与密集信息；支持按需导出为 Obsidian Artifact Embed 代码块。 | 依赖宿主客户端的 HTML 渲染能力（T3 Code 下配合 `html_preview` / `html_render`；Obsidian 导出需安装 Artifact Embed 插件） |

### 各 Skill 简要说明

#### 1. `t3-adversarial`
- **适用场景**：需要让审查子代理以批判性视角多轮挑战当前方案、排查漏洞或进行结构化辩论。
- **核心机制**：首次委派后复用同一审查子代理会话（不另起新任务），主代理保持独立判断、逐轮回应并说服或修正，默认最多 3 轮，最后以**共同见解**与**分歧点**收尾。

#### 2. `t3-secretary`
- **适用场景**：长时、复杂任务的异步委托与跟进，将「面向用户的需求对齐与全局监理」和「面向执行的端到端研发交付」解耦。
- **核心机制**：
  - **秘书（[`references/secretary.md`](t3-secretary/references/secretary.md)）**：对齐核心目标与硬性约束、确认配置后派单、审视 6 小时例行回报以识别阻塞或低效空转、果断纠偏或升级用户拍板，并在最终交付时剔除冗余防御性措辞。
  - **项目经理（[`references/project-manager.md`](t3-secretary/references/project-manager.md)）**：接单后绑定自身线程创建 6 小时循环汇报 Scheduled Task，按自身 `AGENTS.md` 自主推进，遇硬阻塞即时上报，完工验收后先清理定时任务再发送最终交付回报。

#### 3. `visualize`
- **适用场景**：回复包含流程图、架构图、状态机、多维横向对比、信息卡片或需要折叠收拢的密集内容时，优先以内嵌 HTML 提升可读性。
- **扩展能力**：当明确要求写入 Obsidian（如 `$visualize 写入 Obsidian`）时，加载 [`references/obsidian-artifact.md`](visualize/references/obsidian-artifact.md)，将可视化组件以 `artifact` 围栏代码块写入指定笔记。

## 通过 CC Switch 安装与更新

### 首次安装

#### 方式一：在 CC Switch 中手动添加仓库（推荐）

1. 打开 CC Switch，进入 **Skills → ⋯ → 仓库管理**。
2. 点击添加仓库并填写：
   - **仓库**：`Hyperlovimia/agent-skills`
   - **分支**：`main`
   - **技能路径**：留空
3. 切换到 **发现** 页面，选择需要安装的 Skill 以及要启用的目标应用即可完成安装。

#### 方式二：使用 CC Switch 深链接添加仓库

复制下方深链接，在浏览器地址栏或系统运行框中打开以直接导入本仓库，随后在 CC Switch 的 **发现** 页面选择要安装的 Skill：

```text
ccswitch://v1/import?resource=skill&repo=Hyperlovimia/agent-skills&branch=main
```

### 后续更新

当本仓库 `main` 分支发布更新后：

1. 打开 CC Switch，进入 **Skills → 已安装**。
2. 点击 **检查更新**。
3. 点击对应 Skill 的 **更新**，或点击 **全部更新** 即可拉取最新内容。

## 手动安装（不使用 CC Switch）

如果不使用 CC Switch，也可以直接克隆本仓库，将所需 Skill 的完整目录（包含其中的 `references/` 子目录）复制到对应客户端的 Skills 目录（例如 `~/.agents/skills/`）：

```bash
git clone https://github.com/Hyperlovimia/agent-skills.git
```

## 配套全局提示词（Codex `AGENTS.md`）

仓库同时收录了配套的 Codex 全局提示词文件 [`prompts/codex/AGENTS.md`](prompts/codex/AGENTS.md)（[Raw 原文](https://raw.githubusercontent.com/Hyperlovimia/agent-skills/main/prompts/codex/AGENTS.md)），可与 `t3-secretary` 等技能配合使用，内容涵盖：

- 多会话与 Git worktree 隔离策略
- 长时任务追踪指南（`wait_agent` 与原生 `Scheduled Task`）
- 主代理 / 子代理委派、静默执行与通信规范
- 模型与推理强度分工建议

### 使用方式

- **通过 CC Switch 配置**：打开 CC Switch，进入 **提示词 → Codex**，新建或编辑预设，将 [`prompts/codex/AGENTS.md`](prompts/codex/AGENTS.md) 的内容复制粘贴进去并启用。
- **手动配置**：直接将文件内容保存到本地 `~/.codex/AGENTS.md`。

> **提示**：
> - 文件中的具体模型名称、推理强度设置以及“遵循仓库 `协作流程`”等约定，请**按自己使用的模型与仓库规范按需替换**。
> - `AGENTS.md` 不会随 CC Switch 的 Skills 仓库自动同步，后续如有改动需要**自行更新**。

## 仓库结构

```text
.
├── README.md
├── prompts/
│   └── codex/
│       └── AGENTS.md
├── t3-adversarial/
│   └── SKILL.md
├── t3-secretary/
│   ├── SKILL.md
│   └── references/
│       ├── project-manager.md
│       └── secretary.md
└── visualize/
    ├── SKILL.md
    └── references/
        └── obsidian-artifact.md
```
