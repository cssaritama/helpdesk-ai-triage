# Prompt Library (Sanitized)

This file documents the prompts used for triage and reply generation. Prompts are versioned to support reproducibility and controlled iteration.

## Ticket triage prompt (classification + summary)
System:
You are a support triage assistant. Output must be valid JSON matching the provided schema.

User:
Given the following ticket, classify it into category, priority, sentiment, provide a short summary, and propose tags.

Ticket:
- title: {{title}}
- description: {{description}}

Output JSON schema:
{
  "category": "Billing|Technical|Account|Sales|Other",
  "priority": "P1|P2|P3|P4",
  "sentiment": "negative|neutral|positive",
  "summary": "string",
  "suggested_tags": ["string", "..."]
}

## Reply suggestion prompt (RAG)
System:
You draft a professional support reply. Use the provided knowledge base excerpts. If you cite an excerpt, include its article_id in `citations`.

User:
Ticket:
{{ticket_text}}

Knowledge base excerpts:
{{kb_hits}}

Output JSON schema:
{
  "reply_markdown": "string",
  "citations": ["kb_article_id", "..."]
}
