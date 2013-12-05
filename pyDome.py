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



#
# load useful modules
#
import numpy as np
import getopt
import sys

#
# load pyDome modules
#
from Polyhedral import *
from SymmetryTriangle import *
from GeodesicSphere import *
from Output import *
from Truncation import *
from BillOfMaterials import *


def display_help():
  print
  print 'pyDome:  A geodesic dome calculator. Copyright 2013 by Daniel Williams'
  print
  print 'Required Command-Line Input:'
  print
  print '\t-o, --output=\tPath to output file(s). Extensions will be added. Generates DXF and WRL files by default, but only WRL file when "-F" option is active. Example:  \"-o output/test\" produces files output/test.wrl and output/test.dxf.'
  print
  print 'Options:'
  print
  print '\t-r, --radius\tRadius of generated dome. Must be floating point. Default 1.0.'
  print
  print '\t-f, --frequency\tFrequency of generated dome. Must be an integer. Default 4.'
  print
  print '\t-v, --vthreshold\tDistance required to consider two vertices equal. Default 0.0000001. Must be floating point.'
  print
  print '\t-t, --truncation\tDistance (ratio) from the bottom to truncate. Default 0.499999. I advise using only the default or 0.333333. Must be floating point.'
  print
  print '\t-b, --bom-rounding\tThe number of decimal places to round chord length output in the generated Bill of Materials. Default 5. Must be an integer.'
  print
  print '\t-p, --polyhedron\tEither \"octahedron\" or \"icosahedron\". Default icosahedron.'
  print
  print '\t-F, --face\tFlag specifying whether to generate face output in WRL file. Cancels DXF file output and cannot be used with truncation.'
  print

def main():

  #
  # default values
  #
  radius = np.float64(1.)
  frequency = 4
  polyhedral = Icosahedron()
  vertex_equal_threshold = 0.0000001
  truncation_amount = 0.499999
  run_truncate = False
  bom_rounding_precision = 5
  face_output = False
  output_path = None

  #
  # no input arguments
  #
  if len(sys.argv[1:]) == 0:
    display_help()
    sys.exit(-1)

  #
  # parse command line
  #
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'r:f:v:t:b:p:Fo:', ['truncation=', 'vthreshold=', 'radius=', 'frequency=', 'help', 'bom-rounding=', 'polyhedron=', 'face', 'output='])
  except getopt.error, msg:
    print "for help use --help"
    sys.exit(-1)
  for o, a in opts:
    if o in ('-o', '--output'):
      output_path = a
    if o in ('-p', '--polyhedron'):
      if a == 'octahedron':
        polyhedral = Octahedron()
    if o in ('-b', '--bom-rounding'):
      try:
        bom_rounding_precision = int(a)
      except:
        print '-b or --bom-rounding argument must be an integer. Exiting.'
        sys.exit(-1)
    if o in ('-h', '--help'):
      display_help()
      sys.exit(0)
    if o in ('-F', '--face'):
      face_output = True
    if o in ('-r', '--radius'):
      try:
        a = float(a)
        radius = np.float64(a)
      except:
        print '-r or --radius argument must be a floating point number. Exiting.'
        sys.exit(-1)
    if o in ('-f', '--frequency'):
      try:
        frequency = int(a)
      except:
        print '-f or --frequency argument must be an integer. Exiting.'
        sys.exit(-1)
    if o in ('-v', '--vthreshold'):
      try:
        a = float(a)
        vertex_equal_threshold = np.float64(a)
      except:
        print '-v or --vthreshold argument must be a floating point number. Exiting.'
        sys.exit(-1)
    if o in ('-t', '--truncation'):
      try:
        a = float(a)
        truncation_amount = np.float64(a)
        run_truncate = True
      except:
        print '-t or --truncation argument must be a floating point number. Exiting.'
        sys.exit(-1)

  #
  # check for required options
  #
  if output_path == None:
    print 'An output path and filename is required. Use the -o argument. Exiting.'
    sys.exit(-1)

  #
  # check for mutually exclusive options
  #
  if face_output and run_truncate:
    print 'Truncation does not work with face output at this time. Use either -t or -F but not both.'
    exit(-1)

  #
  # generate geodesic sphere
  #
  symmetry_triangle = ClassOneMethodOneSymmetryTriangle(frequency, polyhedral)
  sphere = GeodesicSphere(polyhedral, symmetry_triangle, vertex_equal_threshold, radius)
  C_sphere = sphere.non_duplicate_chords
  F_sphere = sphere.non_duplicate_face_nodes
  V_sphere = sphere.sphere_vertices

  #
  # truncate
  #
  V = V_sphere
  C = C_sphere
  if run_truncate:
    V, C = truncate(V_sphere, C_sphere, truncation_amount)

  #
  # write model output
  #
  if face_output:
    OutputFaceVRML(V, F_sphere, output_path + '.wrl')
  else:
    OutputWireframeVRML(V, C, output_path + '.wrl')
    OutputDXF(V, C, output_path + '.dxf')

  #
  # bill of materials
  #
  get_bill_of_materials(V, C, bom_rounding_precision)

#
# run the main function
#
if __name__ == "__main__":
  main()
