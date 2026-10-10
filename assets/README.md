# Profile assets

- `profile-banner.svg` is a self-contained SVG with a vectorized version of the supplied avatar. It has no external fonts, images, or scripts.
- `avatar-transparent.png` is the background-removed source derivative. Only border-connected near-white pixels and disconnected background artifacts are removed; white details inside the avatar are preserved.
- `hero-lab-sharp.svg` is the previous banner, retained for reference.

To rebuild the avatar and banner, install Pillow and run:

```sh
python3 scripts/build-banner.py /path/to/avatar.jpeg
```

The profile uses the open-source [Skill Icons](https://github.com/tandpfun/skill-icons) service for C, C++, and Python, and [Readme Typing SVG](https://github.com/DenverCoder1/readme-typing-svg) for its two-line welcome animation.

The `Generate contribution snake` workflow uses [Platane/snk](https://github.com/Platane/snk) to generate light and dark contribution animations. It runs daily at 02:23 UTC, can be started manually from GitHub Actions, and runs when its workflow file is pushed to `main`. Generated images are published to the `output` branch, not the source branch.

The snake links become available after the first successful workflow run. GitHub Actions must be enabled for this repository. Theme variants are selected using the README's `picture` elements.
