import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "AI Automation Assistant"}

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
                # Import heavier/optional runtime components only when the
                # automation request is actually made.
                from api.api_client import fetch_demo_jobs
                from ai.analyzer import analyze_jobs
                from automation.selenium_bot import run_selenium_demo
                from utils.report import save_report

                jobs = fetch_demo_jobs()
                analyzed = analyze_jobs(jobs, keyword)

                # Selenium is kept as part of the demo workflow. If the
                # browser runtime is unavailable on a serverless instance,
                # the page will show the specific automation error instead
                # of crashing the entire Flask Function.
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
                app.logger.exception("Automation request failed")
                message = f"Automation error: {type(e).__name__}: {e}"

    return render_template(
        "index.html",
        results=results,
        keyword=keyword,
        message=message,
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=True,
    )
