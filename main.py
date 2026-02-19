# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from src.scraper import scrape_articles
# from src.translator import translate_titles
# from src.text_analyzer import analyze_words

# def run_local():
#     options = Options()
#     options.add_argument("--start-maximized")

#     driver = webdriver.Chrome(options=options)

#     titles = scrape_articles(driver)
#     translated = translate_titles(titles)
#     analyze_words(translated)

#     driver.quit()

# if __name__ == "__main__":
#     run_local()

from src.browserstack_runner import execute_parallel

if __name__ == "__main__":
    execute_parallel()

