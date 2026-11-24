"""Build Proposal 11 as native editable Miro widgets.

After creation, use returned live identities to edit the existing board.
Do not recreate this composition on the same board.
"""
from pathlib import Path
import xml.etree.ElementTree as E

P=Path(__file__).parent; NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
svg=E.Element(f'{{{NS}}}svg',{'width':'11600','height':'35600'})
colors={'context':('#ddddd8','#a8a8a0','#434339'),
        'proposal':('#a0c4fb','#6a8bbf','#14315e'),
        'decision':('#ffe86d','#cbb333','#574900')}
def el(p,tag,**a):
 return E.SubElement(p,f'{{{NS}}}{tag}',{k.replace('_','-'):str(v) for k,v in a.items()})
def text(p,key,x,y,w,body,size=22,bold=False):
 e=el(p,'textArea',id=key,x=x,y=y,width=w,height=64 if size==33 else 40,
      fill='#1a1a1a' if bold else '#595959',font_family='noto_sans',font_size=size,
      text_align='left',font_weight='bold' if bold else 'normal')
 e.text=body;return e
def card(p,key,x,y,w,h,body,kind='proposal'):
 fill,stroke,ink=colors[kind]
 return el(p,'rect',id=key,x=x,y=y,width=w,height=h,data_content=body,fill=fill,
           stroke=stroke,stroke_width=2,data_text_color=ink,data_font_family='noto_sans',
           data_font_size=22,data_text_align='left',data_text_align_vertical='middle')
def link(p,key,a,b,label='',start='right',end='left'):
 def point(e,s):
  x,y,w,h=[float(e.get(k)) for k in ('x','y','width','height')]
  return {'left':(x,y+h/2),'right':(x+w,y+h/2),'top':(x+w/2,y),'bottom':(x+w/2,y+h)}[s]
 x1,y1=point(a,start);x2,y2=point(b,end)
 return el(p,'line',id=key,x1=x1,y1=y1,x2=x2,y2=y2,data_start=a.get('id'),data_end=b.get('id'),
           data_start_side=start,data_end_side=end,stroke='#313131',stroke_width=2,
           data_arrow='end',data_shape='elbowed',data_content=label)
def frame(key,x,title,subtitle):
 f=el(svg,'g',id=key,transform=f'translate({x},33500)',data_frame=title)
 el(f,'rect',data_type='frame',x=0,y=0,width=3152,height=1910,fill='#ffffff',data_title=title)
 text(f,key+'-title',64,64,3024,title,33,True)
 text(f,key+'-subtitle',64,148,3024,subtitle)
 text(f,key+'-legend',64,1750,3024,'Blue = proposed | Gray = reported context or reference | Yellow = exception, boundary or team decision',18)
 return f

f=frame('p11a',-2560,'11A GitOps and SDLC: shared desired state and clear promotion',
        'CTO / developers / QA / DevOps / release owners | Draft | Standardize release handoffs, promote pinned artifacts and reconcile each environment from reviewed desired state.')
text(f,'a-current',64,244,880,'Reported delivery gaps: verify the actual scope',bold=True)
card(f,'a-dev-current',64,320,880,192,
     '<b>Development: automation was reported</b><br>At 23:05 in the Nov 12 discussion, the reviewed GitHub workflow was described as automating development.<br>Verify which products, repositories and steps this covers.','context')
card(f,'a-stage-current',64,552,880,192,
     '<b>Staging: manual handoff was reported</b><br>The discussion described PR comments/approvals followed by manual work.<br>Inventory the actual deployment path, checks and responsible roles.','context')
card(f,'a-prod-current',64,784,880,224,
     '<b>Production: manual completion was reported</b><br>The same discussion identified manual work after approvals.<br>The proposal is to centralize GitOps and simplify SDLC actions.<br>Current engines, branch mappings and release gates remain to verify.','decision')
text(f,'a-proposed',1104,244,1984,'Proposed: shared GitOps conventions with owned state per target',bold=True)
card(f,'a-contract',1104,320,1984,160,
     '<b>Shared GitOps area: an authoritative desired state for each product/environment</b><br>A release manifest pins the service artifacts; target configuration records dependencies, settings and secret references.<br>Use a common review/status workflow with explicit owners. Choose repository placement with Proposal 02 while preserving required access boundaries.')
text(f,'a-env-title',1104,544,1984,'Promote the accepted artifact set; review configuration and evidence at each target',bold=True)
dev=card(f,'a-dev',1104,608,576,256,
     '<b>Development: verify a candidate</b><br>CI publishes pinned images/release manifest.<br>Update reviewed dev desired state.<br>Reconcile and run agreed checks.<br>Record versions, test outcomes and failures.')
stage=card(f,'a-stage',1808,608,576,256,
     '<b>Staging: validate the accepted candidate</b><br>Promote the same immutable artifact set.<br>Use staging configuration and dependencies.<br>Automate reconciliation and technical checks.<br>QA/owners supply agreed acceptance evidence.')
prod=card(f,'a-prod',2512,608,576,256,
     '<b>Production: deliberate promotion</b><br>Promote staging-accepted artifacts.<br>Review production configuration and readiness.<br>Authorize via the agreed release policy.<br>Reconcile, verify service health and monitor.')
link(f,'a-promote-1',dev,stage,'Promote')
link(f,'a-promote-2',stage,prod,'Promote')
card(f,'a-reconcile',1104,928,1984,192,
     '<b>Target agents pull reviewed state and report versions, health and drift</b><br>The proposed <a href="https://opengitops.dev/">GitOps model</a> uses versioned declarative state and continuous reconciliation. Target-scoped agents apply the approved revision and report actual state.<br>Application teams own service changes; QA supplies acceptance evidence; DevOps owns the delivery platform with service/release owners. Engine and promotion automation remain to agree.','context')
for key,x,w,title in [('outcomes',64,960,'Expected outcomes'),('manifest',1088,960,'Release and target contract'),('decisions',2112,976,'Decisions for the team')]:
 text(f,'a-'+key+'-title',x,1180,w,title,bold=True)
card(f,'a-outcomes',64,1244,960,192,
     '• Fewer ambiguous manual handoffs between teams.<br>• Trace source, artifact, desired revision and target outcome.<br>• Promote an accepted candidate without rebuilding it.<br>• Stop failed promotion and handle drift/recovery visibly.')
card(f,'a-manifest',1088,1244,960,192,
     '• Source commit and immutable service artifact references.<br>• Target configuration, dependencies and secret references.<br>• Schema/migration compatibility and recovery requirements.<br>• Review, acceptance evidence and previous known-good revision.','context')
card(f,'a-decisions',2112,1244,976,192,
     '• Repository layout, engine and per-target state ownership.<br>• Branch/reference strategy and automated/manual handoffs.<br>• Required checks, release approval and QA acceptance.<br>• Drift policy, recovery and schema/data compatibility.','decision')
card(f,'a-boundaries',64,1500,3024,192,
     '<b>Infrastructure, build, deployment and acceptance are separate handoffs</b><br>Infrastructure changes follow <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690359619683">01B execution controls</a>; application artifacts follow <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690578070332">03B</a>/<a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690579560266">04B</a>. Terraform apply does not by itself install or approve an application release.<br>QA, sales demo and client pilot targets select manifests through <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503905">05B lifecycle rules</a>. Their provisioning/retirement is separate from dev → staging → production promotion. A branch merge has only the target behavior explicitly chosen by policy.','context')
text(f,'a-evidence',64,1810,3024,
     'Basis: proposal notes; Nov 12 discussion (11:11; 23:05); OpenGitOps principles checked Nov 16, 2026. Current automation gaps are reported concerns, not a new pipeline audit.',18)

f=frame('p11b',1275,'11B GitOps and SDLC: code change to verified environment promotion',
        'Developers / CI / reviewers / release owners / QA / DevOps | Draft | Build a candidate, review target desired state, reconcile, verify and repeat promotion with the same artifacts.')
for key,y,h,label in [('source',264,224,'Developer / source review'),('release',552,224,'CI / release candidate'),
                       ('target',840,224,'Target review / reconcile'),('verify',1128,224,'QA / service acceptance'),
                       ('operate',1416,256,'Release / operations')]:
 el(f,'rect',id='b-lane-'+key,x=64,y=y,width=3024,height=h,fill='#f7f7f7',stroke='none')
 text(f,'b-role-'+key,88,y+16,256,label,18,True)
change=card(f,'b-change',440,280,640,192,
     '<b>1. Propose application change [Developer]</b><br>Open a source PR and identify affected services.<br>Include required tests and compatibility changes.<br>Keep product/source-access boundaries intact.')
checks=card(f,'b-checks',1272,280,640,192,
     '<b>2. Validate and review [CI + owners]</b><br>Run agreed checks and affected-service tests.<br>Review application/schema/security impact.<br>Require the agreed source approval before merge.')
checksfail=card(f,'b-checks-failed',2104,280,840,192,
     '<b>Source checks or review do not pass</b><br>Return findings to the developer; hold the source merge.<br>Correct the PR and repeat the affected checks/review.<br>Retain test and review evidence.','decision')
buildfail=card(f,'b-build-failed',440,568,640,192,
     '<b>Build or candidate publication fails</b><br>Do not promote an incomplete release candidate.<br>Correct the failure and repeat CI.<br>Keep source, artifact and build-log context.','decision')
build=card(f,'b-build',1272,568,640,192,
     '<b>3. Merge and publish candidate [CI]</b><br>Build/test and publish immutable artifacts.<br>Create the manifest of exact service versions.<br>Record source commit and candidate evidence.')
targetpr=card(f,'b-target-pr',2104,568,840,192,
     '<b>4. Propose target desired state [Release owner / CI]</b><br>Open a GitOps PR with the manifest and explicit target configuration.<br>Check dependencies, secret references and migration requirements.<br>Select the product/environment rather than inferring it from a tag.')
reconcile=card(f,'b-reconcile',440,856,640,192,
     '<b>7. Pull and reconcile [Target agent]</b><br>Pull the approved desired state and apply its scope.<br>Resolve pinned artifacts and target configuration.<br>Report actual versions, sync and health status.')
merge=card(f,'b-merge',1272,856,640,192,
     '<b>6. Merge target desired state [Authorized owner]</b><br>Record the reviewed GitOps revision.<br>Update only the approved target desired state.<br>Report deployment health separately from merge status.')
approve=card(f,'b-approve',2104,856,840,192,
     '<b>5. Authorize target change [Owners]</b><br>Render configuration; check policy, artifact and scope.<br>Confirm evidence and infrastructure prerequisites.<br>Apply target approval; if rejected/unready, revise Step 4.')
failed=card(f,'b-target-failed',440,1144,640,192,
     '<b>Sync/readiness/acceptance fails: hold promotion</b><br>Assign an owner; retain versions and diagnostics.<br>Review fix/revert and data/schema compatibility.<br>Return to the appropriate PR step and reverify.','decision')
verify=card(f,'b-verify',1272,1144,640,192,
     '<b>8. Verify target [Automation / QA / owner]</b><br>Match desired revision and deployed manifest.<br>Check readiness, critical journeys and alerts.<br>Retain outcomes; hold promotion if unhealthy.')
promote=card(f,'b-promote',2104,1144,840,192,
     '<b>9. Record acceptance and promotion decision [Owners]</b><br>Require agreed evidence before the next target request.<br>Dev → staging → production follows the chosen release policy.<br>Repeat Steps 4–9 for each target using the same artifact set.')
card(f,'b-contract',440,1432,1472,224,
     '<b>Each environment has its own desired state, review and verification</b><br>Keep artifact identity fixed during promotion; review target configuration and dependencies separately.<br>Record source commit, artifact manifest, GitOps revision, environment, reviewer and test/health outcomes.<br>QA/demo/pilot instances follow 05 lifecycle rules. Required infrastructure changes use the separate 01 path.','context')
operate=card(f,'b-operate',2104,1432,840,224,
     '<b>10. Operate and recover [Service owner / reconciler]</b><br>Continuously compare runtime with reviewed desired state.<br>Report drift and failed reconciliation to an accountable owner.<br>Recover through an approved desired-state change.<br>Verify health and data/schema compatibility; record follow-up.')
link(f,'b-l1',change,checks,'PR')
link(f,'b-l2',checks,build,'Passed','bottom','top')
link(f,'b-l3',build,targetpr,'Candidate')
link(f,'b-l4',targetpr,approve,'Target PR','bottom','top')
link(f,'b-l5',approve,merge,'Approved','left','right')
link(f,'b-l6',merge,reconcile,'Revision','left','right')
link(f,'b-l7',reconcile,verify,'Status','bottom','top')
link(f,'b-l8',verify,promote,'Accepted')
link(f,'b-l9',promote,operate,'Operate','bottom','top')
link(f,'b-checks-failed-link',checks,checksfail,'Failed')
link(f,'b-build-failed-link',build,buildfail,'Failed','left','right')
link(f,'b-target-failed-link',verify,failed,'Failed','left','right')
text(f,'b-evidence',64,1810,3024,
     'Proposed workflow. Verify actual engine, branch/target mapping, automation, acceptance authority and recovery behavior; GitOps centralization does not require every source repository to migrate first.',18)

f=frame('p11c',5110,'11C GitOps and SDLC: delivery plan and validation',
        'DevOps / application owners / QA / release and service owners | Draft | Inventory manual gaps, agree the release contract, prove development, then extend promotion with evidence.')
text(f,'c-work',64,244,3024,'Proposed work packages',bold=True)
phases=[]
for key,x,title,body,owner in [
 ('c-inventory',64,'1. Inventory the real delivery paths',
  'Map repositories, CI, artifacts and deploy engines.<br>Trace dev/staging/production and manual handoffs.<br>Record desired-state ownership and target identities.<br>Prioritize gaps with application and QA teams.',
  'DevOps + application + service owners'),
 ('c-design',860,'2. Agree the shared release contract',
  'Choose GitOps layout, engine and target mapping.<br>Define manifests, pinned artifacts and configuration.<br>Set PR checks, owners and promotion evidence.<br>Agree drift, migration and recovery policies.',
  'DevOps + application + QA/release owners'),
 ('c-pilot',1656,'3. Prove one development release',
  'Build a traceable immutable candidate.<br>Review desired state and reconcile a scoped target.<br>Test failures, acceptance and reported drift.<br>Exercise approved recovery and retain evidence.',
  'DevOps + application owners + QA'),
 ('c-rollout',2452,'4. Extend staging and production',
  'Promote accepted artifacts without rebuilding.<br>Validate target approvals, dependencies and checks.<br>Replace manual steps after equivalent proof.<br>Publish runbooks and assign ongoing ownership.',
  'Release/service owners + DevOps + QA'),
]:
 phases.append(card(f,key,x,328,636,256,f'<b>{title}</b><br>{body}'))
 text(f,key+'-owner',x,616,636,'Proposed owner: '+owner,18)
for i in range(3):link(f,'c-next-'+str(i),phases[i],phases[i+1],'Next')
for key,x,y,title in [('proof',64,744,'Evidence before wider rollout'),('dependencies',1656,744,'Inputs and coordination'),
                      ('controls',64,1120,'Operating controls to agree'),('decisions',1656,1120,'Open decisions for review')]:
 text(f,'c-'+key+'-title',x,y,1432,title,bold=True)
card(f,'c-proof',64,824,1432,224,
     '• Trace source → immutable artifacts → GitOps revision → actual target.<br>• Deploy accepted artifacts with each target’s own configuration/checks.<br>• Failed checks, sync or acceptance stop the next promotion.<br>• Detect drift and route failed reconciliation to an owner.<br>• Prove recovery, including application/data/schema compatibility.','context')
card(f,'c-dependencies',1656,824,1432,224,
     '• Verified existing CI/deploy engines and environment/state inventory.<br>• Approved service artifacts and release manifests from 03/04.<br>• GitOps ownership/layout coordinated with 02; infrastructure controls in 01.<br>• QA/demo/pilot lifecycle in 05; runbooks and monitoring in 06/07.<br>• Repository access and execution identities coordinated with 08–10.','context')
card(f,'c-controls',64,1200,1432,224,
     '• Explicit product/target ownership and scoped reconciliation identities.<br>• Reviewed desired state, pinned artifacts and secret references.<br>• Agreed checks, acceptance evidence and promotion authority.<br>• Drift/incident handling and schema-aware fix/revert/recovery.<br>• Release records, runbook maintenance and recurring workflow review.','decision')
card(f,'c-decisions',1656,1200,1432,224,
     '• Which GitOps area/repositories, engine and state layout are appropriate?<br>• Which branches/references map to each target, and what is automated?<br>• Which QA checks and owners authorize staging/production promotion?<br>• How do data migrations, dependencies and failure recovery work?<br>• What drift behavior, evidence retention and operational support apply?','decision')
card(f,'c-boundaries',64,1504,3024,160,
     '<b>Standardize the operating workflow without assuming every repository or tool changes</b><br>Apply <a href="https://opengitops.dev/">OpenGitOps principles</a> to reviewed desired state and target reconciliation. Coordinate 02–04 repository decisions while preserving source-access boundaries; consolidation is not a prerequisite.<br>Infrastructure apply, application release, target reconciliation and acceptance remain distinct. A Git revert alone does not restore database contents or prove disaster recovery.','context')
text(f,'c-evidence',64,1810,3024,
     'Basis: proposal notes and Nov 12 discussion (11:11; 23:05); OpenGitOps checked Nov 16, 2026. No live pipeline, deployment, branch protection, resource or reconciliation setting is changed.',18)

ids={e.get('id'):e for e in svg.iter() if e.get('id')}
assert len(ids)==sum(bool(e.get('id')) for e in svg.iter()) and len(svg)==3
for f in svg:
 for e in f:
  if e.get('data-start'):
   assert e.get('data-start') in ids and e.get('data-end') in ids
  elif e.get('x') is not None:
   assert 0<=float(e.get('x')) and 0<=float(e.get('y'))
   assert float(e.get('x'))+float(e.get('width',0))<=3152
   assert float(e.get('y'))+float(e.get('height',0))<=1910
assert not any(e.tag.endswith(('image','foreignObject')) for e in svg.iter())
E.indent(svg)
E.ElementTree(svg).write(P/'proposal-11.canvas.svg',encoding='utf-8',xml_declaration=True)
print(f'Built 3 frames and {len(ids)} native widgets; bounds and connector references checked.')

