Library API
==============================================================


.. warning::

   Please be advised that the reference documentation discussing NanoGUI
   is currently being developed.  Presented below is *only* the **C++**
   API.  If you are using the **Python** API, the contents below are still
   applicable for understanding what methods are available.  **Python** users
   are advised to refer to the more concise ``example2`` program for
   understanding how to wield the **C++** API using **Python** --- all of the
   relevant **C++** API is bound to **Python** using ``pybind11``.


.. toctree::
   :maxdepth: 5

   generated_api_arbitrary.rst

.. toctree::
   :maxdepth: 5

   generated_api_external.rst

.. toctree::
   :maxdepth: 5

   generated_api_unscoped_global_namespace.rst

This is a test of the functions
--------------------------------------------------------

.. doxygenfunction:: arbitraryFunction

I wonder how that looks.  Now lets see if it works with the proper namespace:

.. doxygenfunction:: arbitrary::arbitraryFunction

Please be good.

