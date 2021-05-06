# 1003474
# Alex W

import pytest
from present import sBoxLayer, pLayer, present_round, present_inv_round, genRoundKeys


class TestKey:
    def test_one(self):
        key1 = 0x00000000000000000000

        keys = genRoundKeys(key1)
        keysTest = {
            0: 32,
            1: 0,
            2: 13835058055282163712,
            3: 5764633911313301505,
            4: 6917540022807691265,
            5: 12682149744835821666,
            6: 10376317730742599722,
            7: 442003720503347,
            8: 11529390968771969115,
            9: 14988212656689645132,
            10: 3459180129660437124,
            11: 16147979721148203861,
            12: 17296668118696855021,
            13: 9227134571072480414,
            14: 4618353464114686070,
            15: 8183717834812044671,
            16: 1198465691292819143,
            17: 2366045755749583272,
            18: 13941741584329639728,
            19: 14494474964360714113,
            20: 7646225019617799193,
            21: 13645358504996018922,
            22: 554074333738726254,
            23: 4786096007684651070,
            24: 4741631033305121237,
            25: 17717416268623621775,
            26: 3100551030501750445,
            27: 9708113044954383277,
            28: 10149619148849421687,
            29: 2165863751534438555,
            30: 15021127369453955789,
            31: 10061738721142127305,
            32: 7902464346767349504
        }

        for k in keysTest.keys():
            assert keysTest[k] == keys[k]


class TestSbox:
    def test_one(self):
        state0 = 0x0123456789abcdef

        expected = 0xc56b90ad3ef84712

        output = sBoxLayer(state0, 64)

        assert (hex(output) == hex(expected))


class TestPlayer:
    def test_one(self):
        state0 = 0b1

        expected = 0b1

        output = pLayer(state0)

        assert (output == expected)

    def test_two(self):
        state0 = 0b10

        expected = 0b10000000000000000

        output = pLayer(state0)

        assert (bin(output) == bin(expected))

    def test_three(self):
        state0 = 0b1000000000

        expected = 0b1000000000000000000

        output = pLayer(state0)

        assert (bin(output) == bin(expected))


class TestNoKeySchedule:
    def test_one(self):
        plain1 = 0x0000000000000000
        key1 = 0x00000000000000000000

        round1 = present_round(plain1, key1)
        round11 = 0xffffffff00000000
        assert (round1 == round11)

    def test_two(self):
        plain1 = 0x0000000000000000
        key1 = 0x00000000000000000000

        round1 = present_round(plain1, key1)
        round2 = present_round(round1, key1)
        round22 = 0xff00ffff000000
        assert round2 == round22

    def test_three(self):
        plain1 = 0x0000000000000000
        key1 = 0x00000000000000000000

        round1 = present_round(plain1, key1)
        round2 = present_round(round1, key1)
        round3 = present_round(round2, key1)
        round33 = 0xcc3fcc3f33c00000
        assert round3 == round33

    def test_inv(self):
        # invert single rounds
        plain1 = 0x0000000000000000
        key1 = 0x00000000000000000000

        round1 = present_round(plain1, key1)
        round2 = present_round(round1, key1)
        round3 = present_round(round2, key1)

        plain11 = present_inv_round(round1, key1)
        assert plain1 == plain11
        plain22 = present_inv_round(round2, key1)
        assert round1 == plain22
        plain33 = present_inv_round(round3, key1)
        assert round2 == plain33