"""Site hooks (registered in mkdocs.yml).

- Notes get a title plus a category / reading-time line; projects get a title plus their
  one-line summary. Both show featured.jpg as a cover unless the page opens with media.
- Markers expand into listings built from front matter, so new pages show up on their own:
    <!-- zr:projects -->  project cards, ordered by `weight`
    <!-- zr:notes -->     note cards, ordered by `weight`
    <!-- zr:recent N -->  the N leading notes as a compact list
- No dates are rendered anywhere; order comes from the `weight` field (smaller = earlier).
"""
import posixpath
import re

from mkdocs.utils import meta as meta_utils

_pages = {}  # section -> [(src_uri, front matter)]
_files = set()


def _section(src_uri):
    """'notes/<slug>/index.md' -> 'notes'; anything else -> None."""
    parts = src_uri.split("/")
    if len(parts) == 3 and parts[0] in ("notes", "projects") and parts[2] == "index.md":
        return parts[0]
    return None


def on_files(files, config):
    _pages.clear()
    _files.clear()
    _files.update(f.src_uri for f in files)
    for f in files.documentation_pages():
        section = _section(f.src_uri)
        if section:
            _pages.setdefault(section, []).append((f.src_uri, meta_utils.get_data(f.content_string)[1]))
    _pages.get("notes", []).sort(key=lambda p: p[1].get("weight", 99))
    _pages.get("projects", []).sort(key=lambda p: p[1].get("weight", 99))


def _rel(src_uri, page):
    return posixpath.relpath(src_uri, posixpath.dirname(page.file.src_uri) or ".")


def _cover(src_uri):
    cover = posixpath.join(posixpath.dirname(src_uri), "featured.jpg")
    return cover if cover in _files else None


def _cards(section, page):
    items = []
    for src, meta in _pages.get(section, []):
        link, cover = _rel(src, page), _cover(src)
        tag = meta.get("category", "")
        lines = []
        if cover:
            lines.append(f"[![{meta['title']}]({_rel(cover, page)}){{ .off-glb loading=lazy }}]({link})")
        if tag:
            lines.append(f'<span class="zr-card__tag">{tag}</span>')
        lines.append(f"[**{meta['title']}**]({link})")
        if meta.get("description"):
            lines.append(meta["description"])
        items.append("-   " + "\n\n    ".join(lines))
    return '<div class="grid cards zr-cards" markdown>\n\n' + "\n\n".join(items) + "\n\n</div>"


def _recent(page, n):
    rows = [f'-   [{meta["title"]}]({_rel(src, page)})\n\n    {meta.get("description", "")}'
            for src, meta in _pages.get("notes", [])[:n]]
    return '<div class="zr-recent" markdown>\n\n' + "\n\n".join(rows) + "\n\n</div>"


def _minutes(markdown):
    text = re.sub(r"```.*?```|<[^>]+>|!\[[^\]]*\]\([^)]*\)", "", markdown, flags=re.S)
    cjk = len(re.findall(r"[一-鿿]", text))
    words = len(re.findall(r"[A-Za-z0-9]+", text))
    return max(1, round(cjk / 400 + words / 200))


def on_page_markdown(markdown, page, config, files):
    markdown = markdown.replace("<!-- zr:projects -->", _cards("projects", page))
    markdown = markdown.replace("<!-- zr:notes -->", _cards("notes", page))
    markdown = re.sub(r"<!-- zr:recent (\d+) -->", lambda m: _recent(page, int(m[1])), markdown)

    section = _section(page.file.src_uri)
    if not section or markdown.lstrip().startswith("# "):
        return markdown
    meta = page.meta
    head = [f"# {meta.get('title', page.title)}"]
    if section == "notes":
        bits = [meta.get("category", ""), f"约 {_minutes(markdown)} 分钟读完"]
        head.append('<p class="zr-meta">' + "".join(f"<span>{b}</span>" for b in bits if b) + "</p>")
    elif meta.get("description"):
        head.append(f'<p class="zr-meta zr-meta--lead">{meta["description"]}</p>')
    if _cover(page.file.src_uri) and not re.match(r'\s*<(figure|div class="zr-gallery)', markdown):
        head.append(f"![{meta.get('title', '')}](featured.jpg){{ .zr-cover .off-glb }}")
    return "\n\n".join(head) + "\n\n" + markdown
