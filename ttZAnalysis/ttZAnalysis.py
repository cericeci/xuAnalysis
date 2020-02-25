import os,sys
sys.path.append(os.path.abspath(__file__).rsplit("/xuAnalysis/",1)[0]+"/xuAnalysis/")
from framework.analysis import analysis
import framework.functions as functions
from ROOT import TLorentzVector
from modules.PrefireCorr import PrefCorr


# When needed (i.e. multiple loops) add extra entries to produce syst-varied histograms

# Can be used to define "parallel" multiple channels (i.e. separate by lepton flavor, jet multiplicity, etc.)
class ch():
  all  = 0
chan = {ch.all:'all'}

# Used to define multiple level cuts
class lev():
  lep3  = 0 #Has 3 leptons, all other cuts inherit from these
  lep3T = 1 #Has 3 tight leptons
  jet3  = 2 #3 tight leptons + 3 jets
  tag2  = 3 #3 tight leptons + 3 jets + 2 tags

level   = {lev.lep3:'3lep', lev.lep3T:'3leptight', lev.jet3:'3jet', lev.tag2:'2tag'}

class systematic():
  nom       = -1 # Nominal

systlabel = {systematic.nom:''}

class ttZAnalysis(analysis):
  def init(self):
    # This is called once per sample at the start of processing 
    self.createHistograms()
    # Then load any needed things (i.e. SFs, pile-up, btag, etc.)
    # Load trigger prefiring correctors
    self.prefireCorrector = PrefCorr(jetroot="L1prefiring_jetpt_2016BtoH.root", jetmapname="L1prefiring_jetpt_2016BtoH", photonroot="L1prefiring_photonpt_2016BtoH.root", photonmapname="L1prefiring_photonpt_2016BtoH", verbose = False)
    # Load lepton SF histograms
    # To ADD
    # Load btag SF correctors
    # To ADD

  def insideLoop(self,t):
    self.isData = not(getattr(t,"xsec")) # Only MC has xsec variable and we need this flag for later
    # This is called once per event. To speed things up one might want to cut early in some variables
    self.resetObjects()
    self.selectLeptons(t)
    # Selection here to make the thing go quicker but can be put further down
    if (len(self.selLeptons) < 3): return False
    self.selectTrigger(t)
    if not(self.passTrigger): return False
    self.selectJets(t)
    self.selectMET(t)
    self.applyCorrections(t)
    # All events must pass trigger cuts

    # Minimal lepton pT selection to match trigger
    if not(self.selLeptons[0].Pt() >= 25 and self.selLeptons[1].Pt() >= 20): return False
    # Filling the histograms


    for syst in systlabel:
      # For all systematic variations fill the histograms
      if len(self.selLeptons) >= 3: 
        self.fillHistograms(chan[ch.all], level[lev.lep3], systlabel[systematic.nom])
        self.GetHisto('Yields',   chan[ch.all], '', systlabel[systematic.nom]).Fill(level[lev.lep3], self.weight)

      if len(self.selLeptons) >= 3 and self.selLeptons[0].passTightID and self.selLeptons[1].passTightID and self.selLeptons[2].passTightID: 
        self.fillHistograms(chan[ch.all], level[lev.lep3T], systlabel[systematic.nom])
        self.GetHisto('Yields',   chan[ch.all], '', systlabel[systematic.nom]).Fill(level[lev.lep3T], self.weight)

      if len(self.selLeptons) >= 3 and self.selLeptons[0].passTightID and self.selLeptons[1].passTightID and self.selLeptons[2].passTightID and self.nJets >= 3: 
        self.fillHistograms(chan[ch.all], level[lev.jet3], systlabel[systematic.nom])
        self.GetHisto('Yields',   chan[ch.all], '', systlabel[systematic.nom]).Fill(level[lev.jet3], self.weight)

      if len(self.selLeptons) >= 3 and self.selLeptons[0].passTightID and self.selLeptons[1].passTightID and self.selLeptons[2].passTightID and self.nJets >= 3 and self.nBtag >= 2: 
        self.fillHistograms(chan[ch.all], level[lev.tag2], systlabel[systematic.nom])
        self.GetHisto('Yields',   chan[ch.all], '', systlabel[systematic.nom]).Fill(level[lev.tag2], self.weight)

  def resetObjects(self):
    self.selLeptos = []
    self.selJets   = []
    self.pmet = TLorentzVector()

  ##################################################
  ## Selection - Build lepton and jet collections ##
  ##################################################

  def selectLeptons(self,t):    
    # Basic lepton selection
    self.selLeptons = []
    for ilep in range(t.nLepGood):
      passTightID = True
      if abs(t.LepGood_pdgId[ilep]) == 13: #Loose Muon ID
        # Minimal selection cuts
        if t.LepGood_miniPFRelIso_all[ilep] > 0.4: continue
        if t.LepGood_dz[ilep] > 0.1: continue
        if t.LepGood_dxy[ilep] > 0.05: continue
        if t.LepGood_sip3d[ilep] > 8: continue
        if t.LepGood_mediumId[ilep] == 0: continue
        if t.LepGood_pt[ilep] < 10: continue
        if abs(t.LepGood_eta[ilep]) > 2.4: continue
        # Now the true tighter cuts
        if not(t.LepGood_mvaTTH[ilep] > 0.4): passTightID = False

      if abs(t.LepGood_pdgId[ilep]) == 11: #Loose Electron ID
        # Minimal selection cuts
        if t.LepGood_miniPFRelIso_all[ilep] > 0.4: continue
        if t.LepGood_dz[ilep] > 0.1: continue
        if t.LepGood_dxy[ilep] > 0.05: continue
        if t.LepGood_sip3d[ilep] > 8: continue
        if t.LepGood_mvaFall17V2noIso_WPL[ilep] == 0: continue
        if t.LepGood_lostHits[ilep] == 0: continue
        if t.LepGood_pt[ilep] < 10: continue
        if abs(t.LepGood_eta[ilep]) > 2.5: continue
        # Those are included to be resilient against hlt effects
        if (t.LepGood_hoe[ilep] >= 0.10): continue   
        if (t.LepGood_eInvMinusPInv[ilep] <= -0.04): continue      
        if (t.LepGood_sieie[ilep] >= 0.011+0.019*(abs(t.LepGood_eta[ilep])>1.479)): continue         
        # Now the true tighter cuts
        if not(t.LepGood_convVeto[ilep]): passTightID = False
        if not(t.LepGood_mvaTTH[ilep] > 0.4): passTightID = False

      v = TLorentzVector()
      v.SetPtEtaPhiM(t.LepGood_pt[ilep], t.LepGood_eta[ilep], t.LepGood_phi[ilep], t.LepGood_mass[ilep])
      self.selLeptons.append(functions.lepton(v, t.LepGood_charge[ilep], t.LepGood_pdgId[ilep], t.LepGood_genPartFlav[ilep] if not(self.isData) else "\0", passTightID=passTightID))

  def selectJets(self,t):
    # Basic jet selection and cleaning
    for i in range(t.nJet):
      p = TLorentzVector()
      p.SetPtEtaPhiM(t.Jet_pt_nom[i], t.Jet_eta[i], t.Jet_phi[i], t.Jet_mass[i])
      # All possible b tagging discriminants
      csv = t.Jet_btagCSVV2[i]; deepcsv = t.Jet_btagDeepB[i]; deepflav = t.Jet_btagDeepFlavB[i]
      jid = t.Jet_jetId[i]
      flav = t.Jet_hadronFlavour[i] if not self.isData else -999999;
      j = functions.jet(p, csv, flav, jid, deepcsv, deepflav)
      # DeepCSV WPs: 0.2217, 0.6321, 0.8953
      ### Medium WP b tag
      if deepcsv >= 0.6321: j.SetBtag() 
      # Then do jet-lepton cleaning
      if not jid > 1: continue
      if abs(p.Eta()) > 2.4: continue
      if not j.IsClean(self.selLeptons, 0.4): continue
      if p.Pt()      >= 25: self.selJets.append(j)
    self.selJets = functions.SortByPt(self.selJets)
    self.nJets = len(self.selJets)
    self.nBtag = functions.GetNBtags(self.selJets)

  def selectMET(self,t):
    # Basic MET selection
    self.pmet.SetPtEtaPhiM(t.MET_pt_nom, 0, t.MET_phi_nom, 0)

  def selectTrigger(self,t):
    self.passTrigger = False
    if not(self.isData):
      self.passTrigger = self.selectTriggerOverlap([
                    ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",0,1000000],
                    ["HLT_Ele27_WPTight_Gsf",0,1000000],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",0,1000000],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",0,1000000],
                    ["HLT_IsoMu24",0,1000000],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",0,1000000],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",0,1000000],
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",0,1000000],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL",0,1000000],
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",0,1000000],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ",0,1000000]
                    ],[],t)
    else:
      if "DoubleMuon" in self.sampleName:
        self.passTrigger = self.selectTriggerOverlap([
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",280919,1000000],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",280919,1000000],
                    ],[],t)

      if "MuonEG" in self.sampleName:
        self.passTrigger = self.selectTriggerOverlap([
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",0,280919],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL",0,280919],
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",280919,1000000],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ",280919,1000000]
                    ],[
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",280919,1000000],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",280919,1000000],
                    ],t)

      if "DoubleEG" in self.sampleName:
        self.passTrigger = self.selectTriggerOverlap([
                    ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",0,1000000],
                    ],[
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",0,280919],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL",0,280919],
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",280919,1000000],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ",280919,1000000],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",280919,1000000],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",280919,1000000],
                    ],t)

      if "SingleMuon" in self.sampleName:
        self.passTrigger = self.selectTriggerOverlap([
                    ["HLT_IsoMu24",0,1000000],
                    ],[
                    ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",0,1000000],
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",0,280919],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL",0,280919],
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",280919,1000000],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",280919,1000000],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",280919,1000000],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ",280919,1000000]
                    ],t)

      if "SingleElectron" in self.sampleName:
        self.passTrigger = self.selectTriggerOverlap([
                    ["HLT_Ele27_WPTight_Gsf",0,1000000],
                    ],[
                    ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",0,1000000],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",0,280919],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",0,280919],
                    ["HLT_IsoMu24",0,1000000],
                    ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",280919,1000000],
                    ["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",280919,1000000],
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",0,280919],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL",0,280919],
                    ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",280919,1000000],
                    ["HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ",280919,1000000]
                    ],t)

  def selectTriggerOverlap(self,selections,vetos,t):
    # Set the pass trigger flag, taking into account trigger vetoes between datasets
    good = False
    for path in vetos:
      if not(hasattr(t, path[0])): continue
      if getattr(t,path[0]) and path[1] <= t.run and  path[2] >= t.run:
        return False

    for p in selections:
      if not(hasattr(t, p[0])): continue
      if getattr(t,p[0]) and p[1] <= t.run and  p[2] >= t.run:
        return True


  #######################
  ## Weighters and SFs ##
  #######################

  def applyCorrections(self,t):
    # Produce total event weights taking into account all per event corrections
    self.puWeight  = t.puWeight
    self.triggerSF = 1. # triggerSF ~ 1 in trilepton final states
    self.lepSF = 1.     # 1 for now
    self.btagSF = 1.    # 1 for now
    self.weight = self.EventWeight*self.puWeight*self.triggerSF*self.lepSF*self.btagSF
    #print self.EventWeight,self.puWeight,self.triggerSF,self.lepSF,self.btagSF,self.weight

  ########################
  ## Histogram handling ##
  ########################
  def createHistograms(self):
    # A brief example on how to create histograms
    for key_chan in chan:
      # First loop in channels
      ichan = chan[key_chan]
      for key_syst in systlabel.keys():
        isyst = systlabel[key_syst]
        self.NewHisto('Yields',   ichan, '', isyst, 4, -0.5, 4.5)
        for key_level in level:
          # Then loop over cut levels
          ilevel = level[key_level]

          # Last loop over systematics
          # As an example pT of the leading lepton (20 bins)
          self.NewHisto('Lep1Pt', ichan,ilevel,isyst, 20, 20, 220)


  def fillHistograms(self, ich, ilev, isys):
    self.GetHisto("Lep1Pt", ich, ilev, isys).Fill(self.selLeptons[0].Pt(), self.weight)

  #############
  ## Helpers ##
  #############
  def NewHisto(self, var, chan, level, syst, nbins, bin0, binN):
    # Used to create the histos following a structure variable_channel_level_systematic
    self.CreateTH1F(self.GetName(var, chan, level, syst), "", nbins, bin0, binN)
    self.obj[self.GetName(var, chan, level, syst)].Sumw2()

  def GetHisto(self, var, chan, level = '', syst = ''):
    # Get a given histo using the tthisto structure 
    return self.obj[self.GetName(var, chan, level, syst)]

  def GetName(self, var, chan, level = '', syst = ''):
    # Builds the name for a histo given the current channel, level and systematic
    return var + ('_' + chan if chan != '' else '') + ('_' + level if level != '' else '') + ('_'+syst if syst != '' else '')
    
