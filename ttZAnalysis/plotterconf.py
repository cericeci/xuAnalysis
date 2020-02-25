import os, sys
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
sys.path.append(basepath)
from framework.functions import GetLumi
from plotter.TopHistoReader import TopHistoReader, HistoManager
from plotter.Plotter import Stack
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow, kWhite

### Input and output
#path = '../temp5TeV/sep17/'
path = '../tempttZ/'
outpath = 'plotsttZ/'

### Definition of the processes
processDic = {
'TTZ' : 'TTZToLLNuNu_m1to10,TTZToLLNuNu',
'TTW' : 'TTWToLNu',
'TTH' : 'TTHnonbb',
'tZq' : 'tZq_ll',
'TTTT' : 'TTTT',
'WZ'  : 'WZTo3LNu_pow,WZTo2L2Q',
'WW'  : 'WWTo2L2Nu,WW_DPS',
'DY'  : 'DYJetsToLL_M10to50,DYJetsToLL_M50',
'ZZ'  : 'HZZ,GluGluToContinToZZTo2e2mu,GluGluToContinToZZTo2e2nu,GluGluToContinToZZTo2e2tau,GluGluToContinToZZTo2mu2nu,GluGluToContinToZZTo2mu2tau,GluGluToContinToZZTo4e,GluGluToContinToZZTo4mu,GluGluToContinToZZTo4tau,ZZTo4L,ZZTo2L2Nu,ZZTo2L2Q',
'tt'  : 'TTTo2L2Nu,TTJets_SingleLeptFromT,TTJets_SingleLeptFromTbar',
'single t' : 'T_sch,Tbar_tch,T_tch,TbarW,TW', 
'convs' : 'TTGJets,WGToLNuG,ZGTo2LG',
'VVV' : 'WWW,WWZ,WZG,WZZ,ZZZ',
'VH'  : 'VHToNonbb',
'W+Jets' : 'WJetsToLNu',
}
#'data': 'HighEGJet, SingleMuon'}##SingleMuon
processes = [key for key in processDic.keys()]


process = processDic
### Definition of colors for the processes
colors ={
'TTZ' : kGreen,
'TTW' : kViolet+1,
'TTH' : kViolet+5,
'tZq' : kCyan,
'TTTT' : kCyan+2,
'WZ'  : kOrange,
'WW'  : kBlack,
'DY'  : kGray,
'ZZ'  : kViolet+3,
'tt'  : kRed,
'single t' : kYellow, 
'convs' : kOrange + 3,
'VVV' : kOrange+8,
'VH'  : kBlue - 4,
'W+Jets' : kGray+4,}

systematics = ''

Lumi = 35900

def GetName(var, chan, lev):
  return (var + '_' + chan + '_' + lev) if lev != '' else (var + '_' + chan)

"""def GetAllCh(var, lev): #For the future
  return [GetName(var,'eee',lev), GetName(var,'emm',lev), GetName(var,'mee',lev), GetName(var,'mmm',lev)]"""

