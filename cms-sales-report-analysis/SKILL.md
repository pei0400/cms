---
name: cms-sales-report-analysis
description: Analyze Crimson Muse Studio sales performance by checking the user's Gmail account crimsonmusestudio1@gmail.com for the latest email with subject "Powershopz Sales Report", using its latest attachment as the sales report source, then creating a performance report with trends, issues, risks, and recommendations. Use when the user asks Codex to get Crimson Muse Studio or CMS sales information from Gmail; review, summarize, audit, compare, forecast, or extract insights from Powershopz Sales Report emails, sales attachments, CSV, XLSX, PDF, doc, dashboard, monthly sales, product/category, channel, customer/order, revenue, or performance summaries.
---

# CMS Sales Report Analysis

## Overview

Use this skill to find the latest Crimson Muse Studio sales report in Gmail and turn it into a clear business performance report: what changed, why it likely changed, what is driving revenue, what looks risky, what trends are emerging, and what actions are worth taking next.

## Default Data Source

Unless the user provides a different source or date range, use Gmail as follows:

1. Confirm the connected Gmail account is `crimsonmusestudio1@gmail.com` when profile data is available. If the connected account differs, say so and ask the user to connect or select the correct account before analyzing.
2. Search Gmail for the latest message with exact subject `Powershopz Sales Report` and an attachment. Use a query like `to:crimsonmusestudio1@gmail.com subject:"Powershopz Sales Report" has:attachment`, then broaden only if no result is found.
3. Choose the newest matching email by Gmail timestamp, not by the order results happen to appear.
4. Read that email and inspect its attachments.
5. Use the newest or primary sales-report attachment from that latest email as the source of truth. If multiple attachments look like sales reports, prefer spreadsheet or CSV files over PDFs, and mention which file was used.
6. If the latest matching email has no accessible attachment, report the message date, sender, subject, visible attachment metadata, and what is needed to continue.

## Workflow

1. Use the Gmail connector to search for the default Powershopz sales report email unless the user gives another source. Start with the exact subject query, then refine by date range, sender, attachment type, and terms found in promising messages.
2. Read relevant messages and threads. For attachments or linked exports, inspect the available metadata and retrieve the report files when the connector exposes them.
3. State the Gmail search scope used, including queries, date range, and coverage limits. Do not modify, archive, label, delete, forward, or send email unless the user explicitly asks.
4. Identify the report type, period, currency, source system, and available fields.
5. Preserve the user's definitions when provided. Do not silently redefine revenue, net sales, gross sales, orders, refunds, discounts, taxes, shipping, or margin.
6. For files, use structured readers for the file type. For spreadsheets, prefer the Spreadsheets skill and inspect workbook sheets, formulas, pivots, hidden rows, and column meanings before analyzing.
7. Check report integrity before drawing conclusions: duplicated orders, missing dates, negative values, mixed currencies, partial periods, blank categories, subtotal rows mixed into data, and mismatched totals.
8. Analyze the report at the highest useful level first, then drill into product/service, channel, customer, geography, campaign, and time-period segments when those fields exist.
9. Compare against the most relevant baseline available: prior period, same period last year, report target, forecast, or user-provided benchmark.
10. Separate observed facts from interpretation. Mark any inferred causes as hypotheses.
11. End with concrete recommendations, follow-up questions, and any data needed to improve confidence.

## Gmail Search Strategy

Load `references/sales-report-playbook.md` when collecting or analyzing actual sales information.

Start with the default exact query:

- `to:crimsonmusestudio1@gmail.com subject:"Powershopz Sales Report" has:attachment`

If that returns no usable report, broaden carefully and state the fallback used. Useful fallback query patterns include:

- `subject:"Powershopz Sales Report" has:attachment`
- `("Powershopz Sales Report" OR Powershopz) has:attachment`
- `"Crimson Muse Studio" sales`
- `"Crimson Muse Studio" revenue`
- `"Crimson Muse Studio" report`
- `"Crimson Muse Studio" invoice`
- `"Crimson Muse Studio" orders`
- `"Crimson Muse Studio" has:attachment`
- `("Crimson Muse" OR "CMS") (sales OR revenue OR orders OR report) has:attachment`

Prefer Gmail search filters when the user gives a period, such as `after:YYYY/MM/DD before:YYYY/MM/DD`, `newer_than:90d`, `filename:csv`, `filename:xlsx`, or `filename:pdf`.

If search results are noisy, prioritize messages with sales exports, monthly/weekly reports, platform summaries, payment processor statements, order summaries, invoices, receipts, marketplace reports, or attachments named with sales, revenue, orders, transactions, payout, statement, or report.

## Analysis Priorities

Always cover:

- Top-line performance: gross sales, net sales, order count, units sold, average order value, discounts, refunds, and margin when available.
- Trend: period-over-period and year-over-year change when comparison data exists.
- Mix: which products, services, collections, channels, customer types, or campaigns are driving gains or losses.
- Concentration: dependence on a small number of products, customers, orders, or channels.
- Potential issues: declining revenue, falling order count, weaker average order value, high discounts, refunds, channel dependence, product concentration, missing data, suspicious outliers, margin pressure, seasonality risk, or operational bottlenecks.
- Data caveats: Gmail search limitations, report limitations, missing fields, ambiguous definitions, or anomalies that could change the interpretation.
- Actions: pricing, merchandising, promotion, inventory, outreach, bundling, retention, or reporting changes suggested by the data.

## Output Style

Write for a studio owner/operator: direct, concise, and practical. Prefer short sections with numbers, deltas, and plain-language implications.

Use this default structure unless the user asks otherwise:

1. Executive takeaways
2. Key metrics
3. Trends
4. What drove the result
5. Potential issues and risks
6. Recommended next actions
7. Data sources, Gmail search scope, and open questions

When confidence is low, say why and specify exactly what field, file, or comparison period would make the answer stronger.
