# rafa1771.github.io

Rafael Rivlin's bilingual (English / Spanish) CV, live at <https://rafa1771.github.io/>.

It is also a small demonstration of [HTMX](https://htmx.org/): there is no framework, no bundler and no client-side rendering. Every page is plain HTML, and HTMX only handles the language switch.

## How it works

- **The full page is in the first response.** `/` and `/en/` serve the English CV and `/es/` serves the Spanish one. Everything is in the HTML as delivered, so it loads fast, works without JavaScript, and is readable by link-preview scrapers, search engines and AI crawlers.
- **HTMX swaps the language.** The ES / EN links are ordinary `<a href>` elements with HTMX attributes:

  ```html
  <a href="/es/" hx-get="/content-es.html" hx-target="#content" hx-push-url="/es/">ES</a>
  ```

  With JavaScript, HTMX fetches the Spanish fragment, swaps it into `#content` and pushes `/es/` into the address bar, so Back/Forward and shared links work. Without JavaScript, the link simply navigates to `/es/`.
- **Per-language metadata.** Each page has its own `<title>`, description, Open Graph tags, `canonical` and `hreflang` links, so previews match the reader's language. A short script keeps `<html lang>`, the title and the dark-mode label in step after a swap.

## Project layout

| File | Purpose |
| --- | --- |
| `content-en.html`, `content-es.html` | **The copy.** The only files to edit for content changes. Served as-is to HTMX and inlined into the full pages. |
| `build.py` | Page template and build script (Python 3, standard library only). |
| `index.html`, `en/index.html`, `es/index.html` | **Generated** by `build.py`. Don't edit by hand. |
| `styles.css` | Styles, including the light and dark themes. |
| Icons, `site.webmanifest`, `SlackProfilePic.png` | Favicons, PWA manifest and the Open Graph image. |

Dependencies are loaded from CDNs and pinned with Subresource Integrity hashes: HTMX 2.0.11 (unpkg) and Font Awesome 7.3.1 (cdnjs). Fonts come from Google Fonts.

## Editing

1. Edit `content-en.html` and/or `content-es.html`. Use absolute paths for assets (`/SlackProfilePic.png`), since the content is served from `/`, `/en/` and `/es/`.
2. Regenerate the pages:

   ```sh
   python3 build.py
   ```

3. Preview locally:

   ```sh
   python3 -m http.server 8000
   ```

   Then open <http://localhost:8000/>, <http://localhost:8000/en/> and <http://localhost:8000/es/>.

To change page metadata, the template, or a pinned library version, edit `build.py` and rebuild. When updating a CDN version, also update its `integrity` hash.

## Deploying

The site is static and hosted on GitHub Pages from the `main` branch root.

1. Run `python3 build.py` and commit the regenerated `index.html`, `en/index.html` and `es/index.html` together with your change. Pages does not run the build, so the generated files must be committed.
2. Push to `main`:

   ```sh
   git add -A
   git commit -m "Update CV"
   git push origin main
   ```

3. GitHub Pages publishes within a minute or two.
4. If the Open Graph preview doesn't refresh, link scrapers (Slack, LinkedIn, Facebook) cache aggressively, so re-scrape the URL with their debugger tools.

One-time setup: in the repository's **Settings → Pages**, set the source to **Deploy from a branch**, with branch `main` and folder `/ (root)`.
