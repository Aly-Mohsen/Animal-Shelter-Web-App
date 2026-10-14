from playwright.sync_api import expect, sync_playwright

            
def test_floating_chatbot_opens(live_server):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        try:
            page = browser.new_page()
            response = page.goto(
                live_server.url,
                wait_until="domcontentloaded",
            )

            assert response is not None
            assert response.status == 200

            chat_button = page.locator("#chat-button")
            chat_window = page.locator("#chat-window")

            expect(chat_button).to_be_visible()
            expect(chat_window).to_be_hidden()

            chat_button.click()
            expect(chat_window).to_be_visible()
        finally:
            browser.close()


def test_chatbot_displays_mocked_reply(live_server):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        try:
            page = browser.new_page()
            page.goto(live_server.url, wait_until="domcontentloaded")

            page.locator("#chat-button").click()

            chat_input = page.locator("#chat-input")
            chat_input.fill("Hello Bojack")
            page.locator("#chat-send").click()

            expect(page.locator("#chat-log")).to_contain_text(
                "Mock reply to: 'Hello Bojack'",
                timeout=10_000,
            )
        finally:
            browser.close()


def test_chatbot_displays_html_input_as_text(live_server):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        try:
            page = browser.new_page()
            page.goto(live_server.url, wait_until="domcontentloaded")

            page.locator("#chat-button").click()

            payload = '<img src=x onerror="alert(1)">'
            page.locator("#chat-input").fill(payload)
            page.locator("#chat-send").click()

            user_message = page.locator(".user-msg").filter(has_text=payload)
            expect(user_message).to_be_visible()

            # The submitted content must not create an actual image element.
            expect(user_message.locator("img")).to_have_count(0)

            # The message is echoed by the mock, so the reply should also
            # display the original payload as plain text.
            expect(page.locator("#chat-log")).to_contain_text(
                payload,
                timeout=10_000,
            )
        finally:
            browser.close()

def test_chatbot_handles_server_error(live_server):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        try:
            page = browser.new_page()
            page.goto(live_server.url, wait_until="domcontentloaded")

            page.locator("#chat-button").click()

            def fail_chat_request(route):
                route.fulfill(
                    status=500,
                    content_type="application/json",
                    body='{"error": "Simulated server error"}',
                )

            page.route("**/chatbot/get-response/", fail_chat_request)

            page.locator("#chat-input").fill("Hello Bojack")
            page.locator("#chat-send").click()

            chat_log = page.locator("#chat-log")

            expect(chat_log).to_contain_text(
                "Bojack is having an existential crisis. Please try again later.",
                timeout=10_000,
            )

            expect(chat_log).not_to_contain_text("Bojack is Thinking...")
        finally:
            browser.close()