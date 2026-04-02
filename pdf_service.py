from playwright.async_api import async_playwright
from fastapi import Response
import asyncio

async def generate_dashboard_pdf(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print("Opening URL:", url)

            await page.goto(url, timeout=60000)

            # ✅ wait body instead of custom id (safe)
            await page.wait_for_selector("body", timeout=30000)

            await asyncio.sleep(5)

            # debug screenshot
            await page.screenshot(path="debug.png")

            pdf_bytes = await page.pdf(
                format="A4",
                print_background=True
            )

            await browser.close()

            return Response(
                content=pdf_bytes,
                media_type="application/pdf"
            )

        except Exception as e:
            await browser.close()
            print("PDF ERROR:", str(e))
            return Response(content=str(e), status_code=500)
