from base import *


def payment_gku_in_moscow(data):
    """Проверка формы оплаты ЖКУ в Москве"""

    with pytest.allure.step("Открытие главной страницы"):
        driver.get(data['url'])
        assert driver.current_url == data['url'], "Открыт некорректный адрес"
        assert driver.find_elements_by_class_name("TinkoffLogo__text_1OOMY")[1].text == "Тинькофф", "Название логотипа некорректно"

    with pytest.allure.step("Нажатие на пункт меню 'Платежи'"):
        wait.until(EC.element_to_be_clickable((By.XPATH, ".//span[@class='Text__text_6RrjC Text__text_size_13_3Mabb']//a[@href='/payments/']")))
        driver.find_element_by_xpath(".//span[@class='Text__text_6RrjC Text__text_size_13_3Mabb']//a[@href='/payments/']").click()
        time.sleep(0.5)
        assert driver.current_url == "https://www.tinkoff.ru/payments/", "Открыт некорректный адрес"

    with pytest.allure.step("Нажатие на пункт 'ЖКХ'"):
        wait.until(EC.element_to_be_clickable((By.XPATH, ".//*[@aria-label='ЖКХ']")))
        driver.find_element_by_xpath(".//*[@aria-label='ЖКХ']").click()
        assert driver.find_element_by_xpath(".//input[@type='text']").get_attribute('placeholder') == 'Название или ИНН получателя платежа'
        time.sleep(0.5)
        assert driver.current_url == "https://www.tinkoff.ru/payments/categories/kommunalnie-platezhi/", "Открыт некорректный адрес"

    with pytest.allure.step("Выбор региона “г. Москва” из списка регионов"):
        if driver.find_element_by_xpath(".//span[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']").text == 'Москве':
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//span[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']")))

        else:
            driver.find_element_by_xpath(".//span[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']").click()
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//*[contains(text(), '{}')]".format(str(data['region']))))).click()
            time.sleep(0.5)
            assert driver.find_element_by_xpath(".//span[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']").text == 'Москве'

    with pytest.allure.step("Выбор 1-го из списка поставщика услуг '{}'".format(str(data['provider']))):
        time.sleep(0.5)
        elements = driver.find_elements_by_xpath(".//ul[@data-qa-file='UIScrollList']//li[@class='UIMenu__item_xjvFc UIMenu__item_icons_2MY86']")
        time.sleep(0.5)
        assert elements[0].text == data['provider'], "Название 1-ого элемента не соответствует документации"
        elements[0].click()
        time.sleep(0.5)
        assert driver.find_elements_by_class_name("Tab__tab_2Ylcg")[1].text == 'ОПЛАТИТЬ ЖКУ В МОСКВЕ'
        time.sleep(0.5)
        assert driver.current_url == 'https://www.tinkoff.ru/zhku-moskva/', "Открыт некорректный адрес"

    with pytest.allure.step("Переход на вкладку 'Оплатить ЖКУ в Москве'"):
        wait.until(EC.element_to_be_clickable((By.XPATH, ".//a[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']"))).click()
        time.sleep(0.5)
        assert driver.find_element_by_class_name('ui-button__text').text == 'Оплатить ЖКУ в Москве'

    with pytest.allure.step("Ввод невалидных значений для обязательных полей"):
        wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='ui-button ui-button_failure ui-button_mobile-wide ui-button_provider-pay ui-button_size_xxl ui-form__button ui-button_inline']"))).click()
        elements = driver.find_elements_by_xpath(".//div[@class='ui-form__field']//div[@class='ui-form-field-error-message ui-form-field-error-message_ui-form']")
        for i in elements:
            assert i.text == "Поле обязательное"

        for i in data['provider-payerCode']:
            driver.find_element_by_name("provider-payerCode").send_keys(int(i))
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='ui-button ui-button_failure ui-button_mobile-wide ui-button_provider-pay ui-button_size_xxl ui-form__button ui-button_inline']"))).click()
            assert driver.find_elements_by_xpath(".//div[@class='ui-form__field']//div[@class='ui-form-field-error-message ui-form-field-error-message_ui-form']")[0].text == "Поле неправильно заполнено"
            driver.find_element_by_name("provider-payerCode").clear()

        for i in data['provider-period']:
            driver.find_element_by_name("provider-period").send_keys(int(i))
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='ui-button ui-button_failure ui-button_mobile-wide ui-button_provider-pay ui-button_size_xxl ui-form__button ui-button_inline']"))).click()
            assert driver.find_elements_by_xpath(".//div[@class='ui-form__field']//div[@class='ui-form-field-error-message ui-form-field-error-message_ui-form']")[1].text == "Поле заполнено некорректно"
            driver.find_element_by_name("provider-period").clear()

        for i in data['sum-payment-invalid']:
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr undefined Input__layout_background_kfMS7 Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0']")).send_keys(i)
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='ui-button ui-button_failure ui-button_mobile-wide ui-button_provider-pay ui-button_size_xxl ui-form__button ui-button_inline']"))).click()
            assert driver.find_elements_by_xpath(".//div[@class='ui-form__field']//div[@class='ui-form-field-error-message ui-form-field-error-message_ui-form']")[3].text == "Поле заполнено неверно"
            driver.find_elements_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0']"))[1].click()
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.CONTROL, "a")
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.BACKSPACE)
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr undefined Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_focused_2XyP-']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.ENTER)

        for i in data['sum-payment-min']:
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr undefined Input__layout_background_kfMS7 Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0']")).send_keys(i)
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='ui-button ui-button_failure ui-button_mobile-wide ui-button_provider-pay ui-button_size_xxl ui-form__button ui-button_inline']"))).click()
            assert driver.find_elements_by_xpath(".//div[@class='ui-form__field']//div[@class='ui-form-field-error-message ui-form-field-error-message_ui-form']")[2].text == "Минимум — 10 ₽"
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0']")).click()
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.CONTROL, "a")
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.BACKSPACE)
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr undefined Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_focused_2XyP-']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.ENTER)

        for i in data['sum-payment-max']:
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr undefined Input__layout_background_kfMS7 Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0']")).send_keys(i)
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='ui-button ui-button_failure ui-button_mobile-wide ui-button_provider-pay ui-button_size_xxl ui-form__button ui-button_inline']"))).click()
            assert driver.find_elements_by_xpath(".//div[@class='ui-form__field']//div[@class='ui-form-field-error-message ui-form-field-error-message_ui-form']")[2].text == "Максимум — 15 000 ₽"
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0']")).click()
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.CONTROL, "a")
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_error_2mQA4']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.BACKSPACE)
            driver.find_element_by_xpath((".//div[@class='Input__layout_2izQr undefined Input__layout_background_kfMS7 Input__layout_background_focused_1G_GD Input__layout_border_focused_2XyP-']//input[@class='Input__valueContent_1Os4v Input__valueContent_primary_3sxF0 undefined']")).send_keys(Keys.ENTER)

        with pytest.allure.step("Переход в пункт меню 'Платежи'"):
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//span[@class='Text__text_6RrjC Text__text_size_13_3Mabb']//a[@href='/payments/']")))
            driver.find_element_by_xpath(".//span[@class='Text__text_6RrjC Text__text_size_13_3Mabb']//a[@href='/payments/']").click()
            time.sleep(0.5)
            assert driver.current_url == "https://www.tinkoff.ru/payments/", "Открыт некорректный адрес"

        with pytest.allure.step("Поиск поставщика услуг"):
            driver.find_element_by_xpath(".//input[@class='Input__valueContent_1Os4v Input__valueContent_alone_2RBHi Input__valueContent_primary_3sxF0']").click()
            driver.find_element_by_xpath(".//input[@class='Input__valueContent_1Os4v Input__valueContent_alone_2RBHi Input__valueContent_primary_3sxF0']").send_keys(data['provider'])
            driver.find_element_by_xpath(".//input[@class='Input__valueContent_1Os4v Input__valueContent_alone_2RBHi Input__valueContent_primary_3sxF0']").send_keys(Keys.ENTER)
            time.sleep(0.5)
            assert driver.find_elements_by_xpath(".//div[@class='Grid__root_1nlgc Grid__root_display_block_lwIvG']//div[@class='Grid__column_3qcJA Grid__column_size_12_2AOcu Grid__column_sizeMobile_12_1mA7y']//div[@class='Text__text_1yBRv Text__text_size_17_3d9gC Text__text_sizeDesktop_17_2KUMp Text__text_overflowEllipsis_1VQlS']")[0].text == data['provider'], "Поставщик не соответствует искомому значению"
            driver.find_elements_by_xpath(".//div[@class='Grid__root_1nlgc Grid__root_display_block_lwIvG']//div[@class='Grid__column_3qcJA Grid__column_size_12_2AOcu Grid__column_sizeMobile_12_1mA7y']//div[@class='Text__text_1yBRv Text__text_size_17_3d9gC Text__text_sizeDesktop_17_2KUMp Text__text_overflowEllipsis_1VQlS']")[0].click()
            time.sleep(0.5)
            assert driver.find_elements_by_class_name("Tab__tab_2Ylcg")[1].text == 'ОПЛАТИТЬ ЖКУ В МОСКВЕ'
            time.sleep(0.5)
            assert driver.current_url == 'https://www.tinkoff.ru/zhku-moskva/', "Открыт некорректный адрес"

        with pytest.allure.step("Переход в пункт меню 'Платежи'"):
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, ".//span[@class='Text__text_6RrjC Text__text_size_13_3Mabb']//a[@href='/payments/']")))
            driver.find_element_by_xpath(
                ".//span[@class='Text__text_6RrjC Text__text_size_13_3Mabb']//a[@href='/payments/']").click()
            time.sleep(0.5)
            assert driver.current_url == "https://www.tinkoff.ru/payments/", "Открыт некорректный адрес"

        with pytest.allure.step("Нажатие на пункт 'ЖКХ'"):
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//*[@aria-label='ЖКХ']")))
            driver.find_element_by_xpath(".//*[@aria-label='ЖКХ']").click()
            assert driver.find_element_by_xpath(".//input[@type='text']").get_attribute('placeholder') == 'Название или ИНН получателя платежа'
            time.sleep(0.5)
            assert driver.current_url == "https://www.tinkoff.ru/payments/categories/kommunalnie-platezhi/", "Открыт некорректный адрес"

        with pytest.allure.step("Выбор региона “г. Санкт-Петербург” из списка регионов"):
            if driver.find_element_by_xpath(".//span[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']").text == 'Санкт-Петербурге':
                wait.until(EC.element_to_be_clickable((By.XPATH,".//span[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']")))

            else:
                driver.find_element_by_xpath(".//span[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']").click()
                wait.until(EC.element_to_be_clickable((By.XPATH, ".//*[contains(text(), '{}')]".format(str('г. Санкт-Петербург'))))).click()
                time.sleep(0.5)
                assert driver.find_element_by_xpath(".//span[@class='Link__link_3805p Link__link_color_blue_10po6 Link__link_type_simple_l_2v_ Link__link_nodecorated_2q71R']").text == 'Санкт-Петербурге'

            elements = driver.find_elements_by_xpath(".//ul[@data-qa-file='UIScrollList']//li[@class='UIMenu__item_xjvFc UIMenu__item_icons_2MY86']")
            for i in elements:
                assert i.text != data['provider'], "В списке присутствует поставщик услуг из другой локации"

        driver.close()
        driver.quit()
        driver.start_client()
