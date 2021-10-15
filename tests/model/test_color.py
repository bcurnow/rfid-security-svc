from rfidsecuritysvc.model.color import Color


def test_Color__init__():
    c = Color(0xABCDEF)
    assert c.int == 0xABCDEF
    assert c.hex == 'ABCDEF'
    assert c.html == '#abcdef'


def test_Color__init___zero():
    c = Color(0)
    assert c.int == 0
    assert c.hex == '000000'
    assert c.html == '#000000'


def test_Color__init___two_digits():
    c = Color(0xFF)
    assert c.int == 0xFF
    assert c.hex == '0000FF'
    assert c.html == '#0000ff'


def test_Color__init___four_digits():
    c = Color(0xFFFF)
    assert c.int == 0xFFFF
    assert c.hex == '00FFFF'
    assert c.html == '#00ffff'
