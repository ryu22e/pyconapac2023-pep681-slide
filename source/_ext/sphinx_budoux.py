"""Sphinx Extension for automatic formatting."""
from __future__ import annotations

import itertools

import budoux
from bs4 import BeautifulSoup
from sphinx.addnodes import document
from sphinx.application import Sphinx


def html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: document | None,
) -> None:
    if not doctree:
        return

    parser = budoux.load_default_japanese_parser()
    soup = BeautifulSoup(context["body"], "html.parser")
    tags = itertools.chain.from_iterable(
        (soup.find_all(target_tag) for target_tag in app.config["budoux_target_tags"])
    )
    for tag in tags:
        tag.string = parser.translate_html_string(str(tag))
        tag.unwrap()
    context["body"] = soup.prettify(formatter=None)  # type: ignore


def setup(app):
    app.add_config_value("budoux_target_tags", [], "html")
    app.connect("html-page-context", html_page_context)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
