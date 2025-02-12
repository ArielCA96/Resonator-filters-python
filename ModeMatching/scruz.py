import cupy as cp

from ModeMatching.ctct import ctct
from ModeMatching.stst import stst

def scruz(a1, a2, b1, b2, gmtee, gmtme, gmtes, gmtms, del1, del2, gm1, gm2, f):
    c = cp.float64(3e8)  # Velocidad de la luz
    u = cp.float64(4 * cp.pi * 1e-7)  # Permeabilidad del vacío
    e = cp.float64(8.854187817e-12)  # Permisividad del vacío
    mu = cp.sqrt(u / e)
    ka = 2 * cp.pi * f / c

    c0 = cp.complex(0, 0)
    ur = cp.complex(1, 0)
    ui = cp.complex(0, 1)
    c2 = cp.complex(2, 0)

    da = (a1 - a2) / 2
    db = (b1 - b2) / 2

    num_tee = len(gmtee)
    num_tme = len(gmtme)
    num_tes = len(gmtes)
    num_tms = len(gmtms)

    # Cálculo de cruces TE(salida) - TE(entrada)
    gc2 = -(cp.pi**2) * ((gmtes[:, 0] / a2)**2 + (gmtes[:, 1] / b2)**2)
    nte2 = 1.0 / cp.sqrt(del2[:num_tes])
    teex2 = nte2 * ((ui * ka * mu / gc2) * (-gmtes[:, 1] * cp.pi / b2))
    teey2 = nte2 * ((ui * ka * mu / gc2) * (gmtes[:, 0] * cp.pi / a2))
    ckx2 = gmtes[:, 0] * cp.pi / a2
    cky2 = gmtes[:, 1] * cp.pi / b2
    dx = -ckx2 * da
    dy = -cky2 * db

    gc1 = -(cp.pi**2) * ((gmtee[:, 0] / a1)**2 + (gmtee[:, 1] / b1)**2)
    nte1 = 1.0 / cp.sqrt(del1[:num_tee])
    tehx1 = nte1 * (gm1[:num_tee] / gc1) * (-gmtee[:, 0] * cp.pi / a1)
    tehy1 = nte1 * (gm1[:num_tee] / gc1) * (-gmtee[:, 1] * cp.pi / b1)
    ckx1 = gmtee[:, 0] * cp.pi / a1
    cky1 = gmtee[:, 1] * cp.pi / b1

    rcc1 = ctct(da, da + a2, ckx1, ckx2, dx)
    rss1 = stst(db, db + b2, cky1, cky2, dy)
    rss2 = stst(da, da + a2, ckx1, ckx2, dx)
    rcc2 = ctct(db, db + b2, cky1, cky2, dy)

    yb3311 = (teex2 @ tehy1.T) * (rcc1 * rss1) - (teey2 @ tehx1.T) * (rss2 * rcc2)

    # Cálculo de cruces TE(salida) - TM(entrada)
    gc2 = -(cp.pi**2) * ((gmtes[:, 0] / a2)**2 + (gmtes[:, 1] / b2)**2)
    nte2 = 1.0 / cp.sqrt(del2[:num_tes])
    teex2 = nte2 * ((ui * ka * mu / gc2) * (-gmtes[:, 1] * cp.pi / b2))
    teey2 = nte2 * ((ui * ka * mu / gc2) * (gmtes[:, 0] * cp.pi / a2))
    ckx2 = gmtes[:, 0] * cp.pi / a2
    cky2 = gmtes[:, 1] * cp.pi / b2
    dx = -ckx2 * da
    dy = -cky2 * db

    gc1 = -(cp.pi**2) * ((gmtme[:, 0] / a1)**2 + (gmtme[:, 1] / b1)**2)
    ntm1 = 1e6 / cp.sqrt(del1[num_tee:num_tee + num_tme])
    tmhx1 = ntm1 * (ui * ka / (gc1 * mu)) * (-gmtme[:, 1] * cp.pi / b1)
    tmhy1 = ntm1 * (ui * ka / (gc1 * mu)) * (gmtme[:, 0] * cp.pi / a1)
    ckx1 = gmtme[:, 0] * cp.pi / a1
    cky1 = gmtme[:, 1] * cp.pi / b1

    rcc1 = ctct(da, da + a2, ckx1, ckx2, dx)
    rss1 = stst(db, db + b2, cky1, cky2, dy)
    rss2 = stst(da, da + a2, ckx1, ckx2, dx)
    rcc2 = ctct(db, db + b2, cky1, cky2, dy)

    yb3312 = (teex2 @ tmhy1.T) * (rcc1 * rss1) - (teey2 @ tmhx1.T) * (rss2 * rcc2)

    # Cálculo de cruces TM(salida) - TE(entrada)
    gc2 = -(cp.pi**2) * ((gmtms[:, 0] / a2)**2 + (gmtms[:, 1] / b2)**2)
    ntm2 = 1e6 / cp.sqrt(del2[num_tes:num_tes + num_tms])
    tmex2 = ntm2 * (gm2[num_tes:num_tes + num_tms] / gc2) * (gmtms[:, 0] * cp.pi / a2)
    tmey2 = ntm2 * (gm2[num_tes:num_tes + num_tms] / gc2) * (gmtms[:, 1] * cp.pi / b2)
    ckx2 = gmtms[:, 0] * cp.pi / a2
    cky2 = gmtms[:, 1] * cp.pi / b2
    dx = -ckx2 * da
    dy = -cky2 * db

    gc1 = -(cp.pi**2) * ((gmtee[:, 0] / a1)**2 + (gmtee[:, 1] / b1)**2)
    nte1 = 1.0 / cp.sqrt(del1[:num_tee])
    tehx1 = nte1 * (gm1[:num_tee] / gc1) * (-gmtee[:, 0] * cp.pi / a1)
    tehy1 = nte1 * (gm1[:num_tee] / gc1) * (-gmtee[:, 1] * cp.pi / b1)
    ckx1 = gmtee[:, 0] * cp.pi / a1
    cky1 = gmtee[:, 1] * cp.pi / b1

    rcc1 = ctct(da, da + a2, ckx1, ckx2, dx)
    rss1 = stst(db, db + b2, cky1, cky2, dy)
    rss2 = stst(da, da + a2, ckx1, ckx2, dx)
    rcc2 = ctct(db, db + b2, cky1, cky2, dy)

    yb3321 = (tmex2 @ tehy1.T) * (rcc1 * rss1) - (tmey2 @ tehx1.T) * (rss2 * rcc2)

    # Cálculo de cruces TM(salida) - TM(entrada)
    gc2 = -(cp.pi**2) * ((gmtms[:, 0] / a2)**2 + (gmtms[:, 1] / b2)**2)
    ntm2 = 1e6 / cp.sqrt(del2[num_tes:num_tes + num_tms])
    tmex2 = ntm2 * (gm2[num_tes:num_tes + num_tms] / gc2) * (gmtms[:, 0] * cp.pi / a2)
    tmey2 = ntm2 * (gm2[num_tes:num_tes + num_tms] / gc2) * (gmtms[:, 1] * cp.pi / b2)
    ckx2 = gmtms[:, 0] * cp.pi / a2
    cky2 = gmtms[:, 1] * cp.pi / b2
    dx = -ckx2 * da
    dy = -cky2 * db

    gc1 = -(cp.pi**2) * ((gmtme[:, 0] / a1)**2 + (gmtme[:, 1] / b1)**2)
    ntm1 = 1e6 / cp.sqrt(del1[num_tee:num_tee + num_tme])
    tmhx1 = ntm1 * (ui * ka / (gc1 * mu)) * (-gmtme[:, 1] * cp.pi / b1)
    tmhy1 = ntm1 * (ui * ka / (gc1 * mu)) * (gmtme[:, 0] * cp.pi / a1)
    ckx1 = gmtme[:, 0] * cp.pi / a1
    cky1 = gmtme[:, 1] * cp.pi / b1

    rcc1 = ctct(da, da + a2, ckx1, ckx2, dx)
    rss1 = stst(db, db + b2, cky1, cky2, dy)
    rss2 = stst(da, da + a2, ckx1, ckx2, dx)
    rcc2 = ctct(db, db + b2, cky1, cky2, dy)

    yb3322 = (tmex2 @ tmhy1.T) * (rcc1 * rss1) - (tmey2 @ tmhx1.T) * (rss2 * rcc2)

    # Cálculo final
    sal = cp.vstack([cp.hstack([yb3311, yb3312]), cp.hstack([yb3321, yb3322])])

    # Si el valor es menos que 10^-5 lo consideramos nulo, y lo hacemos nulo
    var = cp.abs(sal) < 1e-5
    sal[var] = 0

    return sal