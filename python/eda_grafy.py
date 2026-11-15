"""Grafy k prieskumu dát (kapitola 2). Vstupy: reports/results/01_*.csv a data/raw/*.csv."""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
RES=os.path.join(ROOT,'reports','results'); OUT=os.path.join(ROOT,'reports','figures')
RAW=os.path.join(ROOT,'data','raw','PS_20174392719_1491204439457_log.csv')
INK='#1f1f1e'; INK2='#5f5e5a'; GRID='#e6e5e0'; BLUE='#2a78d6'; ORANGE='#eb6834'; GRAY='#b9b8b2'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.edgecolor':INK2,'axes.labelcolor':INK,'xtick.color':INK2,'ytick.color':INK2,
 'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':GRID,'grid.linewidth':0.8,'axes.axisbelow':True})
sk=lambda x,d=0: f'{x:,.{d}f}'.replace(',',' ').replace('.',',')

# 1) Podvody podľa hodiny – tri panely so spoločnou osou x
h=pd.read_csv(os.path.join(RES,'01_podvody_podla_hodiny.csv')).sort_values('hour')
fig,ax=plt.subplots(3,1,figsize=(9,7.5),dpi=150,sharex=True)
ax[0].bar(h.hour,h['count(fraud_num)']/1000,color=GRAY,width=0.8); ax[0].set_ylabel('tis. transakcií')
ax[0].set_title('Všetky transakcie',loc='left',color=INK,fontsize=11)
ax[1].bar(h.hour,h['sum(fraud_num)'],color=ORANGE,width=0.8); ax[1].set_ylabel('počet')
ax[1].set_title('Podvody – ich počet je počas dňa takmer rovnaký',loc='left',color=INK,fontsize=11)
ax[2].bar(h.hour,h['average(fraud_num)']*100,color=ORANGE,width=0.8); ax[2].set_ylabel('%')
ax[2].set_title('Podiel podvodov – v noci (3.–5. hod.) až 22 %, cez deň pod 0,1 %',loc='left',color=INK,fontsize=11)
for i,r in h[h['average(fraud_num)']>0.1].iterrows(): ax[2].text(r.hour,r['average(fraud_num)']*100+0.6,sk(r['average(fraud_num)']*100,1),ha='center',fontsize=9,color=INK)
ax[2].set_xticks(range(24)); ax[2].set_xlabel('Hodina dňa (step mod 24)')
fig.suptitle('Transakcie a podvody podľa hodiny dňa',x=0.06,ha='left',color=INK,fontsize=13)
fig.tight_layout(); fig.savefig(os.path.join(OUT,'01_podvody_podla_hodiny.png')); plt.close(fig)

# 2) Podiel podvodov podľa typu transakcie
t=pd.read_csv(os.path.join(RES,'01_podvody_podla_typu.csv'))
p=t.pivot_table(index='type',columns='isFraud',values='count(amount)',aggfunc='sum').fillna(0)
p.columns=[str(c) for c in p.columns]; p['spolu']=p['0']+p.get('1',0); p['podiel']=p.get('1',0)/p['spolu']*100
p=p.sort_values('spolu')
fig,ax=plt.subplots(1,2,figsize=(10,3.8),dpi=150,sharey=True)
ax[0].barh(p.index,p.spolu/1e6,color=GRAY,height=0.6); ax[0].set_xlabel('mil. transakcií'); ax[0].set_title('Počet transakcií',loc='left',color=INK,fontsize=11)
for y,v in zip(p.index,p.spolu): ax[0].text(v/1e6+0.03,y,sk(v),va='center',fontsize=9,color=INK)
ax[0].set_xlim(0,p.spolu.max()/1e6*1.35)
ax[1].barh(p.index,p.podiel,color=[ORANGE if v>0 else GRAY for v in p.podiel],height=0.6); ax[1].set_xlabel('% podvodov'); ax[1].set_title('Podiel podvodov',loc='left',color=INK,fontsize=11)
for y,v,n in zip(p.index,p.podiel,p.get('1',0)): ax[1].text(v+0.02,y,(f'{sk(v,2)} % ({sk(n)} podvodov)' if v>0 else '0 podvodov'),va='center',fontsize=9,color=INK)
ax[1].set_xlim(0,p.podiel.max()*1.9)
from matplotlib.ticker import FuncFormatter
for a in ax: a.xaxis.set_major_formatter(FuncFormatter(lambda x,_: sk(x,1)))
fig.suptitle('Podvody sa vyskytujú len v typoch TRANSFER a CASH_OUT',x=0.02,ha='left',color=INK,fontsize=13)
fig.tight_layout(); fig.savefig(os.path.join(OUT,'01_podvody_podla_typu.png')); plt.close(fig)

# 3) Rozdelenie súm podľa triedy (TRANSFER + CASH_OUT), logaritmická os
if os.path.exists(RAW):
    d=pd.read_csv(RAW,usecols=['type','amount','isFraud'])
    d=d[d.type.isin(['TRANSFER','CASH_OUT'])&(d.amount>0)]
    bins=np.linspace(0,7.5,61)
    fig,ax=plt.subplots(figsize=(9,4.8),dpi=150)
    for cls,col,lab in [(0,GRAY,'bežné transakcie'),(1,ORANGE,'podvody')]:
        v=np.log10(d.amount[d.isFraud==cls]); w=np.ones(len(v))/len(v)*100
        ax.hist(v,bins=bins,weights=w,color=col,alpha=0.85 if cls else 0.9,label=f'{lab} (medián {sk(np.median(10**v))})',histtype='stepfilled' if cls==0 else 'step',lw=2.2 if cls else 0)
    ax.axvline(7,color=INK2,ls=':',lw=1); ax.text(6.95,ax.get_ylim()[1]*0.9,'strop simulácie\n10 mil.',fontsize=9,color=INK2,ha='right')
    ax.set_xticks(range(0,8)); ax.set_xticklabels(['1','10','100','1 tis.','10 tis.','100 tis.','1 mil.','10 mil.'])
    ax.set_xlabel('Suma transakcie (logaritmická os)'); ax.set_ylabel('% transakcií v triede')
    ax.set_title('Rozdelenie súm: podvody majú výrazne vyššie sumy',loc='left',color=INK,fontsize=13)
    ax.legend(frameon=False,loc='upper left',labelcolor=INK)
    fig.tight_layout(); fig.savefig(os.path.join(OUT,'01_rozdelenie_sum.png')); plt.close(fig)
print('hotovo')
