from __future__ import generators
from cctbx.array_family import flex

import boost.python
ext = boost.python.import_ext("cctbx_crystal_ext")
from cctbx_crystal_ext import *

from cctbx.crystal.find_best_cell import find_best_cell
from cctbx import sgtbx
from cctbx import uctbx

from scitbx.array_family import shared
from scitbx import stl
import scitbx.stl.set
import scitbx.stl.vector
from scitbx.python_utils.misc import adopt_init_args
from libtbx.utils import Keep
import sys

pair_sym_ops = sgtbx.stl_vector_rt_mx

pair_asu_j_sym_groups = scitbx.stl.vector.set_unsigned
pair_asu_j_sym_group = scitbx.stl.set.unsigned

class symmetry(object):

  def __init__(self, unit_cell=None,
                     space_group_symbol=None,
                     space_group_info=None,
                     space_group=None,
                     assert_is_compatible_unit_cell=True,
                     force_compatible_unit_cell=True):
    assert [space_group_symbol, space_group_info, space_group].count(None) >= 2
    if (    unit_cell is not None
        and not isinstance(unit_cell, uctbx.ext.unit_cell)):
      unit_cell = uctbx.unit_cell(unit_cell)
    self._unit_cell = unit_cell
    self._space_group_info = space_group_info
    if (self._space_group_info is None):
      if (space_group_symbol is not None):
        self._space_group_info = sgtbx.space_group_info(
          symbol=space_group_symbol)
      elif (space_group is not None):
        if (isinstance(space_group, sgtbx.space_group)):
          self._space_group_info = sgtbx.space_group_info(group=space_group)
        else:
          self._space_group_info = sgtbx.space_group_info(symbol=space_group)
    if (self.unit_cell() is not None and self.space_group_info() is not None):
      if (assert_is_compatible_unit_cell):
        assert self.is_compatible_unit_cell(), \
          "Space group is incompatible with unit cell parameters."
      if (force_compatible_unit_cell):
        self._unit_cell = self.space_group().average_unit_cell(self._unit_cell)

  def _copy_constructor(self, other):
    self._unit_cell = other._unit_cell
    self._space_group_info = other._space_group_info

  def customized_copy(self, unit_cell=Keep, space_group_info=Keep):
    if (unit_cell is Keep): unit_cell = self._unit_cell
    if (space_group_info is Keep): space_group_info = self._space_group_info
    return symmetry(unit_cell=unit_cell, space_group_info=space_group_info)

  def unit_cell(self):
    return self._unit_cell

  def space_group_info(self):
    return self._space_group_info

  def space_group(self):
    return self.space_group_info().group()

  def show_summary(self, f=None, prefix=""):
    if (f is None): f = sys.stdout
    if (self.unit_cell() is None):
      print >> f, prefix + "Unit cell:", None
    else:
      self.unit_cell().show_parameters(f=f, prefix=prefix+"Unit cell: ")
    if (self.space_group_info() is None):
      print >> f, prefix + "Space group:", None
    else:
      self.space_group_info().show_summary(f=f, prefix=prefix+"Space group: ")

  def is_similar_symmetry(self, other, relative_length_tolerance=0.01,
                                       absolute_angle_tolerance=1.):
    if (not self.unit_cell().is_similar_to(other.unit_cell(),
      relative_length_tolerance, absolute_angle_tolerance)): return False
    return self.space_group() == other.space_group()

  def is_compatible_unit_cell(self):
    return self.space_group().is_compatible_unit_cell(self.unit_cell())

  def cell_equivalent_p1(self):
    return symmetry(self.unit_cell(), space_group_symbol="P 1")

  def change_basis(self, cb_op):
    if (isinstance(cb_op, str)):
      cb_op = sgtbx.change_of_basis_op(cb_op)
    return symmetry(
      unit_cell=cb_op.apply(self.unit_cell()),
      space_group_info=self.space_group_info().change_basis(cb_op))

  def primitive_setting(self):
    return self.change_basis(self.space_group().z2p_op())

  def change_of_basis_op_to_reference_setting(self):
    return self.space_group_info().type().cb_op()

  def as_reference_setting(self):
    return self.change_basis(self.change_of_basis_op_to_reference_setting())

  def change_of_basis_op_to_best_cell(self, angular_tolerance=None):
    return find_best_cell(self, angular_tolerance=angular_tolerance).cb_op()

  def best_cell(self, angular_tolerance=None):
    return self.change_basis(self.change_of_basis_op_to_best_cell(
      angular_tolerance=angular_tolerance))

  def change_of_basis_op_to_minimum_cell(self):
    z2p_op = self.space_group().z2p_op()
    r_inv = z2p_op.c_inv().r()
    p_cell = self.unit_cell().change_basis(r_inv.num(), r_inv.den())
    red = p_cell.minimum_reduction()
    p2n_op = sgtbx.change_of_basis_op(
      sgtbx.rt_mx(sgtbx.rot_mx(red.r_inv(), 1))).inverse()
    return p2n_op.new_denominators(z2p_op) * z2p_op

  def minimum_cell(self):
    return self.change_basis(self.change_of_basis_op_to_minimum_cell())

  def change_of_basis_op_to_niggli_cell(self,
        relative_epsilon=None,
        iteration_limit=None):
    z2p_op = self.space_group().z2p_op()
    r_inv = z2p_op.c_inv().r()
    p_cell = self.unit_cell().change_basis(r_inv.num(), r_inv.den())
    red = p_cell.niggli_reduction(
      relative_epsilon=relative_epsilon,
      iteration_limit=iteration_limit)
    p2n_op = sgtbx.change_of_basis_op(
      sgtbx.rt_mx(sgtbx.rot_mx(red.r_inv().elems, 1))).inverse()
    return p2n_op.new_denominators(z2p_op) * z2p_op

  def niggli_cell(self,
        relative_epsilon=None,
        iteration_limit=None):
    return self.change_basis(self.change_of_basis_op_to_niggli_cell(
      relative_epsilon=relative_epsilon,
      iteration_limit=iteration_limit))

  def reflection_intensity_symmetry(self, anomalous_flag):
    return symmetry(
      unit_cell=self.unit_cell(),
      space_group=self.space_group()
        .build_derived_reflection_intensity_group(
          anomalous_flag=anomalous_flag))

  def patterson_symmetry(self):
    return symmetry(
      unit_cell=self.unit_cell(),
      space_group=self.space_group().build_derived_patterson_group())

  def is_patterson_symmetry(self):
    return self.space_group().build_derived_patterson_group() \
        == self.space_group()

  def join_symmetry(self, other_symmetry, force=False):
    if (other_symmetry is None):
      return self
    if (force == False):
      strong = self
      weak = other_symmetry
    else:
      strong = other_symmetry
      weak = self
    unit_cell = strong.unit_cell()
    space_group_info = strong.space_group_info()
    if (unit_cell is None):
      unit_cell = weak.unit_cell()
    if (space_group_info is None):
      space_group_info = weak.space_group_info()
    return symmetry(
       unit_cell=unit_cell,
       space_group_info=space_group_info)

  def direct_space_asu(self):
    return self.space_group_info().direct_space_asu().define_metric(
      unit_cell=self.unit_cell())

  def gridding(self, d_min=None,
                     resolution_factor=None,
                     step=None,
                     symmetry_flags=None,
                     mandatory_factors=None,
                     max_prime=5,
                     assert_shannon_sampling=True):
    from cctbx import maptbx
    return maptbx.crystal_gridding(
      unit_cell=self.unit_cell(),
      d_min=d_min,
      resolution_factor=resolution_factor,
      step=step,
      symmetry_flags=symmetry_flags,
      space_group_info=self.space_group_info(),
      mandatory_factors=mandatory_factors,
      max_prime=max_prime,
      assert_shannon_sampling=assert_shannon_sampling)

  def asu_mappings(self, buffer_thickness, is_inside_epsilon=None):
    return direct_space_asu.asu_mappings(
      space_group=self.space_group(),
      asu=self.direct_space_asu().as_float_asu(
        is_inside_epsilon=is_inside_epsilon),
      buffer_thickness=buffer_thickness)

class special_position_settings(symmetry):

  def __init__(self, crystal_symmetry,
               min_distance_sym_equiv=0.5,
               u_star_tolerance=0,
               assert_is_positive_definite=False,
               assert_min_distance_sym_equiv=True):
    symmetry._copy_constructor(self, crystal_symmetry)
    self._min_distance_sym_equiv = min_distance_sym_equiv
    self._u_star_tolerance = u_star_tolerance
    self._assert_is_positive_definite = assert_is_positive_definite
    self._assert_min_distance_sym_equiv = assert_min_distance_sym_equiv

  def _copy_constructor(self, other):
    symmetry._copy_constructor(self, other)
    self._min_distance_sym_equiv = other._min_distance_sym_equiv
    self._u_star_tolerance = other._u_star_tolerance
    self._assert_is_positive_definite = other._assert_is_positive_definite
    self._assert_min_distance_sym_equiv = other._assert_min_distance_sym_equiv

  def min_distance_sym_equiv(self):
    return self._min_distance_sym_equiv

  def u_star_tolerance(self):
    return self._u_star_tolerance

  def assert_is_positive_definite(self):
    return self._assert_is_positive_definite

  def assert_min_distance_sym_equiv(self):
    return self._assert_min_distance_sym_equiv

  def site_symmetry(self, site):
    return sgtbx.site_symmetry(
      self.unit_cell(),
      self.space_group(),
      site,
      self.min_distance_sym_equiv(),
      self.assert_min_distance_sym_equiv())

  def sym_equiv_sites(self, site):
    return sgtbx.sym_equiv_sites(self.site_symmetry(site))

  def site_symmetry_table(self, sites_frac=None, sites_cart=None):
    assert (sites_frac is None) != (sites_cart is None)
    if (sites_frac is None):
      sites_frac = self.unit_cell().fractionalization_matrix() * sites_cart
    result = sgtbx.site_symmetry_table()
    result.process(
      unit_cell=self.unit_cell(),
      space_group=self.space_group(),
      original_sites_frac=sites_frac,
      min_distance_sym_equiv=self.min_distance_sym_equiv(),
      assert_min_distance_sym_equiv=self.assert_min_distance_sym_equiv())
    return result

  def asu_mappings(self,
        buffer_thickness,
        sites_frac=None,
        sites_cart=None,
        site_symmetry_table=None,
        is_inside_epsilon=None):
    asu_mappings = symmetry.asu_mappings(self,
      buffer_thickness=buffer_thickness,
      is_inside_epsilon=is_inside_epsilon)
    if (sites_frac is not None or sites_cart is not None):
      if (sites_frac is None):
        sites_frac = self.unit_cell().fractionalization_matrix() * sites_cart
        del sites_cart
      if (site_symmetry_table is None):
        site_symmetry_table = self.site_symmetry_table(sites_frac=sites_frac)
      asu_mappings.process_sites_frac(
        original_sites=sites_frac,
        site_symmetry_table=site_symmetry_table)
    return asu_mappings

  def change_basis(self, cb_op):
    return special_position_settings(
      crystal_symmetry=symmetry.change_basis(self, cb_op),
      min_distance_sym_equiv=self.min_distance_sym_equiv(),
      u_star_tolerance=self.u_star_tolerance(),
      assert_is_positive_definite=self.assert_is_positive_definite(),
      assert_min_distance_sym_equiv=self.assert_min_distance_sym_equiv())

def correct_special_position(
      unit_cell,
      special_op,
      site_frac=None,
      site_cart=None,
      tolerance=1.e-2,
      error_message="Corrupt gradient calculations."):
  """
  During refinement it is essential to reset special positions
  because otherwise rounding error accumulate over many cycles.
  """
  assert (site_frac is None) != (site_cart is None)
  if (site_frac is None):
    site_frac = unit_cell.fractionalize(site_cart)
  site_special_frac = special_op * site_frac
  distance_moved = unit_cell.distance(site_special_frac, site_frac)
  if (distance_moved > tolerance):
    raise AssertionError(
      error_message + " (special_op: %s; distance_moved: %.6g)"
        % (str(special_op), distance_moved))
  if (site_cart is None):
    return site_special_frac
  return unit_cell.orthogonalize(site_special_frac)

class _pair_asu_table(boost.python.injector, pair_asu_table):

  def show(self, f=None, site_labels=None):
    if (f is None): f = sys.stdout
    if (site_labels is None):
      for i_seq, j_seq_dict in enumerate(self.table()):
        print >> f, "i_seq:", i_seq
        for j_seq,j_sym_group in j_seq_dict.items():
          print >> f, "  j_seq:", j_seq
          for j_syms in j_sym_group:
            print >> f, "    j_syms:", list(j_syms)
    else:
      assert len(site_labels) == self.table().size()
      for i_seq, j_seq_dict in enumerate(self.table()):
        print >> f, "%s(%d)" % (site_labels[i_seq], i_seq)
        for j_seq,j_sym_group in j_seq_dict.items():
          print >> f, "  %s(%d)" % (site_labels[j_seq], j_seq)
          for j_syms in j_sym_group:
            print >> f, "    j_syms:", list(j_syms)

class sym_pair:

  def __init__(self, i_seq, j_seq, rt_mx_ji):
    adopt_init_args(self, locals())

  def i_seqs(self):
    return (self.i_seq, self.j_seq)

class _pair_sym_table(boost.python.injector, pair_sym_table):

  def iterator(self):
    for i_seq,pair_sym_dict in enumerate(self):
      for j_seq,sym_ops in pair_sym_dict.items():
        for rt_mx_ji in sym_ops:
          yield sym_pair(i_seq=i_seq, j_seq=j_seq, rt_mx_ji=rt_mx_ji)

  def show(self, f=None, site_labels=None):
    if (f is None): f = sys.stdout
    if (site_labels is None):
      for i_seq,pair_sym_dict in enumerate(self):
        print >> f, "i_seq:", i_seq
        for j_seq,sym_ops in pair_sym_dict.items():
          print >> f, "  j_seq:", j_seq
          for sym_op in sym_ops:
            print >> f, "   ", sym_op
    else:
      for i_seq,pair_sym_dict in enumerate(self):
        print >> f, "%s(%d)" % (site_labels[i_seq], i_seq)
        for j_seq,sym_ops in pair_sym_dict.items():
          print >> f, "  %s(%d)" % (site_labels[j_seq], j_seq)
          for sym_op in sym_ops:
            print >> f, "   ", sym_op
