"""Test department report generation"""
import requests

print("Testing department report generation...")

try:
    response = requests.post(
        "http://localhost:8002/api/v1/department-reports/generate",
        json={"report_id": 1},
        timeout=30
    )

    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        print("SUCCESS! Saving PDF...")
        with open("department_report_1.pdf", "wb") as f:
            f.write(response.content)
        print(f"Saved to department_report_1.pdf ({len(response.content)} bytes)")
    else:
        print("ERROR:")
        print(response.text)

except Exception as e:
    print(f"Error: {e}")
