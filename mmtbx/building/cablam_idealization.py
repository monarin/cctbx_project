from __future__ import division

from libtbx import group_args
import libtbx.phil

from mmtbx.validation.cablam import cablamalyze, fetch_peptide_expectations, \
    fetch_ca_expectations, fetch_motif_contours
from libtbx.utils import Sorry, null_out

from cctbx import geometry_restraints

import itertools

from scitbx.matrix import rotate_point_around_axis

from mmtbx.refinement.geometry_minimization import run2
from mmtbx.building.loop_closure.utils import list_rama_outliers_h
from mmtbx.secondary_structure import manager as ss_manager_class


master_phil_str = '''
cablam_idealization {
  nproc = 1
    .type = int
    .help = Parallelization is not implemented
  do_gm = False
    .type = bool
    .help = Run geometry minimization after rotation
  find_ss_after_fixes = True
    .type = bool
    .help = re-evaluate SS after fixing Cablam outliers. May be helpful to \
      identify new or extend previous SS elements
  save_intermediates = False
    .type = bool
    .help = Save all cablam rotation for particular residue in separate file
}
'''

# This is needed to import scope
master_phil = libtbx.phil.parse(master_phil_str)

class cablam_idealization(object):
  def __init__(self, model, params, log):
    """
    model is changed in place
    params - those in master_phil_str without scope name
    """
    self.model = model
    self.params = params
    self.log = log
    self.outliers = None
    self.cablam_contours = fetch_peptide_expectations()
    self.ca_contours = fetch_ca_expectations()
    self.motif_contours = fetch_motif_contours()
    self.n_tried_residues = 0
    self.n_rotated_residues = 0


    # with open("in.pdb",'w') as f:
    #   f.write(self.model.model_as_pdb())


    if self.model.get_hierarchy().models_size() > 1:
      raise Sorry("Multi-model files are not supported")

    self.model.search_for_ncs()
    print >> self.log, self.model.get_ncs_obj().show_phil_format()

    self.outliers_by_chain = self.identify_outliers()

    # idealization
    for chain, outliers in self.outliers_by_chain.iteritems():
      b_selection = self.model.selection("chain %s" % chain)
      self.atoms_around = self.model.get_xray_structure().selection_within(7, b_selection).iselection()

      for outlier in outliers:
        self.fix_cablam_outlier(chain, outlier)

    if self.params.find_ss_after_fixes:
      ss_manager = ss_manager_class(
          pdb_hierarchy=self.model.get_hierarchy(),
          geometry_restraints_manager=self.model.get_restraints_manager().geometry,
          sec_str_from_pdb_file=None,
          params=None,
          mon_lib_srv=self.model.get_mon_lib_srv,
          verbose=-1,
          log=self.log)
      self.model.get_restraints_manager().geometry.set_secondary_structure_restraints(
          ss_manager=ss_manager,
          hierarchy=self.model.get_hierarchy(),
          log=self.log)
      self.model.set_ss_annotation(ann=ss_manager.actual_sec_str)

    self.cablam_fixed_minimized = None
    if params.do_gm:
      self.cablam_fixed_minimized = self._minimize()

  def _get_ca_atom(self, chainid, resid):
    for chain in self.model.get_master_hierarchy().only_model().chains():
      if chain.id.strip() == chainid.strip():
        for rg in chain.residue_groups():
          if rg.resid() == resid:
            for a in rg.atoms():
              if a.name.strip() == "CA":
                return a
    raise Sorry("Something went wrong. Cannot find CA atom.")
    return None


  def fix_cablam_outlier(self, chain, outlier):
    self.n_tried_residues += 1
    scores = []
    if len(outlier) == 1:
      curresid = outlier[0].residue.resid()
      prevresid = outlier[0].prevres.residue.resid()
      curresseq_int = outlier[0].residue.resseq_as_int()
      prevresseq_int = outlier[0].prevres.residue.resseq_as_int()
    elif len(outlier) == 2:
      curresid = outlier[1].residue.resid()
      prevresid = outlier[1].prevres.residue.resid()
      curresseq_int = outlier[1].residue.resseq_as_int()
      prevresseq_int = outlier[1].prevres.residue.resseq_as_int()
    else:
      print >> self.log, "Don't know how to deal with more than 2 outliers in a row yet. Skipping."
      return
    # h =  self.model.get_hierarchy()
    # s =  self.model.selection("chain %s and name CA and resid %s" % (chain, prevresid))
    # a1 = self.model.select(s).get_hierarchy().atoms()[0]
    # s =  self.model.selection("chain %s and name CA and resid %s" % (chain, curresid))
    # a2 = self.model.select(s).get_hierarchy().atoms()[0]
    # This is slightly faster, but poorer code. We'll see if it is needed.
    a1 = self._get_ca_atom(chain, prevresid)
    a2 = self._get_ca_atom(chain, curresid)

    print >> self.log, "*"*80
    print >> self.log, "Atoms for rotation:", chain, prevresid, curresid
    print >> self.log, "*"*80

    around_str_sel = "chain %s and resid %d:%d" % (chain, prevresseq_int-2, curresseq_int+2)
    chain_around = self.model.select(self.model.selection(around_str_sel))
    assert chain_around.get_number_of_atoms() > 0
    self.atoms_around_cutted = self.atoms_around.deep_copy()
    for i in range(12):
      # rotation
      angle = 30
      O_atom, N_atom, C_atom = self._rotate_cablam(self.model, chain,
          prevresid, curresid, a1, a2, angle=angle)
      if [O_atom, N_atom, C_atom].count(None) > 0:
        print >> self.log, "Residues are missing essential atom: O, N or C. Skipping."
        return
      self._rotate_cablam(chain_around, chain,
          prevresid, curresid, a1, a2, angle=angle)
      if self.params.save_intermediates:
        with open("out_%s_%d.pdb" % (curresid.strip(), i),'w') as f:
          f.write(self.model.model_as_pdb())
      scores.append(self._score_conformation(O_atom, C_atom, N_atom, chain_around, 30*(i+1)))
    print >> self.log, "angle, rama, cablam, hbonds"
    for s in scores:
      print >> self.log, s
    rot_angle = self._pick_rotation_angle(scores)
    # rotate
    if rot_angle != 360:
      self.n_rotated_residues += 1
      print >> self.log, "ROTATING by", rot_angle
      self._rotate_cablam(self.model, chain,
          prevresid, curresid, a1, a2, angle=rot_angle)

  def _rotate_cablam(self, model, chain, prevresid, curresid, a1, a2, angle):
    inside = False
    O_atom = None
    N_atom = None
    C_atom = None
    for c in model.get_master_hierarchy().only_model().chains():
      if c.id.strip() == chain.strip():
        for atom in c.atoms():
          if atom.name.strip() == "CA" and atom.parent().parent().resid() == prevresid:
            inside = True
          if atom.name.strip() == "CA" and atom.parent().parent().resid() == curresid:
            inside = False
          if inside and atom.name.strip() in ["N", "CA", "C", "O"]:
            new_xyz = rotate_point_around_axis(
                axis_point_1=a1.xyz,
                axis_point_2=a2.xyz,
                point=atom.xyz,
                angle=angle,
                deg=True)
            atom.set_xyz(new_xyz)
            if atom.name.strip() == "O":
              O_atom = atom
            elif atom.name.strip() == "N":
              N_atom = atom
            elif atom.name.strip() == "C":
              C_atom = atom

        model.set_sites_cart_from_hierarchy(multiply_ncs=True)

        return O_atom, N_atom, C_atom


  def _pick_rotation_angle(self, scores):
    # I want to pick the rotation with H-bond, less Rama outliers and less
    # cablam outliers.
    best = scores[-1] # last, no rotation
    for s in scores[:-1]:
      # [angle, rama, cablam, hbond]
      if (len(s[3]) > 0 and # hbond present
           ((s[1] <= best[1] and s[2] < best[2])
        or  (s[1] + s[2] < best[1] + best[2]))):
        best = s
    return best[0]

  def _minimize(self):
    m1 = self.model.deep_copy()
    m1.set_ramachandran_plot_restraints(rama_potential="oldfield")
    run2(
        restraints_manager=m1.get_restraints_manager(),
        pdb_hierarchy=m1.get_hierarchy(),
        correct_special_position_tolerance=1.0,
        riding_h_manager               = None,
        ncs_restraints_group_list      = [], # These are actually for NCS CONSTRAINTS!
        max_number_of_iterations       = 500,
        number_of_macro_cycles         = 5,
        selection                      = None,
        bond                           = True,
        nonbonded                      = True,
        angle                          = True,
        dihedral                       = True,
        chirality                      = True,
        planarity                      = True,
        parallelity                    = True,
        log = null_out())
    m1.set_sites_cart_from_hierarchy(multiply_ncs=True)
    return m1

  def _score_conformation(self, O_atom, C_atom, N_atom, chain_around, angle):
    # gs = self.model.geometry_statistics()
    # gs.show()
    # print "MOLPROBITY Score:", gs.result().molprobity_score
    # print "Cablam outliers:", gs.result().cablam.outliers
    # print "Clashscore: ", gs.result().clash.score
    hbonds = self._search_hbond(O_atom, C_atom, N_atom, chain_around)
    ro = list_rama_outliers_h(chain_around.get_hierarchy())
    cab_results = cablamalyze(
        pdb_hierarchy=chain_around.get_hierarchy(),
        outliers_only=True,
        out=null_out(),
        quiet=True,
        cablam_contours = self.cablam_contours,
        ca_contours = self.ca_contours,
        motif_contours = self.motif_contours,
        )
    outliers_only = [x for x in cab_results.results if x.feedback.cablam_outlier]
    return (angle, len(ro.split("\n"))-1, len(outliers_only), hbonds)

  def _search_hbond(self, O_atom, C_atom, N_atom, chain_around):
    def good_hbond(angle, distance):
      return angle > 140 and distance < 3.8
    results = []
    atoms = self.model.get_atoms()
    filtered_atoms_around_cutted = []
    for atom in [atoms[i_seq] for i_seq in self.atoms_around_cutted]:
      if atom.distance(O_atom) > 10:
        continue
      # no need to check the same residue, looking for N atom for bonding
      filtered_atoms_around_cutted.append(atom.i_seq)
      if atom.parent() == O_atom.parent() or atom.parent() == N_atom.parent():
        # print "skipping same residue ", atom.id_str()
        continue
      if atom.name.strip() == 'N':
        angle = geometry_restraints.angle(
            sites=[C_atom.xyz, O_atom.xyz, atom.xyz],
            angle_ideal=0,
            weight=1).angle_model
        if good_hbond(angle, atom.distance(O_atom)):
          # print "Potential bond:", atom.id_str(), atom.distance(O_atom), angle
          results.append(('forward', atom.distance(O_atom), angle))
      if atom.name.strip() == 'O':
        # now we want to find attached N atom (another one)
        another_C_atom = atom.parent().get_atom("C")
        if another_C_atom is not None:
          angle = geometry_restraints.angle(
              sites=[another_C_atom.xyz, atom.xyz, N_atom.xyz],
              angle_ideal=0,
              weight=1).angle_model
          if good_hbond(angle, atom.distance(N_atom)):
            # print "Potential backwards bond:", atom.id_str(), atom.distance(N_atom), angle
            results.append(('backward', atom.distance(N_atom), angle))
    self.atoms_around_cutted = filtered_atoms_around_cutted
    return results

  def identify_outliers(self):
    cab_results = cablamalyze(
        pdb_hierarchy=self.model.get_master_hierarchy(),
        outliers_only=True,
        out=null_out(),
        quiet=True,
        cablam_contours = self.cablam_contours,
        ca_contours = self.ca_contours,
        motif_contours = self.motif_contours)
    outliers_only = [x for x in cab_results.results if x.feedback.cablam_outlier]# and x.feedback.c_alpha_geom_outlier]
    outliers_by_chain = {}
    for k, g in itertools.groupby(outliers_only, key=lambda x: x.residue_id()[:2]):
      outliers_by_chain[k] = []
      comb = []
      for i in g:
        # print i.resseq, i.resseq_as_int(), i.icode, i, i.altloc, dir(i)
        if i.altloc.strip() != '':
          print >> self.log, "  ", i, "<--- SKIPPING, alternative conformations."
          continue
        if len(comb) == 0:
          comb = [i]
        else:
          if (i.resseq_as_int() - comb[-1].resseq_as_int() == 1 or
              (i.resseq_as_int() == comb[-1].resseq_as_int() and i.icode != comb[-1].icode)):
            comb.append(i)
          else:
            outliers_by_chain[k].append(comb)
            comb = [i]
        print >> self.log, "  ", i
      outliers_by_chain[k].append(comb)
    # here we want to combine them if they are next to each other.
    # probably will go with list of tuples
    return outliers_by_chain

  def get_results(self):
    return group_args(
      model = self.model,
      model_minimized = self.cablam_fixed_minimized,
      n_tried_residues = self.n_tried_residues,
      n_rotated_residues = self.n_rotated_residues)
