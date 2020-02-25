import os, sys
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
sys.path.append(basepath)
from framework.functions import GetLumi
from plotter.TopHistoReader import TopHistoReader, HistoManager
from plotter.Plotter import Stack
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow

### Input and output
#path = '../temp5TeV/sep17/'
path = '../tempWZsamesign/'
outpath = 'plotsWZsamesign/'

### Definition of the processes
processDic = {
'WZ'  : 'WZTo3LNU_NNPDF30_TuneCP5_5p20TeV',
'VV'  : 'WWTo2L2Nu_NNPDF31_TuneCP5_5p02TeV,ZZTo2L2Nu_5p02TeV,ZZTo4L_5p02TeV',
'DY'  : 'DYJetsToLL_MLL_50_TuneCP5_5020GeV_amcatnloFXFX,DYJetsToLL_M_10to50_TuneCP5_5020GeV_amcatnloFXFX',
'WJets': 'W0JetsToLNu_TuneCP5_5020GeV_MLM,W1JetsToLNu_TuneCP5_5020GeV_MLM,W2JetsToLNu_TuneCP5_5020GeV_MLM,W3JetsToLNu_TuneCP5_5020GeV_MLM',
'top'  : 'TT_TuneCP5_5p02TeV,tW_5f_noFullHad_TuneCP5_5p02TeV,tbarW_5f_noFullHad_TuneCP5_5p02TeV'}#,#,tW_noFullHad,tbarW_noFullHad'}
#'data': 'HighEGJet, SingleMuon'}##SingleMuon
processes = ['VV', 'DY', 'WJets', 'top', 'WZ']

process = processDic
### Definition of colors for the processes
colors ={
'WZ'  : kYellow-4,
'VV'  : kGray+2,
'DY'  : kAzure-8,
'WJets': kGreen+1,
'top' : kRed+1,}
#'data': 1}

systematics = 'MuonEff, ElecEff'#, TrigEff, Prefire, JES, JER, ISR, FSR'

Lumi = 296.1 #294.24 #296.1

def GetName(var, chan, lev):
  return (var + '_' + chan + '_' + lev) if lev != '' else (var + '_' + chan)

def GetAllCh(var, lev):
  return [GetName(var,'ee',lev), GetName(var,'me',lev), GetName(var,'mm',lev)]

