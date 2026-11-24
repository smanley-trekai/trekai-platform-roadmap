"""Build the initial native editable Proposal 03 composition.

Use returned live Miro IDs for edits. Do not recreate this composition on the
existing board after successful creation.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).parent
NS="http://www.w3.org/2000/svg"
ET.register_namespace("",NS)
svg=ET.Element(f"{{{NS}}}svg",{"width":"11600","height":"11600"})
COLORS={"context":("#ddddd8","#a8a8a0","#434339"),
        "proposal":("#a0c4fb","#6a8bbf","#14315e"),
        "decision":("#ffe86d","#cbb333","#574900")}

def el(p,tag,**a):
    return ET.SubElement(p,f"{{{NS}}}{tag}",{k.replace('_','-'):str(v) for k,v in a.items()})

def text(p,key,x,y,w,body,size=22,bold=False):
    e=el(p,"textArea",id=key,x=x,y=y,width=w,height=64 if size==33 else 40,
         fill="#1a1a1a" if bold else "#595959",font_family="noto_sans",font_size=size,
         text_align="left",font_weight="bold" if bold else "normal")
    e.text=body
    return e

def card(p,key,x,y,w,h,body,kind="proposal"):
    fill,stroke,ink=COLORS[kind]
    return el(p,"rect",id=key,x=x,y=y,width=w,height=h,data_content=body,fill=fill,
              stroke=stroke,stroke_width=2,data_text_color=ink,data_font_family="noto_sans",
              data_font_size=22,data_text_align="left",data_text_align_vertical="middle")

def link(p,key,a,b,label="",start="right",end="left"):
    def point(e,s):
        x,y,w,h=[float(e.get(k)) for k in ("x","y","width","height")]
        return {"left":(x,y+h/2),"right":(x+w,y+h/2),"top":(x+w/2,y),"bottom":(x+w/2,y+h)}[s]
    x1,y1=point(a,start);x2,y2=point(b,end)
    return el(p,"line",id=key,x1=x1,y1=y1,x2=x2,y2=y2,data_start=a.get("id"),data_end=b.get("id"),
              data_start_side=start,data_end_side=end,stroke="#313131",stroke_width=2,
              data_arrow="end",data_shape="elbowed",data_content=label)

def frame(key,x,title,subtitle):
    f=el(svg,"g",id=key,transform=f"translate({x},9600)",data_frame=title)
    el(f,"rect",data_type="frame",x=0,y=0,width=3152,height=1910,fill="#ffffff",data_title=title)
    text(f,key+"-title",64,64,3024,title,33,True)
    text(f,key+"-subtitle",64,148,3024,subtitle)
    text(f,key+"-legend",64,1750,3024,"Blue = proposed | Gray = saved evidence or context | Yellow = tradeoff, exception or team decision",18)
    return f

f=frame("p03a",-2560,"03A Trek Learning (Hub/LMS): monorepo proposal",
        "CTO / application developers / DevOps | Draft | Organize product code together while retaining clear service ownership and release boundaries.")
text(f,"a-current",64,244,1280,"Current: 16 repositories in the saved product group",bold=True)
text(f,"a-future",1740,244,1348,"Proposed: one product repository, agreed application scope",bold=True)
for key,y,title,body in [
    ("a-ui-core",320,"Web interface and core APIs","tl-lms-ui; tl-lms-service; tl-auth-service"),
    ("a-ai",532,"AI tools, chat and tutor","tl-ai-service; tl-chat-service; tl-lms-agent<br>tl-grading-service"),
    ("a-content",744,"Content, files and scheduled jobs","tl-rag-ingestion-service; tl-rag-retrieval-service<br>tl-file-handling-service; tl-batch-job-service"),
]:
    card(f,key,64,y,1280,180,f"<b>{title}</b><br>{body}","context")
card(f,"a-adjacent",64,956,1280,160,
     "<b>Adjacent scope to decide</b><br>tl-lms-db; tl-oss-components; tl-file-ingestion-pipeline<br>Confirm owners, operating paths and inclusion.","decision")
card(f,"a-root",1740,320,1348,96,"<b>trek-learning/</b>  Illustrative repository name; team to agree")
for key,y,title,body in [
    ("a-apps",448,"apps/ and services/","Web UI plus service folders with their own build and test entry points."),
    ("a-shared",608,"packages/ and .github/","Shared libraries where justified, reusable CI, and affected-service checks."),
    ("a-optional",768,"db/ and supporting components, if included","Agree migrations, Keycloak image and ingestion-pipeline ownership."),
    ("a-docs",928,"docs/ and local development guidance","One onboarding path, clear contracts, service owners and release instructions."),
]:
    card(f,key,1740,y,1348,128,f"<b>{title}</b><br>{body}")
for key,x,w,title in [("benefits",64,960,"Benefits to evaluate"),("costs",1088,960,"Costs and constraints"),
                      ("alternative",2112,976,"Alternative to compare")]:
    text(f,"a-"+key+"-title",x,1180,w,title,bold=True)
card(f,"a-benefits",64,1244,960,192,
     "• Review related UI/API changes together.<br>• Share tooling and local setup where useful.<br>• Make service contracts and owners easier to find.")
card(f,"a-costs",1088,1244,960,192,
     "• Dependency-aware CI and cache design take work.<br>• Shared changes can affect many services.<br>• Access, history and migration need agreement.","decision")
card(f,"a-alternative",2112,1244,976,192,
     "Keep service repositories separate and standardize<br>shared CI, contracts and onboarding. Compare<br>developer effort and release coordination with the team.","context")
card(f,"a-scope",64,1500,3024,192,
     '<b>Scope accounting and proposal boundaries</b><br>16 is the product-group total: 11 application repositories, 3 adjacent candidates and 2 DevOps repositories.<br>Agree the home of tl-lms-gitOps and tl-trekai-terraform with <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690571914544">Proposal 02</a>. TrekCAP/TrekFinder belongs to Proposal 04. One repo does not require one release.',"decision")
text(f,"a-evidence",64,1810,3024,
     "Evidence: Trek Learning product map and repository/delivery matrix, GitHub snapshot Nov 3, 2026. Candidate folders are proposed; final scope needs application-team review.",18)

f=frame("p03b",1275,"03B Trek Learning: developer and release workflow",
        "Developers / reviewers / QA / DevOps | Draft | Check affected services, publish identifiable images, and verify the selected release.")
card(f,"b-current",64,244,3024,112,
     "<b>Saved baseline:</b> application workflows build images and propose GitOps changes; Argo CD consumes the merged configuration.<br>The documented app branches are develop / staging / main, with rebuilds per environment. Successful current execution and enforcement remain unverified.","context")
nodes=[]
for key,x,title,body in [
    ("b-pr",64,"1. Propose a change","Edit UI, service or shared code.<br>Describe affected contracts<br>and migration needs."),
    ("b-affected",584,"2. Find affected services","Inspect paths and dependencies.<br>Include shared-code consumers.<br>Use broader checks if uncertain."),
    ("b-check",1104,"3. Test and review","Run relevant build/tests.<br>Check service compatibility.<br>Get affected-owner approval."),
    ("b-build",1624,"4. Merge and build","Build affected service images.<br>Record commit and image digest.<br>Keep service artifacts distinct."),
    ("b-gitops",2144,"5. Propose deployment","Update intended GitOps paths.<br>Identify services and target.<br>Follow agreed release approval."),
    ("b-verify",2664,"6. Deploy and verify","Argo CD reconciles GitOps.<br>QA checks required journeys.<br>Record outcome and evidence."),
]:
    nodes.append(card(f,key,x,448,400,256,f"<b>{title}</b><br>{body}"))
for i in range(5):link(f,"b-next-"+str(i),nodes[i],nodes[i+1],"Next")
fail=card(f,"b-fail",1104,864,920,160,
          "<b>Checks fail or review requests changes</b><br>Block merge; return findings to the author.<br>Revise, then rerun the affected checks and review.","decision")
deploy_fail=card(f,"b-deploy-fail",2144,864,944,160,
                 "<b>Deployment or acceptance fails</b><br>Stop further promotion; owners investigate.<br>Use the agreed recovery path and record results.","decision")
link(f,"b-ci-fail",nodes[2],fail,"Fail / revise","bottom","top")
link(f,"b-release-fail",nodes[5],deploy_fail,"Failed outcome","bottom","top")
text(f,"b-test-title",64,1096,1432,"Checks follow dependencies, not just changed folders",bold=True)
text(f,"b-release-title",1656,1096,1432,"A shared commit can still produce separate releases",bold=True)
card(f,"b-tests",64,1176,1432,224,
     "• Test changed services and their shared-code consumers.<br>• Check UI/API contracts and schema compatibility.<br>• Recheck all consumers of shared build configuration.<br>• Treat unclear impact as a reason for broader validation.","context")
card(f,"b-independent",1656,1176,1432,224,
     "• Each service keeps an identifiable image and release record.<br>• Coordinate dependent releases when contracts change.<br>• Agree database migration order and recovery separately.<br>• A green build does not prove the deployed journey works.","context")
card(f,"b-policy",64,1464,3024,224,
     "<b>Agree the release contract with application developers</b><br>Choose branch/version strategy, required checks, review owners, QA evidence and deployment gates.<br>Coordinate GitOps location with Proposal 02; release-policy simplification belongs to Proposal 11. Monorepo migration does not require changing branch policy.<br>Terraform execution remains Proposal 01; application branches do not define the Terraform environment target.","decision")
text(f,"b-evidence",64,1810,3024,
     "Basis: sourced repository/delivery matrix, Nov 3–4 snapshots; static GitOps review Nov 6. The affected-service workflow and release evidence above are proposed improvements.",18)

f=frame("p03c",5110,"03C Trek Learning: monorepo delivery plan",
        "Application developers / QA / DevOps | Draft | Agree scope together, prove a small migration, and expand after the release path is verified.")
text(f,"c-work",64,244,3024,"Proposed work packages",bold=True)
phases=[]
for key,x,title,body,owner in [
    ("c-inventory",64,"1. Understand the product code",
     "Confirm the 11 application repositories.<br>Map contracts, shared code and releases.<br>Decide which adjacent components belong.","Application leads + DevOps"),
    ("c-design",860,"2. Agree how the team will work",
     "Compare monorepo and shared standards.<br>Choose folders, owners, tests and access.<br>Define local setup and release boundaries.","Application team + DevOps"),
    ("c-pilot",1656,"3. Prove one small migration",
     "Choose a manageable service or service pair.<br>Verify local setup, CI and a dev release.<br>Rehearse source cutover and recovery.","App owners + QA + DevOps"),
    ("c-expand",2452,"4. Move the rest step by step",
     "Move agreed groups with their history.<br>Switch consumers to the new locations.<br>Retire old write paths after acceptance.","App owners + DevOps"),
]:
    phases.append(card(f,key,x,328,636,256,f"<b>{title}</b><br>{body}"))
    text(f,key+"-owner",x,616,636,"Proposed owner: "+owner,18)
for i in range(3):link(f,"c-next-"+str(i),phases[i],phases[i+1],"Next")
for key,x,y,w,title in [
    ("proof",64,744,1432,"Evidence before expanding"),
    ("consumer",1656,744,1432,"References and automation to update"),
    ("cutover",64,1120,1432,"Cutover and recovery"),
    ("decisions",1656,1120,1432,"Decisions with application developers"),
]:text(f,"c-"+key+"-title",x,y,w,title,bold=True)
card(f,"c-proof",64,824,1432,224,
     "• Build and test a changed service without rebuilding all.<br>• Show a shared change checks every known consumer.<br>• Trace commit → image digest → GitOps → dev outcome.<br>• Verify selected user journeys and migration compatibility.","context")
card(f,"c-consumers",1656,824,1432,224,
     "• Checkout paths, Docker contexts, tests and cache keys.<br>• Workflow triggers, image names and GitOps writers.<br>• Ownership/review rules, identities and security checks.<br>• Local setup, documentation and operational entry points.","context")
card(f,"c-cutover",64,1200,1432,224,
     "• Agree history, open-PR handling and a cutover window.<br>• Keep one writable source per migrated service.<br>• Rehearse restoring build/deploy references if needed.<br>• Plan application recovery and data migration handling.","decision")
card(f,"c-decisions",1656,1200,1432,224,
     "• Confirm application, database, Keycloak and pipeline scope.<br>• Agree owners, access and shared-package boundaries.<br>• Choose affected-service tooling and required checks.<br>• Select pilot scope, acceptance evidence and recovery owner.","decision")
card(f,"c-boundaries",64,1504,3024,160,
     "<b>Keep code organization and deployment behavior explicit</b><br>Folder ownership does not isolate read access; retain separate repositories where visibility requires it. Migration does not make services one application.<br>Coordinate DevOps/GitOps changes with 02 and release-policy changes with 11. Dates, named owners, scope and implementation approval remain to agree.","context")
text(f,"c-evidence",64,1810,3024,
     "Planning uses the existing Nov 3–4 inventory. Database execution and ingestion-pipeline delivery need owner confirmation. Candidate ownership and acceptance criteria require team agreement.",18)

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
ET.indent(svg)
ET.ElementTree(svg).write(ROOT/'proposal-03.canvas.svg',encoding='utf-8',xml_declaration=True)
print(f'Built 3 frames and {len(ids)} native widgets; bounds and connector references checked.')
