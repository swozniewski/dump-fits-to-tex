#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

tag = sys.argv[1] if len(sys.argv)>=2 else "default"
path_to_logs = sys.argv[2] if len(sys.argv)==3 else "output/log"
print "Searching tag '" + tag + "' in " + path_to_logs

eras = ["2016", "2017", "2018", "combined"]
channels = ["em", "et", "mt", "tt", "cmb"]
stages = ["inclusive", "stxs_stage0", "stxs_stage1p1"]

POIdict = {
    "inclusive" : ["r"],
    "stxs_stage0" : ["r_ggH", "r_qqH"],
    "stxs_stage1p1" : ["r_ggH_GG2H_0J",
                       "r_ggH_GG2H_PTH_GT200",
                       "r_ggH_GG2H_1J_PTH_0_120",
                       "r_ggH_GG2H_1J_PTH_120_200",
                       "r_ggH_GG2H_GE2J_MJJ_0_350",
                       "r_xxH_QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200",
                       "r_xxH_QQ2HQQ_GE2J_MJJ_GT700_PTH_0_200",
                       "r_qqH_QQ2HQQ_LE1J",
                       "r_qqH_QQ2HQQ_GE2J_MJJ_0_350",
                       "r_qqH_QQ2HQQ_GE2J_MJJ_GT350_PTH_GT200"]
    }
    

fitresults = {}

#read fit logs
for era in eras:
    fitresults[era] = {}
    for channel in channels:
        fitresults[era][channel] = {}
        for stage in stages:
            if os.path.isfile(os.path.join(path_to_logs, "signal-strength-%s-%s-%s-%s.log"%(era, tag, channel, stage))):
                with open(os.path.join(path_to_logs, "signal-strength-%s-%s-%s-%s.log"%(era, tag, channel, stage))) as infile:
                    lines=infile.read()
                lines=lines.split("\n")
                for line in lines:
                    keys = [key for key in line.split() if key!=""]
                    if len(keys)>4 and keys[0] in POIdict[stage]:
                        nom = float(keys[2])
                        down = float(keys[3].split("/")[0])
                        up = float(keys[3].split("/")[1])
                        fitresults[era][channel][keys[0]]=["{:.2f}".format(nom), "+{:.2f}".format(up), "{:.2f}".format(down)]
            else:
                for POI in POIdict[stage]:
                    fitresults[era][channel][POI]=["", "", ""]
            #check completeness
            for POI in POIdict[stage]:
                if not POI in fitresults[era][channel]:
                    print "WARNING %s fit seems to be corrupt!"%POI
                    fitresults[era][channel][POI]=["", "", ""]

#write latex file
f=open("fit_results.tex", "w")
f.write("\documentclass{article}\n\usepackage{mathtools}\n\\begin{document}\n\\begin{table}[!h]\n\\begin{center}{\\footnotesize\n\\begin{tabular}{c|ccccc}\n")
for era in eras:
    f.write("\multicolumn{6}{c}{%s}\\\\\n\hline\n& e$\mu$ & e$\\tau_\mathrm{h}$ & $\mu\\tau_\mathrm{h}$ & $\\tau_\mathrm{h}\\tau_\mathrm{h}$ & combined\\\\\n\hline\n"%era.replace("combined", "2016 \& 2017 \& 2018"))
    f.write("$gg\\rightarrow H$")
    for channel in channels:
        f.write(" & $%s\\substack{%s \\\\ %s}$"%(fitresults[era][channel]["r_ggH"][0], fitresults[era][channel]["r_ggH"][1], fitresults[era][channel]["r_ggH"][2]))
    f.write("\\\\\n$qq\\rightarrow H$")
    for channel in channels:
        f.write(" & $%s\\substack{%s \\\\ %s}$"%(fitresults[era][channel]["r_qqH"][0], fitresults[era][channel]["r_qqH"][1], fitresults[era][channel]["r_qqH"][2]))
    f.write("\\\\\ninclusive        ")
    for channel in channels:
        f.write(" & $%s\\substack{%s \\\\ %s}$"%(fitresults[era][channel]["r"][0], fitresults[era][channel]["r"][1], fitresults[era][channel]["r"][2]))
    f.write("\\\\\n\hline\n\multicolumn{6}{c}{ }\\\\\n")
f.write("\\end{tabular}\n} % end footnotesize\n\\end{center}\n\\end{table}\n")
for era in eras:
    f.write("\\begin{table}[!h]\n\\begin{center}{\\footnotesize\n\\begin{tabular}{|l|r|}\n\\hline\nSTXS stage 1 category & signal strength \\\\\n\\hline\n")
    
    f.write("VBF topology $350\,\mathrm{GeV}<m_{jj}<700\,\mathrm{GeV}$                                      & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_xxH_QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200"][0], fitresults[era][channel]["r_xxH_QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200"][1], fitresults[era][channel]["r_xxH_QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200"][2]))
    
    f.write("VBF topology $m_{jj}>700\,\mathrm{GeV}$                                                        & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_xxH_QQ2HQQ_GE2J_MJJ_GT700_PTH_0_200"][0], fitresults[era][channel]["r_xxH_QQ2HQQ_GE2J_MJJ_GT700_PTH_0_200"][1], fitresults[era][channel]["r_xxH_QQ2HQQ_GE2J_MJJ_GT700_PTH_0_200"][2]))
    
    f.write("\hline\nVBF:&\\\\\n")
    
    f.write("0, 1 jets                                                                                      & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_qqH_QQ2HQQ_LE1J"][0], fitresults[era][channel]["r_qqH_QQ2HQQ_LE1J"][1], fitresults[era][channel]["r_qqH_QQ2HQQ_LE1J"][2]))
    
    f.write("$m_{jj}<350\,\mathrm{GeV}$                                                                     & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_qqH_QQ2HQQ_GE2J_MJJ_0_350"][0], fitresults[era][channel]["r_qqH_QQ2HQQ_GE2J_MJJ_0_350"][1], fitresults[era][channel]["r_qqH_QQ2HQQ_GE2J_MJJ_0_350"][2]))
    
    f.write("$p_T^{H}>200\,\mathrm{GeV}$                                                                    & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_qqH_QQ2HQQ_GE2J_MJJ_GT350_PTH_GT200"][0], fitresults[era][channel]["r_qqH_QQ2HQQ_GE2J_MJJ_GT350_PTH_GT200"][1], fitresults[era][channel]["r_qqH_QQ2HQQ_GE2J_MJJ_GT350_PTH_GT200"][2]))
    
    f.write("\hline\nGluon fusion:&\\\\\n")
    
    f.write("0 jets, $p_T^{H}\in[0,\,200]\,\mathrm{GeV}$                                                    & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_ggH_GG2H_0J"][0], fitresults[era][channel]["r_ggH_GG2H_0J"][1], fitresults[era][channel]["r_ggH_GG2H_0J"][2]))
    
    f.write("1 jet, $p_T^{H}\in[0,\,120]\,\mathrm{GeV}$                                                     & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_ggH_GG2H_1J_PTH_0_120"][0], fitresults[era][channel]["r_ggH_GG2H_1J_PTH_0_120"][1], fitresults[era][channel]["r_ggH_GG2H_1J_PTH_0_120"][2]))
    
    f.write("1 jet, $p_T^{H}\in[120,\,200]\,\mathrm{GeV}$                                                   & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_ggH_GG2H_1J_PTH_120_200"][0], fitresults[era][channel]["r_ggH_GG2H_1J_PTH_120_200"][1], fitresults[era][channel]["r_ggH_GG2H_1J_PTH_120_200"][2]))
    
    f.write("$\ge2$ jets, $p_T^{H}\in[0,\,200]\,\mathrm{GeV}$, $m_{jj}<350\,\mathrm{GeV}$                   & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_ggH_GG2H_GE2J_MJJ_0_350"][0], fitresults[era][channel]["r_ggH_GG2H_GE2J_MJJ_0_350"][1], fitresults[era][channel]["r_ggH_GG2H_GE2J_MJJ_0_350"][2]))
    
    f.write("$p_T^{H}>\,200\,\mathrm{GeV}$                                                                  & $")
    f.write("%s\\substack{%s \\\\ %s}$\\\\\n"%(fitresults[era][channel]["r_ggH_GG2H_PTH_GT200"][0], fitresults[era][channel]["r_ggH_GG2H_PTH_GT200"][1], fitresults[era][channel]["r_ggH_GG2H_PTH_GT200"][2]))
    
    f.write("\hline\n\\end{tabular}\n} % end footnotesize\n\\end{center}\n\caption{Signal strength per STXS stage 1 category, combining the measurements of "+era.replace("combined", "2016, 2017, 2018")+" in all channels.}\n\\end{table}\n")
f.write("\\end{document}")
f.close()