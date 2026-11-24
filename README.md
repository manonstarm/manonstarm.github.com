# manonstarm.github.com

Source for [manon.lebrun.design](https://manon.lebrun.design), the portfolio of Manon Spruth-Lebrun.

## Portfolio

`index.html` contains the Works, About, CV and Contact sections. Replace the CV and Contact notices with approved copy when available.

The featured illustration scales without cropping. Its local `<picture>` selects the animated WebP with a GIF fallback, or the still PNG when the visitor prefers reduced motion. Keep the three referenced artwork files alongside `index.html`. No build step or external runtime dependency is needed.

To preview locally, open `index.html` in a browser. To check the navigation and artwork markup, run from the repository root:

```sh
python3 -B -m unittest discover -s tests -v
```
