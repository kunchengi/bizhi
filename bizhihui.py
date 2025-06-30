import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

# 配置 Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.bizhihui.com/fengjing/')

# 滚动页面，加载更多壁纸
for i in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 等待加载

# 获取ul元素
ul = driver.find_element(By.ID, "item-lists")
li_list = ul.find_elements(By.CSS_SELECTOR, "li.item-list.masonry-brick")

img_urls = []
for li in li_list:
    a_tag = li.find_element(By.CSS_SELECTOR, "a.item-img")
    img_tag = a_tag.find_element(By.TAG_NAME, "img")
    src = img_tag.get_attribute("src")
    if src:
        # 去掉-pcthumbs
        img_url = src.replace("-pcthumbs", "")
        img_urls.append(img_url)

driver.quit()

# 创建images文件夹
os.makedirs("images", exist_ok=True)

# 下载图片
for url in tqdm(img_urls, desc="Downloading images"):
    filename = url.split("/")[-1]
    filepath = os.path.join("images", filename)
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(resp.content)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

print("下载完成！共下载：", len(img_urls), "张壁纸")