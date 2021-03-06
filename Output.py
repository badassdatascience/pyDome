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



def OutputDXF(V, C, the_filename):
  outfile = open(the_filename, 'w')
  outfile.write('0\n')
  outfile.write('SECTION\n')
  outfile.write('2\n')
  outfile.write('ENTITIES\n')

  for n in C:
    outfile.write('0\n')
    outfile.write('LINE\n')
    outfile.write('8\n')
    outfile.write('1\n')
    outfile.write('62\n')
    outfile.write('3\n')
    outfile.write('10\n')
    outfile.write(str(V[n[0]-1][0]) + '\n')
    outfile.write('20\n')
    outfile.write(str(V[n[0]-1][2]) + '\n')
    outfile.write('30\n')
    outfile.write(str(V[n[0]-1][1]) + '\n')
    outfile.write('11\n')
    outfile.write(str(V[n[1]-1][0]) + '\n')
    outfile.write('21\n')
    outfile.write(str(V[n[1]-1][2]) + '\n')
    outfile.write('31\n')
    outfile.write(str(V[n[1]-1][1]) + '\n')

  outfile.write('0\n')
  outfile.write('ENDSEC\n')
  outfile.write('0\n')
  outfile.write('EOF\n')
  outfile.close()

def OutputWireframeVRML(V, C, the_filename):
  outfile = open(the_filename, 'w')
  outfile.write("#VRML V2.0 utf8\n")
  outfile.write("\n")
  outfile.write("#WRL File Generated by pyDome:\n")
  outfile.write("\n")
  outfile.write("Shape {\n")
  outfile.write("    appearance Appearance {\n")

  outfile.write('material Material {\n')
  #outfile.write('diffuseColor 0 0 1\n')
  outfile.write('emissiveColor 0.80000001 0.80000001 0.80000001\n')
  outfile.write('}\n')

  outfile.write("   }\n")
  outfile.write("   geometry IndexedLineSet {\n")
  outfile.write("        coord Coordinate {\n")
  outfile.write("     point [\n");
  for v in V:
    outfile.write(''.join([str(v[0]), " ", str(v[1]), " ", str(v[2]), ","]) + '\n')
  outfile.write("     ]")
  outfile.write("          }")
  outfile.write("       coordIndex [")
  for c in C:
    outfile.write(''.join([str(c[0]-1), " ", str(c[1]-1), " -1,"]) + '\n')
  outfile.write("               ]")
  outfile.write("          }" )
  outfile.write("     }" )
  outfile.close()

def OutputFaceVRML(V, F, the_filename):
  outfile = open(the_filename, 'w')
  outfile.write("#VRML V2.0 utf8\n")
  outfile.write("\n")
  outfile.write("#WRL File Generated by pyDome:\n")
  outfile.write("\n")
  outfile.write("Shape {\n")
  outfile.write("    appearance Appearance {\n")
  outfile.write('material Material {\n')
  outfile.write('diffuseColor 0.776 0.886 1\n')
  outfile.write('}\n')


  outfile.write("   }\n")
  outfile.write("   geometry IndexedFaceSet {\n")
  outfile.write("        coord Coordinate {\n")
  outfile.write("     point [\n");
  for v in V:
    outfile.write(''.join([str(v[0]), " ", str(v[1]), " ", str(v[2]), ","]) + '\n')
  outfile.write("     ]")
  outfile.write("          }")
  outfile.write("       coordIndex [")
  for f in F:
    outfile.write(''.join([str(f[0]-1), ", ", str(f[1]-1), ", ", str(f[2]-1), ", -1,"]) + '\n')
  outfile.write("               ]")
  outfile.write("          }" )
  outfile.write("     }" )
  outfile.close()
