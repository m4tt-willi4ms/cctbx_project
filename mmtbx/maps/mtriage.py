from __future__ import division
import sys
from libtbx import group_args
from cctbx import maptbx
import iotbx.phil
from libtbx import adopt_init_args
from cctbx.maptbx import resolution_from_map_and_model
import mmtbx.utils

master_params_str = """
  map_file_name = None
    .type = str
    .help = Map file name
  model_file_name = None
    .type = str
    .help = Model file name
  resolution = None
    .type = float
    .help = Data (map) resolution
  scattering_table = wk1995  it1992  *n_gaussian  neutron electron
    .type = choice
    .help = Scattering table (X-ray, neutron or electron)
  atom_radius = None
    .type = float
    .help = Atom radius for masking. If undefined then calculated automatically
"""

def master_params():
  return iotbx.phil.parse(master_params_str, process_includes=False)

def get_box(map_data, pdb_hierarchy, xray_structure):
  box = mmtbx.utils.extract_box_around_model_and_map(
    xray_structure         = xray_structure,
    map_data               = map_data,
    box_cushion            = 5.0,
    selection              = None,
    density_select         = None,
    threshold              = None)
  pdb_hierarchy.adopt_xray_structure(box.xray_structure_box)
  return group_args(
    map_data       = box.map_box,
    xray_structure = box.xray_structure_box,
    pdb_hierarchy  = pdb_hierarchy)

class run(object):
  def __init__(self,
               map_data,
               crystal_symmetry,
               params=master_params(),
               half_map_data_1=None,
               half_map_data_2=None,
               pdb_hierarchy=None,
               nproc=1):
    # XXX assert len(locals().keys()) == 4 # intentional
    assert [half_map_data_1, half_map_data_2].count(None) in [0,2]
    #adopt_init_args(self, locals())
    # Get xray.structure
    xray_structure = None
    if(pdb_hierarchy is not None):
      pdb_hierarchy.atoms().reset_i_seq()
      xray_structure = pdb_hierarchy.extract_xray_structure(
        crystal_symmetry = crystal_symmetry)
    # Compute d99
    d99_obj = maptbx.d99(map=map_data, crystal_symmetry=crystal_symmetry)
    d99_half1_obj, d99_half2_obj = None,None
    if(half_map_data_1 is not None):
      d99_half1_obj = maptbx.d99(
        map=half_map_data_1, crystal_symmetry=crystal_symmetry)
      d99_half2_obj = maptbx.d99(
        map=half_map_data_2, crystal_symmetry=crystal_symmetry)
    # Compute d_model
    d_model = None
    if(pdb_hierarchy is not None):
      xray_structure = pdb_hierarchy.extract_xray_structure(
        crystal_symmetry = crystal_symmetry)
      box = get_box(
        map_data       = map_data,
        pdb_hierarchy  = pdb_hierarchy,
        xray_structure = xray_structure)
      d_model_obj = resolution_from_map_and_model.run(
        map_data         = box.map_data,
        xray_structure   = box.xray_structure.deep_copy_scatterers(),
        pdb_hierarchy    = box.pdb_hierarchy,
        d_min_min        = 1.7,
        nproc            = nproc)
    # Compute half-map FSC
    fsc_obj = d99_half1_obj.f.d_min_from_fsc(
      other=d99_half2_obj.f, bin_width=1000, fsc_cutoff=0.143)
    # XXX
    of = open("zz","w")
    for a,b in zip(fsc_obj.fsc.d_inv, fsc_obj.fsc.fsc):
      print >>of, "%15.9f %15.9f"%(a,b)
    of.close()
    # XXX
    # Map-model FSC and d_fsc_model
    if(pdb_hierarchy is not None):
      f_calc = d99_obj.f.structure_factors_from_scatterers(
        xray_structure = xray_structure).f_calc()
      fsc_map_model_obj = f_calc.d_min_from_fsc(
        other=d99_obj.f, bin_width=1000, fsc_cutoff=0.0)
      d_fsc_model = fsc_map_model_obj.d_min
      # XXX
      of = open("xx","w")
      for a,b in zip(fsc_map_model_obj.fsc.d_inv, fsc_map_model_obj.fsc.fsc):
        print >>of, "%15.9f %15.9f"%(a,b)
      of.close()
      # XXX
    #
    print
    print d99_obj.result.d99 #XXX
    print d99_half1_obj.result.d99, d99_half2_obj.result.d99 #XXX
    print d_model_obj.d_min, d_model_obj.b_iso, d_model_obj.cc
    print fsc_obj.d_min
    print d_fsc_model

if (__name__ == "__main__"):
  run(args=sys.argv[1:])