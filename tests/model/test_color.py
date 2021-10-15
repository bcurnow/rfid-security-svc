from rfidsecuritysvc.model.color import Color


def test_Color__init__():
    c = Color(0xABCDEF)
    assert c.int == 0xABCDEF
    assert c.hex == 'ABCDEF'
    assert c.html == '#abcdef'


def test_Color__init___zero():
    c = Color(0)
    assert c.int == 0
    assert c.hex == '0'
    assert c.html == '#000000'
