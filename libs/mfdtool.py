import numpy as np
import matplotlib.pyplot as plt

#---------------------------------------

def mfdanalytic(a,b,mmin,mmax,mnum):

  '''
  Analytic magnitude-frequency distribution
  '''

  mbin = np.linspace(mmin,mmax,mnum)

  amfd = (1.-(10.**(-b*(mbin-mmin))))/(1.-(10.**(-b*(mmax-mmin))))
  amfd = a*(1-amfd)

  return mbin, amfd

#---------------------------------------

def mfdhist(cat,mmin,mmax,dm,time,area=[]):

  mbin = np.arange(mmin,mmax,dm)-(dm/2)
  mlen = len(mbin)
  mhst = np.zeros(mlen)
  chst = np.zeros(mlen)

  if not area:
    area = 1

  for im, mm in enumerate(mbin[::-1]):

    im = mlen-im-1

    cat_sel = cat[(cat >= mm) & (cat < mm+dm)]
    mhst[im] = len(cat_sel)/(time*area)

    if im == (mlen-1):
      chst[im] = mhst[im]
    else:
      chst[im] = mhst[im]+chst[im+1]

  return mbin, mhst, chst

#---------------------------------------

def mfdplot(mbin,mhst,chst):

  plt.figure(figsize=(6,4))

  plt.semilogy(mbin,mhst,'gs-', markersize=6, label='Non Cumuative')
  plt.semilogy(mbin,chst,'ro-', markersize=6, label='Cumuative')

  plt.legend()
  plt.title('GR-Relation')
  plt.xlabel('Magnitude')
  plt.ylabel('Occurrence Rate (Event/Year)')

  #plt.xlim(2.5,8.5)
  #plt.ylim(1e-3,1e3)

  # plt.show(block=False)