import os.path

def expand(file_name):
  return os.path.normpath(os.path.join(
    "../../../include/scitbx/array_family", file_name))
