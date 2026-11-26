# AnujHealth Deployment Platform (demo-app)

A production-style CI/CD platform for a fictional regulated health company,
AnujHealth. A FastAPI service is built and scanned once, stored as an
immutable image in Amazon ECR, and deployed to EC2 through AWS Systems
Manager. There is no SSH, and every release is health-checked with automatic
rollback.

## Architecture
GitHub → Jenkins (on-prem, Docker) → Amazon ECR → AWS SSM Run Command → EC2 (Docker)

_Diagram: TODO_

## Pipelines
| Pipeline | File | What it does |
|---|---|---|
| CI | `Jenkinsfile.ci` | Builds the image (linux/amd64), tags `1.0.<build>`, pushes to ECR |
| CD | `Jenkinsfile.cd` | Deploys a version via SSM, health-checks `/health`, auto-rolls back to `PREVIOUS_VERSION` on failure |

## Security decisions
- **No SSH:** port 22 closed; access through SSM Session Manager (IAM + audit logs)
- **Least privilege:** the Jenkins IAM user can only push to the `demo-app` repo and send SSM commands
- **Instance role** pulls from ECR, so there are no credentials on the server
- **Immutable image tags:** a released version can never be overwritten
- **Security group:** HTTP from a known IP only

## Deploy / roll back
- Deploy: run `demo-app-cd` with `VERSION=<tag>`
- Rollback: automatic on a failed health check, to `PREVIOUS_VERSION`

## Lessons learned
- **ARM vs. x86:** images built on Apple Silicon failed on EC2 with `exec format error`;
  fixed with `docker build --platform linux/amd64`
- **Tag case-sensitivity:** SSM targeted `App=demo`, the instance had `app=demo`, so zero targets
  and a silent hang. Deploy scripts now surface errors instead of swallowing them

## Costs and teardown
_TODO_

## Next upgrades
- [ ] CI triggers CD automatically; versions tracked in Parameter Store
- [ ] pytest + Trivy gates
- [ ] Dev → prod promotion with recorded approval and audit log
- [ ] Separate prod AWS account (cross-account roles)
- [ ] ALB + rolling deploys
- [ ] CloudWatch logs, alarms, SNS
- [ ] Infrastructure in CloudFormation
- [ ] Short-lived credentials instead of access keys