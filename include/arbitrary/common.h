#pragma once

/**
 * \file
 *
 * \brief Provides various different types, typedefs, and functions used throughout.
 *
 * \rst
 *
 * The brief file description is done using the ``\brief`` command from Doxygen.  The
 * current text you are using has "advanced" reStructuredText syntax such as grid tables
 * and directives.
 *
 * .. tip::
 *
 *    To document a file with directives or other "advanced" syntax, you will need to
 *    use the ``rst`` verbatim environment.  See the description for
 *    :py:data:`exhale.configs.DEFAULT_DOXYGEN_STDIN_BASE` for the definition and usage
 *    of this environment.
 *
 * I can have some C++ code shown:
 *
 * .. code-block:: cpp
 *
 *    throw std::runtime_error("Would you rather I segfault?")
 *
 * Or some Python code:
 *
 * .. code-block:: py
 *
 *    raise RuntimeError("Would you rather I dereference None?")
 *
 * All using the ``.. code-block::`` environment:
 *
 * .. code-block:: rst
 *
 *    I can have some C++ code shown:
 *
 *    .. code-block:: cpp
 *
 *       throw std::runtime_error("Would you rather I segfault?")
 *
 *    Or some Python code:
 *
 *    .. code-block:: py
 *
 *       raise RuntimeError("Would you rather I dereference None?")
 *
 * And since grid tables are just so damn wonderful, we'll do one just for kicks
 *
 * +-------------------------------------+------------------------------------------------+
 * | Did you Know?                       | How is that possible?                          |
 * +=====================================+================================================+
 * | You can link to other Sphinx docs!  | Set it up in your ``conf.py``:                 |
 * |                                     |                                                |
 * |                                     | - `intersphinx`_: ``'sphinx.ext.intersphinx'`` |
 * |                                     | - Specify: ``intersphinx_mapping``.            |
 * +-------------------------------------+------------------------------------------------+
 * | Checkout the :ref:`using_intersphinx` guide for more information.                    |
 * +--------------------------------------------------------------------------------------+
 *
 * .. _intersphinx: http://www.sphinx-doc.org/en/stable/ext/intersphinx.html
 *
 * \endrst
 */

#if !defined(NAMESPACE_BEGIN) || defined(DOXYGEN_DOCUMENTATION_BUILD)
    /**
     * \rst
     * See :c:macro:`NanoGUI macro NAMESPACE_BEGIN <nanogui:NAMESPACE_BEGIN>`.
     * \endrst
     */
    #define NAMESPACE_BEGIN(name) namespace name {
#endif
#if !defined(NAMESPACE_END) || defined(DOXYGEN_DOCUMENTATION_BUILD)
    /**
     * \rst
     * See :c:macro:`NanoGUI macro NAMESPACE_END <nanogui:NAMESPACE_END>`.
     * \endrst
     */
    #define NAMESPACE_END(name) }
#endif

/// An enum that is not in a namespace.
enum UnscopedEnum {
    /// NO
    NO,
    /// YES
    YES
};

/// A namespace outside of arbitrary.
namespace external {
    /// Maximum number of traversals.
    static constexpr unsigned int MAX_DEPTH = 12;
}

/**
 * \struct params common.h arbitrary/common.h
 *
 * \brief A serializable parameters struct that nobody would ever actually use like this.
 */
struct params {
    /// Creates a params struct with ``x``, ``y``, and ``z`` initialized to ``0.0f``;
    params() : x(0.0f), y(0.0f), z(0.0f) {}

    /**
     * \brief The explicit params constructor.
     *
     * \param _x
     * The value to set this params ``x`` field to.
     *
     * \param _y
     * The value to set this params ``y`` field to.
     *
     * \param _z
     * The value to set this params ``z`` field to.
     */
    params(float _x, float _y, float _z) : x(_x), y(_y), z(_z) {}

    /**
     * \union U common.h arbitrary/common.h
     *
     * A nested union of sorts.
     */
    union U {
        /// One way of looking at things.
        int32_t first_view;
        /// Another way of looking at them.
        float second_view;
    };

    /// The x Cartesian coordinate.
    float x;
    /// The y Cartesian coordinate.
    float y;
    /// The z Cartesian coordinate.
    float z;
};

/// This is a variable common to all other files.
static constexpr float common_float_variable = 12.21f;

/// An extra useful typedef to make your readers happy.
typedef bool super_bool;

/**
 * \union SupremeUnion common.h arbitrary/common.h
 *
 * \brief The most supreme unions of them all.
 */
union SupremeUnion {
    int32_t n;     ///< occupies 4 bytes
    uint16_t s[2]; ///< occupies 4 bytes
    uint8_t c;     ///< occupies 1 byte
};

namespace arbitrary {
    /**
     * \union NamespacedUnion common.h arbitrary/common.h
     *
     * \brief This is a union in a namespace.
     */
    union NamespacedUnion {
        int32_t n;     ///< occupies 4 bytes
        uint16_t s[2]; ///< occupies 4 bytes
        uint8_t c;     ///< occupies 1 byte
    };

    /// Testing sort with combined struct and class list.
    struct zed_struct {
        /// constructs a zed
        zed_struct(int _z) : z(_z) {}

        /// the zed
        int z;
    };

    namespace nested {
        /**
         * \union NestedNamespacedUnion common.h arbitrary/common.h
         * \brief This is a union in a a **nested** namespace.
         */
        union NestedNamespacedUnion {
            int32_t n;     ///< occupies 4 bytes
            uint16_t s[2]; ///< occupies 4 bytes
            uint8_t c;     ///< occupies 1 byte
        };
    }

    /// a secondary namespace
    namespace second_nested {
        /// Sort test for namespace hierarchies.
        static constexpr double SN = 99.99;

        /// After ref discovery processing verification.
        typedef void death_star;

        /**
         * \class NestingFirstLastChild common.h arbitrary/common.h
         *
         * \brief Verifying li tags and closure.
         */
        class NestingFirstLastChild {
            /// Does nothing.
            NestingFirstLastChild() {}

            /// Does even more nothing.
            ~NestingFirstLastChild() {}
        };

        /**
         * \class NestingLastChild common.h arbitrary/common.h
         *
         * \brief Verifying li tags and closure.
         */
        class NestingLastChild {
            /// Does nothing.
            NestingLastChild() {}

            /// Does even more nothing.
            ~NestingLastChild() {}
        };
    }

    /// At a first glance, it doesn't seem arbitrary.
    bool arbitraryFunction() {
        return false;
    }

    /**
     * \struct arbitrary_struct common.h arbitrary/common.h
     *
     * Yet another namespaced and overly arbitrary struct.
     */
    struct arbitrary_struct {
        /// Mehem
        int meh = 11;
        /// Mehehem
        arbitrary_struct(int m) : meh(m) {}
    };
}

namespace first {
    namespace second {
        namespace third {
            /**
             * \struct only_namespace_testing common.h arbitrary/common.h
             *
             * \brief This struct needs to appear in the class hierarchy.
             */
            struct only_namespace_testing {
                /// The only constructor.
                only_namespace_testing(double _d) : d(_d) {}

                /// This is a member double.
                double d;
            };

            namespace fourth {
                namespace fifth {
                    /**
                     * \struct deeper_namespace_testing common.h arbitrary/common.h
                     *
                     * \brief This struct needs to appear in the class hierarchy.
                     */
                    struct deeper_namespace_testing {
                        /// The only constructor.
                        deeper_namespace_testing(double _d) : d(_d) {}

                        /// This is a member double.
                        double d;

                        /**
                         * \struct nested_struct common.h arbitrary/common.h
                         *
                         * \brief This struct will also be in the class hierarchy.
                         *
                         * Furthermore, this class should also **only** show up on
                         * the ``fifth`` namespace page, and none of its parents.
                         */
                        struct nested_struct {
                            /// A nested struct constructor...
                            nested_struct(float _f) : f(_f) {}

                            /// This is a member float.
                            float f;
                        };
                    };
                }
            }
        }
    }
}

/**
 * \brief A common function that would be used with ``..doxygenfunction::``.
 *
 * Does absolutely nothing, but this is a **bold** statement.
 *
 * \param anything
 *     Does whatever you want it to.
 */
static void someCommonFunction(super_bool anything) {
    if(anything)
        return;
}
