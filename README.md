# Campaign Report Summariser

A small tool that turns a spreadsheet of Google Ads-style campaign results into a short, plain-language summary. It shows which campaigns are working and which ones need a closer look.

## Who it's for

Anyone who reviews ad campaign performance and wants a quick overview without building formulas in a spreadsheet: marketing managers, account leads, or anyone preparing a weekly update.
All data in campaigns.csv is made up for this example. No real client data is used.

## What it does

1. Reads campaign data from `campaigns.csv`.
2. Calculates four numbers for each campaign:
   - **CTR (click-through rate)**: what % of people who saw the ad clicked it.
   - **CPC (cost per click)**: how much each click cost.
   - **Conversion rate**: what % of clicks led to a conversion (for example a sale or sign-up).
   - **Cost per conversion**: how much each conversion cost.
3. Flags campaigns that **need attention**.
4. Writes the summary to `summary.txt` and also shows it on screen.

## How to run it

You need Python 3, which is already installed on most Macs. Nothing else needs installing.

1. Open the Terminal and go to this project folder.
2. Run:

   ```bash
   python3 summarise.py
   ```

3. Open `summary.txt` to read the report.

To use your own data, replace the rows in `campaigns.csv`. Keep the same column headings:

```
campaign_name,impressions,clicks,cost_eur,conversions
```

## Example output

```
Overview
--------
We looked at 9 campaigns. Together they spent €7,982.50, got 10,740 clicks and 405 conversions.
On average, each conversion cost €19.71.

Campaign by campaign
--------------------
Brand Search
  CTR 9.17% | CPC €0.41 | Conversion rate 8.64% | Cost per conversion €4.74
Display Remarketing  <-- needs attention
  CTR 0.60% | CPC €0.40 | Conversion rate 0.00% | Cost per conversion: n/a (no conversions)
YouTube Awareness  <-- needs attention
  CTR 0.30% | CPC €1.33 | Conversion rate 0.67% | Cost per conversion €200.00
Paused Test Campaign
  CTR n/a | CPC n/a | Conversion rate n/a | Cost per conversion: n/a (no conversions)
...

What needs attention
--------------------
5 of 9 campaigns need attention:
- YouTube Awareness: €200.00 per conversion (10.1x the average).
- Competitor Keywords: €81.00 per conversion (4.1x the average).
...
- Display Remarketing: spent €360.00 with no conversions.

Best performer: Brand Search, at only €4.74 per conversion.
```

## How the average is calculated

The average cost per conversion is **total cost ÷ total conversions** across all campaigns. This is a *weighted* average.

We don't simply average each campaign's figure, because one small, expensive campaign would distort the result. In the sample data, YouTube Awareness costs €200 per conversion but only had 4 conversions. A simple average of all campaigns would be pulled up to around €49. That would make genuinely expensive campaigns, like Generic Search at €30, look fine. The weighted average reflects what the account as a whole is really paying, and matches how ad platforms report it.

A campaign **needs attention** if:
- its cost per conversion is **above the average**, or
- it **spent money but got no conversions**.

## How edge cases are handled

- **No conversions:** Cost per conversion shows as **"n/a (no conversions)"** instead of €0.00, which would wrongly look like the cheapest result. If the campaign spent money, it's flagged as needing attention.
- **Paused campaigns with no spend:** A campaign with 0 impressions, 0 clicks and €0 cost is **not flagged**, because nothing was wasted. Its CTR, CPC and conversion rate show as **"n/a"**, since there's nothing to calculate.
- **No clicks or impressions:** Any number that would mean dividing by zero shows as **"n/a"** rather than a misleading 0. The script never crashes on these.

## What I learned

I built this as a beginner Python project with Claude Code, using only Python's built-in tools.

- **Ask for a plan and explanations, and check the settings.** I asked Claude Code to explain its plan before creating files, but in Auto mode it created and ran them straight away. I reviewed everything afterwards, and next time I would switch to a mode that waits for my approval.
- **Check the AI's judgment calls.** My request said "above the average" without saying which average. Claude Code chose a weighted average (total cost ÷ total conversions) instead of a simple one. I checked this and agreed: a weighted average stops one small, expensive campaign from distorting the benchmark.
- **Test the awkward cases.** The first version worked on the sample data. But when I set one campaign's conversions to 0, the report showed "€0.00 per conversion", which made a campaign that wasted €360 look like the best one.
- **Review the output, then refine.** After reading the results I asked for these changes:
  - Show "n/a" instead of €0.00 when there are no conversions.
  - Don't flag paused campaigns that spent nothing. I added a test campaign with all zeros to check this.
  - Rename "above average" to **"needs attention"**, because a campaign with no conversions is flagged for a different reason.
  - Show "n/a" for CTR, CPC and conversion rate whenever the calculation would divide by zero.
- **The wording matters as much as the maths.** Most of my changes weren't about calculations. They were about making sure the report doesn't mislead the person reading it.
