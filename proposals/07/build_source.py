"""Build Proposal 07 as native editable Miro widgets.

After creation, use returned live identities to edit the existing board.
Do not recreate this composition on the same board.
"""
from pathlib import Path
import xml.etree.ElementTree as E

P=Path(__file__).parent; NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
svg=E.Element(f'{{{NS}}}svg',{'width':'11600','height':'23600'})
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
 f=el(svg,'g',id=key,transform=f'translate({x},21500)',data_frame=title)
 el(f,'rect',data_type='frame',x=0,y=0,width=3152,height=1910,fill='#ffffff',data_title=title)
 text(f,key+'-title',64,64,3024,title,33,True)
 text(f,key+'-subtitle',64,148,3024,subtitle)
 text(f,key+'-legend',64,1750,3024,'Blue = proposed | Gray = reported context or reference | Yellow = exception, boundary or team decision',18)
 return f

f=frame('p07a',-2560,'07A Observability and alerting: signals to response',
        'CTO / developers / QA / DevOps | Draft | Use relevant signals to detect impact, notify an accountable responder and verify recovery.')
text(f,'a-current',64,244,880,'Reported context and the requested improvement',bold=True)
card(f,'a-context',64,320,880,192,
     '<b>Observability tools are reported as deployed</b><br>The Nov 12 discussion questioned their effective use and the visibility of alerts.<br>Current coverage and configuration still need verification.','context')
card(f,'a-request',64,552,880,192,
     '<b>Explicit request: enable alerting for the team</b><br>Turn useful symptoms into actionable notifications.<br>Route by service, environment and severity to a responsible role.<br>Agree backup and escalation coverage.','decision')
card(f,'a-check',64,784,880,192,
     '<b>Start by checking the complete path</b><br>Inventory tools, instrumentation, rules and destinations.<br>Check whether notifications reach the intended people.<br>Record detection and response gaps with owners.','context')
text(f,'a-proposed',1104,244,1984,'Proposed: an observable service and an accountable response path',bold=True)
work=card(f,'a-workload',1104,320,576,192,
     '<b>1. Workload and dependencies</b><br>Apps, infrastructure and data services.<br>Critical journeys and availability probes.<br>Identify product, environment and version.')
signals=card(f,'a-signals',1808,320,576,192,
     '<b>2. Relevant telemetry</b><br>Availability, errors, latency and capacity.<br>Metrics/logs; traces where useful.<br>Include environment and instance context.')
platform=card(f,'a-platform',2512,320,576,192,
     '<b>3. Ingest, store and query</b><br>Dashboards and investigation links.<br>Check collection health and freshness.<br>Actual tools and coverage: verify first.')
rules=card(f,'a-rules',2512,672,576,192,
     '<b>4. Evaluate useful alert rules</b><br>Agree thresholds and time windows.<br>Define missing-data behavior.<br>Severity and routing match the impact.')
notify=card(f,'a-notify',1808,672,576,192,
     '<b>5. Deliver a useful notification</b><br>Named destination and primary/backup.<br>Include impact, scope and runbook link.<br>Channels and recipients: team decision.')
respond=card(f,'a-respond',1104,672,576,192,
     '<b>6. Acknowledge and respond</b><br>Assign incident ownership; investigate.<br>Mitigate and verify service recovery.<br>Record outcome and follow-up actions.')
link(f,'a-l1',work,signals,'Emit')
link(f,'a-l2',signals,platform,'Collect')
link(f,'a-l3',platform,rules,'Evaluate','bottom','top')
link(f,'a-l4',rules,notify,'Route','left','right')
link(f,'a-l5',notify,respond,'Notify','left','right')
card(f,'a-investigation',1104,992,1984,160,
     '<b>Developers and QA also inspect signals directly</b><br>Developers correlate failures with service/release context. QA observes test behavior and saves evidence tied to the manifest and instance.<br>Alerting complements investigation; a missing signal must have an explicit policy.','context')
for key,x,w,title in [('outcomes',64,960,'Expected outcomes'),('coverage',1088,960,'Coverage to agree'),('decisions',2112,976,'Decisions for the team')]:
 text(f,'a-'+key+'-title',x,1180,w,title,bold=True)
card(f,'a-outcomes',64,1244,960,192,
     '• Detect meaningful impact and collection gaps.<br>• Give developers/QA usable investigation evidence.<br>• Reach an accountable responder with useful context.<br>• Verify recovery and improve noisy or missing rules.')
card(f,'a-coverage',1088,1244,960,192,
     '• Critical services, dependencies and user journeys.<br>• Availability, errors, latency and resource saturation.<br>• Telemetry/notification delivery health.<br>• Product, environment, release and instance labels.','context')
card(f,'a-decisions',2112,1244,976,192,
     '• Tools, instrumentation and useful service targets.<br>• Rule thresholds, windows, severity and no-data policy.<br>• Destinations, primary/backup and response coverage.<br>• Escalation, retention, access and review cadence.','decision')
card(f,'a-environments',64,1500,3024,192,
     '<b>Match alerting to the environment purpose</b><br>Temporary QA needs test/instance context and expected expiry/cleanup handling. Customer demos, client pilots and production need agreed stable-service monitoring and support coverage.<br>Use <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503905">05B environment lifecycle</a> to scope QA behavior and <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690590495741">06B documentation maintenance</a> for owned runbooks. Test alerts and maintenance silences need a clear scope and end.','context')
text(f,'a-evidence',64,1810,3024,
     'Basis: proposal notes and Nov 12 discussion (05:56–06:42). Current gaps are reported concerns; actual tools, live rules, channels, recipients and response arrangements remain to verify.',18)

f=frame('p07b',1275,'07B Observability: detect, notify, respond and verify recovery',
        'Workloads / observability operators / responders / developers / QA | Draft | Prove the full notification and response path, including failures and missing acknowledgements.')
for key,y,h,label in [('signal',264,224,'Workloads / signals'),('detect',552,224,'Detection / routing'),
                       ('respond',840,224,'Responders / investigation'),('recover',1128,224,'Mitigation / recovery'),
                       ('review',1416,256,'Closure / improvement')]:
 el(f,'rect',id='b-lane-'+key,x=64,y=y,width=3024,height=h,fill='#f7f7f7',stroke='none')
 text(f,'b-role-'+key,88,y+16,256,label,18,True)
emit=card(f,'b-emit',440,280,640,192,
     '<b>1. Produce signals [Workload / probe]</b><br>Emit selected service/dependency telemetry.<br>Tag product, environment, release and instance.<br>Include probe results for agreed user journeys.')
nodata=card(f,'b-nodata',1272,280,640,192,
     '<b>Missing or stale telemetry</b><br>Evaluate the agreed absence/staleness window.<br>Distinguish expected QA expiry from failure.<br>Route actionable loss of visibility via Step 4.','decision')
deliveryfail=card(f,'b-delivery-fail',2104,280,840,192,
     '<b>Notification delivery fails</b><br>Record the failed route and use the agreed alternate destination.<br>Assign an owner to restore the notification path.<br>Validate delivery again; do not treat a sent event as receipt.','decision')
collect=card(f,'b-collect',440,568,640,192,
     '<b>2. Collect and check [Observability]</b><br>Ingest/store/query the relevant signals.<br>Check collection health and freshness.<br>Preserve context for dashboards and evidence.')
evaluate=card(f,'b-evaluate',1272,568,640,192,
     '<b>3. Evaluate rule [Alerting system]</b><br>Apply agreed condition, window and severity.<br>Group duplicates and check scoped silences.<br>If no condition fires, continue observation.')
deliver=card(f,'b-deliver',2104,568,840,192,
     '<b>4. Notify the responsible role [Routing]</b><br>Select service/environment primary and backup coverage.<br>Send scope, symptom, severity, evidence and runbook link.<br>Check channel delivery and start the agreed acknowledgement timer.')
escalate=card(f,'b-escalate',440,856,640,192,
     '<b>No acknowledgement within agreed time</b><br>Escalate to the designated backup/support role.<br>Confirm someone accepts incident ownership.<br>Coverage and escalation timing remain to agree.','decision')
ack=card(f,'b-ack',1272,856,640,192,
     '<b>5. Acknowledge [Primary / backup]</b><br>Confirm receipt and name the incident owner.<br>Assess impact and start the incident record.<br>Escalate if coverage or expertise is insufficient.')
investigate=card(f,'b-investigate',2104,856,840,192,
     '<b>6. Investigate [Responder + service owner]</b><br>Correlate dashboards/logs/traces with the affected version.<br>Use the runbook; involve developers or QA as relevant.<br>Separate product, environment and telemetry failures.')
actionfail=card(f,'b-action-fail',440,1144,640,192,
     '<b>Mitigation fails or impact stays unclear</b><br>Keep the incident open and reassess Step 6.<br>Escalate to the appropriate service owner.<br>Record failed actions and the next decision.','decision')
mitigate=card(f,'b-mitigate',1272,1144,640,192,
     '<b>7. Mitigate [Authorized operator]</b><br>Choose a scoped action using the runbook.<br>Use existing change/access controls.<br>Record the action, owner and observed result.')
verify=card(f,'b-verify',2104,1144,840,192,
     '<b>8. Verify recovery [Responder / QA as needed]</b><br>Check the affected service/journey and fresh telemetry.<br>Confirm recovery against agreed conditions, not only alert status.<br>If still unhealthy, return to Step 6; keep incident ownership.')
card(f,'b-policy',440,1432,1472,224,
     '<b>Keep an operating record and control expected noise</b><br>Record environment/instance, impact, timeline, acknowledgement, actions and recovery evidence.<br>Scope test/maintenance silences and their expiry; align temporary QA rules with the environment lifecycle.<br>Review notification-path health and stale collection separately from workload health.','context')
close=card(f,'b-close',2104,1432,840,224,
     '<b>9. Close and improve [Incident / service owner]</b><br>Communicate recovery through the agreed incident process.<br>Retain evidence and assign unresolved follow-up work.<br>Tune missing/noisy rules and update the owned runbook.<br>Repeat validation after rule, route or ownership changes.')
link(f,'b-l1',emit,collect,'Signals','bottom','top')
link(f,'b-l2',collect,evaluate,'Fresh data')
link(f,'b-l3',evaluate,deliver,'Alert')
link(f,'b-l4',deliver,ack,'Delivered','bottom','top')
link(f,'b-l5',ack,investigate,'Owned')
link(f,'b-l6',investigate,mitigate,'Action','bottom','top')
link(f,'b-l7',mitigate,verify,'Check')
link(f,'b-l8',verify,close,'Recovered','bottom','top')
link(f,'b-nodata-link',evaluate,nodata,'No data','top','bottom')
link(f,'b-delivery-link',deliver,deliveryfail,'Failed','top','bottom')
link(f,'b-escalate-link',ack,escalate,'No ack','left','right')
link(f,'b-action-link',mitigate,actionfail,'Failed','left','right')
text(f,'b-evidence',64,1810,3024,
     'Proposed operating flow. Tool capabilities, alert conditions, notification channels, acknowledgement tracking, incident process and response coverage require team agreement and testing.',18)

f=frame('p07c',5110,'07C Observability and alerting: delivery plan and controls',
        'DevOps / service owners / developers / QA | Draft | Verify existing coverage, agree actionable rules, then test delivery, response and recovery before expanding.')
text(f,'c-work',64,244,3024,'Proposed work packages',bold=True)
phases=[]
for key,x,title,body,owner in [
 ('c-inventory',64,'1. Verify the existing setup',
  'Inventory tools, signals, dashboards and rules.<br>Map services, dependencies and environments.<br>Check destinations and current ownership.<br>Prioritize gaps around critical user impact.',
  'DevOps + service owners'),
 ('c-design',860,'2. Agree alerts and response coverage',
  'Define symptoms, severity and rule windows.<br>Choose thresholds and missing-data behavior.<br>Name primary/backup roles and destinations.<br>Agree acknowledgement and escalation timing.',
  'Service owners + DevOps + support leads'),
 ('c-configure',1656,'3. Configure a focused first scope',
  'Complete required instrumentation and labels.<br>Connect dashboards, rules and notification routes.<br>Prepare runbooks and incident records.<br>Include telemetry and delivery-path health.',
  'DevOps + developers + service owners'),
 ('c-validate',2452,'4. Exercise, tune and expand',
  'Test controlled impact and absent/stale data.<br>Prove delivery, acknowledgement and escalation.<br>Verify recovery, noise handling and QA expiry.<br>Expand coverage and assign recurring review.',
  'QA + responders + DevOps'),
]:
 phases.append(card(f,key,x,328,636,256,f'<b>{title}</b><br>{body}'))
 text(f,key+'-owner',x,616,636,'Proposed owner: '+owner,18)
for i in range(3):link(f,'c-next-'+str(i),phases[i],phases[i+1],'Next')
for key,x,y,title in [('proof',64,744,'Acceptance evidence before expansion'),('dependencies',1656,744,'Inputs and coordination'),
                      ('controls',64,1120,'Operating controls to agree'),('decisions',1656,1120,'Open decisions for review')]:
 text(f,'c-'+key+'-title',x,y,1432,title,bold=True)
card(f,'c-proof',64,824,1432,224,
     '• Controlled failure creates the expected scoped alert and context.<br>• Actual primary receives it; acknowledgement/ownership is recorded.<br>• Failed delivery and no acknowledgement exercise alternate/escalation paths.<br>• Fresh signals and the affected journey confirm recovery.<br>• Missing data, duplicate noise, silences and temporary QA expiry are tested.','context')
card(f,'c-dependencies',1656,824,1432,224,
     '• Verified tool configuration and access to relevant telemetry.<br>• Critical-service inventory, labels and agreed impact targets.<br>• Supported notification destinations and response arrangements.<br>• Approved test scenarios and environment/release context from 05.<br>• Owned runbooks and maintenance workflow from 06.','context')
card(f,'c-controls',64,1200,1432,224,
     '• Version/review rule and routing changes; retain test evidence.<br>• Primary/backup ownership, escalation and support coverage.<br>• Grouping, scoped silence expiry and periodic noise/coverage review.<br>• Data minimization/redaction, access, retention and collection cost.<br>• Observe the telemetry and notification paths as well as workloads.','decision')
card(f,'c-decisions',1656,1200,1432,224,
     '• Which tools, services, journeys and signals are in the first scope?<br>• Which impact targets, thresholds, windows and no-data rules apply?<br>• Which channels, responding roles, hours and escalation timings?<br>• How do QA, demo, pilot and production policies differ?<br>• Who owns rule/runbook changes, retention, cost and recurring tests?','decision')
card(f,'c-boundaries',64,1504,3024,160,
     '<b>Completion means the alert reaches an accountable responder and recovery is verified</b><br>A deployed dashboard or a configured rule alone does not demonstrate the full operating path. Capture evidence from signal through receipt, response and recovery.<br>Validate and extend the existing setup first. Tool replacement, numeric service targets, 24/7 coverage, named recipients and implementation dates are decisions, not commitments.','context')
text(f,'c-evidence',64,1810,3024,
     'Basis: Nov 12 request to enable alerting. This is a proposed delivery approach; current tools, coverage, rules, routes and operating ownership have not been re-audited here.',18)

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
E.ElementTree(svg).write(P/'proposal-07.canvas.svg',encoding='utf-8',xml_declaration=True)
print(f'Built 3 frames and {len(ids)} native widgets; bounds and connector references checked.')

