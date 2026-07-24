from html.parser import commentclose

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

class UrbanRoutesPage:

    # Seção De e Para
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Fluxo de chamada de taxi
    taxi_option = (By.XPATH, '//button[contains(text(),"Chamar")]')
    comfort_icon = (By.XPATH, '//img[contains(@src,"kids")]')
    comfort_active = (By.XPATH, '//div[contains(@class, "tcard") and contains(@class, "active")]')

    # Telefone
    phone_number_button = (By.XPATH, '//div[contains(@class, "np-button")]')
    phone_number_field = (By.XPATH, '//input[@id="phone"]')
    phone_number_next_button = (By.XPATH, '//button[contains(text(), "Próximo")]')
    phone_code_field = (By.XPATH, '//input[@id="code"]')
    phone_code_confirm_button = (By.XPATH, '//button[contains(text(), "Confirmar")]')
    phone_number_button_text = (By.XPATH, '//div[contains(@class, "np-button")]//div[contains(@class, "np-text")]')

    # Cartão de Crédito
    payment_method_button = (By.XPATH, '//div[contains(@class, "pp-button") and .//div[contains(text(), "Método de pagamento")]]')
    add_card_option = (By.XPATH, '//div[contains(@class, "pp-title") and contains(text(), "Adicionar cartão")]')
    card_number_field = (By.XPATH, '//input[@id="number"]')
    card_code_field = (By.XPATH, '//input[contains(@class, "card-input")]')
    add_card_button = (By.XPATH, '//button[@type="submit" and contains(text(), "Adicionar")]')
    payment_method_value_text = (By.XPATH, '//div[contains(@class, "pp-value-text")]')
    close_payment_button = (By.CSS_SELECTOR, '.close-button.section-close')

    # Mensagem para o motorista
    message_for_driver_field = (By.XPATH, '//input[@id="comment"]')

    # Cobertor e lençóis
    blanket_switch = (By.XPATH, '//div[@class="r-sw-label" and contains(text(), "Cobertor")]/following-sibling::div[@class="r-sw"]//span[contains(@class, "slider")]')
    blanket_checkbox = (By.XPATH, '//div[@class="r-sw-label" and contains(text(), "Cobertor")]/following-sibling::div[@class="r-sw"]//input[@class="switch-input"]')

    # Sorvete
    ice_cream_plus_button = (By.XPATH,'//div[@class="r-counter-label" and text()="Sorvete"]/following-sibling::div[@class="r-counter"]//div[@class="counter-plus"]')
    ice_cream_counter_value = (By.XPATH,'//div[@class="r-counter-label" and text()="Sorvete"]/following-sibling::div[@class="r-counter"]//div[@class="counter-value"]')

    # Botão Pedir (final)
    order_taxi_button = (By.XPATH, '//button[contains(., "Pedir")]')

    # Modal de busca de carro
    search_car_modal = (By.XPATH, '//*[contains(text(),"Buscar carro")]')


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

#Métodos Core POM

    def _find(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def _click(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def _type(self, locator, text):
        element = self._find(locator)
        element.clear()
        element.send_keys(text)

#Endereço

    def _get_text(self, locator):
        return self._find(locator).text

    def _get_value(self, locator):
        return self._find(locator).get_attribute('value')

    def enter_locations(self, from_text, to_text):
        self._type(self.from_field, from_text)
        self._type(self.to_field, to_text)

    def get_from_location(self):
        return self._get_value(self.from_field)

    def get_to_location(self):
        return self._get_value(self.to_field)

    #Chamar Táxi

    def click_taxi_option(self):
        self.driver.find_element(*self.taxi_option).click()

    def click_icon_comfort_selected(self):
        self.driver.find_element(*self.comfort_icon).click()

    def is_comfort_icon_active(self):
        try:
            active_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.comfort_active)
            )
            return "active" in active_button.get_attribute("class")
        except:
            return False

    #Telefone

    def click_phone_number_button(self):
        self._click(self.phone_number_button)

    def enter_phone_number(self, phone_number):
        self._type(self.phone_number_field, phone_number)

    def click_phone_number_next_button(self):
     self._click(self.phone_number_next_button)

    def enter_phone_code(self, code):
        self._type(self.phone_code_field, code)

    def click_phone_code_confirm_button(self):
        self._click(self.phone_code_confirm_button)

    def get_phone_number_value(self):
        return self._get_value(self.phone_number_field)

    def get_phone_button_text(self):
        return self._get_text(self.phone_number_button_text)


    # Cartão de Crédito

    def click_payment_method_button(self):
        self._click(self.payment_method_button)

    def click_add_card_option(self):
        self._click(self.add_card_option)

    def enter_card_number(self, card_number):
        field = self._find(self.card_number_field)
        field.click()
        time.sleep(0.3)
        field.send_keys(card_number)

    def enter_card_code(self, card_code):
        # Navega com Tab do campo do cartão para o campo CVV
        self._find(self.card_number_field).send_keys(Keys.TAB)
        time.sleep(0.5)
        # Digita o CVV no campo que agora está focado
        ActionChains(self.driver).send_keys(card_code).perform()

    def click_outside_card_code(self):
        # Tab para sair do CVV e habilitar o botão Adicionar
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        time.sleep(0.5)

    def click_add_card_button(self):
        self._click(self.add_card_button)

    def get_payment_method_value(self):
        return self._get_text(self.payment_method_value_text)

    def close_payment_modal(self):
        # Procura todos os botões de fechar e clica no que estiver visível
        buttons = self.driver.find_elements(By.CSS_SELECTOR, '.close-button')
        for btn in buttons:
            if btn.is_displayed():
                btn.click()
                time.sleep(1)
                return

    # Mensagem para o motorista
    def enter_message_for_driver(self, message):
        self._type(self.message_for_driver_field, message)

    def get_message_for_driver_value(self):
        return self._find(self.message_for_driver_field).get_attribute("value")

    # Cobertor e lençóis
    def click_blanket_switch(self):
        self._click(self.blanket_switch)

    def is_blanket_selected(self):
        return self.driver.find_element(*self.blanket_checkbox).is_selected()

    # Sorvete
    def click_ice_cream_plus(self):
        self._click(self.ice_cream_plus_button)

    def get_ice_cream_count(self):
        return self._get_text(self.ice_cream_counter_value)

    # Botão Pedir e modal de busca
    def click_order_taxi(self):
        self._click(self.order_taxi_button)

    def is_search_modal_visible(self):
        try:
            self._find(self.search_car_modal)
            return True
        except:
            return False