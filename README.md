# Advanced Web Testing Suite

This project implements a comprehensive testing suite that covers integration, security, and performance testing for web applications. The example implementation uses the SauceDemo website, but the framework can be adapted for any web application.

[![CI/CD Pipeline](https://github.com/your-username/advance-integration-ui-automation/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/your-username/advance-integration-ui-automation/actions)
[![codecov](https://codecov.io/gh/your-username/advance-integration-ui-automation/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/advance-integration-ui-automation)
[![Docker](https://img.shields.io/docker/automated/your-username/web-testing-suite.svg)](https://hub.docker.com/r/your-username/web-testing-suite)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Docker Support](#docker-support)
- [Test Types](#test-types)
  - [Integration Tests](#integration-tests)
  - [Security Tests](#security-tests)
  - [Performance Tests](#performance-tests)
  - [Backend Tests](#backend-tests)
- [Running Tests](#running-tests)
- [Customization](#customization)
- [Best Practices](#best-practices)
- [Deployment](#deployment)

## Prerequisites

- Python 3.8 or higher
- Conda or Mamba package manager
- Git (for version control)
- Modern web browser (Chrome/Firefox/Edge)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd advance-integration-ui-automation
```

2. Create and activate a conda environment:

```bash
mamba create -n joy python=3.12
mamba activate joy
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:

```bash
playwright install
```

## Project Structure

```
advance-integration-ui-automation/
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions CI/CD pipeline
├── tests/
│   ├── backend/             # Backend testing suite
│   │   ├── blackbox/        # Black box testing
│   │   │   ├── __init__.py
│   │   │   ├── test_api_endpoints.py
│   │   │   └── test_database.py
│   │   ├── whitebox/        # White box testing
│   │   │   ├── __init__.py
│   │   │   ├── test_code_coverage.py
│   │   │   └── test_unit_testing.py
│   │   ├── __init__.py
│   │   └── test_service_integration.py
│   ├── integration/          # Integration tests
│   │   ├── __init__.py
│   │   └── test_sauce_demo.py
│   ├── security/            # Security tests
│   │   ├── __init__.py
│   │   └── test_security.py
│   ├── performance/         # Performance tests
│   │   ├── __init__.py
│   │   └── locustfile.py
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration
│   └── utils.py            # Shared utilities
├── reports/                 # Generated test reports
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # Docker Compose for local development
├── .dockerignore           # Docker ignore file
├── requirements.txt
└── README.md
```

## CI/CD Pipeline

This project includes a comprehensive CI/CD pipeline using GitHub Actions that automatically:

### Continuous Integration (CI)

- **Multi-Python Version Testing**: Tests against Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **Code Quality**: Runs flake8 linting to ensure code quality
- **Test Execution**: Runs integration and security tests automatically
- **Coverage Reporting**: Generates code coverage reports and uploads to Codecov
- **Security Scanning**: Performs security analysis using Bandit and Safety
- **Performance Testing**: Runs automated performance tests on main branch

### Continuous Deployment (CD)

- **Docker Build**: Builds and pushes Docker images to Docker Hub
- **Staging Deployment**: Deploys to staging environment for testing
- **Production Deployment**: Deploys to production after all tests pass
- **Smoke Tests**: Runs post-deployment verification tests

### Pipeline Triggers

- **Push Events**: Triggers on pushes to `main` and `develop` branches
- **Pull Requests**: Runs full test suite on PRs to `main` and `develop`
- **Scheduled Runs**: Daily automated test runs at 2 AM UTC
- **Manual Triggers**: Can be triggered manually from GitHub Actions UI

### Artifacts and Reports

- Test reports (HTML format)
- Coverage reports
- Security scan results
- Performance test results
- Docker images

## Docker Support

The project includes full Docker support for consistent testing environments and easy deployment.

### Building and Running with Docker

#### Option 1: Docker Compose (Recommended for local development)

```bash
# Run all tests
docker-compose up web-tests

# Run performance tests with web UI
docker-compose up performance-tests
# Then open http://localhost:8089 in your browser

# Run security scans
docker-compose up security-scan

# Clean up
docker-compose down
```

#### Option 2: Direct Docker Commands

```bash
# Build the image
docker build -t web-testing-suite .

# Run integration and security tests
docker run --rm -v $(pwd)/reports:/app/reports web-testing-suite

# Run performance tests
docker run --rm -p 8089:8089 -v $(pwd)/reports:/app/reports web-testing-suite \
  sh -c "cd tests/performance && locust -f locustfile.py --host=https://www.saucedemo.com --web-host=0.0.0.0"
```

### Docker Features

- **Multi-stage builds** for optimized image size
- **Non-root user** for enhanced security
- **Cached dependencies** for faster builds
- **Volume mounts** for persistent reports
- **Network isolation** for secure testing

## Test Types

### Integration Tests

Located in `tests/integration/test_sauce_demo.py`

Integration tests verify the complete user journey through the application, including:

- Login functionality
- Product browsing and selection
- Cart management
- Checkout process
- AI-powered analysis of user interactions

Key features:

- Uses Playwright for browser automation
- Implements AI integration for smart validation
- Generates detailed test reports

To run integration tests:

```bash
pytest tests/integration/test_sauce_demo.py -v
```

### Security Tests

Located in `tests/security/test_security.py`

Security tests check for common web vulnerabilities:

- XSS (Cross-Site Scripting) prevention
- SQL Injection protection
- CSRF (Cross-Site Request Forgery) safeguards

To run security tests:

```bash
pytest tests/security/test_security.py -v
```

### Performance Tests

Located in `tests/performance/locustfile.py`

Performance tests measure the application's behavior under load:

- Response times
- Concurrent user handling
- System stability

To run performance tests:

1. Start Locust:

```bash
cd tests/performance
locust -f locustfile.py --host=https://your-website.com
```

2. Open http://localhost:8089 in your browser
3. Configure test parameters:
   - Number of users
   - Spawn rate
   - Run time

### Backend Tests

Clean, focused backend testing using essential packages.

#### Black Box Testing (`tests/backend/blackbox/`)

**API Testing** (`test_api_simple.py`):

- RESTful API endpoint testing with real and mocked responses
- Error handling and performance validation
- Uses `requests` and `responses` packages

**Database Testing** (`test_database_simple.py`):

- SQLite database operations (CRUD)
- Automatic test data generation with Factory Boy
- Data integrity and constraint testing

#### White Box Testing (`tests/backend/whitebox/`)

**Unit Testing** (`test_unit_simple.py`):

- Service layer testing with mocking
- Code coverage analysis
- Internal logic validation using `pytest-mock`

#### Integration Testing (`test_integration_simple.py`)

- Multi-service integration testing
- End-to-end workflow validation
- Performance testing

#### Running Backend Tests

```bash
# Simple test runner
python run_backend_tests.py --all                    # All backend tests
python run_backend_tests.py --api                    # API tests only
python run_backend_tests.py --database               # Database tests only
python run_backend_tests.py --unit                   # Unit tests only
python run_backend_tests.py --integration            # Integration tests only
python run_backend_tests.py --security               # Security scan

# Direct pytest commands
pytest tests/backend/ -v --cov=tests/backend --cov-report=html
```

#### Essential Packages Used

- **Factory Boy**: Automatic test data generation
- **Faker**: Realistic fake data
- **Responses**: HTTP request mocking
- **pytest-mock**: Function mocking
- **pytest-cov**: Code coverage analysis
- **Bandit**: Security vulnerability scanning

## Running Tests

### Running All Tests

```bash
pytest tests/ -v
```

### Running Specific Test Types

```bash
# Integration tests only
pytest tests/integration/ -v

# Security tests only
pytest tests/security/ -v

# Performance tests
locust -f tests/performance/locustfile.py --host=https://your-website.com
```

## Customization

### Adapting for Your Website

1. Integration Tests:

   - Update URLs in test_sauce_demo.py
   - Modify selectors to match your website's elements
   - Adjust test scenarios for your use cases

2. Security Tests:

   - Customize payload patterns in test_security.py
   - Add specific security checks for your application
   - Update test cases based on your security requirements

3. Performance Tests:
   - Modify locustfile.py with your website's flows
   - Update URLs and endpoints
   - Adjust task weights based on your usage patterns

### Configuration

- Environment variables in `.env` file
- Test configuration in `conftest.py`
- Browser settings in Playwright configuration

## Best Practices

### Integration Testing

- Use meaningful test names
- Implement proper waiting strategies
- Handle dynamic elements appropriately
- Maintain test independence
- Use fixtures for setup/teardown

### Security Testing

- Regular security test updates
- Comprehensive vulnerability checks
- Safe test environment usage
- Proper error handling
- Documentation of security findings

### Performance Testing

- Start with small user loads
- Gradually increase load
- Monitor system resources
- Analyze response patterns
- Document performance baselines

## Deployment

### Setting up CI/CD

1. **GitHub Secrets Configuration**:

   ```bash
   # Required secrets for the CI/CD pipeline:
   DOCKER_USERNAME=your-docker-hub-username
   DOCKER_PASSWORD=your-docker-hub-password
   ```

2. **Branch Protection Rules**:

   - Enable branch protection for `main` branch
   - Require status checks to pass before merging
   - Require pull request reviews
   - Dismiss stale reviews when new commits are pushed

3. **Environment Configuration**:
   - Create `staging` and `production` environments in GitHub
   - Configure environment-specific secrets and variables
   - Set up deployment approval requirements for production

### Local Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and test locally
pytest tests/ -v

# 3. Run Docker tests
docker-compose up web-tests

# 4. Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name

# 5. Create pull request
# The CI/CD pipeline will automatically run all tests
```

### Production Deployment

The CI/CD pipeline automatically handles deployment when code is merged to the `main` branch:

1. **Automated Testing**: All test suites run automatically
2. **Security Scanning**: Code is scanned for vulnerabilities
3. **Docker Build**: Container images are built and pushed
4. **Staging Deployment**: Code is deployed to staging environment
5. **Smoke Tests**: Post-deployment tests verify functionality
6. **Production Deployment**: After manual approval, deploys to production

### Monitoring and Alerts

- **Test Results**: Available in GitHub Actions artifacts
- **Coverage Reports**: Integrated with Codecov
- **Security Reports**: Generated by Bandit and Safety tools
- **Performance Metrics**: Captured by Locust performance tests

## Reporting Issues

- Use descriptive titles
- Include test logs
- Provide reproduction steps
- Specify environment details
- Add relevant screenshots

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for any changes
- Ensure all CI/CD checks pass
- Add meaningful commit messages

## License

This project is licensed under the MIT License - see the LICENSE file for details
