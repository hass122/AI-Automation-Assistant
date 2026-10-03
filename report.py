import csv
import os
from datetime import datetime

def save_report(results, keyword):
    # Vercel/serverless filesystems are ephemeral. /tmp is the writable
    # runtime location; locally we keep the original output/reports folder.
    if os.getenv("VERCEL"):
        folder = "/tmp/reports"
    else:
        folder = os.path.join("output", "reports")

    os.makedirs(folder, exist_ok=True)

    filename = datetime.now().strftime("report_%Y%m%d_%H%M%S.csv")
    path = os.path.join(folder, filename)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Keyword", "ID", "Title", "Score", "Match"])
        for item in results:
            writer.writerow([
                keyword,
                item["id"],
                item["title"],
                item["score"],
                item["match"],
            ])

    return path
