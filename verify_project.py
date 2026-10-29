#!/usr/bin/env python3
"""Offline read-only integrity checks; run from the repository root."""
from pathlib import Path
import csv,sys,nbformat,math
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,condition):
    checks.append((name,bool(condition)))
    print(('PASS' if condition else 'FAIL') + ' | ' + name)

p=ROOT/'Bank_Marketing_Comparing_Classifiers_17_1.ipynb'
check('Notebook present',p.exists())
if p.exists():
    nb=nbformat.read(p,as_version=4)
    code=[c for c in nb.cells if c.cell_type=='code']
    md=[c for c in nb.cells if c.cell_type=='markdown']
    check('At least 10 code cells and 8 Markdown cells',len(code)>=10 and len(md)>=8)
    check('Every code cell executed',all(c.execution_count is not None for c in code))
    check('No saved execution errors',not any(o.output_type=='error' for c in code for o in c.get('outputs',[])))
    src='\n'.join(str(c.source) for c in code)
    check('All required classifiers represented',all(v in src for v in ['LogisticRegression(','KNeighborsClassifier(','DecisionTreeClassifier(','SVC(']))
    check('Training CV and grid search present','StratifiedKFold(' in src and 'GridSearchCV(' in src)
    check('Duration explicitly excluded','drop(columns=[\'y\',\'duration\'])' in src)
    check('Seaborn and pandas exercised','sns.' in src and 'pd.' in src)

for f in ['README.md','requirements.txt','.gitignore','data/README.md','results/business_summary.md',
          'results/default_model_comparison.csv','results/cross_validation_grid_search.csv',
          'results/tuned_model_holdout_metrics.csv','results/logistic_coefficients.csv',
          'results/permutation_importance.csv','results/ranking_at_20_percent.csv',
          'results/audit_summary.csv']:
    check('Present: '+f,(ROOT/f).exists() and (ROOT/f).stat().st_size>0)
for i,n in enumerate(['01_class_balance_age.png','02_descriptive_segments.png',
                      '03_pr_roc_comparison.png','04_confusion_model_comparison.png',
                      '05_permutation_importance.png'],start=1):
    check('Figure present: '+n,(ROOT/'figures'/n).exists() and (ROOT/'figures'/n).stat().st_size>12000)
check('Large raw CSV excluded from repository package',not (ROOT/'data'/'bank-additional-full.csv').exists())
with open(ROOT/'results'/'tuned_model_holdout_metrics.csv',newline='') as fp:
    rows=list(csv.DictReader(fp))
    check('Tuned results cover four models',len(rows)==4 and set(r['model'] for r in rows)=={'Logistic regression','KNN','Decision tree','SVM (RBF)'})
    check('Numeric AP and AUC within [0,1]',all(0<=float(r['average_precision'])<=1 and 0<=float(r['roc_auc'])<=1 for r in rows))
print(f'\nTOTAL: {sum(ok for _,ok in checks)}/{len(checks)} checks passed')
sys.exit(0 if all(ok for _,ok in checks) else 1)
