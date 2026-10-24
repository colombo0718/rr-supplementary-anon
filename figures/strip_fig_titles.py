#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
strip_fig_titles.py - remove the title/subtitle/footnote/stats-line from the fig5-X HTML files

Per the formatting guidelines, figure titles and captions are handled by the
document-building script (add_fig_caption), so the HTML figure files should
contain only the chart itself, without a duplicated "Figure 5-X ..." title.

Only touches fig5-1 to fig5-5; fig3-2 and fig4-1 are left alone (fig4-1 was rewritten by hand).
"""

import re
from pathlib import Path

FIGURES = [
    "fig5-1-pretest-posttest-box.html",
    "fig5-2-gain-comparison.html",
    "fig5-3-task-completion.html",
    "fig5-4-section3-comparison.html",
    "fig5-5-sus-comparison.html",
]

DIR = Path(__file__).parent

# div classes to remove
DIV_CLASSES_TO_REMOVE = ['title', 'subtitle', 'footnote', 'stats-line']

# CSS rule selectors to remove
CSS_CLASSES_TO_REMOVE = ['.title', '.subtitle', '.footnote', '.stats-line']


def remove_divs(html, class_name):
    """Remove <div class="class_name">...</div>, possibly spanning multiple lines."""
    # Simple version: non-greedy match of <div class="X">...</div>
    pattern = re.compile(
        r'<div\s+class="' + re.escape(class_name) + r'"[^>]*>.*?</div>\s*',
        re.DOTALL
    )
    return pattern.sub('', html)


def remove_css_rule(css, selector):
    """Remove the CSS rule for the given selector."""
    # Match selector { ... } including newlines
    pattern = re.compile(
        r'\s*' + re.escape(selector) + r'\s*\{[^}]*\}\s*',
        re.DOTALL
    )
    return pattern.sub('\n  ', css)


def process(fpath):
    text = fpath.read_text(encoding='utf-8')
    original = text

    # Remove the divs first
    for cls in DIV_CLASSES_TO_REMOVE:
        text = remove_divs(text, cls)

    # Remove the matching CSS rules
    for cls in CSS_CLASSES_TO_REMOVE:
        text = remove_css_rule(text, cls)

    # Shrink body height (800px -> 640px, since removing title/subtitle/footnote lowers the height)
    text = re.sub(r'(\s+height:\s*)800px\s*;', r'\g<1>640px;', text)
    # Some may be 700/900 etc.; leave those alone for now

    if text != original:
        fpath.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    for name in FIGURES:
        fpath = DIR / name
        if not fpath.exists():
            print(f'[error] {name} not found')
            continue
        changed = process(fpath)
        marker = 'changed' if changed else 'unchanged'
        print(f'{marker}: {name}')


if __name__ == '__main__':
    main()
