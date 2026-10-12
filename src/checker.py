import json,re
from pathlib import Path
CHECKLISTS=json.loads((Path(__file__).resolve().parents[1]/'standards/demo_checklists.json').read_text(encoding='utf-8'))

def assess(text,specialty,procedure):
    if specialty not in CHECKLISTS: raise ValueError('Unknown specialty')
    if procedure!='Resection':
        return {'applicable':False,'reason':'Demonstration checklists are restricted to resections. Verify actual protocol applicability with a pathologist.','flags':[],'present':0,'required':0,'completeness_pct':None}
    fields=CHECKLISTS[specialty]['fields']; lower=text.lower();flags=[]; present=[]
    for field,terms in fields.items():
        matches=[t for t in terms if re.search(r'(?<!\w)'+re.escape(t)+r'(?!\w)',lower)]
        if matches:present.append({'element':field,'matched_phrase':matches[0],'status':'POSSIBLY PRESENT — VERIFY'})
        else:flags.append({'element':field,'severity':'REVIEW','status':'NOT DETECTED','suggestion':'Pathologist to verify applicability and whether this element is stated; do not invent a value.'})
    n=len(fields)
    return {'applicable':True,'reason':'Teaching checklist only; not a CAP compliance result.','flags':flags,'present_elements':present,'present':len(present),'required':n,'completeness_pct':round(100*len(present)/n,1)}
