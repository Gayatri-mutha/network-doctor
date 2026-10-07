import unittest
from diagnosis.engine import diagnose_network


class TestDiagnosisEngine(unittest.TestCase):

    def test_good_network(self):
        results = {
            "internet": True,
            "latency": 25,
            "packet_loss": 0,
            "dns": True,
            "gateway": True,
            "tcp": True
        }

        diagnosis = diagnose_network(results)

        self.assertIsInstance(diagnosis, dict)
        self.assertIn("problems", diagnosis)
        self.assertIn("recommendations", diagnosis)

    def test_high_latency(self):
        results = {
            "internet": True,
            "latency": 250,
            "packet_loss": 0,
            "dns": True,
            "gateway": True,
            "tcp": True
        }

        diagnosis = diagnose_network(results)

        self.assertTrue(
            len(diagnosis["problems"]) > 0
        )

    def test_packet_loss(self):
        results = {
            "internet": True,
            "latency": 50,
            "packet_loss": 20,
            "dns": True,
            "gateway": True,
            "tcp": True
        }

        diagnosis = diagnose_network(results)

        self.assertTrue(
            len(diagnosis["problems"]) > 0
        )


if __name__ == "__main__":
    unittest.main()