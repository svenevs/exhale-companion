#ifndef _ARBITRARY_BASE_CLASS_H
#define _ARBITRARY_BASE_CLASS_H

#include <arbitrary/common.h>

NAMESPACE_BEGIN(arbitrary)

/**
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
     * Which is then followed by a more descriptive definition.
     */
    virtual void virtualMethod() = 0;

    /**
     * \brief The value of this `BaseClass`'s ``protected`` data.
     *
     * \return
     * The value of ``protected BaseClass::some_data``.
     */
    virtual unsigned int getData() {
        return some_data;
    }

protected:
    /**
     * \brief The only constructor available, initializes ``some_data``.
     *
     * \param data
     * The number of ``some_data`` this `BaseClass` represents.
     */
    BaseClass(unsigned int data) : some_data(data) {}

    /// The value of something important.
    unsigned int some_data = 0;
};

NAMESPACE_END(arbitrary)

#endif // _ARBITRARY_BASE_CLASS_H
