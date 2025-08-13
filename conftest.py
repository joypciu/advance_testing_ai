import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_type():
    with sync_playwright() as p:
        yield p.chromium

@pytest.fixture(scope="session")
def browser(browser_type):
    browser = browser_type.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()
