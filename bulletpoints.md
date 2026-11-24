Add terraform tool to review every pr (Use github action runner)
main branch -> dev environment | (run terraform plan -> view results -> approval -> terraform apply)
Mono repo for terraform, gitops, ansible, and any type of code related in devops team (review pros and cons first)
Mono repo for trekai platform e.g. LMS/HUB repo's has 16, we need to put them all in one repo (mono) (review pros and cons with app developers)
Mono repo for trekai platform e.g. Trekfinder/CAP repo's has XX, we need to put them all in one repo (mono) (review pros and cons with app developers)
Add  QA environment/lab ( we have dev, staging, production)
way to target it's testing / release manifest
QA must have the ability to run the code to setup the environment? 
There might be a need of another/different environment based on needs

Documentation / knowledge base streamline (focus on devops, cloud architecture and trekai product)
current documentation seems to be incomplete and fragmented

Observability (deployed but seems to be not yet fully implemented or beign used effectively?)
enable alerting for the team

Use Microsoft Entra ID as the Identity Provider (IdP) for Google Cloud.
Review and change  permissions in google cloud
naming conventions must make sense
Use Microsoft Entra ID as the Identity Provider (IdP) for Github
Review current setup or map of teams/groups in github
naming conventions must make sense
Implement PAM (just in time access / temporary elevated access)
Must figure out the team structure to plan the default access
default access based on role
elevated access via pam
Gitops / SDLC - centralizing and simplifying current type actions