"""Export the reviewed journal with Chromium, checking pagination before release."""
from pathlib import Path
import argparse
import json
import re

import pymupdf
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--chromium', default='/usr/bin/chromium')
args = parser.parse_args()
source = root / 'public/research/agent-evolution/report/index.html'
target = root / 'public/research/agent-evolution/agent-evolution-202611.pdf'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.chromium, args=['--no-sandbox'])
    page = browser.new_page(java_script_enabled=False)
    page.goto(source.as_uri())
    page.evaluate('document.fonts.ready')
    page.emulate_media(media='print')
    overflow = page.locator('.folio').evaluate_all('''els => els.filter(e => {
      const c=e.querySelector('.folio-content'), f=e.querySelector('.folio-foot');
      return c.scrollHeight>c.clientHeight+2 || c.lastElementChild.getBoundingClientRect().bottom>f.getBoundingClientRect().top-8;
    }).map(e=>e.id)''')
    contents_overflow = page.locator('.print-contents').evaluate_all('''els => els.some(e =>
      e.querySelector('ol').getBoundingClientRect().bottom > e.querySelector('footer').getBoundingClientRect().top-8)''')
    if overflow or contents_overflow:
        raise SystemExit(f'Print overflow: sections={overflow}, contents={contents_overflow}')
    page.pdf(path=str(target), format='A4', print_background=True,
             prefer_css_page_size=True, tagged=True, outline=True)
    browser.close()

stats = json.loads((root/'research/agent-evolution-202611/content-stats.json').read_text())
with pymupdf.open(target) as doc:
    if len(doc) != 63:
        raise SystemExit(f'Expected 63 pages; got {len(doc)}. Review layout and page metadata.')
    for section in stats['sections']:
        title = re.sub(r'\s+', '', section['title'])
        text = re.sub(r'\s+', '', doc[section['folio']+2].get_text())
        if title not in text:
            raise SystemExit(f'Wrong PDF page for section {section["folio"]}')
    print(json.dumps({'pdf_pages':len(doc), 'outline_entries':len(doc.get_toc()),
                      'bytes':target.stat().st_size, 'output':str(target)}))
