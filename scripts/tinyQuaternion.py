"""
This file is part of the tinyq python module
Author:         Reza Ahmadzadeh
Website:        https://github.com/rezaahmadzadeh/tinyquaternion
Documentation:  https://github.com/rezaahmadzadeh/tinyquaternion
Version:         1.0.0
License:         The MIT License (MIT)
Copyright (c) 2019 Reza Ahmadzadeh
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
tinyQuaternion.py - This file defines the core Quaternion class
"""

import numpy as np

class Quaternion:
    """
    TinyQ
    a library for quaternion operations in Python """

    def __init__(self, q=None, a=None, n=None):
        # either q or (n,a) has to be given
        if q is None:
            # convert (n,a) to quaternion
            self.q = np.concatenate(([np.cos(a/2)],n*np.sin(a/2)),axis=0)
        else:
            # self.q = q / np.dot(q,q)
            self.q = q
            # convert q to (n,a) --- not used
            #if n is None and a is None:
            #    self.a = 2*np.arccos(self.q[0])
            #    self.n = self.q[1:] / np.sin(self.a/2)

    @property
    def w(self):
        return self.q[0]

    @property
    def x(self):
        return self.q[1]

    @property
    def y(self):
        return self.q[2]

    @property
    def z(self):
        return self.q[3]
    
    @property
    def vector(self):
        ''' get the vector part '''
        return self.q[1:]

    @property
    def scalar(self):
        ''' get the scalar part '''
        return self.q[0]

    @property
    def magnitude(self):
        ''' get the magnitude '''
        return np.sqrt(np.dot(self.q, self.q))

    def is_unit(self, tol = 1e-10):
        ''' check for unit quaternion '''
        return np.abs(1.0 - self.magnitude) < tol

    @property
    def normalized(self):
        ''' normalize a quaternion '''
        if not self.is_unit():
            n = self.magnitude
            if n > 0:
                # self.q /= n # this will change the main object
                return self.__class__(q= self.q / n)

        return self.q
         

    @property
    def conjugate(self):
        ''' get conjugate of a quaternion '''
        return self.__class__(q=np.concatenate((np.array([self.scalar]), -self.vector), axis=0))

    @property
    def inverse(self):
        ''' get inverse of a quaternion '''
        ss = np.dot(self.q, self.q)
        if ss > 0:
            d = self.conjugate
            return self.__class__(q = d.q / ss)
        else:
            raise ZeroDivisionError("a zero quaternion cannot be inverted")

    @property
    def log(self):
        ''' get log of a quaternion '''
        v = self.vector
        s = self.scalar
        z = (v / np.sqrt(np.dot(v,v))) * np.arccos(s / self.magnitude)
        r = np.concatenate(([np.log(self.magnitude)],z),axis=0)
        return self.__class__(q=r)

    @property
    def exp(self):
        ''' get exp of a quaternion '''
        v = self.vector
        vn = np.sqrt(np.dot(v,v))
        s = self.scalar
        r = np.exp(s)* np.concatenate(([np.cos(vn)],(np.sin(vn)/vn)*v),axis=0)
        return self.__class__(q=r)

   
    def axisangle(self):
        ''' quaternion to axis-angle '''
        self.a = 2*np.arccos(self.q[0])
        self.n = self.q[1:] / np.sin(self.a/2)
        return self.n, self.a

    #### OPERATIONS ####
    def add(self, other):
        return self.__class__(q = self.q + other.q)

    def sub(self, other):
        return self.__class__(q = self.q - other.q)

    def mul(self, other):
        q1 = self.q
        q2 = other.q
        w = q1[0]*q2[0] - np.dot(q1[1:],q2[1:])
        v = q2[0]*q1[1:] + q1[0]*q2[1:] + np.cross(q1[1:],q2[1:])
        m = np.concatenate((np.array([w]),v), axis = 0)
        return self.__class__(q=m)

    def div(self, other):
        q2i = other.inverse
        return self.mul(q2i)

    def rotatePoint(self, p):
        '''
        rotate a point using P = q P q^-1
        '''
        # convert the point to a quaternion format
        P = np.concatenate((np.array([0.]), p), axis = 0)
        P = self.__class__(q=P)
        Pn = self.mul(P)
        Pr = Pn.mul(self.inverse)
        return Pr.vector

    def __str__(self):
        ''' the format when we print the quaternion '''
        return "[{:.3f} {:.3f} {:.3f} {:.3f}]".format(self.q[0],self.q[1],self.q[2],self.q[3])

    def __repr__(self):
        ''' the format in the command line, using repr() '''
        return "Quaternion({}, {}, {}, {})".format(repr(self.q[0]),repr(self.q[1]),repr(self.q[2]),repr(self.q[3]))

'''
if __name__ == "__main__":
    q1 = Quaternion(a=np.pi/3, n=np.array([0.,0.,1.]))
    p = np.array([1.,2.,-1.])
    print(q1.rotatePoint(p))
'''
