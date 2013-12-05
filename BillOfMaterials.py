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
