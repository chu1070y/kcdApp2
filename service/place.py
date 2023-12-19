from base import Base

from sql.place_sql import place_sql
from module.dbconn import Postgres

from datetime import datetime

from scrap.naver_place import NaverPlace
from scrap.kakao_place import KakaoPlace


class Place(Base):
    def __init__(self):
        super().__init__()
        pg = Postgres()
        self.conn = pg.conn
        self.cursor = pg.cursor
        self.scrap_time = datetime.now()

    def process(self, body, action):
        self.logger.info('Getting message from SQS \n\t >>> {}'.format(body))

        # 작업 진행 중 상태 저장
        self.status_job('InProgress', body)

        # DB 접속해서 id값 가져오기
        place_info = self.get_id(body)

        if not place_info:
            self.logger.error('There is no id value on t_place_info')
            self.status_job('Failed', body)
            # 알람 설정
            return
        else:
            place_info = place_info[0]

        # 스크래핑
        try:
            place_data = []
            review_data = []
            
            # 네이버 플레이스
            if 'n' in action:
                naver = NaverPlace()

                if 'np' in action:
                    n_place = naver.place_scrap(place_info)
                    n_place['scrap_timestamp'] = self.scrap_time

                    place_data.append(n_place)

                if 'nr' in action:
                    n_place_review = naver.review_scrap(place_info, body.get('mode'))

                    for i in n_place_review:
                        i['service_code'] = 'NP'
                        i['place_name'] = body['key']
                        i['scrap_timestamp'] = self.scrap_time

                        review_data.append(i)
            
            # 카카오 플레이스
            if 'k' in action:
                kakao = KakaoPlace()

                if 'kp' in action:
                    k_place = kakao.place_scrap(place_info)
                    k_place['scrap_timestamp'] = self.scrap_time

                    place_data.append(k_place)

                if 'kr' in action:
                    k_place_review = kakao.review_scrap(place_info, body.get('mode'))

                    for j in k_place_review:
                        j['service_code'] = 'KP'
                        j['place_name'] = body['key']
                        j['scrap_timestamp'] = self.scrap_time

                        review_data.append(j)

            # naver = NaverPlace()
            # kakao = KakaoPlace()
            #
            # n_place = naver.place_scrap(place_info)
            # k_place = kakao.place_scrap(place_info)
            #
            # n_place_review = naver.review_scrap(place_info, body.get('mode'))
            # k_place_review = kakao.review_scrap(place_info, body.get('mode'))
            #
            # n_place['scrap_timestamp'] = self.scrap_time
            # k_place['scrap_timestamp'] = self.scrap_time
            #
            # place_data = [n_place] + [k_place]
            # review_data = []
            #
            # for i in n_place_review:
            #     i['service_code'] = n_place['service_code']
            #     i['place_name'] = n_place['place_name']
            #     i['scrap_timestamp'] = self.scrap_time
            #
            #     review_data.append(i)
            #
            # for j in k_place_review:
            #     j['service_code'] = k_place['service_code']
            #     j['place_name'] = k_place['place_name']
            #     j['scrap_timestamp'] = self.scrap_time
            #
            #     review_data.append(j)

        except Exception as e:
            self.logger.error('Scraping failed...')
            self.logger.error(e)
            self.status_job('Failed', body)
            # 알람 설정
            return

        # DB 저장
        sql = place_sql()['insert_place']
        review_sql = place_sql()['insert_place_review']

        if place_data:
            self.cursor.executemany(sql, place_data)

        if review_data:
            self.cursor.executemany(review_sql, review_data)

        self.status_job('Success', body)

    def get_id(self, body):
        self.logger.info('Getting IDS from DB')
        sql = place_sql()['get_place_info']

        self.cursor.execute(sql, [body['key']])
        return self.cursor.fetchall()

    def status_job(self, status, body):
        self.logger.info('Status_job - {}'.format(status))

        if status == 'InProgress':
            sql = place_sql()['status_i']
            self.cursor.execute(sql, [body['operation'], body['key'], self.scrap_time])
            self.conn.commit()

        elif status == 'Success':
            sql = place_sql()['status_s']
            self.cursor.execute(sql, [body['key'], self.scrap_time])
            self.conn.commit()

        else:
            sql = place_sql()['status_f']
            self.cursor.execute(sql, [str(body), body['key'], self.scrap_time])
            self.conn.commit()
