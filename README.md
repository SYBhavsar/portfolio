# Suyash Bhavsar — Portfolio

Static portfolio site (HTML, CSS, vanilla JS). Content lives in `src/data/portfolio.json`.

## Run locally

```bash
python3 tools/serve.py   # http://127.0.0.1:8080
```

## Edit content

Edit `src/data/portfolio.json`, then rebuild `index.html`:

```bash
python3 tools/personalize.py
```

`src/template.html` holds the page markup with `{{placeholders}}`; the script fills them from the JSON. Per-project screenshots: set a project's `"image"` to a file under `public/` (otherwise `/projects/placeholder.png` is used).
