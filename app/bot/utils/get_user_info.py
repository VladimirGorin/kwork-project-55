from script.utils.db.models.info import InfoController, InfoModel
from script.utils.db.models.ads import AdsController, AdsModel


def get(user_info: InfoModel, ads_controller: AdsController, info_controller: InfoController):

    user_info_result = info_controller.get_user_info('''SELECT place, max_price, max_days, from_time, to_time
           FROM users_info WHERE owner_id = ?;''', (str(user_info.owner_id),))

    user_ads_result = ads_controller.get_ads(
        '''SELECT status FROM ads WHERE owner_id = ?;''', (str(user_info.owner_id),), "all")

    if user_info_result:
        user_info.place = user_info_result[0]
        user_info.max_price = user_info_result[1]
        user_info.max_days = user_info_result[2]
        user_info.from_time = user_info_result[3]
        user_info.to_time = user_info_result[4]

        ads_info = "Нет объявлений для данного пользователя."
        ads_status_count = {'0': 0, '1': 0, '2': 0}

        if user_ads_result:
            for result in user_ads_result:
                status = str(result[0])

                if status in ads_status_count:
                    ads_status_count[status] += 1

            ads_info = f"Всего объяв: {len(user_ads_result)}\nСтатус ваших объяв.:{ads_status_count['1']} (в работе) {ads_status_count['0']} (выключено) {ads_status_count['2']} (ошибка)"

        mix_string = f"{ads_info}\n\nМесто: {user_info.place}\nДни работы: {user_info.max_days}\nВремя работы в день: {user_info.from_time} {user_info.to_time}\nМакс ставка: {user_info.max_price}"

        return mix_string
    else:
        return None
