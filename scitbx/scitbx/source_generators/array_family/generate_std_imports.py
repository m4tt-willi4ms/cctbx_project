import sys

import path_to_include
import generate_operator_functors

def write_copyright():
  try: name = __file__
  except: name = sys.argv[0]
  print \
"""/* Copyright (c) 2001-2002 The Regents of the University of California
   through E.O. Lawrence Berkeley National Laboratory, subject to
   approval by the U.S. Department of Energy.
   See files COPYRIGHT.txt and LICENSE.txt for further details.

   Revision history:
     2002 Aug: Copied from cctbx/global (Ralf W. Grosse-Kunstleve)
     2002 Feb: Created (Ralf W. Grosse-Kunstleve)

   *****************************************************
   THIS IS AN AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
   *****************************************************

   Generated by:
     %s
 */""" % (name,)

cmath_1arg = (
  'acos', 'cos', 'tan',
  'asin', 'cosh', 'tanh',
  'atan', 'exp', 'sin',
  'fabs', 'log', 'sinh',
  'ceil', 'floor', 'log10', 'sqrt',
)

cmath_2arg = (
  'fmod', 'pow', 'atan2',
)

cstdlib_1arg = (
  'abs',
)

complex_1arg = (
# "cos",
# "cosh",
# "exp",
# "log",
# "log10",
# "sin",
# "sinh",
# "sqrt",
# "tan",
# "tanh",
  "conj",
)

complex_special = (
("ElementType", "real", "std::complex<ElementType>"),
("ElementType", "imag", "std::complex<ElementType>"),
("ElementType", "abs", "std::complex<ElementType>"),
("ElementType", "arg", "std::complex<ElementType>"),
("ElementType", "norm", "std::complex<ElementType>"),
("std::complex<ElementType>", "pow", "std::complex<ElementType>",
                                     "int"),
("std::complex<ElementType>", "pow", "std::complex<ElementType>",
                                     "ElementType"),
("std::complex<ElementType>", "pow", "std::complex<ElementType>",
                                     "std::complex<ElementType>"),
("std::complex<ElementType>", "pow", "ElementType",
                                     "std::complex<ElementType>"),
("std::complex<ElementType>", "polar", "ElementType",
                                       "ElementType"),
)

complex_special_addl_1arg = ("real", "imag", "arg", "norm")
complex_special_addl_2arg = ("polar",)

def generate_1arg():
  for function_name in (
    cmath_1arg + cstdlib_1arg + complex_1arg + complex_special_addl_1arg):
    generate_operator_functors.generate_unary(
      function_name, function_name + "(x)")

def generate_2arg():
  for function_name in cmath_2arg + complex_special_addl_2arg:
    generate_operator_functors.generate_binary(
      function_name, function_name + "(x, y)")

def run():
  output_file_name = path_to_include.expand("detail/std_imports.h")
  print "Generating:", output_file_name
  f = open(output_file_name, "w")
  sys.stdout = f
  write_copyright()
  print """
#ifndef SCITBX_ARRAY_FAMILY_STD_IMPORTS_H
#define SCITBX_ARRAY_FAMILY_STD_IMPORTS_H

#ifndef DOXYGEN_SHOULD_SKIP_THIS

#include <cmath>
#include <cstdlib>
#include <complex>

namespace scitbx { namespace fn {
"""

  all_function_names = []
  for function_name in cmath_1arg + cmath_2arg + cstdlib_1arg + complex_1arg:
    if (not function_name in all_function_names):
      all_function_names.append(function_name)
  for entry in complex_special:
    function_name = entry[1]
    if (not function_name in all_function_names):
      all_function_names.append(function_name)

  for function_name in all_function_names:
    print "  using std::" + function_name + ";"

  generate_1arg()
  generate_2arg()

  print """
}} // namespace scitbx::af

#endif // DOXYGEN_SHOULD_SKIP_THIS

#endif // SCITBX_ARRAY_FAMILY_STD_IMPORTS_H"""
  sys.stdout = sys.__stdout__
  f.close()

if (__name__ == "__main__"):
  run()
