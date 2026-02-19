from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import os


def scrape_articles(driver, test_name="MAIN"):
    wait = WebDriverWait(driver, 20)

    print(f"[{test_name}] Opening El País...")
    driver.get("https://elpais.com/")

    # Accept cookies if present
    try:
        accept_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Aceptar') or contains(., 'Accept')]")
            )
        )
        accept_btn.click()
        print(f"[{test_name}] Cookie accepted")
    except TimeoutException:
        print(f"[{test_name}] No cookie banner")

    print(f"[{test_name}] Navigating to Opinion section...")

    opinion_link = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href,'opinion')]")
        )
    )

    driver.execute_script("arguments[0].click();", opinion_link)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))

    print(f"[{test_name}] Opinion page loaded")

    # Collect article URLs first (avoids stale references)
    articles = driver.find_elements(By.TAG_NAME, "article")[:5]
    article_links = []

    for article in articles:
        try:
            link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
            if link:
                article_links.append(link)
        except:
            continue

    titles = []

    if not os.path.exists("images"):
        os.makedirs("images")

    # Visit each article separately
    for index, link in enumerate(article_links):
        try:
            driver.get(link)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

            title = driver.find_element(By.TAG_NAME, "h1").text.strip()
            titles.append(title)

            print(f"\n[{test_name}] Article {index+1} Title (Spanish): {title}")

            paragraphs = driver.find_elements(By.TAG_NAME, "p")
            content = "\n".join([p.text for p in paragraphs if p.text])

            print(f"[{test_name}] Content Preview:")
            print(content[:400])
            print("--------------------------------------------------")

            # Download first image if available
            try:
                image = driver.find_element(By.TAG_NAME, "img")
                img_url = image.get_attribute("src")

                if img_url and img_url.startswith("http"):
                    img_data = requests.get(img_url, timeout=10).content
                    with open(f"images/article_{index+1}.jpg", "wb") as f:
                        f.write(img_data)
                    print(f"[{test_name}] Image saved")
            except:
                print(f"[{test_name}] No image found")

        except Exception as e:
            print(f"[{test_name}] Error processing article {index+1}: {e}")

    return titles
