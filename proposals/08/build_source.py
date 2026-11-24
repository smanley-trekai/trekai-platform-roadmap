"""Build Proposal 08 as native editable Miro widgets.

After creation, use returned live identities to edit the existing board.
Do not recreate this composition on the same board.
"""
from pathlib import Path
import xml.etree.ElementTree as E

P=Path(__file__).parent; NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
svg=E.Element(f'{{{NS}}}svg',{'width':'11600','height':'26600'})
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
 f=el(svg,'g',id=key,transform=f'translate({x},24500)',data_frame=title)
 el(f,'rect',data_type='frame',x=0,y=0,width=3152,height=1910,fill='#ffffff',data_title=title)
 text(f,key+'-title',64,64,3024,title,33,True)
 text(f,key+'-subtitle',64,148,3024,subtitle)
 text(f,key+'-legend',64,1750,3024,'Blue = proposed | Gray = reported context or reference | Yellow = exception, boundary or team decision',18)
 return f

f=frame('p08a',-2560,'08A Entra ID for Google Cloud: sign-in and access model',
        'CTO / developers / QA / DevOps / identity owners | Draft | Centralize staff sign-in while explicitly designing Google Cloud roles, scope and group mappings.')
text(f,'a-current',64,244,880,'Requested changes and facts to establish',bold=True)
card(f,'a-intent',64,320,880,192,
     '<b>Use Microsoft Entra ID as the IdP</b><br>The proposal requests centralized staff sign-in to Google Cloud.<br>Inventory existing identity paths, users and required services before selecting the integration.','context')
card(f,'a-permissions',64,552,880,192,
     '<b>Plan, review and change Google Cloud permissions</b><br>The Nov 12 discussion calls for roles/groups that match team needs.<br>Review direct, group and inherited access at the relevant resource scope.','decision')
card(f,'a-naming',64,784,880,224,
     '<b>Make names and ownership meaningful</b><br>Agree team, product/environment and access-purpose naming.<br>Illustration only: qa-learning-nonprod-observe.<br>Record stable group identifiers, owners, target roles and scope; a name alone is not the mapping.','decision')
text(f,'a-proposed',1104,244,1984,'Proposed: separate identity trust from permission mapping',bold=True)
for key,x,label in [('entra',1104,'Microsoft Entra ID: identity and membership'),('google',2208,'Google Cloud: accepted identity and IAM')]:
 el(f,'rect',id='a-boundary-'+key,x=x,y=320,width=880,height=800,fill='#f7f7f7',stroke='none')
 text(f,'a-'+key+'-title',x+32,344,816,label,22,True)
auth=card(f,'a-auth',1136,424,816,192,
     '<b>Person authenticates with Entra ID</b><br>Staff use the agreed Google Cloud sign-in entry point.<br>Entra verifies identity under the approved sign-in policy.<br>Validate console and CLI journeys for the selected model.')
identity=card(f,'a-identity',2240,424,816,192,
     '<b>Google accepts the trusted identity</b><br>The selected integration establishes the cloud identity/session.<br>Federation versus managed-account provisioning is a design choice.<br>Sign-in success does not define resource permissions.')
groups=card(f,'a-groups',1136,824,816,192,
     '<b>Approved team/group membership</b><br>Agree job needs, group owner and membership approvals.<br>Map stable identifiers and required attributes/groups.<br>Lifecycle behavior depends on the chosen integration.')
iam=card(f,'a-iam',2240,824,816,192,
     '<b>Google Cloud IAM baseline access</b><br>Bind approved roles to the mapped identity/group at a defined scope.<br>Evaluate effective permissions, including other applicable grants.<br>Test intended actions and actions that must remain denied.')
link(f,'a-auth-link',auth,identity,'Sign-in trust')
mapping=link(f,'a-map-link',groups,iam,'Access mapping');mapping.set('stroke-dasharray','5,5')
link(f,'a-policy-link',identity,iam,'Check IAM','bottom','top')
text(f,'a-auth-note',1136,664,816,'Solid arrows: sign-in and access evaluation',18)
text(f,'a-map-note',1136,716,816,'Dashed arrow: group/attribute-to-role mapping',18)
for key,x,w,title in [('outcomes',64,960,'Expected outcomes'),('options',1088,960,'Integration choice to validate'),('decisions',2112,976,'Decisions for the team')]:
 text(f,'a-'+key+'-title',x,1180,w,title,bold=True)
card(f,'a-outcomes',64,1244,960,192,
     '• Staff follow a consistent, supported sign-in path.<br>• Team needs map to understandable baseline permissions.<br>• Membership, target role and scope have clear owners.<br>• Allowed, denied and revoked access can be demonstrated.')
card(f,'a-options',1088,1244,960,192,
     '<b>Evaluate Google-documented human identity options</b><br><a href="https://docs.cloud.google.com/iam/docs/workforce-identity-federation">Workforce Identity Federation</a>: external workforce identities.<br><a href="https://docs.cloud.google.com/architecture/identity/federating-gcp-with-azure-ad-configuring-provisioning-and-single-sign-on">Cloud Identity/Workspace + Entra SSO/provisioning</a>: managed accounts.<br>Validate services, console/CLI, group handling and lifecycle.<br>No integration option has been selected.','context')
card(f,'a-decisions',2112,1244,976,192,
     '• Identity integration and required service/client support.<br>• Team structure, group names/IDs and mapping owners.<br>• Baseline roles, resource scope and permission changes.<br>• Membership approvals, removal/session behavior and support.','decision')
card(f,'a-scope',64,1500,3024,192,
     '<b>Baseline access and temporary elevation are separate design decisions</b><br>Proposal 08 covers staff Google Cloud sign-in and the baseline permission model. Proposal 09 covers GitHub. Proposal 10 defines eligible temporary elevation, approval, scope and expiry for agreed targets.<br>Track service accounts and CI/workload identities separately. Maintain the access catalog and user guidance through <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690590495741">06B documentation maintenance</a>; validate effective access before replacing an existing path.','context')
text(f,'a-evidence',64,1810,3024,
     'Basis: proposal notes; Nov 12 discussion (06:54–10:37); Google identity/IAM references checked Nov 16, 2026. Current tenant configuration and effective grants remain to inventory.',18)

f=frame('p08b',1275,'08B Entra to Google Cloud: staff access and lifecycle',
        'Staff / access owners / Entra administrators / Google Cloud IAM owners | Draft | Confirm membership, sign in, evaluate scoped permissions and verify the access lifecycle.')
for key,y,h,label in [('request',264,224,'Staff / access request'),('identity',552,224,'Membership / Entra sign-in'),
                       ('iam',840,224,'Google Cloud / IAM'),('task',1128,224,'Staff task / evidence'),
                       ('lifecycle',1416,256,'Access owners / lifecycle')]:
 el(f,'rect',id='b-lane-'+key,x=64,y=y,width=3024,height=h,fill='#f7f7f7',stroke='none')
 text(f,'b-role-'+key,88,y+16,256,label,18,True)
request=card(f,'b-request',440,280,640,192,
     '<b>1. Identify the staff task [User]</b><br>Select product, environment and resource scope.<br>State the required operation and job need.<br>Use the agreed access request/sign-in route.')
authfail=card(f,'b-auth-fail',1272,280,640,192,
     '<b>Sign-in is blocked</b><br>Return identity/policy findings to support.<br>Entra owner resolves the authorized change.<br>Retry sign-in under the agreed policy.','decision')
mapfail=card(f,'b-map-fail',2104,280,840,192,
     '<b>Cloud identity or mapping is not accepted</b><br>Identity/Cloud owners check the selected trust and mapping.<br>Check the intended user, group attributes or provisioned identity.<br>Resolve the mismatch and repeat the affected checks.','decision')
membership=card(f,'b-membership',440,568,640,192,
     '<b>2. Confirm approved membership [Owner]</b><br>Match the job need to an owned access group.<br>Approve changes through the agreed process.<br>Check identity/group availability for the model.')
auth=card(f,'b-auth',1272,568,640,192,
     '<b>3. Authenticate [User + Entra ID]</b><br>Use the selected cloud sign-in entry point.<br>Apply the approved Entra sign-in controls.<br>Return identity information to the integration.')
identity=card(f,'b-identity',2104,568,840,192,
     '<b>4. Establish cloud identity [Selected integration]</b><br>Accept the trusted identity and required mappings.<br>Use the agreed federation or managed-account path.<br>Validate the supported console/CLI session and target service.')
denied=card(f,'b-denied',440,856,640,192,
     '<b>Denied or more access is needed</b><br>Check identity, mapping, target scope and policy.<br>Baseline changes require access-owner approval.<br>Eligible elevation follows Proposal 10 rules.','decision')
evaluate=card(f,'b-evaluate',1272,856,640,192,
     '<b>5. Evaluate permissions [Cloud IAM]</b><br>Resolve identity/group bindings and role scope.<br>Account for other applicable access policies.<br>Permit only an authorized action on the target.')
allowed=card(f,'b-allowed',2104,856,840,192,
     '<b>6. Confirm the allowed scope [User / access owner]</b><br>Use the intended project/resource and approved baseline role.<br>Verify the task can proceed within that permission scope.<br>Additional access remains subject to its approval/elevation process.')
unexpected=card(f,'b-unexpected',440,1144,640,192,
     '<b>Unexpected allow/deny behavior</b><br>Record identity, action, resource and evidence.<br>Owner reconciles direct/group/inherited access.<br>Review the correction and retest effective access.','decision')
task=card(f,'b-task',1272,1144,640,192,
     '<b>7. Perform the scoped task [User]</b><br>Use the accepted identity and authorized access.<br>Follow the applicable operational workflow.<br>Report access behavior that differs from policy.')
evidence=card(f,'b-evidence-node',2104,1144,840,192,
     '<b>8. Record outcome and relevant audit evidence</b><br>Retain identity/group context, target scope and timestamps as agreed.<br>Capture denied/unexpected actions and route them to an owner.<br>Separate identity failures from permission or application failures.')
card(f,'b-lifecycle-policy',440,1432,1472,224,
     '<b>Joiner, mover and leaver events trigger access maintenance</b><br>Approved membership changes must reach the selected identity integration and Google Cloud permission model.<br>Verify additions, role changes and removals, including direct grants that could retain access.<br>Agree propagation and active-session handling; test removal rather than assume immediate revocation.','context')
lifecycle=card(f,'b-lifecycle',2104,1432,840,224,
     '<b>9. Maintain access [Identity + Cloud owners]</b><br>Reconcile membership, identity mappings and IAM policy.<br>Review access on role changes, departures and the agreed cadence.<br>Verify removal/session behavior and resolve remaining grants.<br>Update the access catalog, support guidance and audit record.')
link(f,'b-l1',request,membership,'Need','bottom','top')
link(f,'b-l2',membership,auth,'Approved')
link(f,'b-l3',auth,identity,'Sign-in')
link(f,'b-l4',identity,evaluate,'Identity','bottom','top')
link(f,'b-l5',evaluate,allowed,'Allowed')
link(f,'b-l6',allowed,task,'Task','bottom','top')
link(f,'b-l7',task,evidence,'Outcome')
link(f,'b-l8',evidence,lifecycle,'Review','bottom','top')
link(f,'b-auth-fail-link',auth,authfail,'Blocked','top','bottom')
link(f,'b-map-fail-link',identity,mapfail,'Mismatch','top','bottom')
link(f,'b-denied-link',evaluate,denied,'Denied','left','right')
link(f,'b-unexpected-link',task,unexpected,'Mismatch','left','right')
text(f,'b-evidence',64,1810,3024,
     'Proposed human-access flow. Exact provisioning/federation, claims/groups, approval mechanism, baseline permissions, session behavior and PAM eligibility remain design decisions.',18)

f=frame('p08c',5110,'08C Entra for Google Cloud: delivery plan and validation',
        'Identity administrators / Google Cloud owners / team leads / QA | Draft | Design roles and mappings, prove sign-in and effective permissions, then migrate in controlled groups.')
text(f,'c-work',64,244,3024,'Proposed work packages',bold=True)
phases=[]
for key,x,title,body,owner in [
 ('c-inventory',64,'1. Inventory identities and effective access',
  'Map staff, current sign-in paths and required services.<br>Review groups, direct grants and inherited access.<br>Separate human and workload identity needs.<br>Record owners and current administrative recovery.',
  'Identity + Cloud owners + team leads'),
 ('c-design',860,'2. Agree roles, naming and integration',
  'Define team-based baseline tasks, roles and scope.<br>Agree meaningful group names and stable mappings.<br>Choose a compatible human identity integration.<br>Plan reviewed permission changes and removal rules.',
  'Identity + Cloud owners + security leads'),
 ('c-pilot',1656,'3. Prove a representative pilot',
  'Configure the agreed limited identity/access scope.<br>Test developer/QA console, CLI and required services.<br>Verify allowed/denied tasks and membership removal.<br>Exercise audit, support and recovery paths.',
  'Identity + Cloud owners + pilot users'),
 ('c-rollout',2452,'4. Migrate and maintain deliberately',
  'Roll out reviewed mappings and permissions by cohort.<br>Verify access before retiring replaced paths/grants.<br>Document support and joiner/mover/leaver steps.<br>Review access and pass baseline needs to Proposal 10.',
  'Identity + Cloud owners + team leads'),
]:
 phases.append(card(f,key,x,328,636,256,f'<b>{title}</b><br>{body}'))
 text(f,key+'-owner',x,616,636,'Proposed owner: '+owner,18)
for i in range(3):link(f,'c-next-'+str(i),phases[i],phases[i+1],'Next')
for key,x,y,title in [('proof',64,744,'Evidence before broader migration'),('dependencies',1656,744,'Inputs and coordination'),
                      ('controls',64,1120,'Access and lifecycle controls'),('decisions',1656,1120,'Open decisions for review')]:
 text(f,'c-'+key+'-title',x,y,1432,title,bold=True)
card(f,'c-proof',64,824,1432,224,
     '• Representative users sign in through the supported console/CLI paths.<br>• Required tasks succeed and out-of-scope actions remain denied.<br>• Multiple memberships/direct/inherited grants match the access model.<br>• Membership changes and departures remove access as designed.<br>• Propagation/session behavior, audit evidence and recovery are tested.','context')
card(f,'c-dependencies',1656,824,1432,224,
     '• Current Entra/directory setup, identity identifiers and existing groups.<br>• Cloud organization/folder/project policies and resource owners.<br>• Required product/service/client support for the chosen integration.<br>• Baseline task matrix, reviewed permission changes and pilot users.<br>• Administrative recovery, audit collection and owned documentation.','context')
card(f,'c-controls',64,1200,1432,224,
     '• Approved baseline roles with explicit resource scope and ownership.<br>• Reviewed group mappings, naming, membership and IAM changes.<br>• Joiner/mover/leaver checks and handling of remaining direct grants.<br>• Staged migration with tested support and administrative recovery.<br>• Access catalog, audit evidence and recurring ownership review.','decision')
card(f,'c-decisions',1656,1200,1432,224,
     '• Workforce federation or managed accounts + Entra SSO/provisioning?<br>• Which console/CLI users, services and resource scopes are required?<br>• Which team/group names, stable IDs, baseline roles and owners?<br>• Who approves membership, permission changes and cutover?<br>• What removal/session behavior, support and PAM handoffs apply?','decision')
card(f,'c-boundaries',64,1504,3024,160,
     '<b>Authentication, authorization and elevation each need their own validation</b><br>Entra establishes staff identity; <a href="https://docs.cloud.google.com/iam/docs/overview">Google Cloud IAM</a> determines allowed actions on resources. Select and validate the integration before configuring the production access path.<br>Proposal 09 handles GitHub; 10 defines target-specific temporary elevation. This proposal does not prescribe universal read/write roles, a fixed migration date or changes to CI/service-account access.','context')
text(f,'c-evidence',64,1810,3024,
     'Basis: Nov 12 discussion (06:54–10:37) and Google identity/IAM documentation checked Nov 16, 2026. Team structure, tenant setup, effective permissions and implementation choice remain to verify.',18)

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
E.ElementTree(svg).write(P/'proposal-08.canvas.svg',encoding='utf-8',xml_declaration=True)
print(f'Built 3 frames and {len(ids)} native widgets; bounds and connector references checked.')

