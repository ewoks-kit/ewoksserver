"""rm -rf doc/_generated/; sphinx-build doc build/sphinx/html -E -a
"""

import importlib.metadata

release = importlib.metadata.version("ewoksserver")

project = "ewoksserver"
version = ".".join(release.split(".")[:2])  # MAJOR.MINOR
copyright = "2021-2024, ESRF"
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

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "icon_links": [
        {
            "name": "gitlab",
            "url": "https://gitlab.esrf.fr/workflow/ewoks/ewoksserver",
            "icon": "fa-brands fa-gitlab",
        },
        {
            "name": "pypi",
            "url": "https://pypi.org/project/ewoksserver/",
            "icon": "fa-brands fa-python",
        },
    ],
    "navbar_start": ["navbar_start"],
    "footer_start": ["copyright"],
    "footer_end": ["footer_end"],
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
