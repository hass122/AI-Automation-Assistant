import os
import logging
from flask import Flask, render_template, request, jsonify

# ---------------------------------------------------------
# Flask App
# ---------------------------------------------------------

app = Flask(__name__)

# Secret key (optional for current app, but useful for Flask)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """
    Simple health-check endpoint for Vercel.
    """

    return jsonify({
        "status": "ok",
        "service": "AI Automation Assistant"
    }), 200


# ---------------------------------------------------------
# Home / Main Application
# ---------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    results = None
    keyword = ""
    message = ""
    message_type = ""

    # -----------------------------------------------------
    # POST Request
    # -----------------------------------------------------

    if request.method == "POST":

        keyword = request.form.get("keyword", "").strip()

        # ---------------------------------------------
        # Validate keyword
        # ---------------------------------------------

        if not keyword:

            message = "Please enter a keyword."
            message_type = "error"

        else:

            try:

                logger.info(
                    "Automation request received for keyword: %s",
                    keyword
                )

                # -----------------------------------------
                # Import project modules
                # -----------------------------------------

                from api.api_client import fetch_demo_jobs
                from ai.analyzer import analyze_jobs

                # -----------------------------------------
                # Fetch demo jobs
                # -----------------------------------------

                logger.info("Fetching demo jobs...")

                jobs = fetch_demo_jobs()

                if jobs is None:
                    jobs = []

                logger.info(
                    "Fetched %s jobs",
                    len(jobs)
                )

                # -----------------------------------------
                # Analyze jobs
                # -----------------------------------------

                logger.info(
                    "Analyzing jobs using keyword: %s",
                    keyword
                )

                analyzed = analyze_jobs(
                    jobs,
                    keyword
                )

                if analyzed is None:
                    analyzed = []

                # -----------------------------------------
                # Calculate statistics
                # -----------------------------------------

                high_count = 0
                medium_count = 0
                low_count = 0

                for item in analyzed:

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

                # -----------------------------------------
                # Selenium
                # -----------------------------------------
                #
                # Selenium may not work on Vercel's
                # serverless environment because a browser
                # runtime may not be available.
                #
                # Therefore Selenium failure should NOT
                # destroy the complete application.
                # -----------------------------------------

                selenium_result = None

                try:

                    from automation.selenium_bot import (
                        run_selenium_demo
                    )

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

                # -----------------------------------------
                # Save Report
                # -----------------------------------------
                #
                # Report generation can also fail in a
                # serverless environment if it attempts
                # to write to a permanent local directory.
                # -----------------------------------------

                report_path = None

                try:

                    from utils.report import save_report

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

                # -----------------------------------------
                # Final Results
                # -----------------------------------------

                results = {
                    "jobs": analyzed,
                    "selenium": selenium_result,
                    "report": report_path,
                    "total": len(analyzed),
                    "high": high_count,
                    "medium": medium_count,
                    "low": low_count,
                }

                message = (
                    f"Analysis completed successfully. "
                    f"{len(analyzed)} jobs analyzed."
                )

                message_type = "success"

                logger.info(
                    "Automation request completed successfully."
                )

            # ---------------------------------------------
            # General Application Error
            # ---------------------------------------------

            except Exception as error:

                logger.exception(
                    "Automation request failed."
                )

                message = (
                    f"Automation error: "
                    f"{type(error).__name__}: {error}"
                )

                message_type = "error"

    # -----------------------------------------------------
    # Render Page
    # -----------------------------------------------------

    try:

        return render_template(
            "index.html",
            results=results,
            keyword=keyword,
            message=message,
            message_type=message_type,
        )

    except Exception as template_error:

        logger.exception(
            "Template rendering failed."
        )

        # This response helps identify template problems
        # instead of returning a generic Vercel 500 page.

        return (
            f"""
            <h1>AI Automation Assistant</h1>

            <h2>Template Error</h2>

            <p>
                {type(template_error).__name__}:
                {template_error}
            </p>

            <p>
                Make sure your project contains:
            </p>

            <pre>
templates/
    index.html
            </pre>
            """,
            500,
        )


# ---------------------------------------------------------
# Vercel / Production Entry Point
# ---------------------------------------------------------

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
        debug=False,
    )
