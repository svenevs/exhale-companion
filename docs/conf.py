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
    "treeViewIsBootstrap": True,
    # NOTE: there exist many other options for you to tweak.  See
    # http://exhale.readthedocs.io/en/latest/reference_exhale_configs.html#bootstrap-mods
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
    # See `html_sidebars` below, since the I am adding a `bootstrap sidebar`
    # for all pages, the contents directive becomes irrelevant.
    "kindsWithContentsDirectives": [],
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
# You should probably choose this according to the theme you are using for bootstrap...
pygments_style = "perldoc"  # or try 'monokai' :)  `pygmentize -L` shows all available

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "bootstrap"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Used in theme and sidebar options
import os
containmentFolder = os.path.basename(exhale_args["containmentFolder"])

# Theme options are theme-specific and customize the look and feel of a
# theme further.
#
# See here for all options:
#     https://ryan-roemer.github.io/sphinx-bootstrap-theme/README.html#customization
html_theme_options = {
    # Render the next and previous page links in navbar. (Default: true)
    "navbar_sidebarrel": False,

    # Render the current pages TOC in the navbar. (Default: true)
    # See `html_sidebars` below for why this is False
    "navbar_pagenav": False,

    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    "globaltoc_depth": -1,

    # A list of tuples containing pages or urls to link to.
    # Valid tuples should be in the following forms:
    #    (name, page)                 # a link to a page
    #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
    #    (name, "http://example.com", True) # arbitrary absolute url
    # Note the "1" or "True" value above as the third argument to indicate
    # an arbitrary url.
    "navbar_links": [
        (
            # Library API -> api/library_root
            exhale_args["rootFileTitle"],
            os.path.join(
                containmentFolder,
                exhale_args["rootFileName"].split(".rst")[0]
            )
        ),
        ("GitHub", "https://github.com/svenevs/exhale-companion", True),
    ],

    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    #
    # NOTE: depends on your theme if you are using bootswatch!
    "navbar_class": "navbar navbar-inverse",

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    "source_link_position": "nav",

    # Bootswatch (http://bootswatch.com/) theme.
    "bootswatch_theme": "simplex",
}

# Include a sidebar for navigational convenience on the pages generated by
# Exhale.  Use "**" as the key if you want it on every page.
gen_sidebar_pages = os.path.join(containmentFolder, "**")
html_sidebars = {
  gen_sidebar_pages:   ["localtoc.html"],
  "how_created":       ["localtoc.html"],
  "using_intersphinx": ["localtoc.html"]
}

# auto-magically called for you by `sphinx`
def setup(app):
    import os
    from textwrap import dedent
    # NOTE: by having `sphinx` installed, you already have `pygments`!
    from pygments.styles import get_style_by_name

    ####################################################################################
    # IMPORTANT!                                                                       #
    # You don't have to re-generate the css and javascript every time!  Simply add the #
    # files to your repo.                                                              #
    #                                                                                  #
    # This is being done here because the bootstrap branch is the only one that needs  #
    # these overrides!                                                                 #
    #                                                                                  #
    # You are more than welcome to just copy-paste this code in your docs without      #
    # citation, but it's probably better to just generate them once and (assuming they #
    # are working), `git add` the _static files.                                       #
    ####################################################################################
    # For bootstrap, there are two things you will probably want to force
    # override:
    #
    # 1. The background color of your code listings.
    # 2. Indent things like class members.
    #
    # Make the _static directory we gave in `html_static_path` above
    try:
        static_dir = "_static"
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        ################################################################################
        # 1. Override the CSS                                                          #
        ################################################################################
        css_name = "override.css"
        with open(os.path.join(static_dir, css_name), "w") as css:
            # NOTE: because I'm using string.format, the starting and closing curly
            # braces need to be escaped.  That's why it is
            #
            #    div[class|="highlight"] pre {{
            #
            # instead of
            #
            #    div[class|="highlight"] pre {
            css.write(dedent('''
                /* Force override of bootstrap.  The Sphinx generated code listings
                 * appear in something like
                 *
                 *   <div class="highlight-cpp">
                 *     <div class="highlight">
                 *       <pre>// the code</pre>
                 *     </div>
                 *   </div>
                 *
                 * So we're going to select the classes that start with highlight.
                 */
                div[class|="highlight"] pre {{
                    background-color: {color} ! important;
                }}
            '''.format(
                color=get_style_by_name(pygments_style).background_color
            )))
        ################################################################################
        # 2. Force indentation.  See                                                   #
        #    https://github.com/ryan-roemer/sphinx-bootstrap-theme/issues/89           #
        ################################################################################
        js_name = "indent.js"
        with open(os.path.join(static_dir, js_name), "w") as js:
            js.write(dedent('''
                $(function(){
                    /* If a user-produced definition list, apply dl-horizontal. */
                    if($("dl").attr("class") == "") {
                        $("dl").addClass("dl-horizontal");
                    }
                    /* Otherwise, this is a `sphinx` definition list for class /
                     * function / etc documentation.  Apply some padding instead. */
                    else {
                        $("dl").children("dd").css({"padding-left": "4%"});
                    }
                });
            '''))
        ################################################################################
        # Last but not least, tell Sphinx to use these files!                          #
        ################################################################################
        # NOTE: Sphinx looks for these in the _static folder
        app.add_css_file(css_name)
        app.add_js_file(js_name)
    except Exception as e:
        raise RuntimeError("Could not generate static files:\n{0}".format(e))
# [[[ end theme marker ]]]

rst_epilog = ".. |theme| replace:: ``{0}``".format(html_theme)

# hack: I need the below setup(app), but the bootstrap docs shouldn't include
# this stuff.  save the above setup(app) before redefining it

bstrap_setup = setup

# Called auto-magicallly by sphinx
def setup(app):
    # hack part two: call the previous setup xD
    bstrap_setup(app)

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
