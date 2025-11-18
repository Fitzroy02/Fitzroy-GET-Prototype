import unittest
from chronicles.access_model import AccessModel

class TestAccessModel(unittest.TestCase):
    def test_purchase_window(self):
        model = AccessModel()
        self.assertTrue(model.is_purchase_available(3))
        self.assertFalse(model.is_purchase_available(10))

if __name__ == '__main__':
    unittest.main()
