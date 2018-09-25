import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# url链接
url ="https://s.taobao.com/search?q=%E5%84%BF%E7%AB%A5%E6%" \
     "88%BF&imgfile=&js=1&stats_click=search_radio_all%3A1&in" \
     "itiative_id=staobaoz_20180923&ie=utf8"

# 设置无界面运行
# option = Options()
# option.add_argument("--headless")
# driver = webdriver.Chrome(chrome_options=option)
# selenium加载全部网页信息
# driver.get(url=url)
# script = "window.scrollTo(0,document.scrollHeight);"
# driver.execute_script(script)
# 源码内容
# content = driver.page_source
# print(content)

req = requests.get(url=url,headers={"User-Agent":"Mozilla/5.0 (X1"
            "1; Linux x86_64) AppleWebKit/537.36 (KHTML, like G"
                    "ecko) Chrome/66.0.3359.181 Safari/537.36"})
print(req.text)

