#!/usr/bin/env python3
"""편집 범위 훅 (PreToolUse). harness/05-roles.md 의 편집 범위를 강제한다.

- 작업 에이전트: 자기 산출물 파일만 Write/Edit 가능, Bash 불가
- judge: 파일 수정 불가, Bash는 `python3 harness/judge.py ...` 만 가능
- 메인 세션(오케스트레이터)과 하네스 밖 에이전트: 이 훅이 제한하지 않음
차단 시 exit 2 + stderr (모델에게 사유가 전달된다).
"""
import fnmatch
import json
import os
import re
import sys

SCOPES = {
    "flow-designer": ["runs/*/s1-flow.md"],
    "edge-case-reviewer": ["runs/*/s2-edge-cases.md"],
    "policy-reviewer": ["runs/*/s3-impact.md", "runs/*/s4-policy-conflicts.md"],
    "ux-writer": ["runs/*/s5-ux-writing.md"],
    "judge": [],
}
EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
JUDGE_CMD = re.compile(r"^python3 (\S*/)?harness/judge\.py( [\w-]+)*$")


def block(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)


def main():
    data = json.load(sys.stdin)
    agent = data.get("agent_type")
    if agent not in SCOPES:
        return 0
    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {})
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd", ".")

    if tool in EDIT_TOOLS:
        path = inp.get("file_path") or inp.get("notebook_path") or ""
        rel = os.path.relpath(os.path.abspath(os.path.join(data.get("cwd", root), path)), root)
        allowed = SCOPES[agent]
        if not any(fnmatch.fnmatch(rel, g) for g in allowed):
            block(f"[guard] {agent}는 {rel}을 수정할 수 없어요. 편집 범위: {', '.join(allowed) or '없음(읽기 전용)'}")
    elif tool == "Bash":
        cmd = inp.get("command", "").strip()
        if agent != "judge" or not JUDGE_CMD.match(cmd):
            block(f"[guard] {agent}는 이 명령을 실행할 수 없어요: {cmd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
