# Forecast

Demand forecasting tool that pulls sales history from Snowflake and generates
per-customer, per-item forecasts using time series models (currently
Exponential Smoothing via statsmodels).

## Status

Early prototype. main.py establishes the Snowflake → DataFrame pipeline and
a test call to an LLM API; static.py is a standalone script that forecasts
a single customer/item pair from a static CSV export. The two aren't wired
together yet, and code/ (intended home for the real pipeline) is still empty.

## Structure

- main.py — connects to Snowflake, pulls sales table into a DataFrame,
  cleans/sorts it (by customer, item, month), and pings an LLM API as a
  connectivity test.
- static.py — standalone example: loads other/sales_data.csv, filters to
  one customer/item/organization, aggregates to monthly demand, plots it, and
  fits an ExponentialSmoothing model to forecast 18 months out.
- code/ — empty; intended location for the production pipeline.
- other/ — reference materials and sample data (sales_data.csv,
  forecasting.pdf, an example plot).
- PSB Documentation.pdf — reference doc (source system / data context).
- requirements.txt — Python dependencies.
- .env — local credentials (not committed): Snowflake connection details
  and LLM API key.

## Setup

1. Create a .env file with:
   
   SNOWFLAKE_USER=
   SNOWFLAKE_PASSWORD=
   SNOWFLAKE_ACCOUNT=
   SNOWFLAKE_WAREHOUSE=
   SNOWFLAKE_DATABASE=
   SNOWFLAKE_SCHEMA=
   GEMINI_API_KEY=
   
2. Install dependencies:
   bash
   pip install -r requirements.txt
   
   Note: requirements.txt currently lists anthropic, but main.py uses
   google-genai — reconcile these before relying on this list.

## Usage

Run the Snowflake connectivity + data pull:
bash
python main.py


Run the standalone single product/customer forecast (uses the CSV in other/):
bash
python static.py


## Next steps

- Decide on one LLM provider (Anthropic vs. Gemini) and align
  requirements.txt with actual imports.
- Move the forecasting logic from static.py into code/, generalized to
  run across all customer/item pairs pulled from Snowflake rather than one
  hardcoded combination.
- Replace the CSV-based data source in static.py with the Snowflake
  DataFrame from main.py.
