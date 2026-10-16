# fact-checker

Checks claims in a CSV against authoritative sources. It uses OpenRouter (model + web search) and traces each check in LangSmith.

## Run

```
# .env: OPEN_ROUTER_KEY, LANGSMITH_TRACING=true, LANGSMITH_API_KEY, LANGSMITH_PROJECT, optional MODEL
.venv/bin/python check.py
```

Input: the CSV in `data/`. Output: `results.csv` (the input columns plus `verdict`, `evidence_url`, `reasoning`).

## Facts checked

Source: `re:Invent Candidate Items (collected 27 Oct – 2 Nov 2025).csv`

| ID | Claim | Claimed origin | Verdict | Evidence |
|----|-------|----------------|---------|----------|
| C-01 | Amazon Bedrock AgentCore is generally available | AWS What's New | TRUE | [AWS ML blog](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-is-now-generally-available/) |
| C-02 | AWS will launch a managed quantum computing Region in us-east-1 at re:Invent 2025 | Hacker News | FALSE | [AWS Quantum blog](https://aws.amazon.com/blogs/quantum-computing/aws-reinvent-2025-your-complete-guide-to-quantum-computing-sessions/) |
| C-03 | EC2 P6e-GB200 UltraServers are available in all commercial AWS Regions | third-party newsletter | FALSE | [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/07/amazon-p6e-gb200-ultraservers-gpu-performance-ec2/) |
| C-04 | Amazon Aurora DSQL is generally available | AWS News Blog | TRUE | [AWS News Blog](https://aws.amazon.com/blogs/aws/amazon-aurora-dsql-is-now-generally-available/) |
| C-05 | Amazon S3 Vectors is GA | r/aws thread | TRUE | [AWS News Blog](https://aws.amazon.com/blogs/aws/amazon-s3-vectors-now-generally-available-with-increased-scale-and-performance/) |

Notes on the verdicts:
- **C-02** is FALSE only because the official quantum blog doesn't mention such a Region. That is absence of evidence, not a denial. Treat it as "unsupported, from a weak source".
- **C-03** rests on a July 2025 announcement that says availability is limited. The page may be outdated relative to the claim's October 2025 date, so confirm against current AWS Region availability before relying on it.
- The three TRUE results all link to official AWS pages. The two non-TRUE claims came from third-party sources (Hacker News, a newsletter).
# fact-checker
