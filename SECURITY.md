# Security policy

## Reporting a problem

If you find a security problem, such as a leaked secret, an unsafe instruction in the skill text, a dangerous script or a vulnerable dependency, please report it privately with **GitHub's private vulnerability reporting** on this repository (Security tab → "Report a vulnerability"). Please don't open a public issue for it.

Include the file and line, what an agent or user would do because of it, and how to reproduce it. We aim to reply within 7 days. This is a small, volunteer-run project, so there is no bug bounty.

## What Motionite does

- `SKILL.md`, `styles/` and `techniques/` are plain Markdown. They tell an agent how to plan and build a Remotion video. The only commands they suggest are local: `npx remotion still|render`, `ffmpeg`/`ffprobe`, and short Python/Pillow QA snippets that read and write files under the project's `out/` folder.
- `examples/` is a Remotion 4 project. It loads fonts and images only from its own `public/` folder and makes no network requests while rendering.
- `scripts/` holds local helpers that build the README images, render the stills and check Markdown links. `check-links.py --external` sends HEAD/GET requests to the links in the docs, and only when you pass that flag.

## What it does not do

- It never asks an agent to download and run remote code (`curl | sh`), install global tools, use `sudo`, read credentials, tokens or environment files, send data anywhere, or turn off safety controls.
- It holds no secrets and needs no API keys or accounts.
- It has no telemetry and runs no post-install scripts of its own.

## Using it safely

- Treat the skill like any third-party agent instruction: review `SKILL.md` before you give it to an agent that has shell access, and keep that agent in a sandbox or project folder.
- Install the example with `npm ci`, which uses the pinned versions in `examples/package-lock.json`. Remotion has its own license terms (<https://www.remotion.dev/license>).
