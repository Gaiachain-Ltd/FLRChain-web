from common.tests import CommonTestCase
from investments.serializers import InvestmentSerializer


class InvestmentSerializerTest(CommonTestCase):
    def test_validate(self):
        serializer = InvestmentSerializer(
            data={
                "start": "2022-03-01",
                "end": "2021-03-01",
                "amount": "0.01"
            })
        self.assertEqual(serializer.is_valid(), False)

        serializer = InvestmentSerializer(
            data={
                "start": "2021-03-01",
                "end": "2021-03-01",
                "amount": "-0.01"
            })
        self.assertEqual(serializer.is_valid(), False)

        serializer = InvestmentSerializer(
            data={
                "start": "2021-03-01",
                "end": "2021-03-01",
                "amount": "0.01"
            })
        self.assertEqual(serializer.is_valid(), True)
