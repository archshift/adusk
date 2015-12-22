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