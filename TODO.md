# Portfolio TODO

Source: portfolio audit (2026-10-23). Content lives in `src/data/portfolio.json`; rebuild with `python3 tools/personalize.py`.

## Quick wins (done, uncommitted)

- [x] Remove the phone number from the contact section
- [x] Label hero stats as Graas figures
- [x] Tighten hero (900px to 675px) and make "Email me" the primary CTA
- [x] Hide GPAVBHAG and Spell Checker (`"hidden": true` in the JSON)
- [ ] Pad the hero Resume link to a 44px hit area (optional)

## Short-term (1-4 hours)

- [ ] Real screenshots for the top 3 projects (set `image` in the JSON); voice agent first. Deferred: placeholder stays for now
- [ ] Add year, role and one result to each project card (`year`, `metric`)
- [x] Trim skills to core tools, rest in an "also used" line (WebRTC, WebSockets, Redis, Celery kept as core)
- [x] Rewrite experience bullets to lead with a bolded outcome
- [x] Publication was not rendered anywhere; now shown as a fact row in Profile

## Major (4+ hours)

- [ ] Graas voice-AI case study with an architecture diagram
- [ ] Replace the placeholder demo video: overwrite `public/projects/demo-placeholder.webm` or change `"video"` on the Voice Calling Agent project (modal and "Watch demo" button already wired)
- [ ] Public repo or technical post as proof (latency chart)
- [ ] Run Lighthouse on the live site and fix findings
- [ ] Confirm `projects/placeholder.png` and `suyash.jpg` return 200 on the real domain

## Needs input from Suyash

- Screenshots or a demo clip per project
- Year and one measurable result per project
