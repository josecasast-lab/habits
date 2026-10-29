import glob, json, os, re, sys
BASE=os.path.dirname(os.path.abspath(__file__))
ORDER=['Cereales y granos','Pastas','Panes y panadería','Tubérculos y raíces','Menestras','Verduras','Frutas','Carnes y vísceras','Aves','Pescados y mariscos','Huevos y lácteos','Frutos secos, semillas y aceites','Platos peruanos','Sopas y caldos','Postres y dulces','Bebidas','Comida rápida y chatarra','Snacks y galletas','Internacional','Salsas y condimentos','Fitness y suplementos','Desayunos y cereales']
foods=[];seen={};cat=None;bad=[]
for fn in sorted(glob.glob(os.path.join(BASE,'data','f*.txt'))):
    for ln,line in enumerate(open(fn,encoding='utf-8'),1):
        line=line.strip()
        if not line: continue
        if line.startswith('## '):
            cat=line[3:].strip()
            if cat not in ORDER: print('CAT?',cat);sys.exit(1)
            continue
        p=line.split('|')
        if len(p)not in(6,7): bad.append((fn,ln,line));continue
        try:
            name=p[0].strip();P,F,C,g=[float(x) for x in p[1:5]];lab=p[5].strip()
            k=float(p[6]) if len(p)==7 else round(4*P+9*F+4*C)
        except Exception as e:
            bad.append((fn,ln,line));continue
        key=name.lower()
        if key in seen: print('DUP',name,'|',fn,ln);continue
        seen[key]=1
        foods.append([name,ORDER.index(cat),round(k),P,F,C,int(g) if g==int(g) else g,lab])
print('foods:',len(foods))
for b in bad: print('BAD',b)
from collections import Counter
cnt=Counter(f[1] for f in foods)
for i,c in enumerate(ORDER): print(f'{c}: {cnt[i]}')
# sanity: portion kcal outliers
for f in foods:
    pk=f[2]*f[6]/100
    if pk>1500 or (f[2]>900) or f[2]<0: print('OUTLIER',f)
js='const FOODS_CATS='+json.dumps(ORDER,ensure_ascii=False)+';\nconst FOODS='+json.dumps(foods,ensure_ascii=False,separators=(',',':'))+';\n'
open(os.path.join(BASE,'foods.js'),'w',encoding='utf-8').write(js)
print('bytes',len(js.encode()))
