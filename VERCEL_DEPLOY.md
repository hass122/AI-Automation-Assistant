# Vercel Deployment

This project is a Flask application using:
- Python
- Flask
- REST API requests
- scikit-learn (TF-IDF + cosine similarity)
- Selenium browser automation
- CSV reporting

## Deploy

Push the repository to GitHub and import it into Vercel.

Vercel recognizes Flask applications from `app.py` automatically.

## Verify

After deployment, open:

`https://YOUR-DOMAIN.vercel.app/health`

Expected response:

`{"status":"ok","service":"AI Automation Assistant"}`

Then open `/` and test the form.

## Important Selenium note

The Flask page is deliberately designed to start without importing Selenium or
scikit-learn. Those heavier components load only when the form is submitted.

If `/health` and `/` work but submitting a keyword shows an automation error,
the remaining issue is the browser runtime (Chromium/Chrome) rather than Flask.
Vercel supports long-running Python Functions and browser-automation workloads,
but the Selenium browser environment must be available to the deployed runtime.

For a production system, a dedicated browser worker/container can be used if
the Selenium workload is not reliable inside the Function runtime.
