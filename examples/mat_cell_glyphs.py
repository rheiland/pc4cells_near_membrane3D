# https://kitware.github.io/vtk-examples/site/Python/Filtering/Glyph3D/
#!/usr/bin/env python

# noinspection PyUnresolvedReferences
# import vtkmodules.vtkInteractionStyle
# import vtkmodules.vtkRenderingOpenGL2
import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from vtk import *

from pyMCDS_cells import pyMCDS_cells
#from vtk.util import numpy_support
import numpy as np
# from numpy import genfromtxt
import random


def reset_model():
    print("\n--------- vis_tab: reset_model ----------")
    # Verify initial.xml and at least one .svg file exist. Obtain bounds from initial.xml
    # tree = ET.parse(output_dir + "/" + "initial.xml")
    output_dir = "."
    xml_file = Path(output_dir, "initial.xml")
    if not os.path.isfile(xml_file):
        print("vis_tab: Warning: Expecting initial.xml, but does not exist.")
        # msgBox = QMessageBox()
        # msgBox.setIcon(QMessageBox.Information)
        # msgBox.setText("Did not find 'initial.xml' in the output directory. Will plot a dummy substrate until you run a simulation.")
        # msgBox.setStandardButtons(QMessageBox.Ok)
        # msgBox.exec()
        return

    tree = ET.parse(Path(output_dir, "initial.xml"))
    xml_root = tree.getroot()

    bds_str = xml_root.find(".//microenvironment//domain//mesh//bounding_box").text
    bds = bds_str.split()
    print('bds=',bds)
    xmin = float(bds[0])
    xmax = float(bds[3])
    print('reset_model(): xmin, xmax=',xmin, xmax)
    x_range = xmax - xmin
    plot_xmin = xmin
    plot_xmax = xmax

    # try:
    #     my_xmin.setText(str(plot_xmin))
    #     my_xmax.setText(str(plot_xmax))
    #     my_ymin.setText(str(plot_ymin))
    #     my_ymax.setText(str(plot_ymax))
    # except:
    #     pass

    ymin = float(bds[1])
    ymax = float(bds[4])
    y_range = ymax - ymin
    plot_ymin = ymin
    plot_ymax = ymax

    xcoords_str = xml_root.find(".//microenvironment//domain//mesh//x_coordinates").text
    xcoords = xcoords_str.split()
    print('reset_model(): xcoords=',xcoords)
    print('reset_model(): len(xcoords)=',len(xcoords))
    numx =  len(xcoords)
    numy =  len(xcoords)
    print("reset_model(): numx, numy = ",numx,numy)

    #-------------------
    vars_uep = xml_root.find(".//microenvironment//domain//variables")
    if vars_uep:
        sub_names = []
        for var in vars_uep:
        # substrate.clear()
        # param[substrate_name] = {}  # a dict of dicts

        # tree.clear()
            idx = 0
        # <microenvironment_setup>
        #   <variable name="food" units="dimensionless" ID="0">
            # print(cell_def.attrib['name'])
            if var.tag == 'variable':
                substrate_name = var.attrib['name']
                print("substrate: ",substrate_name )
                sub_names.append(substrate_name)
            # substrates_cbox.clear()
            print("sub_names = ",sub_names)
            # substrates_cbox.addItems(sub_names)


    # and plot 1st frame (.svg)
    # current_svg_frame = 0


#xml_file = sys.argv[1]
frame = int(sys.argv[1])
reset_model()

# print("plot_cells3D:  output_dir= ",output_dir)
print("plot_cells3D:  frame= ",frame)
# xml_file = Path(output_dir, "output00000000.xml")
# xml_file = "output00000000.xml"
xml_file = "output%08d.xml" % frame
print("plot_cells3D: xml_file = ",xml_file)

if not os.path.isfile(xml_file):
    print("plot_cells3D(): file not found, return. ", xml_file)
    sys.exit()

# iren.ReInitialize()
# iren.GetRenderWindow().Render()

mcds = pyMCDS_cells(xml_file, '.')  
# mcds = pyMCDS_cells(xml_file, 'tmpdir')  
print('time=', mcds.get_time())

print(mcds.data['discrete_cells'].keys())

ncells = len(mcds.data['discrete_cells']['ID'])
# print('total_volume= ',mcds.data['discrete_cells']['total_volume'])
print()
print('total_volume= ',mcds.data['discrete_cells']['total_volume'][0:10])
print('ncells=', ncells)

# global xyz
xyz = np.zeros((ncells, 3))
xyz[:, 0] = mcds.data['discrete_cells']['position_x']
xyz[:, 1] = mcds.data['discrete_cells']['position_y']
xyz[:, 2] = mcds.data['discrete_cells']['position_z']
#xyz = xyz[:1000]
# print("position_x = ",xyz[:,0])
xmin = min(xyz[:,0])
xmax = max(xyz[:,0])
print("xmin = ",xmin)
print("xmax = ",xmax)

ymin = min(xyz[:,1])
ymax = max(xyz[:,1])
print("ymin = ",ymin)
print("ymax = ",ymax)

zmin = min(xyz[:,2])
zmax = max(xyz[:,2])
print("zmin = ",zmin)
print("zmax = ",zmax)

# cell_type = mcds.data['discrete_cells']['cell_type']
cell_custom_ID = mcds.data['discrete_cells']['cell_ID']
# # print(type(cell_type))
# # print(cell_type)
# unique_cell_type = np.unique(cell_type)
unique_cell_custom_ID = np.unique(cell_custom_ID)
# print("\nunique_cell_type = ",unique_cell_type )
# print("\nunique_cell_custom_ID = ",unique_cell_custom_ID )

#------------
colors = vtkNamedColors()

points = vtkPoints()
# points.Reset()
cellID = vtkFloatArray()
# cellID.Reset()
cellVolume = vtkFloatArray()
# cellVolume.Reset()
for idx in range(ncells):
    x= mcds.data['discrete_cells']['position_x'][idx]
    y= mcds.data['discrete_cells']['position_y'][idx]
    z= mcds.data['discrete_cells']['position_z'][idx]
    # id = mcds.data['discrete_cells']['cell_type'][idx]
    id = mcds.data['discrete_cells']['cell_ID'][idx]
    points.InsertNextPoint(x, y, z)
    # cellVolume.InsertNextValue(30.0)
    cellID.InsertNextValue(id)

print("min (parent, custom var) cell_ID = ",min(mcds.data['discrete_cells']['cell_ID']))
print("max (parent, custom var) cell_ID = ",max(mcds.data['discrete_cells']['cell_ID']))

polydata = vtkPolyData()
polydata.SetPoints(points)
# polydata.GetPointData().SetScalars(cellVolume)
polydata.GetPointData().SetScalars(cellID)

cellID_color_dict = {}
random.seed(42)
for utype in unique_cell_custom_ID:
    cellID_color_dict[utype] = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
cellID_color_dict[0.]=[255,255,0]  # yellow basement membrane
print("color dict=",cellID_color_dict)

colors = vtkUnsignedCharArray()
colors.Reset()
colors.SetNumberOfComponents(3)
colors.SetNumberOfTuples(polydata.GetNumberOfPoints())  # ncells
for idx in range(ncells):
    colors.InsertTuple3(idx, cellID_color_dict[cell_custom_ID[idx]][0], cellID_color_dict[cell_custom_ID[idx]][1], cellID_color_dict[cell_custom_ID[idx]][2])

polydata.GetPointData().SetScalars(colors)

nres = 20
sphereSource = vtkSphereSource()
sphereSource.SetPhiResolution(nres)
sphereSource.SetThetaResolution(nres)
sphereSource.SetRadius(8.412)  # rwh ??

glyph = vtkGlyph3D()
glyph.SetSourceConnection(sphereSource.GetOutputPort())
glyph.SetInputData(polydata)
glyph.SetColorModeToColorByScalar()
# glyph.SetScaleModeToScaleByScalar()

# using these 2 results in fixed size spheres
glyph.SetScaleModeToDataScalingOff()  # results in super tiny spheres without 'ScaleFactor'
# glyph.SetScaleFactor(170)  # overall (multiplicative) scaling factor

# glyph.SetScaleModeToDataScalingOn()
# glyph.ScalingOn()
glyph.Update()

# Visualize
cells_mapper = vtkPolyDataMapper()
cells_mapper.SetInputConnection(glyph.GetOutputPort())
cells_mapper.Update()

cells_actor = vtkActor()
cells_actor.SetMapper(cells_mapper)


ren = vtkRenderer()

ren.AddActor(cells_actor)

renderWindow = vtkRenderWindow()
renderWindow.SetPosition(100,100)
renderWindow.SetSize(1400,1200)
renderWindow.AddRenderer(ren)

    # renderWindowInteractor = vtkRenderWindowInteractor()
    # renderWindowInteractor.SetRenderWindow(renderWindow)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)

iren.GetRenderWindow().Render()

ren.GetActiveCamera().ParallelProjectionOn()


# renderWindow.SetWindowName('PhysiCell')
# renderWindow.Render()
iren.Start()
