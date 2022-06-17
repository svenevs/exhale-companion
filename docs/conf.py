# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))

# -- Project information -----------------------------------------------------

project = "ExhaleCompanion"
copyright = "2017-2022, Stephen McDowell"
author = "Stephen McDowell"


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "4.5"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
# [[[ begin extensions marker ]]]
# Tell Sphinx to use both the `breathe` and `exhale` extensions
extensions = [
    "breathe",
    "exhale"
]

# Setup the `breathe` extension
breathe_projects = {"ExhaleCompanion": "./_doxygen/xml"}
breathe_default_project = "ExhaleCompanion"

# Setup the `exhale` extension
from textwrap import dedent
exhale_args = {
    ############################################################################
    # These arguments are required.                                            #
    ############################################################################
    "containmentFolder":     "./api",
    "rootFileName":          "library_root.rst",
    "rootFileTitle":         "Library API",
    "doxygenStripFromPath":  "../include",
    ############################################################################
    # Suggested optional arguments.                                            #
    ############################################################################
    "createTreeView":        True,
    "exhaleExecutesDoxygen": True,
    "exhaleDoxygenStdin": dedent('''
        INPUT       = ../include
        # For this code-base, the following helps Doxygen get past a macro
        # that it has trouble with.  It is only meaningful for this code,
        # not for yours.
        PREDEFINED += NAMESPACE_BEGIN(arbitrary)="namespace arbitrary {"
        PREDEFINED += NAMESPACE_END(arbitrary)="}"
    '''),
    ############################################################################
    # HTML Theme specific configurations.                                      #
    ############################################################################
    # Fix broken Sphinx RTD Theme 'Edit on GitHub' links
    # Search for 'Edit on GitHub' on the FAQ:
    #     http://exhale.readthedocs.io/en/latest/faq.html
    "pageLevelConfigMeta": ":github_url: https://github.com/svenevs/exhale-companion",
    ############################################################################
    # Main library page layout example configuration.                          #
    ############################################################################
    "afterTitleDescription": dedent(u'''
        Welcome to the developer reference to Exhale Companion.  The code being
        documented here is largely meaningless and was only created to test
        various corner cases e.g. nested namespaces and the like.

        .. note::

            The text you are currently reading was fed to ``exhale_args`` using
            the :py:data:`~exhale.configs.afterTitleDescription` key.  Full
            reStructuredText syntax can be used.

        .. tip::

           Sphinx / Exhale support unicode!  You're ``conf.py`` already has
           it's encoding declared as ``# -*- coding: utf-8 -*-`` **by
           default**.  If you want to pass Unicode strings into Exhale, simply
           prefix them with a ``u`` e.g. ``u"👽😱💥"`` (of course you would
           actually do this because you are writing with åçćëñtß or
           non-English 寫作 😉).
    '''),
    "afterHierarchyDescription": dedent('''
        Below the hierarchies comes the full API listing.

        1. The text you are currently reading is provided by
           :py:data:`~exhale.configs.afterHierarchyDescription`.
        2. The Title of the next section *just below this* normally defaults to
           ``Full API``, but the title was changed by providing an argument to
           :py:data:`~exhale.configs.fullApiSubSectionTitle`.
        3. You can control the number of bullet points for each linked item on
           the remainder of the page using
           :py:data:`~exhale.configs.fullToctreeMaxDepth`.
    '''),
    "fullApiSubSectionTitle": "Custom Full API SubSection Title",
    "afterBodySummary": dedent('''
        You read all the way to the bottom?!  This text is specified by giving
        an argument to :py:data:`~exhale.configs.afterBodySummary`.  As the docs
        state, this summary gets put in after a **lot** of information.  It's
        available for you to use if you want it, but from a design perspective
        it's rather unlikely any of your users will even see this text.
    '''),
    ############################################################################
    # Individual page layout example configuration.                            #
    ############################################################################
    # Example of adding contents directives on custom kinds with custom title
    "contentsTitle": "Page Contents",
    "kindsWithContentsDirectives": ["class", "file", "namespace", "struct"],
    # This is a testing site which is why I'm adding this
    "includeTemplateParamOrderList": True,
    ############################################################################
    # useful to see ;)
    "verboseBuild": True
}

# Tell sphinx what the primary language being documented is.
primary_domain = "cpp"

# Tell sphinx what the pygments highlight language should be.
highlight_language = "cpp"
# [[[ end extensions marker ]]]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Hiding this from the main docs for no real reason other than to hopefully
# avoid people thinking they need it
extensions.append("sphinx.ext.intersphinx")
intersphinx_mapping = {
    "exhale":  ("https://exhale.readthedocs.io/en/latest/", None),
    "nanogui": ("https://nanogui.readthedocs.io/en/latest/", None)
}

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
import exhale
# NOTE: this is the companion site for Exhale, which is why I'm setting the
#       version to be the same.  For your own projects, you would NOT do this!
version = exhale.__version__
# The full version, including alpha/beta/rc tags.
release = exhale.__version__

# -- Options for HTML output -------------------------------------------------

# [[[ begin theme marker ]]]
# The name of the Pygments (syntax highlighting) style to use.
# `sphinx` works very well with the RTD theme, but you can always change it
pygments_style = "sphinx"

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
# [[[ end theme marker ]]]

rst_epilog = ".. |theme| replace:: ``{0}``".format(html_theme)

# Called auto-magicallly by sphinx
def setup(app):
    # This is pretty meta.  To help demonstrate what is going on, I'm
    # generating an rst file to `.. include::` in `index.rst` to show
    # the relevant sections of `conf.py` on the page.
    #
    # That is, I love python and how convenient it is to read in files
    # even if the file being read is the one that is running xD
    begin_ext   = "# [[[ begin extensions marker ]]]"
    end_ext     = "# [[[ end extensions marker ]]]"
    begin_theme = "# [[[ begin theme marker ]]]"
    end_theme   = "# [[[ end theme marker ]]]"

    # open up `conf.py` and scan the lines for the markers
    ext_lines   = []
    theme_lines = []
    in_ext      = False
    in_theme    = False

    import codecs
    with codecs.open("conf.py", "r", "utf-8") as conf:
        for line in conf:
            # determine where we are / if we should be grabbing lines
            if line.startswith(begin_ext):
                in_ext = True
                continue
            elif line.startswith(end_ext):
                in_ext = False
                continue
            elif line.startswith(begin_theme):
                in_theme = True
                continue
            elif line.startswith(end_theme):
                # when we reach here, since ext came before theme,
                # we have everything we need
                break

            if in_ext:
                ext_lines.append(line)
            elif in_theme:
                theme_lines.append(line)

    # At this point `ext_lines` and `theme_lines` have the code we care about
    from exhale.utils import prefix
    for fname, lines in [("conf_extensions.rst", ext_lines), ("conf_theme.rst", theme_lines)]:
        with codecs.open(fname, "w", "utf-8") as file:
            file.write(".. code-block:: py\n\n")
            file.write(prefix("   ", "".join(l for l in lines)))
            file.write("\n")

    # write out the requirements used
    requirements = []
    with open("requirements.txt", "r") as req:
        for line in req:
            requirements.append(line)

    with open("the_requirements.rst", "w") as the_req:
        the_req.write(".. code-block:: nginx\n\n")
        the_req.write(prefix("   ", "".join(l for l in requirements)))
        the_req.write("\n")
