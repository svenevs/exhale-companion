#pragma once

/**
 * \file
 * \brief Defines the `BaseClass` that is to be derived from in all instances.
 */

#include <arbitrary/common.h>

NAMESPACE_BEGIN(arbitrary)

/// Documenting a define directive.
#define AN_ARBITRARY_DEFINE 11

/// Testing a nested namespace.
namespace nested {
    /**
     * \struct int2 BaseClass.h arbitrary/BaseClass.h
     *
     * \brief Just a simple coupling of two integers as x and y.
     */
    struct int2 {
        /// Default constructor: (0, 0).
        int2() : x(0), y(0) {}

        /// Explicit constructor: (_x, _y).
        int2(int _x, int _y) : x(_x), y(_y) {}

        /// The first coordinate.
        int x;
        /// The second coordinate.
        int y;
    };

    namespace dual_nested {
        /**
         * \struct int3 BaseClass.h arbitrary/BaseClass.h
         *
         * \brief The int3 struct is just a simple coupling of three integers as x, y, and z.
         */
        struct int3 {
            /// Default constructor: (0, 0, 0).
            int3() : x(0), y(0), z(0) {}

            /// Explicit constructor: (_x, _y, _z).
            int3(int _x, int _y, int _z) : x(_x), y(_y), z(_z) {}

            /// The first coordinate.
            int x;
            /// The second coordinate.
            int y;
            /// The third coordinate.
            int z;
        };
    }
}

/**
 * \class BaseClass BaseClass.h arbitrary/BaseClass.h
 *
 * A fully documented class for inheriting from.
 */
class BaseClass {
public:
    /// The default constructor for this class does not exist, as ``some_data`` must be initialized.
    BaseClass() = delete;

    /// The default destructor; does nothing.
    virtual ~BaseClass() {}

    /**
     * \brief A pure virtual method with a brief definition.
     *
     * Which is then followed by a more descriptive "detailed" definition.
     */
    virtual void virtualMethod() = 0;

    /**
     * \brief The value of this `BaseClass`'s ``protected`` data.
     *
     * \return
     *     The value of \ref BaseClass::some_data
     */
    virtual unsigned int getData() {
        return some_data;
    }

protected:
    /**
     * \brief The only constructor available, initializes ``some_data``.
     *
     * \param data
     *     The number of ``some_data`` this BaseClass represents.
     */
    BaseClass(unsigned int data) : some_data(data) {}

    /// The value of something important.
    unsigned int some_data = 0;
};

NAMESPACE_END(arbitrary)
