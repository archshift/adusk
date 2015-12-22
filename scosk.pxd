cdef class KeyButton:
    cdef float width_weight


cdef class VirtualKeyboard:
#    cdef size_t padding
#    cdef list key_width
#    cdef float key_height
#    cdef size_t key_rows

#    cdef float _uniform_key_width(self, size_t row)
    cdef float _uniform_key_height(self)
    cdef void update_dimensions(self)
#    cdef size_t find_key_row(self, int y_coord)
    cdef object find_key(self, int x_coord, int y_coord)


cdef class VirtualPointer:
    cdef int state
    cdef int x
    cdef int y

    cdef size_t get_radius(self)
#    cdef bint in_box(self, int x, int y, size_t w, size_t h)

cdef sc_adjust_x(int raw_x, float center_fraction, float scalar=*)
cdef sc_adjust_y(int raw_y, float center_fraction, float scalar=*)