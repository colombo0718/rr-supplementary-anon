"""
screenshot_figures.py - screenshot the HTML charts in figures/ into images/

Usage:
    cd <repo root>
    python figures/screenshot_figures.py
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent.parent
FIGURES_DIR = Path(__file__).parent
IMAGES_DIR = ROOT / "images"

# (HTML file, output PNG name, viewport width, viewport height)
# Note: after removing title/subtitle/footnote, the body height was reduced
FIGURES = [
    ("fig3-2-protocol-flow.html",       "fig3-2.png", 1200, 800),
    ("fig3-3-qlearning-flow.html",      "fig3-3.png",  900, 620),
    ("fig3-4-dqn-bidirectional.html",   "fig3-4.png",  800, 500),
    ("fig4-1-experiment-flow.html",     "fig4-1.png", 1400, 980),
    ("fig5-1-pretest-posttest-box.html","fig5-1.png", 1200, 640),
    ("fig5-2-gain-comparison.html",     "fig5-2.png", 1200, 640),
    ("fig5-3-task-completion.html",     "fig5-3.png", 1200, 640),
    ("fig5-4-section3-comparison.html", "fig5-4.png", 1200, 640),
    ("fig5-5-sus-comparison.html",      "fig5-5.png", 1200, 640),
]


async def shot_one(context, html_file: str, png_name: str, w: int, h: int):
    html_path = FIGURES_DIR / html_file
    if not html_path.exists():
        print(f"  [skip] {html_file} (not found)")
        return False

    page = await context.new_page()
    await page.set_viewport_size({"width": w, "height": h})
    url = html_path.absolute().as_uri()
    await page.goto(url)
    await page.wait_for_load_state("networkidle")
    # Give Chart.js / Mermaid time to finish rendering
    await asyncio.sleep(2.5)

    out_path = IMAGES_DIR / png_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    await page.screenshot(path=str(out_path), full_page=False)
    await page.close()
    print(f"  [ok] {png_name}  ({w}x{h})")
    return True


async def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {IMAGES_DIR}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        for html_file, png_name, w, h in FIGURES:
            print(f"> {html_file}")
            await shot_one(context, html_file, png_name, w, h)

        await browser.close()
    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
