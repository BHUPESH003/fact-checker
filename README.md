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

| ID | Claim | Claimed origin | Verdict | Evidence | Trace |
|----|-------|----------------|---------|----------|-------|
| C-01 | Amazon Bedrock AgentCore is generally available | AWS What's New | TRUE | [AWS ML blog](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-is-now-generally-available/) | [trace](https://smith.langchain.com/public/ae621065-3bc0-4b17-ac96-9c069c019435/r) |
| C-02 | AWS will launch a managed quantum computing Region in us-east-1 at re:Invent 2025 | Hacker News | FALSE | [AWS Quantum blog](https://aws.amazon.com/blogs/quantum-computing/aws-reinvent-2025-your-complete-guide-to-quantum-computing-sessions/) | [trace](https://smith.langchain.com/public/c5d62436-f41e-469a-8c9f-2238f7c480d0/r) |
| C-03 | EC2 P6e-GB200 UltraServers are available in all commercial AWS Regions | third-party newsletter | FALSE | [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/07/amazon-p6e-gb200-ultraservers-gpu-performance-ec2/) | [trace](https://smith.langchain.com/public/17c34962-a1d6-4319-9868-d68776069e5d/r) |
| C-04 | Amazon Aurora DSQL is generally available | AWS News Blog | TRUE | [AWS News Blog](https://aws.amazon.com/blogs/aws/amazon-aurora-dsql-is-now-generally-available/) | [trace](https://smith.langchain.com/public/25e54da1-527f-477d-9141-6b9c0d418256/r) |
| C-05 | Amazon S3 Vectors is GA | r/aws thread | TRUE | [AWS News Blog](https://aws.amazon.com/blogs/aws/amazon-s3-vectors-now-generally-available-with-increased-scale-and-performance/) | [trace](https://smith.langchain.com/public/2159ab9a-ea40-4926-ab4f-7018ff81f9e5/r) |

Notes on the verdicts:
- **C-02** is FALSE only because the official quantum blog doesn't mention such a Region. That is absence of evidence, not a denial. Treat it as "unsupported, from a weak source".
- **C-03** rests on a July 2025 announcement that says availability is limited. The page may be outdated relative to the claim's October 2025 date, so confirm against current AWS Region availability before relying on it.
- The three TRUE results all link to official AWS pages. The two non-TRUE claims came from third-party sources (Hacker News, a newsletter).
# fact-checker
