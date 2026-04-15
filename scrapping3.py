from playwright.sync_api import sync_playwright
import os
import dotenv

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# প্লেউইটার শুরু
with sync_playwright() as p:
    # ব্রাউজার লঞ্চ (headless=False মানে ব্রাউজার দেখা যাবে)
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # ---------------------
    # LOGIN
    # ---------------------

    page.goto("https://app.airwork.ai/login")

    # সেলেনিয়ামের time.sleep(3) এর পরিবর্তে এখানে wait_for_timeout ব্যবহার করা হয়েছে
    page.wait_for_timeout(3000)

    # send_keys এর পরিবর্তে fill ব্যবহার করা হয়
    page.locator("[name='email']").fill(EMAIL)
    page.locator("[name='password']").fill(PASSWORD)

    page.locator("button[type='submit']").click()

    page.wait_for_timeout(5000)

    print("Login Successful")

    # ---------------------
    # COLLECT JOB LINKS
    # ---------------------

    # XPath এবং find_elements এর পরিবর্তে locator এবং all() ব্যবহার করা হয়েছে
    job_elements = page.locator("xpath=/html/body/div[2]/div/div/main/div/div/div/div[2]//a")

    job_links = []
    
    # এলিমেন্টের সংখ্যা বের করে লুপ চালানো হয়েছে
    count = job_elements.count()
    for i in range(count):
        # nth(i) দিয়ে নির্দিষ্ট এলিমেন্ট ধরা হয়েছে
        link = job_elements.nth(i).get_attribute("href")

        if link:
            job_links.append(link)

    print(f"Job links: {job_links}")

    print("Total jobs found:", len(job_links))

    # ---------------------
    # VISIT EACH JOB
    # ---------------------

    for link in job_links:

        print("Opening:", link)

        # লিংক হ্যান্ডেল করা (relative url হলে ফুল url বানানো)
        full_link = "https://app.airwork.ai" + link if link.startswith("/") else link
        page.goto(full_link)

        page.wait_for_timeout(1000)

        # ---------------------------- By ID -----------------------------------
        try:
            # .text এর পরিবর্তে .inner_text() ব্যবহার করা হয়েছে
            summary = page.locator("#job-summary").inner_text()
        except:
            summary = ""

        try:
            description = page.locator("#job-description").inner_text()
        except:
            description = ""

        # ---------------------------- By Others specific area -----------------------------------

        # Catchphrase (CSS Selector)
        try:
            # ব্যাকস্ল্যাশ (\) এস্কেপ করার জন্য ডাবল ব্যাকস্ল্যাশ (\\) ব্যবহার করা হয়েছে
            catchphrase = page.locator("div.flex.flex-1.flex-col.gap-0\\.5 p").inner_text()
        except:
            catchphrase = ""

        # Job title (CSS Selector)
        try:
            title = page.locator("div.flex.flex-1.flex-col.gap-0\\.5 h1").inner_text()
        except:
            title = ""

        # Salary (XPath)
        try:
            salary = page.locator("xpath=//span[text()='Salary range']/following::span[1]").inner_text()
        except:
            salary = ""
        
        # Job type (XPath)
        try:
            job_type = page.locator("xpath=//span[text()='Type']/following::span[1]").inner_text()
        except:
            job_type = ""

        # Job nature (XPath)
        try:
            job_nature = page.locator("xpath=//span[text()='Nature']/following::span[1]").inner_text()
        except:
            job_nature = ""

        print("Catchphrase:", catchphrase)
        print("Title:", title)
        print("Salary:", salary)
        print("Type:", job_type)
        print("Nature:", job_nature)
        print("Summary:", summary)
        # print("Description:", description)
        print("----------------------")

    browser.close()