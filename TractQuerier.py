from __main__ import vtk, qt, ctk, slicer
import unittest
from itertools import izip
from vtk.util import numpy_support as ns
import numpy as np

#
# global variables 
#
tractography_file_name='C:\\Users\\Georgios\\workspace\\tract_querier\\OutputFiberBundle.vtk'
atlas_file_name='C:\\Users\\Georgios\\workspace\\tract_querier\\parc.nii.gz'
queries_string='C:\\Users\Georgios\\workspace\\tract_querier\\queries\\wmql_1_cst.qry'

#
# TractQuerier
#
class TractQuerier:
  def __init__(self, parent):
    parent.title = "Tract Querier"
    parent.categories = ["Examples"]
    parent.dependencies = []
    parent.contributors = ["Lichen Liang (MGH)",
                           "Steve Pieper (Isomics)"
                           ] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    TractQurier
    """
    parent.acknowledgementText = """
    This file was originally developed by ....""" # replace with organization, grant and thanks.
    self.parent = parent

#
# TractQuerierWidget
#

class TractQuerierWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Collapsible button
    self.queryCollapsibleButton = ctk.ctkCollapsibleButton()
    self.queryCollapsibleButton.text = "query Operator"
    self.layout.addWidget(self.queryCollapsibleButton)

    # Layout within the collapsible button
    self.queryFormLayout = qt.QFormLayout(self.queryCollapsibleButton)

    # the volume selectors
    self.inputFrame = qt.QFrame(self.queryCollapsibleButton)
    self.inputFrame.setLayout(qt.QHBoxLayout())
    self.queryFormLayout.addWidget(self.inputFrame)
    self.inputSelector = qt.QLabel("Input Fiber Bundle: ", self.inputFrame)
    self.inputFrame.layout().addWidget(self.inputSelector)
    self.fiberSelector = slicer.qMRMLNodeComboBox(self.inputFrame)
    self.fiberSelector.nodeTypes = ( ("vtkMRMLFiberBundleNode"), "" )
    self.fiberSelector.addEnabled = False
    self.fiberSelector.removeEnabled = False
    self.fiberSelector.setMRMLScene( slicer.mrmlScene )
    self.inputFrame.layout().addWidget(self.fiberSelector)

    self.outputFrame = qt.QFrame(self.queryCollapsibleButton)
    self.outputFrame.setLayout(qt.QHBoxLayout())
    self.queryFormLayout.addWidget(self.outputFrame)
    self.outputSelector = qt.QLabel("Parc Volume: ", self.outputFrame)
    self.outputFrame.layout().addWidget(self.outputSelector)
    self.labelSelector = slicer.qMRMLNodeComboBox(self.outputFrame)
    self.labelSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.labelSelector.setMRMLScene( slicer.mrmlScene )
    self.outputFrame.layout().addWidget(self.labelSelector)

    self.queryFrame = qt.QFrame(self.queryCollapsibleButton)
    self.queryFrame.setLayout(qt.QHBoxLayout())
    self.queryFormLayout.addWidget(self.queryFrame)
    self.querySelector = qt.QLabel("Query Fiber Bundle: ", self.queryFrame)
    self.queryFrame.layout().addWidget(self.querySelector)
    self.fiberQuerySelector = slicer.qMRMLNodeComboBox(self.queryFrame)
    self.fiberQuerySelector.nodeTypes = ( ("vtkMRMLFiberBundleNode"), "" )
    #self.fiberQuerySelector.addEnabled = False
    #self.fiberQuerySelector.removeEnabled = False
    self.fiberQuerySelector.setMRMLScene( slicer.mrmlScene )
    self.queryFrame.layout().addWidget(self.fiberQuerySelector)


    # Apply button
    queryButton = qt.QPushButton("Apply Tract Query")
    queryButton.toolTip = "Run the query."
    self.queryFormLayout.addWidget(queryButton)
    queryButton.connect('clicked(bool)', self.onApply)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.queryButton = queryButton
    
  def onApply(self):
    print "Hello World !"
    fiberNode = self.fiberSelector.currentNode()
    labelNode = self.labelSelector.currentNode()
    if not fiberNode and not labelNode:
       qt.QMessageBox.critical(slicer.util.mainWindow(), 'FiberBundleToLabelMap', "Must select fiber bundle and label map")
       return
   # query_script=file('\\Users\\Georgios\\workspace\\tract_querier\\queries\\FreeSurfer.qry').read()
   # fiber_path='\\Users\\Georgios\\workspace\\tract_querier\\OutputFiberBundle.vtk'
   # slicer.util.loadFiberBundle(fiber_path)
   # fiberNode=slicer.util.getNode(pattern="OutputFiberBundle")
   # parc_path='\\Users\\Georgios\\workspace\\tract_querier\\parc.nii.gz'
   # slicer.util.loadVolume(parc_path)
   # parcNode=slicer.util.getNode(pattern="parc")
    run(fiberNode, labelNode)

from optparse import OptionParser
import os
import sys

def run(fiberNode,parcNode):
    parser = OptionParser(
        version=0.1,
        usage="usage: %prog -t tractography_file -a atlas_file "
        "-q queries -o result_prefix"
    )
    (options, args) = parser.parse_args()

    options.tractography_file_name=tractography_file_name
    options.atlas_file_name=atlas_file_name
    options.queries_string=queries_string
    options.output_file_name='output'
    options.bounding_box_affine_transform=None
    #options.include='C:\\Users\\Georgios\\workspace\\tract_querier'
    options.length_threshold=2
    options.threshold=0
    options.interactive=False
    options.query_selection=''
    if (
        not options.tractography_file_name or
        not options.atlas_file_name or
        not options.queries_string or
        not options.output_file_name
    ):
        parser.error("incorrect number of arguments")

    global np
    global tract_querier

    import numpy as np
    import nibabel

    import tract_querier

    if options.bounding_box_affine_transform:
        bounding_box_affine_transform = np.fromstring(
            options.bounding_box_affine_transform, sep=','
        ).reshape(4, 4)
        print "RAS transform:"
    else:
        bounding_box_affine_transform = np.eye(4)

    print "Loading files"
#    if options.include:
#        folders = [options.include]
#    else:
    folders = []

    default_folder = tract_querier.default_queries_folder
    folders = [os.getcwd()] + folders + [default_folder]
    print folders
    for folder in folders:
        if not (os.path.exists(folder) and os.path.isdir(folder)):
            parser.error("Error in include folder %s" % folder)

    try:
        if os.path.exists(options.queries_string):
            query_script = file(options.queries_string).read()
            query_filename = options.queries_string
        else:
            found = False
            for folder in folders:
                file_ = os.path.join(folder, options.queries_string)
                if os.path.exists(file_):
                    found = True
                    break
            if found:
                query_script = file(file_).read()
                query_filename = file_
            else:
                query_script = options.queries_string
                query_filename = '<script>'

        query_file_body = tract_querier.queries_preprocess(
            query_script,
            filename=query_filename,
            include_folders=folders
        )

        tract_querier.queries_syntax_check(query_file_body)
    except tract_querier.TractQuerierSyntaxError, e:
        parser.error(e.value)

    labels_nii = nibabel.load(options.atlas_file_name)
    img = labels_nii.get_data()
    
    #
    #  covert slicer polydata to tract
    #
    polyData = fiberNode.GetPolyData()
    tr = tract_querier.tractography.vtkInterface.vtkPolyData_to_tracts(polyData)
    print 'tract-to-polydata'
    
    #
    #  run tract-querier
    #
    tractography_extension = os.path.splitext(options.tractography_file_name)[-1]
    if tractography_extension == '.trk':
        tractography_extra_kwargs = {
            'affine': tr.affine,
            'image_dimensions': tr.image_dims
        }

    else:
        tractography_extra_kwargs = {}

    print "Calculating labels and crossings"
    affine_ijk_2_ras = labels_nii.get_affine()
    tracts = tr.tracts()
    
    tractography_spatial_indexing = tract_querier.TractographySpatialIndexing(
        tracts, img, affine_ijk_2_ras, options.length_threshold, options.threshold
    )
    
    print "Computing queries"
    evaluated_queries = tract_querier.eval_queries(
        query_file_body,
        tractography_spatial_indexing,
    )

    query_names = evaluated_queries.keys()
    print query_names
    if options.query_selection != '':
        selected_queries = set(options.query_selection.lower().split(','))
        query_names = list(set(query_names) & set(selected_queries))

    query_names.sort()
    print 'save_query'
    for query_name in query_names:
        tr_out=save_query(
            query_name, tr, options, evaluated_queries,
            extension=tractography_extension, extra_kwargs=tractography_extra_kwargs
        )

    #
    #   covert resulting tract to polydata 
    # 
    polyDataOut=tracts_to_vtkPolyData64(tr_out)
    print 'update polydata'
    updateOutputNode(polyDataOut)
    return   
     
def save_query(query_name, tractography, options, evaluated_queries, extension='.vtk', extra_kwargs={}):
    tract_numbers = evaluated_queries[query_name]
    print "\tQuery %s: %.6d" % (query_name, len(tract_numbers))
    if tract_numbers:
        tr=save_tractography_file(
            options.output_file_name + "_" + query_name + extension,
            tractography,
            tract_numbers,
            extra_kwargs=extra_kwargs
        )
    return tr

def save_tractography_file(filename, tractography, tract_numbers, extra_kwargs={}):
    print 'start save tractography file'
    tract_numbers = list(tract_numbers)

    original_tracts = tractography.original_tracts()
    print tract_numbers
    tracts_to_save = [original_tracts[i] for i in tract_numbers]

    if len(tracts_to_save) == 0:
        return
    
    tracts_data_to_save = {}
    print 'extract key-data'
    for key, data in tractography.original_tracts_data().items():
        tracts_data_to_save[key] = [data[f] for f in tract_numbers]

    if (
        'ActiveTensors' not in tracts_data_to_save and
        'Tensors_' in tracts_data_to_save
    ):
        tracts_data_to_save['ActiveTensors'] = 'Tensors_'
    if (
        'ActiveVectors' not in tracts_data_to_save and
        'Vectors_' in tracts_data_to_save
    ):
        tracts_data_to_save['ActiveVectors'] = 'Vectors_'

    print "tractography.tractorgrapy_to_file"
    
    tr=tract_querier.tractography.Tractography(
            tracts_to_save,
            tracts_data_to_save
        )
    
    return tr

def tracts_to_vtkPolyData64(tracts, tracts_data={}, lines_indices=None):
  #  if isinstance(tracts, Tractography):
    tracts_data = tracts.tracts_data()
    tracts = tracts.tracts()
    lengths = [len(p) for p in tracts]
    line_starts = ns.numpy.r_[0, ns.numpy.cumsum(lengths)]
    if lines_indices is None:
        lines_indices = [
            ns.numpy.arange(length) + line_start
            for length, line_start in izip(lengths, line_starts)
        ]

    ids = ns.numpy.hstack([
        ns.numpy.r_[c[0], c[1]]
        for c in izip(lengths, lines_indices)
    ])
    ids=np.int64(ids)
    vtk_ids = ns.numpy_to_vtkIdTypeArray(ids, deep=True)

    cell_array = vtk.vtkCellArray()
    cell_array.SetCells(len(tracts), vtk_ids)
    points = ns.numpy.vstack(tracts).astype(
        ns.get_vtk_to_numpy_typemap()[vtk.VTK_DOUBLE]
    )
    points_array = ns.numpy_to_vtk(points, deep=True)

    poly_data = vtk.vtkPolyData()
    vtk_points = vtk.vtkPoints()
    vtk_points.SetData(points_array)
    poly_data.SetPoints(vtk_points)
    poly_data.SetLines(cell_array)

    saved_keys = set()
    for key, value in tracts_data.items():
        if key in saved_keys:
            continue
        if key.startswith('Active'):
            saved_keys.add(value)
            name = value
            value = tracts_data[value]
        else:
            name = key

        if len(value) == len(tracts):
            if value[0].ndim == 1:
                value_ = ns.numpy.hstack(value)[:, None]
            else:
                value_ = ns.numpy.vstack(value)
        elif len(value) == len(points):
            value_ = value
        else:
            raise ValueError(
                "Data in %s does not have the correct number of items")

        vtk_value = ns.numpy_to_vtk(np.ascontiguousarray(value_), deep=True)
        vtk_value.SetName(name)
        if key == 'ActiveScalars' or key == 'Scalars_':
            poly_data.GetPointData().SetScalars(vtk_value)
        elif key == 'ActiveVectors' or key == 'Vectors_':
            poly_data.GetPointData().SetVectors(vtk_value)
        elif key == 'ActiveTensors' or key == 'Tensors_':
            poly_data.GetPointData().SetTensors(vtk_value)
        else:
            poly_data.GetPointData().AddArray(vtk_value)

    poly_data.BuildCells()

    return poly_data

def updateOutputNode(polydata):
    # clear scene
    scene=slicer.mrmlScene
    scene.Clear(0)
    
    # create fiber node
    fiber=slicer.vtkMRMLModelNode()
    fiber.SetScene(scene)
    fiber.SetName("QueryTract")
    fiber.SetAndObservePolyData(polydata)
    
    # create display model fiber node
    fiberDisplay=slicer.vtkMRMLModelDisplayNode()
    fiberDisplay.SetScene(scene)
    scene.AddNode(fiberDisplay)
    fiber.SetAndObserveDisplayNodeID(fiberDisplay.GetID())
    
    # add to scene
    fiberDisplay.SetInputPolyData(polydata)
    scene.AddNode(fiber)
    