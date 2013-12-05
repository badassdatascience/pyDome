#    pyDome:  A geodesic dome calculator
#    Copyright (C) 2013  Daniel Williams
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np

PI = np.pi

from Polyhedral import Vertex


class SymmetryTriangle(object):

  def convertRCNotationToVertexNumber(self, r, c):
    cnt = 1;
    for i in range(len(self.row_list)):
      for j in range(len(self.row_list[i])):
        if (i == r) and (j == c):
          return cnt
	cnt = cnt + 1;
    return cnt

  def __init__(self, chord_frequency):

    # self.chord_list and self.face_list contain integers indicating local position
    # on the symmetry triangle, and therefore do not use the Chord and Face 
    # classes defined in Polyhedral.py

    # specify chords
    self.chord_list = []
    for r in range(len(self.row_list)):
      for c in range(0, len(self.row_list[r])):

        if r + c != chord_frequency:
          the_start = self.convertRCNotationToVertexNumber(r, c)
	  the_end = self.convertRCNotationToVertexNumber(r+1, c)
	  self.chord_list.append([the_start, the_end])
	
	  the_start = self.convertRCNotationToVertexNumber(r, c)
	  the_end = self.convertRCNotationToVertexNumber(r, c+1)
	  self.chord_list.append([the_start, the_end])

	if c != 0:
          the_start = self.convertRCNotationToVertexNumber(r, c);
	  the_end = self.convertRCNotationToVertexNumber(r+1, c-1);
	  self.chord_list.append([the_start, the_end])

    # specify faces
    self.face_list = []
    for r in range(len(self.row_list)):
      for c in range(0, len(self.row_list[r]) - 1):
        the_first = self.convertRCNotationToVertexNumber(r, c)
	the_second = self.convertRCNotationToVertexNumber(r, c+1)
	the_third = self.convertRCNotationToVertexNumber(r+1, c)
	self.face_list.append([the_first, the_second, the_third])

	if c != 0 and r + 1 != chord_frequency:

          the_first = self.convertRCNotationToVertexNumber(r+1, c-1)
	  the_second = self.convertRCNotationToVertexNumber(r, c)
	  the_third = self.convertRCNotationToVertexNumber(r+1, c)
	  self.face_list.append([the_first, the_second, the_third])



class ClassOneMethodOneSymmetryTriangle(SymmetryTriangle):
  def __init__(self, f, polyhedral):

    # specify vertices
    CL = polyhedral.ppt_side_length
    self.row_list = []
    self.vertices = []
    for r in range(0, f + 1):
      col_list = []
      for c in range(0, f - r + 1):
        x = ((CL / np.float64(f)) * np.float64(r) * np.cos(PI / 3.)) + (CL / np.float64(f)) * np.float64(c) - (CL / np.float64(2.));
	y = (CL / np.float64(f)) * np.float64(r) * np.sin(PI / 3.) - ((CL / np.float64(3.)) * np.sin(PI / np.float64(3)));
	col_list.append(Vertex(x, y, 0.))
	self.vertices.append(Vertex(x, y, 0.))
      self.row_list.append(col_list)

    super(ClassOneMethodOneSymmetryTriangle, self).__init__(f)

