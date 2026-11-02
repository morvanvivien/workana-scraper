# How to Scrape Workana: LatAm Freelance Projects (Budget, Skills, Client Country)

> **Run it now, no code: [workana-projects-scraper on the Apify Store](https://apify.com/bibian/workana-projects-scraper)** &nbsp;|&nbsp; $2.00 per 1,000 projects &nbsp;|&nbsp; no browser, no proxy

Workana is Latin America's largest freelance marketplace, with open projects posted by clients across Argentina, Brazil, Mexico, Chile, Colombia, Peru and more. It has no public export and no official API for third parties. This guide shows how to get those projects as clean structured data: budget, skills, category and client country, with a paid Apify Actor, from the console or from code.

Searches this page answers: workana scraper, latam freelance projects, workana api, freelance marketplace scraper.

## What you get from the Workana scraper

- Every open project on Workana, newest first, with title, category, subcategory, skills and client country.
- Budget parsed from Workana's own text into `salaryMin`, `salaryMax`, `salaryCurrency` and `salaryPeriod` (always USD on Workana; `salaryPeriod` is `"hour"` for hourly projects, `null` for a fixed budget).
- Workana-specific signals: hourly vs. fixed (`isHourly`), the site's own "urgent" flag, number of bids so far, and whether the client has a verified payment method.
- Optional full project description as plain text, with any e-mail address or phone number removed.
- The same unified field names (`datePosted`, `salaryMin`, `employmentType`, `skills`...) shared by every job and freelance-mission Actor from this author, so Workana drops straight into a pipeline already built for one of the others.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results, no personal data, long descriptions truncated) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `id`, `url`, `title` | `workana:<slug>`, the public `/job/<slug>` page, and the full project title |
| `companyName`, `companyUrl`, `confidentialCompany` | Almost every client on Workana is an individual shown only as a first name and initial, which is personal data: `companyName` is `null` and `confidentialCompany` is `true` for those. When the client is an actual company (`isCompany` on the site), its name is kept here. |
| `locationLabel`, `city`, `region`, `postalCode`, `country` | The client's country, as published by Workana (for example `"Argentina"` / `AR`). Workana's list does not publish a city or region, so those stay `null`. |
| `remote` | Always `"unknown"`: Workana does not publish whether a project is remote, hybrid or on-site. |
| `employmentType` | Always `"freelance"`. |
| `salaryMin`, `salaryMax`, `salaryCurrency`, `salaryPeriod` | Parsed from Workana's own budget text (always in USD), for example `"USD 250 - 500"` or `"Less than USD 15 / hour"`. |
| `datePosted` | Computed from Workana's relative label ("2 hours ago", "Yesterday"): approximate, to the hour or the day. |
| `validThrough`, `experienceLevel` | Always `null`: not published by Workana's project list. |
| `industry`, `subcategory` | Workana's own "Category" and "Subcategory" labels (for example `"IT & Programming"` / `"Web development"`). |
| `skills` | Skills listed by the client, as Workana's own tags. |
| `source`, `sourceId`, `scrapedAt` | `"workana.com"`, the project's slug, and when this run read it. |
| `isHourly`, `isUrgent`, `bidsCount`, `clientHasVerifiedPayment`, `budgetLabel` | Hourly vs. fixed budget, the site's "urgent" flag, number of freelancer bids so far, whether the client has a verified payment method, and the original budget text. |
| `description` | Full project description as plain text (only when **Include full descriptions** is on). Any e-mail address or phone number is removed before saving. |

## Use cases

- **Track freelance daily rates and project budgets across LatAm.** Group `salaryMin`/`salaryMax` by skill, country or category.
- **Build a daily job alert.** Schedule a run every morning with `publishedWithinDays: 1` and send only the new projects to Slack, e-mail or a Google Sheet.
- **Feed a lead list.** A client posting a project for a skill you sell is a lead; filter by category and country.
- **Study the LatAm freelance market.** Budgets, in-demand skills and project volume by country over time.

## Input

| Field | What it does |
|---|---|
| `keywords` | Job title or skill, using Workana's own search, for example `wordpress`. Empty means every open project. |
| `country` | Optional 2-letter ISO code of the client who posted the project (`AR`, `BR`, `MX`, `CL`, `CO`, `PE`...). Empty means every country. |
| `category` | Optional, Workana's own category slug (for example `it-programming`), copied from a filtered `workana.com/jobs` URL. |
| `publishedWithinDays` | Keep only projects published in the last N days. Use `1` for a daily monitoring run. |
| `maxItems` | The run stops once this many projects are saved (default 50). |
| `onlyNew` | For scheduled runs: skip the projects an earlier run of this same search already delivered. |
| `includeDescriptions` | Adds the full project description as plain text, with any e-mail address or phone number removed. |

Example input:

```json
{
  "keywords": "wordpress",
  "publishedWithinDays": 7,
  "maxItems": 50,
  "onlyNew": false,
  "includeDescriptions": false
}
```

## Four ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/workana-projects-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (keywords, filters and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/workana-projects-scraper').call({
    "keywords": "wordpress",
    "publishedWithinDays": 7,
    "maxItems": 50,
    "onlyNew": false,
    "includeDescriptions": false
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.title} | ${item.locationLabel ?? '-'} | ${item.budgetLabel ?? '-'} | ${item.industry ?? '-'}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/workana-projects-scraper").call(run_input={
    "keywords": "wordpress",
    "publishedWithinDays": 7,
    "maxItems": 50,
    "onlyNew": False,
    "includeDescriptions": False,
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{item['title']} | {item.get('locationLabel')} | {item.get('budgetLabel')} | {item.get('industry')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

### 4. Schedule it and connect your tools

1. **Schedule it.** Save a task with your keywords and schedule it daily with Apify Schedules. Tick **Only new results** (`onlyNew: true`) and each run returns, and charges, only the projects earlier runs of the same search did not deliver.
2. **Push the results where you work.** Add an Apify integration or a webhook to the task: Google Sheets, Slack, Make, Zapier, n8n or your own endpoint, triggered at the end of every run.
3. **Let an AI agent use it.** Through the [Apify MCP server](https://docs.apify.com/platform/integrations/mcp), assistants such as Claude or ChatGPT can search the Store, read this page and run the Actor as a tool.

## Pricing

Pay per result: **$2.00 per 1,000 projects** (that is $0.002 per project), plus a small start fee. For example, a 50-project test run costs about $0.11. You pay only for the results saved to the dataset. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/workana-projects-scraper) when this guide was written; the Store page is the reference.

## Limits and honest notes

- No login, proxy or browser needed for a default run: the Actor reads Workana's own public project feed directly.
- Workana only exposes its most recent pages through this feed: a very large **Maximum number of projects** (or a narrow filter) can return fewer results than requested once the site's own window is exhausted. That is the normal end of the list, not an error.
- `datePosted` is approximate, computed from Workana's relative label, not an exact timestamp: the site does not publish one.
- No personal data is collected. On Workana almost every client is an individual, not a company: their name is never saved, `companyName` stays `null` and `confidentialCompany` is `true` (this is visible in `sample-output.json`, where all five sample records have `companyName: null`). A freelancer's own profile (name, photo, rating, portfolio, bids) is never part of this feed; only the client's project is.
- Any e-mail address or phone number a client typed into the description is removed before saving.
- This is an unofficial tool, not affiliated with Workana. Check the site terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy?**
No. The Actor reads Workana's own JSON feed directly, so runs are fast and cheap.

**How do I only get new projects every day?**
Set `publishedWithinDays` to `1` and `onlyNew` to `true`, then schedule the Actor once a day.

**Why is `companyName` almost always empty?**
Because almost every client on Workana is an individual, not a company, and an individual's name is personal data. `companyName` is kept only for the clients Workana itself marks as a company.

**Why is `remote` always `"unknown"`?**
Workana's project feed does not publish a remote/hybrid/on-site flag, so the Actor never guesses one.

**Can I get the data in Excel or Google Sheets?**
Yes. Export the dataset as CSV, Excel, JSON, XML, HTML table or RSS from the Apify console, or connect the Apify Google Sheets integration.

**Is it legal to scrape?**
The Actor collects publicly visible projects and respects the robots.txt rules of the site. How you use the data is your responsibility: check the site's terms and the laws that apply to you, for example the GDPR.

**Something does not work?**
Open an issue in the Issues tab of the Actor's Apify Store page, or on this repository. Every public Actor is test-run daily and the broken ones are repaired.

## Try it

**[Open workana-projects-scraper on the Apify Store](https://apify.com/bibian/workana-projects-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
