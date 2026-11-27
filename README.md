# Agent Skills

个人维护的 AI Agent Skills 与配套提示词集合，包含 **T3 Code 多代理协作协议**、**可视化表达规范**以及 **Codex / Gemini 全局 `AGENTS.md`**。其中 Skills 支持通过 [CC Switch](https://github.com/farion1231/cc-switch) 直接导入与一键更新。

> **说明**：CC Switch 仅负责安装与同步 Skill 文件；AGENTS.md 需要自行复制到本地。

## 包含的 Skills

| Skill | 简介 | 运行环境要求 |
| :--- | :--- | :--- |
| [`t3-adversarial`](t3-adversarial/SKILL.md) | **T3 Code 集思广益**：与子代理进行多轮对抗式方案审查或辩论，保持主代理主见与子代理会话连续（默认最多 3 轮），最终输出共同见解与分歧点供用户决策。可单独调用，也作为 `t3-secretary` 调研/方案审查场景的依赖技能。 | 依赖 T3 Code 中支持复用子代理会话的编排环境（跨 Provider 需 `delegate_task` + `t3_thread_send`） |
| [`t3-secretary`](t3-secretary/SKILL.md) | **T3 Code 秘书模式**：双角色（一秘书统筹多项目经理）异步协作协议，支持异构 PM 选型、双层 TODO 管理（秘书私有索引 + 主仓库单项目 `TODO.md`）、6 小时定时汇报、阻塞介入、完工验收与定时任务清理。 | 依赖 T3 Code 线程与定时任务工具；调研/方案对抗审查场景依赖本仓库 [`t3-adversarial`](t3-adversarial/SKILL.md)（建议一并安装） |
| [`visualize`](visualize/SKILL.md) | **可视化表达（丰富图谱模式）**：使用内嵌 HTML 图谱与排版组件结构化呈现复杂逻辑、横向对比与密集信息；支持按需导出为 Obsidian Artifact Embed 代码块。 | 依赖宿主客户端的 HTML 渲染能力（T3 Code 下配合 `html_preview` / `html_render`；Obsidian 导出需安装 Artifact Embed 插件） |

### 各 Skill 简要说明

#### 1. `t3-adversarial`
- **适用场景**：需要让审查子代理以批判性视角多轮挑战当前方案、排查漏洞或进行结构化辩论。
- **核心机制**：首次委派后复用同一审查子代理会话（不另起新任务），主代理保持独立判断、逐轮回应并说服或修正，默认最多 3 轮，最后以**共同见解**与**分歧点**收尾。

#### 2. `t3-secretary`
- **适用场景**：长时、多线并行的复杂任务异步委托与跟进，将「面向用户的需求对齐与全局监理」和「面向执行的端到端交付」解耦。
- **核心机制**：
  - **秘书（[`references/secretary.md`](t3-secretary/references/secretary.md)）**：可同时统筹多个异构项目经理主线程（工程执行用 Codex/GPT，调研与方案设计用 Gemini 等模型并绑定 [`t3-adversarial`](t3-adversarial/SKILL.md) 线程内对抗审查），维护仅秘书可见的私有 TODO 索引（附 [`scripts/cleanup_indices.py`](t3-secretary/scripts/cleanup_indices.py) 清理脚本），不介入 worktree 等纯工程环境。
  - **项目经理（[`references/project-manager.md`](t3-secretary/references/project-manager.md)）**：接单后自行按需初始化 worktree（默认复用主分支 `.venv`）、独家维护主仓库中的单项目 `TODO.md`，创建 6 小时循环汇报 Scheduled Task；需对抗审查时在线程内调用 `t3-adversarial` 与审查子代理收敛方案；完工验收后先清理定时任务再发送最终交付回报。
- **技能依赖**：使用调研/方案对抗审查能力时依赖 [`t3-adversarial`](t3-adversarial/SKILL.md)，建议通过 CC Switch 同时安装两者（`t3-adversarial` 仍可完全独立调用）。

#### 3. `visualize`
- **适用场景**：回复包含流程图、架构图、状态机、多维横向对比、信息卡片或需要折叠收拢的密集内容时，优先以内嵌 HTML 提升可读性。
- **扩展能力**：当明确要求写入 Obsidian（如 `$visualize 写入 Obsidian`）时，加载 [`references/obsidian-artifact.md`](visualize/references/obsidian-artifact.md)，将可视化组件以 `artifact` 围栏代码块写入指定笔记。

## 动机

### 1. 为什么拆成「秘书 + 项目经理」？
实际干活时，**思维活络的 Gemini** 和 **严谨保守的 GPT（Codex）** 性格反差极大：Gemini 思路开阔、主动性强、擅长抓全局；GPT 工程能力很强，但自带浓重的“防御性和保守思想”，动不动一坨车轱辘话，或在局部细节里钻牛角尖。在被 GPT 多次气红温的背景下，我发现让 Gemini 当**秘书**对齐需求、定目标，让 GPT 当**项目经理**实际执行，最终的效果会好特别多。

~~你说得对，但需要首先说明的是，以下表述仅旨在就相关问题提供一种可能的、有限的、非穷尽性的分析视角，而不应被理解为对任何特定事实、结论、立场、意图或结果的无条件确认；当然，这并不意味着我否认相关事实、拒绝形成判断，或主张任何相反结论，只是说，在缺乏进一步背景信息、完整上下文及可独立验证的证据之前，我无法合理地排除其他解释的可能性，也不宜将当前表述视为唯一、最终或具有普遍适用性的答案。严格来说，即使在现有信息足以支持某种初步判断的情况下，这种支持也仅限于当前可获得的信息范围之内，并不必然延伸至尚未明确的情境、未被讨论的例外情况，或未来可能出现的新证据；但与此同时，我也不希望因为强调这些限制，而使人误以为现有信息毫无价值，或者任何判断都同样合理。换言之，我既不主张这一结论必然成立，也不主张它必然不成立；既不排除其在特定条件下成立的可能性，也不保证这些条件已经得到满足；既不能仅凭现有材料确认其完全正确，也不能仅凭尚存的不确定性断言其错误。需要特别指出的是，上述限定本身同样受到信息范围、语境理解及表述方式的限制，因此不应被视为对所有潜在例外的完整列举；如果其中某些限定看起来过于谨慎，这并不必然意味着相关问题本身极其复杂，也可能只是因为目前没有充分理由将其简化为更强、更明确的断言。反过来说，如果某些表述看起来相对明确，也不应据此推断我已排除所有替代解释，或愿意对该表述在任何语境下的适用性承担无条件责任。对于可能产生的误解，我愿意在获得更明确的语境后作进一步澄清，但这一意愿本身并不构成对任何特定解释、后续结果或澄清效果的保证；同样，澄清也并不必然意味着原表述存在错误，正如原表述未被证明错误，也不意味着它已经得到了充分证明。最后，为避免对以上内容作出超出其实际含义的推断，我想强调：这段话既不是对某一具体结论的完全肯定，也不是对该结论的完全否定，而是在现有条件下，对能够表达什么、不能确定什么，以及为什么暂时不宜作出更强断言所进行的一种有限说明。当然，这一说明本身也并非不受限制；如果需要，还可以进一步限定其适用范围，但是否有必要如此，仍取决于具体语境、实际目的，以及对表述精确程度的要求。以上仅供参考，不构成任何形式的绝对承诺；如有不同理解，应以相关事实、具体语境及进一步核实的结果为准，而不宜仅依据本段文字本身作出超出其明确含义的推断。~~😡😡😡😅😅给我恶心坏了。

### 2. 双层 TODO 与 多任务并行
一旦秘书需要**“统筹全局，同时管好几个项目经理（Thread）”**，纯靠聊天记录在长对话压缩后迟早失忆。于是拆出双层 TODO：**“只给秘书看的 TODO 索引清单（一秘书对应一个）”** + **“秘书和项目经理都能看的单项目 `TODO.md`（一项目经理对应一个）”**。

关于多任务并行：秘书只管在主分支目录建好各项目的 `TODO.md`；项目经理自己拉 worktree、默认复用主分支 `.venv`，跨目录去读写主分支那份 `TODO.md`。

### 3. 调研要对抗审查，怎么不污染秘书？
碰到工程调研、架构选型这类需要双模型核对口径的活。可以保持扁平两层不动，按任务性质用**异构 PM**——写代码跑实验派给 GPT，调研定方案直接派给 Gemini 当项目经理，再让它在自己线程里挂上依赖技能 `$t3-adversarial`、请 GPT 当挑刺子代理。唇枪舌剑全消化在 PM 内部，秘书干干净净只收「推荐方案 + 共同见解 + 核心分歧点」。

### 4. 只恨财力不足😭
我的 Gemini 只有一个 20$ 的订阅，GPT 是 100$ 的 Pro，**“Gemini 额度限制只有 GPT 的 1/10”**，调研决策型 PM 根本经不起 Gemini 事事亲力亲为，更不能让它狂调同样烧 Gemini 额度的内置子代理。

于是补了 [`prompts/gemini/AGENTS.md`](prompts/gemini/AGENTS.md) 分工：**“调研时的一些搜寻、检索、整理等繁杂的内容，以及其他不涉及决策、取舍的内容，交给 GPT 子代理完成”**。为了避免干扰 Gemini 发挥其积极性，日常 GPT 子代理只准当力工😆，**绝不把疑难诊断和方案取舍也交给GPT**。主方案成形后再走 `$t3-adversarial` 对抗性审查。

### 5. 一点写提示词的克制
**“现在基模越来越强大，很多工作流其实已被内化到大模型中。所以 SKILL 要精炼、少改已有内容，只添加必要功能和约束。”** 本仓库的 Skills 和 `AGENTS.md` 都尽量守住这条底线——只写清楚边界、权责和防踩坑护栏，不写长篇大论教大模型怎么走路。

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

## 配套全局提示词（Codex & Gemini `AGENTS.md`）

仓库同时收录了两份配套全局提示词文件，可与 `t3-secretary`、`t3-adversarial` 等技能配合使用：

- **Codex 全局提示词**：[`prompts/codex/AGENTS.md`](prompts/codex/AGENTS.md)（[Raw 原文](https://raw.githubusercontent.com/Hyperlovimia/agent-skills/main/prompts/codex/AGENTS.md)）
  - 涵盖多会话与 Git worktree 隔离、长时任务追踪（`wait_agent` 与 `Scheduled Task`）、主/子代理静默委派及三档模型分工。
- **Gemini（Antigravity + T3 Code）全局提示词**：[`prompts/gemini/AGENTS.md`](prompts/gemini/AGENTS.md)（[Raw 原文](https://raw.githubusercontent.com/Hyperlovimia/agent-skills/main/prompts/gemini/AGENTS.md)）
  - 涵盖多会话与 Git worktree 隔离，以及 T3 Code 跨 Provider 子代理委派规则（保护 Gemini 额度、繁杂检索/整理外包 Codex/GPT、只交事实不代定调、复用上下文与两档日常模型分工）。

### 使用方式

- **通过 CC Switch 配置**：打开 CC Switch，进入 **提示词** 对应客户端页面，新建或编辑预设，将对应 `AGENTS.md` 内容复制粘贴进去并启用。
- **手动配置**：分别保存到本地 `~/.codex/AGENTS.md` 或 `~/.gemini/config/AGENTS.md`。

> **提示**：
> - 文件中的具体模型名称、推理强度设置以及“遵循仓库 `协作流程`”等约定，请**按自己使用的模型与仓库规范按需替换**。
> - `AGENTS.md` 不会随 CC Switch 的 Skills 仓库自动同步，后续如有改动需要**自行更新**。

## 仓库结构

```text
.
├── README.md
├── prompts/
│   ├── codex/
│   │   └── AGENTS.md
│   └── gemini/
│       └── AGENTS.md
├── t3-adversarial/
│   └── SKILL.md
├── t3-secretary/
│   ├── SKILL.md
│   ├── references/
│   │   ├── project-manager.md
│   │   └── secretary.md
│   └── scripts/
│       └── cleanup_indices.py
└── visualize/
    ├── SKILL.md
    └── references/
        └── obsidian-artifact.md
```
