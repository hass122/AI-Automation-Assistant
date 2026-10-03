# Deploy AI Automation Assistant to Vercel

## Important
This project uses Flask + scikit-learn + Selenium.

Vercel supports Flask as a Python Function. The ML/API part is suitable for Vercel.
The Selenium step depends on a Chromium/Chrome browser being available in the
runtime. Selenium 4.36+ uses Selenium Manager, but browser automation should
still be tested after deployment. If the Selenium step cannot start a browser
in the chosen runtime, move only the Selenium worker to a VPS/container while
keeping the Flask/API frontend on Vercel.

## 1. Test locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## 2. Push this folder to GitHub

Create a repository and upload the contents of this folder.

## 3. Deploy on Vercel

1. Sign in to Vercel.
2. Add New Project.
3. Import the GitHub repository.
4. Keep the project root at the repository root.
5. Vercel should detect Flask/Python automatically.
6. Deploy.

No `/api` folder is required for current Flask deployments.

## 4. CLI alternative

```bash
npm install -g vercel
vercel login
vercel
vercel --prod
```

## 5. If Vercel reports a large Python Function

Vercel's Large Functions support can be enabled for projects that need it.
Add this environment variable in Vercel:

VERCEL_SUPPORT_LARGE_FUNCTIONS=1

Then redeploy.

## 6. If Selenium fails in production

Check the Vercel Function logs. The Flask/ML/API functionality can remain
on Vercel, while the Selenium browser worker can be moved to a VPS/container
with Chromium installed. This is the most reliable production architecture
for heavy browser automation.
