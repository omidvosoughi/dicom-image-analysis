import os
import unittest
import pydicom
import numpy as np
from main import pixel_volume
import argparse

class TestPixelVolume(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('--threshold', type=float, required=True, help="Threshold for the pixel volume test.")
        args, _ = parser.parse_known_args()
        cls.threshold = args.threshold

    def test_pixel_volume(self):
        # Path to the DICOM file for testing
        file_path = 'test.dcm'
        cwd = os.getcwd()
        dicomPath = f"{cwd}/backend/uploads/1-101.dcm"
        # Threshold value
        threshold = 0.5051  # You need to adjust this based on what you expect to use

        # Call the function under test
        result = pixel_volume(dicomPath, self.threshold)

        # Assert that the result is approximately equal to the expected value
        expected_value = 143280.029
        tolerance = 400.0  # You can adjust the tolerance level to your needs

        # Print custom message regardless of test outcome
        print(f"Result {result} is expected to be approximately equal to {expected_value} within {tolerance} tolerance.")

        self.assertAlmostEqual(result, expected_value, delta=tolerance, 
                               msg=f"Result {result} is not approximately equal to expected {expected_value} within {tolerance} tolerance.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)