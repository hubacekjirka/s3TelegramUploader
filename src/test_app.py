from app import _get_diag
import re


def test_diag():
    message = _get_diag().split("\n")

    assert len(message) == 6

    ip = message[4]
    matched = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", ip)
    assert len(matched) == 1, f"Couldn't find IP in the response: {ip}"
