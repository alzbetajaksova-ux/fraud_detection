import os
import csv,glob,sys
print(f"{'model':14s}{'TP':>7}{'FN':>6}{'FP':>8}{'zachránené (mil.)':>19}{'stratené (mil.)':>17}{'podiel sumy':>12}{'poplachy':>10}")
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','reports','results')+'/03_kontingencna_*.csv')):
    d={}
    for r in csv.DictReader(open(f)):
        d[(r['isFraud'],r['prediction(isFraud)'])]=(float(r['count(isFraud)']),float(r['sum(amount)']))
    tp,stp=d.get(('1','1'),(0,0)); fn,sfn=d.get(('1','0'),(0,0)); fp,sfp=d.get(('0','1'),(0,0))
    print(f"{f.split('kontingencna_')[1][:-4]:14s}{tp:7.0f}{fn:6.0f}{fp:8.0f}{stp/1e6:19.1f}{sfn/1e6:17.1f}{stp/(stp+sfn)*100:11.2f}%{tp+fp:10.0f}")
