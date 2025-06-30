# 壁纸收集器

## 壁纸汇网站下载

### AI提示词

- 帮我写一个壁纸收集的脚本
  1. 打开https://www.bizhihui.com/fengjing/页面
  2. 该页面的壁纸是按需加载的，当滚动到页面最底部时，会加载更多壁纸，为了加载到足够的壁纸，你需要循环滚动到最底部50次，每次停留3秒，以保证壁纸加载完
  3. 获取该页面的id="item-lists"的元素，该元素是一个ul标签
  4. 遍历ul标签的所有class="item-list masonry-brick"的li标签，获取li标签里面的class="item-img"的a标签
  5. a标签里的img标签的src即为要获取的壁纸链接，要删除链接中的"-pcthumbs"后缀，然后将所有链接收集到数组中
  6. 循环遍历链接数组，将壁纸下载到images文件夹中

### 实现思路

1. 用 Selenium 自动打开网页并模拟滚动加载。
2. 等待页面加载，获取所有壁纸图片链接。
3. 处理链接，去掉 -pcthumbs 后缀。
4. 用 requests 下载图片到本地 images 文件夹。

### 实现步骤

1. 安装依赖

```bash
  pip install selenium requests tqdm
```

2. 下载 ChromeDriver

- 打开[ChromeDriver下载页面](https://developer.chrome.com/docs/chromedriver/downloads?hl=zh-cn)
- 下载与你的 Chrome 版本对应的 ChromeDriver。
- 解压后，将 chromedriver.exe 放到你的脚本所在目录，或者添加到系统 PATH。

3. 编写脚本代码

```python
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
```

4. 运行脚本

```bash
  python bizhi_collector.py
```