
## MarketTor is an all-in-one, open source platform for building better products

- Specify events manually, or use autocapture to get started quickly
- Analyze data with ready-made visualizations, or do it yourself with SQL
- Track website visitors separately with our GA4 alternative
- Only capture properties on the people you want to track, save money when you don't
- Gather insights by capturing session replays, console logs, and network monitoring
- Improve your product with Experiments that automatically analyze performance
- Safely roll out features to select users or cohorts with feature flags
- Send out fully customizable surveys to specific cohorts of users
- Connect to external services and manage data flows with MarketTor CDP

MarketTor is available with hosting in the EU or US and is fully SOC 2 compliant. It's free to get started and comes with a generous monthly free tier:
- 1 million events
- 5k session replays
- 1 million feature flag requests
- 250 survey responses

We're constantly adding new features, with <a href="https://markettor.com/docs/web-analytics">web analytics</a> and <a href="https://markettor.com/docs/data-warehouse">data warehouse</a> now in beta!

## Table of Contents

- [Get started for free](#get-started-for-free)
- [Docs](#docs)
- [Contributing](#contributing)
- [Philosophy](#philosophy)
- [Open-source vs paid](#open-source-vs-paid)

## Get started for free

### MarketTor Cloud (Recommended)

The fastest and most reliable way to get started with MarketTor is signing up for free to [MarketTor Cloud](https://us.markettor.com/signup) or [MarketTor Cloud EU](https://eu.markettor.com/signup). Your first 1 million events (and 5k replays) are free every month, after which you pay based on usage.

### Open-source hobby deploy (Advanced)

You can deploy a hobby instance in one line on Linux with Docker (recommended 4GB memory):

 ```bash 
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/markettor/markettor/HEAD/bin/deploy-hobby)" 
 ``` 

Open source deployments should scale to approximately 100k events per month, after which we recommend migrating to a MarketTor Cloud instance. See our [docs for more info and limitations](https://markettor.com/docs/self-host/open-source/deployment). Please note that we do not provide customer support for open source deployments. 

### Analytics and optimization tools

- **Event-based analytics:** Capture your product's usage [automatically](https://markettor.com/docs/libraries/js#autocapture), or [customize](https://markettor.com/docs/getting-started/install) it to your needs
- **User and group tracking:** Understand the [people](https://markettor.com/manual/persons) and [groups](https://markettor.com/manual/group-analytics) behind the events and track properties about them when needed
- **Data visualizations:** Create and share [graphs](https://markettor.com/docs/features/trends), [funnels](https://markettor.com/docs/features/funnels), [paths](https://markettor.com/docs/features/paths), [retention](https://markettor.com/docs/features/retention), and [dashboards](https://markettor.com/docs/features/dashboards)
- **SQL access:** Use [SQL](https://markettor.com/docs/product-analytics/sql) to get a deeper understanding of your users, breakdown information and create completely tailored visualizations
- **Session replays:** [Watch videos](https://markettor.com/docs/features/session-recording) of your users' behavior, with fine-grained filters and privacy controls, as well as network monitoring and captured console logs
- **Heatmaps:** See where users click and get a visual representation of their behaviour with the [MarketTor Toolbar](https://markettor.com/docs/features/toolbar)
- **Feature flags:** Test and manage the rollout of [new features](https://markettor.com/docs/feature-flags/installation) to specific users and groups, or deploy flags as kill-switches
- **Experiments:** run simple or complex changes as [experiments](https://markettor.com/manual/experimentation) and get automatic significance calculations
- **Correlation analysis:** Discover what events and properties [correlate](https://markettor.com/manual/correlation) with success and failure
- **Surveys:** Collect qualitative feedback from your users using fully customizable [surveys](https://markettor.com/docs/surveys/installation)

### Data and infrastructure tools

- **Import and export your data:** Import from and export to the services that matter to you with [the MarketTor CDP](https://markettor.com/docs/cdp)
- **Ready-made libraries:** We’ve built libraries for [JavaScript](https://markettor.com/docs/libraries/js), [Python](https://markettor.com/docs/libraries/python), [Ruby](https://markettor.com/docs/libraries/ruby), [Node](https://markettor.com/docs/libraries/node), [Go](https://markettor.com/docs/libraries/go), [Android](https://markettor.com/docs/libraries/android), [iOS](https://markettor.com/docs/libraries/ios), [PHP](https://markettor.com/docs/libraries/php), [Flutter](https://markettor.com/docs/libraries/flutter), [React Native](https://markettor.com/docs/libraries/react-native), [Elixir](https://markettor.com/docs/libraries/elixir), [Nim](https://github.com/Yardanico/markettor-nim), and an [API](https://markettor.com/docs/api) for anything else
- **Plays nicely with data warehouses:** import events or user data from your warehouse by writing a simple transformation plugin, and export data with pre-built apps - such as [BigQuery](https://markettor.com/apps/bigquery-export), [Redshift](https://markettor.com/apps/redshift-export), [Snowflake](https://markettor.com/apps/snowflake-export), and [S3](https://markettor.com/apps/s3-expo)

[Read a full list of MarketTor features](https://markettor.com/product).

