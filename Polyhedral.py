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

class Face():
  def __init__(self, v1, v2, v3):
    self.v1 = v1
    self.v2 = v2
    self.v3 = v3

    self.origin = (self.v1.xyz + self.v2.xyz + self.v3.xyz) / np.float64(3.)

    # compute transfer matrix
    x = self.v2.xyz - self.v1.xyz
    x = x / np.linalg.linalg.norm(x)
    y = self.v3.xyz - self.origin
    y = y / np.linalg.linalg.norm(y)
    z = np.cross(x, y)
    self.transfer_matrix = np.transpose(np.matrix([x, y, z]))

class Chord():
  def __init__(self, v1, v2):
    self.v1 = v1
    self.v2 = v2

class Vertex():
  def __init__(self, x, y, z):
    self.xyz = np.array([x, y, z])
		
  def distance_to(self, vertex):
    return np.linalg.linalg.norm(self.xyz - vertex.xyz)
	
class Polyhedron(object):
  def __init__(self):
    self.ppt_side_length = self.vertices[0].distance_to(self.vertices[1])

class Octahedron(Polyhedron):
  def __init__(self):

    self.vertices = [
      Vertex(np.float64(0.), np.float64(0.), np.float64(1.)),
      Vertex(np.float64(1.), np.float64(0.), np.float64(0.)),
      Vertex(np.float64(0.), np.float64(1.), np.float64(0.)),
      Vertex(np.float64(-1.), np.float64(0.), np.float64(0.)),
      Vertex(np.float64(0.), np.float64(-1.), np.float64(0.)),
      Vertex(np.float64(0.), np.float64(0.), np.float64(-1.)),
      ]

    self.faces = [
	    Face(self.vertices[1], self.vertices[2], self.vertices[0]),
	    Face(self.vertices[2], self.vertices[3], self.vertices[0]),
	    Face(self.vertices[3], self.vertices[4], self.vertices[0]),
	    Face(self.vertices[4], self.vertices[1], self.vertices[0]),
	    Face(self.vertices[5], self.vertices[2], self.vertices[1]),
	    Face(self.vertices[5], self.vertices[3], self.vertices[2]),
	    Face(self.vertices[5], self.vertices[4], self.vertices[3]),
	    Face(self.vertices[5], self.vertices[1], self.vertices[4]),
            ]

    self.chords = [
	    Chord(self.vertices[0], self.vertices[1]),
	    Chord(self.vertices[0], self.vertices[2]),
	    Chord(self.vertices[0], self.vertices[3]),
	    Chord(self.vertices[0], self.vertices[4]),
	    Chord(self.vertices[5], self.vertices[1]),
	    Chord(self.vertices[5], self.vertices[2]),
	    Chord(self.vertices[5], self.vertices[3]),
	    Chord(self.vertices[5], self.vertices[4]),
            Chord(self.vertices[1], self.vertices[2]),
            Chord(self.vertices[2], self.vertices[3]),
            Chord(self.vertices[3], self.vertices[4]),
            Chord(self.vertices[4], self.vertices[1]),
	    ]

    super(Octahedron, self).__init__()


class Icosahedron(Polyhedron):
  def __init__(self):
    self.sine_of_phi = np.float64(2.) / np.sqrt(np.float64(5.))
    self.cosine_of_phi = np.float64(0.5) * self.sine_of_phi

    self.vertices = [
	    Vertex(np.float64(0.), np.float64(0.), np.float64(1.)),
	    Vertex(self.sine_of_phi, 0., self.cosine_of_phi),
	    Vertex(self.sine_of_phi*np.cos(0.4*PI), self.sine_of_phi*np.sin(0.4*PI), self.cosine_of_phi),
	    Vertex(self.sine_of_phi*np.cos(0.8*PI), self.sine_of_phi*np.sin(0.8*PI), self.cosine_of_phi),
	    Vertex(self.sine_of_phi*np.cos(0.8*PI), -self.sine_of_phi*np.sin(0.8*PI), self.cosine_of_phi),
	    Vertex(self.sine_of_phi*np.cos(0.4*PI), -self.sine_of_phi*np.sin(0.4*PI), self.cosine_of_phi),
	    Vertex(-self.sine_of_phi*np.cos(0.8*PI), -self.sine_of_phi*np.sin(0.8*PI), -self.cosine_of_phi),
	    Vertex(-self.sine_of_phi*np.cos(0.8*PI), self.sine_of_phi*np.sin(0.8*PI), -self.cosine_of_phi),
	    Vertex(-self.sine_of_phi*np.cos(0.4*PI), self.sine_of_phi*np.sin(0.4*PI), -self.cosine_of_phi),
	    Vertex(-self.sine_of_phi, 0., -self.cosine_of_phi),
	    Vertex(-self.sine_of_phi*np.cos(0.4*PI), -self.sine_of_phi*np.sin(0.4*PI), -self.cosine_of_phi),
	    Vertex(np.float64(0.), np.float64(0.), np.float64(-1.))
	    ]

    self.faces = [
	    Face(self.vertices[1], self.vertices[2], self.vertices[0]),
	    Face(self.vertices[2], self.vertices[3], self.vertices[0]),
	    Face(self.vertices[3], self.vertices[4], self.vertices[0]),
	    Face(self.vertices[4], self.vertices[5], self.vertices[0]),
	    Face(self.vertices[5], self.vertices[1], self.vertices[0]),
	    Face(self.vertices[5], self.vertices[6], self.vertices[1]),
	    Face(self.vertices[1], self.vertices[7], self.vertices[2]),
	    Face(self.vertices[2], self.vertices[8], self.vertices[3]),
	    Face(self.vertices[3], self.vertices[9], self.vertices[4]),
	    Face(self.vertices[4], self.vertices[10], self.vertices[5]),
	    Face(self.vertices[1], self.vertices[6], self.vertices[7]),
	    Face(self.vertices[2], self.vertices[7], self.vertices[8]),
	    Face(self.vertices[3], self.vertices[8], self.vertices[9]),
	    Face(self.vertices[4], self.vertices[9], self.vertices[10]),
	    Face(self.vertices[5], self.vertices[10], self.vertices[6]),
	    Face(self.vertices[6], self.vertices[11], self.vertices[7]),
	    Face(self.vertices[7], self.vertices[11], self.vertices[8]),
	    Face(self.vertices[8], self.vertices[11], self.vertices[9]),
	    Face(self.vertices[9], self.vertices[11], self.vertices[10]),
	    Face(self.vertices[10], self.vertices[11], self.vertices[6]),
	    ]
  
    self.chords = [
	    Chord(self.vertices[0], self.vertices[1]),
	    Chord(self.vertices[0], self.vertices[2]),
	    Chord(self.vertices[0], self.vertices[3]),
	    Chord(self.vertices[0], self.vertices[4]),
	    Chord(self.vertices[0], self.vertices[5]),
	    Chord(self.vertices[1], self.vertices[2]),
	    Chord(self.vertices[2], self.vertices[3]),
	    Chord(self.vertices[3], self.vertices[4]),
	    Chord(self.vertices[4], self.vertices[5]),
	    Chord(self.vertices[5], self.vertices[1]),
	    Chord(self.vertices[1], self.vertices[7]),
	    Chord(self.vertices[2], self.vertices[7]),
	    Chord(self.vertices[2], self.vertices[8]),
	    Chord(self.vertices[3], self.vertices[8]),
	    Chord(self.vertices[3], self.vertices[9]),
	    Chord(self.vertices[4], self.vertices[9]),
	    Chord(self.vertices[4], self.vertices[10]),
	    Chord(self.vertices[5], self.vertices[10]),
	    Chord(self.vertices[5], self.vertices[6]),
	    Chord(self.vertices[1], self.vertices[6]),
	    Chord(self.vertices[6], self.vertices[7]),
	    Chord(self.vertices[7], self.vertices[8]),
	    Chord(self.vertices[8], self.vertices[9]),
	    Chord(self.vertices[9], self.vertices[10]),
	    Chord(self.vertices[6], self.vertices[10]),
	    Chord(self.vertices[6], self.vertices[11]),
	    Chord(self.vertices[7], self.vertices[11]),
	    Chord(self.vertices[8], self.vertices[11]),
	    Chord(self.vertices[9], self.vertices[11]),
	    Chord(self.vertices[10], self.vertices[11]),
	    ]
    super(Icosahedron, self).__init__()
