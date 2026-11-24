"""Public HTML contract for the supplied animated artwork embed.

Run from the repository root: python3 -m unittest discover -s tests -p 'test_animated_embed.py' -v
No third-party test dependencies or network access are required.
"""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Elements(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.nodes = []
        self.stack = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        ancestors = tuple(self.stack)
        self.nodes.append((tag, dict(attrs), ancestors))
        if tag not in {"source", "img", "meta", "link", "br", "input", "hr"}:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[: len(self.stack) - 1 - self.stack[::-1].index(tag)]

    def find(self, tag):
        return [(attrs, ancestors) for name, attrs, ancestors in self.nodes if name == tag]


class AnimatedArtworkEmbedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.page = Elements(cls.html)

    def test_one_figure_contains_webp_source_and_gif_fallback(self):
        figures = self.page.find("figure")
        self.assertEqual(len(figures), 1, "display one artwork figure")
        self.assertEqual(len(self.page.find("picture")), 1, "display one picture")
        sources = self.page.find("source")
        images = self.page.find("img")
        self.assertEqual(len(sources), 2, "static reduced-motion source plus animated WebP")
        self.assertEqual(len(images), 1, "display one image, not a doubled layer")
        source, source_parents = sources[1]
        image, image_parents = images[0]
        self.assertIn("figure", source_parents)
        self.assertIn("picture", source_parents)
        self.assertIn("figure", image_parents)
        self.assertIn("picture", image_parents)
        self.assertEqual(source.get("type"), "image/webp")
        self.assertEqual(source.get("srcset"), "whimsical_girl_loop_v2.webp")
        self.assertEqual(image.get("src"), "whimsical_girl_loop_v2.gif")

    def test_fallback_keeps_description_and_intrinsic_dimensions(self):
        image = self.page.find("img")[0][0]
        self.assertEqual(
            image.get("alt"),
            "Watercolour illustration of a whimsical girl winking as her hair drifts "
            "in a breeze, with swirling spirals and blinking circles around her",
        )
        self.assertEqual((image.get("width"), image.get("height")), ("1200", "885"))

    def test_reduced_motion_selects_local_still_before_animated_sources(self):
        sources = [attrs for attrs, _ in self.page.find("source")]
        self.assertEqual(len(sources), 2, "a still must precede animated WebP")
        still, animated = sources
        self.assertEqual(still.get("media"), "(prefers-reduced-motion: reduce)")
        self.assertEqual(still.get("type"), "image/png")
        self.assertEqual(still.get("srcset"), "whimsical_girl_loop_v2_still.png")
        self.assertIsNone(animated.get("media"), "normal motion still selects animated WebP")
        path = ROOT / still["srcset"]
        self.assertTrue(path.is_file(), "reduced-motion image must be local")
        self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n", "still must not animate")

    def test_old_jpg_is_not_displayed(self):
        self.assertNotIn("whimsicle_girl.jpg", [attrs.get("src") for attrs, _ in self.page.find("img")])

    def test_svg_motion_overlay_is_removed(self):
        self.assertFalse(self.page.find("svg"), "animated asset must not be doubled by SVG")
        self.assertNotIn("data-motion", self.html)
        self.assertNotIn("@keyframes", self.html, "remove the old CSS motion overlay")

    def test_artwork_paths_are_local_existing_assets(self):
        for tag, attr in (("source", "srcset"), ("img", "src")):
            with self.subTest(tag=tag):
                for attrs, _ in self.page.find(tag):
                    value = attrs[attr]
                    parsed = urlsplit(value)
                    self.assertFalse(parsed.scheme or parsed.netloc or value.startswith("/"), value)
                    self.assertTrue((ROOT / parsed.path).is_file(), value)


if __name__ == "__main__":
    unittest.main()
