import csv
import os
from typing import List, Dict


class DataReader:
    @staticmethod
    def read_csv(filename: str) -> List[Dict]:
        """Read CSV file and return list of dictionaries"""
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        data = []
        with open(data_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        
        return data
    
    @staticmethod
    def get_product_search_data() -> List[Dict]:
        """Get product search test data"""
        return DataReader.read_csv("product_search_data.csv")
    
    @staticmethod
    def get_search_test_case(test_case_name: str) -> Dict:
        """Get specific test case data by name"""
        data = DataReader.get_product_search_data()
        for row in data:
            if row['test_case'] == test_case_name:
                return row
        raise ValueError(f"Test case not found: {test_case_name}")
    
    @staticmethod
    def get_cart_test_data() -> List[Dict]:
        """Get cart management test data"""
        return DataReader.read_csv("cart_test_data.csv")
    
    @staticmethod
    def get_cart_test_case(test_case_name: str) -> Dict:
        """Get specific cart test case data by name"""
        data = DataReader.get_cart_test_data()
        for row in data:
            if row['test_case'] == test_case_name:
                return row
        raise ValueError(f"Cart test case not found: {test_case_name}")
    
    @staticmethod
    def get_checkout_test_data() -> List[Dict]:
        """Get checkout test data"""
        return DataReader.read_csv("checkout_test_data.csv")
    
    @staticmethod
    def get_checkout_test_case(test_case_name: str) -> Dict:
        """Get specific checkout test case data by name"""
        data = DataReader.get_checkout_test_data()
        for row in data:
            if row['test_case'] == test_case_name:
                return row
        raise ValueError(f"Checkout test case not found: {test_case_name}")
    
    @staticmethod
    def get_reports_test_data() -> List[Dict]:
        """Get reports test data"""
        return DataReader.read_csv("reports_test_data.csv")
    
    @staticmethod
    def get_reports_test_case(test_case_name: str) -> Dict:
        """Get specific reports test case data by name"""
        data = DataReader.get_reports_test_data()
        for row in data:
            if row['test_case'] == test_case_name:
                return row
        raise ValueError(f"Reports test case not found: {test_case_name}")
    
    @staticmethod
    def get_login_test_data() -> List[Dict]:
        """Get login test data"""
        return DataReader.read_csv("login_test_data.csv")
    
    @staticmethod
    def get_login_test_case(test_case_name: str) -> Dict:
        """Get specific login test case data by name"""
        data = DataReader.get_login_test_data()
        for row in data:
            if row['test_case'] == test_case_name:
                return row
        raise ValueError(f"Login test case not found: {test_case_name}")