from base import Base
from module.aws import SQS

import json
from time import sleep


class Main(Base):
    def process(self):
        sqs = SQS()

        try:
            while True:
                # 메세지 컨슘
                msg = sqs.consume()

                if not msg:
                    self.logger.info('Waiting for getting message from SQS')
                    sleep(1)
                    continue

                msg = msg[0]
                msg.delete()
                body = json.loads(msg.body)

                # operation에 따른 동작
                if body['operation'] == 'place_all':
                    from service.place import Place
                    Place().process(body, 'npnrkpkr')

                elif body['operation'] == 'place_naver_all':
                    from service.place import Place
                    Place().process(body, 'npnr')

                elif body['operation'] == 'place_kakao_all':
                    from service.place import Place
                    Place().process(body, 'kpkr')

                elif body['operation'] == 'place_naver_place':
                    from service.place import Place
                    Place().process(body, 'np')

                elif body['operation'] == 'place_naver_review':
                    from service.place import Place
                    Place().process(body, 'nr')

                elif body['operation'] == 'place_kakao_place':
                    from service.place import Place
                    Place().process(body, 'kp')

                elif body['operation'] == 'place_kakao_review':
                    from service.place import Place
                    Place().process(body, 'kr')

                else:
                    self.logger.info('Unknown operation - {}'.format(body['operation']))

        except Exception as e:
            # 알람 설정
            raise e


if __name__ == '__main__':
    from module.custom_log import CustomLog
    CustomLog('kcd')

    Main().process()

