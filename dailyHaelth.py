from time import sleep
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from PIL import Image
from pytesseract import pytesseract
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge.service import Service


def pic_to_str(): # 获取验证码
    image = Image.open("code.png")
    pix = image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b, k = pix[i, j]
            if g >= 46 and g < 132 and g >= r + 15 and g >= b + 10:
                pix[i, j] = (0, 0, 0)
            else:
                pix[i,j] = (255,255,255)
    image.save("code2.png")
    result = pytesseract.image_to_string(image,lang="eng",config=\
                                "--psm 6 --oem 3 -c tessdit_char_whitelist=0123456789").strip()
    # print(s)
    return result

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML,likeGecko)Chrome/63.0.3239.132Safari/537.36"
    }
    s = Service("D:\\python project\\Bilibili\\msedgedriver.exe")
    driver = webdriver.Edge(service=s)
    driver.get("https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin")

    username = ""   # enter your username(e.g PB...)
    password = ""   # enter your passwd

    usr = driver.find_element(By.ID,'username')
    usr.send_keys(username)

    pwd = driver.find_element(By.ID, "password")
    pwd.send_keys(password)

    try:
        img = driver.find_element(By.CLASS_NAME,"validate-img")
        img.screenshot("code.png")
        result = pic_to_str()
        print(result)
        input_box = driver.find_element(By.ID,"validate")
        input_box.send_keys(result)
    except NoSuchElementException:
        print("无验证码!")

    driver.find_element(By.ID,"login").click()
    driver.implicitly_wait(5)

    sleep(2)
    button = driver.find_element(By.ID,"report-submit-btn-a24").click()

    sleep(2)
    html = str(driver.page_source)
    print(re.findall("alert-success\">(.+?)<a href", html)[0])
    driver.quit()

