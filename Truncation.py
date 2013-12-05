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

def truncate(V_sphere, C_sphere, cutoff_from_bottom):

  #
  # figure out the range between top and bottom of the sphere
  #
  min_vy = 1.
  max_vy = -1.
  for idx, v in enumerate(V_sphere):
      if v[2] > max_vy:  max_vy = v[2]
      if v[2] < min_vy:  min_vy = v[2]
  v_range = abs(max_vy - min_vy)
  cutoff = min_vy + cutoff_from_bottom * v_range

  #
  # find chords to remove or modify
  #
  V_new = list(V_sphere)
  chords_to_remove = []
  chords_to_add = []
  vertices_to_remove = []
  for c_idx, c in enumerate(C_sphere):
    v1_idx = c[0] - 1
    v2_idx = c[1] - 1
    v1 = V_sphere[v1_idx]
    v2 = V_sphere[v2_idx]
    
    # both vertices below cutoff
    if v1[2] < cutoff and v2[2] < cutoff:
      chords_to_remove.append(c_idx)
      vertices_to_remove.append(v1_idx)
      vertices_to_remove.append(v2_idx)

    # vertex 1 below cutoff
    if v1[2] < cutoff and v2[2] >= cutoff:
      chords_to_remove.append(c_idx)
      norm = np.linalg.linalg.norm(v1 - v2)
      norm_vec = (v1 - v2) / norm
      scalar = (cutoff - v2[2]) / norm_vec[2]
      V_new.append(v2 + scalar * norm_vec)
      chords_to_add.append([c[1], len(V_new)])

    # vertex 2 below cutoff
    if v2[2] < cutoff and v1[2] >= cutoff:
      chords_to_remove.append(c_idx)
      norm = np.linalg.linalg.norm(v2 - v1)
      norm_vec = (v2 - v1) / norm
      scalar = (cutoff - v1[2]) / norm_vec[2]
      V_new.append(v1 + scalar * norm_vec)
      chords_to_add.append([c[0], len(V_new)])

  #
  # consolidate chords
  #
  C_next = []
  for c_idx, c in enumerate(C_sphere):
    if chords_to_remove.count(c_idx) == 0:
      C_next.append(c)
  for c in chords_to_add:
    C_next.append(c)

  #
  # re-number nodes, getting ride of unused ones
  #
  old_vidx_2_new_v = {}
  V_final = []
  for c_idx, c in enumerate(C_next):
    vertex_1_idx = c[0] - 1
    vertex_2_idx = c[1] - 1

    if not old_vidx_2_new_v.has_key(vertex_1_idx):
      V_final.append(V_new[vertex_1_idx])
      old_vidx_2_new_v[vertex_1_idx] = len(V_final)

    if not old_vidx_2_new_v.has_key(vertex_2_idx):
      V_final.append(V_new[vertex_2_idx])
      old_vidx_2_new_v[vertex_2_idx] = len(V_final)

  C_final = []
  for c_idx, c in enumerate(C_next):
    vertex_1_idx = c[0] - 1
    vertex_2_idx = c[1] - 1
    C_final.append([old_vidx_2_new_v[vertex_1_idx], old_vidx_2_new_v[vertex_2_idx]])

  return V_final, C_final
