"""Build Proposal 09 as native editable Miro widgets.

After creation, use returned live identities to edit the existing board.
Do not recreate this composition on the same board.
"""
from pathlib import Path
import xml.etree.ElementTree as E

P=Path(__file__).parent; NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
svg=E.Element(f'{{{NS}}}svg',{'width':'11600','height':'29600'})
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
 f=el(svg,'g',id=key,transform=f'translate({x},27500)',data_frame=title)
 el(f,'rect',data_type='frame',x=0,y=0,width=3152,height=1910,fill='#ffffff',data_title=title)
 text(f,key+'-title',64,64,3024,title,33,True)
 text(f,key+'-subtitle',64,148,3024,subtitle)
 text(f,key+'-legend',64,1750,3024,'Blue = proposed | Gray = reported context or reference | Yellow = exception, boundary or team decision',18)
 return f

f=frame('p09a',-2560,'09A Entra ID for GitHub: sign-in, teams and repository access',
        'CTO / developers / QA / DevOps / identity and GitHub owners | Draft | Centralize staff identity checks while explicitly mapping groups to teams and repository permissions.')
text(f,'a-current',64,244,880,'Requested changes and facts to establish',bold=True)
card(f,'a-intent',64,320,880,192,
     '<b>Use Microsoft Entra ID as the GitHub IdP</b><br>The proposal requests centralized staff access through Entra.<br>Confirm GitHub deployment, plan and account model before choosing the integration.','context')
card(f,'a-access-review',64,552,880,192,
     '<b>Review teams, group mappings and repository access</b><br>The Nov 12 discussion calls for clearer Entra-to-GitHub team mappings.<br>Review organization base permissions, direct grants and team-derived access.','decision')
card(f,'a-naming',64,784,880,224,
     '<b>Make group and team names meaningful</b><br>Agree team/product and access-purpose names with clear owners.<br>Illustration only: dev-learning-source-write.<br>Record Entra group ID, GitHub organization/team, repositories and roles; names alone do not establish access.','decision')
text(f,'a-proposed',1104,244,1984,'Proposed: identity checks, team membership and repository roles',bold=True)
for key,x,label in [('entra',1104,'Microsoft Entra ID: identity and groups'),('github',2208,'GitHub: identity, teams and repository policy')]:
 el(f,'rect',id='a-boundary-'+key,x=x,y=320,width=880,height=800,fill='#f7f7f7',stroke='none')
 text(f,'a-'+key+'-title',x+32,344,816,label,22,True)
auth=card(f,'a-auth',1136,424,816,192,
     '<b>Staff follows the supported sign-in route</b><br>Entra applies the approved authentication policy.<br>The GitHub account model determines the sign-in journey.<br>Validate the organization/enterprise SSO entry point.')
identity=card(f,'a-identity',2240,424,816,192,
     '<b>GitHub account and SSO access context</b><br>The selected model links or provisions the staff identity.<br>With personal accounts, normal GitHub login remains.<br>Validate web and required Git/CLI/API access.')
groups=card(f,'a-groups',1136,824,816,192,
     '<b>Approved Entra group membership</b><br>Owners approve assignments for the staff member’s job.<br>Choose the group/team mechanism supported by the model.<br>Organization membership/provisioning is a separate step.')
repos=card(f,'a-repositories',2240,824,816,192,
     '<b>Owned GitHub teams and repository roles</b><br>Map groups to teams; assign team access per repository.<br>Review organization base, direct and team-derived grants.<br>Test required actions and restricted-repository denials.')
link(f,'a-auth-link',auth,identity,'SSO / identity')
mapping=link(f,'a-map-link',groups,repos,'Membership map');mapping.set('stroke-dasharray','5,5')
link(f,'a-policy-link',identity,repos,'Check access','bottom','top')
text(f,'a-auth-note',1136,664,816,'Solid arrows: identity checks and access evaluation',18)
text(f,'a-map-note',1136,716,816,'Dashed arrow: approved group-to-team membership',18)
for key,x,w,title in [('outcomes',64,960,'Expected outcomes'),('options',1088,960,'Account model and integration choice'),('decisions',2112,976,'Decisions for the team')]:
 text(f,'a-'+key+'-title',x,1180,w,title,bold=True)
card(f,'a-outcomes',64,1244,960,192,
     '• Staff follow a supported GitHub identity/access path.<br>• Team needs map to understandable repository roles.<br>• Restricted source visibility remains controlled.<br>• Membership changes and removals can be demonstrated.')
card(f,'a-options',1088,1244,960,192,
     '<b>Confirm deployment, plan and enterprise account type</b><br><a href="https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/about-saml-for-enterprise-iam">Personal accounts + SAML SSO</a>; <a href="https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization/managing-team-synchronization-for-your-organization">team synchronization</a> where supported.<br>Or evaluate Enterprise Managed Users with Entra.<br>Validate provisioning, migration and collaboration needs.<br>The account model and mechanism remain to agree.','context')
card(f,'a-decisions',2112,1244,976,192,
     '• Deployment/plan, account model and SSO scope.<br>• Group/team names, stable mapping IDs and owners.<br>• Organization base access and per-repository roles.<br>• Membership approvals, provisioning, removal and support.','decision')
card(f,'a-scope',64,1500,3024,192,
     '<b>Preserve source-access boundaries while improving identity management</b><br>SSO verifies identity/access context; repository permissions and branch/review rules still govern actions. Preserve the restricted-source boundaries described in <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690579560265">04A product access scope</a> when reviewing teams or repository consolidation.<br>Proposal 08 covers Google Cloud; 10 must define any supported GitHub elevation mechanism. Inventory GitHub Apps, deploy keys and workflow identities separately; maintain the access catalog through <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690590495741">06B</a>.','context')
text(f,'a-evidence',64,1810,3024,
     'Basis: proposal notes; Nov 12 discussion (06:54–10:37); GitHub identity/team/repository-role references checked Nov 16, 2026. Current plan, account model and effective grants remain to inventory.',18)

f=frame('p09b',1275,'09B Entra to GitHub: staff access and membership lifecycle',
        'Staff / identity administrators / organization and repository owners | Draft | Establish identity and membership, evaluate repository access and verify changes/removal.')
for key,y,h,label in [('request',264,224,'Staff / access request'),('identity',552,224,'Membership / identity'),
                       ('github',840,224,'GitHub / repository policy'),('task',1128,224,'Staff task / evidence'),
                       ('lifecycle',1416,256,'Access owners / lifecycle')]:
 el(f,'rect',id='b-lane-'+key,x=64,y=y,width=3024,height=h,fill='#f7f7f7',stroke='none')
 text(f,'b-role-'+key,88,y+16,256,label,18,True)
request=card(f,'b-request',440,280,640,192,
     '<b>1. Identify the GitHub task [Staff]</b><br>Select organization, repository and operation.<br>State the team/job need and required role.<br>Use the agreed membership/access request route.')
authfail=card(f,'b-auth-fail',1272,280,640,192,
     '<b>GitHub login or Entra SSO is blocked</b><br>Identify which identity check failed.<br>Owners resolve the authorized policy/account fix.<br>Repeat the supported sign-in journey.','decision')
mapfail=card(f,'b-map-fail',2104,280,840,192,
     '<b>Membership or mapping is incomplete</b><br>Check organization membership, linked identity and group/team mapping.<br>Review provisioning/synchronization status for the selected model.<br>Resolve the approved configuration and repeat the affected checks.','decision')
membership=card(f,'b-membership',440,568,640,192,
     '<b>2. Confirm membership [Access owners]</b><br>Confirm approved organization membership/invitation.<br>Assign Entra groups through the agreed process.<br>Check linked GitHub teams and their owners.')
auth=card(f,'b-auth',1272,568,640,192,
     '<b>3. Complete identity checks [User / Entra]</b><br>GitHub login plus organization SSO as required.<br>Entra applies approved authentication controls.<br>Use the journey for the selected account model.')
identity=card(f,'b-identity',2104,568,840,192,
     '<b>4. Establish membership/context [Integration]</b><br>Confirm the intended GitHub identity and organization membership.<br>Apply the model-supported group/team mapping.<br>Check SSO, provisioning and synchronization status.')
denied=card(f,'b-denied',440,856,640,192,
     '<b>Denied or additional access is needed</b><br>Check SSO, credentials, team grants and repo role.<br>Use the agreed GitHub approval path for changes.<br>Temporary elevation design belongs to Proposal 10.','decision')
evaluate=card(f,'b-evaluate',1272,856,640,192,
     '<b>5. Evaluate access [GitHub policy]</b><br>Resolve team, base and direct repository grants.<br>Check organization and repository constraints.<br>Permit only the authorized repository operation.')
allowed=card(f,'b-allowed',2104,856,840,192,
     '<b>6. Confirm allowed repository scope [User / owner]</b><br>Check the effective role and applicable branch/review rules.<br>Use an approved web, Git/CLI or API credential path.<br>Additional access follows its agreed request/approval mechanism.')
unexpected=card(f,'b-unexpected',440,1144,640,192,
     '<b>Unexpected repository visibility/action</b><br>Record user, repository, action and evidence.<br>Owner checks base, direct and team access.<br>Approve the correction and retest effective access.','decision')
task=card(f,'b-task',1272,1144,640,192,
     '<b>7. Perform the scoped task [Staff]</b><br>Use the accepted identity and repository role.<br>Follow the applicable development/review flow.<br>Report access that differs from the agreed policy.')
evidence=card(f,'b-evidence-node',2104,1144,840,192,
     '<b>8. Record outcome and relevant audit evidence</b><br>Retain identity, team/repository context and timestamps as agreed.<br>Capture denied/unexpected behavior and route it to an owner.<br>Separate identity, membership, permission and branch-policy failures.')
card(f,'b-lifecycle-policy',440,1432,1472,224,
     '<b>Joiner, mover and leaver events trigger membership/access review</b><br>Reconcile Entra assignments, organization membership, teams and direct/collaborator roles as applicable.<br>Verify propagation, session and human-credential handling for the selected account model.<br>Inventory automation/App/deploy-key access separately; removal from one group may leave another access path.','context')
lifecycle=card(f,'b-lifecycle',2104,1432,840,224,
     '<b>9. Maintain access [Identity + GitHub owners]</b><br>Reconcile identities, groups, teams and repository roles.<br>Review role changes, departures and the agreed cadence.<br>Verify removal and resolve remaining access paths.<br>Update the access catalog, support guidance and audit record.')
link(f,'b-l1',request,membership,'Need','bottom','top')
link(f,'b-l2',membership,auth,'Approved')
link(f,'b-l3',auth,identity,'Identity')
link(f,'b-l4',identity,evaluate,'Context','bottom','top')
link(f,'b-l5',evaluate,allowed,'Allowed')
link(f,'b-l6',allowed,task,'Task','bottom','top')
link(f,'b-l7',task,evidence,'Outcome')
link(f,'b-l8',evidence,lifecycle,'Review','bottom','top')
link(f,'b-auth-fail-link',auth,authfail,'Blocked','top','bottom')
link(f,'b-map-fail-link',identity,mapfail,'Mismatch','top','bottom')
link(f,'b-denied-link',evaluate,denied,'Denied','left','right')
link(f,'b-unexpected-link',task,unexpected,'Mismatch','left','right')
text(f,'b-evidence',64,1810,3024,
     'Proposed human-access flow. Validate deployment/plan, account model, provisioning/team mapping, credential journeys, base/repository roles and removal behavior before implementation.',18)

f=frame('p09c',5110,'09C Entra for GitHub: delivery plan and access validation',
        'Identity administrators / GitHub and repository owners / developers / QA | Draft | Verify the account model, prove group/team and repository access, then migrate in controlled groups.')
text(f,'c-work',64,244,3024,'Proposed work packages',bold=True)
phases=[]
for key,x,title,body,owner in [
 ('c-inventory',64,'1. Inventory accounts, teams and access',
  'Confirm GitHub deployment, plan and account model.<br>Map members, teams, repositories and direct grants.<br>Review base access and restricted-source boundaries.<br>Inventory human and automation credentials separately.',
  'Identity + GitHub owners + repo owners'),
 ('c-design',860,'2. Agree identity and team/role mappings',
  'Choose the supported Entra/GitHub integration.<br>Define groups, teams, owners and meaningful names.<br>Agree organization base and per-repository roles.<br>Plan membership, provisioning and removal changes.',
  'Identity + GitHub owners + team leads'),
 ('c-pilot',1656,'3. Prove representative staff access',
  'Configure limited mappings and reviewed permissions.<br>Test web and required Git/CLI/API credential paths.<br>Verify allowed/denied tasks and restricted repos.<br>Exercise membership removal, audit and recovery.',
  'Identity + GitHub owners + pilot users'),
 ('c-rollout',2452,'4. Migrate and maintain deliberately',
  'Roll out approved teams/mappings by cohort.<br>Verify access before retiring replaced grants/paths.<br>Document joiner/mover/leaver and support steps.<br>Review source boundaries and recurring access.',
  'GitHub + identity + repository owners'),
]:
 phases.append(card(f,key,x,328,636,256,f'<b>{title}</b><br>{body}'))
 text(f,key+'-owner',x,616,636,'Proposed owner: '+owner,18)
for i in range(3):link(f,'c-next-'+str(i),phases[i],phases[i+1],'Next')
for key,x,y,title in [('proof',64,744,'Evidence before broader migration'),('dependencies',1656,744,'Inputs and coordination'),
                      ('controls',64,1120,'Membership and repository controls'),('decisions',1656,1120,'Open decisions for review')]:
 text(f,'c-'+key+'-title',x,y,1432,title,bold=True)
card(f,'c-proof',64,824,1432,224,
     '• Representative users complete the supported account/SSO journey.<br>• Required web/Git/API actions work; restricted repos/actions stay denied.<br>• Base, team, inherited and direct access match the agreed model.<br>• Joiner/mover/leaver changes and remaining credentials are tested.<br>• Sync/session behavior, audit evidence, support and recovery are verified.','context')
card(f,'c-dependencies',1656,824,1432,224,
     '• Verified hosting/plan/account model and supported Entra features.<br>• Organization/enterprise owners, Entra admins and repository owners.<br>• Membership/group/team inventory and baseline task-to-role matrix.<br>• Restricted-source classifications and repository consolidation scope.<br>• Pilot users, recovery path, audit access and maintained user guidance.','context')
card(f,'c-controls',64,1200,1432,224,
     '• Reviewed group-to-team mappings and repository-role changes.<br>• Meaningful names, stable identifiers and accountable owners.<br>• Organization base permissions, direct access and collaborator review.<br>• Tested provisioning, membership removal and credential handling.<br>• Staged migration, administrative recovery and recurring access review.','decision')
card(f,'c-decisions',1656,1200,1432,224,
     '• Personal accounts + SAML SSO or Enterprise Managed Users?<br>• What plan/features and organization/enterprise integration scope?<br>• Which groups/teams, base permissions, repository roles and owners?<br>• How are outside collaborators and restricted sources handled?<br>• Which approvals, removal rules, support and elevation mechanisms apply?','decision')
card(f,'c-boundaries',64,1504,3024,160,
     '<b>Identity, membership and repository authorization are separate checks</b><br>Use the selected account model’s provisioning/group mechanism and verify <a href="https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization">GitHub repository roles</a>. Team synchronization is not a substitute for establishing organization membership.<br>Coordinate source-access boundaries with 02–04 and documentation with 06. Any temporary GitHub elevation needs its own supported design in 10; no automatic Google Cloud PAM-to-GitHub grant is assumed.','context')
text(f,'c-evidence',64,1810,3024,
     'Basis: proposal notes and Nov 12 discussion (06:54–10:37); official GitHub references checked Nov 16, 2026. Current hosting, license, account model, memberships and permissions remain to verify.',18)

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
E.ElementTree(svg).write(P/'proposal-09.canvas.svg',encoding='utf-8',xml_declaration=True)
print(f'Built 3 frames and {len(ids)} native widgets; bounds and connector references checked.')

