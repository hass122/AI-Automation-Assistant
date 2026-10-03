import os
import logging

from flask import Flask, render_template, request, jsonify


# =========================================================
# Flask Application
# =========================================================

app = Flask(__name__)

# Optional secret key
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


# =========================================================
# Logging
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# =========================================================
# Health Check
# =========================================================

@app.route("/health", methods=["GET"])
def health():
    """
    Health-check endpoint for Vercel.
    """

    return jsonify({
        "status": "ok",
        "service": "AI Automation Assistant"
    }), 200


# =========================================================
# Home Page
# =========================================================

@app.route("/", methods=["GET", "POST"])
def index():

    results = None
    keyword = ""
    message = ""
    message_type = ""

    # =====================================================
    # POST Request
    # =====================================================

    if request.method == "POST":

        keyword = request.form.get("keyword", "").strip()

        # -------------------------------------------------
        # Validate keyword
        # -------------------------------------------------

        if not keyword:

            message = "Please enter a keyword."
            message_type = "error"

        else:

            try:

                logger.info(
                    "Automation request received. Keyword: %s",
                    keyword
                )

                # =================================================
                # Import Project Modules
                # =================================================
                #
                # IMPORTANT:
                # These files are located in the ROOT directory
                # of your GitHub repository.
                #
                # api_client.py
                # analyzer.py
                # selenium_bot.py
                # report.py
                #
                # Therefore we DO NOT use:
                # api.api_client
                # ai.analyzer
                # automation.selenium_bot
                # utils.report
                # =================================================

                from api_client import fetch_demo_jobs
                from analyzer import analyze_jobs

                # =================================================
                # Fetch Jobs
                # =================================================

                logger.info("Fetching jobs...")

                jobs = fetch_demo_jobs()

                if jobs is None:
                    jobs = []

                logger.info(
                    "Jobs fetched: %s",
                    len(jobs)
                )

                # =================================================
                # Analyze Jobs
                # =================================================

                logger.info(
                    "Analyzing jobs for keyword: %s",
                    keyword
                )

                analyzed = analyze_jobs(
                    jobs,
                    keyword
                )

                if analyzed is None:
                    analyzed = []

                # =================================================
                # Calculate Match Statistics
                # =================================================

                high_count = 0
                medium_count = 0
                low_count = 0

                for item in analyzed:

                    if not isinstance(item, dict):
                        continue

                    match_level = item.get(
                        "match",
                        ""
                    )

                    if match_level == "High":
                        high_count += 1

                    elif match_level == "Medium":
                        medium_count += 1

                    elif match_level == "Low":
                        low_count += 1

                # =================================================
                # Selenium Automation
                # =================================================
                #
                # Selenium may not work properly on Vercel
                # Serverless Functions because Chrome/browser
                # runtime may not be available.
                #
                # Therefore Selenium errors are handled separately.
                # =================================================

                selenium_result = None

                try:

                    from selenium_bot import run_selenium_demo

                    logger.info(
                        "Starting Selenium automation..."
                    )

                    selenium_result = run_selenium_demo(
                        keyword
                    )

                    logger.info(
                        "Selenium automation completed."
                    )

                except Exception as selenium_error:

                    logger.exception(
                        "Selenium automation failed."
                    )

                    selenium_result = {
                        "status": "error",
                        "message": (
                            f"{type(selenium_error).__name__}: "
                            f"{selenium_error}"
                        )
                    }

                # =================================================
                # Generate Report
                # =================================================
                #
                # Report generation is also handled separately
                # because Vercel has temporary filesystem storage.
                # =================================================

                report_path = None

                try:

                    from report import save_report

                    logger.info(
                        "Generating report..."
                    )

                    report_path = save_report(
                        analyzed,
                        keyword
                    )

                    logger.info(
                        "Report generated: %s",
                        report_path
                    )

                except Exception as report_error:

                    logger.exception(
                        "Report generation failed."
                    )

                    report_path = {
                        "status": "error",
                        "message": (
                            f"{type(report_error).__name__}: "
                            f"{report_error}"
                        )
                    }

                # =================================================
                # Final Results
                # =================================================

                results = {
                    "jobs": analyzed,
                    "selenium": selenium_result,
                    "report": report_path,
                    "total": len(analyzed),
                    "high": high_count,
                    "medium": medium_count,
                    "low": low_count
                }

                message = (
                    f"Analysis completed successfully. "
                    f"{len(analyzed)} jobs analyzed."
                )

                message_type = "success"

                logger.info(
                    "Automation request completed successfully."
                )

            # =====================================================
            # General Application Error
            # =====================================================

            except Exception as error:

                logger.exception(
                    "Automation request failed."
                )

                message = (
                    f"Automation error: "
                    f"{type(error).__name__}: {error}"
                )

                message_type = "error"

    # =========================================================
    # Render Template
    # =========================================================

    try:

        return render_template(
            "index.html",
            results=results,
            keyword=keyword,
            message=message,
            message_type=message_type
        )

    except Exception as template_error:

        logger.exception(
            "Template rendering failed."
        )

        return (
            f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>AI Automation Assistant</title>
                <meta charset="UTF-8">
            </head>

            <body>

                <h1>AI Automation Assistant</h1>

                <h2>Template Error</h2>

                <p>
                    <strong>
                        {type(template_error).__name__}
                    </strong>
                    :
                    {template_error}
                </p>

                <p>
                    Make sure this file exists:
                </p>

                <pre>
templates/
    index.html
                </pre>

            </body>
            </html>
            """,
            500
        )


# =========================================================
# Vercel / Local Development
# =========================================================

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
