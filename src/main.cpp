#include <iostream>
#include <arbitrary/DerivedClass.h>

struct two_floats {
    two_floats() : x(0.0f), y(0.0f) {}
    two_floats(float _x, float _y) : x(_x), y(_y) {}
    float x;
    float y;
    friend std::ostream& operator<<(std::ostream &strm, const two_floats &tf) {
        return strm << "(" << tf.x << ", " << tf.y << ")";
    }
};

int main(int argc, char **argv) {
    std::cout << "Creating an arbitrary example using DerivedClass<float, 4>:" << std::endl;
    arbitrary::DerivedClass<float, 4> derived_obj;
    std::cout << "  Insertions:" << std::endl;
    for(unsigned int i = 0; i < 4; ++i) {
        derived_obj.virtualMethod();
        float f = (float) i;
        if(derived_obj.insertAt(f, i))
            std::cout << "    Inserted at: " << i << ", retrieved: " << derived_obj.itemAt(i) << std::endl;
    }
    std::cout << "  Retrievals only:" << std::endl;
    for(unsigned int i = 0; i < 4; ++i) {
        derived_obj.virtualMethod();
        std::cout << "    Retrieved: " << derived_obj.itemAt(i) << std::endl;
    }


    std::cout << "Creating an arbitrary example using DerivedClass<struct two_floats, 4>:" << std::endl;
    arbitrary::DerivedClass<two_floats, 4> second_derived_obj;
    std::cout << "  Insertions:" << std::endl;
    for(unsigned int i = 0; i < 4; ++i) {
        second_derived_obj.virtualMethod();
        two_floats tf((float) i, (float) i);
        if(second_derived_obj.insertAt(tf, i))
            std::cout << "    Inserted at: " << i << ", retrieved: " << second_derived_obj.itemAt(i) << std::endl;
    }
    std::cout << "  Retrievals only:" << std::endl;
    for(unsigned int i = 0; i < 4; ++i) {
        second_derived_obj.virtualMethod();
        std::cout << "    Retrieved: " << second_derived_obj.itemAt(i) << std::endl;
    }
}