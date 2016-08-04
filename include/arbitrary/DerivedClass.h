/**
 * \file
 * \brief An example of the derivation strategies you could conceivably use.
 */
#ifndef _ARBITRARY_DERIVED_CLASS_H
#define _ARBITRARY_DERIVED_CLASS_H

#include <typeinfo>
#include <iostream>
#include <string>
#include <exception>

#include <arbitrary/BaseClass.h>

NAMESPACE_BEGIN(arbitrary)

///A bitmasking enum for determining what the current camera actions are.
enum CAMERA_STATES {
    /// Camera state is not changing.
    CAM_NONE      = (1 << 0),
    /// Camera is actively rotating.
    CAM_ROTATE    = (1 << 1),
    /// Camera is actively translating.
    CAM_TRANSLATE = (1 << 2),
    /// Camera is actively scaling.
    CAM_SCALE     = (1 << 3)
};

/**
 * \class DerivedClass DerivedClass.h arbitrary/DerivedClass.h
 *
 * \brief A derivation class of `BaseClass` serving as an extremely rudimentary array wrapper.
 */
template <typename T, unsigned int N>
class DerivedClass : public BaseClass {
public:
    /// Initializes the `BaseClass` field ``some_data`` to be the template parameter `N`.
    DerivedClass() : BaseClass(N) {}

    /// The default destructor; does nothing.
    virtual ~DerivedClass() {}

    /**
     * \brief Advances the printing index of this `DerivedClass`.
     *
     * Prints a message to the console indicating what ``current_index`` is, and then increases
     * ``current_index`` by one, wrapping around to ``0`` if ``current_index >= N``.
     */
    void virtualMethod() {
        std::cout << "    virtualMethod() current index is [" << current_index << "]." << std::endl;
        current_index++;
        if(current_index >= N) current_index = 0;
    }

    /**
     * \brief Inserts `item` and `index` if it is a valid item to add, and a valid index.
     *
     * A valid index is in the range ``[0, N)`` where ``N`` is the second template parameter
     * of the class.  A valid index is also, for some arbitrary reason, one that has not
     * already been set by a previous call.  A valid ``item`` is anything that is not
     * still ``nullptr`` from the constructor initialization.
     *
     * \param item
     * A pointer to the item that you want to store.
     *
     * \param index
     * The index you would like to store `item` at.
     *
     * \return
     * Whether or not this `DerivedClass`'s internal storage was modified or not.
     */
    bool insertAt(T &item, unsigned int index) {
        if(index >= N) return false;

        items[index] = item;
        return true;
    }

    /**
     * \brief Retrieve a pointer to the item at the specified `index`.
     *
     * \param index
     * The index of the item you want to retrieve a pointer to.
     *
     * \return
     * A pointer to the item at `index`.  Returns ``nullptr`` if either the item has not
     * been set yet by `insertAt`, or if `index` is not in the range ``[0, N)`` where
     * ``N`` is the second template parameter of this class.
     */
    const T& itemAt(unsigned int index) {
        if(index >= N) throw std::runtime_error("Invalid index.");
        else return items[index];
    }

protected:
    T items[N];
    unsigned int current_index = 0;
};

NAMESPACE_END(arbitrary)

#endif // _ARBITRARY_DERIVED_CLASS_H
