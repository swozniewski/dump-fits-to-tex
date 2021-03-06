#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ROOT

tag = sys.argv[1]
stage = sys.argv[2]

eras = ["2016", "2017", "2018"]
channels = ["em", "et", "mt", "tt"]
stages = ["stxs_stage0", "stxs_stage1p1"]
if not stage in stages:
    print "invalid stage"
    raise Exception

bkgcategories_per_channel = {
  "em" : [
    "db",
    "emb",
    "misc",
    "ss",
    "tt"
    ],
  "et" : [
    "emb",
    "ff",
    "misc",
    "zll",
    "tt"
    ],
  "mt" : [
    "emb",
    "ff",
    "misc",
    "zll",
    "tt"
    ],
  "tt" : [
    "emb",
    "ff",
    "misc"
    ]
  }

signalcategories = ["xxh"]
if stage=="stxs_stage1p1":
  signalcategories = [
    "ggh_0J_PTH_0_10",
    "ggh_0J_PTH_GT10",
    "ggh_1J_PTH0to60",
    "ggh_1J_PTH60to120",
    "ggh_1J_PTH120to200",
    "ggh_2J_PTH0to60",
    "ggh_2J_PTH60to120",
    "ggh_2J_PTH120to200",
    "ggh_vbftopo",
    "ggh_PTHGT200",
    "qqh_2J",
    "qqh_PTHGT200",
    "qqh_vbftopo_highmjj",
    "qqh_vbftopo_lowmjj"
    ]

bkgs_per_channel = {
    "em" : ["W", "EMB", "QCD", "ZL", "TTL", "VVL"],
    "et" : ["EMB", "jetFakes", "ZL", "TTL", "VVL"],
    "mt" : ["EMB", "jetFakes", "ZL", "TTL", "VVL"],
    "tt" : ["EMB", "jetFakes", "ZL", "TTL", "VVL"]
    }

signals = []
if stage=="stxs_stage1p1":
    signals += [
      "ggH_GG2H_PTH_GT200125",
      "ggH_GG2H_0J_PTH_0_10125",
      "ggH_GG2H_0J_PTH_GT10125",
      "ggH_GG2H_1J_PTH_0_60125",
      "ggH_GG2H_1J_PTH_60_120125",
      "ggH_GG2H_1J_PTH_120_200125",
      "ggH_GG2H_GE2J_MJJ_0_350_PTH_0_60125",
      "ggH_GG2H_GE2J_MJJ_0_350_PTH_60_120125",
      "ggH_GG2H_GE2J_MJJ_0_350_PTH_120_200125",
      "ggH_GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25125",
      "ggH_GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25125",
      "ggH_GG2H_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25125",
      "ggH_GG2H_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25125",
      "qqH_QQ2HQQ_0J125",
      "qqH_QQ2HQQ_1J125",
      "qqH_QQ2HQQ_GE2J_MJJ_0_60125",
      "qqH_QQ2HQQ_GE2J_MJJ_60_120125",
      "qqH_QQ2HQQ_GE2J_MJJ_120_350125",
      "qqH_QQ2HQQ_GE2J_MJJ_GT350_PTH_GT200125",
      "qqH_QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25125",
      "qqH_QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25125",
      "qqH_QQ2HQQ_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25125",
      "qqH_QQ2HQQ_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25125"]
else:
    signals += ["ggH125", "qqH125"]
signals += ["WH125", "ZH125", "ttH125", "ggHWW125", "qqHWW125", "WHWW125", "ZHWW125"]

yields = {}
for era in eras:
    yields[era] = {}
    for channel in channels:
        yields[era][channel] = {}
        infile = ROOT.TFile("output/shapes/%s-%s-%s-synced-ML.root"%(era,tag,channel), "READ")
        for cat in (bkgcategories_per_channel[channel] + signalcategories):
            yields[era][channel][cat] = {}
            for process in (bkgs_per_channel[channel] + signals):
                shape = infile.Get("%s_%s/%s"%(channel,cat,process))
                yields[era][channel][cat][process] = shape.Integral()
            yields[era][channel][cat]["sum"] = sum(yields[era][channel][cat].values())
        infile.Close()

clustering = {
    "VH125" : ["WH125", "ZH125"],
    "HWW" : ["ggHWW125", "qqHWW125", "WHWW125", "ZHWW125"],
    "ggH_GG2H_GE2J_MJJ_GT350125" : ["ggH_GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25125", "ggH_GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25125", "ggH_GG2H_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25125", "ggH_GG2H_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25125"],
    "qqH_QQ2HQQ_LE1J125" : ["qqH_QQ2HQQ_0J125", "qqH_QQ2HQQ_1J125"],
    "qqH_QQ2HQQ_GE2J_MJJ_0_350125" : ["qqH_QQ2HQQ_GE2J_MJJ_0_60125", "qqH_QQ2HQQ_GE2J_MJJ_60_120125", "qqH_QQ2HQQ_GE2J_MJJ_120_350125"],
    "qqH_GE2J_MJJ_350_700_PTH_0_200125" : ["qqH_QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25125", "qqH_QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25125"],
    "qqH_GE2J_MJJ_GT700_PTH_0_200125" : ["qqH_QQ2HQQ_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25125", "qqH_QQ2HQQ_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25125"],
    }

for proc, procs in clustering.items():
    for era in eras:
        for channel in channels:
            for cat in (bkgcategories_per_channel[channel] + signalcategories):
                content = 0.0
                registered = False
                for subproc in procs:
                    if subproc in yields[era][channel][cat]:
                        content += yields[era][channel][cat].pop(subproc)
                        for i in range(len(signals)):
                            if(signals[i]==subproc):
                                if not registered:
                                    signals[i] = proc
                                    registered = True
                                    break
                                else:
                                    del signals[i]
                                    break
                yields[era][channel][cat][proc] = content

channellables = {
    "em" : "e$\mu$",
    "et" : "e$\\tau_\mathrm{h}$",
    "mt" : "$\mu\\tau_\mathrm{h}$",
    "tt" : "$\\tau_\mathrm{h}\\tau_\mathrm{h}$"
        }

processlabels = {
    "ggH125" : 'ggH',
    "qqH125" : 'VBF',
    "VH125" : 'VH (lep)',
    "ttH125" : 'ttH',
    "HWW" : "HWW",
    "EMB" : '$\\mu\\rightarrow\\tau$ embedded',
    "ZL" : 'Z$\\rightarrow ll$',
    "TTL" : '$\mathrm{t}\\bar{\mathrm{t}}$',
    "W" : 'W+jets',
    "VVL" : 'Diboson',
    "QCD" : 'QCD multijet',
    "jetFakes" : 'Jet$\\rightarrow\\tau_{\mathrm{h}}$',
    "ggH_GG2H_PTH_GT200125" : 'ggH $p\mathrm{^H_T}\ge 200$',
    "ggH_GG2H_0J125" : 'ggH 0 Jet $p\mathrm{^H_T}[0,200]$',
    "ggH_GG2H_0J_PTH_0_10125" : 'ggH 0 Jet $p\mathrm{^H_T}[0,10]$',
    "ggH_GG2H_0J_PTH_GT10125" : 'ggH 0 Jet $p\mathrm{^H_T}[10,200]$',
    "ggH_GG2H_1J_PTH_0_60125" : 'ggH 1 Jet $p\mathrm{^H_T}[0,60]$',
    "ggH_GG2H_1J_PTH_60_120125" : 'ggH 1 Jet $p\mathrm{^H_T}[60,120]$',
    "ggH_GG2H_1J_PTH_0_120125" : 'ggH 1 Jet $p\mathrm{^H_T}[0,120]$',
    "ggH_GG2H_1J_PTH_120_200125" : 'ggH 1 Jet $p\mathrm{^H_T}[120,200]$',
    "ggH_GG2H_GE2J_MJJ_0_350_PTH_0_60125" : 'ggH $\ge$2 Jet $m_{jj}[0,350]$ $p\mathrm{^H_T}[0,60]$',
    "ggH_GG2H_GE2J_MJJ_0_350_PTH_60_120125" : 'ggH $\ge$2 Jet $m_{jj}[0,350]$ $p\mathrm{^H_T}[60,120]$',
    "ggH_GG2H_GE2J_MJJ_0_350_PTH_120_200125" : 'ggH $\ge$2 Jet $m_{jj}[0,350]$ $p\mathrm{^H_T}[120,200]$',
    "ggH_GG2H_GE2J_MJJ_0_350125" : 'ggH $\ge$2 Jet $m_{jj}[0,350]$ $p\mathrm{^H_T}[0,200]$',
    "ggH_GG2H_GE2J_MJJ_GT350125" : 'ggH $m_{jj}\ge 350$',
    "qqH_QQ2HQQ_LE1J125" : 'qqH $\le$1 Jet',
    "qqH_QQ2HQQ_GE2J_MJJ_0_350125" : 'qqH $\ge$2 Jet $m_{jj}[0,350]$',
    "qqH_QQ2HQQ_GE2J_MJJ_GT350_PTH_GT200125" : 'qqH $\ge$2 Jet $m_{jj}\ge 350$ $p\mathrm{^H_T}\ge 200$',
    "xxH_GE2J_MJJ_350_700_PTH_0_200125" : 'ggH/qqH $\ge$2 Jet $m_{jj}[350,700]$ $p\mathrm{^H_T}[0,200]$',
    "xxH_GE2J_MJJ_GT700_PTH_0_200125" : 'ggH/qqH $\ge$2 Jet $m_{jj}\ge 700$ $p\mathrm{^H_T}[0,200]$',
    "qqH_GE2J_MJJ_350_700_PTH_0_200125" : 'qqH $\ge$2 Jet $m_{jj}[350,700]$ $p\mathrm{^H_T}[0,200]$',
    "qqH_GE2J_MJJ_GT700_PTH_0_200125" : 'qqH $\ge$2 Jet $m_{jj}\ge 700$ $p\mathrm{^H_T}[0,200]$'
    }

#one table per channel
#|process|      2016       |      2017       |      2018       |
#|       |n_events|fraction|n_events|fraction|n_events|fraction|

f=open("datacard_yields.tex", "w")
f.write("\documentclass{article}\n\usepackage[hscale=0.7,vscale=0.8]{geometry}\n\usepackage{mathtools}\n\\begin{document}\n")
ind = False
for channel in channels:
    if stage!="stxs_stage1p1":
        f.write("\\begin{table}[!h]\n\\begin{center}{\\tiny\n\\begin{tabular}{cc|cc|cc|cc}\n")
        f.write("category & process & \multicolumn{2}{c}{2016} & \multicolumn{2}{c}{2017} & \multicolumn{2}{c}{2018}\\\\\n")
        f.write("& & \\# events & fraction & \\# events & fraction & \\# events & fraction\\\\\n\hline\n")
    for cat in (signalcategories+bkgcategories_per_channel[channel]):
        if stage=="stxs_stage1p1":
            f.write("\\begin{table}[!h]\n\\begin{center}{\\tiny\n\\begin{tabular}{cc|cc|cc|cc}\n")
            f.write("category & process & \multicolumn{2}{c}{2016} & \multicolumn{2}{c}{2017} & \multicolumn{2}{c}{2018}\\\\\n")
            f.write("& & \\# events & fraction & \\# events & fraction & \\# events & fraction\\\\\n\hline\n")
        f.write("%s & & & & & & &\\\\\n"%(cat.replace("_","\\_")))
        for process in (signals + bkgs_per_channel[channel]):
            valuesstring = " & ".join("{:.2f} & {:.3f}\%".format(yields[era][channel][cat][process], yields[era][channel][cat][process]/yields[era][channel][cat]["sum"]*100.0) for era in eras)
            f.write("& %s & %s\\\\\n"%(processlabels[process], valuesstring))
        f.write("\hline\n")
        if stage=="stxs_stage1p1":
            f.write("\\end{tabular}\n} % end tiny\n\\end{center}\n\caption{Datacard event contents in the "+channellables[channel]+" channel for the "+("stage1 training" if stage=="stage1p1" else "stage0 training")+", "+cat.replace("_","\\_")+" category}\n\\end{table}\n%s"%("\\clearpage\n" if ind else ""))
            ind = not ind
    if stage!="stxs_stage1p1":
        f.write("\\end{tabular}\n} % end tiny\n\\end{center}\n\caption{Datacard event contents in the "+channellables[channel]+" channel for the "+("stage1 training" if stage=="stage1p1" else "stage0 training")+"}\n\\end{table}\n\\clearpage\n")
f.write("\\end{document}")
f.close()
