from playwright.async_api import async_playwright
from fastapi import Response
import asyncio

async def generate_dashboard_pdf(url: str):
    async with async_playwright() as p:
        # RAM Bachane ke liye extra options
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-zygote",
                "--single-process"
            ]
        )
        
        # Ek chota aur fast browser window kholna
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        try:
            # Page load hone ka wait (Timeout set to 60s for Render speed)
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await asyncio.sleep(2) # Charts load hone ka extra buffer
            
            # Faltu cheezein hide karna
            await page.evaluate("""() => {
                const hideIds = ['mobileAside', 'mobileTabs', 'dropZone', 'actionPanelWrapper'];
                hideIds.forEach(id => { const el = document.getElementById(id); if(el) el.style.display = 'none'; });
                const header = document.querySelector('header'); if(header) header.style.display = 'none';
                const main = document.getElementById('mainContainer'); if(main) main.style.overflow = 'visible';
            }""")
            
            # PDF Generate karna (Landscape mode)
            pdf_bytes = await page.pdf(
                format="A4",
                landscape=True, 
                print_background=True,
                margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}
            )
            
            await browser.close()
            return Response(content=pdf_bytes, media_type="application/pdf")

        except Exception as e:
            await browser.close()
            return Response(content=f"Error: {str(e)}", status_code=500)
