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

def get_bill_of_materials(V, C, rounding_precision):
  bom = {}
  for c in C:
    v1 = V[c[0] - 1]
    v2 = V[c[1] - 1]
    distance_between = round(np.linalg.linalg.norm(v1 - v2), rounding_precision)  # CHECK THIS!

    if not bom.has_key(distance_between):
      bom[distance_between] = 0
    bom[distance_between] += 1

  #
  # display
  #
  keys = [x for x in sorted(bom.keys())]
  keys.reverse()
  print
  print 'Bill of Materials'
  print
  print '\tlength\tnumber'
  for k in keys:
      print '\t' + str(k) + '\t' + str(bom[k])
  print
  print 'Small length chords could be artifacts, so check them with a DXF viewer before you build anything!'
  print

  #
  # data structure to store hub information
  #
  hubs = {}
  for c in C:
    if not hubs.has_key(c[0]):  hubs[c[0]] = {'connected_vertices': {}, 'vertex' : None}
    hubs[c[0]]['connected_vertices'][c[1]] = {'vertex' : V[c[1]-1]}
    hubs[c[0]]['vertex'] = V[c[0]-1]
    if not hubs.has_key(c[1]):  hubs[c[1]] = {'connected_vertices' : {}, 'vertex' : None}
    hubs[c[1]]['connected_vertices'][c[0]] = {'vertex' : V[c[0]-1]}
    hubs[c[1]]['vertex'] = V[c[1]-1]


  #
  # compute angles at hub between outbound chords and tangential plane
  #
  for h in hubs.keys():
    vertex = hubs[h]['vertex']
    for c in hubs[h]['connected_vertices']:
      A = vertex
      B = vertex - hubs[h]['connected_vertices'][c]['vertex']
      angle = (np.pi/2) - np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)))
      angle_in_degrees = 180 * angle / np.pi
      hubs[h]['connected_vertices'][c]['tangential_angle'] = angle_in_degrees

  #
  # display the tangential plane angles we just calculated
  #
  print 'Angles at hub between outbound cords and tangential plane:'
  print
  print '\thub\tconnecting hub\tangle (degrees)'
  for h in hubs.keys():
    print '\t' + str(h)
    number_of_connected_vertices = len(hubs[h]['connected_vertices'])
    for c in hubs[h]['connected_vertices']:
      if number_of_connected_vertices == 1:
        print '\t\t' + str(c) + '\t' + 'base hub of truncated sphere, no angle to report'
      else:
        print '\t\t' + str(c) + '\t' + str(hubs[h]['connected_vertices'][c]['tangential_angle'])
