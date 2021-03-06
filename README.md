# Google Places

Collect and parse data from the google map api for any retail outlet in the united states.

For example, use this program to plot competitor proximity curves - the % of retail storefronts that operate without a competitor within N meters.

### Getting Started

From the command line, run `python zip_codes.py` to collect and store a list of all zip codes in the US, along with their corresponding GPS coordinates.

To collect storefront location data for Chipotle, from the command line run `python google_maps.py chipotle`.

### Analysis

Which zip codes have more Starbucks than Dunkin? Which zip codes only have Dunkin?

![image](https://github.com/BrandonEmmerich/google_maps/blob/master/analysis/zip_code_winners.png)

What is the competitor proximity curve for both Starbucks and Dunkin?

![image](https://github.com/BrandonEmmerich/google_maps/blob/master/analysis/competitor_proximity_curve.png)
