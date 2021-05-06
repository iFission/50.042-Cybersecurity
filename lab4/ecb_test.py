# 1003474
# Alex W
from ecb import *


class TestEcb:
    def test_zero(self):
        assert True

    def test_key(self):
        ecb('Tux.ppm', 'Tux_Encrypted.ppm', 'key', '4')

    def test_encrypt_short(self):
        ecb('Tux_short.ppm', 'Tux_short_E.ppm', 'key', 'e')

    def test_decrypt_short(self):
        ecb('Tux_short_E.ppm', 'Tux_short_E_D.ppm', 'key', 'd')

    def test_tux_short_end_to_end(self):
        ecb('Tux_short.ppm', 'Tux_short_E.ppm', 'key', 'e')
        ecb('Tux_short_E.ppm', 'Tux_short_E_D.ppm', 'key', 'd')

        with open('Tux_short.ppm', 'rb') as original:
            with open('Tux_short_E_D.ppm', 'rb') as processed:
                assert original.read() == processed.read()

    def test_tux_end_to_end(self):
        ecb('Tux.ppm', 'Tux_E.ppm', 'key', 'e')
        ecb('Tux_E.ppm', 'Tux_E_D.ppm', 'key', 'd')

        with open('Tux.ppm', 'rb') as original:
            with open('Tux_E_D.ppm', 'rb') as processed:
                assert original.read() == processed.read()
