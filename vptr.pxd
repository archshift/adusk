cdef class VirtualPointer:
    cdef int state
    cdef int x
    cdef int y

    cdef size_t get_radius(self)
#    cdef bint in_box(self, int x, int y, size_t w, size_t h)