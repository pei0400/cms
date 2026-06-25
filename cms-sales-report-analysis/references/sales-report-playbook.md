# Crimson Muse Studio Sales Report Playbook

## Gmail Collection

Use Gmail as the first source when the user asks to analyze Crimson Muse Studio sales performance and does not provide a report file directly.

Default source rule:

1. Check whether the connected Gmail profile is `crimsonmusestudio1@gmail.com` when profile data is available.
2. Search for the latest email with exact subject `Powershopz Sales Report` and an attachment using `to:crimsonmusestudio1@gmail.com subject:"Powershopz Sales Report" has:attachment`.
3. Select the newest matching message by timestamp.
4. Read the message and retrieve the attachment that contains the sales report.
5. If there are multiple attachments, prefer the latest spreadsheet or CSV sales export over a PDF summary; document the filename used.
6. If no matching email or accessible attachment is found, state the exact query and coverage, then ask for the missing report or permission/account correction.

Search in passes:

1. Exact report query: `to:crimsonmusestudio1@gmail.com subject:"Powershopz Sales Report" has:attachment`.
2. Broader Powershopz queries: `subject:"Powershopz Sales Report" has:attachment`, `Powershopz has:attachment`.
3. Brand/company queries: `"Crimson Muse Studio"`, `"Crimson Muse"`, and `CMS` combined with sales terms.
4. Sales terms: sales, revenue, orders, transactions, invoice, receipt, payout, statement, report, summary, export, shop, marketplace, payment, Stripe, Square, Shopify, Etsy, PayPal, WooCommerce, POS.
5. Attachment filters: `has:attachment`, `filename:csv`, `filename:xlsx`, `filename:xls`, `filename:pdf`.
6. Date filters: use the user's requested report period; otherwise start with the latest matching email and say the scope used.

Read the most relevant email bodies and threads, then retrieve attachments when available. If attachment contents cannot be accessed, summarize the available metadata and ask for the file or permission path needed to inspect it.

Do not change mailbox state. Avoid archive, delete, label, forward, or send actions unless the user explicitly asks.

Record provenance in the final report: search query coverage, email dates, sender/source names, attachment names, and any gaps.

## Metric Definitions

Use the report's definitions when provided. If definitions are absent, state assumptions explicitly.

- Gross sales: sales before discounts, refunds, taxes, shipping, and fees.
- Net sales: gross sales minus discounts, returns, refunds, and allowances. Exclude taxes and shipping unless the report defines them as revenue.
- Orders: unique completed orders or invoices. Avoid counting line items as orders.
- Units sold: quantity sold, net of returns when return data exists.
- Average order value: net sales divided by orders.
- Discount rate: discounts divided by gross sales.
- Refund rate: refunds divided by gross sales or orders, matching the report's grain.
- Gross margin: net sales minus cost of goods sold. Gross margin percentage is gross margin divided by net sales.
- Attach rate: add-on units, services, or products per order when those fields exist.

## Common Column Synonyms

- Date: order date, transaction date, paid at, invoice date, created at.
- Revenue: sales, gross sales, net sales, subtotal, amount, total, item total.
- Product: SKU, item, title, collection, service, package, class, commission type.
- Channel: source, sales channel, marketplace, store, POS, online, wholesale, event.
- Customer: customer name, email, account, company, buyer, client.
- Quantity: qty, units, count, item quantity.
- Discount: coupon, promo, markdown, discount amount.
- Refund: return, refunded amount, credit, adjustment.
- Cost: COGS, unit cost, production cost, material cost.

## Integrity Checks

Before analysis, inspect:

- Whether Gmail search may have missed reports because of alternate names, senders, labels, or forwarded attachments.
- Whether totals include subtotal rows, tax, shipping, tips, platform fees, or gift-card redemptions.
- Whether report dates are complete for the stated period.
- Whether order IDs repeat because the data is line-item level.
- Whether refunds are separate rows, negative rows, or columns on the original order.
- Whether currencies or time zones are mixed.
- Whether blank or "unknown" channels/categories hide meaningful volume.
- Whether unusually large orders, bulk buyers, event sales, or one-off commissions distort the average.

## Core Analyses

Top line:

- Calculate sales, orders, units, AOV, discounts, refunds, and margin if available.
- Show absolute change and percentage change against the best available baseline.
- Call out whether growth came from more orders, higher AOV, more units, better mix, fewer refunds, or lower discounting.

Product and service mix:

- Rank products/services by net sales, units, margin, and growth.
- Identify new winners, declining staples, high-volume low-margin items, and low-volume high-margin opportunities.
- Watch for concentration risk if the top product, service, or collection contributes a large share of revenue.

Channel performance:

- Compare online, in-person, wholesale, marketplace, event, email, social, and other channels when present.
- Evaluate each channel by sales, orders, AOV, refund rate, discount rate, and margin.
- Distinguish a traffic/order problem from a pricing or mix problem when enough fields exist.

Customer behavior:

- Separate new and returning customers when available.
- Identify repeat-purchase rate, revenue from top customers, customer concentration, and unusually large orders.
- Flag retention opportunities such as customers who bought previously but not in the current period, if history is available.

Seasonality and timing:

- Break down by week, month, day of week, or campaign/event windows when useful.
- Avoid overinterpreting partial periods. Normalize daily run rate when comparing incomplete periods.

Potential issues:

- Revenue decline, slower order volume, reduced AOV, lower unit volume, or worsening conversion proxy metrics.
- Margin pressure from discounts, rising refunds, fees, shipping, production cost, or low-margin product mix.
- Overdependence on one product, customer, channel, event, platform, or campaign.
- Stockouts, fulfillment delays, unusually high cancellations, or repeated refund reasons when email/report text exposes them.
- Reporting gaps: missing cost data, inconsistent product names, duplicated order rows, incomplete date ranges, or ambiguous gross vs net definitions.

Trend handling:

- Use absolute and percentage deltas together.
- Prefer period-over-period and year-over-year comparisons when both exist.
- For incomplete periods, compare daily run rate instead of raw totals.
- Treat causes as hypotheses unless supported by explicit fields, report notes, or email context.

## Recommended Readout

Use concise, decision-ready language:

1. State the headline result in one sentence.
2. List the 3-5 biggest quantified takeaways.
3. Explain the likely drivers, using "observed" for facts and "likely" for supported hypotheses.
4. Flag data quality issues that could change the conclusion.
5. Call out potential issues and emerging trends.
6. Recommend specific next actions, each tied to an observed metric or segment.

## Useful Follow-Up Questions

Ask only questions that materially affect the analysis:

- Is the report gross or net of refunds, discounts, tax, and shipping?
- Is this data order-level, line-item-level, or summarized?
- What comparison period or target should be used?
- Are costs, fees, or production expenses available for margin analysis?
- Are channels, campaigns, customer status, or product categories reliable in this export?
- Are there alternate names, email senders, platforms, or labels that contain Crimson Muse Studio sales data?
