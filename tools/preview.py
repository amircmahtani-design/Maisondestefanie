# -*- coding: utf-8 -*-
"""Build hero-preview.html — the first screen as a film, for approval.

It is the real home page in every respect except the first screen: same
shell, same header, same footer, same stylesheet. Only the opening
section is replaced by the composited film, and only this file loads
assets/hero-film.css and assets/hero-film.js.

    python3 tools/preview.py

The page is noindex. index.html is not touched by this script, and the
film does not reach the home page until it is approved.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = os.path.join(ROOT, 'tools', 'shell.html')
SECTIONS = os.path.join(ROOT, 'tools', 'sections.html')
OUT = os.path.join(ROOT, 'hero-preview.html')

FILM = """<!-- ══════════════ THE FIRST SCREEN, AS A FILM ══════════════ -->
<section class="hero filmhero" id="top">
  <div class="fh-scenes" aria-hidden="true"></div>

  <div class="hero-copy">
    <p class="hero-eyebrow" data-t="hero.eyebrow"></p>
    <h1><span data-t="hero.titleA"></span> <em data-t="hero.titleB"></em></h1>
    <p class="hero-lede" data-t="hero.lede"></p>
    <div class="hero-acts">
      <a class="hero-cta" href="/bespoke.html" data-nav>
        <span data-t="hero.ctaPrimary"></span>
        <svg viewBox="0 0 8 8" fill="none" aria-hidden="true">
          <path d="M1 0.6 4.4 4 1 7.4" stroke="currentColor" stroke-width="1.1"/></svg>
      </a>
      <a class="hero-alt" href="/visit.html" data-nav data-t="hero.ctaSecondary"></a>
    </div>
  </div>
</section>
"""

MOUNT = """<script type="module">
  import { mountFilmHero } from "/assets/hero-film.js";
  mountFilmHero(document.querySelector(".filmhero"));
</script>
</body>"""


def main():
    page = open(SHELL, encoding='utf-8').read()
    body = open(SECTIONS, encoding='utf-8').read()

    marks = [(m.start(), m.group(1).strip())
             for m in re.finditer(r'<!-- ═+ (.*?) ═+ -->', body)]
    chunk = {}
    for i, (pos, name) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        chunk[name] = body[pos:end].rstrip() + '\n'

    # no curtain: whoever is reviewing this wants the picture, not the door
    page = re.sub(r'<!-- ═+ THE CURTAIN.*?\n</div>\n', '', page, flags=re.S)

    page = page.replace('<meta charset="utf-8">',
                        '<meta charset="utf-8">\n'
                        '<meta name="robots" content="noindex, nofollow">', 1)
    page = page.replace(
        '<link rel="stylesheet" href="/assets/site.css">',
        '<link rel="preload" as="image" href="/assets/hero/plate-1-wide.webp"'
        ' fetchpriority="high">\n'
        '<link rel="stylesheet" href="/assets/site.css">\n'
        '<link rel="stylesheet" href="/assets/hero-film.css">', 1)
    page = page.replace('</body>', MOUNT, 1)

    content = FILM + '\n' + chunk['A MEMORY, DISTILLED'] + '\n' + chunk['THE FIVE DOORS']
    out = page.replace('<!--PAGE-->', content.rstrip() + '\n')
    open(OUT, 'w', encoding='utf-8').write(out)
    print(f'hero-preview.html  {len(out)//1024} KB')


if __name__ == '__main__':
    main()
