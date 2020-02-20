import ROOT

import os, sys

basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
sys.path.append(basepath)
from plotterconf import *
from tt5TeV.scripts.CrossSection import CrossSection



def xsec(chan = 'eee', lev = 'lep'):
  x = CrossSection(outpath, chan, lev)
  x.SetTextFormat("tex")
  bkg = []
  bkg.append(['DY',            process['DY'],   0.15])
  bkg.append(['VV',            process['VV'],   0.30])
  bkg.append(['top',           process['top'],  0.10])   
  signal   = ['WZ',            process['WZ']]
  data     = process['WZ']
  expunc = "JER"
  modunc = "JER"

  x.ReadHistos(path, chan, lev, bkg = bkg, signal = signal, data = data, expUnc = expunc, modUnc = modunc)
  x.SetLumi(296.1)
  x.SetLumiUnc(0.035)

  
  suf = '_'+chan+'_'+lev
  x.PrintYields('Yields'+suf)
  #x.PrintSystTable('Systematics'+suf)
  #x.PrintXsec('CrossSection'+suf)

xsec('eee','lep')
xsec('mmm','lep')
