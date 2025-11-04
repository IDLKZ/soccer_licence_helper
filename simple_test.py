"""Simple test without emoji"""
import requests

print("Testing report generation...")

try:
    response = requests.post(
        "http://localhost:8001/api/v1/reports/generate",
        json={"report_id": 1},
        timeout=30
    )

    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        print("SUCCESS! Saving PDF...")
        with open("report_1.pdf", "wb") as f:
            f.write(response.content)
        print(f"Saved to report_1.pdf ({len(response.content)} bytes)")
    else:
        print("ERROR:")
        print(response.text)

except Exception as e:
    print(f"Error: {e}")
