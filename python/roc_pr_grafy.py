import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
import os; base=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','reports'); d=os.path.join(base,'results'); out=os.path.join(base,'figures')
INK='#1f1f1e'; INK2='#5f5e5a'; GRID='#e6e5e0'
COL={'LR':'#2a78d6','DT':'#eb6834'}
NAME={'LR':'Logistická regresia','DT':'Rozhodovací strom'}
STY={'S1':'-','S2':(0,(4,3))}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.edgecolor':INK2,'axes.labelcolor':INK,
 'xtick.color':INK2,'ytick.color':INK2,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':GRID,'grid.linewidth':0.8})
res={}
for s in ['S1','S2']:
    for m in ['LR','DT']:
        p=pd.read_csv(f'{d}/03_predikcie_{s}_{m}_test.csv')
        y=p['isFraud'].astype(int).values; sc=p['confidence(1)'].values
        res[(s,m)]=(y,sc)
        print(s,m,'n',len(y),'pos',y.sum(),'AUC %.4f'%roc_auc_score(y,sc),'PR-AUC %.4f'%average_precision_score(y,sc))
try:
    p=pd.read_csv(f'{d}/03_predikcie_S2_LR_train.csv'); print('S2 LR train AUC %.4f'%roc_auc_score(p.isFraud.astype(int),p['confidence(1)']))
except Exception as e: print('train',e)
# ROC
fig,ax=plt.subplots(figsize=(9,6.2),dpi=150)
for s in ['S1','S2']:
    for m in ['LR','DT']:
        y,sc=res[(s,m)]; f,t,_=roc_curve(y,sc)
        ax.plot(f*100,t*100,color=COL[m],ls=STY[s],lw=2,label=f'{NAME[m]}, {s} (AUC {roc_auc_score(y,sc):.3f})'.replace('.',','))
        pr_=sc>=0.5; ax.plot(((pr_)&(y==0)).sum()/(y==0).sum()*100,((pr_)&(y==1)).sum()/(y==1).sum()*100,'o',ms=7,color=COL[m],mec='white',mew=1.5,zorder=5)
ax.set_xlim(0,10); ax.set_ylim(50,101)
ax.set_xlabel('Falošné poplachy – podiel bežných transakcií označených ako podvod (%)'); ax.set_ylabel('Zachytené podvody – senzitivita (%)')
ax.set_title('ROC krivky na testovacej množine (výrez 0–10 % falošných poplachov)',loc='left',color=INK,fontsize=12)
ax.plot([],[],'o',color=INK2,mec='white',label='bod pri prahu 0,5 (kontingenčná tabuľka)')
ax.legend(frameon=False,loc='upper center',bbox_to_anchor=(0.5,-0.14),ncol=2,labelcolor=INK,fontsize=10)
fig.tight_layout(); fig.savefig(f'{out}/03_roc_test.png'); plt.close(fig)
# PR
fig,ax=plt.subplots(figsize=(9,6.2),dpi=150)
for s in ['S1','S2']:
    for m in ['LR','DT']:
        y,sc=res[(s,m)]; pr,rc,_=precision_recall_curve(y,sc)
        ax.step(rc*100,pr*100,where='post',color=COL[m],ls=STY[s],lw=2,label=f'{NAME[m]}, {s} (PR-AUC {average_precision_score(y,sc):.3f})'.replace('.',','))
        pr_=sc>=0.5; tp=((pr_)&(y==1)).sum(); ax.plot(tp/(y==1).sum()*100,tp/pr_.sum()*100,'o',ms=7,color=COL[m],mec='white',mew=1.5,zorder=5)
base=res[('S1','LR')][0].mean()*100
ax.axhline(base,color=INK2,lw=1,ls=':'); ax.text(2,base+1.5,f'náhodný model ({base:.2f} %)'.replace('.',','),color=INK2,fontsize=9,ha='left')
ax.set_xlim(0,100); ax.set_ylim(0,101)
ax.set_xlabel('Zachytené podvody – senzitivita / recall (%)'); ax.set_ylabel('Presnosť poplachov – precision (%)')
ax.set_title('Precision–recall krivky na testovacej množine',loc='left',color=INK,fontsize=12)
ax.plot([],[],'o',color=INK2,mec='white',label='bod pri prahu 0,5 (kontingenčná tabuľka)')
ax.legend(frameon=False,loc='upper center',bbox_to_anchor=(0.5,-0.14),ncol=2,labelcolor=INK,fontsize=10)
fig.tight_layout(); fig.savefig(f'{out}/03_pr_test.png'); plt.close(fig)
