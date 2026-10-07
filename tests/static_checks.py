#!/usr/bin/env python3
"""Static repository checks. Python standard library only.

Run from the project root:   python3 tests/static_checks.py
Exits non-zero if any check fails.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_EXT = {".html", ".js", ".css", ".py", ".md", ".yml", ".yaml", ".json", ".txt"}
SKIP_DIRS = {"tests", "__pycache__", ".git", "node_modules"}

failures = []
notes = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (f"  ({detail})" if detail else ""))
    if not ok:
        failures.append(name)

def text_files(include_tests=False):
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if include_tests or d not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1].lower() in TEXT_EXT or f in {".gitignore", "_headers"}:
                yield os.path.join(dirpath, f)

def read(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()

def rel(p):
    return os.path.relpath(p, ROOT)

# Terms are assembled from fragments so this file never matches itself.
REMOVED_TERMS = {
    "old phone 1": "081" + "-670-95700",
    "old phone 2": "081" + "-857-69700",
    "old phone 3": "080" + "-331-30374",
    "old phone 4": "080" + "-868-34332",
    "old whatsapp placeholder": "WHATSAPP_NUMBER" + "_HERE",
    "Lagos branch": "La" + "gos",
    "Abuja branch": "Abu" + "ja",
    "catalogue": "catal" + "ogue",
    "fuel dispenser": "fuel" + r"[\s-]*dispens",
    "pump dispenser": "pump" + r"\s+fuel",
    "non woven": "non" + r"[\s-]*woven",
}

print("== Removed content must not appear anywhere ==")
for label, pattern in REMOVED_TERMS.items():
    hits = []
    for p in text_files():
        for i, line in enumerate(read(p).splitlines(), 1):
            if re.search(pattern, line, re.I):
                hits.append(f"{rel(p)}:{i}")
    check(f"no '{label}' references", not hits, ", ".join(hits[:5]))

print("\n== Removed files must not exist ==")
check("catalogue page absent", not os.path.exists(os.path.join(ROOT, "catal" + "ogue.html")))
pdfs = [rel(os.path.join(d, f)) for d, _, fs in os.walk(ROOT) for f in fs if f.lower().endswith(".pdf")]
check("no PDF files in project", not pdfs, ", ".join(pdfs))
imgs = set(os.listdir(os.path.join(ROOT, "assets", "img")))
removed_imgs = [i for i in imgs if re.search(r"fuel|nonwoven|cover-collage|catal" + "ogue", i)]
check("no images for removed products/catalogue", not removed_imgs, ", ".join(removed_imgs))

print("\n== Contact configuration ==")
data = read(os.path.join(ROOT, "js", "data.js"))
check("WhatsApp is 2349022330011", 'whatsapp: "2349022330011"' in data)
check("call number 08033100374 present", "08033100374" in data)
check("call number 09095555222 present", "09095555222" in data)
m = re.search(r"phones:\s*\[(.*?)\]", data, re.S)
phones = re.findall(r'"(\d+)"', m.group(1)) if m else []
check("exactly the two official phone numbers", sorted(phones) == ["08033100374", "09095555222"], str(phones))

print("\n== WhatsApp centralisation ==")
wa_digits = []
for p in text_files():
    if p.endswith(".md"):
        continue  # documentation may quote the number as an example; this check is about code
    s = read(p)
    if re.search(r"234902" + "2330011", s):
        wa_digits.append(rel(p))
check("WhatsApp number defined in exactly one file", wa_digits == [os.path.join("js", "data.js")], str(wa_digits))
wa_me = []
for p in text_files():
    for i, line in enumerate(read(p).splitlines(), 1):
        if "wa.me/" in line and not line.strip().startswith(("//", "*", "/*")):
            wa_me.append(f"{rel(p)}:{i}")
check("wa.me link constructed in exactly one place", len(wa_me) == 1 and wa_me[0].startswith(os.path.join("js", "main.js")), str(wa_me))
raw_tel_digits = []
for p in text_files():
    if rel(p) in (os.path.join("js", "data.js"), "README.md", "SECURITY.md"):
        continue
    if re.search(r"0(8033100374|9095555222|9022330011)", read(p)):
        raw_tel_digits.append(rel(p))
check("phone numbers not duplicated outside data.js/docs", not raw_tel_digits, ", ".join(raw_tel_digits))

print("\n== Dangerous DOM sinks (in source we wrote) ==")
js_src = {rel(p): read(p) for p in text_files() if p.endswith(".js")}
for sink, pat in {
    "eval()": r"\beval\s*\(", "new Function": r"new\s+Function\b", "document.write": r"document\.write\s*\(",
    "outerHTML": r"\.outerHTML\s*=", "insertAdjacentHTML": r"insertAdjacentHTML", "javascript: URL": r"javascript:",
    "localStorage/sessionStorage": r"(local|session)Storage",
    "assignment to location from input": r"location\.(href|assign|replace)\s*=",
}.items():
    hits = [f for f, s in js_src.items() if re.search(pat, s)]
    check(f"no {sink}", not hits, ", ".join(hits))
inner = []
for f, s in js_src.items():
    for i, line in enumerate(s.splitlines(), 1):
        if re.search(r"\.innerHTML\s*=", line):
            inner.append(f"{f}:{i}")
notes.append(f"innerHTML assignments remaining ({len(inner)}): all render developer-controlled data through escapeHtml(): " + ", ".join(inner))
status_inner = [x for x in inner if "status" in js_src['js/main.js'].splitlines()[int(x.split(':')[1]) - 1]]
check("status messages built without innerHTML", not status_inner, ", ".join(status_inner))

print("\n== Secrets scan ==")
patterns = {
    "AWS access key": r"AKIA[0-9A-Z]{16}", "private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "GitHub token": r"gh[pousr]_[A-Za-z0-9]{30,}", "Slack token": r"xox[abp]-[A-Za-z0-9-]{10,}",
    "Google API key": r"AIza[0-9A-Za-z_\-]{35}", "generic secret assignment": r"(?i)(api[_-]?key|secret|passwd|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]",
    "long hex string (32+)": r"\b[0-9a-f]{32,}\b",
}
for label, pat in patterns.items():
    hits = [rel(p) for p in text_files() if re.search(pat, read(p))]
    check(f"no {label}", not hits, ", ".join(hits))
env_files = [rel(os.path.join(d, f)) for d, _, fs in os.walk(ROOT) for f in fs if f.startswith(".env") or f.endswith((".pem", ".key"))]
check("no .env / key files present", not env_files, ", ".join(env_files))
gi = read(os.path.join(ROOT, ".gitignore")) if os.path.exists(os.path.join(ROOT, ".gitignore")) else ""
check(".gitignore covers .env and keys", ".env" in gi and "*.pem" in gi)
check("no .github/workflows (no CI secrets surface)", not os.path.exists(os.path.join(ROOT, ".github")))

print("\n== External hosts and mixed content ==")
ALLOWED = {"cdnjs.cloudflare.com", "fonts.googleapis.com", "fonts.gstatic.com", "www.google.com", "wa.me", "www.w3.org"}
hosts = {}
for p in text_files():
    for u in re.findall(r"https?://[^\s\"'<>)`;,\\]+", read(p)):
        h = re.match(r"https?://([^/:?#]+)", u).group(1)
        hosts.setdefault(h, set()).add(rel(p))
unexpected = {h: sorted(f) for h, f in hosts.items() if h not in ALLOWED and h not in ("localhost", "127.0.0.1") and not h.startswith("$")}
unexpected.pop("github.com", None)
check("only allow-listed external hosts", not unexpected, str(unexpected))
http_plain = []
for p in text_files():
    for i, line in enumerate(read(p).splitlines(), 1):
        for u in re.findall(r"http://[^\s\"'<>)]+", line):
            if "www.w3.org" not in u:
                http_plain.append(f"{rel(p)}:{i}")
check("no plain http:// resources (mixed content)", not http_plain, ", ".join(http_plain))
html = read(os.path.join(ROOT, "index.html"))
check("CSP meta tag present on pages", "Content-Security-Policy" in html)
check("CSP has no unsafe-inline for scripts", not re.search(r"script-src[^;]*unsafe-inline", html))
check("CSP has no unsafe-eval", "unsafe-eval" not in html)
check("referrer policy meta present", 'name="referrer"' in html)
inline_scripts = []
for p in text_files():
    if p.endswith(".html"):
        for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>", read(p)):
            inline_scripts.append(rel(p))
check("no inline <script> blocks (CSP-compatible)", not inline_scripts, ", ".join(sorted(set(inline_scripts))))
check("no empty src attributes (browsers treat them as errors)", not any('src=""' in read(p) for p in text_files() if p.endswith(".html")))
check("no inline event handler attributes", not any(re.search(r"\son(click|load|error|mouseover)\s*=", read(p)) for p in text_files() if p.endswith(".html")))
check("external script tag has crossorigin + referrerpolicy", 'crossorigin="anonymous" referrerpolicy="no-referrer"' in html)
check("external links with target=_blank use rel=noopener", not re.search(r'target="_blank"(?![^>]*noopener)', "".join(read(p) for p in text_files() if p.endswith(".html"))))

print("\n== Copy: connector dashes ==")
copy_files = [os.path.join(ROOT, f) for f in ("js/data.js", "build.py", "build_pages.py")]
dash_hits = []
for p in copy_files:
    src = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), read(p), flags=re.S)  # drop block comments, keep line numbers
    for i, line in enumerate(src.splitlines(), 1):
        if line.strip().startswith(("//", "#")) or "print(" in line:
            continue
        if re.search(r" — |&mdash;| - ", line):
            dash_hits.append(f"{rel(p)}:{i}")
check("no spaced em dash / hyphen connectors in visible copy", not dash_hits, ", ".join(dash_hits[:6]))

print("\n== Notes ==")
for n in notes:
    print("NOTE  " + n)

print(f"\n{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
