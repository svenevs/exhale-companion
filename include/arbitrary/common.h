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

#endif // _ARBITRARY_COMMON_H
