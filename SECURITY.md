# Security notes

## Architecture in one paragraph

Static files only. No server code, no database, no accounts, no cookies, no
stored data, no API keys and no dependency manifest. The browser loads
HTML/CSS/JS from the same origin plus three third-party resources: Google
Fonts (CSS and font files), Three.js from cdnjs (the homepage 3D image) and
an optional Google Maps embed on the contact page. Customer input (quote and
contact forms) is turned into a WhatsApp link that the visitor's own browser
opens; it is not transmitted to any server we operate.

## What is in place

- Content Security Policy (via `<meta>`): same-origin scripts plus cdnjs only, no inline scripts, no `eval`, no plugins, outbound requests limited to same origin, framing limited to Google (maps).
- Referrer policy `strict-origin-when-cross-origin`.
- No `innerHTML` for anything built from visitor input; data rendered into templates is escaped.
- The WhatsApp number is fixed configuration. Forms can only supply message text, which is URL encoded.
- Input limits and format checks on every form field.
- All `target="_blank"` links use `rel="noopener"`.
- `.gitignore` blocks `.env`, keys and credentials. `_config.yml` keeps tooling out of the published site.

## What cannot be done on GitHub Pages

GitHub Pages does not let a repository set HTTP response headers, so these are
not enforced today: `X-Frame-Options` / CSP `frame-ancestors` (clickjacking
protection), `Strict-Transport-Security` (GitHub already serves HTTPS and
redirects, but cannot be told to pin it), `X-Content-Type-Options` and
`Permissions-Policy`. `_headers` contains the full recommended set; it takes
effect if the site moves to Netlify or Cloudflare Pages, or sits behind
Cloudflare.

## Open item

The Three.js script from cdnjs has no Subresource Integrity hash because a
correct hash could not be computed offline. To add one, run:

```bash
curl -s https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js | openssl dgst -sha384 -binary | openssl base64 -A
```

and add `integrity="sha384-<result>"` to the script tag in `build.py`, then
rebuild. Alternatively download the file and serve it from `js/`, then remove
the cdnjs host from the CSP.
