## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Project conventions

This is a Korean-language personal dev blog. Read `README.md` first — it documents
the image workflow, the theme system, and the deploy setup.

- **Write user-facing text in Korean.** Post bodies, page copy, and `description`
  fields are Korean. Code identifiers, file names, and frontmatter keys stay English.
  The terminal-style nav labels (`home` / `posts` / `about`) are intentionally
  English — they read as shell commands, which is the design intent.
- **Never hardcode colors.** Every color is a CSS custom property defined in
  `src/styles/global.css`, in two sets: `:root` (light) and
  `html[data-theme='dark']`. Edit both together or theme switching breaks.
- **Keep the theme script inline.** `BaseHead.astro` sets `data-theme` via a
  synchronous `is:inline` script in `<head>`. Deferring or bundling it causes a
  white flash for dark-mode readers (FOUC).
- **Images live under `src/assets/`**, referenced by relative path so Astro
  optimizes them and fails the build on a bad path. Do not put post images in
  `public/`.
- **Do not lower `node-version: 22`** in `.github/workflows/deploy.yml`.
  `withastro/action` defaults to Node 20, but astro 7 requires >= 22.12.0.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)
