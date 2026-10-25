# AGENTS.md

Working instructions for coding agents in this repository — `ksiazka-kucharska`.

This is a standalone Git repository nested inside the parent `Code` workspace,
structured similarly to `hiragana-study`.

---

## 1. The Project

A standalone digital cookbook & archive preserving handwritten family recipes:
1. **Interactive Web App (PWA)**: Vanilla JavaScript, CSS, HTML, Service Worker.
   No framework, no build step, no npm/node dependencies. Published to GitHub Pages.
2. **Printable PDF Book**: 300-page A4 cookbook generated via Python (`generate_pdf_book.py`).

### Repository Structure

```text
index.html                    App shell (PWA)
app.js                        Application logic (offline cache, search, kitchen mode, converter)
style.css                     Warm vintage styling, dark/light themes, typography
sw.js                         Service Worker for full offline caching (przepisnik-v1)
manifest.json                 Web App Manifest for mobile installation
recipes.json                  Structured database of 144 recipes
icons/                        PWA icons (192px, 512px)
images/                       154 upright, high-resolution original recipe scans
ksiazka_kucharska.pdf         Compiled 300-page printable PDF cookbook
generate_pdf_book.py          Python script compiling recipes into A4 PDF
start_offline.command         Click-to-launch local server on macOS (port 8080)
bundle_for_sharing.py         Helper script creating a standalone distribution ZIP
.nojekyll                     Bypasses Jekyll processing on GitHub Pages
.github/workflows/deploy.yml  Automated deployment to GitHub Pages on push to main
```

---

## 2. Ground Rules

1. **Keep it Dependency-Free**: Do not introduce frameworks (React, Vue) or build tools (Vite, Webpack) unless explicitly requested. The zero-build architecture is deliberate.
2. **Relative Paths**: Always use relative URLs (`./` or `style.css`, `images/...`) so the app works seamlessly both locally and under GitHub Pages subpaths (`https://<user>.github.io/ksiazka-kucharska/`).
3. **PWA & Offline Integrity**: Any changes to core assets must be reflected in `sw.js` cache definitions.
4. **Git Discipline**:
   - Work committed here must only belong to `ksiazka-kucharska`.
   - Never stage parent `Code` workspace files from this repository.
   - Large generated archives (`*.zip`) remain gitignored.

---

## 3. Verification

1. **Local Test**: Run `./start_offline.command` or `python3 -m http.server 8080`.
2. **Browser Check**: Open `http://localhost:8080`, verify search, filters, modal popups, image display, and PDF download.
