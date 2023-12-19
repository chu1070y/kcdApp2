from time import sleep
from datetime import date, timedelta
from scrap.scrap_base import ScrapBase

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException


class KakaoPlace(ScrapBase):
    def place_scrap(self, place_info):
        self.logger.info('Start to scrap kakao place')
        place_id = str(place_info[2])

        ##### 카카오 플레이스 접속
        url = "https://place.map.kakao.com/{}".format(place_id)
        self.driver.get(url)
        sleep(1)

        ##### 데이터 추출
        place_name = place_info[0]

        try:
            place_contact = self.driver.find_element(By.CLASS_NAME, "txt_contact").text
        except NoSuchElementException as e:
            place_contact = None
        
        try:
            place_address = self.driver.find_element(By.CLASS_NAME, "txt_address").text
        except NoSuchElementException as e:
            place_address = None

        try:
            place_description = self.driver.find_element(By.CLASS_NAME, "txt_introduce").text
        except NoSuchElementException as e:
            place_description = None

        try:
            place_score = self.driver.find_element(By.XPATH, "//em[@class='num_rate']").text.replace('점', '')
        except NoSuchElementException as e:
            place_score = None

        return {
            "service_code": "KP",
            "place_name": place_name,
            "place_contact": place_contact,
            "place_address": place_address,
            "place_description": place_description,
            "place_score": place_score
        }

    def review_scrap(self, place_info, mode='daily'):
        place_id = str(place_info[2])

        ##### 카카오 플레이스 접속
        url = "https://place.map.kakao.com/{}".format(place_id)
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
            review_elements = self.driver.find_elements(By.XPATH, "//ul[@class='list_evaluation']/li")

            if len(review_elements) == 0:
                break

            for e in review_elements[prev_review_count:]:
                prev_review_count += 1

                review_author = e.find_element(By.CLASS_NAME, "link_user").text
                review_score = e.find_elements(By.CLASS_NAME, "txt_desc")[-1].text
                review_comment = e.find_element(By.CLASS_NAME, "txt_comment").find_element(By.TAG_NAME, 'span').text.encode().decode().replace("\x00", "")

                review_date = e.find_element(By.CLASS_NAME, "time_write").text.split('.')[:-1]
                review_date = [int(x) for x in review_date]
                review_date = date(year=review_date[0], month=review_date[1], day=review_date[2])

                if review_date >= base_date and review_date != date.today():
                    tmp = {
                        "review_author": review_author,
                        "review_score": review_score,
                        "review_comment": review_comment,
                        "review_date": str(review_date)
                    }
                    reviews.append(tmp)

                elif review_date < base_date:
                    r_flag = 1
                    break

            try:
                self.driver.find_element(By.XPATH, "//div[@data-viewid='comment']//a[@class='link_more']").click()
                sleep(1)

            except NoSuchElementException as e:
                self.logger.info("There is no '더보기' button on review list")
                r_flag = 1

        return reviews


if __name__ == "__main__":
    result = KakaoPlace().place_scrap(['국수나무 경산중산점', 1751155505, 1667217868])
    # result = KakaoPlace().review_scrap(['국수나무 경산중산점', 1751155505, 1667217868], 'init')

    print(result)
