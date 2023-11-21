"""rm -rf doc/_generated/; sphinx-build doc build/sphinx/html -E -a
"""

from ewoksserver import __version__

project = "ewoksserver"
version = ".".join(__version__.split(".")[:2])  # MAJOR.MINOR
copyright = "2021-2023, ESRF"
author = "ESRF"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinxcontrib.redoc",
    "sphinx_autodoc_typehints",
    "sphinx_design",
]
templates_path = ["_templates"]
exclude_patterns = []

always_document_param_types = True

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://gitlab.esrf.fr/workflow/ewoks/ewoksserver",
    "use_repository_button": True,
}
html_static_path = []

autosummary_generate = True
autodoc_default_flags = [
    "members",
    "undoc-members",
    "show-inheritance",
]

redoc = [
    {
        "name": "Ewoks API",
        "page": "restapi",
        "spec": "spec.json",
        "embed": True,
        "opts": {
            "required-props-first": True,
            "expand-responses": ["200"],
        },
    },
]

redoc_uri = "https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"
