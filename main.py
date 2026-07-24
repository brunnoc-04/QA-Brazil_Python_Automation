import time

import data
import helpers

from pages import UrbanRoutesPage
from helpers import retrieve_phone_code
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = Chrome()
        cls.driver.implicitly_wait(5)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)


    def test_set_route(self):
        assert self.page.get_from_location() == data.ADDRESS_FROM
        assert self.page.get_to_location() == data.ADDRESS_TO


    def test_select_plan(self):
        self.page.click_taxi_option()
        self.page.click_icon_comfort_selected()
        assert self.page.is_comfort_icon_active()


    def test_fill_phone_number(self):
        # Passos necessários para chegar na tela de telefone
        self.page.click_taxi_option()
        self.page.click_icon_comfort_selected()

        # Abre o popup do telefone
        self.page.click_phone_number_button()

        # Digita o número de telefone
        self.page.enter_phone_number(data.PHONE_NUMBER)

        # Clica em Próximo para enviar o SMS
        self.page.click_phone_number_next_button()

        # Recupera o código SMS interceptando os logs do Chrome
        code = helpers.retrieve_phone_code(self.driver)
        self.page.enter_phone_code(code)

        # Confirma o código
        self.page.click_phone_code_confirm_button()

        # Valida que o número foi preenchido
        assert data.PHONE_NUMBER in self.page.get_phone_button_text()


    def test_fill_card(self):
        # Passos necessários para chegar na tela de pagamento
        self.page.click_taxi_option()
        self.page.click_icon_comfort_selected()

        # Abre o modal de metodo de pagamento
        self.page.click_payment_method_button()
        time.sleep(1)

        # Clica em Adicionar cartão
        self.page.click_add_card_option()
        time.sleep(1)

        # Digita o número do cartão
        self.page.enter_card_number(data.CARD_NUMBER)
        time.sleep(1)

        # Digita o CVV do cartão
        self.page.enter_card_code(data.CARD_CODE)

        # Pressiona Tab para tirar o foco do CVV
        self.page.click_outside_card_code()

        # Clica em Adicionar
        self.page.click_add_card_button()

        # Valida que o metodo de pagamento mudou
        assert "Cartão" in self.page.get_payment_method_value()


    def test_comment_for_driver(self):
        # Passos necessários para chegar na tela
        self.page.click_taxi_option()
        self.page.click_icon_comfort_selected()

        # Digita a mensagem para o motorista
        self.page.enter_message_for_driver(data.MESSAGE_FOR_DRIVER)

        # Valida que a mensagem foi digitada
        assert self.page.get_message_for_driver_value() == data.MESSAGE_FOR_DRIVER



    def test_order_blanket_and_handkerchiefs(self):
        # Passos necessários para chegar na tela
        self.page.click_taxi_option()
        self.page.click_icon_comfort_selected()

        # Clica no toggle de cobertor e lençóis
        self.page.click_blanket_switch()
        time.sleep(1)

        # Verifica se o toggle foi ativado
        assert self.page.is_blanket_selected() == True

    def test_order_2_ice_creams(self):
        numbers_of_ice_creams = 2

        # Passos necessários para chegar na tela
        self.page.click_taxi_option()
        self.page.click_icon_comfort_selected()

        # Clica no botão + duas vezes para pedir 2 sorvetes
        for count in range(numbers_of_ice_creams):
            self.page.click_ice_cream_plus()
            time.sleep(0.5)

        # Verifica se o contador mostra 2
        assert self.page.get_ice_cream_count() == "2"


    def test_car_search_model_appears(self):
        self.page.click_taxi_option()
        self.page.click_icon_comfort_selected()

        # Telefone
        self.page.click_phone_number_button()
        self.page.enter_phone_number(data.PHONE_NUMBER)
        self.page.click_phone_number_next_button()
        code = retrieve_phone_code(self.page.driver)
        self.page.enter_phone_code(code)
        self.page.click_phone_code_confirm_button()
        time.sleep(1)

        # Cartão de crédito
        self.page.click_payment_method_button()
        time.sleep(1)
        self.page.click_add_card_option()
        time.sleep(1)
        self.page.enter_card_number(data.CARD_NUMBER)
        time.sleep(1)
        self.page.enter_card_code(data.CARD_CODE)
        self.page.click_outside_card_code()
        self.page.click_add_card_button()
        time.sleep(3)
        self.page.close_payment_modal()
        time.sleep(1)

        # Mensagem para o motorista
        self.page.enter_message_for_driver(data.MESSAGE_FOR_DRIVER)

        # Cobertor e lençóis
        self.page.click_blanket_switch()
        time.sleep(1)

        # 2 sorvetes
        for count in range(2):
            self.page.click_ice_cream_plus()
            time.sleep(0.5)

        # Clica em Pedir
        self.page.click_order_taxi()
        time.sleep(3)

        # Verifica se o modal "Buscar carro" apareceu
        assert self.page.is_search_modal_visible() == True


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
