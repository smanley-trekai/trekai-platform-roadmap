"""Prepare sparse label edits from the latest read of 01B, 01D and 01E."""
from pathlib import Path
import copy
import xml.etree.ElementTree as E

P=Path(__file__).parent
N="{http://www.w3.org/2000/svg}"
E.register_namespace("",N[1:-1])
root=E.parse(P/'proposal-01.relationship.before.svg').getroot()
lookup={e.get('data-miro-id'):e for e in root.iter() if e.get('data-miro-id')}
base='https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget='
def anchor(label,id):
    return f'<a href="{base}{id}">{label}</a>'

changes={
    '3458764690359619735': '6. Merge to main<br>Promotion: see '+anchor('01D','3458764690575950778'),
    '3458764690359619737': '10. Verify outcome<br>Return status<br>Checks: see '+anchor('01E','3458764690575950779'),
    '3458764690575950798': '<b>1. Review the PR</b><br>Checks and preview plans.<br>Review code and target impact.<br><b>01B: steps 1–5</b>',
    '3458764690575950799': '<b>2. Merge to main</b><br>Record the exact revision.<br>Production does not run<br>just because code merged.<br><b>01B: step 6</b>',
    '3458764690575950800': '<b>3. Apply to dev</b><br>Generate the final dev plan.<br>Authorize under dev policy.<br>Actions applies that plan.<br><b>01B: steps 7–9 for dev</b>',
    '3458764690575950801': '<b>4. Verify dev</b><br>Check settings and acceptance.<br>Record results before promotion.<br><b>01B: step 10</b><br>Test examples: '+anchor('01E','3458764690575950779'),
    '3458764690575950802': '<b>5. Promote to staging</b><br>Select the tested version.<br>Own plan, approval and apply.<br>Verify staging requirements.<br><b>Repeat 01B steps 7–10</b>',
    '3458764690575950803': '<b>6. Promote to production</b><br>Select the tested version.<br>Own plan, approval and apply.<br>Verify production requirements.<br><b>Repeat 01B steps 7–10</b>',
    '3458764690575950805': '<b>Required tests fail: stop promotion</b><br>01B step 10 supplies the acceptance evidence; failed required tests stop the next environment.<br>Correct the change and repeat review, planning and authorization as needed.',
    '3458764690575950820': '<b>Requirement / acceptance criteria</b><br>Agree these before starting 01B.',
    '3458764690575950821': '<b>Before apply: planned configuration</b><br>01B steps 2–8: checks, plans, review and authorization.',
    '3458764690575950822': '<b>After apply: deployed behavior</b><br>01B step 10: verify outcome and return status.',
    '3458764690575950837': '<b>01B checks and plan: before apply</b><br>terraform validate checks syntax and consistency.<br>Plan review checks intended changes and replacements.<br>These feed review and approval in 01B steps 2–8.',
    '3458764690575950838': '<b>01B step 10: acceptance before promotion</b><br>Verify requirements and record the deployment evidence.<br>Successful apply alone does not establish acceptance.<br>Required tests must pass before the next stage in '+anchor('01D','3458764690575950778')+'.',
}
text_changes={
    '3458764690359619719': 'Developer / reviewers / DevOps | Proposed | Core workflow for one target; see 01D for promotion and 01E for validation.',
    '3458764690575950791': 'Supporting view for '+anchor('01B','3458764690359619683')+' | Draft recommendation | Shows how its core workflow repeats across dev, staging and production.',
    '3458764690575950797': '01D expands 01B across environments; each process box names the corresponding 01B steps',
    '3458764690575950817': 'Supporting view for '+anchor('01B','3458764690359619683')+' | Draft | Explains checks before apply and the requirement tests within step 10, Verify outcome.',
    '3458764690575950819': '01E expands 01B validation: agree criteria first, inspect planned changes, then test the actual environment',
}
patch=E.Element(N+'svg')
for f in root:
    if f.tag!=N+'g':
        continue
    edited=[]
    for e in f:
        id=e.get('data-miro-id')
        if id in changes:
            c=E.Element(N+'rect',{'id':e.get('id'),'data-miro-id':id,'data-content':changes[id]})
            edited.append(c)
        elif id in text_changes:
            c=E.Element(N+'textArea',{'id':e.get('id'),'data-miro-id':id})
            fragment=E.fromstring('<body>'+text_changes[id]+'</body>')
            c.text=fragment.text
            for child in fragment:
                c.append(child)
            edited.append(c)
    if f.get('data-miro-id')=='3458764690359619683':
        cue=E.Element(N+'textArea',{'id':'workflow-detail-links','x':'68','y':'1680',
          'width':'2156','height':'54','fill':'#595959','font-family':'noto_sans','font-size':'19','text-align':'left'})
        fragment=E.fromstring('<body>Supporting detail views: '+anchor('01D: repeat this workflow across environments','3458764690575950778')+'<br/>'+anchor('01E: before-apply checks and step 10 acceptance tests','3458764690575950779')+'</body>')
        cue.text=fragment.text
        for child in fragment:
            cue.append(child)
        edited.append(cue)
    if edited:
        wrapper=E.SubElement(patch,N+'g',{'id':f.get('id'),'data-miro-id':f.get('data-miro-id'),
            'data-frame':f.get('data-frame'),'transform':f.get('transform')})
        wrapper.append(copy.deepcopy(f[0]))
        for e in edited:
            wrapper.append(e)
E.indent(patch)
E.ElementTree(patch).write(P/'proposal-01.relationship.update.svg',encoding='utf-8',xml_declaration=True)
assert len(changes)==14 and len(text_changes)==5
print('Prepared 19 existing label edits and one navigation cue; positions and user connectors preserved.')
