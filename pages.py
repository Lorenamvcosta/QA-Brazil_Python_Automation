from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import helpers
import time


class UrbanRoutesPage:

    # ==========================
    # ENDEREÇOS
    # ==========================

    from_field = (
        By.ID,
        "from"
    )

    to_field = (
        By.ID,
        "to"
    )

    # ==========================
    # BOTÃO CHAMAR UM TÁXI
    # ==========================

    taxi_option_locator = (
        By.CSS_SELECTOR,
        "#root > div > div.workflow > div.workflow-subcontainer > "
        "div.type-picker.shown > div.results-container > "
        "div.results-text > button"
    )

    # ==========================
    # TARIFA
    # ==========================

    # Não usamos mais nth-child(5).
    # Vamos procurar o card pelo texto "Comfort".
    comfort_cards_locator = (
        By.CSS_SELECTOR,
        "div.tcard"
    )

    # ==========================
    # TELEFONE
    # ==========================

    number_text_locator = (
        By.CSS_SELECTOR,
        ".np-button"
    )

    number_enter = (
        By.ID,
        "phone"
    )

    number_confirm = (
        By.CSS_SELECTOR,
        ".button.full"
    )

    number_code = (
        By.ID,
        "code"
    )

    code_confirm = (
        By.XPATH,
        "//button[contains(text(),'Confirmar')]"
    )

    number_finish = (
        By.CSS_SELECTOR,
        ".np-text"
    )

    # ==========================
    # CARTÃO
    # ==========================

    payment_method = (
        By.CSS_SELECTOR,
        ".pp-button"
    )

    add_card = (
        By.XPATH,
        "//div[text()='Adicionar cartão']"
    )

    card_number = (
        By.ID,
        "number"
    )

    card_code = (
        By.ID,
        "code"
    )

    add_button = (
        By.CSS_SELECTOR,
        ".pp-buttons button[type='submit']"
    )

    # ==========================
    # COMENTÁRIO PARA O MOTORISTA
    # ==========================

    add_comment = (
        By.ID,
        "comment"
    )

    # ==========================
    # REQUISITOS DO PEDIDO
    # ==========================

    requirements_header = (
        By.XPATH,
        "//div[contains(@class,'reqs-header') and "
        "normalize-space()='Requisitos do pedido']"
    )

    requirements_body = (
        By.CSS_SELECTOR,
        ".reqs-body"
    )

    # Texto do requisito
    blanket_label = (
        By.CSS_SELECTOR,
        ".r-sw-label"
    )

    call_taxi_button = (
        By.XPATH,
        "//button[contains(@class,'smart-button')][.//span[contains(@class,'smart-button-main') and normalize-space()='Pedir']]"
    )

    pop_up = (
        By.CSS_SELECTOR,
        ".order-header-title"
    )

    # ==========================
    # CONSTRUTOR
    # ==========================

    def __init__(self, driver):
        self.driver = driver

    # ==========================
    # ENDEREÇOS
    # ==========================

    def enter_from_location(self, from_text):

        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.from_field
            )
        )

        field.clear()
        field.send_keys(from_text)

    def enter_to_location(self, to_text):

        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.to_field
            )
        )

        field.clear()
        field.send_keys(to_text)

    def enter_locations(self, from_text, to_text):

        self.enter_from_location(from_text)
        self.enter_to_location(to_text)

    def get_from_location_value(self):

        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.from_field
            )
        ).get_attribute("value")

    def get_to_location_value(self):

        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.to_field
            )
        ).get_attribute("value")

    # ==========================
    # CHAMAR TÁXI
    # ==========================

    def click_taxi_option(self):

        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.taxi_option_locator
            )
        )

        button.click()

    # ==========================
    # COMFORT
    # ==========================

    def _get_comfort_card(self):

        """
        Procura o card que contém o texto Comfort.

        Não depende de nth-child porque a posição
        dos cards pode mudar.
        """

        cards = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                self.comfort_cards_locator
            )
        )

        for card in cards:

            if not card.is_displayed():
                continue

            texto = card.text.strip().lower()

            if "comfort" in texto:

                return card

        raise Exception(
            "Não foi encontrado o plano Comfort."
        )

    def click_comfort_icon(self):

        comfort = self._get_comfort_card()

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            comfort
        )

        WebDriverWait(self.driver, 10).until(
            lambda driver: comfort.is_displayed()
        )

        self.driver.execute_script(
            "arguments[0].click();",
            comfort
        )

    def is_comfort_selected(self):

        """
        Verifica especificamente se o card Comfort
        está com a classe active.
        """

        cards = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                self.comfort_cards_locator
            )
        )

        for card in cards:

            if not card.is_displayed():
                continue

            texto = card.text.strip().lower()

            if "comfort" in texto:

                classes = card.get_attribute("class") or ""

                return "active" in classes.split()

        return False

    def select_comfort_plan(self):

        """
        Seleciona Comfort somente se ainda não estiver
        selecionado.

        IMPORTANTE:
        Não chama is_comfort_selected() esperando que
        exista um .tcard.active global antes da seleção.
        """

        if not self.is_comfort_selected():

            self.click_comfort_icon()

            WebDriverWait(self.driver, 10).until(
                lambda driver: self.is_comfort_selected()
            )

    # ==========================
    # TELEFONE
    # ==========================

    def fill_phone_number(self, phone):

        # Abre a janela do telefone
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.number_text_locator
            )
        ).click()

        # Digita o telefone
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.number_enter
            )
        ).send_keys(phone)

        # Solicita o código SMS
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.number_confirm
            )
        ).click()

        # Recupera o código
        code = helpers.retrieve_phone_code(
            self.driver
        )

        # Digita o código
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.number_code
            )
        ).send_keys(code)

        # Confirma
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.code_confirm
            )
        ).click()

    def get_phone_number(self):

        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.number_finish
            )
        ).text

    # ==========================
    # CARTÃO
    # ==========================

    def fill_card(self, card, code):

        # Abre o método de pagamento
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.payment_method
            )
        ).click()

        # Clica em "Adicionar cartão"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.add_card
            )
        ).click()

        # Aguarda o formulário aparecer
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.card_number
            )
        )

        # Número do cartão
        numbers = self.driver.find_elements(
            *self.card_number
        )

        number = next(
            element
            for element in numbers
            if element.is_displayed()
        )

        number.click()
        number.clear()
        number.send_keys(card)

        # Código do cartão
        codes = self.driver.find_elements(
            *self.card_code
        )

        cvv = next(
            element
            for element in codes
            if element.is_displayed()
        )

        cvv.click()
        cvv.clear()
        cvv.send_keys(code)

        # Tira o foco
        cvv.send_keys(Keys.TAB)

        # Botão Adicionar
        button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.add_button
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

    def get_payment_method(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.payment_method
            )
        ).text

    # ==========================
    # COMENTÁRIO PARA O MOTORISTA
    # ==========================

    def add_driver_comment(self, message):

        comment = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.add_comment
            )
        )

        comment.clear()
        comment.send_keys(message)

    def get_driver_comment(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.add_comment
            )
        ).get_attribute("value")

    # ==========================
    # COBERTOR E LENÇÓIS
    # ==========================

    def _get_blanket_container(self):

        """
        Procura o requisito pelo TEXTO visível.

        Estrutura mostrada no DevTools:

        div.r-sw-container
            div.r-sw-label
                Cobertor e lençóis
            div.r-sw
                div.switch
                    input.switch-input
                    span.slider
        """

        labels = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                self.blanket_label
            )
        )

        for label in labels:

            if not label.is_displayed():
                continue

            texto = label.get_attribute(
                "textContent"
            ).strip()

            if texto == "Cobertor e lençóis":

                container = label.find_element(
                    By.XPATH,
                    "./parent::div[contains(@class,'r-sw-container')]"
                )

                return container

        raise Exception(
            "Não foi encontrado o requisito "
            "'Cobertor e lençóis' entre os elementos visíveis."
        )

    def switch_cobertor(self):

        print("=== PROCURANDO COBERTOR E LENÇÓIS ===")

        # Aguarda a área de requisitos
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.requirements_body
            )
        )

        container = self._get_blanket_container()

        print(
            "Requisito encontrado: "
            "'Cobertor e lençóis'"
        )

        # Garante que o requisito fique visível
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            container
        )

        # Pega o checkbox DENTRO do mesmo container
        checkbox = WebDriverWait(self.driver, 10).until(
            lambda driver: container.find_element(
                By.CSS_SELECTOR,
                "input.switch-input"
            )
        )

        print(
            "Estado antes do clique:",
            checkbox.is_selected()
        )

        # Só clica se ainda estiver desligado
        if not checkbox.is_selected():

            # Primeiro tenta clicar no checkbox diretamente
            try:

                self.driver.execute_script(
                    "arguments[0].click();",
                    checkbox
                )

            except Exception:

                # Caso o input esteja bloqueado pelo layout,
                # clica no slider visual.
                slider = container.find_element(
                    By.CSS_SELECTOR,
                    "span.slider"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    slider
                )

        # Confirma que ficou selecionado
        WebDriverWait(self.driver, 10).until(
            lambda driver:
            container.find_element(
                By.CSS_SELECTOR,
                "input.switch-input"
            ).is_selected()
        )

        print(
            "Cobertor e lençóis SELECIONADO!"
        )

    def switch_cobertor_active(self):

        """
        Retorna True se o checkbox de
        Cobertor e lençóis estiver selecionado.
        """

        container = self._get_blanket_container()

        checkbox = container.find_element(
            By.CSS_SELECTOR,
            "input.switch-input"
        )

        return checkbox.is_selected()

    def add_2_ice_creams(self):

        print("=== ADICIONANDO 2 SORVETES ===")

        # Localiza os itens de requisitos
        items = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    ".r-group-items > div"
                )
            )
        )

        sorvete = None

        for item in items:
            texto = item.text.strip().lower()

            if "sorvete" in texto:
                sorvete = item
                break

        if sorvete is None:
            raise Exception("Sorvete não encontrado.")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            sorvete
        )

        time.sleep(2)

        # Primeiro sorvete
        plus_button = sorvete.find_element(
            By.CSS_SELECTOR,
            ".counter-plus"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            plus_button
        )

        time.sleep(2)

        # Localiza NOVAMENTE o sorvete após a atualização do DOM
        items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    ".r-group-items > div"
                )
            )
        )

        sorvete = None

        for item in items:
            texto = item.text.strip().lower()

            if "sorvete" in texto:
                sorvete = item
                break

        if sorvete is None:
            raise Exception("Sorvete não encontrado após o primeiro clique.")

        # Segundo sorvete
        plus_button = sorvete.find_element(
            By.CSS_SELECTOR,
            ".counter-plus"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            plus_button
        )

        time.sleep(3)

        print("=== SORVETES ADICIONADOS ===")

    def get_ice_cream_quantity(self):

        sorvete = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'r-counter-container')]"
                    "[.//div[contains(@class,'r-counter-label') "
                    "and normalize-space()='Sorvete']]"
                )
            )
        )

        return sorvete.find_element(
            By.CSS_SELECTOR,
            ".counter-value"
        ).text

    def call_taxi(self):

        print("=== AGUARDANDO BOTÃO PEDIR TÁXI ===")

        # Espera qualquer overlay/modal anterior desaparecer
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".overlay")
            )
        )

        # Localiza EXATAMENTE o botão "Pedir"
        button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                self.call_taxi_button
            )
        )

        # Garante que o botão esteja visível
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        # Espera o botão ficar clicável
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                self.call_taxi_button
            )
        )

        print("=== CLICANDO EM PEDIR ===")

        # Clique via JavaScript para evitar o overlay interceptar
        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        print("=== TÁXI SOLICITADO ===")

    def get_pop_up(self):
        return self.driver.find_element(
            *self.pop_up
        ).text