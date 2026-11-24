"""Build initial Proposal 04 as native editable Miro widgets.

Do not recreate on the existing board after creation. Edit using live Miro IDs.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).parent
NS="http://www.w3.org/2000/svg"
ET.register_namespace("",NS)
svg=ET.Element(f"{{{NS}}}svg",{"width":"11600","height":"14500"})
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
    f=el(svg,"g",id=key,transform=f"translate({x},12500)",data_frame=title)
    el(f,"rect",data_type="frame",x=0,y=0,width=3152,height=1910,fill="#ffffff",data_title=title)
    text(f,key+"-title",64,64,3024,title,33,True)
    text(f,key+"-subtitle",64,148,3024,subtitle)
    text(f,key+"-legend",64,1750,3024,"Blue = proposed | Gray = saved evidence or context | Yellow = boundary, exception or team decision",18)
    return f

f=frame("p04a",-2560,"04A TrekCAP and TrekFinder: repository consolidation",
        "CTO / application teams / IP owners / DevOps | Draft | Evaluate consolidation by source-access boundary and preserve controlled artifact handoffs.")
text(f,"a-current",64,244,1280,"Current: 17 repositories in the saved product group",bold=True)
text(f,"a-proposed",1740,244,1348,"Proposed option: product monorepo plus restricted sources",bold=True)
card(f,"a-apps",64,320,1280,150,
     "<b>Application UI and backend (2)</b><br>cap-trekfinder; cap-tutor-app-backend<br>TrekFinder is the app; CAP supplies the adaptive engine.","context")
card(f,"a-engine",64,502,1280,224,
     "<b>Engine, modules and supporting services (9)</b><br>c-orch; C-MCP; c-mcp-gateway; c-data-access; c-keycloak<br>C-IP-ORCH; C-EMP-IP-CORE; C-EMP-IP-REASONING; C-EMP-IP-MCP<br>Source classification and actual grants need separate review.","context")
card(f,"a-ci",64,758,1280,160,
     "<b>CI and tests (4)</b><br>C-CI-GATES; C-INTEGRATION; cap-benchmark<br>cap-trekfinder-automation-test", "context")
card(f,"a-devops",64,950,1280,138,
     "<b>Deployment and infrastructure (2)</b><br>cap-gitOps; tl-trekcap-terraform", "context")
product=card(f,"a-product",1740,320,1348,192,
             "<b>Product monorepo: compatible source access</b><br>TrekFinder UI/backend plus agreed services, modules and tests.<br>Include a repository only after its actual access needs are matched.")
restricted=card(f,"a-restricted",1740,672,1348,192,
                "<b>Retain restricted source and build boundaries</b><br>C-IP-ORCH and employee-only source stay separately controlled.<br>Authorized builds publish approved images or packages for consumers.")
link(f,"a-artifacts",restricted,product,"Approved artifacts","top","bottom")
card(f,"a-trusted",1740,928,1348,160,
     "<b>Trusted policy and test ownership</b><br>Keep C-CI-GATES under its restricted policy ownership.<br>Place integration/E2E/benchmark code by access and release needs.")
for key,x,w,title in [("benefits",64,960,"Benefits to evaluate"),("tradeoffs",1088,960,"Costs and constraints"),
                      ("alternative",2112,976,"Alternative to compare")]:
    text(f,"a-"+key+"-title",x,1180,w,title,bold=True)
card(f,"a-benefits",64,1244,960,192,
     "• Coordinate app and compatible service changes.<br>• Share setup and contract tests where useful.<br>• Make artifact versions and dependencies explicit.")
card(f,"a-tradeoffs",1088,1244,960,192,
     "• Several access boundaries still need coordination.<br>• Image/module pins and CI references must change.<br>• Shared checks and migration increase team effort.","decision")
card(f,"a-alternative",2112,1244,976,192,
     "Keep repositories separate with shared workflows,<br>versioned contracts and release manifests.<br>Compare this with consolidation inside each access tier.","context")
card(f,"a-boundary",64,1500,3024,192,
     '<b>Decide the boundary before moving source</b><br>One broad monorepo would give its readers visibility of all included source; folder review rules do not preserve separate read access.<br>17 is the product-group total, not an approved migration count. Coordinate cap-gitOps and tl-trekcap-terraform with <a href="https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690571914544">Proposal 02</a>; Hub/LMS remains Proposal 03.',"decision")
text(f,"a-evidence",64,1810,3024,
     "Evidence: Nov 3, 2026 inventory; Nov 12 count clarification. All 17 repos are private in the saved inventory; open is an IP classification, not public visibility. Current grants need confirmation.",18)

f=frame("p04b",1275,"04B TrekCAP: controlled builds and RD delivery",
        "Application developers / restricted-source owners / QA / DevOps | Draft | Connect permitted source through versioned artifacts and explicit test evidence.")
text(f,"b-restricted-title",64,244,3024,"Restricted-source path: its own owners, review and build identity",bold=True)
source=card(f,"b-source",64,352,880,192,
            "<b>1. Review restricted-source changes</b><br>Authorized owners review kernel/employee-only changes.<br>Keep source and trusted build authority in their boundary.")
sealed=card(f,"b-sealed",1104,352,880,192,
            "<b>2. Build and inspect approved artifacts</b><br>Run the applicable sealing, IP and image checks.<br>Resolve incomplete build paths before relying on them.")
artifact=card(f,"b-artifact",2144,352,880,192,
              "<b>3. Publish versioned artifacts</b><br>Record source revision, image digest or package version.<br>Grant consumers only the artifact access they need.")
link(f,"b-r1",source,sealed,"Approved")
link(f,"b-r2",sealed,artifact,"Checks pass")
text(f,"b-product-title",64,704,1000,"Product-source path: compatible access and explicit dependencies",bold=True)
app=card(f,"b-app",64,800,880,224,
         "<b>4. Review product/service changes</b><br>Work in the agreed source area; check affected contracts.<br>Restricted-source changes follow the path above.<br>Review each affected owner’s scope.")
build=card(f,"b-build",1104,800,880,224,
           "<b>5. Build affected services</b><br>Pin approved images and module/package versions.<br>Run applicable code, image and IP checks.<br>Keep service artifacts separately identifiable.")
integration=card(f,"b-integration",2144,800,880,224,
                 "<b>6. Require agreed release tests</b><br>Test the exact image/version combination.<br>Run Tier 2 integration and relevant TrekFinder E2E tests.<br>Proposed: selected passing tests gate the GitOps handoff.")
link(f,"b-p1",app,build,"Approved")
link(f,"b-p2",build,integration,"Service images")
link(f,"b-consume",artifact,build,"Pinned artifacts","bottom","top")
card(f,"b-baseline",64,1216,880,224,
     "<b>Saved baseline and limits</b><br>RD is the identified CAP target; stage/prod are not established.<br>Tier 2 dispatch occurs after the GitOps merge in saved code.<br>Current success and effective blocking are unverified.","context")
failed=card(f,"b-failed",1104,1216,880,224,
            "<b>Required gate fails: stop the release</b><br>Return findings to the responsible source/build owner.<br>Correct, review, rebuild and rerun affected tests.<br>Agree the response to failed RD acceptance checks.","decision")
rd=card(f,"b-rd",2144,1216,880,224,
        "<b>7. Propose, deploy and verify RD</b><br>GitOps approval selects the intended artifact versions.<br>Argo CD reconciles; QA verifies the deployed journeys.<br>Record versions, outcome and recovery evidence.")
link(f,"b-tests-pass",integration,rd,"Pass / GitOps approval","bottom","top")
link(f,"b-tests-fail",integration,failed,"Failed required tests","bottom","top")
card(f,"b-decisions",64,1504,3024,160,
     "<b>Agree the controls before implementation</b><br>Source-access groups, policy owners, artifact consumers, required pre-deployment tests and recovery owners remain team decisions.<br>Keep post-deployment verification as well. Future stage/prod and promotion-policy design belong to separately agreed scope with Proposal 11.","decision")
text(f,"b-evidence",64,1810,3024,
     "Basis: CAP source/delivery snapshots Nov 2–3 and qualified GitOps assessment Nov 6, 2026. Pre-handoff test gates and artifact traceability above are proposals, not verified live controls.",18)

f=frame("p04c",5110,"04C TrekCAP and TrekFinder: consolidation delivery plan",
        "Application teams / IP owners / QA / DevOps | Draft | Agree access-compatible groups, prove one migration, then expand with verified artifact handoffs.")
text(f,"c-packages",64,244,3024,"Proposed work packages",bold=True)
phases=[]
for key,x,title,body,owner in [
    ("c-map",64,"1. Map the code and access",
     "Confirm the 17-repository product inventory.<br>Compare IP classes with actual source grants.<br>Map build owners, artifacts, pins and consumers.","App leads + IP owners + DevOps"),
    ("c-agree",860,"2. Agree the consolidation boundaries",
     "Compare per-boundary consolidation with shared standards.<br>Choose source groups and trusted policy ownership.<br>Agree test gates, artifact access and release contracts.","App team + IP owners + DevOps"),
    ("c-pilot",1656,"3. Prove a permitted pilot",
     "Choose UI/backend or another compatible group.<br>Verify pinned dependencies, tests and an RD release.<br>Rehearse source cutover and recovery.","App owners + QA + DevOps"),
    ("c-expand",2452,"4. Move the rest step by step",
     "Migrate only the agreed access-compatible groups.<br>Switch references and keep one writable source.<br>Retire old write paths after acceptance.","App owners + IP owners + DevOps"),
]:
    phases.append(card(f,key,x,328,636,256,f"<b>{title}</b><br>{body}"))
    text(f,key+"-owner",x,616,636,"Proposed owner: "+owner,18)
for i in range(3):link(f,"c-next-"+str(i),phases[i],phases[i+1],"Next")
for key,x,y,title in [
    ("proof",64,744,"Evidence before expanding"),("references",1656,744,"References and consumers to migrate"),
    ("recovery",64,1120,"Cutover and recovery"),("decisions",1656,1120,"Decisions with the product and IP owners"),
]:text(f,"c-"+key+"-title",x,y,1432,title,bold=True)
card(f,"c-proof",64,824,1432,224,
     "• Verify source visibility remains within agreed boundaries.<br>• Trace source revision → artifact version → service → RD.<br>• Show required checks gate the selected release handoff.<br>• Verify integration, user journeys and recovery evidence.","context")
card(f,"c-references",1656,824,1432,224,
     "• Kernel/image pins and module/package source references.<br>• Reusable CI, classification manifests and build contexts.<br>• Registry consumers, GitOps writers and dispatch targets.<br>• Local setup, integration fixtures and ownership guidance.","context")
card(f,"c-recovery",64,1200,1432,224,
     "• Agree history handling and open-PR cutover per group.<br>• Keep restricted source and policy authority controlled.<br>• Rehearse restoring references and a known artifact set.<br>• Agree application/data recovery and failure ownership.","decision")
card(f,"c-decisions",1656,1200,1432,224,
     "• Which source groups share the same permitted readers?<br>• Where should CI policy, tests and shared modules live?<br>• Which build paths and acceptance tests are ready?<br>• Who approves the pilot, gates and recovery evidence?", "decision")
card(f,"c-boundary",64,1504,3024,160,
     "<b>Scope and dependencies</b><br>All 17 repositories are inventory context, not an approved single-source migration. Exclude legacy c-trekai-adventure from this product group.<br>Coordinate GitOps/infra with Proposal 02 and release policy with 11. RD is the starting target to confirm; stage/prod, dates and implementation approval remain separate decisions.","context")
text(f,"c-evidence",64,1810,3024,
     "Planning basis: existing product map, Nov 12 repository-count clarification and qualified CAP delivery assessment. Access, build readiness and current runtime require owner verification before migration.",18)

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
ET.ElementTree(svg).write(ROOT/'proposal-04.canvas.svg',encoding='utf-8',xml_declaration=True)
print(f'Built 3 frames and {len(ids)} native widgets; bounds and connector references checked.')
