import ordinary

def test_temporary_delimiter():
    encode = lambda: ordinary.encode("Kreusada")
    with ordinary.temporary_delimiter("U"):
        assert encode() == "75U114U101U117U115U97U100U97"
    assert encode() == "75-114-101-117-115-97-100-97"
    with ordinary.temporary_delimiter("U", after="O"):
        assert encode() == "75U114U101U117U115U97U100U97"
    assert encode() == "75O114O101O117O115O97O100O97"
