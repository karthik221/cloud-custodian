Yes, but I’d separate **Port’s role in the process** from **the system that owns and deploys AWS permissions**. Port can provide the developer experience and trigger work. For organization-wide provisioning permissions, I’d keep the permission definitions versioned and deploy them through your AWS infrastructure pipeline.

| Choice | Pros | Cons | Fit |
|---|---|---|---|
| **Port’s IAM permission workflow guide** | Fastest way to offer permission requests and revocation in Port; tracks requests in the catalog; supports time-bound grants. | It addresses requesting permissions for AWS resources, which is different from maintaining the cross-account provisioning role for every golden path. Port’s guide uses GitHub Actions and an IAM user with broad IAM operations on `Resource: "*"`, which would need redesign for a production multi-account setup. [Port’s guide](https://docs.port.io/guides/all/iam-permissions-guide/) | Good if developers need temporary access requests. **Not my choice as the policy source of truth for this problem.** |
| **Port actions/workflows with a custom backend** | Keeps the developer experience in Port; you can validate inputs, open a pull request, trigger a workflow, show status, and record the result. Port supports self-service actions backed by your existing workflow systems. [Port self-service actions](https://docs.port.io/workflows/actions-and-automations/create-self-service-experiences/) | You own the backend, security checks, retries, audit trail, and policy lifecycle. Directly changing IAM from a Port action can make policy changes harder to review and reproduce. | Useful as the **front door** to a governed pipeline. |
| **Policy-as-code repository + CI + AWS StackSets** | Makes each golden path’s permissions reviewable, testable, versioned, and traceable. StackSets can target an OU and its child OUs, with automatic deployment to accounts added to the target OU. [AWS StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-associate-stackset-with-org.html) | Requires building and operating the permission manifest format, policy generation, validations, and deployment pipeline. | **Best fit for consistent cross-account role permissions across nested OUs and environments.** |
| **AWS-native controls such as SCPs and permission boundaries** | Useful guardrails: constrain what Port’s role or other principals can do, even when an identity policy grants access. | They don’t grant the actions a golden path needs; you still need identity policies on the role. [AWS Organizations security guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/organizations-security.html) | Use alongside the policy pipeline, not instead of it. |

## Recommendation

Use a **hybrid**:

- Port owns the catalog, golden-path interface, and workflow initiation.
- Each golden path declares its required AWS permissions in a versioned manifest.
- A CI pipeline validates the change and produces a reviewable policy update.
- CloudFormation StackSets deploy the approved role policies to the target OUs and accounts.
- SCPs and permission boundaries enforce organization guardrails.
- Port shows the rollout status and links back to the change record.

That way, onboarding a new service requires a permission change alongside the golden-path change. Port can initiate or track that change, while your AWS deployment pipeline remains the controlled mechanism for applying it. I would reserve Port’s IAM permission workflow pattern for **developer access requests**; it is not, by itself, the OU-wide policy distribution mechanism you need.

==============

Since the Port provisioning role already exists in each target account, the change is **attaching additional permissions to that role as golden paths are onboarded**.

That’s a valid automation pattern, but I’d make **your IAM policy-as-code pipeline the source of truth** and use Port as the trigger and status surface. Port workflows can invoke a backend such as GitHub Actions, but Port’s IAM guide demonstrates creating and revoking temporary roles; it doesn’t document updating a standing cross-account provisioning role across target accounts. [Port IAM permission guide](https://docs.port.io/guides/all/iam-permissions-guide/)

A good flow is:

1. A golden path adds its required permissions in a versioned manifest.
2. CI reviews and validates the policy change.
3. The deployment pipeline attaches the approved policy to the existing Port role in the target accounts, using StackSets or your existing IaC deployment system.
4. Port shows the request and rollout status.

So Port **can handle the workflow around the change**, and a custom Port action could trigger the deployment. I would avoid making Port itself the authoritative place where teams define or directly edit AWS permissions; keep that in reviewed, version-controlled IaC. StackSets support OU targeting, including child OUs when a parent OU is targeted. [AWS StackSets and Organizations](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-associate-stackset-with-org.html)



======================

**Confirmed—with an important distinction:** Port’s IAM permission guide does not provide a built-in, OU-wide mechanism for applying new policies to an existing cross-account provisioning role.

As written, the guide creates a **new IAM role and policy** through GitHub Actions using configured AWS credentials. The workflow calls `create-policy`, `create-role`, and `attach-role-policy`; its trust policy names an AWS account principal so users from that account can assume the temporary role. That’s a different pattern from updating a standing Port provisioning role across target accounts. [Port’s IAM permission workflow guide](https://docs.port.io/guides/all/iam-permissions-guide/)

The guide does use a single configured `AWS_ACCOUNT_ID`, and the sample workflow doesn’t show assuming roles into multiple target accounts or deploying through OUs. So it doesn’t cover your multi-account rollout **out of the box**.

You could customize its GitHub Actions backend to assume a deployment role in each target account and apply policies there. For consistent OU-wide rollout, I’d have Port trigger or track a policy-as-code pipeline and let AWS StackSets distribute the approved changes.

==============
