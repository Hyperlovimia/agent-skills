#!/usr/bin/env python3
"""Manage and clean up t3-secretary private index files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import sys

FALLBACK_INDICES_DIR = Path.home() / ".agents" / "skills" / "t3-secretary" / "indices"
TERMINAL_STATUSES = {"已完成", "已终止", "completed", "terminated", "done", "cancelled"}


@dataclass
class IndexEntry:
    path: Path
    thread_id: str
    status: str
    updated_at: datetime
    total_pms: int
    active_pms: int
    open_todos: int

    @property
    def is_completed(self) -> bool:
        if self.status.lower() == "completed":
            return True
        return self.total_pms > 0 and self.active_pms == 0 and self.open_todos == 0


def resolve_indices_dirs(custom_dir: str | None) -> list[Path]:
    if custom_dir:
        return [Path(custom_dir).expanduser().resolve()]
    primary = Path(__file__).resolve().parent.parent / "indices"
    dirs = [primary]
    if FALLBACK_INDICES_DIR.exists():
        fb = FALLBACK_INDICES_DIR.resolve()
        if fb != primary.resolve():
            dirs.append(fb)
    return dirs


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        return {}
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = re.sub(r"\s+#.*$", "", line).strip()
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip().strip("'\"")
    return meta


def parse_datetime(raw: str | None, fallback_ts: float) -> datetime:
    if raw:
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return dt if dt.tzinfo else dt.astimezone()
        except ValueError:
            pass
    return datetime.fromtimestamp(fallback_ts).astimezone()


def parse_index(path: Path) -> IndexEntry:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_frontmatter(text)
    thread_id = meta.get("secretary_thread_id") or path.stem
    status = meta.get("status", "active")
    updated_at = parse_datetime(meta.get("updated_at"), path.stat().st_mtime)

    open_todos = 0
    total_pms = 0
    active_pms = 0
    section = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if "待办" in section or "拍板" in section:
            if re.match(r"^-\s*\[\s\]\s+\S+", line):
                open_todos += 1
        elif "台账" in section and line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 3 or cells[0] == "代号" or all(set(c) <= set("-: ") for c in cells):
                continue
            total_pms += 1
            if cells[2].lower() not in TERMINAL_STATUSES and cells[2] not in TERMINAL_STATUSES:
                active_pms += 1

    return IndexEntry(path, thread_id, status, updated_at, total_pms, active_pms, open_todos)


def load_entries(dirs: list[Path]) -> list[IndexEntry]:
    entries: list[IndexEntry] = []
    seen: set[Path] = set()
    for directory in dirs:
        if not directory.is_dir():
            continue
        for md in sorted(directory.glob("*.md")):
            resolved = md.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            entries.append(parse_index(md))
    return entries


def format_list(entries: list[IndexEntry], dirs: list[Path]) -> str:
    if not entries:
        locs = ", ".join(str(d) for d in dirs)
        return f"暂无秘书索引文件（扫描目录：{locs}）"
    lines = ["THREAD_ID | STATE | PMS(ACTIVE/TOTAL) | OPEN_TODOS | UPDATED_AT | PATH"]
    for e in entries:
        state = "completed" if e.is_completed else "active"
        ts = e.updated_at.strftime("%Y-%m-%d %H:%M")
        lines.append(
            f"{e.thread_id} | {state} | {e.active_pms}/{e.total_pms} | {e.open_todos} | {ts} | {e.path}"
        )
    return "\n".join(lines)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="列出或清理 t3-secretary 秘书私有 TODO 索引文件。")
    parser.add_argument("--indices-dir", help="自定义索引目录（覆盖自动发现）")
    parser.add_argument("--list", action="store_true", help="列出所有秘书索引文件（默认行为）")
    parser.add_argument("--thread-id", action="append", default=[], help="按秘书 threadId 精确删除（可重复指定）")
    parser.add_argument("--completed", action="store_true", help="删除所有已终结的索引文件")
    parser.add_argument("--older-than", type=float, metavar="DAYS", help="删除超过指定天数未更新的索引文件")
    parser.add_argument("--all", action="store_true", help="删除全部索引文件（非 --dry-run 需配合 --yes 或交互确认）")
    parser.add_argument("--dry-run", action="store_true", help="仅预览拟删除文件，不实际删除")
    parser.add_argument("--yes", "-y", action="store_true", help="跳过 --all 的交互确认")
    args = parser.parse_args()

    dirs = resolve_indices_dirs(args.indices_dir)
    entries = load_entries(dirs)

    has_delete = bool(args.thread_id or args.completed or args.older_than is not None or args.all)
    if args.list or not has_delete:
        print(format_list(entries, dirs))
        if not has_delete:
            return 0

    targets: dict[Path, IndexEntry] = {}
    if args.all:
        for e in entries:
            targets[e.path] = e
    if args.thread_id:
        wanted = set(args.thread_id)
        for e in entries:
            if e.thread_id in wanted or e.path.stem in wanted:
                targets[e.path] = e
    if args.completed:
        for e in entries:
            if e.is_completed:
                targets[e.path] = e
    if args.older_than is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.older_than)
        for e in entries:
            if e.updated_at.astimezone(timezone.utc) < cutoff:
                targets[e.path] = e

    selected = list(targets.values())
    if not selected:
        print("没有匹配的索引文件需要清理。")
        return 0

    if args.dry_run:
        print(f"[dry-run] 将删除 {len(selected)} 个索引文件：")
        for e in selected:
            print(f"  - {e.thread_id}: {e.path}")
        return 0

    if args.all and not args.yes:
        reply = input(f"确认删除全部 {len(selected)} 个索引文件？输入 yes 继续：").strip().lower()
        if reply != "yes":
            print("已取消。")
            return 1

    for e in selected:
        e.path.unlink(missing_ok=True)
        print(f"已删除：{e.thread_id} ({e.path})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
