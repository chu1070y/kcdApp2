def place_sql():
    return {
        "get_place_info": "select place_name, naver_place_id, kakao_place_id from scrap.t_scrap_place_info where place_name=%s",
        "status_i": "insert into scrap.t_scrap_place_log (operation, place_name, scrap_status, scrap_timestamp, ins_user) values (%s, %s, 'I', %s, 'app')",
        "status_s": "update scrap.t_scrap_place_log set scrap_status = 'S', upd_user = 'app', upd_timestamp = now() where place_name = %s and scrap_timestamp = %s",
        "status_f": "update scrap.t_scrap_place_log set scrap_status = 'F', sqs_message = %s, upd_user='app', upd_timestamp = now() where place_name = %s and scrap_timestamp = %s",
        "insert_place": """insert into scrap.t_scrap_place 
                            (service_code, place_name, place_contact, place_address, place_description,
                                place_score, scrap_timestamp) values 
                            (%(service_code)s, %(place_name)s, %(place_contact)s, %(place_address)s, %(place_description)s,
                                %(place_score)s, %(scrap_timestamp)s
                            ) on conflict (service_code, place_name)
                            do update
                            set place_contact = excluded.place_contact,
                                place_address = excluded.place_address,
                                place_description = excluded.place_description,
                                place_score = excluded.place_score,
                                scrap_timestamp = excluded.scrap_timestamp""",
        "insert_place_review": """
                        insert into scrap.t_scrap_place_review
                        (service_code, place_name, review_date, review_author, review_score, review_comment, scrap_timestamp) values
                        (%(service_code)s, %(place_name)s, %(review_date)s, %(review_author)s, %(review_score)s, %(review_comment)s, %(scrap_timestamp)s)
                        on conflict (service_code, place_name, review_date, review_author)
                        do update
                        set review_score = excluded.review_score,
                            review_comment = excluded.review_comment,
                            scrap_timestamp = excluded.scrap_timestamp
        """
    }


