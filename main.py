from fastapi import FastAPI
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get('/')
def root():
    return {"message": 'API DZIAŁA!'}

@app.get('/data')
def get_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://playwright.dev/')
        title = page.title()
        heading = page.locator('h1').inner_text()
        browser.close()
    return {"title": title, "heading": heading}