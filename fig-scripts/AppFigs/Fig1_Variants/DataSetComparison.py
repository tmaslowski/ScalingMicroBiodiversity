from __future__ import division
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import setp

mydir = os.path.expanduser("~/GitHub/MicrobialScaling/")

# function for setting the colors of the box plots pairs
def setBoxColors(bp):

    #print len(bp['caps'])
    #print bp['fliers'][0]
    #print bp['fliers'][1]
    #print bp['fliers'][2]
    #print bp['fliers'][3]

    setp(bp['boxes'][0], color='blue')
    setp(bp['caps'][0], color='blue')
    setp(bp['caps'][1], color='blue')
    setp(bp['whiskers'][0], color='blue')
    setp(bp['whiskers'][1], color='blue')
    #setp(bp['fliers'][0], color='blue')
    #setp(bp['fliers'][1], color='blue')
    setp(bp['medians'][0], color='blue')

    setp(bp['boxes'][1], color='red')
    setp(bp['caps'][2], color='red')
    setp(bp['caps'][3], color='red')
    setp(bp['whiskers'][2], color='red')
    setp(bp['whiskers'][3], color='red')
    #setp(bp['fliers'][2], color='red')
    #setp(bp['fliers'][3], color='red')
    setp(bp['medians'][1], color='red')

    return


datasets = []
metrics = ['rarity', 'dominance', 'evenness', 'richness']

#GoodNames = ['BIGN', 'SED', 'BOVINE','CHU', 'LAUB', 'CHINA', 'CATLIN', 'FUNGI', 'HUMAN', 'HYDRO', 'HMP', 'EMPopen', 'BBS', 'CBC', 'MCDB', 'GENTRY', 'FIA']
GoodNames = ['BCLS', 'CHINA', 'CATLIN', 'HUMAN', 'FUNGI', 'HYDRO', 'EMPopen', 'HMP', 'BBS', 'CBC', 'MCDB', 'GENTRY', 'FIA']


for m in metrics:

    micNlist, micSlist, micIntList, micCoefList = [[], [], [], []]
    macNlist, macSlist, macIntList, macCoefList = [[], [], [], []]

    #IN = open(mydir + 'output/SummaryPerDataset_NoMicrobe1s.txt','r')
    IN = open(mydir + 'output/SummaryPerDataset.txt','r')

    for data in IN:

        data = data.split()
        name, kind, metric, avgN, avgS, Int, Coef = data
        if name in GoodNames: pass
        else: continue

        if metric == m and kind == 'micro':
            micNlist.append(float(avgN))
            micSlist.append(float(avgS))
            micIntList.append(float(Int))
            micCoefList.append(float(Coef))

        elif metric == m and kind == 'macro':
            macNlist.append(float(avgN))
            macSlist.append(float(avgS))
            macIntList.append(float(Int))
            macCoefList.append(float(Coef))

        #print name, avgN, avgS

    IN.close()

    fig = plt.figure()
    ax = plt.axes()
    #plt.hold(True)

    # first boxplot pair
    Ints = [micIntList, macIntList]
    bp = plt.boxplot(Ints, positions = [1, 2], widths = 0.6)
    setBoxColors(bp)

    # second boxplot pair
    Coefs = [micCoefList, macCoefList]
    bp = plt.boxplot(Coefs, positions = [4, 5], widths = 0.6)
    setBoxColors(bp)


    # set axes limits and labels
    plt.xlim(0, 10)
    #plt.ylim(0, 9)
    #plt.yscale('log')
    ax.set_xticklabels(['Intercepts', 'Exponents'])#, 'avg N', 'avg S'])
    ax.set_xticks([1.5, 4.5])#, 7.5, 10.5])

    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('Microbes', 'Macrobes'))
    if m == 'dominance':
        ax.axhline(1.0, 0, 1., ls = '--', c = '0.3')
    plt.title(m)
    hB.set_visible(False)
    hR.set_visible(False)

    #plt.savefig(mydir+'/figs/appendix/DatasetComparison/'+m+'_NoMicrobeSingletons_ClosedRef.png', dpi=600, bbox_inches = "tight")
    #plt.savefig(mydir+'/figs/appendix/DatasetComparison/'+m+'_NoMicrobeSingletons_OpenRef.png', dpi=600, bbox_inches = "tight")

    #plt.savefig(mydir+'/figs/appendix/DatasetComparison/'+m+'_ClosedRef.png', dpi=600, bbox_inches = "tight")
    plt.savefig(mydir+'/figs/appendix/DatasetComparison/'+m+'_OpenRef.png', dpi=600, bbox_inches = "tight")

    plt.show()
