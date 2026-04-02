from playwright.async_api import async_playwright
from fastapi import Response

async def generate_dashboard_pdf(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(2000) # Charts render hone ka wait
        
        # Dashboard ko clean karo (Faltu UI hide karo)
        await page.evaluate("""
            () => {
                const hideElements = ['mobileAside', 'mobileTabs', 'dropZone', 'actionPanelWrapper'];
                hideElements.forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.style.display = 'none';
                });
                const header = document.querySelector('header');
                if (header) header.style.display = 'none';
                const main = document.getElementById('mainContainer');
                if (main) {
                    main.style.height = 'auto';
                    main.style.overflow = 'visible';
                }
            }
        """)
        
        # Landscape PDF nikalo
        pdf_bytes = await page.pdf(
            format="A4",
            landscape=True, 
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}
        )
        
        await browser.close()
        return Response(content=pdf_bytes, media_type="application/pdf")
