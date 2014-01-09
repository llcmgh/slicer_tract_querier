=====================================================================
Name: 		TrackQuerier Module for Slicer 4
Creator:	.... 
Date:		01.06.2014
Version:	b1.0
Language:	Python
Platforms:	Slicer 4 (Windows, Mac OS X, Linux)
=====================================================================

This Module allows users to query fiber tracks with White Matter Query Language (WMQL) 
introduced by Demain Wasssermann et. al. in MICCAI 2013. 
 

1) Download and Install Slicer			http://download.slicer.org/


2) Download and Install Numpy 1.7

Note: Numpy 1.4.1 comes with Slicer4, but our module requires Numpy 1.7. 
Download numpy 1.7. 
http://sourceforge.net/projects/numpy/files/NumPy/1.7.1/numpy-1.7.1.tar.gz
  >tar xvzf numpy-1.7.1.tar.gz 
  >cd numpy-1.7.1 
  >Slicer-SuperBuild/python-install/bin/python setup.py install 


3) Download TractQuerier Module 

  >git clone https://github.com/llcmgh/slicer_tract_querier.git

  It will create a directory called slicer_tract_querier


4) Load TractQuerier module into Slicer
 
	Slicer -> Edit -> Application Settings -> Modules -> 
	Additional module paths ->
	Add slicer_tract_querier to the path
	
	Restart Slicer after adding the path
	
----------

Usage of the module :
(1) A tractography in VTK format: It must be a vtkPolyData object where all the cells are lines.
(2) A brain parcellation, obtained from freesurfer in the same space as the full-brain tractography.
(3) A WMQL query script typed in the EditBox

----------
