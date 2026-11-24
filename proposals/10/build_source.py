"""Build Proposal 10 as native editable Miro widgets.

After creation, use returned live identities to edit the existing board.
Do not recreate this composition on the same board.
"""
from pathlib import Path
import xml.etree.ElementTree as E

P=Path(__file__).parent; NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
svg=E.Element(f'{{{NS}}}svg',{'width':'11600','height':'32600'})
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
 f=el(svg,'g',id=key,transform=f'translate({x},30500)',data_frame=title)
 el(f,'rect',data_type='frame',x=0,y=0,width=3152,height=1910,fill='#ffffff',data_title=title)
 text(f,key+'-title',64,64,3024,title,33,True)
 text(f,key+'-subtitle',64,148,3024,subtitle)
 text(f,key+'-legend',64,1750,3024,'Blue = proposed | Gray = reported context or reference | Yellow = exception, boundary or team decision',18)
 return f

f=frame('p10a',-2560,'10A Role-based access and PAM: baseline plus temporary elevation',
        'CTO / developers / QA / DevOps / access owners | Draft | Give each job an agreed baseline and make additional privileged access scoped, eligible and time-bound.')
text(f,'a-current',64,244,880,'Inputs and the requested change',bold=True)
card(f,'a-team-model',64,320,880,192,
     '<b>Agree team structure and normal job needs</b><br>Identify application, QA, DevOps and other staff tasks.<br>Define the normal roles and resource/repository scope.<br>Use the identity and mapping models from 08 and 09.','context')
card(f,'a-inventory',64,552,880,192,
     '<b>Inventory standing access and existing controls</b><br>Review direct/group/inherited grants and current elevation tools.<br>Identify tasks that need temporary additional privileges.<br>Current entitlements, configuration and coverage remain to verify.','context')
card(f,'a-intent',64,784,880,224,
     '<b>Request temporary access for an explicit task</b><br>The Nov 12 discussion separates default access from elevation.<br>Read versus write was an example, not a universal role policy.<br>Agree the smallest useful privilege scope and its owner.','decision')
text(f,'a-proposed',1104,244,1984,'Proposed: maintained baseline and a separate temporary-access path',bold=True)
team=card(f,'a-team',1104,320,576,192,
     '<b>Agreed team / job role</b><br>Required day-to-day tasks.<br>Target product and environment.<br>Named role and access owners.')
group=card(f,'a-group',1808,320,576,192,
     '<b>Approved membership / mapping</b><br>Owned identity group and target mapping.<br>Joiner/mover/leaver approvals.<br>Eligibility is separately defined.')
baseline=card(f,'a-baseline',2512,320,576,192,
     '<b>Baseline access at the target</b><br>Approved role and resource/repo scope.<br>Maintained while separately authorized.<br>Normal task follows its existing controls.')
catalog=card(f,'a-catalog',1104,672,576,192,
     '<b>Predefined entitlement</b><br>Target system, resource scope and roles.<br>Eligible requesters and approval policy.<br>Maximum duration and accountable owner.')
request=card(f,'a-request',1808,672,576,192,
     '<b>Eligible user requests a grant</b><br>Select entitlement, reason and duration.<br>Apply configured approval/controls.<br>Pending or declined requests grant no access.')
grant=card(f,'a-grant',2512,672,576,192,
     '<b>Temporary access is activated</b><br>Verify the target privilege before use.<br>Record grant ID, start/end and actions.<br>Use only the approved task and scope.')
ending=card(f,'a-ending',1104,992,1984,160,
     '<b>Entitlement = access definition; grant = one time-bound activation</b><br>Expiry or supported revocation ends the temporary grant. Verify the elevated action is denied after propagation; investigate other grants if access remains.<br>Baseline access continues only while its separate membership/role authorization remains valid.','context')
link(f,'a-l1',team,group,'Map')
link(f,'a-l2',group,baseline,'Baseline')
link(f,'a-l3',catalog,request,'Request')
link(f,'a-l4',request,grant,'Authorized')
link(f,'a-l5',group,request,'Eligibility','bottom','top')
link(f,'a-l6',grant,ending,'Ends','bottom','top')
for key,x,w,title in [('outcomes',64,960,'Expected outcomes'),('fields',1088,960,'Entitlement catalog fields to agree'),('decisions',2112,976,'Decisions for the team')]:
 text(f,'a-'+key+'-title',x,1180,w,title,bold=True)
card(f,'a-outcomes',64,1244,960,192,
     '• Normal tasks use understandable baseline permissions.<br>• Additional privilege has a task, scope and end time.<br>• Owners can trace who requested, approved and used it.<br>• Removal is tested and lingering access gets follow-up.')
card(f,'a-fields',1088,1244,960,192,
     '• Meaningful name, purpose, target system and scope.<br>• Roles, eligible identities/groups and mapping.<br>• Approval/justification policy and maximum duration.<br>• Owner, audit, revocation and verification requirements.','context')
card(f,'a-decisions',2112,1244,976,192,
     '• Baseline versus elevated tasks and target systems.<br>• Eligible requesters, approvals and bounded duration.<br>• Activation/removal behavior, emergency access and support.<br>• Remaining standing grants, evidence and review cadence.','decision')
card(f,'a-targets',64,1500,3024,192,
     '<b>Choose and validate an elevation mechanism for each target</b><br>Google Cloud: evaluate <a href="https://docs.cloud.google.com/iam/docs/pam-overview">Google Cloud PAM</a> for selected IAM roles and resource scope using the identity model in <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690610675776">08A</a>.<br>GitHub: define a separate supported mechanism against <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690640001435">09A</a>. <a href="https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups">Entra PIM for Groups</a> is a candidate to evaluate; downstream activation/removal and sync delays must be proven. Google Cloud PAM is not a direct GitHub permission grant.','context')
text(f,'a-evidence',64,1810,3024,
     'Basis: proposal notes; Nov 12 discussion (07:43–10:37); Google PAM and Entra PIM references checked Nov 16, 2026. Targets, roles, policies and tools remain proposed.',18)

f=frame('p10b',1275,'10B Temporary elevation: request, authorize, use and verify removal',
        'Requester / access owners / approvers / elevation service / target operators | Draft | Verify access before the task and verify its removal when the grant ends.')
for key,y,h,label in [('request',264,224,'Requester / task'),('policy',552,224,'Eligibility / authorization'),
                       ('activate',840,224,'Target activation / checks'),('use',1128,224,'Task / grant ending'),
                       ('verify',1416,256,'Verification / audit owners')]:
 el(f,'rect',id='b-lane-'+key,x=64,y=y,width=3024,height=h,fill='#f7f7f7',stroke='none')
 text(f,'b-role-'+key,88,y+16,256,label,18,True)
need=card(f,'b-need',440,280,640,192,
     '<b>1. Identify a privileged task [Requester]</b><br>State target, operation and reason for more access.<br>Select an approved entitlement and duration.<br>If baseline is sufficient, use the normal workflow.')
denied=card(f,'b-denied',1272,280,640,192,
     '<b>Ineligible, declined or request expired</b><br>Return the policy/approval outcome to the requester.<br>Do not activate elevated access.<br>Correct the request or follow the agreed review path.','decision')
grantfail=card(f,'b-grant-failed',2104,280,840,192,
     '<b>Grant creation or activation fails</b><br>Track the actual grant/target state; do not assume access is active.<br>Assigned owners reconcile partial changes and record recovery.<br>Repeat verification or end the failed grant under the agreed policy.','decision')
validate=card(f,'b-validate',440,568,640,192,
     '<b>2. Validate request [Elevation service]</b><br>Check requester eligibility and entitlement scope.<br>Apply reason/duration requirements and limits.<br>Reject unsupported or out-of-scope requests.')
authorize=card(f,'b-authorize',1272,568,640,192,
     '<b>3. Authorize under the entitlement policy</b><br>Apply configured approval/control requirements.<br>Approver(s) decide where the policy requires them.<br>Pending requests grant no elevated access.')
issue=card(f,'b-issue',2104,568,840,192,
     '<b>4. Issue a time-bound grant [Elevation service]</b><br>Record requester, target, roles and grant start/end.<br>Proceed only when the configured policy is satisfied.<br>Track activation, expiry and assigned failure ownership.')
notactive=card(f,'b-not-active',440,856,640,192,
     '<b>Access is not active or scope is wrong</b><br>Hold the privileged task; owners check target state.<br>Check identity, roles and propagation status.<br>Repeat verification or end the failed grant.','decision')
verifyactive=card(f,'b-verify-active',1272,856,640,192,
     '<b>6. Verify effective access [Requester / owner]</b><br>Check the approved action on the correct target.<br>Confirm the grant is active before the task.<br>Record verification and the remaining time window.')
activate=card(f,'b-activate',2104,856,840,192,
     '<b>5. Apply target access [Selected mechanism]</b><br>Use the target-specific IAM or membership change.<br>Watch activation state and allow for propagation.<br>Google Cloud and GitHub implementations are validated separately.')
taskissue=card(f,'b-task-issue',440,1144,640,192,
     '<b>Task fails, overruns or needs early removal</b><br>Stop privileged work if the grant ends.<br>Use a new request for a new access window.<br>Record failure and use supported revocation as needed.','decision')
task=card(f,'b-task',1272,1144,640,192,
     '<b>7. Perform the approved task [Requester]</b><br>Use only the authorized operation and scope.<br>Follow change/review and runbook controls.<br>Record actions and results during the grant window.')
end=card(f,'b-end',2104,1144,840,192,
     '<b>8. End the grant [Service / authorized revoker]</b><br>Expiry ends elevation; supported revocation can end it earlier.<br>Track target removal and propagation under the selected mechanism.<br>Early task completion follows the agreed early-ending policy.')
mismatch=card(f,'b-removal-mismatch',440,1432,1472,224,
     '<b>Removal mismatch: keep follow-up open</b><br>If the elevated action still works, reconcile target bindings/membership, sessions and other grants.<br>Assign an access owner, record the exception and escalate unresolved removal.<br>Correct the approved scope and repeat the denial check; retain legitimate baseline access only while separately authorized.','decision')
close=card(f,'b-close',2104,1432,840,224,
     '<b>9. Verify the end and retain evidence [Owner / service]</b><br>Test that elevated access is denied after agreed propagation.<br>Check remaining grants if the action is still allowed.<br>Keep baseline only if its separate authorization remains valid.<br>Retain request, decision, grant, action and removal records.')
link(f,'b-l1',need,validate,'Needed','bottom','top')
link(f,'b-l2',validate,authorize,'Eligible')
link(f,'b-l3',authorize,issue,'Authorized')
link(f,'b-l4',issue,activate,'Activate','bottom','top')
link(f,'b-l5',activate,verifyactive,'Check','left','right')
link(f,'b-l6',verifyactive,task,'Verified','bottom','top')
link(f,'b-l7',task,end,'End policy')
link(f,'b-l8',end,close,'Ended','bottom','top')
link(f,'b-denied-link',authorize,denied,'No grant','top','bottom')
link(f,'b-grant-fail-link',issue,grantfail,'Failed','top','bottom')
link(f,'b-not-active-link',verifyactive,notactive,'Not ready','left','right')
link(f,'b-task-issue-link',task,taskissue,'Issue','left','right')
link(f,'b-removal-link',close,mismatch,'Still allowed','left','right')
text(f,'b-evidence',64,1810,3024,
     'Proposed target-neutral lifecycle. Approval stages, justification, duration, session/propagation behavior, early-ending capability, support and audit retention require per-target agreement.',18)

f=frame('p10c',5110,'10C Role-based access and PAM: delivery plan and validation',
        'Identity / platform and access owners / team leads / QA | Draft | Define baseline and entitlements, prove the complete grant lifecycle, then reduce unnecessary standing privilege.')
text(f,'c-work',64,244,3024,'Proposed work packages',bold=True)
phases=[]
for key,x,title,body,owner in [
 ('c-needs',64,'1. Agree baseline and elevated tasks',
  'Map jobs/groups to normal target access.<br>Identify tasks needing extra temporary privilege.<br>Review direct, inherited and overlapping grants.<br>Use 08/09 identity and mapping requirements.',
  'Team leads + identity + target owners'),
 ('c-design',860,'2. Design a target-specific catalog',
  'Define purpose, roles, scope and eligible identities.<br>Agree approval, justification and duration policy.<br>Assign owners, audit and removal requirements.<br>Choose a supported mechanism for each target.',
  'Access + identity + platform owners'),
 ('c-pilot',1656,'3. Prove one limited entitlement',
  'Test ineligible, pending and declined requests.<br>Verify active scope before the approved task.<br>Exercise expiry, supported revocation and delays.<br>Prove denial afterwards and audit completeness.',
  'Platform owner + requester/approver + QA'),
 ('c-rollout',2452,'4. Expand and review standing access',
  'Roll out reviewed entitlements in controlled scope.<br>Remove replaced standing grants after validation.<br>Publish request, support and recovery runbooks.<br>Review eligibility, usage and lingering access.',
  'Target + identity owners + team leads'),
]:
 phases.append(card(f,key,x,328,636,256,f'<b>{title}</b><br>{body}'))
 text(f,key+'-owner',x,616,636,'Proposed owner: '+owner,18)
for i in range(3):link(f,'c-next-'+str(i),phases[i],phases[i+1],'Next')
for key,x,y,title in [('proof',64,744,'Acceptance evidence before expansion'),('dependencies',1656,744,'Inputs and coordination'),
                      ('controls',64,1120,'Operating controls to agree'),('decisions',1656,1120,'Open decisions for review')]:
 text(f,'c-'+key+'-title',x,y,1432,title,bold=True)
card(f,'c-proof',64,824,1432,224,
     '• Baseline works; elevated operations are denied before activation.<br>• Ineligible, pending and declined requests do not gain privilege.<br>• Active grants permit only the agreed target operation/scope.<br>• Expiry/revocation removes elevation; valid baseline remains.<br>• Delays, remaining access, audit and failed-removal escalation are tested.','context')
card(f,'c-dependencies',1656,824,1432,224,
     '• Agreed team/job baseline and identity mappings from 08/09.<br>• Target roles, resource/repository scope and effective-access inventory.<br>• Supported elevation service, licensing/integration and owners.<br>• Requester/approver test identities and an approved pilot scope.<br>• Audit/alerts from 07 and owned catalog/runbooks through 06.','context')
card(f,'c-controls',64,1200,1432,224,
     '• Explicit administrators, eligible requesters, approvers and owners.<br>• Reviewed role/scope changes, justification and bounded duration.<br>• Verified activation/removal, audit trail and exception ownership.<br>• Emergency/recovery access and overdue-removal response.<br>• Recurring eligibility, overlapping-grant and standing-access review.','decision')
card(f,'c-decisions',1656,1200,1432,224,
     '• Which baseline/elevated tasks, roles and target scopes come first?<br>• Google Cloud PAM scope; any separately supported GitHub mechanism?<br>• Who is eligible, who approves, and what duration/reason is required?<br>• How are early ending, propagation/sessions and emergencies handled?<br>• Who owns removal failures, audit retention and recurring review?','decision')
card(f,'c-boundaries',64,1504,3024,160,
     '<b>Elevation grants access; the task still follows its normal change and execution controls</b><br>Use <a href="https://docs.cloud.google.com/iam/docs/pam-request-temporary-elevated-access">Google PAM grant lifecycle guidance</a> for the chosen cloud implementation. Prove target activation/removal; group-based downstream access must meet the required timing and scope.<br>Coordinate 08/09 identity decisions, 01 execution controls and 06/07 documentation/audit operations. Exact roles, target mechanisms, duration, approvals and rollout sequence remain decisions.','context')
text(f,'c-evidence',64,1810,3024,
     'Basis: Nov 12 discussion (07:43–10:37) and official Google/Microsoft references checked Nov 16, 2026. This is a proposed model; no entitlement, permission or group configuration is changed.',18)

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
E.ElementTree(svg).write(P/'proposal-10.canvas.svg',encoding='utf-8',xml_declaration=True)
print(f'Built 3 frames and {len(ids)} native widgets; bounds and connector references checked.')

