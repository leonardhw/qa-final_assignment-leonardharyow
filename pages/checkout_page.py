from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Checkout Page Object - Handles checkout modal form functionality
    """

    # Checkout form selectors (exact XPaths provided)
    CUSTOMER_NAME_INPUT = (
        By.XPATH,
        '//*[@id="root"]/div/main/div/div[3]/div/form/div[2]/div[1]/input',
    )
    CUSTOMER_EMAIL_INPUT = (
        By.XPATH,
        '//*[@id="root"]/div/main/div/div[3]/div/form/div[2]/div[2]/input',
    )
    PAYMENT_CARD_BUTTON = (
        By.XPATH,
        '//*[@id="root"]/div/main/div/div[3]/div/form/div[3]/div/button[2]',
    )
    NOTES_TEXTAREA = (
        By.XPATH,
        '//*[@id="root"]/div/main/div/div[3]/div/form/div[4]/textarea',
    )
    CANCEL_BUTTON = (
        By.XPATH,
        '//*[@id="root"]/div/main/div/div[3]/div/form/div[5]/button[1]',
    )
    COMPLETE_TRANSACTION_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')

    def __init__(self, driver):
        super().__init__(driver)

    def is_checkout_modal_open(self):
        """Check if checkout modal is open by looking for customer name input"""
        return self.is_element_visible(self.CUSTOMER_NAME_INPUT)

    def enter_customer_name(self, name):
        """Enter customer name in the form"""
        if self.is_element_visible(self.CUSTOMER_NAME_INPUT):
            self.send_keys_to_element(self.CUSTOMER_NAME_INPUT, name)
            return True
        return False

    def enter_customer_email(self, email):
        """Enter customer email in the form"""
        if self.is_element_visible(self.CUSTOMER_EMAIL_INPUT):
            self.send_keys_to_element(self.CUSTOMER_EMAIL_INPUT, email)
            return True
        return False

    def select_card_payment(self):
        """Select Card payment method (click the Card button)"""
        if self.is_element_visible(self.PAYMENT_CARD_BUTTON):
            self.click_element(self.PAYMENT_CARD_BUTTON)
            return True
        return False

    def enter_notes(self, notes):
        """Enter notes in the textarea"""
        if self.is_element_visible(self.NOTES_TEXTAREA):
            self.send_keys_to_element(self.NOTES_TEXTAREA, notes)
            return True
        return False

    def click_complete_transaction(self):
        """Click the Complete Transaction button to submit the form"""
        if self.is_element_visible(self.COMPLETE_TRANSACTION_BUTTON):
            self.click_element(self.COMPLETE_TRANSACTION_BUTTON)
            return True
        return False

    def click_cancel(self):
        """Click the Cancel button to close checkout modal"""
        if self.is_element_visible(self.CANCEL_BUTTON):
            self.click_element(self.CANCEL_BUTTON)
            return True
        return False

    def fill_checkout_form(self, customer_name, customer_email, notes):
        """Fill the entire checkout form with customer information"""
        success_steps = []

        # Fill customer name
        success_steps.append(self.enter_customer_name(customer_name))

        # Fill customer email
        success_steps.append(self.enter_customer_email(customer_email))

        # Select Card payment method
        success_steps.append(self.select_card_payment())

        # Fill notes
        success_steps.append(self.enter_notes(notes))

        # Return True if all steps succeeded
        return all(success_steps)

    def complete_checkout_transaction(self, customer_name, customer_email, notes):
        """Complete the entire checkout process and handle success alert"""
        # Fill the form
        form_filled = self.fill_checkout_form(customer_name, customer_email, notes)
        if not form_filled:
            return False, "Failed to fill checkout form"

        # Submit the form
        transaction_clicked = self.click_complete_transaction()
        if not transaction_clicked:
            return False, "Failed to click Complete Transaction button"

        # Wait for alert and get success message
        alert_appeared = self.wait_for_alert(timeout=10)
        if not alert_appeared:
            return False, "Success alert did not appear"

        # Get alert text
        alert_text = self.get_alert_text()

        # Accept the alert
        alert_accepted = self.accept_alert()
        if not alert_accepted:
            return False, "Failed to accept success alert"

        # Verify success message
        if alert_text and "Transaction completed successfully" in alert_text:
            return True, alert_text
        else:
            return False, f"Unexpected alert message: {alert_text}"
