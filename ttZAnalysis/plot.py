import os, sys
from plotterconf import *
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
sys.path.append(basepath)
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow
from ROOT import TCanvas, gROOT
gROOT.SetBatch(1)

######################################################################################
### Plots

hm = HistoManager(processes, systematics, '', path=path, processDic=processDic, lumi = Lumi)
doParallel = True

def Draw(name = 'Lep0Pt_eee_lep', rebin = 1, xtit = '', ytit = 'Events', doStackOverflow = False, binlabels = '', setLogY = False, maxscale = 2, tag = False):
  if doParallel:
    return "Draw(%s, %i, \'%s\', \'%s\', %s, \'%s\', %s, %i, %s)"%("\'" + name + "\'" if type(name) == str else "[\'"+ "\',\'".join(name) + "\']" , rebin, xtit, ytit, "True" if doStackOverflow else "False", binlabels, "True" if setLogY else "False", maxscale, "False" if not(tag) else tag)

  s = Stack(outpath=outpath, doRatio = False)
  s.SetColors(colors)
  s.SetProcesses(processes)
  s.SetLumi(Lumi)
  s.SetHistoPadMargins(top = 0.08, bottom = 0.10, right = 0.06, left = 0.10)
  s.SetRatioPadMargins(top = 0.03, bottom = 0.40, right = 0.06, left = 0.10)
  s.SetTextLumi(texlumi = '%2.0f pb^{-1} (13 TeV)', texlumiX = 0.61, texlumiY = 0.96, texlumiS = 0.05)
  s.SetTextCMSmode(y = 0.865, s = 0.052)
  s.SetTextCMS(y = 0.87, s = 0.06)
  hm.SetStackOverflow(doStackOverflow)
  hm.SetHisto(name, rebin)
  s.SetHistosFromMH(hm)
  if tag == False:
    tag = name if type(name) == str else name[0]
    if type(name) == type([]):
      tag = tag.replace("eee","all").replace("emm","all").replace("mee","all").replace("mmm","all")
  s.SetOutName(tag)
  s.SetBinLabels(binlabels)
  s.SetTextChan('')
  s.SetRatioMin(2-maxscale)
  s.SetRatioMax(maxscale)
  s.SetTextChan('')
  s.SetLogY(setLogY)
  s.SetPlotMaxScale(maxscale)
  s.SetXtitle(size = 0.05, offset = 0.8, nDiv = 510, labSize = 0.04)
  s.SetYtitle(labSize = 0.04)
  s.DrawStack(xtit, ytit)
  return 1

joblist = []
#lev = 'met' #lep, met
for lev in ['3lep','3leptight','3jet','2tag']:
  for ch in ['all']:
    joblist.append(Draw(GetName('Yields', ch, ''), 1, 'Yields', 'Events',setLogY = True))
    joblist.append(Draw(GetName('Lep1Pt', ch, lev), 1, 'p_{T} (l_{1}) [GeV]', 'Events'))

if doParallel:
  from multiprocessing import Pool
  from contextlib import closing
  import time
  doParallel = False
  def execute(com):
    eval(com)

  with closing(Pool(8)) as p:
    print "Now running " + str(len(joblist)) + " commands using: " + str(8) + " processes. Please wait" 
    retlist1 = p.map_async(execute, joblist, 1)
    while not retlist1.ready():
      print("Plots left: {}".format(retlist1._number_left ))
      time.sleep(1)
    retlist1 = retlist1.get()
    p.close()
    p.join()
    p.terminate()
