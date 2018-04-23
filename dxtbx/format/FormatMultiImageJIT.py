from __future__ import absolute_import, division, print_function
from dxtbx.format.FormatMultiImage import FormatMultiImage

class FormatMultiImageJIT(FormatMultiImage):

  '''
  Just-in-Time version of FormatMultiImage that does not instantiate the models ahead of time.
  It creates an ImageSetJIT class and returns it. Saves time when image file contains
  too many images to setup before processing.
  '''

  @classmethod
  def get_imageset(Class,
                   filenames,
                   beam=None,
                   detector=None,
                   goniometer=None,
                   scan=None,
                   as_sweep=False,
                   as_imageset=False,
                   single_file_indices=None,
                   format_kwargs=None,
                   template=None,
                   check_format=True,
                   just_in_time=True):

    return super(FormatMultiImageJIT, Class).get_imageset(filenames=filenames,
                                                          beam=beam,
                                                          detector=detector,
                                                          goniometer=goniometer,
                                                          scan=scan,
                                                          as_sweep=as_sweep,
                                                          as_imageset=as_imageset,
                                                          single_file_indices=single_file_indices,
                                                          format_kwargs=format_kwargs,
                                                          template=template,
                                                          check_format=check_format,
                                                          just_in_time=just_in_time)
