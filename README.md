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

## How to run it (Mac, step by step)

You don't need any coding experience. It takes about 5 minutes.

### 1. Download the project
1. On this GitHub page, click the green **Code** button.
2. Click **Download ZIP**.
3. Open your **Downloads** folder and double-click the ZIP file.
   A folder called **campaign-report-summariser-main** appears.

### 2. Open Terminal
1. Press **Cmd + Space** to open Spotlight search.
2. Type **Terminal** and press **Enter**.
   A window with text and a blinking cursor opens.

### 3. Go to the project folder
Type this and press **Enter**:

    cd ~/Downloads/campaign-report-summariser-main

You're in the right place if the folder name now appears just before the `%` sign.

If you moved the folder somewhere else (for example to your Desktop), replace `Downloads` with that location, for example:

    cd ~/Desktop/campaign-report-summariser-main

### 4. Check that Python is installed
Type this and press **Enter**:

    python3 --version

You should see something like `Python 3.x.x`.
If your Mac asks to install **Command Line Tools**, click **Install** and wait for it to finish, then try again.

### 5. Run the tool
Type this and press **Enter**:

    python3 summarise.py

The report appears in Terminal and is also saved as **summary.txt**.

### 6. Open the report
Type this and press **Enter**:

    open summary.txt

Or open the **campaign-report-summariser-main** folder in Finder and double-click **summary.txt**.

## Using your own data

1. In the project folder, right-click **campaigns.csv** and choose **Open With → TextEdit**.
   (Avoid Excel here: it can change the file's format when saving.)
2. Replace the example rows with your own campaigns. Keep the first line exactly as it is:

       campaign_name,impressions,clicks,cost_eur,conversions

3. Save with **Cmd + S**.
4. In Terminal, run `python3 summarise.py` again to get a new report.

### Common problems
- **"No such file or directory"**: you're not in the project folder, or the folder name has a typo. Check the spelling and repeat step 3.
- **"command not found: python3"**: Python isn't installed. Repeat step 4 and install Command Line Tools when asked.
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
