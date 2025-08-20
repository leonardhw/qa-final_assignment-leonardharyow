from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ReportsPage(BasePage):
    """
    Reports Page Object - Handles Sales Reports page functionality
    """
    
    # Reports page selectors (exact XPaths provided)
    REPORTS_HEADING = (By.CSS_SELECTOR, 'h1.text-2xl.font-semibold.text-gray-900')
    TOTAL_SALES_VALUE = (By.XPATH, '//*[@id="root"]/div/main/div/div[2]/div[1]/div/div[2]/p[2]')
    TRANSACTIONS_VALUE = (By.XPATH, '//*[@id="root"]/div/main/div/div[2]/div[2]/div/div[2]/p[2]')
    AVERAGE_ORDER_VALUE = (By.XPATH, '//*[@id="root"]/div/main/div/div[2]/div[3]/div/div[2]/p[2]')
    TOP_PRODUCTS_COUNT = (By.XPATH, '//*[@id="root"]/div/main/div/div[2]/div[4]/div/div[2]/p[2]')
    
    # Top Products section selectors
    TOP_PRODUCTS_SECTION = (By.XPATH, "//h3[contains(text(), 'Top Products')]")
    TOP_PRODUCTS_LIST = (By.XPATH, "//h3[contains(text(), 'Top Products')]/following-sibling::div//p[@class='font-medium text-gray-900']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_on_reports_page(self):
        """Check if we're on the Reports page by looking for the heading"""
        return self.is_element_visible(self.REPORTS_HEADING)
    
    def get_reports_heading_text(self):
        """Get the text of the reports heading"""
        if self.is_element_visible(self.REPORTS_HEADING):
            return self.get_element_text(self.REPORTS_HEADING)
        return None
    
    def get_total_sales(self):
        """Get the total sales value"""
        if self.is_element_visible(self.TOTAL_SALES_VALUE):
            return self.get_element_text(self.TOTAL_SALES_VALUE)
        return None
    
    def get_transactions_count(self):
        """Get the transactions count value"""
        if self.is_element_visible(self.TRANSACTIONS_VALUE):
            return self.get_element_text(self.TRANSACTIONS_VALUE)
        return None
    
    def get_average_order(self):
        """Get the average order value"""
        if self.is_element_visible(self.AVERAGE_ORDER_VALUE):
            return self.get_element_text(self.AVERAGE_ORDER_VALUE)
        return None
    
    def get_top_products_count(self):
        """Get the top products count value"""
        if self.is_element_visible(self.TOP_PRODUCTS_COUNT):
            return self.get_element_text(self.TOP_PRODUCTS_COUNT)
        return None
    
    def get_all_metrics(self):
        """Get all metrics as a dictionary"""
        return {
            "total_sales": self.get_total_sales(),
            "transactions": self.get_transactions_count(),
            "average_order": self.get_average_order(),
            "top_products_count": self.get_top_products_count()
        }
    
    def verify_product_in_top_products(self, product_name):
        """Verify if a specific product appears in the Top Products list"""
        try:
            # Find all product names in the top products section
            product_elements = self.find_elements(self.TOP_PRODUCTS_LIST)
            
            for element in product_elements:
                if product_name.lower() in element.text.lower():
                    return True
            return False
        except Exception:
            return False
    
    def get_top_products_list(self):
        """Get list of all products in Top Products section"""
        try:
            product_elements = self.find_elements(self.TOP_PRODUCTS_LIST)
            return [element.text for element in product_elements]
        except Exception:
            return []
    
    def verify_reports_data(self, expected_total_sales, expected_transactions, 
                           expected_average_order, expected_top_products_count, 
                           expected_product=None):
        """Verify all reports data matches expected values"""
        verification_results = {}
        
        # Verify page is loaded
        verification_results["page_loaded"] = self.is_on_reports_page()
        
        # Verify heading
        heading = self.get_reports_heading_text()
        verification_results["correct_heading"] = heading == "Sales Reports"
        
        # Verify metrics
        actual_metrics = self.get_all_metrics()
        
        verification_results["total_sales_match"] = actual_metrics["total_sales"] == expected_total_sales
        verification_results["transactions_match"] = actual_metrics["transactions"] == expected_transactions
        verification_results["average_order_match"] = actual_metrics["average_order"] == expected_average_order
        verification_results["top_products_count_match"] = actual_metrics["top_products_count"] == expected_top_products_count
        
        # Verify specific product if provided
        if expected_product:
            verification_results["product_in_list"] = self.verify_product_in_top_products(expected_product)
        
        # Store actual values for debugging
        verification_results["actual_values"] = actual_metrics
        verification_results["expected_values"] = {
            "total_sales": expected_total_sales,
            "transactions": expected_transactions,
            "average_order": expected_average_order,
            "top_products_count": expected_top_products_count,
            "product": expected_product
        }
        
        return verification_results