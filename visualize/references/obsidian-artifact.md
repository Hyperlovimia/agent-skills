# 写入 Obsidian（Artifact Embed）

仅处理当前请求明确指定的写入或导出。普通对话中的可视化继续按 `SKILL.md` 的相应规范处理。

## 写入流程

1. 优先使用用户指定的 `.md` 路径，其次使用项目约定的默认笔记或目录。项目无约定时使用项目根目录下的 `output/`。只指定目录时按内容标题命名。相对路径以项目根目录为准。
2. 复用已完成的内容。正文保留为普通 Markdown。之前已渲染的组件优先从原文件或渲染工具输入取回 HTML、CSS 和 JavaScript。源码缺失时说明缺少哪一部分。
3. 将组件写入 `artifact` 围栏代码块。保留布局与交互，按需调整原渲染环境专用的样式变量和脚本依赖，使组件能在 Obsidian 的 iframe 中运行。
4. 现有笔记保留原有内容。按用户指定位置插入，未指定时追加到末尾。目标位置已有相同内容时直接复用。回读确认 Markdown 和代码块完整后返回笔记路径。

## `artifact` 代码块

Artifact Embed 在阅读视图和实时预览中将代码块显示为组件。每个块放一个独立组件。块首行可以加 `height=320 title="结果摘要"`，数字是 iframe 高度（像素，默认为 `480`），标题显示在卡片顶部。省略标题时，插件会按内容来源显示默认名称。

### 直接写入 HTML

默认使用此写法，将源码和正文保存在同一个 `.md` 文件中。块内可包含 HTML 片段或完整文档，以及 `<style>` 和 `<script>`。

```artifact
height=220 title="结果摘要"
<details style="color: var(--text-normal, CanvasText)">
  <summary>查看结果</summary>
  <p>在此放入已经写好的摘要。</p>
</details>
```

脚本在隔离的 iframe 中执行。组件内部的 DOM 事件可以保留。需要 Obsidian API、父页面 DOM 或宿主专用接口的功能要改为可在 iframe 内运行的实现。需跟随主题时，优先使用 `--text-normal`、`--background-primary` 或 `--background-modifier-border` 等 Obsidian 变量。

### 引用库内 HTML 文件

需要多篇笔记复用同一文件时，在块内单独写一行相对于 Obsidian 库根目录的 `.html` 或 `.htm` 路径。

```artifact
Assets/live-clock.html
```

### 引用外部网页

需要嵌入网页时，在块内单独写一行 `http://` 或 `https://` URL。能否显示取决于网页是否允许 iframe 嵌入。

```artifact
https://example.org/dashboard
```

[格式依据：Artifact Embed 用法](https://community.obsidian.md/plugins/artifact-embed#usage)
