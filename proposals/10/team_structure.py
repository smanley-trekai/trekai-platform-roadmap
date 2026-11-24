"""Additional proposed team/access matrix for fresh board composition only."""
import xml.etree.ElementTree as E
N='http://www.w3.org/2000/svg'
def append_team_frame(svg):
 def el(p,tag,**a):
  return E.SubElement(p,f'{{{N}}}{tag}',{k.replace('_','-'):str(v) for k,v in a.items()})
 title='10D Team structure and access design'
 f=el(svg,'g',id='p10d',transform='translate(8945,30500)',data_frame=title)
 el(f,'rect',data_type='frame',x=0,y=0,width=3152,height=1910,fill='#ffffff',data_title=title)
 def text(key,x,y,w,h,body,size=22,bold=False):
  e=el(f,'textArea',id=key,x=x,y=y,width=w,height=h,font_family='noto_sans',font_size=size,font_weight='bold' if bold else 'normal',fill='#1a1a1a' if bold else '#595959',text_align='left');e.text=body
 def card(key,x,y,w,h,body,kind='proposal'):
  colors={'proposal':('#a0c4fb','#6a8bbf','#14315e'),'context':('#ddddd8','#a8a8a0','#434339'),'decision':('#ffe86d','#cbb333','#574900')}
  fill,stroke,ink=colors[kind]
  return el(f,'rect',id=key,x=x,y=y,width=w,height=h,fill=fill,stroke=stroke,stroke_width=2,data_content=body,data_font_family='noto_sans',data_font_size=22,data_text_color=ink,data_text_align='left',data_text_align_vertical='middle')
 text('d-title',64,64,3024,64,title,33,True)
 text('d-subtitle',64,148,3024,40,'Proposed / Draft | Agree responsibilities first, then define Entra groups, target permissions and temporary elevation.')
 cols=[(64,576,'Team / role'),(704,704,'Work and boundary'),(1472,768,'Proposed baseline'),(2304,784,'Extra access / decision')]
 for i,(x,w,t) in enumerate(cols):text('d-col-'+str(i),x,264,w,40,t,22,True)
 rows=[
 ('app','Application developers', 'Build product / platform application code.<br>Scope Trek Learning (Hub/LMS)<br>and TrekCAP/TrekFinder separately.', 'Approved source repositories and<br>development resources for assigned tasks.<br>Preserve restricted-source boundaries.', 'Production diagnosis or admin work:<br>define a scoped, eligible entitlement.<br>Keep normal code/change review.'),
 ('devops','DevOps', 'Build and operate environments,<br>infrastructure and delivery tooling.<br>Maintain templates and automation.', 'Agreed non-production operations<br>and delivery/configuration access.<br>Automation has its own identity.', 'Production change or recovery:<br>define task, target and time window.<br>Review execution identity separately.'),
 ('qa','QA', 'Test releases and report defects.<br>Request approved QA environments;<br>record acceptance evidence.', 'Test accounts, allowed diagnostics<br>and controlled environment requests.<br>No default Terraform/cloud admin.', 'Sensitive data or production access:<br>separate review and scoped access.<br>Keep demo/client-pilot rules separate.'),
 ('lead','Management / leadership', 'Leads, managers and directors:<br>coordinate delivery, quality and oversight.<br>Exact reporting structure remains open.', 'Agreed reports and dashboards.<br>Hands-on leads receive separately<br>assigned technical task roles.', 'Title alone grants no admin rights.<br>Assign approval authority explicitly;<br>manage conflicts of interest by policy.')]
 for r,(key,team,work,base,extra) in enumerate(rows):
  y=360+r*224
  for i,body in enumerate([f'<b>{team}</b>',work,base,extra]):
   x,w,_=cols[i];card('d-'+key+'-'+str(i),x,y,w,192,body)
 text('d-map-title',64,1300,3024,40,'Access design record for each team / task',22,True)
 card('d-map',64,1380,3024,160,'Team + task + product + environment → approved Entra group → target role and resource/repository scope.<br>Record group owner, membership rules and mapping; keep baseline separate from elevation eligibility.<br>For elevation: purpose, eligible identities, roles/scope, approval policy, maximum duration, owner and removal evidence.','context')
 card('d-decisions',64,1604,3024,128,'<b>Decisions before rollout</b><br>Agree team boundaries, reporting relationships, memberships, role names, access owners and approvers. Exact permissions remain to design.<br>Validate each target integration; test allowed/denied actions, role changes, overlapping grants and removal.','decision')
 text('d-legend',64,1764,3024,32,'Blue = proposed responsibilities / access | Gray = design record | Yellow = decisions; no teams, groups or permissions are configured.',18)
 text('d-evidence',64,1828,3024,32,'Basis: original proposal notes, Nov 12 discussion (07:43–10:37), and user clarification Nov 24, 2026. Reporting lines and authority are unconfirmed.',18)
 return f
