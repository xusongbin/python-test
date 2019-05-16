
import numpy as np

from numpy.lib import stride_tricks


class StudyNumpy(object):
    # Print the numpy version and the configuration (★☆☆)
    def class2(self):
        print(np.__version__)
        print(np.show_config())

    # How to get the documentation of the numpy add function from the command line? (★☆☆)
    def class3(self):
        a = np.zeros(10)
        print(a)
        print(a[4])
        print(a.size)

    # Create a vector with values ranging from 10 to 49 (★☆☆)
    def class6(self):
        a = np.arange(10, 20)
        print(a)

    # Reverse a vector (first element becomes last) (★☆☆)
    def class7(self):
        a = np.arange(50)
        print(a)
        a = a[::-1]
        print(a)

    # Create a 3x3 matrix with values ranging from 0 to 8 (★☆☆)
    def class8(self):
        a = np.arange(9).reshape(3, 3)
        print(a)

    # Find indices of non-zero elements from [1,2,0,0,4,0] (★☆☆)
    def class9(self):
        a = np.nonzero([1, 2, 0, 0, 4, 0])
        print(a)

    # Create a 3x3 identity matrix (★☆☆)
    def class10(self):
        a = np.eye(3)
        print(a)

    # Create a 3x3x3 array with random values (★☆☆)
    def class11(self):
        a = np.random.random((3, 3, 3))
        print(a)

    # Create a 10x10 array with random values and find the minimum and maximum values (★☆☆)
    def class12(self):
        a = np.random.random((4, 4))
        print(a)
        print(a.min(), a.max())

    # Create a random vector of size 30 and find the mean value (★☆☆)
    def class13(self):
        a = np.random.random(5)
        print(a)
        print(a.mean())

    # Create a 2d array with 1 on the border and 0 inside (★☆☆)
    def class14(self):
        a = np.ones((4, 4))
        print(a)
        a[1:-1, 1:-1] = 0
        print(a)

    # What is the result of the following expression? (★☆☆)
    def class15(self):
        a = 0 * np.nan
        print(a)
        a = np.nan == np.nan
        print(a)
        a = np.inf > np.nan
        print(a)
        a = np.nan - np.nan
        print(a)
        a = 0.3 == 3 * 0.1
        print(a)

    # Create a 5x5 matrix with values 1,2,3,4 just below the diagonal (★☆☆)
    def class16(self):
        a = np.diag(1+np.arange(4), k=-1)
        print(a)
        a = np.arange(1, 4)
        a = np.diag(a)
        print(a)

    # Create a 8x8 matrix and fill it with a checkerboard pattern (★☆☆)
    def class17(self):
        a = np.zeros((8, 8), dtype=int)
        # a[1::2, ::2] = 1
        # a[::2, 1::2] = 1
        a[0::2, 0::2] = 1
        a[1::2, 1::2] = 1
        print(a)

    # Consider a (6,7,8) shape array, what is the index (x,y,z) of the 100th element?
    def class18(self):
        a = np.unravel_index(5, (1, 2, 3))
        print(a)

    # Create a checkerboard 8x8 matrix using the tile function (★☆☆)
    def class19(self):
        a = np.tile(np.array([[0, 1], [1, 0]]), (4, 4))
        print(a)

    # Normalize a 5x5 random matrix (★☆☆)
    def class20(self):
        a = np.random.random((5, 5))
        print(a)
        b = a - a.min()
        print(b)
        a = (a - a.min()) / (a.max() - a.min())
        print(a)

    # Create a custom dtype that describes a color as four unisgned bytes (RGBA) (★☆☆)
    def class21(self):
        color = np.dtype([('r', np.ubyte, 1),
                          ('g', np.ubyte, 1),
                          ('b', np.ubyte, 1),
                          ('a', np.ubyte, 1)])
        print(color)

    # Multiply a 5x3 matrix by a 3x2 matrix (real matrix product) (★☆☆)
    def class22(self):
        b = np.ones((5, 3))
        print(b)
        c = np.ones((3, 2))
        print(c)
        a = np.dot(b, c)
        print(a)

    # Given a 1D array, negate all elements which are between 3 and 8, in place. (★☆☆)
    def class23(self):
        a = np.arange(11)
        print(a)
        a[(3 < a) & (a <= 8)] *= -1
        print(a)

    # What is the output of the following script? (★☆☆)
    # print(sum(range(5), -1))
    # from numpy import *
    # print(sum(range(5), -1))
    def class24(self):
        b = range(5)
        print(b)
        a = sum(b, -1)
        print(a)

    # What are the result of the following expressions?
    def class26(self):
        a = np.array(0) // np.arange(0)
        print(a)
        a = np.array(0) // np.arange(0.)
        print(a)
        a = np.array(0) / np.arange(0)
        print(a)
        a = np.array(0) / np.arange(0.)
        print(a)
        a = 5
        a = a / 3
        print(a, type(a))
        a = 5
        a = a / 3.0
        print(a, type(a))
        a = 5
        a = a // 3
        print(a, type(a))
        a = 5
        a = a // 3.0
        print(a, type(a))

    # How to round away from zero a float array ? (★☆☆)
    def class27(self):
        a = np.random.uniform(-10, +10, 10)
        print(a)
        b = np.copysign(0.5, a)
        print(b)
        c = a + b
        print(c)
        c = np.trunc(c)
        print(c)

    # Extract the integer part of a random array using 5 different methods (★★☆)
    def class28(self):
        a = np.random.uniform(0, 10, 10)
        print('a', a)
        b = a - a % 1
        print('nof', b)
        b = np.floor(a)
        print('floor', b)
        b = np.ceil(a)
        print('ceil', b)
        b = a.astype(int)
        print('astype', b)
        b = np.trunc(a)
        print('trunc', b)

    # Create a 5x5 matrix with row values ranging from 0 to 4 (★★☆)
    def class29(self):
        a = np.zeros((5, 5))
        print(a)
        a += np.arange(1, 6)
        print(a)

    # Create a vector of size 10 with values ranging from 0 to 1, both excluded (★★☆)
    def class31(self):
        a = np.linspace(0, 1, 12, endpoint=True)
        print(a)
        a = a[1:-1]
        print(a)

    # Create a random vector of size 10 and sort it (★★☆)
    def class32(self):
        a = np.random.random(10)
        print(a)
        a.sort()
        print(a)

    # How to sum a small array faster than np.sum? (★★☆)
    def class33(self):
        a = np.arange(10)
        print(a)
        b = np.add.reduce(a)
        print(b)
        a = np.random.random(10)
        print(a)
        b = np.add.reduce(a)
        print(b)

    # Consider two random array A anb B, check if they are equal (★★☆)
    def class34(self):
        a = np.random.randint(0, 2, 3)
        print(a)
        b = np.random.randint(0, 2, 3)
        print(b)
        c = np.allclose(a, b)
        print(c)

    # Make an array immutable (read-only) (★★☆)
    def class35(self):
        a = np.zeros(10)
        print(a)
        # a.flags.writeable = True
        # a.flags.readable = False
        a[0] = 1
        print(a)
        print(a[0])

    # Consider a random 10x2 matrix representing cartesian coordinates, convert them to polar coordinates (★★☆)
    def class36(self):
        a = np.random.random((10, 2))
        print(a)
        x, y = a[:, 0], a[:, 1]
        print(x)
        print(y)
        b = np.sqrt(x**2 + y**2)
        c = np.arctan2(y, x)
        print(b)
        print(c)

    # Create random vector of size 10 and replace the maximum value by 0 (★★☆)
    def class37(self):
        a = np.random.random(10)
        print(a)
        a[a.argmax()] = 0
        print(a)
        a = np.random.random(10)
        print(a)
        a[np.where(a == a.max())] = 0
        print(a)

    # Create a structured array with x and y coordinates covering the [0,1]x[0,1] area (★★☆)
    def class38(self):
        a = np.zeros((10, 10))
        print(a)
        print('====================================')
        a = np.linspace(0, 1, 10)
        print(a)
        print('====================================')
        a = np.zeros((10, 10), [('x', float), ('y', float)])
        print(a)
        print('====================================')
        a['x'], a['y'] = np.meshgrid(np.linspace(0, 1, 10),
                                     np.linspace(0, 1, 10))
        print(a)

    # Given two arrays, X and Y, construct the Cauchy matrix C (Cij = 1/(xi - yj))
    def class39(self):
        x = np.arange(3)
        print(x)
        y = x + 0.5
        a = x - y
        print(a)
        z = np.subtract.outer(x, y)
        print(z)
        c = 1.0 / z
        print(c)
        print(np.linalg.det(c))

    # Print the minimum and maximum representable value for each numpy scalar type (★★☆)
    def class40(self):
        for dtype in [np.int8, np.int32, np.int64]:
            min = np.iinfo(dtype).min
            max = np.iinfo(dtype).max
            print(min, hex(min).upper())
            print(max, hex(max).upper())
        for dtype in [np.float32, np.float64]:
            print(np.finfo(dtype).min)
            print(np.finfo(dtype).max)
            print(np.finfo(dtype).eps)

    # How to print all the values of an array? (★★☆)
    def class41(self):
        # np.set_printoptions(threshold=np.inf)
        a = np.zeros((16, 16))
        print(a)

    # How to find the closest value (to a given scalar) in an array? (★★☆)
    def class42(self):
        a = np.arange(10)
        print(a)
        b = np.random.uniform(0, 10)
        print(b)
        c = np.abs(a - b)
        print(c)
        idx = c.argmin()
        print(a[idx])

    # Create a structured array representing a position (x,y) and a color (r,g,b) (★★☆)
    def class43(self):
        a = np.zeros(10, [('position', [('x', float, 1), ('y', float, 1)]),
                          ('color', [('r', float, 1), ('g', float, 1), ('b', float, 1)])])
        print(a)
        b = a[1]['position']
        c = a[1]['color']
        print(b, c)

    # Consider a random vector with shape (100,2) representing coordinates, find point by point distances (★★☆)
    def class44(self):
        a = np.random.random((5, 2))
        print(a)
        x, y = np.atleast_2d(a[:, 0]), np.atleast_2d(a[:, 1])
        print(x)
        print(y)
        d = np.sqrt((x - x.T) ** 2 + (y - y.T) ** 2)
        print(d)

    # How to convert a float (32 bits) array into an integer (32 bits) in place?
    def class45(self):
        a = np.zeros(10, dtype=np.int32)
        print(a)
        a = a.astype(np.float32, copy=False)
        print(a)
        a = a.astype(np.int32, copy=False)
        print(a)

    # How to read the following file? (★★☆)
    def class46(self):
        a = np.genfromtxt('class46.txt', delimiter=',', skip_header=0)
        print(a)
        a[np.isnan(a)] = 0
        print(a)
        a = np.genfromtxt('class46.txt', delimiter=',', skip_header=1)
        print(a)
        a[np.isnan(a)] = 0
        print(a)

    # What is the equivalent of enumerate for numpy arrays? (★★☆)
    def class47(self):
        a = np.arange(9).reshape(3, 3)
        print(a)
        for index, value in np.ndenumerate(a):
            print(index, value)
        for index in np.ndindex(a.shape):
            print(index, a[index])

    # Generate a generic 2D Gaussian-like array (★★☆)
    def class48(self):
        a = np.linspace(-1, 1, 5)
        print(a)
        x, y = np.meshgrid(a, a)
        print(x)
        print(y)
        d = np.sqrt(x**2 + y**2)
        print(d)
        sigma, mu = 1.0, 0.0
        g = np.exp(-((d - mu) ** 2 / (2.0 * sigma ** 2)))
        print(g)

    # How to randomly place p elements in a 2D array? (★★☆)
    def class49(self):
        n = 5
        p = 3
        z = np.zeros((n, n))
        print(z)
        a = np.random.choice(range(n*n), p, replace=False)
        print(a)
        np.put(z, a, 1)
        print(z)

        for _ in range(5):
            a = np.random.choice(5, 3, replace=False, p=[0.01, 0, 0.10, 0.89, 0])
            print(a)

    # Subtract the mean of each row of a matrix (★★☆)
    def class50(self):
        x = np.random.rand(2, 3)
        print(x)
        y = x - x.mean(axis=1, keepdims=True)
        print(y)
        y = x - x.mean(axis=1).reshape(-1, 1)
        print(y)

    # How to I sort an array by the nth column? (★★☆)
    def class51(self):
        a = np.random.randint(0, 10, (3, 3))
        print(a)
        b = a[:, 1]
        print(b)
        b = b.argsort()
        print(b)
        print(a[b])

    # How to tell if a given 2D array has null columns? (★★☆)
    def class52(self):
        a = np.random.randint(0, 3, (3, 10))
        print(a)
        print(a.any())
        print(a.any(axis=0))
        print(~a.any(axis=0))
        print((~a.any(axis=0)).any())

    # Find the nearest value from a given value in an array (★★☆)
    def class53(self):
        a = np.random.uniform(0, 1, 10)
        print(a)
        b = 0.5
        b = np.abs(a - b)
        print(b.argmin())
        m = a.flat[b.argmin()]
        print(m)

    # Create an array class that has a name attribute (★★☆)
    def class54(self):
        # class NamedArray(np.ndarray):
        #     def __new__(cls, array, name="no name"):
        #         obj = np.asarray(array).view(cls)
        #         obj.name = name
        #         return obj
        #
        #     def __array_finalize__(self, obj):
        #         if obj is None: return
        #         self.info = getattr(obj, 'name', "no name")
        #
        # Z = NamedArray(np.arange(10), "range_10")
        # print(Z.name)
        pass

    # Consider a given vector, how to add 1 to each element indexed by a second vector
    # (be careful with repeated indices)? (★★★)
    def class55(self):
        z = np.ones(10)
        print(z)
        i = np.random.randint(0, len(z), 20)
        print(i)
        z += np.bincount(i, minlength=len(z))
        print(z)

        x = np.array([2, 1, 3, 4, 7, 3])
        print(np.bincount(x))
        y = np.array([0.3, 0.5, 0.2, 0.7, 1., -0.6])
        print(np.bincount(x, weights=y))

    # How to accumulate elements of a vector (X) to an array (F) based on an index list (I)? (★★★)
    def class56(self):
        x = [1, 2, 3, 4, 5, 6]
        i = [1, 3, 9, 3, 4, 1]
        f = np.bincount(i, x)
        print(f)

    # Considering a (w,h,3) image of (dtype=ubyte), compute the number of unique colors (★★★)
    def class57(self):
        w, h = 4, 4
        i = np.random.randint(0, 2, (h, w, 3)).astype(np.ubyte)
        print(i)
        f = i[..., 0] * 256 * 256 + i[..., 1] * 256 + i[..., 2]
        print(f)
        print(np.unique(f))
        n = len(np.unique(f))
        print(n)
        print(np.unique(i))

    # Considering a four dimensions array, how to get sum over the last two axis at once? (★★★)
    def class58(self):
        a = np.random.randint(0, 10, (2, 3, 4, 5))
        print(a)
        print(a.shape)
        b = a.shape[: -2]
        print(b + (-1, ))
        c = a.reshape(b + (-1, ))
        print(c)
        print(c.sum(axis=0))
        print(c.sum(axis=1))
        print(c.sum(axis=-1))

    # Considering a one-dimensional vector D,
    # how to compute means of subsets of D using a vector S of same size describing subset indices? (★★★)
    def class59(self):
        d = np.random.uniform(0, 1, 100)
        s = np.random.randint(0, 10, 100)
        ds = np.bincount(s, weights=d)
        dc = np.bincount(s)
        dm = ds / dc
        print(dm)

    # How to get the diagonal of a dot product? (★★★)
    def class60(self):
        a = np.random.randint(1, 9, (3, 3))
        print(a)
        b = np.random.randint(1, 9, (3, 3))
        print(b)
        print(np.dot(a, b))
        print(np.diag(np.dot(a, b)))
        print('=============================')
        print(a)
        print(b.T)
        print(a * b.T)
        print('-----------------------------')
        print(np.sum(a * b.T, axis=0))
        print(np.sum(a * b.T, axis=1))

    # Consider the vector [1, 2, 3, 4, 5],
    # how to build a new vector with 3 consecutive zeros interleaved between each value? (★★★)
    def class61(self):
        a = np.arange(1, 6)
        print(a)
        n = 3
        b = np.zeros(len(a) + (len(a) - 1) * n)
        print(b)
        b[::n+1] = a
        print(b)

    # Consider an array of dimension (5,5,3), how to mulitply it by an array with dimensions (5,5)? (★★★)
    def class62(self):
        a = np.ones((5, 5, 3))
        print(a)
        print('=============================')
        b = 2 * np.ones((5, 3))
        print(b)
        print('-----------------------------')
        print(a * b[None, :, :])

    # How to swap two rows of an array? (★★★)
    def class63(self):
        a = np.arange(25).reshape(5, 5)
        print(a)
        a[[0, 1]] = a[[1, 0]]
        print(a)
        print('==================================')
        a = np.array([[1, 2, 3], [2, 3, 4], [1, 6, 5], [9, 3, 4]])
        print(a)
        a[[1, 2], :] = a[[2, 1], :]
        print(a)

    # Consider a set of 10 triplets describing 10 triangles (with shared vertices),
    # find the set of unique line segments composing all the triangles (★★★)
    def class64(self):
        a = np.random.randint(0, 100, (10, 3))
        print(a)
        print('11111111111111111111111111111111')
        b = a.repeat(2, axis=1)
        print(b)
        print('22222222222222222222222222222222')
        f = np.roll(b, -1, axis=1)
        print(f)
        print('33333333333333333333333333333333')
        f = f.reshape(len(a) * 3, 2)
        print(f)
        print('44444444444444444444444444444444')
        f = np.sort(f, axis=1)
        print(f)
        print('55555555555555555555555555555555')
        g = f.view(dtype=[('p0', f.dtype), ('p1', f.dtype)])
        print(g)
        print('66666666666666666666666666666666')
        g = np.unique(g)
        print(g)

    # Given an array C that is a bincount, how to produce an array A such that np.bincount(A) == C? (★★★)
    def class65(self):
        c = np.bincount([1, 1, 2, 3, 4, 4, 6])
        a = np.repeat(np.arange(len(c)), c)
        print(a)

    # How to compute averages using a sliding window over an array? (★★★)
    def class66(self):
        a = np.arange(20)
        print(a)
        print('11111111111111111111111111111111')
        n = 5
        r = np.cumsum(a, dtype=float)
        print(r)
        print('22222222222222222222222222222222')
        print(r[n:])
        print(r[:-n])
        r[n:] = r[n:] - r[:-n]
        print(r[n:])
        print('33333333333333333333333333333333')
        print(r)
        print('44444444444444444444444444444444')
        k = r[n-1] / n
        print(r[n-1])
        print(k)

        b = np.arange(20)
        m = 5
        s = np.cumsum(b, dtype=float)
        l = s[m-1] / m
        print(l)

    # Consider a one-dimensional array Z,
    # build a two-dimensional array whose first row is (Z[0],Z[1],Z[2]) and
    # each subsequent row is shifted by 1 (last row should be (Z[-3],Z[-2],Z[-1]) (★★★)
    def class67(self):
        a = np.arange(10)
        print(a)
        w = 3
        shape = (a.size - w + 1, w)
        print(shape)
        strides = (a.itemsize, a.itemsize)
        print(strides)
        z = stride_tricks.as_strided(a, shape=shape, strides=strides)
        print(z)


if __name__ == '__main__':
    sn = StudyNumpy()
    sn.class67()
