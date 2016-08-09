/**
 * \file
 * \brief Provides various different types, typedefs, and functions used throughout.
 */
#ifndef _ARBITRARY_COMMON_H
#define _ARBITRARY_COMMON_H

/**
 * Mimic the ``nanogui`` style namespacing to make sure doxygen is configured correctly.
 */
#if !defined(NAMESPACE_BEGIN)
    /// Convenience pragma to begin namespace scoping in a legible manner without requiring indentation.
    #define NAMESPACE_BEGIN(name) namespace name {
#endif
#if !defined(NAMESPACE_END)
    /// Convenience pragma to end namespace scoping in a legible manner without requiring indentation.
    #define NAMESPACE_END(name) }
#endif

/// An enum that is not in a namespace.
enum UnscopedEnum {
    NO,
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
    /// Creates a `params` struct with `x`, `y`, and `z` initialized to ``0.0f``;
    params() : x(0.0f), y(0.0f), z(0.0f) {}

    /**
     * \brief The explicit `params` constructor.
     *
     * \param _x
     * The value to set this `params` `x` field to.
     *
     * \param _y
     * The value to set this `params` `y` field to.
     *
     * \param _z
     * The value to set this `params` `z` field to.
     */
    params(float _x, float _y, float _z) : x(_x), y(_y), z(_z) {}

    /**
     * \union U common.h arbitrary/common.h
     *
     * A union of sorts.
     */
    union U {
        /// One way of looking at things.
        int first_view;
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
static float common_float_variable = 12.21f;

/// An extra useful typedef to make your readers happy.
typedef bool super_bool;

/**
 * \union SupremeUnion common.h arbitrary/common.h
 *
 * \brief The most supreme unions of them all.
 */
union SupremeUnion {
    std::int32_t n;     // occupies 4 bytes
    std::uint16_t s[2]; // occupies 4 bytes
    std::uint8_t c;     // occupies 1 byte
};

namespace arbitrary {
    /**
     * \union NamespacedUnion common.h arbitrary/common.h
     *
     * \brief This is a union in a namespace.
     */
    union NamespacedUnion {
        std::int32_t n;     // occupies 4 bytes
        std::uint16_t s[2]; // occupies 4 bytes
        std::uint8_t c;     // occupies 1 byte
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
         * \brief This is a union in a a _nested_ namespace.
         */
        union NestedNamespacedUnion {
            std::int32_t n;     // occupies 4 bytes
            std::uint16_t s[2]; // occupies 4 bytes
            std::uint8_t c;     // occupies 1 byte
        };
    }

    /// a secondary namespace
    namespace second_nested {
        /// Sort test for namespace hierarchies.
        static constexpr double SN = 99.99;

        /// After ref discovery processing verification.
        typedef void death_star;

        /**
         * \class NestingSecondLastChild common.h arbitrary/common.h
         *
         * \brief Verifying li tags and closure.
         */
        class NestingSecondLastChild {
            /// Does nothing.
            NestingSecondLastChild() {}

            /// Does even more nothing.
            ~NestingSecondLastChild() {}
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
                    };
                }
            }
        }
    }
}

/**
 * \brief A common function that would be used with ..doxygenfunction::.
 *
 * Does absolutely nothing.
 *
 * \param params
 * Does whatever you want it to.
 */
static void someCommonFunction(super_bool anything) {
    if(anything)
        return;
}



#endif // _ARBITRARY_COMMON_H
