"""Build Proposal 02 as native editable Miro shapes, text and connectors.

The canvas export is for initial creation only. Use returned live widget IDs
for subsequent edits on the existing board.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
svg = ET.Element(f"{{{NS}}}svg", {"width": "11600", "height": "4400"})
COLORS = {
    "context": ("#ddddd8", "#a8a8a0", "#434339"),
    "proposal": ("#a0c4fb", "#6a8bbf", "#14315e"),
    "decision": ("#ffe86d", "#cbb333", "#574900"),
}

def el(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {k.replace("_", "-"): str(v) for k, v in attrs.items()})

def text(parent, key, x, y, w, content, size=22, bold=False, color="#595959"):
    e = el(parent, "textArea", id=key, x=x, y=y, width=w, height=64 if size == 33 else 40,
           fill=color, font_family="noto_sans", font_size=size, text_align="left",
           font_weight="bold" if bold else "normal")
    e.text = content
    return e

def card(parent, key, x, y, w, h, content, kind="proposal", align="left", shape=None):
    fill, stroke, ink = COLORS[kind]
    e = el(parent, "rect", id=key, x=x, y=y, width=w, height=h,
           data_content=content, fill=fill, stroke=stroke, stroke_width=2,
           data_text_color=ink, data_font_family="noto_sans", data_font_size=22,
           data_text_align=align, data_text_align_vertical="middle")
    if shape:
        e.set("data-shape", shape)
    return e

def link(parent, key, a, b, label="", start="right", end="left"):
    def point(e, side):
        x, y, w, h = [float(e.get(k)) for k in ("x", "y", "width", "height")]
        return {"left": (x, y+h/2), "right": (x+w, y+h/2),
                "top": (x+w/2, y), "bottom": (x+w/2, y+h)}[side]
    x1, y1 = point(a, start)
    x2, y2 = point(b, end)
    return el(parent, "line", id=key, x1=x1, y1=y1, x2=x2, y2=y2,
              data_start=a.get("id"), data_end=b.get("id"), stroke="#313131",
              stroke_width=2, data_arrow="end", data_shape="elbowed",
              data_start_side=start, data_end_side=end, data_content=label)

def frame(key, x, title, subtitle):
    f = el(svg, "g", id=key, transform=f"translate({x},2400)", data_frame=title)
    el(f, "rect", data_type="frame", x=0, y=0, width=3152, height=1910,
       fill="#ffffff", data_title=title)
    text(f, key+"-title", 64, 64, 3024, title, 33, True, "#1a1a1a")
    text(f, key+"-subtitle", 64, 148, 3024, subtitle)
    text(f, key+"-legend", 64, 1750, 3024,
         "Blue = proposed | Gray = saved evidence or context | Yellow = tradeoff, exception or team decision", 18)
    return f

f = frame("p02a", -2560, "02A DevOps monorepo: proposal",
          "CTO / team | Draft | Bring DevOps code together while keeping ownership and execution boundaries clear.")
text(f, "a-current", 64, 244, 1280, "Current: separate repositories in saved evidence", bold=True, color="#1a1a1a")
text(f, "a-proposed", 1740, 244, 1348, "Proposed: one DevOps repository, distinct areas", bold=True, color="#1a1a1a")
card(f, "a-tf", 64, 320, 1280, 180,
     "<b>Terraform</b><br>tl-trekai-terraform: TL and shared infrastructure<br>tl-trekcap-terraform: CAP RD infrastructure", "context")
card(f, "a-gitops", 64, 532, 1280, 180,
     "<b>GitOps</b><br>tl-lms-gitOps: dev, stage, prod and common<br>cap-gitOps: RD configuration", "context")
card(f, "a-adjacent", 64, 744, 1280, 148,
     "<b>Other infrastructure candidates</b><br>ir-terraform-temporary; b-metric-dashboard-terraform<br>Legacy trekai-infra: review before including", "context")
card(f, "a-unknown", 64, 924, 1280, 128,
     "<b>Scope to confirm</b><br>Locate Ansible, scripts and other DevOps-owned code.", "decision")
card(f, "a-root", 1740, 320, 1348, 96,
     "<b>devops/</b>  Proposed repository name; team to agree", align="center")
for key, y, title, body in [
    ("a-folder-tf", 448, "terraform/", "Keep product, environment and state boundaries explicit."),
    ("a-folder-gitops", 608, "gitops/", "Separate TL and CAP configuration and environment paths."),
    ("a-folder-automation", 768, "automation/", "Ansible if used, plus reviewed DevOps scripts."),
    ("a-folder-ci", 928, ".github/ and docs/", "Shared validation, ownership rules and operating guidance."),
]:
    card(f, key, 1740, y, 1348, 128, f"<b>{title}</b><br>{body}")
text(f, "a-benefit-title", 64, 1120, 960, "Expected benefits", bold=True, color="#1a1a1a")
text(f, "a-cost-title", 1088, 1120, 960, "Costs and constraints", bold=True, color="#1a1a1a")
text(f, "a-alternative-title", 2112, 1120, 976, "Alternative to compare", bold=True, color="#1a1a1a")
card(f, "a-benefits", 64, 1184, 960, 224,
     "• Easier discovery and consistent structure.<br>• Reuse checks and operating guidance.<br>• Review related configuration changes together.")
card(f, "a-costs", 1088, 1184, 960, 224,
     "• More complex dependency-aware validation.<br>• Wider impact from shared workflow changes.<br>• Recheck repository access and integrations.", "decision")
card(f, "a-alternative", 2112, 1184, 976, 224,
     "Keep repositories separate with shared workflows<br>and standards. Compare access needs, team effort<br>and coordination cost before choosing.", "context")
card(f, "a-decisions", 64, 1472, 3024, 192,
     "<b>Team decision</b><br>Agree repository scope, owners and access before migration. Folder review rules do not isolate read access.<br>If code requires separate visibility, keep that scope in a separate repository. Shared state and release scope remain separate decisions.", "decision")
text(f, "a-evidence", 64, 1810, 3024,
     "Evidence: saved GitHub inventory Nov 3 and Terraform/GitOps evidence Nov 3–4, 2026. Repository names and folders are snapshot observations, not a live inventory.", 18)

f = frame("p02b", 1275, "02B DevOps monorepo: change workflow",
          "Contributors / reviewers / DevOps | Draft | One place to propose changes; execution stays specific to each affected area.")
for key, x, title in [("author",64,"Contributor"),("ci",704,"Validation automation"),
                      ("review",1344,"Area owners / reviewers"),("merge",1984,"Merge / execution handoff")]:
    text(f, "b-role-"+key, x, 280, 480, title, bold=True, color="#1a1a1a")
author = card(f, "b-author", 64, 376, 480, 192,
              "<b>1. Open a pull request</b><br>Change the relevant area.<br>Describe intent and affected targets.")
checks = card(f, "b-checks", 704, 376, 480, 192,
              "<b>2. Check affected scope</b><br>Detect paths and dependencies.<br>Run the relevant validation.")
review = card(f, "b-review", 1344, 376, 480, 192,
              "<b>3. Review the change</b><br>Owners inspect results and impact.<br>All affected areas get review.")
merge = card(f, "b-merge", 1984, 376, 480, 192,
             "<b>4. Merge agreed code</b><br>Required checks and reviews pass.<br>Route each change to its process.")
link(f, "b-l1", author, checks)
link(f, "b-l2", checks, review, "Results")
link(f, "b-l3", review, merge, "Approved")
fail = card(f, "b-fail", 704, 728, 480, 160,
            "<b>Checks fail or scope is unclear</b><br>Block merge; return diagnostics.<br>Author revises and reruns checks.", "decision")
revise = card(f, "b-revise", 1344, 728, 480, 160,
              "<b>Changes requested</b><br>Author revises the pull request.<br>Repeat checks and affected review.", "decision")
link(f, "b-l-fail", checks, fail, "Failed / unresolved", "bottom", "top")
link(f, "b-l-revise", review, revise, "Revise", "bottom", "top")
tf = card(f, "b-tf", 1984, 1048, 480, 224,
          "<b>Terraform changes</b><br>Final target plan and authorization.<br>Apply and verify under Proposal 01.<br>Keep each state independent.")
gitops = card(f, "b-gitops", 2608, 1048, 480, 224,
              "<b>GitOps changes</b><br>Argo CD reads approved paths.<br>Reconcile under agreed policy.<br>Verify the deployment outcome.")
link(f, "b-l-tf", merge, tf, "Terraform", "bottom", "top")
link(f, "b-l-gitops", merge, gitops, "GitOps", "right", "top")
card(f, "b-other", 1984, 1336, 1104, 160,
     "<b>Other automation</b><br>Use its agreed trigger, identity and authorization.<br>Include run results in the change record.")
card(f, "b-check-details", 64, 1048, 1760, 224,
     "<b>What validation needs to understand</b><br>Terraform: validate affected roots and shared-module consumers; show target plans.<br>GitOps: validate affected manifests, charts and values, including shared dependencies.<br>Scripts / Ansible: choose suitable checks after inventory; unclear impact blocks merge.", "context")
card(f, "b-boundaries", 64, 1336, 1760, 160,
     "<b>Ownership and access</b><br>Route reviews to each affected area. Restrict execution identities by target.<br>A shared commit can coordinate code; it does not make separate deployments atomic.", "context")
card(f, "b-decisions", 64, 1560, 3024, 128,
     "<b>Agree with the team:</b> required reviewers and checks; dependency detection; cross-area ordering; who handles failures.<br>App build writers and Argo CD references need an explicit migration plan. Broader release-policy redesign belongs to Proposal 11.", "decision")
text(f, "b-evidence", 64, 1810, 3024,
     "Proposed workflow. Saved evidence shows app workflows write GitOps changes; Terraform apply and Argo CD reconciliation are separate. Current execution and access remain unverified.", 18)

f = frame("p02c", 5110, "02C DevOps monorepo: delivery plan",
          "DevOps / team | Draft | Confirm the boundaries, prove a small migration, then move one agreed scope at a time.")
text(f, "c-work", 64, 244, 3024, "Proposed work packages", bold=True, color="#1a1a1a")
phases = []
for key,x,title,body,owner in [
    ("c-inventory",64,"1. Understand today’s setup",
     "List candidate code, owners and consumers.<br>Map workflows, access, state references<br>and Argo CD sources before moving files.", "DevOps + current owners"),
    ("c-agree",860,"2. Agree the repository boundaries",
     "Compare consolidation with shared standards.<br>Choose scope, folders and ownership.<br>Agree access, checks and migration criteria.", "Team + DevOps"),
    ("c-pilot",1656,"3. Prove a small migration",
     "Move one agreed development scope.<br>Check review, automation and references.<br>Rehearse cutover and rollback.", "DevOps + pilot owners"),
    ("c-expand",2452,"4. Move the rest step by step",
     "Switch one source of truth per scope.<br>Verify consumers after every cutover.<br>Retire old write paths after acceptance.", "DevOps + affected teams"),
]:
    phases.append(card(f,key,x,328,636,256,f"<b>{title}</b><br>{body}"))
    text(f,key+"-owner",x,616,636,"Proposed owner: "+owner,18)
for i in range(3):
    link(f,"c-next-"+str(i),phases[i],phases[i+1],"Next")
text(f, "c-ready-title", 64, 744, 1432, "Evidence before expanding", bold=True, color="#1a1a1a")
text(f, "c-risk-title", 1656, 744, 1432, "Cutover and rollback", bold=True, color="#1a1a1a")
card(f, "c-ready", 64, 824, 1432, 224,
     "• Show checks for changed files and shared dependencies.<br>• Demonstrate required reviews and scoped execution.<br>• Prove app writers and Argo CD use the new locations.<br>• Confirm Terraform resolves the same intended state.", "context")
card(f, "c-cutover", 1656, 824, 1432, 224,
     "• Inventory every writer and reader before the switch.<br>• Freeze the migrating scope; update references together.<br>• Keep one writable source of truth after cutover.<br>• Rehearse restoring consumers and reconciling changes.", "decision")
text(f, "c-dep-title", 64, 1120, 1432, "Dependencies to update and verify", bold=True, color="#1a1a1a")
text(f, "c-scope-title", 1656, 1120, 1432, "Scope and team decisions", bold=True, color="#1a1a1a")
card(f, "c-dependencies", 64, 1200, 1432, 224,
     "• Argo CD repository, revision and path references.<br>• App workflow targets and GitHub App repository access.<br>• Terraform paths, module sources and backend settings.<br>• Approval rules, identity bindings, docs and runbooks.", "context")
card(f, "c-scope", 1656, 1200, 1432, 224,
     "• Confirm Ansible, scripts, business and legacy scope.<br>• Agree naming, history handling and area owners.<br>• Retain separate repos where access needs require it.<br>• Choose the pilot, rollback owner and acceptance criteria.", "decision")
card(f, "c-separation", 64, 1504, 3024, 160,
     "<b>Keep the proposal boundaries clear</b><br>Proposal 01 covers controlled Terraform execution. Proposals 03/04 cover application monorepos. Proposal 11 covers GitOps / SDLC simplification.<br>Repository consolidation alone does not resolve release policy, access or recovery gaps. No migration dates or named owners are committed.", "context")
text(f, "c-evidence", 64, 1810, 3024,
     "Planning basis: saved infrastructure / GitOps map and control assessment, Nov 3–6, 2026. Migration and runtime verification are proposed work, not completed actions.", 18)

ids = {e.get("id"): e for e in svg.iter() if e.get("id")}
assert len(ids) == sum(bool(e.get("id")) for e in svg.iter())
assert len(svg) == 3
for f in svg:
    for e in f:
        if e.get("data-start"):
            assert e.get("data-start") in ids and e.get("data-end") in ids
        elif e.get("x") is not None:
            assert float(e.get("x")) >= 0 and float(e.get("y")) >= 0
            assert float(e.get("x"))+float(e.get("width",0)) <= 3152
            assert float(e.get("y"))+float(e.get("height",0)) <= 1910
assert not any(e.tag.endswith(("image", "foreignObject")) for e in svg.iter())
ET.indent(svg)
ET.ElementTree(svg).write(ROOT / "proposal-02.canvas.svg", encoding="utf-8", xml_declaration=True)
print(f"Built 3 frames and {len(ids)} identified native widgets; bounds and connector references checked.")
