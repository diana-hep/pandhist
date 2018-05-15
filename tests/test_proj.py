#!/usr/bin/env python

# Copyright (c) 2017, DIANA-HEP
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest

import numpy

from histbook.axis import *
from histbook.hist import *

class TestProj(unittest.TestCase):
    def runTest(self):
        pass

    def test_bin_axis(self):
        for underflow in False, True:
            for overflow in False, True:
                h = Hist(bin("x", 4, -1, 1, underflow=underflow, overflow=overflow))
                if underflow:
                    self.assertEqual(h.only("x < -1").axis("x"), bin("x", 0,   -1,   -1, underflow=underflow,    overflow=False, nanflow=False))
                self.assertEqual(h.only("x < -0.5").axis("x"),   bin("x", 1,   -1, -0.5, underflow=underflow,    overflow=False, nanflow=False))
                self.assertEqual(h.only("x < 0").axis("x"),      bin("x", 2,   -1,    0, underflow=underflow,    overflow=False, nanflow=False))
                self.assertEqual(h.only("x < 0.5").axis("x"),    bin("x", 3,   -1,  0.5, underflow=underflow,    overflow=False, nanflow=False))
                self.assertEqual(h.only("x < 1").axis("x"),      bin("x", 4,   -1,    1, underflow=underflow,    overflow=False, nanflow=False))

                self.assertEqual(h.only("x >= -1").axis("x"),    bin("x", 4,   -1,    1,     underflow=False, overflow=overflow, nanflow=False))
                self.assertEqual(h.only("x >= -0.5").axis("x"),  bin("x", 3, -0.5,    1,     underflow=False, overflow=overflow, nanflow=False))
                self.assertEqual(h.only("x >= 0").axis("x"),     bin("x", 2,    0,    1,     underflow=False, overflow=overflow, nanflow=False))
                self.assertEqual(h.only("x >= 0.5").axis("x"),   bin("x", 1,  0.5,    1,     underflow=False, overflow=overflow, nanflow=False))
                if overflow:
                    self.assertEqual(h.only("x >= 1").axis("x"), bin("x", 0,    1,    1,     underflow=False, overflow=overflow, nanflow=False))

                h = Hist(bin("x", 4, -1, 1, underflow=underflow, overflow=overflow, closedlow=False))
                if underflow:
                    self.assertEqual(h.only("x <= -1").axis("x"), bin("x", 0,   -1,   -1, underflow=underflow,    overflow=False, nanflow=False, closedlow=False))
                self.assertEqual(h.only("x <= -0.5").axis("x"),   bin("x", 1,   -1, -0.5, underflow=underflow,    overflow=False, nanflow=False, closedlow=False))
                self.assertEqual(h.only("x <= 0").axis("x"),      bin("x", 2,   -1,    0, underflow=underflow,    overflow=False, nanflow=False, closedlow=False))
                self.assertEqual(h.only("x <= 0.5").axis("x"),    bin("x", 3,   -1,  0.5, underflow=underflow,    overflow=False, nanflow=False, closedlow=False))
                self.assertEqual(h.only("x <= 1").axis("x"),      bin("x", 4,   -1,    1, underflow=underflow,    overflow=False, nanflow=False, closedlow=False))

                self.assertEqual(h.only("x > -1").axis("x"),      bin("x", 4,   -1,    1,     underflow=False, overflow=overflow, nanflow=False, closedlow=False))
                self.assertEqual(h.only("x > -0.5").axis("x"),    bin("x", 3, -0.5,    1,     underflow=False, overflow=overflow, nanflow=False, closedlow=False))
                self.assertEqual(h.only("x > 0").axis("x"),       bin("x", 2,    0,    1,     underflow=False, overflow=overflow, nanflow=False, closedlow=False))
                self.assertEqual(h.only("x > 0.5").axis("x"),     bin("x", 1,  0.5,    1,     underflow=False, overflow=overflow, nanflow=False, closedlow=False))
                if overflow:
                    self.assertEqual(h.only("x > 1").axis("x"),   bin("x", 0,    1,    1,     underflow=False, overflow=overflow, nanflow=False, closedlow=False))

    def test_bin_content(self):
        for nanflow in False, True:
            h = Hist(bin("x", 4, -1, 1, underflow=True, overflow=True, nanflow=nanflow))
            h._content = numpy.arange(1, h.axis("x").totbins + 1, dtype=numpy.float64).reshape(h.axis("x").totbins, 1)
            self.assertEqual(h.only("x < -1")._content.tolist(), [[1]])
            self.assertEqual(h.only("x < -0.5")._content.tolist(), [[1], [2]])
            self.assertEqual(h.only("x < 0")._content.tolist(), [[1], [2], [3]])
            self.assertEqual(h.only("x < 0.5")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x < 1")._content.tolist(), [[1], [2], [3], [4], [5]])
            self.assertEqual(h.only("x >= -1")._content.tolist(), [[2], [3], [4], [5], [6]])
            self.assertEqual(h.only("x >= -0.5")._content.tolist(), [[3], [4], [5], [6]])
            self.assertEqual(h.only("x >= 0")._content.tolist(), [[4], [5], [6]])
            self.assertEqual(h.only("x >= 0.5")._content.tolist(), [[5], [6]])
            self.assertEqual(h.only("x >= 1")._content.tolist(), [[6]])

            h = Hist(bin("x", 4, -1, 1, underflow=True, overflow=False, nanflow=nanflow))
            h._content = numpy.arange(1, h.axis("x").totbins + 1, dtype=numpy.float64).reshape(h.axis("x").totbins, 1)
            self.assertEqual(h.only("x < -1")._content.tolist(), [[1]])
            self.assertEqual(h.only("x < -0.5")._content.tolist(), [[1], [2]])
            self.assertEqual(h.only("x < 0")._content.tolist(), [[1], [2], [3]])
            self.assertEqual(h.only("x < 0.5")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x < 1")._content.tolist(), [[1], [2], [3], [4], [5]])
            self.assertEqual(h.only("x >= -1")._content.tolist(), [[2], [3], [4], [5]])
            self.assertEqual(h.only("x >= -0.5")._content.tolist(), [[3], [4], [5]])
            self.assertEqual(h.only("x >= 0")._content.tolist(), [[4], [5]])
            self.assertEqual(h.only("x >= 0.5")._content.tolist(), [[5]])

            h = Hist(bin("x", 4, -1, 1, underflow=False, overflow=True, nanflow=nanflow))
            h._content = numpy.arange(1, h.axis("x").totbins + 1, dtype=numpy.float64).reshape(h.axis("x").totbins, 1)
            self.assertEqual(h.only("x < -0.5")._content.tolist(), [[1]])
            self.assertEqual(h.only("x < 0")._content.tolist(), [[1], [2]])
            self.assertEqual(h.only("x < 0.5")._content.tolist(), [[1], [2], [3]])
            self.assertEqual(h.only("x < 1")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x >= -1")._content.tolist(), [[1], [2], [3], [4], [5]])
            self.assertEqual(h.only("x >= -0.5")._content.tolist(), [[2], [3], [4], [5]])
            self.assertEqual(h.only("x >= 0")._content.tolist(), [[3], [4], [5]])
            self.assertEqual(h.only("x >= 0.5")._content.tolist(), [[4], [5]])
            self.assertEqual(h.only("x >= 1")._content.tolist(), [[5]])

            h = Hist(bin("x", 4, -1, 1, underflow=False, overflow=False, nanflow=nanflow))
            h._content = numpy.arange(1, h.axis("x").totbins + 1, dtype=numpy.float64).reshape(h.axis("x").totbins, 1)
            self.assertEqual(h.only("x < -0.5")._content.tolist(), [[1]])
            self.assertEqual(h.only("x < 0")._content.tolist(), [[1], [2]])
            self.assertEqual(h.only("x < 0.5")._content.tolist(), [[1], [2], [3]])
            self.assertEqual(h.only("x < 1")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x >= -1")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x >= -0.5")._content.tolist(), [[2], [3], [4]])
            self.assertEqual(h.only("x >= 0")._content.tolist(), [[3], [4]])
            self.assertEqual(h.only("x >= 0.5")._content.tolist(), [[4]])

        for nanflow in False, True:
            h = Hist(bin("x", 4, -1, 1, underflow=True, overflow=True, nanflow=nanflow, closedlow=False))
            h._content = numpy.arange(1, h.axis("x").totbins + 1, dtype=numpy.float64).reshape(h.axis("x").totbins, 1)
            self.assertEqual(h.only("x <= -1")._content.tolist(), [[1]])
            self.assertEqual(h.only("x <= -0.5")._content.tolist(), [[1], [2]])
            self.assertEqual(h.only("x <= 0")._content.tolist(), [[1], [2], [3]])
            self.assertEqual(h.only("x <= 0.5")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x <= 1")._content.tolist(), [[1], [2], [3], [4], [5]])
            self.assertEqual(h.only("x > -1")._content.tolist(), [[2], [3], [4], [5], [6]])
            self.assertEqual(h.only("x > -0.5")._content.tolist(), [[3], [4], [5], [6]])
            self.assertEqual(h.only("x > 0")._content.tolist(), [[4], [5], [6]])
            self.assertEqual(h.only("x > 0.5")._content.tolist(), [[5], [6]])
            self.assertEqual(h.only("x > 1")._content.tolist(), [[6]])

            h = Hist(bin("x", 4, -1, 1, underflow=True, overflow=False, nanflow=nanflow, closedlow=False))
            h._content = numpy.arange(1, h.axis("x").totbins + 1, dtype=numpy.float64).reshape(h.axis("x").totbins, 1)
            self.assertEqual(h.only("x <= -1")._content.tolist(), [[1]])
            self.assertEqual(h.only("x <= -0.5")._content.tolist(), [[1], [2]])
            self.assertEqual(h.only("x <= 0")._content.tolist(), [[1], [2], [3]])
            self.assertEqual(h.only("x <= 0.5")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x <= 1")._content.tolist(), [[1], [2], [3], [4], [5]])
            self.assertEqual(h.only("x > -1")._content.tolist(), [[2], [3], [4], [5]])
            self.assertEqual(h.only("x > -0.5")._content.tolist(), [[3], [4], [5]])
            self.assertEqual(h.only("x > 0")._content.tolist(), [[4], [5]])
            self.assertEqual(h.only("x > 0.5")._content.tolist(), [[5]])

            h = Hist(bin("x", 4, -1, 1, underflow=False, overflow=True, nanflow=nanflow, closedlow=False))
            h._content = numpy.arange(1, h.axis("x").totbins + 1, dtype=numpy.float64).reshape(h.axis("x").totbins, 1)
            self.assertEqual(h.only("x <= -0.5")._content.tolist(), [[1]])
            self.assertEqual(h.only("x <= 0")._content.tolist(), [[1], [2]])
            self.assertEqual(h.only("x <= 0.5")._content.tolist(), [[1], [2], [3]])
            self.assertEqual(h.only("x <= 1")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x > -1")._content.tolist(), [[1], [2], [3], [4], [5]])
            self.assertEqual(h.only("x > -0.5")._content.tolist(), [[2], [3], [4], [5]])
            self.assertEqual(h.only("x > 0")._content.tolist(), [[3], [4], [5]])
            self.assertEqual(h.only("x > 0.5")._content.tolist(), [[4], [5]])
            self.assertEqual(h.only("x > 1")._content.tolist(), [[5]])

            h = Hist(bin("x", 4, -1, 1, underflow=False, overflow=False, nanflow=nanflow, closedlow=False))
            h._content = numpy.arange(1, h.axis("x").totbins + 1, dtype=numpy.float64).reshape(h.axis("x").totbins, 1)
            self.assertEqual(h.only("x <= -0.5")._content.tolist(), [[1]])
            self.assertEqual(h.only("x <= 0")._content.tolist(), [[1], [2]])
            self.assertEqual(h.only("x <= 0.5")._content.tolist(), [[1], [2], [3]])
            self.assertEqual(h.only("x <= 1")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x > -1")._content.tolist(), [[1], [2], [3], [4]])
            self.assertEqual(h.only("x > -0.5")._content.tolist(), [[2], [3], [4]])
            self.assertEqual(h.only("x > 0")._content.tolist(), [[3], [4]])
            self.assertEqual(h.only("x > 0.5")._content.tolist(), [[4]])
