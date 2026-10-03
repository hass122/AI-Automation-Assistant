import os
from flask import Flask, render_template, request
from api.api_client import fetch_demo_jobs
from ai.analyzer import analyze_jobs
from automation.selenium_bot import run_selenium_demo
from utils.report import save_report

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    keyword = ""
    message = ""

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

        if not keyword:
            message = "Please enter a keyword."
        else:
            try:
                jobs = fetch_demo_jobs()
                analyzed = analyze_jobs(jobs, keyword)
                selenium_result = run_selenium_demo(keyword)
                report_path = save_report(analyzed, keyword)

                results = {
                    "jobs": analyzed,
                    "selenium": selenium_result,
                    "report": report_path,
                    "total": len(analyzed),
                    "high": sum(1 for x in analyzed if x["match"] == "High"),
                    "medium": sum(1 for x in analyzed if x["match"] == "Medium"),
                    "low": sum(1 for x in analyzed if x["match"] == "Low"),
                }
            except Exception as e:
                message = f"Automation error: {e}"

    return render_template("index.html", results=results, keyword=keyword, message=message)

if __name__ == "__main__":
    # Local development only. Vercel imports `app` directly.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
