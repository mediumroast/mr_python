import unittest
import os
from dotenv import load_dotenv

class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        pass  # Do not print the dot

    def printErrors(self):
        # Do not print a newline character after each test case
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

def main():
    # Load environment variables
    load_dotenv()

    # Create a TestSuite
    suite = unittest.TestSuite()

    # Add tests to the TestSuite
    loader = unittest.TestLoader()
    suite.addTests(loader.discover(start_dir='tests'))

    # Run the tests in serial with custom result class
    runner = unittest.TextTestRunner(resultclass=CustomTestResult)
    runner.run(suite)

if __name__ == "__main__":
    main()
