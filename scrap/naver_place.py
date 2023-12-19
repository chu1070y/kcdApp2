import json
from time import sleep
from datetime import date, timedelta
from scrap.scrap_base import ScrapBase

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException


class NaverPlace(ScrapBase):
    def place_scrap(self, place_info):
        self.logger.info('Start to scrap naver place')
        place_id = str(place_info[1])

        ##### 네이버 플레이스 접속
        url = "https://pcmap.place.naver.com/place/{}/home".format(place_id)
        self.driver.get(url)
        sleep(1)
        current_url = self.driver.current_url

        scripts = self.driver.find_elements(By.TAG_NAME, "script")

        for script in scripts:
            data = script.get_attribute('innerHTML').strip()
            if data.startswith("var naver=typeof"):
                break

        ##### 데이터 파싱
        data = data.split('\n')[1].strip().replace('window.__APOLLO_STATE__ = ', '')[:-1]
        data = json.loads(data)

        if current_url.startswith("https://pcmap.place.naver.com/restaurant"):
            base = "RestaurantBase:" + place_id
        else:
            base = "PlaceBase:" + place_id

        place_name = place_info[0]
        place_contact = data[base]['virtualPhone'] if data[base]['phone'] is None else data[base]['phone']
        place_address = data[base]['roadAddress']
        place_description = data[base]['description']
        place_score = data[base]['visitorReviewsScore']

        return {
            "service_code": "NP",
            "place_name": place_name,
            "place_contact": place_contact,
            "place_address": place_address,
            "place_description": place_description,
            "place_score": place_score
        }
    
    # D-1일 리뷰 수집.. 수집 당일 리뷰 제외, 기준일 전 리뷰 제외
    def review_scrap(self, place_info, mode='daily'):
        place_id = str(place_info[1])

        url = "https://pcmap.place.naver.com/place/{}/review/visitor?reviewSort=recent".format(place_id)
        self.driver.get(url)
        sleep(1)

        if mode == 'init':
            base_date = date.today() - timedelta(days=2*365)
        else:
            base_date = date.today() - timedelta(days=1)

        reviews = []
        r_flag = 0
        prev_review_count = 0 ### 스크랩핑 당일 리뷰가 생길 수 있으므로 사용

        while r_flag == 0:
            review_elements = self.driver.find_elements(By.CLASS_NAME, "YeINN")

            if len(review_elements) == 0:
                break

            for e in review_elements[prev_review_count:]:
                prev_review_count += 1

                review_author = e.find_element(By.CLASS_NAME, "VYGLG").text

                try:
                    review_comment = e.find_element(By.CLASS_NAME, "zPfVt").text.encode().decode().replace("\x00", "")
                except Exception as ex:
                    review_comment = None

                review_date = e.find_element(By.CLASS_NAME, "tzZTd").find_element(By.TAG_NAME, "time").text.split('.')[:-1]

                if len(review_date) == 3:
                    review_date[0] = '20' + review_date[0]
                else:
                    review_date.insert(0, date.today().year)

                review_date = [int(x) for x in review_date]
                review_date = date(year=review_date[0], month=review_date[1], day=review_date[2])

                if review_date >= base_date and review_date != date.today():
                    tmp = {
                        "review_author": review_author,
                        "review_score": None,
                        "review_comment": review_comment,
                        "review_date": str(review_date)
                    }
                    reviews.append(tmp)

                elif review_date < base_date:
                    r_flag = 1
                    break

            try:
                self.driver.find_element(By.CLASS_NAME, "fvwqf").click()
                sleep(1)

            except NoSuchElementException as e:
                self.logger.info("There is no '더보기' button on review list")
                r_flag = 1

        return reviews


if __name__ == "__main__":
    result = NaverPlace().place_scrap(['바틀드', 1554507446, 1247290145])
    # result = NaverPlace().review_scrap(['바틀드', 1554507446, 1247290145], 'init')

    print(result)
