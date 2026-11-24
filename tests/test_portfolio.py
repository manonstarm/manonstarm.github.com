"""Check that the portfolio's four navigation links lead to real content."""

from html.parser import HTMLParser
import unittest

from test_animated_embed import ROOT


class Portfolio(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.targets = {}
        self.in_nav = False
        self.in_link = False
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "nav":
            self.in_nav = True
        if tag == "a" and self.in_nav:
            self.links.append([attrs.get("href"), ""])
            self.in_link = True
        if element_id := attrs.get("id"):
            self.targets["#" + element_id] = tag

    def handle_data(self, data):
        if self.in_link:
            self.links[-1][1] += data

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_link = False
        if tag == "nav":
            self.in_nav = False


class PortfolioTests(unittest.TestCase):
    def test_navigation_has_only_the_requested_labels(self):
        page = Portfolio((ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertEqual([label.strip() for _, label in page.links], ["Works", "About", "CV", "Contact"])

    def test_navigation_points_to_four_distinct_sections(self):
        page = Portfolio((ROOT / "index.html").read_text(encoding="utf-8"))
        targets = {href for href, _ in page.links}
        self.assertEqual(len(targets), 4)
        for target in targets:
            with self.subTest(target=target):
                self.assertEqual(page.targets.get(target), "section")
