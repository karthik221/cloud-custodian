# Enterprise Multi-Cloud Advisory Recommendation & Remediation Platform



Recommended architecture

&#x20;Centralized Multi-Cloud Advisory Intelligence Platform with a Provider-Native Remediation Engine



As a Senior Agentic Architect, I would approach this as an enterprise platform engineering initiative rather than simply building a dashboard or an agent.

The problem has four distinct responsibilities:

1. Discover: Collect recommendations across 1,000 AWS accounts and 1,000 Azure subscriptions.
2. Understand: Normalize recommendations, classify them by category, identify affected resources, calculate business impact and prioritize remediation.
3. Act: Execute approved remediation actions against AWS and Azure resources.
4. Close the loop: Update the recommendation status with the respective cloud provider and verify that the recommendation is actually resolved.

My strongest recommendation is to build a provider-agnostic advisory data platform with provider-specific collection and remediation adapters.

Do not make AWS or Azure the system of record for your enterprise governance process. Equally, do not discard the native provider data and retain only a normalized representation.

I would use a hybrid data strategy:

- Preserve the original AWS and Azure recommendation payloads.
- Transform them into a common enterprise recommendation model.
- Maintain provider-specific extensions for information that cannot be represented uniformly.
- Maintain a separate remediation and governance lifecycle.
- Expose the data through APIs to dashboards, automation and agentic applications.

This gives you a foundation to add GCP, OCI and other cloud providers without redesigning the platform.

# 1. Target architecture

[Multi-Cloud Detection at Scale: A Normalization Framework](https://images.openai.com/static-rsc-4/s0VhHeV1Ab2rNZh__58_yTn79ctfND36goC-Dh4LGqWVByKv1nxfVCnsPF9Ne5mVoCmbk05w1zd8FO2Kvwv-in0fG9b8W89k1eivyHITSvNFrBSzbRTDb46izV-fas1-Sgfr9wxejWfkdJr4gs_2mnMN8ilP3zL4JKZPZHeZc0c?purpose=inline)

[cloudnativedetection.substack.com](https://cloudnativedetection.substack.com/p/multi-cloud-detection-at-scale-a?utm_source=chatgpt.com)

I would divide the solution into six logical layers.

Layer 1

Cloud provider data sources

AWS Trusted Advisor, AWS Organizations, Azure Advisor, Azure Resource Graph, Azure Resource Manager.

Layer 2

Collection and ingestion

AWS collectors, Azure collectors, scheduled jobs, event-driven triggers, pagination, retries and checkpoints.

Layer 3

Raw data and normalization

Raw payload storage, schema validation, common recommendation schema, resource enrichment, category mapping.

Layer 4

Enterprise advisory intelligence

Recommendation database, resource inventory, business impact, deduplication, prioritization, history and ownership.

Layer 5

Remediation and governance

Approval workflow, policy checks, Terraform/SSM/Automation Runbooks, execution, validation and provider status updates.

Layer 6

Consumption and intelligence

Splunk / Power Apps / Custom Dashboard, enterprise APIs, conversational AI and controlled remediation agents.

The key architectural principle is that collection, recommendation intelligence, remediation and visualization must be independently scalable.

For example, a failure in the Power Apps dashboard should not affect recommendation collection or remediation execution.

## 2. Data collection: AWS API vs Azure Resource Graph

This is one of the most important architectural decisions.

My recommendation is not to use the same collection mechanism for both clouds. Each provider has different strengths.

### 2.1 AWS: Trusted Advisor APIs

AWS provides Trusted Advisor APIs for programmatic access to recommendations.

The primary API operations to evaluate are:

| API                                          | Purpose                                             |
| -------------------------------------------- | --------------------------------------------------- |
| `ListRecommendations`                        | Retrieve recommendation summaries                   |
| `GetRecommendation`                          | Retrieve recommendation details                     |
| `ListRecommendationResources`                | Retrieve resources associated with a recommendation |
| `ListRecommendationSummaries`                | Retrieve recommendation summaries by category       |
| `BatchUpdateRecommendationResourceExclusion` | Manage resource exclusions where supported          |

The collection process should retrieve:

- Recommendation ID
- Recommendation category
- Recommendation type
- Description
- Status
- Severity
- Affected resources
- Estimated savings, where available
- Resource metadata
- Last updated timestamp

AWS collection strategy for 1,000 accounts

I would not deploy an independently managed collector in every account.

Instead:

[Use AWS Lambda with AWS Control Tower Audit account to inspect your multi-account setup | AWS Cloud Operations Blog](https://images.openai.com/static-rsc-4/R95QSlD6TPwf_khMBNwIRgO81M3WkVTuBLpoqq1gb9SzMQ5lfMHXAVQWAC6leNyiihegBc3hTYcwqkM43weSf8lDPJdVE2L7C-gATX54MKLEYHfQEIKDOX9WJrpClx6LKm2Hr7Cy-CTP7Ew-exJ7NMU1TJCE_rKfl0op382CWok?purpose=inline)

[aws.amazon.com](https://aws.amazon.com/blogs/mt/use-aws-lambda-with-aws-control-tower-audit-account-to-inspect-your-multi-account-setup/?utm_source=chatgpt.com)

1. Create a central AWS collection account.
2. Deploy a cross-account IAM role in each of the 1,000 accounts.
3. Establish a trusted relationship with the central collector role.
4. Use AWS Organizations to maintain account inventory.
5. Run collection workers through Step Functions, Lambda or ECS.
6. Collect Trusted Advisor recommendations using the appropriate account context.
7. Store the original payload in S3.
8. Publish normalized records to the enterprise data layer.

An important distinction: evaluate AWS Trusted Advisor organizational-level capabilities and the applicable AWS Organizations integration before deciding to assume roles into all 1,000 accounts. Some recommendation collection capabilities are available through centralized organizational views, while others have account-level or support-plan restrictions.

I would prefer centralized organization-level collection wherever the specific recommendation API supports it, and use cross-account collection for the remaining coverage.

AWS implementation considerations

- AWS Organizations account discovery.
- Trusted Advisor API quotas and throttling.
- Exponential backoff and retry.
- Account-level collection checkpoints.
- Pagination.
- Support-plan and feature availability.
- Regional versus global recommendation coverage.
- Collection completeness monitoring.

### 2.2 Azure: Azure Advisor API + Azure Resource Graph

For Azure, I would use a combination of Azure Advisor REST APIs and Azure Resource Graph.

These services serve different purposes.

Azure Advisor API

Primary recommendation source

Retrieves actual Azure Advisor recommendations, including:

- Recommendation ID
- Category
- Impact
- Description
- Recommendation metadata
- Affected resource ID
- Suppression information
- Recommendation status and lifecycle information where exposed.

Azure Resource Graph

Resource enrichment and inventory

Retrieves:

- Resource IDs
- Resource types
- Resource groups
- Subscription IDs
- Locations
- Resource tags
- Additional resource properties
- Relationships and resource inventory context.

The distinction matters.

Azure Resource Graph is not a replacement for the Azure Advisor API.

ARG is excellent at querying large-scale Azure resource inventory. However, the authoritative recommendation information should come from Azure Advisor.

I would use the following flow:

1. Enumerate subscriptions using Azure management hierarchy APIs.
2. Use Azure Advisor REST APIs to collect recommendation records.
3. Capture affected resource IDs.
4. Use Azure Resource Graph to enrich affected resources.
5. Capture resource ownership, tags, environment and other attributes.
6. Store raw Advisor responses.
7. Normalize into the common enterprise schema.

For 1,000 subscriptions, use a centralized service principal or managed identity with appropriately scoped read permissions, preferably through Azure Lighthouse or another approved delegated-access pattern where appropriate.

Do not execute an unrestricted ARG query for every resource every time you collect recommendations. Instead, query only the affected resource IDs when possible, and maintain a separate incremental resource inventory.

### 2.3 AWS vs Azure collection comparison

| Dimension           | AWS                                            | Azure                                                  |
| ------------------- | ---------------------------------------------- | ------------------------------------------------------ |
| Primary source      | Trusted Advisor APIs                           | Azure Advisor REST API                                 |
| Resource enrichment | AWS Resource APIs / Config                     | Azure Resource Graph                                   |
| Account discovery   | AWS Organizations                              | Management Groups / Subscriptions                      |
| Collection model    | Org view + cross-account roles                 | Central identity + subscription scope                  |
| Raw storage         | S3                                             | ADLS / central object storage                          |
| Main challenge      | API coverage, throttling, account-level access | Subscription permissions, pagination, ARG query limits |

My recommendation:

- AWS: Trusted Advisor API first, supplemented by AWS Config and resource-specific APIs.
- Azure: Advisor API first, supplemented by Azure Resource Graph.
- Both: preserve original provider payloads and enrich through a separate pipeline.

## 3. How should we collect data across 2,000 cloud scopes?

At this scale, I would implement a distributed, centrally orchestrated collection framework, not a single long-running job that iterates through all subscriptions and accounts sequentially.

### 3.1 Collection architecture

[Setting up real-time event delivery](https://images.openai.com/static-rsc-4/Mh5R0pFrGS_wkxNjdLAfpLsCfvSTgfx4YzcRFOoSw7GKRrECVZKvy1HpIkqZfcHXREs3utHSHAL196CdhTUh2eKCjDbuBqhOYQHYd9gLFfrxrUiCYoaIQfMdtOeUKujDu75OW3maVt0fBHG7quxkY48VHVokqb4s9_XBBnJk8wQ?purpose=inline)

[developers.pismo.io](https://developers.pismo.io/pismo-docs/docs/setting-up-real-time-event-delivery?utm_source=chatgpt.com)

Recommended components:

| Component       | AWS implementation  | Azure implementation             |
| --------------- | ------------------- | -------------------------------- |
| Scope discovery | AWS Organizations   | Azure Management Groups          |
| Scope inventory | Organizations API   | Subscription APIs                |
| Collector       | Lambda / ECS        | Azure Functions / Container Apps |
| Orchestration   | Step Functions      | Durable Functions                |
| Queue           | SQS                 | Service Bus                      |
| Raw storage     | S3                  | ADLS Gen2                        |
| Processing      | Glue / ECS / Lambda | Databricks / Functions           |
| Monitoring      | CloudWatch          | Azure Monitor                    |

You do not necessarily need to deploy all these services. Select one primary orchestration and processing approach rather than creating unnecessary infrastructure in both clouds.

### 3.2 Collection execution model

I would design the collection process as follows:

\#chatgpt-mermaid-\_r_cd\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_cd\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_cd\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_cd\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_cd\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_cd\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_cd\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_cd\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_cd\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_cd\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_cd\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_cd\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_cd\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_cd\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_cd\_ p{margin:0;}#chatgpt-mermaid-\_r_cd\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_cd\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_cd\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_cd\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_cd\_ .label text,#chatgpt-mermaid-\_r_cd\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_cd\_ .node rect,#chatgpt-mermaid-\_r_cd\_ .node circle,#chatgpt-mermaid-\_r_cd\_ .node ellipse,#chatgpt-mermaid-\_r_cd\_ .node polygon,#chatgpt-mermaid-\_r_cd\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_cd\_ .rough-node .label text,#chatgpt-mermaid-\_r_cd\_ .node .label text,#chatgpt-mermaid-\_r_cd\_ .image-shape .label,#chatgpt-mermaid-\_r_cd\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_cd\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_cd\_ .rough-node .label,#chatgpt-mermaid-\_r_cd\_ .node .label,#chatgpt-mermaid-\_r_cd\_ .image-shape .label,#chatgpt-mermaid-\_r_cd\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_cd\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_cd\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_cd\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_cd\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_cd\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_cd\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_cd\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_cd\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_cd\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_cd\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_cd\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_cd\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_cd\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_cd\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_cd\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_cd\_ .icon-shape,#chatgpt-mermaid-\_r_cd\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_cd\_ .icon-shape p,#chatgpt-mermaid-\_r_cd\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_cd\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_cd\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_cd\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_cd\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_cd\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_cd\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_cd\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_cd\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_cd\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_cd\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_cd\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_cd\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_cd\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_cd\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_cd\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_cd\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_cd\_ .node rect,#chatgpt-mermaid-\_r_cd\_ .node circle,#chatgpt-mermaid-\_r_cd\_ .node ellipse,#chatgpt-mermaid-\_r_cd\_ .node polygon,#chatgpt-mermaid-\_r_cd\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_cd\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_cd\_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_cd\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_cd\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_cd\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Scheduled Collection TriggerScope DiscoveryDiscover 1000 AWS AccountsDiscover 1000 AzureSubscriptionsAWS Collection QueueAzure Collection QueueAWS Trusted AdvisorWorkersAzure Advisor WorkersRaw Payload StorageSchema ValidationNormalization andEnrichmentEnterprise RecommendationStoreDashboard and AnalyticsRemediation WorkflowProvider Status UpdatePost-RemediationVerification

How I would execute the collection:

1. Discover all active AWS accounts and Azure subscriptions.
2. Create collection jobs at the account/subscription level.
3. Publish jobs into provider-specific queues.
4. Process multiple jobs concurrently with controlled concurrency.
5. Implement pagination and retry logic.
6. Save every original API response to raw storage.
7. Publish a collection-completed event.
8. Start normalization and enrichment.
9. Update the central recommendation database.
10. Record collection timestamp and completeness.

### 3.3 How frequently should we collect?

I would not use the same collection frequency for every type of information.

| Data                              | Recommended frequency                                   |
| --------------------------------- | ------------------------------------------------------- |
| Recommendation collection         | Every 6–12 hours                                        |
| Critical security recommendations | Every 1–4 hours, subject to provider refresh capability |
| Resource inventory                | Every 12–24 hours                                       |
| Account/subscription inventory    | Every 12–24 hours and event-triggered                   |
| Remediation execution status      | Event-driven                                            |
| Post-remediation verification     | After execution, followed by provider refresh           |
| Historical analytics              | Daily                                                   |

These are proposed scheduling targets, not guarantees of how quickly AWS or Azure generates fresh recommendations.

An important consideration: collecting recommendations every hour does not mean the underlying provider has recalculated them every hour.

For AWS, Trusted Advisor refresh capabilities and support-plan eligibility must be considered. AWS Trusted Advisor API access requires Business Support+, Enterprise Support or Unified Operations. The organizational view also has support-plan and member-account limitations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

AWS Support+2



For Azure, Advisor provides cached recommendations, and the API supports continuation tokens for pagination.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learn.microsoft.com\&sz=32)

Microsoft Learn+1



### 3.4 Important AWS consideration: Standard vs Priority recommendations

This is a design detail I would explicitly validate during the proof of concept.

AWS Trusted Advisor has two different concepts:

- Standard recommendations: Normal Trusted Advisor checks, including cost optimization, security, fault tolerance, performance and service limits.
- Priority recommendations: Recommendations managed through Trusted Advisor Priority.

The AWS APIs `ListOrganizationRecommendations` and `ListOrganizationRecommendationResources` are specifically for Priority recommendations. They are not a universal replacement for collecting every standard recommendation across an organization.

For standard recommendations, use `ListRecommendations`, `GetRecommendation` and `ListRecommendationResources` with the appropriate account context.

Also, the API exposes global recommendations, so you do not need to make redundant regional calls for those recommendations.

This distinction is critical when designing the AWS collector.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

AWS Support+2



# 4. Data architecture: Unified schema vs raw data

This is probably the most important long-term architectural decision.

I would strongly recommend a hybrid data model: Raw + Canonical + Provider Extension.

Do not choose exclusively between raw data and a unified schema.

Each serves a different purpose.

## 4.1 Why not store only raw data?

Suppose AWS reports:

- Unattached EBS volumes.
- Underutilized EC2 instances.
- S3 buckets without encryption.

Azure reports:

- Unattached managed disks.
- Underutilized virtual machines.
- Storage accounts without encryption.

If you retain only raw provider payloads, every dashboard, report and agent needs to understand AWS and Azure-specific response structures.

That results in:

- Duplicated transformation logic.
- Provider-specific dashboard queries.
- Complex cross-cloud reporting.
- Difficult prioritization.
- Increased complexity when adding GCP.

## 4.2 Why not store only a unified model?

Because cloud providers expose different information.

For example:

- AWS has Trusted Advisor check identifiers.
- Azure has Advisor recommendation type GUIDs.
- AWS has recommendation lifecycle stages for Priority recommendations.
- Azure has recommendation states such as Active, Postponed, Dismissed and Completed.
- AWS and Azure have different cost-saving calculation methods.
- Recommendation remediation instructions vary considerably.

If you discard these details during normalization, you lose useful information for remediation and future analytics.

## 4.3 Recommended three-layer storage model

Layer A — Raw data

Immutable

Store original provider API payloads in JSON/Parquet format.

Suggested storage:

- S3
- ADLS Gen2

Partition by provider, scope, collection date and recommendation category.

Layer B — Canonical data

Unified

Standardized enterprise recommendation schema.

Used by:

- Dashboards
- Analytics
- Search
- Reporting
- Agentic applications

Layer C — Provider extensions

Extensible

Store provider-specific fields, original identifiers, remediation instructions and native lifecycle attributes.

This preserves provider functionality without polluting the common schema.

I would also separate the recommendation data from the remediation execution database. They have different update patterns and transactional requirements.

## 4.4 Proposed canonical data model

I would create the following logical entities.

| Entity                 | Purpose                                    |
| ---------------------- | ------------------------------------------ |
| CloudProvider          | AWS, Azure, GCP                            |
| CloudOrganization      | AWS Organization / Azure Tenant            |
| CloudScope             | AWS Account / Azure Subscription           |
| Recommendation         | Master recommendation definition           |
| RecommendationInstance | Recommendation in a particular scope       |
| AffectedResource       | Resources associated with a recommendation |
| ResourceInventory      | Resource details and ownership             |
| RecommendationCategory | Standardized categories                    |
| RemediationPlan        | Proposed remediation steps                 |
| RemediationExecution   | Actual execution details                   |
| Approval               | Approval and risk acceptance               |
| RecommendationHistory  | Historical state changes                   |
| CollectionRun          | Collector execution and completeness       |
| ProviderStatusSync     | Status synchronization with cloud provider |

### Relationship model

\#chatgpt-mermaid-\_r_da\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_da\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_da\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_da\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_da\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_da\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_da\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_da\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_da\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_da\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_da\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_da\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_da\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_da\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_da\_ p{margin:0;}#chatgpt-mermaid-\_r_da\_ .entityBox{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_da\_ .relationshipLabelBox{fill:rgb(48, 48, 48);opacity:0.7;background-color:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_da\_ .relationshipLabelBox rect{opacity:0.5;}#chatgpt-mermaid-\_r_da\_ .labelBkg{background-color:rgba(48, 48, 48, 0.5);}#chatgpt-mermaid-\_r_da\_ .edgeLabel{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_da\_ .edgeLabel .label rect{fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_da\_ .edgeLabel .label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_da\_ .edgeLabel .label{fill:rgb(31, 78, 148);font-size:14px;}#chatgpt-mermaid-\_r_da\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_da\_ .edge-pattern-dashed{stroke-dasharray:8,8;}#chatgpt-mermaid-\_r_da\_ .node rect,#chatgpt-mermaid-\_r_da\_ .node circle,#chatgpt-mermaid-\_r_da\_ .node ellipse,#chatgpt-mermaid-\_r_da\_ .node polygon{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_da\_ .relationshipLine{stroke:rgb(175, 175, 175);stroke-width:1px;fill:none;}#chatgpt-mermaid-\_r_da\_ .marker{fill:none!important;stroke:rgb(175, 175, 175)!important;stroke-width:1;}#chatgpt-mermaid-\_r_da\_ [data-look=neo].labelBkg{background-color:rgba(48, 48, 48, 0.5);}#chatgpt-mermaid-\_r_da\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_da\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_da\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_da\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_da\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_da\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_da\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_da\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_da\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_da\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}CLOUD_PROVIDERCLOUD_SCOPERECOMMENDATION_INSTANCERECOMMENDATIONRECOMMENDATION_CATEGORYAFFECTED_RESOURCERESOURCE_INVENTORYREMEDIATION_PLANREMEDIATION_EXECUTIONAPPROVALRECOMMENDATION_HISTORYPROVIDER_STATUS_SYNCCOLLECTION_RUNcontainsdiscoversdefinesclassifiesimpactsidentifieshasexecutesrequirestrackssynchronizesdiscovers

### 4.5 Example canonical recommendation record

Here is an example of how I would represent an underutilized compute recommendation.

```
{
  "recommendation_key": "rec-10001",
  "provider": "AWS",
  "scope": {
    "account_id": "123456789012",
    "organization_id": "org-123"
  },
  "recommendation": {
    "native_id": "native-recommendation-id",
    "category": "COST_OPTIMIZATION",
    "subcategory": "COMPUTE_RIGHTSIZING",
    "title": "Underutilized compute resource",
    "severity": "MEDIUM",
    "provider_status": "warning"
  },
  "resources": [
    {
      "resource_id": "i-0123456789abcdef0",
      "resource_type": "AWS::EC2::Instance",
      "region": "us-east-1",
      "environment": "PRODUCTION",
      "owner": "application-team-a"
    }
  ],
  "impact": {
    "estimated_monthly_savings": 250,
    "currency": "USD"
  },
  "governance": {
    "enterprise_status": "OPEN",
    "remediation_status": "NOT_STARTED",
    "approval_required": true
  },
  "timestamps": {
    "first_detected": "2026-11-01T00:00:00Z",
    "last_collected": "2026-11-04T00:00:00Z"
  }
}
```

This is illustrative, not an actual Trusted Advisor API response.

Notice that I have deliberately separated:

- `provider_status`
- `enterprise_status`
- `remediation_status`

These should never be treated as the same field.

For example, a recommendation can still be `warning` at AWS while the enterprise remediation workflow is `IN_PROGRESS`.

### 4.6 Category standardization

I would establish a common enterprise taxonomy rather than directly adopting AWS or Azure categories.

| Enterprise category    | AWS examples                        | Azure examples                         |
| ---------------------- | ----------------------------------- | -------------------------------------- |
| Cost Optimization      | Idle EC2, unattached EBS            | Idle VMs, unattached disks             |
| Security               | IAM risks, public S3                | NSG risks, storage encryption          |
| Reliability            | Multi-AZ, backup gaps               | Availability, backup gaps              |
| Performance            | EC2 optimization                    | VM sizing                              |
| Operational Excellence | Configuration gaps                  | Operational recommendations            |
| Service Lifecycle      | Service limits, deprecated services | Retirement and upgrade recommendations |
| Sustainability         | Resource efficiency                 | Resource efficiency                    |

I would use a two-level taxonomy:

- Level 1: Enterprise category.
- Level 2: Enterprise subcategory.

Keep the original provider category alongside it.

This becomes particularly valuable when leadership asks questions such as:

- How many security recommendations are open across all clouds?
- How much cost-saving opportunity exists across AWS and Azure?
- Which business units have the highest number of reliability findings?
- Which recommendations have remained open for more than 90 days?

## 4.7 How to associate recommendations with resources

This is particularly important because your end goal is not just a recommendation count; it is a recommendation-to-resource relationship.

I would use a many-to-many relationship.

Example:

Recommendation: Underutilized Compute

COST OPTIMIZATION · MEDIUM

AWS Account A

4 resources

- EC2 Instance 1
- EC2 Instance 2
- EC2 Instance 3
- EC2 Instance 4

  Azure Subscription B

  3 resources
- Virtual Machine 1
- Virtual Machine 2
- Virtual Machine 3

  Enterprise recommendation total

# 7 resources

One recommendation definition can have thousands of instances across scopes and multiple affected resources per instance.

Use a stable identity based on:

`Provider + Scope ID + Native Recommendation ID`

For affected resources, use:

`Provider + Canonical Resource ID + Recommendation Instance ID`

Also maintain the first-seen and last-seen timestamps. This enables trend reporting and prevents duplicate records during repeated collection runs.

# 5. Remediation architecture: Acting on recommendations

This is where I would invest significant architectural attention.

Collecting recommendations is relatively straightforward. Safely remediating thousands of resources across different cloud providers is considerably more complex.

I would avoid allowing the collection service or an AI agent to directly modify resources.

Instead, introduce a dedicated Remediation Orchestration Service.

[Multi-Cloud Compliance Automation — End-to-End Implementation | by Jegangopal | Medium](https://images.openai.com/static-rsc-4/B7nn98kUWHI3xKNWuGy1IIvXwTgRsikSmrJhEFYeAR_82Ptf2kfqF-uxg_Bk5dM0kuzJ3rQth2ZAkHhyfotwZhDdAQRbvhkqDfVmSCicY0icBx3I1BJBV_aq-inuWSrAWELrYJSSMcGuK6ZD03rowYVcNP8rizVLGhY26allh2I?purpose=inline)

[medium.com](https://medium.com/%40jegangopal09/multi-cloud-compliance-automation-end-to-end-implementation-09dc7dd8269a?utm_source=chatgpt.com)

## 5.1 Remediation lifecycle

I would define an enterprise lifecycle independently of AWS and Azure.

| Enterprise status    | Meaning                            |
| -------------------- | ---------------------------------- |
| OPEN                 | Recommendation discovered          |
| TRIAGED              | Assessed and prioritized           |
| APPROVAL_PENDING     | Waiting for approval               |
| APPROVED             | Approved for execution             |
| IN_PROGRESS          | Remediation running                |
| REMEDIATED           | Change successfully executed       |
| VERIFICATION_PENDING | Waiting for cloud validation       |
| CLOSED               | Resolution verified                |
| EXCEPTION            | Risk accepted or exception granted |
| FAILED               | Remediation failed                 |

The enterprise status is your internal governance record. It does not necessarily match the provider's status.

## 5.2 Remediation execution framework

I would use three remediation execution patterns.

| Remediation type             | AWS                        | Azure                   |
| ---------------------------- | -------------------------- | ----------------------- |
| Configuration changes        | SSM Automation             | Azure Automation        |
| Infrastructure changes       | Terraform / CloudFormation | Terraform / ARM / Bicep |
| Resource-specific operations | AWS SDK / service APIs     | Azure SDK / REST APIs   |

For example:

| Recommendation         | Remediation                                                              |
| ---------------------- | ------------------------------------------------------------------------ |
| Unattached EBS volume  | Validate ownership and snapshot requirements, then delete after approval |
| Public S3 bucket       | Apply approved bucket access policy                                      |
| Underutilized EC2      | Recommend rightsizing; execute after workload owner approval             |
| Unattached Azure disk  | Validate backup and retention requirements, then delete                  |
| Storage encryption gap | Apply approved encryption configuration                                  |
| Idle Azure VM          | Deallocate or resize after business validation                           |

Not every recommendation should be automatically remediated.

### 5.3 Introduce remediation risk classification

Tier 1

Low-risk automation

Examples: Enable approved diagnostic settings, apply missing tags, enable certain monitoring configurations.

Automatic execution may be allowed when policy conditions are satisfied.

Tier 2

Approval-based automation

Examples: Resize VMs, modify security groups, change storage configurations.

Require application owner or platform team approval.

Tier 3

High-impact remediation

Examples: Delete resources, change production network architecture, modify critical identity permissions.

Require formal change management, security review and explicit approval.

I would also introduce:

- Pre-execution configuration snapshots.
- Dry-run support.
- Idempotency.
- Rollback procedures.
- Execution timeouts.
- Resource locks where appropriate.
- Separation of duties.
- Full audit logging.

### 5.4 How do we update the cloud provider after remediation?

This is an important distinction: remediating the resource and updating the recommendation status are two different operations.

They should be implemented as separate workflow steps.

AWS

For standard Trusted Advisor recommendations, do not assume that there is a general-purpose API to mark any recommendation as resolved.

AWS recommendation statuses such as `ok`, `warning` and `error` reflect the check result.

The `UpdateRecommendationLifecycle` API supports Trusted Advisor Priority recommendations, with lifecycle stages such as:

- `pending_response`
- `in_progress`
- `dismissed`
- `resolved`

It is not a universal lifecycle-update API for standard recommendations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

AWS Trusted Advisor+1



Therefore:

1. Execute the AWS resource remediation.
2. Refresh or allow Trusted Advisor to refresh the check.
3. Collect the recommendation again.
4. Verify that its native status has changed.
5. Update the enterprise recommendation record.
6. For Priority recommendations, use the appropriate lifecycle API where applicable.

Azure

Azure provides recommendation state management.

The documented states include:

- Active
- Postponed
- Dismissed
- Completed

The recommendation can be marked completed, or Azure Advisor can verify that the issue has been resolved.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learn.microsoft.com\&sz=32)

Microsoft Learn+1



You can use the Azure Advisor recommendation update operation where supported by the applicable API version, or the suppression APIs for snoozing and dismissing recommendations.

One important version consideration: the newer recommendation-state update operation is documented in preview API versions. I would not make a preview API a production dependency without explicit approval and validation of its stability.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learn.microsoft.com\&sz=32)

Microsoft Learn+1



### 5.5 The most important design pattern: Reconciliation

I would introduce a dedicated reconciliation process.

\#chatgpt-mermaid-\_r_ej\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_ej\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_ej\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_ej\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_ej\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ej\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_ej\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_ej\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_ej\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_ej\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_ej\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_ej\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ej\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ej\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_ej\_ p{margin:0;}#chatgpt-mermaid-\_r_ej\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ej\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ej\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ej\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_ej\_ .label text,#chatgpt-mermaid-\_r_ej\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ej\_ .node rect,#chatgpt-mermaid-\_r_ej\_ .node circle,#chatgpt-mermaid-\_r_ej\_ .node ellipse,#chatgpt-mermaid-\_r_ej\_ .node polygon,#chatgpt-mermaid-\_r_ej\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_ej\_ .rough-node .label text,#chatgpt-mermaid-\_r_ej\_ .node .label text,#chatgpt-mermaid-\_r_ej\_ .image-shape .label,#chatgpt-mermaid-\_r_ej\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_ej\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_ej\_ .rough-node .label,#chatgpt-mermaid-\_r_ej\_ .node .label,#chatgpt-mermaid-\_r_ej\_ .image-shape .label,#chatgpt-mermaid-\_r_ej\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_ej\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_ej\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ej\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ej\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_ej\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_ej\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_ej\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_ej\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_ej\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_ej\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_ej\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ej\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ej\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_ej\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ej\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_ej\_ .icon-shape,#chatgpt-mermaid-\_r_ej\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_ej\_ .icon-shape p,#chatgpt-mermaid-\_r_ej\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_ej\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_ej\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_ej\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_ej\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_ej\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_ej\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_ej\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_ej\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_ej\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ej\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_ej\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ej\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_ej\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_ej\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_ej\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_ej\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_ej\_ .node rect,#chatgpt-mermaid-\_r_ej\_ .node circle,#chatgpt-mermaid-\_r_ej\_ .node ellipse,#chatgpt-mermaid-\_r_ej\_ .node polygon,#chatgpt-mermaid-\_r_ej\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_ej\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_ej\_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_ej\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_ej\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ej\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Recommendation IdentifiedCreate Remediation PlanApprovalExecute Resource ChangeExecution Successful?Mark Enterprise StatusFAILEDValidate ResourceConfigurationRefresh ProviderRecommendationProvider ConfirmsResolution?VERIFICATION_PENDINGUpdate Provider StatusWhere SupportedMark Enterprise StatusCLOSEDNoYesNoYes

I would also distinguish between:

- Remediation successful: The automation executed successfully.
- Resource compliant: The actual resource configuration meets the desired state.
- Recommendation resolved: The cloud provider no longer reports the issue or confirms completion.
- Enterprise closed: Your governance process has verified and recorded the resolution.

These are four different events.

This prevents the dashboard from reporting a recommendation as closed simply because a Terraform deployment succeeded.

# 6. How to make this extensible for GCP and other cloud providers

I would make this a first-class design requirement from Day 1.

Do not build an AWS collector, Azure collector and then hardcode their outputs into your dashboard.

Instead, implement a Cloud Provider Adapter Pattern.

## 6.1 Provider adapter architecture

[🧭 Cloud-Agnostic by Design: Hexagonal Architecture That Outlives Your Stack | by Chaos To Clarity | Medium](https://images.openai.com/static-rsc-4/UCUJCft8S68jH4IlVExz2f_fJCr8t8nOgLqOKYsQa3S7RCTV-Ig93WpZQKGqQKVZ5NVhdXY3NMUK0HLHgyYA7sV_jOHPvayMi87kUNJZgUmQZ_82lElm7YL9FHfA0lTxHCQJPG2Qw804VEjGtc2e96LHZVRHh9ITI4Z2c-mXvH8?purpose=inline)

[medium.com](https://medium.com/%40sonal.sadafal/cloud-agnostic-by-design-hexagonal-architecture-that-outlives-your-stack-03698ad8fd44?utm_source=chatgpt.com)

Each provider should implement a standard interface.

For example:

```
class CloudAdvisoryProvider:    def discover_scopes(self):        pass    def collect_recommendations(self, scope):        pass    def collect_affected_resources(self, recommendation):        pass    def enrich_resource_metadata(self, resource):        pass    def execute_remediation(self, remediation_plan):        pass    def update_provider_status(self, recommendation, status):        pass    def verify_remediation(self, recommendation):        pass
```

Implement separate adapters:

| Provider | Recommendation source | Resource inventory         |
| -------- | --------------------- | -------------------------- |
| AWS      | Trusted Advisor       | AWS Config / Resource APIs |
| Azure    | Azure Advisor         | Azure Resource Graph       |
| GCP      | Recommender API       | Cloud Asset Inventory      |

For GCP, the Google Cloud Recommender provides recommendations across several areas, including cost, security, reliability and performance. Cloud Asset Inventory can provide resource inventory and metadata enrichment.

The important thing is that the core recommendation-processing pipeline does not need to know how each provider collected the data.

It only consumes the canonical schema.

## 6.2 Provider capability registry

I would go one step further and introduce a provider capability registry.

Why?

Because not every cloud provider supports the same functionality.

For example:

| Capability                            | AWS               | Azure            | GCP                                  |
| ------------------------------------- | ----------------- | ---------------- | ------------------------------------ |
| Recommendation discovery              | Yes               | Yes              | Yes                                  |
| Resource association                  | Yes               | Yes              | Yes                                  |
| Native lifecycle updates              | Priority-specific | Supported states | Recommendation-specific capabilities |
| Automated remediation                 | Service-specific  | Service-specific | Service-specific                     |
| Provider-side resolution verification | Check-specific    | Advisor-specific | Recommender-specific                 |

Store these capabilities as metadata.

For example:

```
{
  "provider": "AWS",
  "capabilities": {
    "recommendation_read": true,
    "resource_discovery": true,
    "native_status_update": "PRIORITY_ONLY",
    "automated_remediation": true,
    "provider_verification": true
  }
}
```

This avoids making incorrect assumptions that all cloud providers expose identical APIs.

# 7. Should we build an Agentic use case on top of the centralized data?

My recommendation: Yes

I believe this is where the platform becomes significantly more valuable.

However, I would not start by building an autonomous remediation agent.

I would first establish the centralized data platform, deterministic remediation workflows and APIs. Then introduce AI agents as an intelligence and orchestration layer.

There are three stages of maturity.

## 7.1 Stage 1: Advisory Intelligence Chatbot

Build a conversational interface over the centralized recommendation database.

Examples of questions:

- Show me all critical security recommendations across AWS and Azure.
- Which AWS accounts have the highest number of open recommendations?
- Show recommendations affecting production resources.
- Which application teams have the most outstanding cost optimization opportunities?
- Show all resources associated with recommendations that have been open for more than 60 days.
- What are the top 10 remediation opportunities based on estimated savings?
- Compare AWS and Azure security recommendations by business unit.

This is essentially a natural-language interface to your centralized data.

Architecture:

User / Enterprise Dashboard

Conversational AI Interface

Agent / LLM + Query Orchestration

Read-only APIs

Recommendations, resources, cost, ownership

Enterprise Data

Canonical recommendation store

For this use case, I would use structured database queries rather than relying entirely on RAG.

For example, the question:

"Show me all critical security recommendations across production accounts"

should translate into a validated query against your recommendation database.

RAG is useful for:

- Understanding recommendation descriptions.
- Retrieving remediation documentation.
- Explaining why a recommendation matters.
- Searching internal cloud standards.
- Finding Terraform remediation examples.
- Explaining potential business impact.

Use SQL or governed APIs for counts, totals, filtering and financial calculations.

Do not let an LLM independently calculate enterprise reporting numbers from loosely retrieved documents.

## 7.2 Stage 2: Recommendation Analysis Agent

This is where you introduce actual agentic capabilities.

The agent should analyze recommendations and propose remediation.

For example:

User asks:

"Analyze all critical security recommendations in production across AWS and Azure and suggest remediation actions."

The agent performs:

1. Query the recommendation API.
2. Filter production resources.
3. Group recommendations by category.
4. Identify duplicated or related issues.
5. Retrieve remediation documentation.
6. Evaluate risk and potential impact.
7. Identify whether remediation is automated or manual.
8. Generate a remediation plan.
9. Present the plan for review.

The agent should return structured output.

Example:

| Resource       | Finding                | Proposed action            | Risk   |
| -------------- | ---------------------- | -------------------------- | ------ |
| EC2 Instance A | Public access exposure | Restrict security group    | High   |
| S3 Bucket B    | Encryption gap         | Enable approved encryption | Medium |
| Azure VM C     | Missing monitoring     | Enable diagnostic settings | Low    |

This is more valuable than a generic chatbot because it produces actionable recommendations.

## 7.3 Stage 3: Remediation Agent

Eventually, introduce an agent that can invoke approved remediation tools.

For example:

User:

"Remediate all low-risk recommendations in the development environment."

The agent:

1. Queries eligible recommendations.
2. Checks resource ownership and environment.
3. Checks remediation eligibility.
4. Generates a remediation plan.
5. Runs policy validations.
6. Requests approval if required.
7. Invokes the appropriate remediation tool.
8. Validates the resource.
9. Updates the enterprise lifecycle.
10. Synchronizes the provider status where supported.

### 7.4 Recommended agent/tool architecture

I would not build one giant agent with access to every AWS account and Azure subscription.

Instead, introduce specialized tools and potentially separate agents.

| Agent / service            | Responsibility                              |
| -------------------------- | ------------------------------------------- |
| Advisory Analysis Agent    | Analyze recommendations and identify trends |
| Cost Optimization Agent    | Identify savings opportunities              |
| Security Advisory Agent    | Analyze security findings                   |
| Remediation Planning Agent | Generate proposed remediation plans         |
| AWS Remediation Adapter    | Execute approved AWS actions                |
| Azure Remediation Adapter  | Execute approved Azure actions              |
| Verification Service       | Validate the actual resource state          |
| Governance Agent           | Track exceptions, approvals and closure     |

These can be independently deployed services. They do not all need to be autonomous LLM agents.

### 7.5 Important security controls for agentic remediation

Given that the agent can potentially act on 2,000 cloud scopes, I would implement:

- Entra ID or another enterprise identity integration.
- User-to-resource authorization.
- Per-account and per-subscription RBAC.
- Separate read and write tools.
- Least-privilege execution identities.
- Tool-level allowlists.
- Approval gates for sensitive operations.
- Environment-specific policies.
- Resource ownership validation.
- Complete execution audit trail.
- Rate limiting and blast-radius controls.
- Idempotent remediation operations.

The LLM should never receive unrestricted cloud credentials.

I would also ensure that the agent cannot bypass the remediation orchestration service by directly invoking cloud SDKs.

My architectural principle: The agent decides what should be done; the policy engine determines whether it is permitted; the remediation service executes it.

This separation is essential for enterprise-grade agentic governance.

# 8. Dashboard strategy: Splunk vs Power Apps vs Custom Dashboard

This is another important decision.

I would not select the dashboard technology until the centralized data model and APIs are established.

All three approaches can consume the centralized recommendation store, but they serve different purposes.

## 8.1 Option A — Splunk Dashboard

[Cloud Security Monitoring (CSM) | Splunkbase](https://images.openai.com/static-rsc-4/VRVJm4M-MbzhkSr-0uObxxTd3G4_aY3J2sVt_P09p1MXg-WIZdTODilNviWiEepNI1e0JxU3R2TpdXJuxnIBhov1d2Ho9lnaq6W1fB8vrdG8o634HAu3lK4K5JnLJdWiYXVJwVdil5r67l7uSCjwWN7VAghrhLCuWyKRHUwiX1I?purpose=inline)

[splunkbase.splunk.com](https://splunkbase.splunk.com/app/5283?utm_source=chatgpt.com)

Splunk is a strong choice when the primary requirement is enterprise reporting, operational analytics and visibility.

Advantages

- Mature dashboarding and search capabilities.
- Powerful filtering and aggregation.
- Good for monitoring recommendation trends.
- Existing enterprise Splunk deployment may reduce adoption friction.
- Alerting and operational reporting.
- Integration with security and operational data.
- Can correlate cloud advisory findings with security events.

Disadvantages

- Not naturally designed as a transactional remediation workflow application.
- Complex multi-step approval experiences may require additional development.
- Managing recommendation lifecycle and resource-level transactions can become cumbersome.
- Licensing and ingestion costs need evaluation.
- May require a separate backend service for remediation operations.

Best fit: Enterprise operational dashboard, security reporting and recommendation trend analysis.

## 8.2 Option B — Microsoft Power Apps + Power BI

[Monitor with the CoE Power BI dashboard - Power Platform | Microsoft Learn](https://images.openai.com/static-rsc-4/dH8eXR9bvRAc-7pQ3aFXpRSEM278lBxqeXSwPxecZAS_R7LolaXOe7E4znXDlXmknWFzlaI_jVcQGG1J3bSv7c9__FCz_2w8e9B_RaL6qYuVac9JnEcXAuZuyF5QjBkSvsTLXJh7ioDB46JRxu_1DAf7N9wVQBUsvXx52J7yMog?purpose=inline)

[learn.microsoft.com](https://learn.microsoft.com/en-us/power-platform/guidance/coe/power-bi-monitor?utm_source=chatgpt.com)

This is a good option if the primary requirement is an internal enterprise workflow application.

I would distinguish between Power Apps and Power BI:

- Power BI: Analytics, reporting and visualization.
- Power Apps: User interactions, approvals, exception management and workflow applications.
- Power Automate: Workflow orchestration and notifications.

Advantages

- Faster development of internal applications.
- Native integration with Microsoft 365.
- Approval workflows.
- Forms and exception management.
- Role-based user experience.
- Power BI can provide executive-level reporting.
- Good for application owner engagement.

Disadvantages

- Large-scale data processing should not be implemented inside Power Apps.
- Power Apps should not directly query thousands of cloud scopes.
- Dataverse licensing and storage costs need consideration.
- Complex resource-level tables and high-volume data require careful architecture.
- More complex remediation execution needs backend APIs.
- Premium connectors and API limits may introduce additional costs.

Best fit: Governance application, approval management, exception management and enterprise reporting.

## 8.3 Option C — Custom Dashboard

[Cloud Management Platform| Cluster Reply](https://images.openai.com/static-rsc-4/GA13ueyDkFC9hV9QRBtOWW19pv0xglRyduq0C__8GSsIAeHByhyvj7PFL5smFZIKF8seaIkCeaW0zKwsmeqDPdYev98qFYeMFti50IUE77kXGj4LoaMY_HcAjaEzlKia--1tPeSdnxblZv88_tRk7BaYyyffswdzfAWknhoF_mM?purpose=inline)

[reply.com](https://www.reply.com/cluster-reply-italy/en/cloud-management-platform?utm_source=chatgpt.com)

A custom dashboard gives you the most control over the end-user experience and the underlying architecture.

Suggested technology stack:

| Layer          | Technology                                    |
| -------------- | --------------------------------------------- |
| Frontend       | React / Next.js                               |
| Backend APIs   | Python FastAPI / .NET                         |
| Database       | PostgreSQL / Azure SQL                        |
| Analytics      | Databricks SQL / cloud data warehouse         |
| Raw data       | S3 / ADLS                                     |
| Authentication | Entra ID / enterprise SSO                     |
| Workflow       | Temporal / Step Functions / Durable Functions |
| AI             | Enterprise LLM gateway and agent framework    |
| Observability  | Dynatrace / OpenTelemetry                     |

Advantages

- Full control over functionality.
- Native integration with remediation APIs.
- Better control over resource-level drill-down.
- Custom multi-cloud data visualization.
- Easier to integrate conversational AI.
- Better control over approval and remediation lifecycle.
- Ability to build a reusable enterprise platform.

Disadvantages

- Higher initial development effort.
- Requires ongoing product engineering.
- Need to build and maintain authentication, authorization and audit features.
- More responsibility for scalability, availability and operational support.
- Longer time to deliver the initial user experience.

Best fit: Long-term enterprise multi-cloud advisory and remediation platform.

## 8.4 Side-by-side comparison

| Evaluation dimension       | Splunk             | Power Apps + BI     | Custom                          |
| -------------------------- | ------------------ | ------------------- | ------------------------------- |
| Initial development        | Fast if deployed   | Fast                | Moderate/slow                   |
| Analytics                  | Excellent          | Excellent           | Excellent with suitable backend |
| Resource-level drill-down  | Good               | Good                | Excellent                       |
| Approval workflows         | Limited natively   | Excellent           | Excellent                       |
| Remediation integration    | API/backend needed | API/backend needed  | Native control                  |
| Agentic integration        | Possible           | Possible            | Excellent flexibility           |
| Customization              | Moderate           | Moderate            | Excellent                       |
| Multi-cloud extensibility  | Good               | Good                | Excellent                       |
| Operational overhead       | Moderate           | Low–moderate        | High                            |
| Licensing considerations   | Splunk licensing   | Microsoft licensing | Infrastructure and engineering  |
| Long-term platform control | Moderate           | Moderate            | High                            |

## 8.5 My recommendation

I would choose a hybrid approach rather than forcing all functionality into one product.

Custom dashboard

Recommended core platform

Primary enterprise interface for:

- Multi-cloud recommendations.
- Resource-level drill-down.
- Remediation lifecycle.
- Agentic chat.
- Remediation execution.

  Power BI

Executive-level analytics:

- Cost optimization opportunities.
- Security posture.
- Recommendation closure rate.
- Business-unit comparisons.

  Splunk

Operational and security monitoring:

- Collection failures.
- Remediation failures.
- High-risk recommendation alerts.
- Security event correlation.

  Power Apps

Optional application for:

- Risk acceptance.
- Exception approval.
- Application owner remediation decisions.

Why?

Because the requirements go beyond visualization. You need an application that can manage the complete lifecycle of a recommendation, from discovery through remediation and verification.

A custom application is better suited to become the central operational interface, while existing enterprise products can consume the same APIs and data.

# 9. What should the final dashboard actually display?

I would design the dashboard around four primary personas:

1. Senior leadership.
2. Cloud governance and platform teams.
3. Security and FinOps teams.
4. Application and resource owners.

## 9.1 Executive overview

Multi-Cloud Advisory Overview

Total recommendations

# 12,450

Affected resources

# 28,300

Open recommendations

# 8,200

Verified closures

# 4,250

Cloud distribution

AWS

60%

Azure

40%

Illustrative dashboard values, not actual collected data.

## 9.2 Category-based recommendations

| Category               | Open findings | Affected resources | Business priority |
| ---------------------- | ------------- | ------------------ | ----------------- |
| Cost optimization      | 3,200         | 8,500              | High              |
| Security               | 2,100         | 4,800              | Critical          |
| Reliability            | 1,500         | 3,500              | High              |
| Performance            | 900           | 2,000              | Medium            |
| Operational excellence | 500           | 1,200              | Medium            |

## 9.3 Resource-level recommendation drill-down

This is the most important functional requirement.

When someone clicks a category, they should be able to drill down:

Security → Encryption recommendations

AWS ACCOUNT

123456789012

S3 bucket encryption not configured

High priority

Affected resources

- `s3://application-bucket-01`
- `s3://application-bucket-02`
- `s3://application-bucket-03`

Resource metadata

- Environment: Production
- Application owner: Team A
- Business unit: Finance
- Region: us-east-1

Remediation

- Proposed action: Apply approved encryption configuration.
- Approval: Required.
- Enterprise status: Approval pending.
- Provider status: Warning.

The dashboard should also provide filters for:

- Cloud provider.
- Account or subscription.
- Management group or organization.
- Business unit.
- Application owner.
- Environment.
- Recommendation category.
- Severity.
- Recommendation age.
- Remediation status.
- Risk acceptance.
- Last collection timestamp.

## 9.4 Governance KPIs

I would specifically build the following KPIs:

| KPI                         | What it measures                                            |
| --------------------------- | ----------------------------------------------------------- |
| Advisory coverage           | Percentage of accounts/subscriptions successfully collected |
| Recommendation closure rate | Percentage of recommendations verified as closed            |
| Remediation SLA             | Time taken to remediate recommendations                     |
| Aging recommendations       | Recommendations open for 30/60/90+ days                     |
| Cost opportunity            | Estimated potential savings                                 |
| Realized savings            | Verified savings after remediation                          |
| High-risk findings          | Outstanding critical/high-risk findings                     |
| Exception rate              | Recommendations accepted as business risk                   |
| Automation rate             | Percentage remediated automatically                         |
| Collection success rate     | Successful collection jobs / total jobs                     |

One important point: distinguish estimated savings from realized savings. Do not report the potential savings of a recommendation as savings already achieved.

# 10. Technology architecture I would actually implement

Given the scale and the future requirement to support agentic capabilities, here is my preferred technology stack.

| Layer                | Recommended technology               |
| -------------------- | ------------------------------------ |
| AWS collection       | Python, Trusted Advisor SDK/API      |
| Azure collection     | Python/.NET, Advisor REST API        |
| Azure enrichment     | Azure Resource Graph                 |
| AWS enrichment       | AWS Config / resource APIs           |
| Orchestration        | Step Functions or Durable Functions  |
| Messaging            | SQS / Service Bus                    |
| Raw data lake        | S3 / ADLS Gen2                       |
| Transformation       | Databricks / Spark                   |
| Operational database | PostgreSQL or Azure SQL              |
| Analytical database  | Databricks SQL / data warehouse      |
| Backend              | FastAPI / .NET                       |
| Frontend             | React                                |
| Identity             | Enterprise SSO / Entra ID            |
| Remediation          | Terraform, AWS SSM, Azure Automation |
| Agentic layer        | Enterprise agent framework           |
| Monitoring           | Dynatrace / OpenTelemetry            |
| Reporting            | Custom dashboard + Power BI + Splunk |

### One important database decision

I would not store everything in a single relational database.

Use different storage patterns for different purposes:

| Data                       | Storage                                               |
| -------------------------- | ----------------------------------------------------- |
| Raw provider responses     | S3 / ADLS                                             |
| Normalized recommendations | PostgreSQL / Azure SQL or lakehouse tables            |
| Resource inventory         | Lakehouse / relational store                          |
| Remediation execution      | Relational transactional database                     |
| Audit history              | Immutable object storage plus queryable audit records |
| Analytics                  | Databricks SQL / warehouse                            |
| Agent knowledge            | Search index / vector store, where needed             |

For 2,000 scopes, PostgreSQL or Azure SQL can be sufficient for the operational recommendation store if properly indexed and partitioned. You do not need to introduce a distributed database simply because you have 2,000 accounts and subscriptions.

The larger consideration is the number of recommendation-resource records and their update frequency.

# 11. Implementation roadmap

I would divide this initiative into four phases.

1. Phase 1 — Discovery and data collection

   Weeks 1–4
   - Validate AWS Trusted Advisor API availability and support plans.
   - Validate Azure Advisor API permissions.
   - Build AWS and Azure scope discovery.
   - Implement collectors.
   - Establish raw storage.
   - Build collection monitoring.
   Deliverable: Raw recommendation inventory across AWS and Azure.
2. Phase 2 — Normalization and dashboard

   Weeks 5–9
   - Implement canonical data model.
   - Map provider categories.
   - Enrich resource metadata.
   - Build recommendation-resource relationships.
   - Implement backend APIs.
   - Build initial dashboard and executive reports.
   Deliverable: Unified multi-cloud advisory dashboard.
3. Phase 3 — Remediation and governance

   Weeks 10–15
   - Implement remediation catalog.
   - Build policy engine.
   - Integrate Terraform and native automation.
   - Implement approval workflows.
   - Implement provider status synchronization.
   - Build reconciliation and audit history.
   Deliverable: End-to-end recommendation remediation platform.
4. Phase 4 — Agentic intelligence

   Weeks 16–20
   - Build recommendation chatbot.
   - Introduce analysis agents.
   - Integrate remediation planning tools.
   - Add approval-based agent execution.
   - Implement agent observability and governance.
   Deliverable: Agentic multi-cloud advisory and remediation assistant.

These are indicative planning estimates assuming an experienced engineering team, access to both cloud environments, established identity infrastructure and a limited initial remediation catalog. Production rollout across all 2,000 scopes may require additional validation and hardening.

## 12. What I would validate in the initial POC

Before committing to the complete implementation, I would run a POC with:

- 10 AWS accounts.
- 10 Azure subscriptions.
- 5–7 recommendation categories.
- At least 100 recommendation instances.
- Resource-level associations.
- One low-risk remediation in each cloud.
- One approval-based remediation in each cloud.
- Provider status synchronization.
- Dashboard drill-down.

I would measure:

| Validation area          | Success criteria                                      |
| ------------------------ | ----------------------------------------------------- |
| Collection coverage      | All eligible scopes accounted for                     |
| Data completeness        | Recommendation and affected-resource details captured |
| Deduplication            | No duplicate recommendation instances                 |
| Normalization            | Correct provider-to-enterprise category mapping       |
| Incremental collection   | Only changed data needs processing where supported    |
| Remediation              | Approved operation executes successfully              |
| Verification             | Actual resource state is checked                      |
| Provider synchronization | Native state is updated where supported               |
| Auditability             | Every action has an attributable audit record         |

I would specifically test the difference between AWS standard recommendations and Priority recommendations. I would also test Azure recommendation state management against the API versions approved for production.

# 13. Key architectural risks and decisions

These are the questions I would take to the cloud platform, security and FinOps teams before implementation.

| Area               | Question / decision                                                                                      |
| ------------------ | -------------------------------------------------------------------------------------------------------- |
| AWS support        | Do all 1,000 accounts have eligible Trusted Advisor support coverage?                                    |
| AWS centralization | Can organizational views cover the required recommendation types, or is per-account collection required? |
| Azure access       | Can a centralized identity access all subscriptions through delegated RBAC?                              |
| Data freshness     | What is the actual refresh frequency of each recommendation source?                                      |
| Resource ownership | Do resources have consistent application and business-unit tags?                                         |
| Data quality       | How will we handle recommendations with missing resource metadata?                                       |
| Remediation        | Which recommendations are safe for automatic remediation?                                                |
| Provider updates   | Which native recommendation states can actually be updated through supported APIs?                       |
| Governance         | Who approves production remediation?                                                                     |
| Cost               | What are the ingestion, processing, storage and dashboard licensing costs?                               |
| Security           | How do we enforce tenant and account-level authorization?                                                |
| Scalability        | How do we handle throttling and partial collection failures?                                             |

A particularly important design decision is whether the 1,000 AWS accounts belong to one AWS Organization or multiple organizations. The same consideration applies to Azure tenants and management groups. This directly affects collection identity, delegation and governance architecture.

# 14. My final architectural recommendation

If I were presenting this to senior leadership, I would position it as an Enterprise Multi-Cloud Advisory and Remediation Platform, rather than an AWS/Azure reporting solution.

Here is how I would prioritize the decisions:

| Architecture decision  | My recommendation                                                    |
| ---------------------- | -------------------------------------------------------------------- |
| AWS data collection    | Trusted Advisor APIs + Organizations                                 |
| Azure data collection  | Advisor API + Azure Resource Graph                                   |
| Collection model       | Distributed, queue-based collectors                                  |
| Raw data               | Preserve original JSON payloads                                      |
| Common data model      | Canonical recommendation schema                                      |
| Provider-specific data | Separate extension fields                                            |
| Resource relationships | Recommendation-to-resource many-to-many model                        |
| Database               | Relational operational store + lakehouse                             |
| Remediation            | Dedicated orchestration and policy engine                            |
| Provider status        | Provider-specific synchronization adapters                           |
| GCP expansion          | Provider adapter architecture                                        |
| Agentic capability     | Start with analysis, progress to controlled remediation              |
| Dashboard              | Custom dashboard as core, Power BI and Splunk as complementary tools |

## 15. Five architectural decisions I would strongly defend

1\. Do not build separate AWS and Azure reporting applications.

Build one enterprise recommendation platform with provider-specific adapters.

2\. Do not discard raw recommendation payloads.

Retain raw data for audit, troubleshooting, schema evolution and future processing.

3\. Do not confuse recommendation status with remediation status.

Your enterprise lifecycle must be independent of the provider's lifecycle.

4\. Do not give an AI agent unrestricted cloud access.

Use a governed tool layer with identity, policy evaluation, approvals and auditability.

5\. Do not make the dashboard the core of the platform.

Build the data model, APIs and remediation orchestration first. The dashboard should be just one consumer of the platform.

## 16. Useful official technical references

These are the primary API documents I would use when creating the low-level design.

| Technology                                       | Documentation                                                                                                                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AWS Trusted Advisor API                          | [Trusted Advisor API Reference](https://docs.aws.amazon.com/trustedadvisor/latest/APIReference/?utm_source=chatgpt.com)                                                                    |
| AWS Trusted Advisor API access and prerequisites | [Getting started with Trusted Advisor API](https://docs.aws.amazon.com/awssupport/latest/user/get-started-with-aws-trusted-advisor-api.html?utm_source=chatgpt.com)                        |
| AWS Organizational View                          | [Organizational View](https://docs.aws.amazon.com/awssupport/latest/user/organizational-view.html?utm_source=chatgpt.com)                                                                  |
| AWS Recommendation lifecycle                     | [UpdateRecommendationLifecycle](https://docs.aws.amazon.com/trustedadvisor/latest/APIReference/API_UpdateRecommendationLifecycle.html?utm_source=chatgpt.com)                              |
| Azure Advisor recommendations                    | [Recommendations List API](https://learn.microsoft.com/en-us/rest/api/advisor/recommendations/list?view=rest-advisor-2025-01-01\&utm_source=chatgpt.com)                                   |
| Azure Resource Graph API                         | [Resource Graph REST API](https://learn.microsoft.com/rest/api/azureresourcegraph/resourcegraph/resources/resources?utm_source=chatgpt.com)                                                |
| Azure Resource Graph pagination                  | [Pagination guidance](https://learn.microsoft.com/en-us/azure/governance/resource-graph/concepts/paging-results?utm_source=chatgpt.com)                                                    |
| Azure Advisor status management                  | [Recommendation state management](https://learn.microsoft.com/en-us/azure/advisor/advisor-azure-state-management?trk=article-ssr-frontend-pulse_little-text-block\&utm_source=chatgpt.com) |
| Azure Advisor recommendation update              | [Recommendations Update API](https://learn.microsoft.com/en-us/rest/api/advisor/recommendations/update?view=rest-advisor-2026-03-01-preview\&utm_source=chatgpt.com)                       |

My strongest recommendation: Build the centralized collection, canonical data model, resource relationship and remediation orchestration first. Once those four capabilities are established, the dashboard, GCP expansion and agentic use cases become significantly easier to implement.

The next logical design artifact would be a detailed low-level architecture covering the actual AWS and Azure collectors, API contracts, database DDL, queue design, IAM/RBAC, normalization code and remediation workflow, including how to deploy it across all 2,000 scopes.
