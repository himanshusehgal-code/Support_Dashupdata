from playwright.async_api import async_playwright
from fastapi import Response

async def generate_dashboard_pdf(url: str):
    async with async_playwright() as p:
        # 🔥 RAM Saving Arguments add kiye hain
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox", 
                "--disable-setuid-sandbox", 
                "--disable-dev-shm-usage", 
                "--disable-accelerated-2d-canvas", 
                "--no-first-run", 
                "--no-zygote", 
                "--single-process" # Memory bachane ke liye single process
            ]
        )
        
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Timeout badha diya hai taaki Render slow hone par fail na ho
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(3000) # Charts render hone ka buffer
        
        # Cleanup UI
        await page.evaluate("""() => {
            const ids = ['mobileAside', 'mobileTabs', 'dropZone', 'actionPanelWrapper'];
            ids.forEach(id => { const el = document.getElementById(id); if(el) el.style.display = 'none'; });
            const header = document.querySelector('header'); if(header) header.style.display = 'none';
        }""")
        
        pdf_bytes = await page.pdf(
            format="A4",
            landscape=True, 
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}
        )
        
        await browser.close()
        return Response(content=pdf_bytes, media_type="application/pdf")
