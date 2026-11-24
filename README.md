# manonstarm.github.com

Source for [manon.lebrun.design](http://manon.lebrun.design)

## Artwork embed

`index.html` displays one responsive illustration using a local `<picture>`: browsers that support WebP select `whimsical_girl_loop_v2.webp`, while the `<img>` uses `whimsical_girl_loop_v2.gif` as its fallback. When `prefers-reduced-motion: reduce` matches, the first source selects the non-animated `whimsical_girl_loop_v2_still.png` instead. The image retains the descriptive alternative text and 1200 × 885 intrinsic dimensions from `embedded.html`; its rendered width fits the page. The former JPEG and SVG/CSS motion overlay are not displayed. `embedded.html` remains the supplied reference snippet, not the full page embed (which adds the reduced-motion source).

Keep `index.html` and all three referenced artwork assets together at the same directory level when serving the page. The original `whimsicle_girl.jpg` and `embedded.html` remain in the repository but are not required by the displayed image. No build step or external runtime dependency is needed for this static page.

To preview locally, open `index.html` in a browser at desktop and narrow viewport widths; use the browser's reduced-motion emulation to inspect the still. To run the local HTML contract checks from the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_animated_embed.py' -v
```

The checks verify the source/fallback structure, snippet alt and dimensions, local paths, reduced-motion still, and removal of the old display and overlay. Browser rendering and animation/fallback behavior need separate visual checks; the unit tests do not validate those. No HTML linter or dependency scanner is configured here. These changes have only been checked locally; this documentation does not imply that the updated page has been deployed.

