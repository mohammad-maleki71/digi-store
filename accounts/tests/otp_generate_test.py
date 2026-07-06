import pytest

from accounts.utils import generate_otp


# ==========================================================
# generate_otp Tests
# ==========================================================

def test_generate_otp_default_length():
    otp = generate_otp()

    assert len(otp) == 6
    assert otp.isdigit()


def test_generate_otp_custom_length():
    otp = generate_otp(length=4)

    assert len(otp) == 4
    assert otp.isdigit()


def test_generate_otp_zero_length():
    otp = generate_otp(length=0)

    assert otp == ""


def test_generate_otp_returns_string():
    otp = generate_otp()

    assert isinstance(otp, str)


@pytest.mark.parametrize("length", [1, 2, 4, 6, 8, 10])
def test_generate_otp_various_lengths(length):
    otp = generate_otp(length)

    assert len(otp) == length
    assert otp.isdigit()
