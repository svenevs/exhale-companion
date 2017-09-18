#pragma once

/**
 * \file
 *
 * \brief Document a file that does not have any parents.
 *
 * This file exists to make sure that classes not owned by a specific parent directory
 * still appear in the File Hierarchy.  This file level documentation uses simple
 * constructs and text, and therefore does **not** need to utilize the \c \\rst
 * environment.
 *
 * 1. There is no need to use a raw \c \\rst environment.
 *    - Listings and the like can be parsed by Exhale.
 *    - Basic formatting from Doxygen such as \c \\c or \a \\a can be used.
 * 2. This is about the maximum amount of "normal" formatting Exhale can handle.
 *
 * To see a file that requires documentation be in an \c \\rst environment, see
 * \ref arbitrary/common.h and it's associated code online.  Note that the link just
 * generated was by using \c \\ref \c arbitrary/common.h .
 */

#include <arbitrary/BaseClass.h>

/**
 * \class SomeOuterClass OuterFile.h OuterFile.h
 *
 * \brief A demonstration of inheritance relationships across namespaces for the docs.
 */
class SomeOuterClass : arbitrary::BaseClass {
public:
    /// Pass-through constructor for the arbitrary base.
    SomeOuterClass(unsigned int someData) : arbitrary::BaseClass(someData) {}

    /// Sets the data.
    void setData(unsigned int someData) { some_data = someData; }

    /// Does the thing it should do.
    virtual void virtualMethod() {}
};
