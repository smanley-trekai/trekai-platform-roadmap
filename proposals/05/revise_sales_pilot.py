"""Build the authorized 05 revision against a fresh, scoped live snapshot.

Run once against proposal-05.before-sales-pilot.svg. The patch preserves live
widget identities and frame positions; it is not a fresh-board creation file.
"""
from pathlib import Path
import copy
import json
import xml.etree.ElementTree as E

P = Path(__file__).parent
N = '{http://www.w3.org/2000/svg}'
E.register_namespace('', N[1:-1])
live = E.parse(P/'proposal-05.before-sales-pilot.svg').getroot()
created = E.fromstring(json.loads((P/'proposal-05.created.json').read_text())['result_svg'])
friendly = {e.get('id'): e.get('data-miro-id') for e in created.iter() if e.get('id')}
current = {e.get('data-miro-id'): e for e in live.iter() if e.get('data-miro-id')}
patch = E.Element(N+'svg')
frames = {}
titles = {
 'p05a': '05A QA, sales demo and client pilot: proposal',
 'p05b': '05B QA, demo and pilot: provision, accept, operate and retire',
 'p05c': '05C QA, demo and pilot: delivery plan and operating controls',
}
for key, title in titles.items():
 old = current[friendly[key]]
 frame = E.SubElement(patch, N+'g', dict(old.attrib))
 frame.set('data-frame', title)
 bg = copy.deepcopy(old[0]); bg.set('data-title', title); frame.append(bg)
 frames[key] = frame

changes = {}
def change(frame, key, body):
 old = current[friendly[key]]
 tag = old.tag
 attrs = dict(old.attrib) if tag == N+'line' else {'id': old.get('id'), 'data-miro-id': old.get('data-miro-id')}
 attrs.pop('data-rendered-bounds', None)
 assert old.get('data-locked') != 'true' and old.get('data-read-only') != 'true'
 el = E.SubElement(frames[frame], tag, attrs)
 if tag == N+'textArea':
  el.text = body
 else:
  el.set('data-content', body)
 changes[key] = body

for k, title in titles.items(): change(k, k+'-title', title)
change('p05a','p05a-subtitle','QA / sales / product / DevOps | Draft | Separate internal testing, fully working customer demonstrations and production-like student pilots.')
change('p05a','a-current','Saved baseline and clarified requirement')
change('p05a','a-need','<b>Scope clarified by the project owner</b><br>Add internal QA, sales demo/POC and client pilot environments.<br>Customer-facing workflows must function end to end.<br>Pilots must accommodate multiple students.')
change('p05a','a-proposed','Proposed: reusable templates, three distinct environment purposes')
change('p05a','a-entry','<b>QA, sales or a pilot owner requests an approved environment</b><br>Select product, release manifest and purpose-specific profile; assign business and technical owners.<br>Reuse provisioning code with separate configuration, access, data, capacity and lifecycle policies.')
change('p05a','a-example-title','Three purposes, not a fixed instance count; capacity and isolation remain to agree')
change('p05a','a-functional','<b>Internal QA</b><br>Functional, load and recovery testing.<br>Repeatable test accounts and data.<br>May reset or run disruptive experiments.<br>Isolate impact from customer sessions.')
change('p05a','a-load','<b>Sales demo / proof of concept</b><br>Fully working agreed product workflows.<br>Ready accounts, data and integrations.<br>Rehearse before client demonstrations.<br>Stable sessions; reset on an agreed schedule.')
change('p05a','a-poc','<b>Client pilot</b><br>Production-like, working user journeys.<br>Agreed concurrent students and teachers.<br>Persistent data, monitoring and support.<br>Controlled changes and owner-led retirement.')
change('p05a','a-isolation','<b>Protect customer use from QA resets, load and fault tests</b><br>Separate environment identities, data, deployment targets and state; choose shared infrastructure or dedicated project/cluster by impact.<br>Identify shared dependencies and validate isolation. A namespace alone may not contain every test or failure.')
change('p05a','a-benefits','• QA can reproduce versions and test independently.<br>• Sales can demonstrate complete, rehearsed workflows.<br>• Clients can run a supported, multi-student pilot.<br>• Reuse templates while operating each purpose separately.')
change('p05a','a-manifest','• Artifact/template versions, settings and dependencies.<br>• Data profile, account setup and secret references.<br>• Purpose, owners, capacity and acceptance criteria.<br>• Change, retention, reset and retirement policies.')
change('p05a','a-lifecycle','• QA: approved expiry, reset and managed cleanup.<br>• Demo: stable sessions; controlled data refresh/reset.<br>• Pilot: retain active data; approved changes and end date.<br>• Define monitoring, support, recovery and cost owners.')
change('p05a','a-boundary','<b>“Fully functioning” needs evidence before customer handoff</b><br>All agreed end-to-end workflows, accounts and integrations must pass; pilots must meet agreed concurrent-user and response/error criteria.<br>Terraform provisions infrastructure; app deployment and acceptance are separate. Use <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690359619683">01B execution controls</a> and approved artifacts from 03/04; production promotion remains a separate decision.')
change('p05a','a-evidence','Basis: Nov 12 discussion, Nov 2–3 snapshots and Nov 16 owner clarification. Proposed operating model; agree workload, capacity, owners and service targets before implementation.')

change('p05b','p05b-subtitle','QA / sales / pilot owner / automation / DevOps | Draft | Provision from code, verify by purpose, accept customer use, then follow the correct lifecycle.')
change('p05b','b-role-qa-request','QA / sales / pilot request')
change('p05b','b-role-qa-test','Acceptance / users / evidence')
change('p05b','b-request','<b>1. Request an environment [Owner]</b><br>Choose QA, sales demo/POC or client pilot.<br>Select manifest, profile, capacity and lifetime.<br>Name business and technical owners.')
change('p05b','b-invalid','<b>Incomplete or unauthorized request</b><br>Return findings to the requesting owner.<br>Correct inputs or obtain required approval.<br>Do not provision until the request is valid.')
change('p05b','b-partial','<b>Provisioning failed or only partly completed</b><br>Hold QA and customer handoff; no assumed rollback.<br>DevOps reconciles owned resources and state.<br>Record recovery or cleanup actions.')
change('p05b','b-policy','<b>2. Validate the request [Automation]</b><br>Check versions, access, purpose and limits.<br>Allocate instance ID and ownership scope.<br>Confirm capacity and required approvals.')
change('p05b','b-plan','<b>3. Review the final target plan</b><br>Select purpose-specific inputs and isolated state.<br>Authorize execution under the agreed policy.<br>Apply controls: <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690359619683">01B</a> (review or approved policy).')
change('p05b','b-apply','<b>4. Provision infrastructure [Automation]</b><br>A scoped executor runs Terraform for this environment.<br>Verify resources and capture required outputs.<br>Stop on failed or partial apply.')
change('p05b','b-deploy','<b>5. Deploy the selected release [Automation]</b><br>Install manifest versions, dependencies and integrations.<br>Prepare approved accounts, schema and purpose-specific data.<br>Application deployment is separate from Terraform apply.')
change('p05b','b-ready','<b>6. Check readiness [Automation]</b><br>Verify versions, health, access and integrations.<br>Check accounts, data and monitoring setup.<br>Send a ready instance for acceptance checks.')
change('p05b','b-not-ready','<b>Not ready: hold tests and handoff</b><br>Return deployment/readiness diagnostics.<br>Assigned owners correct the setup.<br>Repeat readiness checks before acceptance.')
change('p05b','b-tests','<b>7. Verify acceptance [QA + owner]</b><br>QA: functional, load and recovery checks.<br>Demo: rehearse agreed end-to-end workflows.<br>Pilot: verify workflows + concurrent students.<br>Keep evidence; owner signs off customer use.')
change('p05b','b-results','<b>8. Use the accepted environment [Owner / users]</b><br>QA executes tests; sales demos/POCs; client runs the pilot.<br>Save versions, outcomes, issues and support history.<br>Keep customer use stable under agreed change control.')
change('p05b','b-expiry','<b>Each purpose follows its own lifecycle</b><br>QA: completion/expiry can start approved reset or cleanup. Demo: reset between agreed sessions.<br>Pilot: keep active data and service; owner approves extension, export/retention and retirement.<br>No automatic QA cleanup of active customer use. Track costs, residual resources and failure owners.')
change('p05b','b-cleanup','<b>9. Reset or retire under the agreed policy</b><br>Confirm owner approval and data retention/export.<br>For retirement, stop deployment desired state first.<br>Clean only owned resources; protect shared services.<br>Verify residue, cost and evidence/closure records.')
change('p05b','b-l7','Accepted')
change('p05b','b-l8','Lifecycle')
change('p05b','b-evidence','Proposed workflow. Agree request interface, approvals, acceptance thresholds, monitoring/support, customer change windows and per-purpose data/lifecycle rules before implementation.')

# A native exception card fills the previously empty acceptance-lane column.
new = E.SubElement(frames['p05b'], N+'rect', {
 'id':'b-acceptance-failed','x':'440','y':'1144','width':'640','height':'192',
 'fill':'#ffe86d','stroke':'#cbb333','stroke-width':'2','data-text-color':'#574900',
 'data-font-family':'noto_sans','data-font-size':'22','data-text-align':'left',
 'data-text-align-vertical':'middle',
 'data-content':'<b>Acceptance fails: hold customer handoff</b><br>Record failed journeys or capacity checks.<br>Assign product/environment fixes to owners.<br>Repeat affected checks and obtain sign-off.'})
oldtests = current[friendly['b-tests']]
E.SubElement(frames['p05b'], N+'line', {
 'id':'b-acceptance-failed-link','x1':'1272','y1':'1240','x2':'1080','y2':'1240',
 'data-start':oldtests.get('id'),'data-end':'b-acceptance-failed',
 'data-start-side':'left','data-end-side':'right','stroke':'#313131',
 'stroke-width':'2','data-arrow':'end','data-shape':'elbowed','data-content':'Failed'})

change('p05c','p05c-subtitle','QA / sales / product / DevOps | Draft | Agree measurable requirements, prove each purpose, then operate customer environments with clear ownership.')
change('p05c','c-needs','<b>1. Agree requirements by purpose</b><br>QA test types; sales demonstration journeys.<br>Pilot student/teacher journeys and concurrency.<br>List integrations, data, duration and success criteria.<br>Check infrastructure-code coverage.')
change('p05c','c-design','<b>2. Design reusable environment profiles</b><br>Agree manifest, isolation, access and approvals.<br>Separate QA, demo and pilot configuration/data.<br>Set capacity, cost and operating policies.<br>Name business and technical owners.')
change('p05c','c-pilot','<b>3. Prove each profile in a trial</b><br>Recreate QA; rehearse a full sales demonstration.<br>Validate a production-like multi-student pilot.<br>Test integrations, recovery and failure handling.<br>Capture evidence and owner acceptance.')
change('p05c','c-expand','<b>4. Launch and operate agreed instances</b><br>Publish request and acceptance guidance.<br>Enable monitoring, support and change windows.<br>Schedule demo resets and pilot data recovery.<br>Review costs, feedback and owner-led retirement.')
change('p05c','c-needs-owner','Proposed owner: QA + sales + product + DevOps')
change('p05c','c-design-owner','Proposed owner: DevOps + product + security')
change('p05c','c-pilot-owner','Proposed owner: QA + sales + pilot owner')
change('p05c','c-expand-owner','Proposed owner: business owner + DevOps')
change('p05c','c-proof-title','Acceptance evidence before customer use')
change('p05c','c-proof','• All agreed workflows, accounts and integrations work end to end.<br>• Pilot meets concurrent-student and response/error thresholds.<br>• Approved versions, isolation and data persistence are verified.<br>• Monitoring, support and backup/restore are exercised as agreed.<br>• QA resets and failed/partial operations cannot disrupt customers.')
change('p05c','c-dependencies','• Reviewed modules, state scopes and execution identities.<br>• Release artifacts, deployment path and required integrations.<br>• Test/demo fixtures; approved pilot data, accounts and secrets.<br>• Monitoring, support routing, backup/restore and evidence storage.<br>• Environment ownership, cost visibility and cleanup reconciliation.')
change('p05c','c-controls','• Separate QA disruption from stable demo and pilot use.<br>• Budget, sizing, quotas and concurrency per environment purpose.<br>• Approved data handling, access and customer change windows.<br>• Named support/escalation owner and recovery expectations.<br>• QA expiry; scheduled demo resets; approved pilot retirement.')
change('p05c','c-decisions','• Which workflows, integrations and production similarities are required?<br>• How many concurrent users; which response/error targets and duration?<br>• Shared or dedicated resources; which dependencies need isolation?<br>• Who accepts, supports and authorizes changes for each purpose?<br>• Which data, backup/restore, retention and end-of-pilot rules apply?')
change('p05c','c-boundaries','<b>Agree “fully functioning” as measurable acceptance criteria</b><br>Every agreed workflow must pass with ready accounts, data and integrations; the pilot must support its agreed multi-student workload and operating requirements.<br>Use approved 03/04 artifacts and 01 execution controls; coordinate release policy with 11. Production promotion, availability targets and pilot-to-production transition require separate agreement.')
change('p05c','c-evidence','Basis: Nov 12 discussion and Nov 16 owner clarification. Three purposes share templates, not QA disruption or automatic cleanup. Counts, capacity, service targets, dates and named owners remain to agree.')

# Connector endpoints must be present in the sparse document.
tests_patch = next(e for e in frames['p05b'] if e.get('data-miro-id') == friendly['b-tests'])
assert tests_patch.get('id') == oldtests.get('id')
assert not any(e.get('data-deleted') for e in patch.iter())
E.indent(patch)
E.ElementTree(patch).write(P/'proposal-05.sales-pilot.patch.svg',encoding='utf-8',xml_declaration=True)
(P/'proposal-05.sales-pilot.expected.json').write_text(json.dumps({friendly[k]:v for k,v in changes.items()},ensure_ascii=False,indent=2)+'\n')
print(f'Prepared {len(changes)} content updates, 3 frame renames and 2 new native items.')
