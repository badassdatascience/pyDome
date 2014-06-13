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
      angle_in_degrees = 180. * angle / np.pi
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




  #
  # spoke angles 
  #
  for hub in hubs.keys():
    normal_vector = hubs[hub]['vertex'] / np.linalg.norm(hubs[hub]['vertex'])
    point_on_plane = hubs[hub]['vertex']
    line_origin = np.array([0., 0., 0.])
    for spoke in hubs[hub]['connected_vertices']:
      line = hubs[hub]['connected_vertices'][spoke]['vertex'] / np.linalg.norm(hubs[hub]['connected_vertices'][spoke]['vertex'])
      d = np.dot((point_on_plane - line_origin), normal_vector) / np.dot(line, normal_vector)   # http://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
      hubs[hub]['connected_vertices'][spoke]['point_of_tangential_plane_intersection'] = d * line

  #
  # display spoke angles
  #
  print
  print 'Spoke angles:'
  print
  print '\thub\tconnecting hub\tangle (degrees)'
  for hub in hubs.keys():
    print '\t' + str(hub)
    spoke_list = sorted(hubs[hub]['connected_vertices'])
    vertex = hubs[hub]['vertex']
    point = hubs[hub]['connected_vertices'][spoke_list[0]]['point_of_tangential_plane_intersection']
    reference_vector = point - vertex
    
    print '\t\t' + str(spoke_list[0]) + '\t0.0'
    
    for spoke in spoke_list[1:]:
      point = hubs[hub]['connected_vertices'][spoke]['point_of_tangential_plane_intersection']
      comparison_vector = point - vertex

      normalized_dot_product = np.dot(reference_vector, comparison_vector) / (np.linalg.norm(reference_vector) * np.linalg.norm(comparison_vector))

      if normalized_dot_product < -1.0:
        normalized_dot_product = -1.0

      angle = np.arccos(normalized_dot_product)
      angle_in_degrees = 180. * angle / np.pi

      # http://www.opengl.org/discussion_boards/showthread.php/159385-Deriving-angles-from-0-to-360-from-Dot-Product
      C = np.cross(reference_vector, comparison_vector)
      direction = np.dot(C, vertex)
      if direction < 0.:  angle_in_degrees = -1 * angle_in_degrees

      print '\t\t' + str(spoke) + '\t' +  str(angle_in_degrees)



  ##
  ## display unprojected spoke angles
  ##
  #print
  #print 'Unprojected spoke angles:'
  #print
  #print '\thub\tconnecting hub\tangle (degrees)'
  #for hub in hubs.keys():
  #  print '\t' + str(hub)
  #  spoke_list = sorted(hubs[hub]['connected_vertices'])
  #  vertex = hubs[hub]['vertex']
  #  point = hubs[hub]['connected_vertices'][spoke_list[0]]['vertex']
  #  reference_vector = point - vertex
  #  
  #  print '\t\t' + str(spoke_list[0]) + '\t0.0'
  #  
  #  for spoke in spoke_list[1:]:
  #    point = hubs[hub]['connected_vertices'][spoke]['vertex']
  #    comparison_vector = point - vertex

  #    normalized_dot_product = np.dot(reference_vector, comparison_vector) / (np.linalg.norm(reference_vector) * np.linalg.norm(comparison_vector))

  #    if normalized_dot_product < -1.0:
  #      normalized_dot_product = -1.0

  #    angle = np.arccos(normalized_dot_product)
  #    angle_in_degrees = 180. * angle / np.pi

  #    # http://www.opengl.org/discussion_boards/showthread.php/159385-Deriving-angles-from-0-to-360-from-Dot-Product
  #    C = np.cross(reference_vector, comparison_vector)
  #    direction = np.dot(C, vertex)
  #    if direction < 0.:  angle_in_degrees = -1 * angle_in_degrees

  #    print '\t\t' + str(spoke) + '\t' +  str(angle_in_degrees)
