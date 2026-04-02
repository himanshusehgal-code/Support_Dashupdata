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
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()

        try:
            print("Opening URL:", url)

            # ✅ Better loading strategy
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)

            # ✅ IMPORTANT: wait for dashboard content
            await page.wait_for_selector("#mainContainer", timeout=30000)

            # Extra buffer for charts
            await asyncio.sleep(3)

            # ✅ Clean UI before PDF
            await page.evaluate("""() => {
                const hideIds = ['mobileAside', 'mobileTabs', 'dropZone', 'actionPanelWrapper'];
                hideIds.forEach(id => { 
                    const el = document.getElementById(id); 
                    if(el) el.style.display = 'none'; 
                });

                const header = document.querySelector('header'); 
                if(header) header.style.display = 'none';

                const main = document.getElementById('mainContainer'); 
                if(main) main.style.overflow = 'visible';
            }""")

            # ✅ Generate PDF
            pdf_bytes = await page.pdf(
                format="A4",
                landscape=True,
                print_background=True,
                margin={
                    "top": "10mm",
                    "bottom": "10mm",
                    "left": "10mm",
                    "right": "10mm"
                }
            )

            await browser.close()

            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": "attachment; filename=dashboard.pdf"
                }
            )

        except Exception as e:
            await browser.close()
            print("PDF ERROR:", str(e))
            return Response(
                content=f"Error: {str(e)}",
                status_code=500
            )
