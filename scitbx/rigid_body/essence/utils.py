from scitbx.rigid_body.essence import featherstone
from scitbx import matrix

def center_of_mass_from_sites(sites):
  assert len(sites) != 0
  result = matrix.col((0,0,0))
  for site in sites:
    result += site
  result /= len(sites)
  return result

def inertia_from_sites(sites, pivot):
  m = [0] * 9
  for site in sites:
    x,y,z = site - pivot
    m[0] += y*y+z*z
    m[4] += x*x+z*z
    m[8] += x*x+y*y
    m[1] -= x*y
    m[2] -= x*z
    m[5] -= y*z
  m[3] = m[1]
  m[6] = m[2]
  m[7] = m[5]
  return matrix.sqr(m)

def spatial_inertia_from_sites(
      sites,
      mass=None,
      center_of_mass=None,
      alignment_T=None):
  if (mass is None):
    mass = len(sites)
  if (center_of_mass is None):
    center_of_mass = center_of_mass_from_sites(sites=sites)
  inertia = inertia_from_sites(sites=sites, pivot=center_of_mass)
  if (alignment_T is not None):
    center_of_mass = alignment_T * center_of_mass
    inertia = alignment_T.r * inertia * alignment_T.r.transpose()
  return featherstone.mcI(m=mass, c=center_of_mass, I=inertia)

def kinetic_energy(I_spatial, v_spatial):
  "RBDA Eq. 2.67"
  return 0.5 * v_spatial.dot(I_spatial * v_spatial)

def T_as_X(Tps):
  return featherstone.Xrot(Tps.r) \
       * featherstone.Xtrans(-Tps.r.transpose() * Tps.t)

class featherstone_system_model(object):

  def __init__(O, bodies):
    O.bodies = bodies
    for B in bodies:
      if (B.parent == -1):
        Ttree = B.A.T0b
      else:
        Ttree = B.A.T0b * bodies[B.parent].A.Tb0
      B.Xtree = T_as_X(Ttree)

  def Xup(O):
    result = []
    for B in O.bodies:
      result.append(B.J.Xj * B.Xtree)
    return result

  def spatial_velocities(O, Xup):
    result = []
    if (Xup is None): Xup = O.Xup()
    for B,Xup_i in zip(O.bodies, O.Xup()):
      if (B.J.S is None):
        vJ = B.qd
      else:
        vJ = B.J.S * B.qd
      if B.parent == -1:
        result.append(vJ)
      else:
        result.append(Xup_i * result[B.parent] + vJ)
    return result

  def e_kin(O, Xup=None):
    result = 0
    for B,v in zip(O.bodies, O.spatial_velocities(Xup=Xup)):
      result += kinetic_energy(I_spatial=B.I, v_spatial=v)
    return result
