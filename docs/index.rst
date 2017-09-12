Exhale Companion
========================================================================================

.. contents:: Contents
   :local:
   :backlinks: none

Welcome to the companion website for `Exhale`_.  The purpose of this website is to give
a simple example of what your Library API could look like if you follow the
`start to finish directions <start_to_finish_>`_ to get things hosted on RTD.

.. _Exhale:          http://exhale.readthedocs.io/en/latest/
.. _start_to_finish: http://exhale.readthedocs.io/en/latest/usage.html#start-to-finish-for-read-the-docs

.. tip::

   The webpage you are viewing are using the |theme|.

This example repository has different versions built for you to get an idea of how
things might look.

.. include:: ../README.rst
   :start-after: begin_in_action
   :end-before:  end_in_action

Make sure to view the :ref:`extension_setup` and :ref:`html_theme_setup` for the
different versions, as they vary slightly (e.g., ``bootstrap`` gets more supplied in the
``exhale_args`` portion of ``conf.py``).

.. toctree::
   :maxdepth: 2

   api/library_root
   using_intersphinx

How this Version of ExhaleCompanion was Created
----------------------------------------------------------------------------------------

For convenience, I'm going to inline the code used in this configuration from
``conf.py`` here.  The two main things you need to do here are

1. Setup the ``breathe`` and ``exhale`` extensions.
2. Choose your ``html_theme``, which affects what you choose for the ``exhale`` side.

.. _extension_setup:

Extension Setup
****************************************************************************************

.. include:: conf_extensions.rst

.. _html_theme_setup:

HTML Theme Setup
****************************************************************************************

.. include:: conf_theme.rst
