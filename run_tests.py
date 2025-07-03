#!/usr/bin/env python3
"""
Test runner script for Star Wars application test automation
Provides a simple interface for running different test suites
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description=""):
    """Run a shell command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description or command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def setup_environment():
    """Set up the test environment"""
    print("Setting up test environment...")
    
    # Create necessary directories
    directories = ['screenshots', 'reports', 'test_data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Check if .env file exists
    if not Path('.env').exists():
        if Path('.env.example').exists():
            print("Creating .env file from .env.example")
            subprocess.run('cp .env.example .env', shell=True)
        else:
            print("Warning: No .env file found. Please create one with your configuration.")
    
    print("Environment setup complete!")


def run_tests(test_type="all", browser="chrome", headless=True, verbose=True):
    """Run the specified test suite"""
    
    # Set environment variables
    os.environ['BROWSER'] = browser
    os.environ['HEADLESS'] = str(headless).lower()
    
    # Base pytest command
    base_cmd = "python -m pytest"
    
    # Add verbosity
    if verbose:
        base_cmd += " -v"
    
    # Add test path based on type
    if test_type == "ui":
        test_path = "tests/ui/"
    elif test_type == "api":
        test_path = "tests/api/"
    elif test_type == "all":
        test_path = "tests/"
    else:
        print(f"Unknown test type: {test_type}")
        return False
    
    # Generate HTML report
    report_name = f"{test_type}_report_{browser}{'_headless' if headless else ''}.html"
    report_path = f"reports/{report_name}"
    
    # Complete command
    command = f"{base_cmd} {test_path} --html={report_path} --self-contained-html --tb=short"
    
    # Run the tests
    success = run_command(command, f"Running {test_type} tests with {browser}")
    
    if success:
        print(f"\n✅ Tests completed successfully!")
        print(f"📊 Report saved to: {report_path}")
    else:
        print(f"\n❌ Tests failed!")
        if Path('screenshots').exists():
            screenshots = list(Path('screenshots').glob('*.png'))
            if screenshots:
                print(f"📸 Screenshots available: {len(screenshots)} files")
    
    return success


def main():
    """Main function to handle command line arguments and run tests"""
    parser = argparse.ArgumentParser(description="Star Wars Test Automation Runner")
    
    parser.add_argument(
        '--type', 
        choices=['all', 'ui', 'api'], 
        default='all',
        help='Type of tests to run (default: all)'
    )
    
    parser.add_argument(
        '--browser', 
        choices=['chrome', 'firefox', 'edge'], 
        default='chrome',
        help='Browser to use for UI tests (default: chrome)'
    )
    
    parser.add_argument(
        '--headless', 
        action='store_true',
        help='Run browser in headless mode'
    )
    
    parser.add_argument(
        '--setup', 
        action='store_true',
        help='Set up test environment only'
    )
    
    parser.add_argument(
        '--quiet', 
        action='store_true',
        help='Run tests with minimal output'
    )
    
    args = parser.parse_args()
    
    # Setup environment
    setup_environment()
    
    if args.setup:
        print("Environment setup complete. Use --type to run tests.")
        return
    
    # Run tests
    success = run_tests(
        test_type=args.type,
        browser=args.browser,
        headless=args.headless,
        verbose=not args.quiet
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()