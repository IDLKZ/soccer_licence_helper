from __future__ import annotations

import httpx
from app.domain.services.pdf_generator import IPDFGenerator


class PuppeteerPdfGenerator(IPDFGenerator):
    def __init__(self, service_url: str = "http://localhost:3001/render", timeout: int = 90):
        self.service_url = service_url
        self.timeout = timeout

    def generate_from_html(self, html: str, output_path: str) -> None:
        # IPDFGenerator у тебя синхронный — поэтому используем sync httpx.Client
        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(self.service_url, json={"html": html})
            r.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(r.content)
