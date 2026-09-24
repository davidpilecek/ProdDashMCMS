from metrisapi.historian import HistorianClient
from metrisapi.account import AccountClient
from metrisapi.configuration import ConfigurationClient
from metrisapi.dataanalysis import DataAnalysisClient


def connect():
    BASE_URI = "https://localhost:9000"

    ac = AccountClient(BASE_URI)

    token = ac.authenticate(
        username="metris.user",
        password="Metris123!"
    )["id"]

    hc = HistorianClient(BASE_URI, lambda: token)
    cc = ConfigurationClient(BASE_URI, token=lambda: token)
    dac = DataAnalysisClient(BASE_URI, lambda: token)

    return hc, cc, dac

