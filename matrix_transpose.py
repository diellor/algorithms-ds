class Matrix:
    """Interface of a matrix.

    This class provides only the matrix size N and a method for swapping
    two items. The actual storage of the matrix in memory is provided by
    subclasses in testing code.
    """

    def __init__(self, N):
        self.N = N

    def swap(self, i1, j1, i2, j2):
        """Swap elements (i1,j1) and (i2,j2)."""
        # Overridden in subclasses
        raise NotImplementedError

    def naiveSwap(self,i1, i2, j1, j2):
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                self.swap(i, j, j, i)

    def recursiveSwap(self, i1, i2, j1, j2):
        if j1 == j2 or i1 == i2:
            self.naiveSwap(i1,i2,j1,j2)
        else:
            self.recursiveSwap( i1, (i1 + i2) // 2, j1, (j1 + j2) // 2)
            self.recursiveSwap( (i1 + i2) // 2 + 1, i2, j1, (j1 + j2) // 2)
            self.recursiveSwap( (i1 + i2) // 2 + 1, i2, (j1 + j2) // 2 + 1, j2)
            if (i1 >= (j1 + j2) // 2 + 1):
                self.recursiveSwap( i1, (i1 + i2) // 2, (j1 + j2) // 2 + 1, j2)

    def transpose(self):
        self.recursiveSwap(0, self.N - 1, 0, self.N - 1)
