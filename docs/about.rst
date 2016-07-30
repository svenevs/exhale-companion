About
==============================================
NanoGUI builds on [GLFW](http://www.glfw.org/) for cross-platform OpenGL context
creation and event handling, [GLEW](http://glew.sourceforge.net/) to use OpenGL
3.x Windows, [Eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page) for
basic vector types, and [NanoVG](https://github.com/memononen/NanoVG) to draw
2D primitives.

Note that the depencency library NanoVG already includes some basic example
code to draw good-looking static widgets; what NanoGUI does is to flesh it
out into a complete GUI toolkit with event handling, layout generation, etc.

NanoGUI currently works on Mac OS X (Clang) Linux (GCC or Clang) and Windows
(Visual Studio >= 2015); it requires a recent C++11 capable compiler. All
dependencies are jointly built using a CMake-based build system.
