"""rm -rf doc/_generated/; python setup.py build_sphinx -E -a
"""

project = "ewoksserver"
release = "0.1"
copyright = "2021, ESRF"
author = "ESRF"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinxcontrib.redoc"]
templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"
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
