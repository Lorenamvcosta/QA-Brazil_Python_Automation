import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage
import time


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):

        self.driver.get(data.URBAN_ROUTES_URL)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        assert routes_page.get_from_location_value() == data.ADDRESS_FROM
        assert routes_page.get_to_location_value() == data.ADDRESS_TO

    def test_select_plan(self):

        self.driver.get(data.URBAN_ROUTES_URL)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        routes_page.click_taxi_option()

        time.sleep(2)

        routes_page.select_comfort_plan()

        assert routes_page.is_comfort_selected()

    def test_fill_phone_number(self):

        self.driver.get(data.URBAN_ROUTES_URL)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        routes_page.click_taxi_option()

        routes_page.select_comfort_plan()

        routes_page.fill_phone_number(
            data.PHONE_NUMBER
        )

        assert data.PHONE_NUMBER in routes_page.get_phone_number()

    def test_fill_card(self):

        self.driver.get(data.URBAN_ROUTES_URL)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        routes_page.click_taxi_option()

        routes_page.select_comfort_plan()

        routes_page.fill_phone_number(
            data.PHONE_NUMBER
        )

        routes_page.fill_card(
            data.CARD_NUMBER,
            data.CARD_CODE
        )

        assert "Cartão" in routes_page.get_payment_method()

    def test_comment_for_driver(self):

        self.driver.get(data.URBAN_ROUTES_URL)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        routes_page.click_taxi_option()

        routes_page.select_comfort_plan()

        routes_page.add_driver_comment(
            data.MESSAGE_FOR_DRIVER
        )

        assert routes_page.get_driver_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):

        self.driver.get(data.URBAN_ROUTES_URL)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        routes_page.click_taxi_option()

        routes_page.select_comfort_plan()

        routes_page.switch_cobertor()

        assert routes_page.switch_cobertor_active() is True

    def test_order_2_ice_creams(self):

        self.driver.get(data.URBAN_ROUTES_URL)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        routes_page.click_taxi_option()

        routes_page.select_comfort_plan()

        routes_page.add_2_ice_creams()

        assert routes_page.get_ice_cream_quantity() == "2"

    def test_car_search_model_appears(self):

        self.driver.get(data.URBAN_ROUTES_URL)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        routes_page.click_taxi_option()

        routes_page.select_comfort_plan()

        routes_page.switch_cobertor()

        routes_page.fill_phone_number(
            data.PHONE_NUMBER
        )

        routes_page.fill_card(
            data.CARD_NUMBER,
            data.CARD_CODE
        )

        routes_page.add_driver_comment(
            data.MESSAGE_FOR_DRIVER
        )

        routes_page.add_2_ice_creams()

        routes_page.call_taxi()

        time.sleep(5)

        assert routes_page.get_pop_up() != ""

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
