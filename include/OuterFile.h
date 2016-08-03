/** \file */
#include <arbitrary/BaseClass.h>

class SomeOuterClass : arbitrary::BaseClass {
public:
    /** \brief Pass-through constructor for the arbitrary base. */
    SomeOuterClass(unsigned int someData) : arbitrary::BaseClass(someData) {}

    /** \brief Sets the data. */
    void setData(unsigned int someData) { some_data = someData; }

    /** \brief Does the thing it should do. */
    virtual void virtualMethod() {}
};
