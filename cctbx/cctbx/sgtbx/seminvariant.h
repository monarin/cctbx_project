// $Id$
/* Copyright (c) 2001 The Regents of the University of California through
   E.O. Lawrence Berkeley National Laboratory, subject to approval by the
   U.S. Department of Energy. See files COPYRIGHT.txt and
   cctbx/LICENSE.txt for further details.

   Revision history:
     2001 Sep 02: start port of sglite/sgss.c (R.W. Grosse-Kunstleve)
 */

#ifndef CCTBX_SGTBX_SEMINVARIANT_H
#define CCTBX_SGTBX_SEMINVARIANT_H

#include <cctbx/fixcap_vector.h>
#include <cctbx/sgtbx/groups.h>

namespace sgtbx {

  //! Helper struct for class StructureSeminvariant.
  struct ssVM {
    Vec3 V;
    int M;
  };

  //! Structure-seminvariant vector and moduli.
  /*! Implementation of the algorithm published in section 6. of
      <A HREF="http://journals.iucr.org/a/issues/1999/02/02/au0146/"
      ><I>Acta Cryst.</I> 1999, <B>A55</B>:383-395</A>.<br>
      <p>
      Structure seminvariant (s.s.) vectors and moduli are
      a description of "permissible" or "allowed" origin
      shifts. These are important in crystal structure
      determination methods (e.g. direct methods) or for
      comparing crystal structures.
      <p>
      If the origin of the basis for a given group of
      symmetry operations is shifted by an allowed origin
      shift, the symmetry environment of the old and the
      new origin is identical. See International Tables for
      Crystallography Volume B, 2001, chapter 2.2.3. for
      details.
      <p>
      Allowed origin-shifts are also a part of the
      Euclidean normalizer symmetry. See International
      Tables for Crystallography Volume A, 1983, Table
      15.3.2., column "Translations."
      <p>
      See also: SgOps::getAddlGeneratorsOfEuclideanNormalizer()
   */
  class StructureSeminvariant {
    public:
      //! Default constructor.
      /*! Default-constructed instances have 0 vectors and moduli.
       */
      StructureSeminvariant() {}
      /*! \brief Compute structure-seminvariant vectors and moduli
          for given symmetry operations.
       */
      /*! See class details.
       */
      StructureSeminvariant(const SgOps& sgo);
      //! Number of structure-seminvariant vectors and moduli.
      /*! Possible results are in the range from 0 (e.g. space group
          Im-3m) to 3 (e.g. space group P1).
       */
      inline std::size_t size() const { return m_VM.size(); }
      //! The i'th structure-seminvariant vector and modulus.
      /*! An exception is thrown if i is out of range.
          <p>
          See also: V(), M()
       */
      inline const ssVM& VM(std::size_t i) const {
        if (i >= size()) throw error_index();
        return m_VM[i];
      }
      //! The i'th structure-seminvariant vector.
      /*! An exception is thrown if i is out of range.
          <p>
          See also: VM(), M()
       */
      inline const Vec3& V(std::size_t i) const { return VM(i).V; }
      //! The i'th structure-seminvariant modulus.
      /*! An exception is thrown if i is out of range.
          <p>
          See also: VM(), V()
       */
      inline int M(std::size_t i) const { return VM(i).M; }
      /*! \brief Test if the phase angle of the reflection with
          given Miller index is a structure-seminvariant.
       */
      bool is_ss(const Miller::Index& H) const;
      /*! \brief Reduce given Miller index for establishing the
           <i>primitivity condition</i>.
       */
      /*! The expression (V(i) * H) % M(i) is computed for
          each of the size() structure-seminvariant
          vectors and moduli. The size() results can be
          used to establish the <i>primitivity condition</i>
          (see International Tables for Crystallography Volume B,
          2001, chapter 2.2.3(h)):
          <p>
          A square (size() x size()) matrix is formed with size()
          reduced Miller indices. The size() reflections define
          the origin uniquely if the determinant of the matrix
          is +1 or -1.
       */
      cctbx::fixcap_vector<int, 3>
      apply_mod(const Miller::Index& H) const;

    private:
      cctbx::fixcap_vector<ssVM, 3> m_VM;
  };

} // namespace sgtbx

#endif // CCTBX_SGTBX_SEMINVARIANT_H
