from __future__ import division
import  matplotlib.pyplot as plt

import numpy as np
import random
import scipy as sc
from scipy import stats

import os
import sys
from scipy.stats.distributions import t

import statsmodels.stats.api as sms
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import summary_table

import itertools as it

import pandas as pd
from math import log10
import linecache

mydir = os.path.expanduser("~/GitHub/MicrobialScaling/")
mydir2 = os.path.expanduser("~/")

sys.path.append(mydir2 + "GitHub/DiversityTools/metrics")
import metrics as mets


def modelcomparison():

    OUT = open(mydir + 'output/model_comparison.txt','w+')

    datasets = []
    GoodNames = ['MGRAST', 'HMP', 'EMPclosed', 'BBS', 'CBC', 'MCDB', 'GENTRY', 'FIA']

    for name in os.listdir(mydir +'data/micro'):
        if name in GoodNames: pass
        else: continue

        #path = mydir+'data/micro/'+name+'/'+name+'-SADMetricData_NoMicrobe1s.txt'
        path = mydir+'data/micro/'+name+'/'+name+'-SADMetricData.txt'

        num_lines = sum(1 for line in open(path))
        datasets.append([name, 'micro', num_lines])
        print>>OUT, name, num_lines

    for name in os.listdir(mydir +'data/macro'):
        if name in GoodNames: pass
        else: continue

        #path = mydir+'data/macro/'+name+'/'+name+'-SADMetricData_NoMicrobe1s.txt'
        path = mydir+'data/macro/'+name+'/'+name+'-SADMetricData.txt'

        num_lines = sum(1 for line in open(path))
        datasets.append([name, 'macro', num_lines])
        print>>OUT, name, num_lines

    FS_rarity = []
    FS_dom = []
    FS_ev = []
    FS_S = []
    FS_Nlist = []

    IN = mydir+'/output/partitions.txt'
    num_lines = sum(1 for line in open(IN))

    for line in open(IN):
        rad = eval(line)

        skew = stats.skew(rad)
        # log-modulo transformation of skewnness
        lms = np.log10(np.abs(skew) + 1)
        if skew < 0: lms = lms * -1
        FS_rarity.append(lms)

        FS_S.append(np.log10(len(rad)))
        FS_Nlist.append(np.log10(sum(rad)))
        FS_dom.append(np.log10(max(rad)))
        ESimp = mets.e_simpson(rad)
        FS_ev.append(np.log10(ESimp))

    metrics = ['Rarity', 'Dominance', 'Evenness', 'Richness']

    for index, i in enumerate(metrics):

        #metric = i
        #fs = 10 # font size used across figures

        loglogR2s, linlogR2s, linearR2s, loglinR2s = [[],[],[],[]]
        loglogAICs, linlogAICs, linearAICs, loglinAICs = [[],[],[],[]]
        loglogBICs, linlogBICs, linearBICs, loglinBICs = [[],[],[],[]]

        metlist = []
        if index == 0: metlist = list(FS_rarity)
        elif index == 1: metlist = list(FS_dom)
        elif index == 2: metlist = list(FS_ev)
        elif index == 3: metlist = list(FS_S)

        # Multiple regression
        d = pd.DataFrame({'N': list(FS_Nlist)})
        d['y'] = list(metlist)
        loglog = smf.ols('y ~ N', d).fit()

        print>>OUT,'\n', 'results', 'r-square', 'aic', 'bic'

        print 'FS log-log:', round(loglog.rsquared,3), round(loglog.aic,3), round(loglog.bic, 3)
        print>>OUT,'FS log-log', round(loglog.rsquared,3), round(loglog.aic,3), round(loglog.bic, 3)

        # Multiple regression
        xlist = 10**np.array(FS_Nlist)
        d = pd.DataFrame({'N': list(xlist)})
        d['y'] = list(metlist)
        loglin = smf.ols('y ~ N', d).fit()

        print 'FS log-lin:', round(loglin.rsquared,3), round(loglin.aic,3), round(loglin.bic,3)
        print>>OUT, 'FS log-lin', round(loglin.rsquared,3), round(loglin.aic,3), round(loglin.bic,3)

        # Multiple regression
        ylist = 10**np.array(metlist)
        d = pd.DataFrame({'N': list(FS_Nlist)})
        d['y'] = list(ylist)
        linlog = smf.ols('y ~ N', d).fit()

        print 'FS lin-log:', round(linlog.rsquared, 3), round(linlog.aic,3), round(linlog.bic,3)
        print>>OUT,'FS lin-log', round(linlog.rsquared, 3), round(linlog.aic,3), round(linlog.bic,3)

        # Multiple regression
        ylist = 10**np.array(metlist)
        xlist = 10**np.array(FS_Nlist)
        d = pd.DataFrame({'N': list(xlist)})
        d['y'] = list(ylist)
        linear = smf.ols('y ~ N', d).fit()

        print 'FS linear:',  round(linear.rsquared,3), round(linear.aic,3), round(linear.bic,3),'\n'
        print>>OUT, 'FS linear',  round(linear.rsquared,3), round(linear.aic,3), round(linear.bic,3),'\n'

        Nlist, Slist, Evarlist, ESimplist, klist, radDATA, BPlist, NmaxList, rareSkews, KindList, StdList = [[], [], [], [], [], [], [], [], [], [], []]

        if index == 0: metlist = list(rareSkews)
        elif index == 1: metlist = list(NmaxList)
        elif index == 2: metlist = list(ESimplist)
        elif index == 3: metlist = list(Slist)

        its = 1000
        for n in range(its):

            Nlist, Slist, Evarlist, ESimplist, klist, radDATA, BPlist, NmaxList, rareSkews, KindList, StdList = [[], [], [], [], [], [], [], [], [], [], []]

            numMac = 0
            numMic = 0
            radDATA = []

            for dataset in datasets:

                name, kind, numlines = dataset
                lines = []
                if name == 'EMPclosed' or name == 'EMPopen':
                    lines = np.random.choice(range(1, numlines+1), 166, replace=True)
                elif kind == 'micro': lines = np.random.choice(range(1, numlines+1), 167, replace=True)
                else: lines = np.random.choice(range(1, numlines+1), 100, replace=True)

                #path = mydir+'data/'+kind+'/'+name+'/'+name+'-SADMetricData_NoMicrobe1s.txt'
                path = mydir+'data/'+kind+'/'+name+'/'+name+'-SADMetricData.txt'

                for line in lines:
                    data = linecache.getline(path, line)
                    radDATA.append(data)

            for data in radDATA:

                data = data.split()
                name, kind, N, S, Var, Evar, ESimp, EQ, O, ENee, EPielou, EHeip, BP, SimpDom, Nmax, McN, skew, logskew, chao1, ace, jknife1, jknife2, margalef, menhinick, preston_a, preston_S = data

                N = float(N)
                S = float(S)

                if S < 2 or N < 10: continue

                Nlist.append(float(np.log10(N)))
                Slist.append(float(np.log10(S)))

                ESimplist.append(float(np.log10(float(ESimp))))
                KindList.append(kind)

                BPlist.append(float(BP))
                NmaxList.append(float(np.log10(float(Nmax))))

                # log-modulo transformation of skewnness
                lms = np.log10(np.abs(float(skew)) + 1)
                if skew < 0: lms = lms * -1
                rareSkews.append(float(lms))


            if index == 0: metlist = list(rareSkews)
            elif index == 1: metlist = list(NmaxList)
            elif index == 2: metlist = list(ESimplist)
            elif index == 3: metlist = list(Slist)

            # Multiple regression
            d = pd.DataFrame({'N': list(Nlist)})
            d['y'] = list(metlist)
            d['Kind'] = list(KindList)
            loglog = smf.ols('y ~ N * Kind', d).fit()

            loglogR2s.append(loglog.rsquared)
            loglogAICs.append(loglog.aic)
            loglogBICs.append(loglog.bic)

            # Multiple regression
            xlist = 10**np.array(Nlist)
            d = pd.DataFrame({'N': list(xlist)})
            d['y'] = list(metlist)
            d['Kind'] = list(KindList)
            loglin = smf.ols('y ~ N * Kind', d).fit()

            loglinR2s.append(loglin.rsquared)
            loglinAICs.append(loglin.aic)
            loglinBICs.append(loglin.bic)

            # Multiple regression
            ylist = 10**np.array(metlist)
            d = pd.DataFrame({'N': list(Nlist)})
            d['y'] = list(ylist)
            d['Kind'] = list(KindList)
            linlog = smf.ols('y ~ N * Kind', d).fit()

            linlogR2s.append(linlog.rsquared)
            linlogAICs.append(linlog.aic)
            linlogBICs.append(linlog.bic)

            # Multiple regression
            ylist = 10**np.array(metlist)
            xlist = 10**np.array(Nlist)
            d = pd.DataFrame({'N': list(xlist)})
            d['y'] = list(ylist)
            d['Kind'] = list(KindList)
            linear = smf.ols('y ~ N * Kind', d).fit()

            linearR2s.append(linear.rsquared)
            linearAICs.append(linear.aic)
            linearBICs.append(linear.bic)


        st, data, ss2 = summary_table(linear, alpha=0.05)
        # ss2: Obs, Dep Var Population, Predicted Value, Std Error Mean Predict,
        # Mean ci 95% low, Mean ci 95% upp, Predict ci 95% low, Predict ci 95% upp,
        # Residual, Std Error Residual, Student Residual, Cook's D

        fittedvalues = data[:,2]
        predict_mean_se = data[:,3]
        predict_mean_ci_low, predict_mean_ci_upp = data[:,4:6].T
        predict_ci_low, predict_ci_upp = data[:,6:8].T


        avgloglogR2 = round(np.mean(loglogR2s),3)
        avglinlogR2 = round(np.mean(linlogR2s),3)
        avglinearR2 = round(np.mean(linearR2s),3)
        avgloglinR2 = round(np.mean(loglinR2s),3)

        avgloglogAIC = round(np.mean(loglogAICs),3)
        avglinlogAIC = round(np.mean(linlogAICs),3)
        avglinearAIC = round(np.mean(linearAICs),3)
        avgloglinAIC = round(np.mean(loglinAICs),3)

        avgloglogBIC = round(np.mean(loglogBICs),3)
        avglinlogBIC = round(np.mean(linlogBICs),3)
        avglinearBIC = round(np.mean(linearBICs),3)
        avgloglinBIC = round(np.mean(loglinBICs),3)


        print 'averages from log-log', avgloglogR2, avgloglogAIC, avgloglogBIC
        print>>OUT, 'averages from log-log', avgloglogR2, avgloglogAIC, avgloglogBIC

        print 'averages from lin-log', avglinlogR2, avglinlogAIC, avglinlogBIC
        print>>OUT,'averages from lin-log', avglinlogR2, avglinlogAIC, avglinlogBIC

        print 'averages from log-lin', avgloglinR2, avgloglinAIC, avgloglinBIC
        print>>OUT,'averages from log-lin', avgloglinR2, avgloglinAIC, avgloglinBIC

        print 'averages from linear',  avglinearR2, avglinearAIC, avglinearBIC,'\n'
        print>>OUT,'averages from linear',  avglinearR2, avglinearAIC, avglinearBIC,'\n'

    OUT.close()
    return


modelcomparison()