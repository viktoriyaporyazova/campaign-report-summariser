"""
Campaign Report Summariser
--------------------------
Reads Google Ads-style campaign data from a CSV file, works out the key
metrics for each campaign, flags the expensive ones, and writes a short
plain-language summary to a text file.

How to run it (from this folder):
    python3 summarise.py
"""

# "csv" is part of Python's standard library, so nothing needs installing.
import csv

# File names are kept at the top so they are easy to find and change.
INPUT_FILE = "campaigns.csv"
OUTPUT_FILE = "summary.txt"


def safe_divide(top, bottom):
    """Divide top by bottom. If bottom is 0, return 0 instead of crashing."""
    if bottom == 0:
        return 0
    return top / bottom


def read_campaigns(filename):
    """Read the CSV file and return a list of campaigns (one dictionary each)."""
    campaigns = []

    # "with open(...)" opens the file and closes it again automatically.
    with open(filename, newline="", encoding="utf-8") as file:
        # DictReader uses the header row, so each row becomes a dictionary
        # like {"campaign_name": "Brand Search", "clicks": "1100", ...}
        reader = csv.DictReader(file)

        for row in reader:
            # Everything in a CSV is read as text, so we convert the numbers:
            # int() for whole numbers, float() for numbers with decimals.
            campaign = {
                "name": row["campaign_name"],
                "impressions": int(row["impressions"]),
                "clicks": int(row["clicks"]),
                "cost": float(row["cost_eur"]),
                "conversions": int(row["conversions"]),
            }
            campaigns.append(campaign)

    return campaigns


def add_metrics(campaign):
    """Calculate the four metrics and store them inside the campaign dictionary."""
    # Click-through rate: what % of people who saw the ad clicked it.
    campaign["ctr"] = safe_divide(campaign["clicks"], campaign["impressions"]) * 100

    # Cost per click: how much one click cost on average.
    campaign["cpc"] = safe_divide(campaign["cost"], campaign["clicks"])

    # Conversion rate: what % of clicks turned into a conversion (e.g. a sale).
    campaign["conv_rate"] = safe_divide(campaign["conversions"], campaign["clicks"]) * 100

    # Cost per conversion: how much we paid for each conversion.
    campaign["cost_per_conv"] = safe_divide(campaign["cost"], campaign["conversions"])


def build_summary(campaigns):
    """Create the summary text and return it as a list of lines."""
    # --- Account totals ---------------------------------------------------
    # sum(...) adds up one field across all campaigns.
    total_cost = sum(c["cost"] for c in campaigns)
    total_clicks = sum(c["clicks"] for c in campaigns)
    total_conversions = sum(c["conversions"] for c in campaigns)

    # The average cost per conversion for the whole account.
    # We use total cost / total conversions rather than averaging the eight
    # campaign figures, so one tiny campaign can't skew the result.
    average_cost_per_conv = safe_divide(total_cost, total_conversions)

    # --- Flag expensive campaigns -----------------------------------------
    # A campaign is flagged if:
    #   - it got no conversions but still spent money (paid, got nothing back), or
    #   - it costs more per conversion than the average.
    # A campaign with no conversions AND no spend (e.g. paused) is not flagged.
    flagged = []
    for c in campaigns:
        if c["conversions"] == 0:
            if c["cost"] > 0:
                flagged.append(c)
        elif c["cost_per_conv"] > average_cost_per_conv:
            flagged.append(c)

    # Sort so the most expensive campaign comes first.
    flagged.sort(key=lambda c: c["cost_per_conv"], reverse=True)

    # The best performer is the cheapest campaign that has conversions.
    converting = [c for c in campaigns if c["conversions"] > 0]
    best = min(converting, key=lambda c: c["cost_per_conv"])

    # --- Write the text ---------------------------------------------------
    # Inside f-strings, ":,.2f" means "comma for thousands, 2 decimal places".
    lines = []
    lines.append("CAMPAIGN REPORT SUMMARY")
    lines.append("=======================")
    lines.append("")
    lines.append("Overview")
    lines.append("--------")
    lines.append(
        f"We looked at {len(campaigns)} campaigns. Together they spent "
        f"€{total_cost:,.2f}, got {total_clicks:,} clicks and "
        f"{total_conversions:,} conversions."
    )
    lines.append(f"On average, each conversion cost €{average_cost_per_conv:,.2f}.")
    lines.append("")

    lines.append("Campaign by campaign")
    lines.append("--------------------")
    for c in campaigns:
        # Put a marker next to flagged campaigns so they stand out.
        marker = "  <-- needs attention" if c in flagged else ""
        # When we would divide by zero there is no real answer, so we say
        # "n/a" instead of showing a misleading 0.00.
        # CTR needs impressions; CPC needs clicks.
        if c["impressions"] == 0:
            ctr_text = "CTR n/a"
        else:
            ctr_text = f"CTR {c['ctr']:.2f}%"

        if c["clicks"] == 0:
            cpc_text = "CPC n/a"
        else:
            cpc_text = f"CPC €{c['cpc']:.2f}"

        # Conversion rate also needs clicks.
        if c["clicks"] == 0:
            conv_rate_text = "Conversion rate n/a"
        else:
            conv_rate_text = f"Conversion rate {c['conv_rate']:.2f}%"

        # Cost per conversion needs conversions.
        if c["conversions"] == 0:
            cost_per_conv_text = "Cost per conversion: n/a (no conversions)"
        else:
            cost_per_conv_text = f"Cost per conversion €{c['cost_per_conv']:.2f}"

        lines.append(f"{c['name']}{marker}")
        lines.append(
            f"  {ctr_text} | {cpc_text} | "
            f"{conv_rate_text} | "
            f"{cost_per_conv_text}"
        )
    lines.append("")

    lines.append("What needs attention")
    lines.append("--------------------")
    if flagged:
        lines.append(f"{len(flagged)} of {len(campaigns)} campaigns need attention:")
        for c in flagged:
            if c["conversions"] == 0:
                lines.append(f"- {c['name']}: spent €{c['cost']:,.2f} with no conversions.")
            else:
                # How many times more expensive than average, e.g. "2.5x".
                times = c["cost_per_conv"] / average_cost_per_conv
                lines.append(
                    f"- {c['name']}: €{c['cost_per_conv']:,.2f} per conversion "
                    f"({times:.1f}x the average)."
                )
    else:
        lines.append("Good news: no campaign is above the average cost per conversion.")
    lines.append("")

    lines.append(
        f"Best performer: {best['name']}, at only "
        f"€{best['cost_per_conv']:,.2f} per conversion."
    )

    return lines


def main():
    """Run all the steps in order."""
    campaigns = read_campaigns(INPUT_FILE)

    for campaign in campaigns:
        add_metrics(campaign)

    lines = build_summary(campaigns)

    # "\n".join(...) glues the lines together with a line break between each.
    summary_text = "\n".join(lines)

    # "w" means write mode: create the file, or replace it if it exists.
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(summary_text + "\n")

    # Also show the summary in the terminal.
    print(summary_text)
    print(f"\nSummary saved to {OUTPUT_FILE}")


# This line means: only run main() when this file is run directly,
# not when another script imports it.
if __name__ == "__main__":
    main()
