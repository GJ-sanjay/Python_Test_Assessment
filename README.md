# Star Wars Application Test Automation Framework

A comprehensive test automation framework for the Star Wars application using Selenium WebDriver with Python, designed to demonstrate advanced testing practices and clean code architecture.

## 🚀 Framework Features

- **Page Object Model**: Clean separation of page logic and test logic
- **Advanced Configuration Management**: Environment-based configuration with fallbacks
- **Robust Error Handling**: Retry mechanisms and detailed error reporting
- **Cross-Browser Testing**: Support for Chrome, Firefox, and Edge browsers
- **CI/CD Integration**: GitHub Actions workflow for automated testing
- **Comprehensive Reporting**: HTML reports with screenshots on failure
- **API Testing**: Integration with Star Wars API for data validation
- **Scalable Architecture**: Modular design for easy maintenance and extension

## 🏗️ Project Structure

```
star-wars-test-automation/
├── config/
│   └── config.py                  # Configuration management
├── pages/
│   ├── movie_list_page.py         # Movie list page object
│   └── movie_detail_page.py       # Movie detail page object
├── api/
│   └── star_wars_api.py           # API client for Star Wars API
├── utils/
│   ├── driver_manager.py          # WebDriver management
│   ├── base_page.py               # Base page class
│   └── test_helpers.py            # Test utilities and helpers
├── tests/
│   ├── ui/
│   │   ├── test_movie_sorting.py  # UI tests for movie sorting
│   │   └── test_movie_details.py  # UI tests for movie details
│   ├── api/
│   │   └── test_star_wars_api.py  # API tests
│   └── conftest.py                # Test configuration and fixtures
├── .github/
│   └── workflows/
│       └── test-automation.yml    # GitHub Actions workflow
├── requirements.txt               # Python dependencies
├── pytest.ini                    # Pytest configuration
├── .env.example                   # Environment variables example
└── README.md                      # This file
```

## 🧪 Test Coverage

### UI Test Scenarios
1. **Movie Sorting**: Sort movies by 'Title' and verify 'The Phantom Menace' is last
2. **Movie Details - Species**: Verify 'The Empire Strikes Back' contains 'Wookie' in species list
3. **Movie Details - Planets**: Verify 'The Phantom Menace' does NOT contain 'Camino' in planets list

### API Test Scenarios
1. **Movies Count**: Verify the API returns exactly 6 movies
2. **Third Movie Director**: Verify the 3rd movie's director is 'Richard Marquand'
3. **Fifth Movie Producer**: Verify the 5th movie's producer is NOT 'Gary Kurtz, George Lucas'

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.9+ (recommended: 3.11)
- Chrome, Firefox, or Edge browser
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd star-wars-test-automation
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Create required directories**
   ```bash
   mkdir -p screenshots reports test_data
   ```

## 🏃‍♂️ Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run UI Tests Only
```bash
python -m pytest tests/ui/ -v
```

### Run API Tests Only
```bash
python -m pytest tests/api/ -v
```

### Run Tests with HTML Report
```bash
python -m pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Run Tests in Headless Mode
```bash
HEADLESS=true python -m pytest tests/ -v
```

### Run Tests with Different Browser
```bash
BROWSER=firefox python -m pytest tests/ -v
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `http://localhost:3000` | URL of the Star Wars application |
| `API_BASE_URL` | `https://swapi.dev/api` | Star Wars API base URL |
| `BROWSER` | `chrome` | Browser to use (chrome, firefox, edge) |
| `HEADLESS` | `false` | Run browser in headless mode |
| `IMPLICIT_WAIT` | `10` | Implicit wait timeout in seconds |
| `PAGE_LOAD_TIMEOUT` | `30` | Page load timeout in seconds |
| `SCREENSHOT_ON_FAILURE` | `true` | Take screenshots on test failure |

### Browser Configuration
The framework supports multiple browsers with automatic WebDriver management:
- **Chrome**: Uses ChromeDriver via webdriver-manager
- **Firefox**: Uses GeckoDriver via webdriver-manager
- **Edge**: Uses EdgeDriver via webdriver-manager

## 🤖 CI/CD Integration

The framework includes a comprehensive GitHub Actions workflow that:

### Automated Testing
- Runs on push to main/develop branches
- Runs on pull requests
- Scheduled daily execution
- Manual workflow dispatch with parameters

### Matrix Testing
- Multiple Python versions (3.9, 3.10, 3.11)
- Multiple browsers (Chrome, Firefox)
- Parallel execution for faster feedback

### Reporting and Artifacts
- HTML test reports
- Screenshots on failure
- Security vulnerability scanning
- Test result summaries

### Workflow Features
- **Caching**: Python dependencies cached for faster builds
- **Parallel Execution**: Multiple configurations run simultaneously
- **Failure Handling**: Continues on error to run all test suites
- **Artifact Management**: Automatic upload of reports and screenshots

## 📊 Test Reports

### HTML Reports
- Comprehensive test execution reports
- Test duration and status
- Error details and stack traces
- Screenshots attached to failed tests

### Screenshot Capture
- Automatic screenshot on test failure
- Organized by test name and timestamp
- Uploaded as GitHub Actions artifacts

## 🔍 Code Quality Features

### Design Patterns
- **Page Object Model**: Encapsulates page elements and actions
- **Factory Pattern**: WebDriver creation and management
- **Singleton Pattern**: Configuration management
- **Strategy Pattern**: Browser selection and configuration

### Best Practices
- **DRY Principle**: Reusable components and utilities
- **SOLID Principles**: Clean, maintainable code architecture
- **Error Handling**: Comprehensive exception handling and retry logic
- **Documentation**: Detailed docstrings and comments

### Testing Practices
- **Test Isolation**: Each test is independent
- **Data-Driven Testing**: Parameterized tests where applicable
- **Retry Logic**: Automatic retry on transient failures
- **Cleanup**: Proper resource cleanup after tests

## 🛡️ Security Considerations

### Secure Practices
- Environment variable management for sensitive data
- No hardcoded credentials or URLs
- Security scanning in CI/CD pipeline
- Dependency vulnerability checking

### Privacy
- No personal data collection
- Minimal logging of sensitive information
- Secure artifact handling

## 📈 Performance Optimization

### Efficiency Features
- **Parallel Execution**: Multiple test configurations run simultaneously
- **Caching**: WebDriver binaries and Python dependencies cached
- **Lazy Loading**: Resources loaded only when needed
- **Connection Pooling**: Reused HTTP connections for API tests

### Resource Management
- **Memory Optimization**: Proper cleanup of WebDriver instances
- **Timeout Configuration**: Appropriate timeouts to prevent hanging
- **Selective Execution**: Run only necessary tests based on changes

## 🔧 Troubleshooting

### Common Issues

1. **WebDriver Issues**
   ```bash
   # Clear WebDriver cache
   rm -rf ~/.wdm
   ```

2. **Screenshot Directory**
   ```bash
   # Create screenshots directory
   mkdir -p screenshots
   ```

3. **Permission Issues**
   ```bash
   # Fix permissions
   chmod +x venv/bin/activate
   ```

4. **Browser Not Found**
   ```bash
   # Install Chrome on Ubuntu
   sudo apt-get install google-chrome-stable
   ```

### Debug Mode
```bash
# Run with verbose output
python -m pytest tests/ -v -s --tb=long
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guide
- Add docstrings to all functions and classes
- Write unit tests for new functionality
- Update documentation as needed

### Pull Request Process
1. Ensure all tests pass
2. Update README if needed
3. Add test coverage for new features
4. Request review from maintainers

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Star Wars API**: Thanks to SWAPI for providing the data
- **Selenium Community**: For the robust testing framework
- **Python Community**: For the excellent testing ecosystem

---

**Note**: This framework is designed for assessment purposes. It demonstrates advanced testing practices, clean code architecture, and professional-grade automation framework design. Cloned the repo from "https://github.com/MindfulMichaelJames/star-wars/tree/main" and did a yarn install,build and start to run the app in localhost:3000