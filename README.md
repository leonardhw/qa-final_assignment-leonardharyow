# POS Automation Test Suite

Automated testing suite for a Point of Sale (POS) web application using Selenium WebDriver with Python and the Page Object Model (POM) design pattern.

## Application Under Test
- **URL**: https://simple-pos-pwdk.netlify.app/
- **Credentials**: admin@pos.com / admin

## Test Coverage
- ✅ User Login/Logout (3 test cases)
- ✅ Product Search & Selection (7 test cases) 
- ✅ Cart Management (4 test cases)
- ✅ Checkout & Payment (1 test case)
- ✅ Reports Verification (2 test cases)

**Total: 17 automated test cases**

## Quick Start

### Prerequisites
- Python 3.8+
- Chrome browser (latest version)

### Installation
```bash
cd test/
pip install -r requirements.txt
```

### Run Tests
```bash
# Run all tests with HTML report
pytest tests/ --html=reports/test_report.html --self-contained-html

# Run specific test module
pytest tests/test_login.py -v

# Run tests by priority
pytest -m high -v
```

## Project Structure
```
test/
├── pages/           # Page Object Model classes
├── tests/           # Test cases organized by functionality
├── data/            # CSV test data files
├── config/          # Configuration settings
├── utils/           # Helper utilities and data readers
├── reports/         # Generated test reports and screenshots
├── requirements.txt # Python dependencies
└── pytest.ini      # Test configuration
```

## Key Features
- **Page Object Model**: Maintainable and reusable code structure
- **Data-Driven Testing**: CSV-based test data management
- **HTML Reports**: Detailed test execution reports with pass/fail status
- **Screenshot on Failure**: Automatic screenshot capture for failed tests
- **Test Prioritization**: High/Medium/Low priority markers
- **Cross-browser Ready**: Configurable for different browsers

## Test Data
Test scenarios use CSV files for data-driven testing:
- `login_test_data.csv` - Login credentials and scenarios
- `product_search_data.csv` - Product search terms and categories
- `cart_test_data.csv` - Cart operations test data
- `checkout_test_data.csv` - Customer checkout information
- `reports_test_data.csv` - Expected report values

## Troubleshooting

### Common Issues
**Browser driver issues**: WebDriverManager handles Chrome driver automatically

**Network timeouts**: Increase wait times in `config/config.py`:
```python
EXPLICIT_WAIT: int = 30  # Increase from 20
```

**Element not found**: Check if application UI has changed, update locators in page objects

**Tests running slowly**: Ensure stable internet connection, application may be slow

### Test Execution Tips
- Run tests individually first to isolate issues
- Check `reports/screenshots/` folder for failure screenshots
- Review HTML reports for detailed execution logs
- Ensure Chrome browser is updated to latest version

## Reporting
- **HTML Reports**: Generated in `reports/` directory
- **Screenshots**: Failure screenshots saved automatically
- **Test Metrics**: Pass/fail counts and execution times
- **Detailed Logs**: Step-by-step execution details

## Configuration
Modify `config/config.py` to customize:
- Browser type (Chrome/Firefox)
- Headless mode
- Wait timeouts
- Test environment URLs