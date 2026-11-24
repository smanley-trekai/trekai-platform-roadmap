"""Build Proposal 06 as native editable Miro widgets.

After creation, use returned live identities to edit the existing board.
Do not recreate this composition on the same board.
"""
from pathlib import Path
import xml.etree.ElementTree as E

P=Path(__file__).parent; NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
svg=E.Element(f'{{{NS}}}svg',{'width':'11600','height':'20600'})
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
 f=el(svg,'g',id=key,transform=f'translate({x},18500)',data_frame=title)
 el(f,'rect',data_type='frame',x=0,y=0,width=3152,height=1910,fill='#ffffff',data_title=title)
 text(f,key+'-title',64,64,3024,title,33,True)
 text(f,key+'-subtitle',64,148,3024,subtitle)
 text(f,key+'-legend',64,1750,3024,'Blue = proposed | Gray = reported context or reference | Yellow = exception, boundary or team decision',18)
 return f

f=frame('p06a',-2560,'06A Documentation and knowledge base: knowledge map',
        'CTO / developers / QA / DevOps | Draft | Make trustworthy DevOps, cloud and product knowledge easy to find, understand and maintain.')
text(f,'a-current',64,244,880,'Reported gaps and their effect',bold=True)
card(f,'a-fragmented',64,320,880,192,
     '<b>P1: Incomplete and fragmented information</b><br>The proposal notes identify missing or scattered documentation.<br>Readers may not know where the authoritative explanation lives.','context')
card(f,'a-outdated',64,544,880,192,
     '<b>P2: Useful material, but freshness is uncertain</b><br>The Nov 12 discussion reports useful Confluence and product pages, with many pages outdated.<br>This is a reported concern, not a new page-by-page audit.','context')
card(f,'a-impact',64,768,880,224,
     '<b>Why this matters</b><br>Teams need to understand systems without repeated walkthroughs.<br>Outdated instructions create uncertainty during delivery and support.<br>Start with DevOps, then cloud architecture and product knowledge.','decision')
text(f,'a-proposed',1104,244,1984,'Proposed: one clear entry point, linked authoritative sources',bold=True)
card(f,'a-entry',1104,320,1984,160,
     '<b>Knowledge index: browse by task, role, product or environment</b><br>Point readers to the authoritative page or repository for each topic; avoid competing copies.<br>Assign a content owner and show status, scope, last verification and the source/version used.')
text(f,'a-domains-title',1104,544,1984,'Content map: DevOps first, then cloud architecture and TrekAI products',bold=True)
for key,x,title,body in [
 ('a-devops',1104,'DevOps: how to operate and deliver',
  'Terraform and infrastructure changes.<br>CI/CD, GitOps and release handoffs.<br>QA provisioning, expiry and cleanup.<br>Runbooks, troubleshooting and recovery.'),
 ('a-cloud',1776,'Cloud: how the environment fits together',
  'Environment and component maps.<br>Networking, identity and access.<br>Dependencies, data services and boundaries.<br>Link diagrams to configuration and evidence.'),
 ('a-products',2448,'Products: how TrekAI works',
  'Trek Learning: Hub / LMS.<br>TrekCAP engine and TrekFinder application.<br>Service interactions and user journeys.<br>Dependencies, setup and product terminology.'),
]:card(f,key,x,608,608,256,f'<b>{title}</b><br>{body}')
card(f,'a-authority',1104,928,1984,160,
     '<b>Match the explanation to an identifiable system state</b><br>Link maintained how-to pages to code/configuration, release versions and dated evidence; distinguish current behavior from proposals.<br>Choose page-versus-repository ownership by content type. The entry point does not require moving every document into one tool.','decision')
for key,x,w,title in [('outcomes',64,960,'Expected outcomes'),('template',1088,960,'Proposed page minimum'),('decisions',2112,976,'Decisions for the team')]:
 text(f,'a-'+key+'-title',x,1180,w,title,bold=True)
card(f,'a-outcomes',64,1244,960,192,
     '• Readers find the right instructions and scope.<br>• Onboarding and support need fewer repeated explanations.<br>• Verified steps can be reused across the team.<br>• Owners resolve stale pages and conflicting copies.')
card(f,'a-template',1088,1244,960,192,
     '• Purpose, audience and applicable product/environment.<br>• Prerequisites, steps, expected result and failure path.<br>• Owner, review status, verification date and version.<br>• Authoritative references and related diagrams/runbooks.','context')
card(f,'a-decisions',2112,1244,976,192,
     '• Entry point and authoritative source for each topic.<br>• Content owners, reviewers and access boundaries.<br>• Priority gaps, page templates and review cadence.<br>• How delivery changes trigger documentation updates.','decision')
card(f,'a-example',64,1500,3024,192,
     '<b>Concrete starting point: the temporary QA environment guide</b><br>Explain how QA selects a manifest, starts the approved infrastructure workflow, checks readiness, runs tests and closes the environment; include expiry, cost ownership and cleanup failures.<br>Link the guide to <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503905">05B environment workflow</a> and <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690359619683">01B execution controls</a>. Documentation follows the agreed implementation and must identify the version it describes.','context')
text(f,'a-evidence',64,1810,3024,
     'Basis: proposal notes and Nov 12 discussion (04:45; 12:58). Proposed information structure; tool choice, actual content coverage, ownership and maintenance policy require agreement.',18)

f=frame('p06b',1275,'06B Documentation: change, review, publish and maintain',
        'Contributors / content owners / reviewers / readers | Draft | Tie documentation to system changes, validate instructions and keep a visible maintenance loop.')
for key,y,h,label in [('request',264,224,'Contributors / requests'),('author',552,224,'Owner / author / reviewer'),
                       ('publish',840,224,'Publication / discovery'),('reader',1128,224,'Readers / feedback'),
                       ('maintain',1416,256,'Maintenance / ownership')]:
 el(f,'rect',id='b-lane-'+key,x=64,y=y,width=3024,height=h,fill='#f7f7f7',stroke='none')
 text(f,'b-role-'+key,88,y+16,256,label,18,True)
request=card(f,'b-request',440,280,640,192,
     '<b>1. Identify a documentation change</b><br>A system change, incident or reader reveals a gap.<br>Link the change/task and affected topic/version.<br>State what readers need to understand or do.')
noowner=card(f,'b-noowner',1272,280,640,192,
     '<b>No owner or conflicting sources</b><br>Record the gap and request an accountable owner.<br>Resolve which source is authoritative.<br>Keep unverified material visibly marked.','decision')
failed=card(f,'b-review-failed',2104,280,840,192,
     '<b>Review does not pass</b><br>Return inaccurate, incomplete or untested instructions to the author.<br>Resolve findings and repeat the affected validation.<br>Publish as verified only after the agreed review passes.','decision')
triage=card(f,'b-triage',440,568,640,192,
     '<b>2. Assign and scope [Content owner]</b><br>Confirm audience, source, owner and reviewer.<br>Identify related pages and affected release.<br>Track the update with the system change.')
draft=card(f,'b-draft',1272,568,640,192,
     '<b>3. Draft or update [Author]</b><br>Explain scope, prerequisites and steps.<br>Add expected outcomes and failure handling.<br>Link code/configuration and dated evidence.')
review=card(f,'b-review',2104,568,840,192,
     '<b>4. Validate accuracy [Domain reviewer]</b><br>Compare claims with the identified implementation/version.<br>Exercise instructions in an appropriate approved environment.<br>Check completeness, readability and intended access.')
missing=card(f,'b-missing',440,856,640,192,
     '<b>Missing, stale or inaccessible page</b><br>Flag the issue and route it to the content owner.<br>Check authoritative sources for the answer.<br>Feed the gap back into Step 2.','decision')
find=card(f,'b-find',1272,856,640,192,
     '<b>6. Find the right guide [Reader]</b><br>Browse/search the agreed knowledge index.<br>Check product, environment, version and status.<br>Follow the authoritative page or repository.')
publish=card(f,'b-publish',2104,856,840,192,
     '<b>5. Publish and link [Content owner]</b><br>Publish the reviewed version and update the knowledge index.<br>Show owner, verification date, scope and review status.<br>Replace duplicate guidance with links or retirement notices.')
card(f,'b-example',440,1144,640,192,
     '<b>Example reader task: temporary QA setup</b><br>Find prerequisites, manifest and launch steps.<br>Know readiness, test and expiry/cleanup behavior.<br>Locate troubleshooting and the support owner.','context')
use=card(f,'b-use',1272,1144,640,192,
     '<b>7. Use and verify [Developer / QA / Ops]</b><br>Follow the guide within its stated scope.<br>Compare the result with its expected outcome.<br>Record missing steps or version differences.')
feedback=card(f,'b-feedback',2104,1144,840,192,
     '<b>8. Capture feedback and change evidence</b><br>Attach the page, applicable version and findings to a tracked task.<br>Owner distinguishes a documentation gap from a system issue.<br>Route urgent operational issues through the support process.')
card(f,'b-maintenance-policy',440,1432,1472,224,
     '<b>Changes and periodic reviews keep the loop active</b><br>Infrastructure, application, access and environment changes trigger an impact check on related documentation.<br>Track the update with the change/release; agree which updates must be ready before handoff.<br>Choose a review cadence and escalation owner. Automation or reminders are implementation options.','context')
maintain=card(f,'b-maintain',2104,1432,840,224,
     '<b>9. Refresh, reaffirm or retire [Content owner]</b><br>Review feedback and the scheduled freshness check.<br>If changed, return to Step 2 and repeat review.<br>If still valid, record the verification and next review.<br>If obsolete, archive/mark retired and link its replacement.')
link(f,'b-l1',request,triage,'Change','bottom','top')
link(f,'b-l2',triage,draft,'Scoped')
link(f,'b-l3',draft,review,'Draft')
link(f,'b-l4',review,publish,'Reviewed','bottom','top')
link(f,'b-l5',publish,find,'Indexed','left','right')
link(f,'b-l6',find,use,'Located','bottom','top')
link(f,'b-l7',use,feedback,'Findings')
link(f,'b-l8',feedback,maintain,'Review','bottom','top')
link(f,'b-noowner-link',draft,noowner,'Unresolved','top','bottom')
link(f,'b-failed-link',review,failed,'Revise','top','bottom')
link(f,'b-missing-link',find,missing,'Gap','left','right')
text(f,'b-evidence',64,1810,3024,
     'Proposed process, not a verified existing publishing workflow. Agree owners, review authority, release handoffs, access, freshness cadence and tracking/automation before implementation.',18)

f=frame('p06c',5110,'06C Documentation: delivery plan and ownership',
        'CTO / DevOps / application and product owners / QA | Draft | Inventory the evidence, prove one useful guide, then expand with accountable maintenance.')
text(f,'c-work',64,244,3024,'Proposed work packages',bold=True)
phases=[]
for key,x,title,body,owner in [
 ('c-inventory',64,'1. Inventory and prioritize',
  'List existing pages, diagrams and repository docs.<br>Identify gaps, duplicates and stale claims.<br>Prioritize high-use DevOps tasks and runbooks.<br>Record actual source and access boundaries.',
  'DevOps + domain owners'),
 ('c-design',860,'2. Agree structure and responsibility',
  'Choose the entry point and canonical sources.<br>Define page types, metadata and templates.<br>Assign owners, reviewers and change triggers.<br>Agree review cadence and retirement handling.',
  'Content owners + DevOps + team leads'),
 ('c-trial',1656,'3. Prove a DevOps guide',
  'Use an agreed QA provisioning or release task.<br>Write from verified code and versioned evidence.<br>Have another reader exercise the instructions.<br>Resolve gaps and validate the maintenance loop.',
  'DevOps author + domain reviewer + QA'),
 ('c-expand',2452,'4. Expand and maintain',
  'Add cloud architecture, then product knowledge.<br>Connect diagrams, runbooks and code references.<br>Retire duplicates with replacement links.<br>Review feedback, ownership and freshness.',
  'Domain owners + team leads'),
]:
 phases.append(card(f,key,x,328,636,256,f'<b>{title}</b><br>{body}'))
 text(f,key+'-owner',x,616,636,'Proposed owner: '+owner,18)
for i in range(3):link(f,'c-next-'+str(i),phases[i],phases[i+1],'Next')
for key,x,y,title in [('proof',64,744,'Evidence that the proposal works'),('dependencies',1656,744,'Inputs and coordination'),
                      ('controls',64,1120,'Maintenance rules to agree'),('decisions',1656,1120,'Open decisions for review')]:
 text(f,'c-'+key+'-title',x,y,1432,title,bold=True)
card(f,'c-proof',64,824,1432,224,
     '• A reader locates the authoritative guide for an agreed task.<br>• A second reader completes it and gets the stated outcome.<br>• Scope, implementation version and verification date are visible.<br>• A sample system change triggers the right documentation update.<br>• Feedback, stale content and retired links reach an accountable owner.','context')
card(f,'c-dependencies',1656,824,1432,224,
     '• Access to existing Confluence/product and repository material.<br>• Verified configuration, release evidence and domain reviewers.<br>• Agreed environment/deployment workflows from related proposals.<br>• Time to exercise instructions in an approved environment.<br>• Team decisions on where the index, pages and tracked updates live.','context')
card(f,'c-controls',64,1200,1432,224,
     '• One authoritative source per topic; link rather than fork copies.<br>• Named content owner/reviewer and explicit page status.<br>• System-change impact checks and agreed handoff requirements.<br>• Periodic verification, overdue escalation and ownership transfer.<br>• Existing access boundaries; secret references rather than values.','decision')
card(f,'c-decisions',1656,1200,1432,224,
     '• Which existing tool is the entry point and which content stays in code?<br>• Which DevOps guides and gaps come first?<br>• Who owns and approves each cloud/product subject area?<br>• What review cadence and freshness indicators are useful?<br>• How are updates tracked, prioritized and checked during delivery?','decision')
card(f,'c-boundaries',64,1504,3024,160,
     '<b>Review the direction before detailed documentation delivery</b><br>This proposal defines the information map and operating process. Detailed Confluence/runbook work follows the agreed review and implementation scope.<br>No tool migration, AI ingestion, repository consolidation, dates or named assignments are assumed; preserve access to each authoritative source.','context')
text(f,'c-evidence',64,1810,3024,
     'Basis: proposal notes and Nov 12 discussion. Current gaps are reported concerns; the content inventory, source selection, owners, cadence and delivery priorities remain to validate.',18)

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
E.ElementTree(svg).write(P/'proposal-06.canvas.svg',encoding='utf-8',xml_declaration=True)
print(f'Built 3 frames and {len(ids)} native widgets; bounds and connector references checked.')
