"""Security proposal: fresh composition only. Use returned live IDs for edits."""
from pathlib import Path
import xml.etree.ElementTree as E

P=Path(__file__).parent
NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
svg=E.Element(f'{{{NS}}}svg',{'width':'8500','height':'38800'})

def el(p,tag,**a):
 return E.SubElement(p,f'{{{NS}}}{tag}',{k.replace('_','-'):str(v) for k,v in a.items()})

def text(p,key,x,y,w,body,size=22,bold=False,h=80):
 e=el(p,'textArea',id=key,x=x,y=y,width=w,height=h,fill='#1a1a1a' if bold else '#595959',font_family='noto_sans',font_size=size,text_align='left',font_weight='bold' if bold else 'normal')
 e.text=body
 return e

def card(p,key,x,y,w,h,body,kind='proposal'):
 colors={'context':('#f7f7f7','#b0b0b0','#313131'),'proposal':('#c6dcff','#659df2','#305bab'),'decision':('#fff6b6','#ffdc4a','#af7e04')}
 fill,stroke,ink=colors[kind]
 return el(p,'rect',id=key,x=x,y=y,width=w,height=h,data_content=body,fill=fill,stroke=stroke,stroke_width=2,data_text_color=ink,data_font_family='noto_sans',data_font_size=22,data_text_align='left',data_text_align_vertical='middle')

def frame(key,x,title,subtitle):
 f=el(svg,'g',id=key,transform=f'translate({x},36700)',data_frame=title)
 el(f,'rect',data_type='frame',x=0,y=0,width=3152,height=1910,fill='#ffffff',data_title=title)
 text(f,key+'-title',64,64,3024,title,33,True)
 text(f,key+'-subtitle',64,148,3024,subtitle)
 text(f,key+'-legend',64,1782,3024,'Draft for team review | Blue: proposed | Neutral: documented context | Yellow: gap or decision',18,h=64)
 return f

def diagram(p,key,x,y,w,h,title):
 return el(p,'g',id=key,transform=f'translate({x},{y})',data_diagram=title,data_width=w,data_height=h)

def node(p,key,x,y,w,h,body,kind='proposal'):
 colors={'proposal':('#A0C4FB','#6A8BBF','#14315E'),'context':('#DDDDD8','#A8A8A0','#434339'),'decision':('#FFE86D','#CBB333','#574900')}
 fill,stroke,ink=colors[kind]
 return el(p,'rect',id=key,x=x,y=y,width=w,height=h,data_content=body,fill=fill,stroke=stroke,stroke_width=2,data_text_color=ink,data_font_size=22,data_text_align='center',data_text_align_vertical='middle')

def link(p,key,a,b,label='',start='right',end='left'):
 def point(e,s):
  x,y,w,h=[float(e.get(k)) for k in ('x','y','width','height')]
  return {'left':(x,y+h/2),'right':(x+w,y+h/2),'top':(x+w/2,y),'bottom':(x+w/2,y+h)}[s]
 x1,y1=point(a,start);x2,y2=point(b,end)
 return el(p,'line',id=key,x1=x1,y1=y1,x2=x2,y2=y2,data_start=a.get('id'),data_end=b.get('id'),data_start_side=start,data_end_side=end,stroke='#313131',stroke_width=2,data_arrow='end',data_shape='elbowed',data_content=label)

f=frame('p12a',-2560,'12A Security: current coverage and proposed baseline','CTO / IT / DevOps / product owners | Security extends beyond laptops; verify protection separately for each environment.')
text(f,'a-current-title',64,244,1450,'Documented current state',22,True)
text(f,'a-proposed-title',1616,244,1472,'Proposed baseline',22,True)
current=[
 ('devices','Employee and contractor devices','Falcon is required; enrollment and effective policies must be checked.<br>Complete fleet compliance has not been verified.'),
 ('cloud','Google Cloud posture and foundations','Falcon posture monitoring is reported active across 64 projects.<br>The Nov 2 audit records private GKE/SQL, workload identity and backups.'),
 ('runtime','LMS runtime and Cloud Workstations','Staging/production GKE sensing remains an open rollout task.<br>Cloud Workstations has sensor health gaps and a canary in progress.'),
 ('scans','Scanning, access and logging','Registry read-access source exists; live scanning needs verification.<br>Recheck dated privileged-access, key and audit-log findings.'),
]
future=[
 ('identity','Identity and access','Agreed Entra identities and minimum normal access.<br>Controlled temporary elevation and verified removal.'),
 ('workloads','Runtime and image coverage','Supported sensors and working registry/image scans.<br>Check exact targets, policies and useful security signals.'),
 ('data','Cloud, network and data','Reviewed posture findings and restricted access.<br>Secret references, appropriate test data and recovery checks.'),
 ('response','Logs and response','Required events, delivery checks and agreed retention.<br>Named alert responders, escalation and a tested runbook.'),
]
for i,(key,title,body) in enumerate(current):
 card(f,'a-current-'+key,64,320+i*224,1450,192,f'<b>{title}</b><br>{body}','context' if i<2 else 'decision')
for i,(key,title,body) in enumerate(future):
 card(f,'a-future-'+key,1616,320+i*224,1472,192,f'<b>{title}</b><br>{body}')
text(f,'a-vendor-title',64,1260,3024,'Roles to confirm with the team and partners',22,True)
for key,x,title,body in [
 ('trekai',64,'TrekAI IT / DevOps','Own device/platform implementation.<br>Agree accountable security and incident owners.'),
 ('moxfive',1088,'MOXFIVE','Documented incident response and controls review.<br>Confirm current engagement and escalation duties.'),
 ('atbay',2112,'At-Bay','Documented post-incident hardening and M365/SSO work.<br>Confirm current scope and handoffs.'),
]: card(f,'a-role-'+key,x,1334,976,192,f'<b>{title}</b><br>{body}','context')
card(f,'a-decision',64,1590,3024,128,'<b>Team decision</b><br>Agree the required baseline, accountable owner, partner duties and first rollout scope. Record unsupported targets and approved exceptions.','decision')

f=frame('p12b',1232,'12B Security: rollout, verification and response','IT / DevOps / security responders / partners | Proposed workflow | A control is complete when the target is protected and its signals reach an owner.')
text(f,'b-rollout-title',64,244,3024,'Implementation and acceptance',22,True)
d=diagram(f,'b-rollout',64,320,3024,600,'Security control implementation and validation')
steps=[('inventory','1. Inventory targets','List systems and controls.<br>Confirm live coverage.<br>Assign each gap.'),('review','2. Review the change','Confirm supported model.<br>Review code, permissions<br>and rollback.'),('pilot','3. Prove in staging','Deploy a small pilot.<br>Check workload health<br>and security telemetry.'),('expand','4. Expand by target','Approve production.<br>Roll out in stages.<br>Record acceptance.')]
nodes=[]
for i,(key,title,body) in enumerate(steps): nodes.append(node(d,'b-step-'+key,40+i*736,40,672,224,f'<b>{title}</b><br>{body}'))
fail=node(d,'b-fail',1512,392,672,152,'<b>Validation fails</b><br>Hold rollout. Fix or roll back.<br>Keep the gap assigned.','decision')
for i in range(3):link(d,'b-step-link-'+str(i),nodes[i],nodes[i+1])
link(d,'b-fail-link',nodes[2],fail,'Checks fail','bottom','top')
text(f,'b-tests-title',64,990,3024,'Acceptance checks for each target',22,True)
for key,x,title,body in [
 ('sensor',64,'Runtime protection','Fresh check-in and intended policy.<br>Safe test yields exact-target events.'),
 ('scan',1088,'Image scanning','Working registry connection and scan.<br>Match the deployed image digest.'),
 ('logs',2112,'Logs and alerts','Required events arrive and parse.<br>A test alert reaches the responder.'),
]: card(f,'b-test-'+key,x,1064,976,160,f'<b>{title}</b><br>{body}')
text(f,'b-response-title',64,1288,3024,'Alert and incident workflow',22,True)
d=diagram(f,'b-response',64,1362,3024,282,'Security alert and incident response')
resp=[]
for i,(key,title,body) in enumerate([
 ('detect','Detect and route','Identify product and environment.'),('assign','Assess and assign','Record impact and incident owner.'),('recover','Contain and recover','Authorized response and partner help.'),('improve','Review and improve','Verify recovery and assign follow-ups.')]):
 resp.append(node(d,'b-response-'+key,40+i*736,40,672,160,f'<b>{title}</b><br>{body}'))
for i in range(3):link(d,'b-response-link-'+str(i),resp[i],resp[i+1])
text(f,'b-ownership',64,1680,3024,'Agree coverage hours, response targets, backup contacts and containment authority. Preserve investigation records and use the existing incident process.',22,h=80)

f=frame('p12c',5024,'12C Security: delivery plan and environment coverage','CTO / IT / DevOps / QA / security partners | Draft | Build one coverage record, prove the changes and make checks part of normal delivery.')
text(f,'c-phases-title',64,244,3024,'Delivery work packages',22,True)
for i,(key,title,body) in enumerate([
 ('inventory','1. Confirm coverage','Inventory controls by target.<br>Check live health and open findings.<br>Prioritize gaps and propose owners.'),
 ('baseline','2. Agree the baseline','Agree required controls and checks.<br>Confirm vendor scope and responders.<br>Set exception and approval rules.'),
 ('pilot','3. Prove the changes','Pilot supported sensing, scans and logs.<br>Check health and safe test signals.<br>Exercise response in staging.'),
 ('expand','4. Expand and maintain','Approve each production rollout.<br>Add checks to templates and releases.<br>Recheck after lifecycle changes.'),
]): card(f,'c-phase-'+key,64+i*768,320,720,256,f'<b>{title}</b><br>{body}')
text(f,'c-inventory-title',64,640,1450,'Coverage record: separate controls and targets',22,True)
card(f,'c-environments',64,714,1450,192,'<b>Products and environments</b><br>Hub/LMS: development, QA, staging and production.<br>CAP/TrekFinder: RD and each agreed additional target.<br>Track devices and Cloud Workstations separately.','context')
card(f,'c-record',64,946,1450,192,'<b>Record for every applicable control</b><br>Exact target, required coverage, actual status and latest check.<br>Owner, gap or approved exception, and next review.<br>Statuses: verified / configured but unverified / gap / exception.')
text(f,'c-qa-title',1616,640,1472,'QA template and handoff',22,True)
card(f,'c-qa-baseline',1616,714,1472,192,'<b>Include security in the approved template</b><br>Scoped identity, network isolation and secret references.<br>Applicable runtime protection, scanning and security logs.<br>Agreed test-data, retention, expiry and cleanup rules.')
card(f,'c-qa-ready',1616,946,1472,192,'<b>Verify before QA receives the URL</b><br>DevOps owns template and readiness checks; QA requests approved options.<br>A failed required control holds handoff unless an exception is approved.<br>Cleanup ends temporary access and preserves required records.')
text(f,'c-priorities-title',64,1202,3024,'Initial priorities and dependencies',22,True)
card(f,'c-priorities',64,1276,3024,160,'<b>Prioritize from verified impact</b><br>LMS staging/production sensing, Cloud Workstations canary, registry scanning and the highest-impact access/logging findings.<br>Coordinate with Terraform/GitOps delivery, Entra/PAM, QA requests, observability and documentation.','context')
text(f,'c-decisions-title',64,1500,3024,'Decisions for the team',22,True)
card(f,'c-decisions',64,1574,3024,144,'Who owns security and response? Which controls block release or QA handoff?<br>What do MOXFIVE and At-Bay currently cover? Who approves exceptions and production rollout?','decision')

ids={e.get('id') for e in svg.iter() if e.get('id')}
assert len(ids)==sum(bool(e.get('id')) for e in svg.iter())
for e in svg.iter():
 if e.get('data-start'): assert e.get('data-start') in ids and e.get('data-end') in ids
assert sum('data-frame' in e.attrib for e in svg)==3
E.indent(svg)
E.ElementTree(svg).write(P/'proposal-12.canvas.svg',encoding='utf-8',xml_declaration=True)
print('Built three native security frames, with editable control rollout and incident diagrams.')
