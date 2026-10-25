#!/usr/bin/env python3
"""
generate_pdf_book.py
Generuje kompletną, elegancką książkę kucharską w formacie PDF (A4)
na podstawie 110 przepisów z recipes.json i zdjęć z images_upright/.
"""

import json
import os
import subprocess

def generate_html_book():
    with open("recipes.json", "r", encoding="utf-8") as f:
        recipes = json.load(f)

    # Group recipes by category in logical dining order:
    category_order = [
        "Zupy",
        "Dania główne",
        "Sałatki i surówki",
        "Sosy i dodatki",
        "Ciasta i wypieki",
        "Desery i słodkości",
        "Przetwory"
    ]

    recipes_by_cat = {cat: [] for cat in category_order}
    for r in recipes:
        cat = r.get("category", "Dania główne")
        if cat in recipes_by_cat:
            recipes_by_cat[cat].append(r)
        else:
            recipes_by_cat.setdefault("Dania główne", []).append(r)

    # Sort recipes alphabetically within categories
    for cat in recipes_by_cat:
        recipes_by_cat[cat].sort(key=lambda x: x["title"])

    abs_img_dir = os.path.abspath("images")

    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>Rodzinny Przepiśnik - Skarbnica Domowych Smaków</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400;1,600&display=swap');

    @page {{
      size: A4 portrait;
      margin: 15mm 15mm 18mm 15mm;
      @bottom-right {{
        content: counter(page);
        font-family: 'Outfit', sans-serif;
        font-size: 8pt;
        color: #887a6d;
      }}
      @bottom-left {{
        content: "Rodzinny Przepiśnik • Skarbnica Domowych Smaków";
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 8pt;
        color: #887a6d;
      }}
    }}

    @page :first {{
      margin: 0;
      @bottom-right {{ content: normal; }}
      @bottom-left {{ content: normal; }}
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Outfit', sans-serif;
      color: #2b2118;
      background: #ffffff;
      line-height: 1.5;
      font-size: 9.5pt;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    /* COVER PAGE */
    .cover-page {{
      width: 100vw;
      height: 100vh;
      page-break-after: always;
      background: radial-gradient(circle at center, #fffbf2 0%, #f4ede0 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 50mm 25mm;
      position: relative;
      border: 12mm solid #36261a;
      outline: 1.5mm solid #c98020;
      outline-offset: -7mm;
    }}

    .cover-ornament-top {{
      font-size: 24pt;
      color: #c98020;
      margin-bottom: 8mm;
    }}

    .cover-subtitle-top {{
      font-family: 'Outfit', sans-serif;
      text-transform: uppercase;
      letter-spacing: 4px;
      font-size: 11pt;
      color: #7d6e60;
      margin-bottom: 6mm;
      font-weight: 600;
    }}

    .cover-main-title {{
      font-family: 'Cinzel', 'Playfair Display', serif;
      font-size: 36pt;
      font-weight: 800;
      letter-spacing: 2px;
      color: #221811;
      line-height: 1.15;
      margin-bottom: 6mm;
    }}

    .cover-tagline {{
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 16pt;
      color: #bd4a30;
      margin-bottom: 12mm;
    }}

    .cover-divider {{
      width: 120px;
      height: 2px;
      background: linear-gradient(90deg, transparent, #c98020, transparent);
      margin: 0 auto 12mm;
    }}

    .cover-desc {{
      max-width: 140mm;
      font-size: 11pt;
      line-height: 1.7;
      color: #55473a;
      margin-bottom: 18mm;
    }}

    .cover-footer {{
      margin-top: auto;
      font-size: 9.5pt;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #8c7d6f;
      font-weight: 600;
    }}

    /* INTRO PAGE */
    .intro-page {{
      page-break-after: always;
      padding: 10mm 5mm;
    }}

    .intro-title {{
      font-family: 'Playfair Display', serif;
      font-size: 24pt;
      color: #bd4a30;
      text-align: center;
      margin-bottom: 2mm;
      font-weight: 700;
    }}

    .intro-subtitle {{
      text-align: center;
      font-size: 10pt;
      color: #8c7d6f;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 8mm;
    }}

    .intro-body {{
      font-size: 10.5pt;
      line-height: 1.75;
      color: #3b2f25;
      column-count: 2;
      column-gap: 10mm;
      text-align: justify;
    }}

    .intro-body p {{
      margin-bottom: 4mm;
    }}

    /* TABLE OF CONTENTS */
    .toc-page {{
      page-break-after: always;
      padding: 10mm 5mm;
    }}

    .toc-title {{
      font-family: 'Playfair Display', serif;
      font-size: 24pt;
      color: #2b2118;
      text-align: center;
      margin-bottom: 2mm;
    }}

    .toc-ornament {{
      text-align: center;
      color: #c98020;
      font-size: 14pt;
      margin-bottom: 6mm;
    }}

    .toc-grid {{
      column-count: 2;
      column-gap: 12mm;
    }}

    .toc-category {{
      break-inside: avoid;
      margin-bottom: 6mm;
    }}

    .toc-category-header {{
      font-family: 'Playfair Display', serif;
      font-size: 12.5pt;
      font-weight: 700;
      color: #bd4a30;
      border-bottom: 1.5px solid #bd4a30;
      padding-bottom: 1.5mm;
      margin-bottom: 2.5mm;
    }}

    .toc-item {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      font-size: 8.8pt;
      line-height: 1.45;
      margin-bottom: 1.5mm;
      color: #382c22;
    }}

    .toc-item-title {{
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 4px;
    }}

    /* RECIPE PAGE */
    .recipe-page {{
      page-break-after: always;
      padding-top: 2mm;
      display: flex;
      flex-direction: column;
      height: 265mm;
    }}

    .recipe-header {{
      border-bottom: 2px solid #36261a;
      padding-bottom: 3mm;
      margin-bottom: 4mm;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }}

    .recipe-header-left {{
      flex: 1;
    }}

    .recipe-category-tag {{
      display: inline-block;
      font-size: 8pt;
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 700;
      color: #bd4a30;
      margin-bottom: 1mm;
    }}

    .recipe-title {{
      font-family: 'Playfair Display', serif;
      font-size: 18pt;
      font-weight: 700;
      line-height: 1.2;
      color: #221811;
    }}

    .recipe-meta-row {{
      display: flex;
      gap: 3mm;
      margin-top: 2mm;
      font-size: 8.5pt;
      color: #635345;
      font-weight: 500;
    }}

    .recipe-meta-badge {{
      background: #f5ede1;
      padding: 1mm 2.5mm;
      border-radius: 3px;
      border: 0.5px solid #ded3c1;
    }}

    /* RECIPE MAIN COLUMNS */
    .recipe-cols {{
      display: grid;
      grid-template-columns: 72mm 1fr;
      gap: 7mm;
      flex: 1;
    }}

    .col-title {{
      font-family: 'Playfair Display', serif;
      font-size: 11pt;
      font-weight: 700;
      color: #bd4a30;
      border-bottom: 1px solid #e0d5c3;
      padding-bottom: 1.5mm;
      margin-bottom: 2.5mm;
      display: flex;
      align-items: center;
      gap: 2mm;
    }}

    /* Ingredients column */
    .ingredients-col {{
      background: #faf7f0;
      border: 1px solid #e8ded0;
      border-radius: 4px;
      padding: 3.5mm 4mm;
      display: flex;
      flex-direction: column;
    }}

    .ing-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 1.8mm;
      font-size: 8.8pt;
      line-height: 1.35;
    }}

    .ing-list li {{
      display: flex;
      align-items: baseline;
      gap: 2mm;
    }}

    .ing-bullet {{
      color: #c98020;
      font-size: 9pt;
      line-height: 1;
    }}

    .ing-qty {{
      font-weight: 700;
      color: #2b2118;
      white-space: nowrap;
    }}

    .ing-name {{
      color: #44372c;
    }}

    /* Instructions & Photos column */
    .instructions-col {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .steps-list {{
      display: flex;
      flex-direction: column;
      gap: 2.5mm;
    }}

    .step-row {{
      display: flex;
      gap: 2.5mm;
      font-size: 8.8pt;
      line-height: 1.45;
      text-align: justify;
    }}

    .step-num {{
      width: 17px;
      height: 17px;
      background: #bd4a30;
      color: #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 7.5pt;
      font-weight: 700;
      flex-shrink: 0;
      margin-top: 1px;
    }}

    .step-text {{
      flex: 1;
      color: #2b2118;
    }}

    /* Family tips box */
    .recipe-tips-box {{
      background: #fff8eb;
      border-left: 3px solid #c98020;
      padding: 2.5mm 3.5mm;
      margin-top: 3mm;
      border-radius: 0 4px 4px 0;
      font-size: 8.2pt;
      line-height: 1.4;
      color: #524233;
    }}

    .recipe-tips-title {{
      font-weight: 700;
      color: #c98020;
      margin-bottom: 1mm;
      display: flex;
      align-items: center;
      gap: 1.5mm;
      font-size: 8.5pt;
    }}

    /* Manuscript photo thumbnail at bottom */
    .manuscript-footer-box {{
      margin-top: 3mm;
      border-top: 1px dashed #d9ccb8;
      padding-top: 2.5mm;
      display: flex;
      align-items: center;
      gap: 3mm;
    }}

    .manuscript-img-box {{
      width: 48mm;
      height: 28mm;
      border-radius: 3px;
      overflow: hidden;
      border: 1px solid #cfc2ad;
      background: #eee6d8;
      flex-shrink: 0;
    }}

    .manuscript-img-box img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}

    .manuscript-caption {{
      font-size: 7.8pt;
      line-height: 1.35;
      color: #706254;
    }}

    .manuscript-caption strong {{
      color: #2b2118;
      display: block;
      margin-bottom: 0.5mm;
    }}
  </style>
</head>
<body>

  <!-- OKŁADKA -->
  <div class="cover-page">
    <div class="cover-ornament-top">❦ ❧</div>
    <div class="cover-subtitle-top">Kolekcja Dziedzictwa Kulinarnego</div>
    <h1 class="cover-main-title">RODZINNY PRZEPIŚNIK</h1>
    <div class="cover-tagline">Skarbnica Tradycyjnych Domowych Smaków</div>
    <div class="cover-divider"></div>
    <p class="cover-desc">
      Kompletny zbiór {len(recipes)} sprawdzonych receptur kulinarnych zebranych z rękopisów,
      domowych zapisków i zeszytów babcinych. Autentyczne receptury na zupy, dania mięsne,
      wystawne ciasta, desery, sałatki oraz przetwory na zimę wraz z oryginalnymi kartami odręcznymi.
    </p>
    <div class="cover-footer">Wydanie Pamiątkowe • Domowe Archiwum Kulinarne</div>
  </div>

  <!-- WSTĘP -->
  <div class="intro-page">
    <h2 class="intro-title">Od Autorów</h2>
    <div class="intro-subtitle">Ocalić od zapomnienia smaki rodzinnego domu</div>
    <div class="intro-body">
      <p>
        W każdej rodzinie istnieje miejsce szczególne – szuflada w kredensie lub tekturowe pudełko,
        w którym przez dziesięciolecia gromadziły się skrawki papieru. Zapisywano na nich to, co najcenniejsze:
        receptury na potrawy, które gromadziły bliskich wokół niedzielnego stołu, ciasta pieczone na Boże Narodzenie
        oraz przetwory zamykające zapach letnich owoców w słoikach na długie zimowe wieczory.
      </p>
      <p>
        Wśród zebranych w tej księdze kart odnajdziemy notatki sporządzane w biegu – na odwrocie lekarskich bloczków,
        firmowych karteczkach czy wyrwanych kartkach z zeszytów w kratkę. Każdy z tych rękopisów kryje w sobie
        nie tylko gramatury mąki, cukru czy przypraw, ale przede wszystkim cząstkę rodzinnej historii, ciepła i troski.
      </p>
      <p>
        Tworząc ten przepiśnik, postawiliśmy sobie za cel zachowanie pełnej autentyczności receptur przy jednoczesnym
        nadaniu im nowoczesnej, przejrzystej i wygodnej formy. Każdy przepis został precyzyjnie przepisany,
        uporządkowany krok po kroku oraz wzbogacony o miniatury oryginalnego rękopisu, pozwalające powrócić do źródeł.
      </p>
      <p>
        Życzymy Państwu wspaniałych chwil spędzonych przy wspólnym gotowaniu i odkrywaniu na nowo smaków, które
        nie przemijają!
      </p>
    </div>
  </div>

  <!-- SPIS TREŚCI -->
  <div class="toc-page">
    <h2 class="toc-title">Spis Treści</h2>
    <div class="toc-ornament">❦</div>
    <div class="toc-grid">
"""

    for cat in category_order:
        cat_recipes = recipes_by_cat[cat]
        if not cat_recipes:
            continue
        html += f"""
      <div class="toc-category">
        <div class="toc-category-header">{cat} ({len(cat_recipes)})</div>
"""
        for r in cat_recipes:
            html += f"""
        <div class="toc-item">
          <span class="toc-item-title">• {r['title']}</span>
        </div>
"""
        html += "      </div>\n"

    html += """
    </div>
  </div>
"""

    # RECIPE PAGES
    for r in recipes:
        img_name = r.get("image", "")
        img_full_path = os.path.join(abs_img_dir, img_name) if img_name else ""
        img_file_url = f"file://{img_full_path}" if os.path.exists(img_full_path) else ""

        # Format ingredients
        ings_html = ""
        for ing in r.get("ingredients", []):
            amt = ing.get("amount", "")
            unit = ing.get("unit", "")
            qty_str = f"{amt} {unit}".strip()
            item = ing.get("item", "")
            ings_html += f"""
            <li>
              <span class="ing-bullet">•</span>
              <div><span class="ing-qty">{qty_str}</span> <span class="ing-name">{item}</span></div>
            </li>
"""

        # Format instructions
        steps_html = ""
        for i, step in enumerate(r.get("instructions", [])):
            steps_html += f"""
            <div class="step-row">
              <div class="step-num">{i+1}</div>
              <div class="step-text">{step}</div>
            </div>
"""

        # Tips
        tips = r.get("tips", [])
        tips_html = ""
        if tips:
            tips_text = " ".join(tips) if isinstance(tips, list) else str(tips)
            tips_html = f"""
            <div class="recipe-tips-box">
              <div class="recipe-tips-title">💡 Wskazówki Babci:</div>
              <div>{tips_text}</div>
            </div>
"""

        # Manuscript footer
        manuscript_html = ""
        if img_file_url:
            manuscript_html = f"""
            <div class="manuscript-footer-box">
              <div class="manuscript-img-box">
                <img src="{img_file_url}" alt="Rękopis {r['title']}">
              </div>
              <div class="manuscript-caption">
                <strong>Oryginalna notatka z archiwum ({img_name}):</strong>
                Autentyczny rękopis, na bazie którego zredagowano powyższą recepturę.
              </div>
            </div>
"""

        html += f"""
  <!-- STRONA PRZEPISU: {r['title']} -->
  <div class="recipe-page">
    <div class="recipe-header">
      <div class="recipe-header-left">
        <div class="recipe-category-tag">{r.get('category', 'Dania główne')}</div>
        <h2 class="recipe-title">{r['title']}</h2>
        <div class="recipe-meta-row">
          <span class="recipe-meta-badge">⏱️ Przygotowanie: {r.get('prep_time', '20 min')}</span>
          <span class="recipe-meta-badge">🔥 Gotowanie/Pieczenie: {r.get('cook_time', '30 min')}</span>
          <span class="recipe-meta-badge">🍽️ Porcje: {r.get('servings', 4)}</span>
          <span class="recipe-meta-badge">⭐ Poziom: {r.get('difficulty', 'Średni')}</span>
        </div>
      </div>
    </div>

    <div class="recipe-cols">
      <div class="ingredients-col">
        <div class="col-title">Składniki</div>
        <ul class="ing-list">
          {ings_html}
        </ul>
      </div>

      <div class="instructions-col">
        <div>
          <div class="col-title">Sposób przygotowania</div>
          <div class="steps-list">
            {steps_html}
          </div>
          {tips_html}
        </div>
        {manuscript_html}
      </div>
    </div>
  </div>
"""

    html += """
</body>
</html>
"""

    temp_html = "cookbook_print.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html)

    print("📄 Wygenerowano szablon HTML (cookbook_print.html)...")
    print("⏳ Kompilacja książki PDF przez Google Chrome (to może zająć ok. 15-20 sekund)...")

    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    pdf_out = "ksiazka_kucharska.pdf"
    html_abs_url = "file://" + os.path.abspath(temp_html)

    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_out}",
        html_abs_url
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)

    # Clean up temporary HTML file
    if os.path.exists(temp_html):
        os.remove(temp_html)

    if res.returncode == 0 and os.path.exists(pdf_out):
        size_mb = os.path.getsize(pdf_out) / (1024 * 1024)
        print(f"🎉 SUKCES! Utworzono kompletną książkę kucharską: {pdf_out} ({size_mb:.1f} MB)")
    else:
        print(f"❌ Błąd kompilacji PDF. Kod powrotu: {res.returncode}")
        if res.stderr:
            print("Stderr:", res.stderr)

if __name__ == "__main__":
    generate_html_book()
