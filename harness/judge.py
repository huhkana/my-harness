#!/usr/bin/env python3
"""허들링 기획 하네스 판정 스크립트 (읽기 전용).

사용법:
  python3 harness/judge.py <slug> <S1|S2|S3|S4|S5>   runs/<slug>/ 의 해당 단계 판정
  python3 harness/judge.py --selftest                harness/tests/ 샘플로 판정기 자체 검증

종료 코드: 0 통과 / 1 위반 / 3 S1 복귀 신호 / 2 사용법·입력 오류
규칙 값은 harness/rules.yaml 에서만 읽는다 (PyYAML 없이 내장 간이 파서 사용).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "harness" / "rules.yaml"
TESTS_DIR = ROOT / "harness" / "tests"
TEST_SLUG = "sale-request"

STAGE_FILES = {
    "S1": ["s1-flow.md"],
    "S2": ["s2-edge-cases.md"],
    "S3": ["s3-impact.md"],
    "S4": ["s4-policy-conflicts.md"],
    "S5": ["s5-ux-writing.md"],
}
GATE_IDS = [f"G{i}" for i in range(1, 11)]


# ---------------------------------------------------------------- rules.yaml 간이 파서
# rules.yaml 이 쓰는 부분집합만 지원: 들여쓰기 블록 매핑, "- " 리스트, 흐름형 [..] / {..},
# 따옴표 문자열, 줄 끝 주석.

def _strip_comment(line):
    out, quote = [], None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(tok):
    tok = tok.strip()
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "'\"":
        return tok[1:-1]
    if tok == "true":
        return True
    if tok == "false":
        return False
    if re.fullmatch(r"-?\d+", tok):
        return int(tok)
    return tok


def _parse_flow(s, i=0):
    """흐름형 값 파싱. (값, 다음 인덱스) 반환."""
    while s[i] == " ":
        i += 1
    if s[i] == "[":
        items, i = [], i + 1
        while True:
            while s[i] in " ,":
                i += 1
            if s[i] == "]":
                return items, i + 1
            val, i = _parse_flow(s, i)
            items.append(val)
    if s[i] == "{":
        obj, i = {}, i + 1
        while True:
            while s[i] in " ,":
                i += 1
            if s[i] == "}":
                return obj, i + 1
            j = s.index(":", i)
            key = _scalar(s[i:j])
            val, i = _parse_flow(s, j + 1)
            obj[key] = val
    # 일반 스칼라: 따옴표 처리 후 , ] } 앞까지
    if s[i] in "'\"":
        q = s[i]
        j = s.index(q, i + 1)
        return s[i + 1:j], j + 1
    j = i
    while j < len(s) and s[j] not in ",]}":
        j += 1
    return _scalar(s[i:j]), j


def _collect_flow(first, lines, idx):
    """괄호가 닫힐 때까지 여러 줄을 이어 붙인다."""
    buf = first
    while buf.count("[") + buf.count("{") > buf.count("]") + buf.count("}"):
        idx += 1
        buf += " " + lines[idx][1].strip()
    return buf, idx


def load_rules(path=RULES_PATH):
    raw = path.read_text(encoding="utf-8").splitlines()
    lines = []
    for ln in raw:
        s = _strip_comment(ln)
        if s.strip():
            lines.append((len(s) - len(s.lstrip(" ")), s))

    def parse_block(idx, indent):
        if lines[idx][1].strip().startswith("- "):
            out = []
            while idx < len(lines) and lines[idx][0] == indent and lines[idx][1].strip().startswith("- "):
                body = lines[idx][1].strip()[2:]
                body, idx = _collect_flow(body, lines, idx)
                out.append(_parse_flow(body)[0] if body[0] in "[{" else _scalar(body))
                idx += 1
            return out, idx
        out = {}
        while idx < len(lines) and lines[idx][0] == indent:
            text = lines[idx][1].strip()
            key, _, rest = text.partition(":")
            key, rest = _scalar(key), rest.strip()
            if rest:
                rest, idx = _collect_flow(rest, lines, idx)
                out[key] = _parse_flow(rest)[0] if rest[0] in "[{" else _scalar(rest)
                idx += 1
            elif lines[idx + 1][1].strip()[0] in "[{":
                body, idx = _collect_flow(lines[idx + 1][1].strip(), lines, idx + 1)
                out[key] = _parse_flow(body)[0]
                idx += 1
            else:
                idx += 1
                out[key], idx = parse_block(idx, lines[idx][0])
        return out, idx

    return parse_block(0, 0)[0]


# ---------------------------------------------------------------- Markdown 표 읽기

def read_table(path):
    """파일의 첫 번째 Markdown 표를 (헤더, 행 dict 리스트)로 반환."""
    rows, header = [], None
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            if header is not None:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = cells
        elif all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            continue
        else:
            rows.append(dict(zip(header, cells)))
    return header or [], rows


def split_list(value):
    return [v.strip() for v in re.split(r"[,·/]", value) if v.strip()]


def prd_sections():
    text = (ROOT / "docs" / "prd.md").read_text(encoding="utf-8")
    return set(re.findall(r"^#{2,3} (\d+(?:-\d+)?)\.", text, flags=re.M))


# ---------------------------------------------------------------- 게이트

def judge(run_dir, slug, stage, rules):
    v = []  # (gate, file, message)
    returns, highlights = [], []
    nv = rules["never_violate"]
    design = rules["design"]

    for fname in STAGE_FILES[stage]:
        path = run_dir / fname
        required = rules["artifacts"][fname]

        # G1 구조
        if not path.exists():
            v.append(("G1", fname, "파일 없음"))
            continue
        header, rows = read_table(path)
        missing = [c for c in required if c not in header]
        if missing:
            v.append(("G1", fname, f"필수 컬럼 없음: {', '.join(missing)}"))
            continue
        if not rows:
            v.append(("G1", fname, "행 0개"))
            continue

        # G2 근거
        ev = rules["evidence"]
        if ev["column"] in required:
            sections = prd_sections()
            for n, r in enumerate(rows, 1):
                cell = r.get(ev["column"], "")
                refs = split_list(cell)
                if not refs:
                    v.append(("G2", fname, f"{n}행 근거 비어 있음"))
                for ref in refs:
                    if not re.fullmatch(ev["pattern"], ref):
                        v.append(("G2", fname, f"{n}행 근거 형식 오류: {ref}"))
                    elif ref not in sections:
                        v.append(("G2", fname, f"{n}행 prd.md에 없는 섹션: {ref}"))

        # G6 MVP 밖 금지어 (전체 파일 텍스트)
        text = path.read_text(encoding="utf-8")
        for term in nv["banned_terms"]:
            if term in text:
                v.append(("G6", fname, f"금지어 등장: {term}"))

        if fname == "s1-flow.md":
            role_col = "진입 조건(role)"
            # G4 admin 전용 화면
            a = nv["admin_only_screens"]
            for n, r in enumerate(rows, 1):
                if any(k in r["화면명"] for k in a["keywords"]):
                    roles = set(split_list(r[role_col]))
                    if roles != {a["role"]}:
                        v.append(("G4", fname, f"{n}행 '{r['화면명']}' 진입 role={r[role_col]} (admin만 허용)"))
            # G5 seller 전용 화면
            s = nv["seller_only_screens"]
            if slug in s["flows"]:
                for n, r in enumerate(rows, 1):
                    if any(k in r["화면명"] for k in s["keywords"]):
                        roles = set(split_list(r[role_col]))
                        if roles != {s["role"]}:
                            v.append(("G5", fname, f"{n}행 '{r['화면명']}' 진입 role={r[role_col]} (seller만 허용)"))
            # G7 컴포넌트
            allowed = set(design["components"])
            for n, r in enumerate(rows, 1):
                comps = split_list(r["컴포넌트"])
                if not comps:
                    v.append(("G7", fname, f"{n}행 컴포넌트 비어 있음"))
                for c in comps:
                    if c not in allowed:
                        v.append(("G7", fname, f"{n}행 design.md에 없는 컴포넌트: {c}"))

        if fname == "s2-edge-cases.md":
            # G3 상태값
            allowed = rules["allowed_status"]
            union = {x for vals in allowed.values() for x in vals}
            for n, r in enumerate(rows, 1):
                tokens = split_list(r["관련 상태값"])
                if not tokens:
                    v.append(("G3", fname, f"{n}행 관련 상태값 비어 있음"))
                for t in tokens:
                    if "=" in t:
                        k, _, val = t.partition("=")
                        if k.strip() not in allowed or val.strip() not in allowed[k.strip()]:
                            v.append(("G3", fname, f"{n}행 허용되지 않은 상태값: {t}"))
                    elif t not in union:
                        v.append(("G3", fname, f"{n}행 허용되지 않은 상태값: {t}"))
            # G5 / G10 필수 엣지케이스
            for req in nv["required_edge_cases"]:
                if slug not in req["flows"]:
                    continue
                joined = [" ".join(r.values()) for r in rows]
                if "match" in req:
                    ok = any(all(m in row for m in req["match"]) for row in joined)
                    if not ok:
                        v.append(("G5", fname, f"필수 엣지케이스 없음: {' + '.join(req['match'])}"))
                else:
                    ok = any(any(m in row for m in req["match_any"]) for row in joined)
                    if not ok:
                        v.append(("G10", fname, f"민감정보 엣지케이스 없음: {'/'.join(req['match_any'])}"))

        if fname == "s5-ux-writing.md":
            # G8 all-caps
            if design.get("ban_all_caps"):
                allow = set(design.get("all_caps_allow", []))
                for n, r in enumerate(rows, 1):
                    for w in re.findall(r"\b[A-Z]{2,}\b", r["문구"]):
                        if w not in allow:
                            v.append(("G8", fname, f"{n}행 all-caps 단어: {w}"))
            # G9 accent
            acc = design["accent"]
            per_screen = {}
            for n, r in enumerate(rows, 1):
                if r["accent(Y/N)"].upper() == "Y":
                    per_screen[r["화면ID"]] = per_screen.get(r["화면ID"], 0) + 1
                    if acc["banned_on"] in r["위치"]:
                        v.append(("G9", fname, f"{n}행 {acc['banned_on']}에 accent 사용"))
            for sid, cnt in per_screen.items():
                if cnt > acc["max_per_screen"]:
                    v.append(("G9", fname, f"화면 {sid} accent {cnt}개 (최대 {acc['max_per_screen']})"))

        # 복귀 신호 / 승인 강조
        for ret in rules["returns"]["to_s1"]:
            if ret["file"] == fname:
                for n, r in enumerate(rows, 1):
                    if r.get(ret["column"], "").strip() == ret["value"]:
                        returns.append(f"{fname} {n}행 {ret['column']}={ret['value']}")
        ha = rules["human_approval"].get("highlight_if")
        if ha and ha["file"] == fname:
            for n, r in enumerate(rows, 1):
                if r.get(ha["column"], "").strip() == ha["value"]:
                    highlights.append(f"{fname} {n}행 {r.get('충돌 정책', '')}")

    return v, returns, highlights


def report(v, returns, highlights):
    for g, f, m in v:
        print(f"[{g}] {f}: {m}")
    for r in returns:
        print(f"[RETURN_S1] {r}")
    for h in highlights:
        print(f"[PM 확인] {h}")
    print(f"violations: {len(v)}")
    if v:
        print("RESULT: FAIL")
        return 1
    if returns:
        print("RESULT: RETURN_S1")
        return 3
    print("RESULT: PASS")
    return 0


# ---------------------------------------------------------------- 자체 테스트

def selftest(rules):
    cases = sorted(p for p in TESTS_DIR.iterdir() if p.is_dir())
    ok_all = True
    for case in cases:
        hit = set()
        for stage in STAGE_FILES:
            v, _, _ = judge(case, TEST_SLUG, stage, rules)
            hit |= {g for g, _, _ in v}
        if case.name == "pass":
            expected = set()
        else:
            expected = {case.name.removeprefix("fail-")}
        ok = hit == expected
        ok_all &= ok
        print(f"{'OK  ' if ok else 'FAIL'} {case.name:10} expected={sorted(expected) or '-'} got={sorted(hit) or '-'}")
    print(f"selftest: {'PASS' if ok_all else 'FAIL'} ({len(cases)} cases)")
    return 0 if ok_all else 1


def main(argv):
    rules = load_rules()
    if argv[1:] == ["--selftest"]:
        return selftest(rules)
    if argv[1:] == ["--dump-rules"]:
        print(json.dumps(rules, ensure_ascii=False, indent=2))
        return 0
    if len(argv) != 3 or argv[2] not in STAGE_FILES:
        print(__doc__)
        return 2
    slug, stage = argv[1], argv[2]
    run_dir = ROOT / "runs" / slug
    if not run_dir.is_dir():
        print(f"runs/{slug}/ 없음")
        return 2
    return report(*judge(run_dir, slug, stage, rules))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
