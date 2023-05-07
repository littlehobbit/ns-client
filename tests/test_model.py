import client.data.model as model
import unittest


class TestModel(unittest.TestCase):
    def test_create(self):
        m = model.current_model

    def test_can_be_modified(self):
        m = model.current_model
        m.precision = model.Precision.H
        self.assertEqual(m.precision, model.current_model.precision)