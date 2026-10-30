from src.intervals import merge


def test_more_cases():
    assert merge(["[0,10)", "[10,10]"]) == ["[0,10]"]
    assert merge(["(0,1)", "(1,2)"]) == ["(0,1)", "(1,2)"]
    assert merge(["[-5,-1]", "[-3,0)"]) == ["[-5,0)"]
    assert merge(["[2,3]", "[1,2)"]) == ["[1,3]"]
    assert merge([" [ 1 , 2 ] ", "[2,3)"]) == ["[1,3)"]
