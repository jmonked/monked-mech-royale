"""CrossHair `cover --coverage_type=path` examples for the v72 kernel (generated; regression pins).
Inputs include inf/nan on purpose: v72_bounded clamps them into game ranges first."""
from crosshair_props import v72_bounded

def test_v72_bounded():
    assert v72_bounded(1.0, 1.0, 1.0, 0.0, 0, 3.141592653589793, -3.141592653589793, 0.0, True, float("inf"), 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 0.0) == [0.707106781, 0.707106781]

def test_v72_bounded_2():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, 0, -3.141592653589793, float("-inf"), 0.0, False, -3.141592653589793, 15.0, 400.0, -400.0, 400.0, -60.0, 60.0, 0.0) == [0.707106781, 0.707106781]

def test_v72_bounded_3():
    assert v72_bounded(-1.0, 1.0, 1.0, 1.0, 0, float("nan"), 3.141592653589793, 0.0, False, 3.141592653589793, -15.0, float("nan"), 0.0, 0.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_4():
    assert v72_bounded(float("inf"), 1.0, 1.0, 0.0, 0, 0.0, float("nan"), float("nan"), True, 3.141592653589793, float("inf"), 0.0, -30.0, 0.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_5():
    assert v72_bounded(-1.0, 1.0, -1.0, 1.0, 0, 0.0, 3.141592653589793, float("inf"), False, float("inf"), -15.0, 0.0, -400.0, 400.0, -60.0, -60.0, float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_6():
    assert v72_bounded(1.0, float("inf"), float("inf"), 1.0, 0, float("nan"), float("inf"), float("inf"), True, float("-inf"), 15.0, 30.0, 30.0, 0.0, 60.0, 60.0, 0.0) == [0.707106781, -0.707106781]

def test_v72_bounded_7():
    assert v72_bounded(1.0, float("inf"), 1.0, -1.0, 0, float("nan"), 0.0, 3.141592653589793, False, 0.0, 15.0, 400.0, 400.0, 400.0, float("inf"), 60.0, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_8():
    assert v72_bounded(0.0, 1.0, 1.0, 1.0, 0, float("nan"), float("-inf"), 3.141592653589793, False, 3.141592653589793, -15.0, 400.0, 400.0, 400.0, 60.0, -60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_9():
    assert v72_bounded(-1.0, float("inf"), 1.0, 1.0, -2, 3.141592653589793, 3.141592653589793, float("nan"), False, 0.0, 15.0, 400.0, 400.0, 400.0, -60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_10():
    assert v72_bounded(1.0, float("nan"), 1.0, -1.0, 0, float("nan"), 3.141592653589793, 3.141592653589793, True, 0.0, 0.0, 30.0, 30.0, float("nan"), 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_11():
    assert v72_bounded(float("inf"), 1.0, 1.0, 1.0, 0, 3.141592653589793, 0.0, 3.141592653589793, False, float("-inf"), 15.0, 30.0, 30.0, 0.0, 60.0, 60.0, float("inf")) == [-0.707106781, 0.707106781]

def test_v72_bounded_12():
    assert v72_bounded(1.0, -1.0, 1.0, 0.0, 0, 3.141592653589793, 0.0, 3.141592653589793, False, 3.141592653589793, 15.0, -400.0, float("nan"), 400.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_13():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("inf"), 0.0, -400.0, 400.0, 400.0, 0.0, 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_14():
    assert v72_bounded(1.0, 1.0, float("nan"), 1.0, 5, 3.141592653589793, 3.141592653589793, 0.0, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_15():
    assert v72_bounded(float("nan"), float("nan"), 1.0, -1.0, 0, float("-inf"), 3.141592653589793, float("nan"), True, 0.0, -15.0, -400.0, 0.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_16():
    assert v72_bounded(1.0, float("inf"), 1.0, -1.0, 0, float("nan"), 0.0, 3.141592653589793, False, 3.141592653589793, 15.0, 30.0, 30.0, float("nan"), 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_17():
    assert v72_bounded(0.0, 1.0, 1.0, -1.0, 0, 3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, -400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_18():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 0.0, 31.0, 31.0, 60.0, -60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_19():
    assert v72_bounded(1.0, -1.0, 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, float("inf"), True, float("nan"), 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_20():
    assert v72_bounded(0.0, 1.0, 0.5, 1.0, -1, float("inf"), 3.141592653589793, float("inf"), False, -3.141592653589793, 15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_21():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, 0, 3.141592653589793, float("nan"), -3.141592653589793, False, float("nan"), 15.0, -30.0, float("-inf"), 0.0, -60.0, 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_22():
    assert v72_bounded(0.5, float("-inf"), 1.0, 1.0, 0, 3.141592653589793, 0.0, -3.141592653589793, False, -3.141592653589793, 15.0, -400.0, 400.0, 400.0, 60.0, 60.0, 0.0) == [0.447213595, -0.894427191]

def test_v72_bounded_23():
    assert v72_bounded(float("inf"), -1.0, 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, -3.141592653589793, True, 0.0, float("inf"), 30.0, 0.0, 0.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_24():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, 0, float("nan"), float("inf"), float("inf"), False, float("nan"), 15.0, 400.0, -400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_25():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 0, float("nan"), float("-inf"), float("inf"), False, 3.141592653589793, 15.0, 30.0, 30.0, 0.0, 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_26():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), 4, float("nan"), float("inf"), 3.141592653589793, False, float("nan"), 15.0, 30.0, 0.0, 0.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_27():
    assert v72_bounded(1.0, 1.0, -1.0, 1.0, -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 31.0, 31.0, 31.0, 60.0, 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_28():
    assert v72_bounded(1.0, float("inf"), float("-inf"), 1.0, 0, float("inf"), 0.0, 3.141592653589793, False, float("nan"), float("nan"), -31.0, 31.0, 31.0, 60.0, 0.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_29():
    assert v72_bounded(1.0, 1.0, -1.0, 0.0, 4, -3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 0.0, 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_30():
    assert v72_bounded(-1.0, 1.0, 0.0, 0.0, 0, float("-inf"), 3.141592653589793, 3.141592653589793, False, float("inf"), 15.0, float("inf"), 400.0, 400.0, -60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_31():
    assert v72_bounded(1.0, 1.0, float("inf"), 1.0, 0, 3.141592653589793, float("inf"), float("inf"), True, float("-inf"), 15.0, -31.0, 31.0, 31.0, 60.0, float("nan"), 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_32():
    assert v72_bounded(-1.0, float("inf"), float("nan"), 1.0, -2, 3.141592653589793, float("nan"), float("inf"), True, 0.0, float("nan"), 31.0, 31.0, 31.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_33():
    assert v72_bounded(float("-inf"), float("inf"), 0.0, 1.0, 0, 3.141592653589793, 0.0, 3.141592653589793, True, float("nan"), 15.0, 400.0, 400.0, 400.0, 60.0, -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_34():
    assert v72_bounded(1.0, 0.0, float("inf"), -1.0, 0, 3.141592653589793, float("nan"), 0.0, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, -60.0, 60.0, float("inf")) == [1.0, 0.0]

def test_v72_bounded_35():
    assert v72_bounded(-1.0, float("nan"), 1.0, 1.0, -1, 3.141592653589793, 3.141592653589793, float("nan"), True, float("inf"), 15.0, -400.0, -400.0, 400.0, 0.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_36():
    assert v72_bounded(1.0, 1.0, -1.0, 0.0, 4, -3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, -0.5, 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_37():
    assert v72_bounded(float("inf"), 1.0, -1.0, float("nan"), 4, float("nan"), float("inf"), 3.141592653589793, True, 0.0, 15.0, float("nan"), 400.0, 400.0, -60.0, 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_38():
    assert v72_bounded(-1.0, 1.0, float("-inf"), 1.0, -1, float("nan"), 0.0, 3.141592653589793, False, float("inf"), 15.0, float("nan"), 30.0, float("nan"), 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_39():
    assert v72_bounded(1.0, 0.0, -1.0, 0.0, 4, -3.141592653589793, -3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 399.0, 400.0, 400.0, 60.0, 0.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_40():
    assert v72_bounded(1.0, 1.0, -1.0, 1.0, 4, -3.141592653589793, 3.141592653589793, -3.141592653589793, True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 0.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_41():
    assert v72_bounded(float("inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, 0.0, float("inf"), False, float("inf"), float("nan"), 399.0, 400.0, 400.0, 60.0, 60.0, 0.5) == [-0.0, -1.0]

def test_v72_bounded_42():
    assert v72_bounded(1.0, 0.0, 1.0, 0.0, 0, float("nan"), 3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("inf"), 400.0, 400.0, 400.0, 60.0, -60.0, 30.0) == [1.0, 0.0]

def test_v72_bounded_43():
    assert v72_bounded(1.0, 1.0, -1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, float("inf"), True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("nan"), 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_44():
    assert v72_bounded(1.0, float("-inf"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, float("nan"), 15.0, 400.0, 400.0, 400.0, 0.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_45():
    assert v72_bounded(float("inf"), -1.0, 1.0, 1.0, 0, float("nan"), 3.141592653589793, float("nan"), False, float("-inf"), 15.0, 31.0, -31.0, 31.0, -60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_46():
    assert v72_bounded(float("inf"), float("-inf"), 1.0, 1.0, 4, 3.141592653589793, float("nan"), float("nan"), True, float("-inf"), 15.0, 399.0, 400.0, 400.0, 60.0, 60.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_47():
    assert v72_bounded(float("inf"), 1.0, 0.5, -1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("nan"), -15.0, 30.0, 0.0, 0.0, -60.0, -60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_48():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 0, 0.0, float("inf"), 3.141592653589793, True, 3.141592653589793, 0.0, 0.0, 400.0, 400.0, 60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_49():
    assert v72_bounded(1.0, -1.0, 1.0, 1.0, 0, 3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, float("nan"), 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_50():
    assert v72_bounded(-1.0, 1.0, 0.0, 1.0, 0, float("inf"), -3.141592653589793, float("nan"), False, 3.141592653589793, float("nan"), 30.0, 30.0, float("nan"), 60.0, 60.0, 0.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_51():
    assert v72_bounded(1.0, 1.0, 1.0, float("inf"), 0, float("inf"), float("-inf"), 3.141592653589793, False, float("inf"), float("inf"), 400.0, 400.0, 400.0, 60.0, -60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_52():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, 0, float("inf"), 3.141592653589793, 3.141592653589793, False, float("inf"), 0.0, 400.0, float("inf"), 400.0, 60.0, 60.0, float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_53():
    assert v72_bounded(float("inf"), 1.0, 1.0, -1.0, 0, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, -30.0, -30.0, 0.0, -60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_54():
    assert v72_bounded(-1.0, 0.0, 1.0, 1.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 30.0, float("inf"), 0.0, 60.0, 60.0, 0.0) == [-1.0, 0.0]

def test_v72_bounded_55():
    assert v72_bounded(1.0, 0.0, float("nan"), float("inf"), -1, float("nan"), 3.141592653589793, float("inf"), False, float("inf"), 15.0, 399.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [1.0, 0.0]

def test_v72_bounded_56():
    assert v72_bounded(-1.0, float("nan"), 1.0, 1.0, 0, 0.0, 3.141592653589793, float("nan"), True, 3.141592653589793, 15.0, 400.0, float("nan"), 400.0, 60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_57():
    assert v72_bounded(float("inf"), 0.5, 1.0, float("inf"), 0, float("inf"), 3.141592653589793, 3.141592653589793, False, float("nan"), 15.0, 31.0, 31.0, 31.0, 60.0, 60.0, 30.0) == [-0.894427191, 0.447213595]

def test_v72_bounded_58():
    assert v72_bounded(1.0, 1.0, 1.0, -1.0, 5, 3.141592653589793, float("nan"), -3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_59():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 4, 3.141592653589793, 3.141592653589793, float("-inf"), False, float("-inf"), 15.0, 30.0, 30.0, 0.0, 60.0, 60.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_60():
    assert v72_bounded(-1.0, 1.0, 1.0, 1.0, 0, -3.141592653589793, -3.141592653589793, 3.141592653589793, False, float("nan"), 0.0, -400.0, 400.0, 400.0, 0.0, -60.0, float("inf")) == [-0.707106781, 0.707106781]

def test_v72_bounded_61():
    assert v72_bounded(1.0, 0.5, float("nan"), 1.0, 0, float("inf"), 3.141592653589793, 3.141592653589793, False, float("nan"), float("inf"), 400.0, 400.0, 400.0, 60.0, 0.0, 30.0) == [0.894427191, 0.447213595]

def test_v72_bounded_62():
    assert v72_bounded(1.0, float("nan"), 1.0, 1.0, -1, 0.0, 3.141592653589793, float("nan"), False, float("-inf"), -15.0, 400.0, -400.0, 400.0, 60.0, float("inf"), float("-inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_63():
    assert v72_bounded(1.0, 1.0, 1.0, -1.0, 0, 3.141592653589793, 3.141592653589793, float("-inf"), False, float("nan"), 15.0, -31.0, 0.0, 31.0, float("inf"), 60.0, float("-inf")) == [0.707106781, 0.707106781]

def test_v72_bounded_64():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, 0, float("nan"), float("nan"), float("nan"), True, 3.141592653589793, 15.0, -30.0, 30.0, 0.0, float("inf"), 0.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_65():
    assert v72_bounded(float("nan"), -1.0, -1.0, 1.0, 0, float("inf"), float("inf"), float("nan"), False, 3.141592653589793, 15.0, -400.0, -400.0, 400.0, 60.0, float("inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_66():
    assert v72_bounded(1.0, 0.5, 1.0, 1.0, 0, float("-inf"), float("inf"), 3.141592653589793, True, 3.141592653589793, float("inf"), 400.0, 400.0, 400.0, 60.0, float("inf"), 30.0) == [0.894427191, 0.447213595]

def test_v72_bounded_67():
    assert v72_bounded(float("nan"), 0.5, -1.0, 1.0, 0, float("inf"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, -400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.894427191, 0.447213595]

def test_v72_bounded_68():
    assert v72_bounded(float("inf"), float("inf"), 1.0, -1.0, 0, 3.141592653589793, float("inf"), 3.141592653589793, False, float("inf"), 15.0, 400.0, 0.0, 400.0, 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_69():
    assert v72_bounded(1.0, 0.5, -1.0, 1.0, 0, -3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, -15.0, -400.0, 400.0, 400.0, float("nan"), 60.0, 30.0) == [0.894427191, 0.447213595]

def test_v72_bounded_70():
    assert v72_bounded(-1.0, float("nan"), 1.0, -1.0, 0, 3.141592653589793, 0.0, float("nan"), True, 3.141592653589793, -15.0, float("inf"), 400.0, 400.0, 60.0, float("inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_71():
    assert v72_bounded(1.0, 1.0, 1.0, -1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, -3.141592653589793, 15.0, 31.0, float("inf"), 31.0, 60.0, -60.0, 0.5) == [0.707106781, 0.707106781]

def test_v72_bounded_72():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 4, float("nan"), float("inf"), float("inf"), False, float("-inf"), -15.0, -30.0, 30.0, 0.0, -60.0, -60.0, float("nan")) == [0.0, 1.0]

def test_v72_bounded_73():
    assert v72_bounded(1.0, float("nan"), float("-inf"), -1.0, 0, 3.141592653589793, 0.0, -3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_74():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), 0, float("inf"), float("inf"), float("nan"), True, 3.141592653589793, 15.0, 30.0, 30.0, 0.0, float("nan"), 60.0, 30.0) == [1.0, 0.0]

def test_v72_bounded_75():
    assert v72_bounded(1.0, float("inf"), 1.0, -1.0, 0, float("inf"), float("inf"), 3.141592653589793, True, 3.141592653589793, 0.0, 400.0, -400.0, 400.0, 60.0, float("inf"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_76():
    assert v72_bounded(float("inf"), 1.0, 0.0, 1.0, 0, 0.0, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("inf"), float("nan"), 30.0, 0.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_77():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 5, float("inf"), 3.141592653589793, float("inf"), False, float("inf"), 0.0, 30.0, 30.0, float("inf"), 60.0, 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_78():
    assert v72_bounded(float("inf"), float("inf"), 0.5, 1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, float("inf"), 15.0, 400.0, 399.0, 400.0, 60.0, 60.0, 0.25) == [0.0, 1.0]

def test_v72_bounded_79():
    assert v72_bounded(1.0, -1.0, -1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, -3.141592653589793, 15.0, 30.0, 0.0, float("nan"), -60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_80():
    assert v72_bounded(float("nan"), 1.0, -1.0, -1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, -3.141592653589793, 15.0, 31.0, 31.0, 31.0, 0.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_81():
    assert v72_bounded(float("inf"), 0.0, float("-inf"), -1.0, 0, float("inf"), 3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, -31.0, 31.0, 31.0, 60.0, 60.0, 30.0) == [-1.0, 0.0]

def test_v72_bounded_82():
    assert v72_bounded(1.0, float("nan"), float("nan"), -1.0, 0, 3.141592653589793, 3.141592653589793, 0.0, False, -3.141592653589793, -15.0, 399.0, 400.0, 400.0, 60.0, -60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_83():
    assert v72_bounded(float("inf"), float("nan"), 1.0, 1.0, 4, 3.141592653589793, float("inf"), float("nan"), False, float("inf"), 15.0, 31.0, 31.0, 31.0, 60.0, float("nan"), 30.0) == [0.0, 1.0]

def test_v72_bounded_84():
    assert v72_bounded(float("-inf"), float("inf"), 0.0, 0.0, 4, float("nan"), 3.141592653589793, float("nan"), False, float("inf"), float("inf"), 30.0, 30.0, 0.0, 60.0, 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_85():
    assert v72_bounded(float("-inf"), float("-inf"), 0.0, -1.0, 4, 3.141592653589793, 3.141592653589793, float("-inf"), False, float("-inf"), 15.0, 30.0, 30.0, 0.0, 60.0, 60.0, 0.5) == [0.0, -1.0]

def test_v72_bounded_86():
    assert v72_bounded(1.0, 0.0, -1.0, 0.0, 0, -3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 0.0, float("inf"), 30.0) == [1.0, 0.0]

def test_v72_bounded_87():
    assert v72_bounded(-1.0, 1.0, 1.0, 1.0, 0, float("inf"), -3.141592653589793, 3.141592653589793, False, -3.141592653589793, -15.0, 400.0, 400.0, 400.0, 60.0, float("-inf"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_88():
    assert v72_bounded(float("inf"), float("-inf"), -1.0, 1.0, 4, 0.0, float("inf"), 3.141592653589793, False, float("inf"), 15.0, 31.0, float("nan"), 31.0, float("nan"), 60.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_89():
    assert v72_bounded(float("inf"), float("inf"), 0.5, 1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, float("inf"), -15.0, 399.0, 400.0, 400.0, 60.0, 60.0, 0.25) == [0.0, 1.0]

def test_v72_bounded_90():
    assert v72_bounded(1.0, -1.0, float("inf"), 1.0, 0, -3.141592653589793, 3.141592653589793, -3.141592653589793, False, float("nan"), -15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_91():
    assert v72_bounded(float("-inf"), float("inf"), -1.0, float("inf"), 0, 3.141592653589793, 0.0, float("inf"), True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_92():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, -3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, float("inf")) == [0.707106781, 0.707106781]

def test_v72_bounded_93():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, -2, float("nan"), float("inf"), 3.141592653589793, True, 3.141592653589793, -15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_94():
    assert v72_bounded(1.0, -1.0, -1.0, 1.0, 0, 3.141592653589793, -3.141592653589793, -3.141592653589793, False, float("-inf"), 15.0, 400.0, 400.0, 400.0, -60.0, 60.0, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_95():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, 1.0, 0, float("nan"), float("-inf"), -3.141592653589793, False, 3.141592653589793, 15.0, 31.0, 31.0, 31.0, 60.0, -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_96():
    assert v72_bounded(float("inf"), 0.0, 1.0, float("nan"), 4, float("nan"), 3.141592653589793, float("inf"), False, float("inf"), 15.0, 30.0, -30.0, float("inf"), 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_97():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 0.0, 4, 3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, 30.0, 30.0, 0.0, 60.0, 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_98():
    assert v72_bounded(float("-inf"), float("nan"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 0.0, 15.0, 31.0, 31.0, 31.0, 60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_99():
    assert v72_bounded(1.0, 1.0, 1.0, float("nan"), 4, 3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, 30.0, 30.0, float("nan"), -60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_100():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 4, 3.141592653589793, float("inf"), -3.141592653589793, False, float("-inf"), 15.0, -400.0, 400.0, 400.0, 60.0, 60.0, 0.5) == [0.0, 1.0]

def test_v72_bounded_101():
    assert v72_bounded(float("inf"), float("nan"), 1.0, 1.0, 0, 3.141592653589793, float("-inf"), float("-inf"), True, float("nan"), float("-inf"), -30.0, 30.0, 0.0, -60.0, 60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_102():
    assert v72_bounded(float("-inf"), 1.0, float("inf"), float("inf"), 0, float("inf"), float("nan"), float("-inf"), False, float("inf"), 15.0, -400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_103():
    assert v72_bounded(float("-inf"), float("inf"), 0.0, -1.0, 4, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, -400.0, 400.0, 400.0, 0.0, 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_104():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 0, 3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, 31.0, 31.0, 31.0, 0.0, -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_105():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 0, float("nan"), float("inf"), 3.141592653589793, True, float("-inf"), float("inf"), 400.0, 400.0, 400.0, -60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_106():
    assert v72_bounded(1.0, float("-inf"), 1.0, 1.0, 0, float("inf"), 3.141592653589793, float("inf"), False, float("inf"), float("inf"), float("nan"), 400.0, 400.0, 60.0, -60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_107():
    assert v72_bounded(float("-inf"), float("inf"), 0.5, 1.0, 4, 3.141592653589793, 3.141592653589793, float("-inf"), False, float("-inf"), 15.0, 399.0, 400.0, 400.0, 60.0, 60.0, 0.25) == [0.0, 1.0]

def test_v72_bounded_108():
    assert v72_bounded(float("inf"), 0.0, 1.0, float("-inf"), 4, float("inf"), 3.141592653589793, 3.141592653589793, False, float("nan"), 15.0, 30.0, 0.0, 0.0, 0.0, 60.0, float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_109():
    assert v72_bounded(-1.0, 0.0, float("inf"), 1.0, 0, 3.141592653589793, 3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, 0.0) == [-1.0, 0.0]

def test_v72_bounded_110():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, 0, -3.141592653589793, float("inf"), 3.141592653589793, False, 0.0, 15.0, float("inf"), 30.0, 0.0, float("-inf"), 60.0, 0.5) == [-0.707106781, 0.707106781]

def test_v72_bounded_111():
    assert v72_bounded(1.0, float("inf"), float("inf"), 1.0, 4, float("nan"), float("inf"), float("inf"), False, -3.141592653589793, 15.0, float("-inf"), 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.0, 1.0]

def test_v72_bounded_112():
    assert v72_bounded(1.0, 1.0, float("inf"), 1.0, 0, 3.141592653589793, 3.141592653589793, -3.141592653589793, True, 0.0, float("inf"), 400.0, 400.0, 400.0, 60.0, -60.0, float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_113():
    assert v72_bounded(1.0, 0.5, float("nan"), 1.0, 0, 3.141592653589793, 3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, float("inf")) == [0.894427191, 0.447213595]

def test_v72_bounded_114():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), 3.141592653589793, float("nan"), True, 3.141592653589793, 15.0, float("-inf"), 30.0, 0.0, 60.0, 60.0, 0.0) == [0.0, -1.0]

def test_v72_bounded_115():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, 0, float("inf"), -3.141592653589793, 3.141592653589793, False, -3.141592653589793, 15.0, 400.0, float("nan"), 400.0, float("nan"), 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_116():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, -1, float("inf"), 3.141592653589793, 3.141592653589793, False, float("inf"), -15.0, -400.0, 400.0, 400.0, 60.0, -60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_117():
    assert v72_bounded(float("inf"), float("inf"), 1.0, -1.0, 4, 3.141592653589793, 3.141592653589793, float("nan"), False, float("inf"), 15.0, float("nan"), 30.0, 0.0, 60.0, 60.0, 0.5) == [-0.0, -1.0]

def test_v72_bounded_118():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 0, 3.141592653589793, float("nan"), float("-inf"), False, float("nan"), 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_119():
    assert v72_bounded(float("inf"), 0.5, 1.0, float("nan"), 4, float("nan"), float("inf"), 3.141592653589793, False, float("nan"), 15.0, 400.0, 400.0, 400.0, 60.0, -60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_120():
    assert v72_bounded(float("inf"), float("-inf"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, float("-inf"), False, float("-inf"), -15.0, -400.0, 400.0, 400.0, 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_121():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, 0, -3.141592653589793, float("-inf"), 3.141592653589793, False, 3.141592653589793, float("nan"), float("inf"), 400.0, 400.0, 60.0, -60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_122():
    assert v72_bounded(float("nan"), 0.0, float("nan"), 1.0, 0, float("nan"), float("-inf"), 3.141592653589793, False, 3.141592653589793, 0.0, 30.0, 30.0, 0.0, 60.0, -60.0, float("nan")) == [-1.0, 0.0]

def test_v72_bounded_123():
    assert v72_bounded(1.0, 1.0, float("nan"), 1.0, -1, 3.141592653589793, float("inf"), 3.141592653589793, False, float("nan"), -15.0, 30.0, 30.0, float("inf"), 0.0, 60.0, float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_124():
    assert v72_bounded(float("nan"), 1.0, 1.0, -1.0, -1, 3.141592653589793, -3.141592653589793, float("-inf"), False, float("inf"), 15.0, 400.0, 400.0, 400.0, -60.0, -60.0, float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_125():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, -15.0, float("nan"), 30.0, 0.0, 60.0, 60.0, 0.0) == [0.0, -1.0]

def test_v72_bounded_126():
    assert v72_bounded(-1.0, 1.0, float("nan"), float("nan"), 0, 3.141592653589793, 3.141592653589793, 0.0, False, 3.141592653589793, 15.0, 400.0, -400.0, 400.0, float("inf"), 60.0, 0.5) == [-0.707106781, 0.707106781]

def test_v72_bounded_127():
    assert v72_bounded(1.0, float("nan"), 1.0, float("inf"), 4, 3.141592653589793, float("nan"), 3.141592653589793, True, 3.141592653589793, 15.0, 400.0, -400.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_128():
    assert v72_bounded(-1.0, 0.0, float("nan"), 1.0, 0, 3.141592653589793, 3.141592653589793, float("-inf"), True, float("nan"), 15.0, -31.0, float("inf"), 31.0, 60.0, float("nan"), 0.5) == [-1.0, 0.0]

def test_v72_bounded_129():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, -1, float("inf"), -3.141592653589793, 3.141592653589793, False, -3.141592653589793, -15.0, 30.0, float("-inf"), 0.0, 60.0, -60.0, float("-inf")) == [0.707106781, 0.707106781]

def test_v72_bounded_130():
    assert v72_bounded(0.0, float("inf"), 1.0, 0.0, -1, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, -60.0, 60.0, float("nan")) == [0.0, -1.0]

def test_v72_bounded_131():
    assert v72_bounded(1.0, float("inf"), float("-inf"), 1.0, 0, 3.141592653589793, float("nan"), float("-inf"), True, 3.141592653589793, float("nan"), -31.0, 31.0, 31.0, 60.0, 60.0, 0.0) == [0.707106781, -0.707106781]

def test_v72_bounded_132():
    assert v72_bounded(float("inf"), 1.0, float("inf"), -1.0, 4, 0.0, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, -400.0, 400.0, 400.0, 60.0, float("inf"), 30.0) == [-0.0, -1.0]

def test_v72_bounded_133():
    assert v72_bounded(1.0, 1.0, float("nan"), 1.0, 4, float("nan"), -3.141592653589793, float("inf"), True, 3.141592653589793, 15.0, float("nan"), float("inf"), 400.0, 60.0, -60.0, 30.0) == [-0.0, 1.0]

def test_v72_bounded_134():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, float("nan"), 31.0, 31.0, 60.0, 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_135():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 0, float("nan"), float("inf"), 3.141592653589793, True, 3.141592653589793, 15.0, float("nan"), -31.0, 31.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_136():
    assert v72_bounded(0.0, float("nan"), 1.0, -1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("inf"), 15.0, float("-inf"), -400.0, 400.0, 60.0, 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_137():
    assert v72_bounded(float("inf"), 1.0, float("inf"), -1.0, 0, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, float("nan"), 31.0, 31.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_138():
    assert v72_bounded(1.0, float("inf"), float("inf"), 1.0, 0, 3.141592653589793, float("inf"), float("inf"), False, 3.141592653589793, 15.0, -31.0, 31.0, 31.0, 60.0, float("nan"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_139():
    assert v72_bounded(1.0, float("-inf"), 1.0, float("inf"), 4, float("inf"), 0.0, 3.141592653589793, False, 3.141592653589793, 15.0, 30.0, -30.0, float("nan"), 60.0, float("inf"), 30.0) == [-0.0, -1.0]

def test_v72_bounded_140():
    assert v72_bounded(float("-inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, -3.141592653589793, float("inf"), True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 0.5) == [-0.0, -1.0]

def test_v72_bounded_141():
    assert v72_bounded(float("inf"), float("inf"), 1.0, float("nan"), 0, 3.141592653589793, 0.0, float("-inf"), False, 3.141592653589793, -15.0, float("nan"), 0.0, 400.0, 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_142():
    assert v72_bounded(0.0, float("-inf"), float("inf"), float("inf"), 0, float("nan"), -3.141592653589793, float("inf"), True, float("nan"), -15.0, 400.0, 400.0, 400.0, -60.0, 60.0, 0.5) == [0.0, -1.0]

def test_v72_bounded_143():
    assert v72_bounded(float("inf"), 1.0, 1.0, float("-inf"), -1, float("inf"), float("inf"), float("nan"), False, float("inf"), 15.0, float("inf"), -30.0, float("inf"), 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_144():
    assert v72_bounded(float("nan"), float("inf"), 0.5, 1.0, 0, float("nan"), float("inf"), -3.141592653589793, True, 3.141592653589793, 15.0, -30.0, -30.0, 0.0, float("nan"), 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_145():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("inf"), 3.141592653589793, float("-inf"), True, 3.141592653589793, 15.0, 31.0, 31.0, 31.0, 60.0, float("nan"), 30.0) == [0.0, -1.0]

def test_v72_bounded_146():
    assert v72_bounded(float("-inf"), float("nan"), -1.0, 1.0, 0, float("inf"), float("nan"), float("inf"), False, float("nan"), 15.0, 30.0, 30.0, float("inf"), float("nan"), -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_147():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, -1.0, 5, float("nan"), float("nan"), float("-inf"), False, 3.141592653589793, 15.0, float("nan"), -400.0, 400.0, 60.0, 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_148():
    assert v72_bounded(float("-inf"), -1.0, 1.0, 1.0, 0, float("nan"), float("nan"), 3.141592653589793, False, 3.141592653589793, float("inf"), 30.0, 30.0, float("nan"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_149():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 4, 3.141592653589793, float("nan"), -3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, -60.0, 0.5) == [0.0, 1.0]

def test_v72_bounded_150():
    assert v72_bounded(float("inf"), 1.0, 1.0, -1.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 30.0, -30.0, 0.0, 0.0, 60.0, float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_151():
    assert v72_bounded(1.0, 1.0, 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, -3.141592653589793, False, 3.141592653589793, -15.0, 30.0, float("inf"), float("nan"), 60.0, 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_152():
    assert v72_bounded(1.0, 1.0, -1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, float("nan"), 0.0, 400.0, float("nan"), -60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_153():
    assert v72_bounded(1.0, 1.0, -1.0, 0.0, 0, float("nan"), float("nan"), 3.141592653589793, False, -3.141592653589793, 15.0, 30.0, 30.0, float("-inf"), float("inf"), float("-inf"), 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_154():
    assert v72_bounded(float("inf"), float("nan"), float("nan"), 1.0, 4, float("inf"), -3.141592653589793, 0.0, True, 3.141592653589793, -15.0, -30.0, 30.0, 0.0, -60.0, float("inf"), 30.0) == [-0.0, 1.0]

def test_v72_bounded_155():
    assert v72_bounded(float("inf"), float("nan"), 1.0, float("nan"), 0, float("inf"), 3.141592653589793, 3.141592653589793, True, float("inf"), 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_156():
    assert v72_bounded(0.0, -1.0, float("-inf"), 1.0, -1, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("nan"), 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_157():
    assert v72_bounded(float("nan"), 1.0, -1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, float("inf"), 400.0, 400.0, 0.0, 60.0, 0.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_158():
    assert v72_bounded(1.0, float("nan"), 1.0, 1.0, 4, 3.141592653589793, 3.141592653589793, float("inf"), True, 3.141592653589793, -9.035533905932738, 400.0, 0.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_159():
    assert v72_bounded(1.0, float("inf"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, -3.141592653589793, True, 3.141592653589793, 15.0, 29.0, 30.0, float("nan"), 60.0, -60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_160():
    assert v72_bounded(float("inf"), -1.0, float("inf"), -1.0, 0, float("nan"), float("inf"), -3.141592653589793, False, 3.141592653589793, 15.0, float("nan"), 31.0, 31.0, 60.0, 0.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_161():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, 0.0, 4, 3.141592653589793, float("inf"), float("inf"), False, 3.141592653589793, 15.0, 30.0, 30.0, float("nan"), 60.0, -60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_162():
    assert v72_bounded(1.0, -1.0, float("nan"), float("inf"), -2, float("nan"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, -400.0, 400.0, 0.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_163():
    assert v72_bounded(float("-inf"), float("inf"), 0.5, 1.0, 4, 3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, -60.0, 0.25) == [0.0, 1.0]

def test_v72_bounded_164():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 0, 3.141592653589793, float("inf"), 3.141592653589793, True, float("nan"), 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_165():
    assert v72_bounded(float("inf"), float("nan"), 1.0, -1.0, -2, 3.141592653589793, -3.141592653589793, float("inf"), False, float("inf"), -15.0, 30.0, 0.0, float("nan"), 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_166():
    assert v72_bounded(float("nan"), float("inf"), 1.0, 1.0, -1, -3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_167():
    assert v72_bounded(1.0, float("-inf"), 1.0, float("nan"), 0, float("nan"), -3.141592653589793, -3.141592653589793, True, 0.0, 15.0, float("nan"), 30.0, float("nan"), -60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_168():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), float("inf"), 4, float("inf"), 3.141592653589793, float("nan"), True, 0.0, 15.0, float("nan"), 30.0, 0.0, 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_169():
    assert v72_bounded(float("inf"), 0.5, 1.0, float("nan"), -1, float("-inf"), float("-inf"), float("inf"), False, float("nan"), float("inf"), 400.0, float("-inf"), 400.0, 60.0, 60.0, 0.0) == [-0.894427191, 0.447213595]

def test_v72_bounded_170():
    assert v72_bounded(0.5, float("inf"), 1.0, float("nan"), 0, float("-inf"), float("-inf"), float("inf"), False, float("-inf"), 15.0, float("nan"), 400.0, 400.0, float("inf"), 60.0, 30.0) == [0.447213595, -0.894427191]

def test_v72_bounded_171():
    assert v72_bounded(float("nan"), 1.0, 1.0, 1.0, 4, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, float("nan"), 0.0) == [0.0, 1.0]

def test_v72_bounded_172():
    assert v72_bounded(float("-inf"), float("nan"), -1.0, 1.0, -1, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, 31.0, float("inf"), 31.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_173():
    assert v72_bounded(1.0, float("inf"), -1.0, 1.0, 0, 3.141592653589793, -3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("-inf"), -60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_174():
    assert v72_bounded(1.0, float("inf"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, -3.141592653589793, False, 3.141592653589793, 15.0, 30.0, 30.0, float("nan"), -60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_175():
    assert v72_bounded(float("inf"), float("inf"), 1.0, -1.0, 0, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, float("-inf"), 400.0, 400.0, 60.0, 60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_176():
    assert v72_bounded(1.0, 1.0, float("inf"), float("inf"), 0, 3.141592653589793, float("-inf"), float("nan"), False, float("inf"), float("inf"), 30.0, 30.0, 0.0, 60.0, 60.0, float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_177():
    assert v72_bounded(float("inf"), float("inf"), -1.0, 1.0, -1, float("nan"), 3.141592653589793, float("-inf"), False, 3.141592653589793, 15.0, float("nan"), 31.0, 31.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_178():
    assert v72_bounded(1.0, 0.5, float("nan"), 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 31.0, 31.0, 31.0, -60.0, 60.0, float("-inf")) == [0.894427191, 0.447213595]

def test_v72_bounded_179():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), 4, 3.141592653589793, float("nan"), float("inf"), False, 3.141592653589793, float("nan"), 400.0, 400.0, 400.0, 60.0, 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_180():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, -1.0, 4, float("nan"), float("inf"), float("inf"), False, float("-inf"), 15.0, float("nan"), float("nan"), 400.0, 60.0, -60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_181():
    assert v72_bounded(float("-inf"), float("-inf"), 0.0, -1.0, 0, 3.141592653589793, 3.141592653589793, float("-inf"), True, float("nan"), -15.0, 30.0, 30.0, 0.0, 60.0, float("inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_182():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, 0, float("inf"), 3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, float("nan"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_183():
    assert v72_bounded(float("nan"), 0.0, 1.0, 1.0, 4, 3.141592653589793, 3.141592653589793, float("-inf"), True, 3.141592653589793, -6.768807716974935, 400.0, 0.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_184():
    assert v72_bounded(float("inf"), float("-inf"), 1.0, 1.0, 4, 3.141592653589793, float("nan"), -3.141592653589793, True, float("inf"), -15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, 0.5) == [0.0, 1.0]

def test_v72_bounded_185():
    assert v72_bounded(float("inf"), float("-inf"), float("inf"), 1.0, 0, float("inf"), float("nan"), float("inf"), False, -3.141592653589793, 0.0, 30.0, 30.0, 0.0, float("nan"), 0.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_186():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, float("inf"), True, float("inf"), 15.0, 400.0, 400.0, 400.0, 60.0, float("inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_187():
    assert v72_bounded(-1.0, float("inf"), float("inf"), float("nan"), 0, float("nan"), float("inf"), float("inf"), False, 3.141592653589793, 15.0, 30.0, 30.0, 0.0, float("nan"), 60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_188():
    assert v72_bounded(1.0, float("inf"), 1.0, float("nan"), 0, float("inf"), float("nan"), float("inf"), True, 3.141592653589793, 0.0, 400.0, 400.0, 400.0, 60.0, float("inf"), float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_189():
    assert v72_bounded(1.0, -1.0, 1.0, 1.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, -3.141592653589793, float("inf"), 400.0, float("nan"), 400.0, 60.0, 60.0, 0.5) == [0.707106781, -0.707106781]

def test_v72_bounded_190():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, 1.0, 4, float("nan"), float("-inf"), float("inf"), False, float("nan"), float("nan"), 400.0, -400.0, 400.0, 60.0, 60.0, float("inf")) == [-0.0, 1.0]

def test_v72_bounded_191():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, 0.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, -5.5, -30.0, 30.0, 0.0, 60.0, float("nan"), 0.0) == [0.0, 1.0]

def test_v72_bounded_192():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, 3.141592653589793, float("nan"), float("nan"), True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, -60.0, float("nan"), 30.0) == [0.0, -1.0]

def test_v72_bounded_193():
    assert v72_bounded(float("-inf"), 0.0, -1.0, float("nan"), 4, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, float("nan"), 400.0, 400.0, 400.0, 0.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_194():
    assert v72_bounded(float("nan"), 1.0, 1.0, float("-inf"), 4, 3.141592653589793, float("inf"), float("nan"), False, 3.141592653589793, 15.0, 400.0, float("-inf"), 400.0, 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_195():
    assert v72_bounded(float("-inf"), float("inf"), 0.5, 1.0, 4, float("inf"), 3.141592653589793, -3.141592653589793, True, float("nan"), 15.0, 400.0, 400.0, 400.0, 60.0, float("nan"), 30.0) == [0.0, 1.0]

def test_v72_bounded_196():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, -1.0, 4, float("inf"), -3.141592653589793, 3.141592653589793, True, float("-inf"), 15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, 0.0) == [0.0, -1.0]

def test_v72_bounded_197():
    assert v72_bounded(float("inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, 3.141592653589793, float("inf"), True, float("-inf"), float("nan"), 399.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_198():
    assert v72_bounded(float("inf"), 1.0, float("inf"), -1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 0.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_199():
    assert v72_bounded(float("nan"), float("inf"), -1.0, -1.0, 0, 3.141592653589793, -3.141592653589793, float("nan"), False, -3.141592653589793, 15.0, 399.0, 400.0, 400.0, -60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_200():
    assert v72_bounded(float("inf"), 1.0, 1.0, float("nan"), -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, float("inf"), 15.0, 31.0, 31.0, 31.0, 60.0, 60.0, float("inf")) == [-0.707106781, 0.707106781]

def test_v72_bounded_201():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 0, float("nan"), float("nan"), float("nan"), False, 3.141592653589793, 15.0, 400.0, float("nan"), 400.0, 60.0, float("inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_202():
    assert v72_bounded(-1.0, 1.0, 1.0, 1.0, 4, -3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, float("inf"), -400.0, 400.0, -60.0, 60.0, float("inf")) == [0.0, 1.0]

def test_v72_bounded_203():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, -1.0, 0, float("inf"), 3.141592653589793, float("inf"), False, float("nan"), 15.0, 0.0, 0.0, float("nan"), -60.0, -60.0, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_204():
    assert v72_bounded(float("-inf"), float("-inf"), 0.0, -1.0, 4, float("nan"), 0.0, 3.141592653589793, False, 3.141592653589793, -15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, float("inf")) == [0.0, -1.0]

def test_v72_bounded_205():
    assert v72_bounded(float("inf"), 1.0, float("-inf"), float("inf"), 0, float("inf"), float("nan"), float("inf"), False, 3.141592653589793, 15.0, float("inf"), -30.0, 0.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_206():
    assert v72_bounded(float("inf"), float("nan"), float("inf"), float("nan"), -1, float("nan"), 3.141592653589793, 0.0, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_207():
    assert v72_bounded(float("-inf"), float("inf"), 0.5, 1.0, 4, 3.141592653589793, 3.141592653589793, float("-inf"), True, float("nan"), 15.0, 400.0, 400.0, 400.0, 60.0, -60.0, float("nan")) == [0.0, 1.0]

def test_v72_bounded_208():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), 1.0, -1, float("nan"), 3.141592653589793, 3.141592653589793, True, float("inf"), 0.0, -30.0, 0.0, float("nan"), 0.0, 0.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_209():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 0, 3.141592653589793, float("inf"), 3.141592653589793, False, float("nan"), float("inf"), 0.0, 0.0, float("inf"), 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_210():
    assert v72_bounded(1.0, float("-inf"), 1.0, float("nan"), 0, float("nan"), float("-inf"), 3.141592653589793, True, float("inf"), 15.0, 31.0, float("nan"), 31.0, float("-inf"), 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_211():
    assert v72_bounded(float("-inf"), float("inf"), 0.0, -1.0, 4, float("inf"), 3.141592653589793, 3.141592653589793, False, float("-inf"), 15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_212():
    assert v72_bounded(float("nan"), 0.0, 1.0, 1.0, -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, -3.141592653589793, float("nan"), 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-1.0, 0.0]

def test_v72_bounded_213():
    assert v72_bounded(1.0, 1.0, float("nan"), float("-inf"), 4, 3.141592653589793, float("inf"), float("inf"), False, float("inf"), float("inf"), 400.0, 0.0, 400.0, 60.0, float("nan"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_214():
    assert v72_bounded(float("-inf"), float("nan"), 1.0, 1.0, 5, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, 30.0, 30.0, float("inf"), 60.0, 60.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_215():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, 0, 3.141592653589793, float("nan"), float("-inf"), False, float("inf"), float("nan"), -30.0, 30.0, float("inf"), 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_216():
    assert v72_bounded(0.5, float("nan"), float("nan"), 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("inf"), -15.0, 30.0, 30.0, 0.0, 60.0, float("-inf"), 30.0) == [0.447213595, -0.894427191]

def test_v72_bounded_217():
    assert v72_bounded(float("inf"), -1.0, 1.0, -1.0, 4, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("-inf"), 15.0, 30.0, 0.0, float("inf"), 60.0, float("inf"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_218():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, -15.0, -30.0, 30.0, 0.0, 60.0, float("nan"), 30.0) == [0.0, -1.0]

def test_v72_bounded_219():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), 4, 3.141592653589793, float("nan"), 3.141592653589793, True, 3.141592653589793, float("inf"), -30.0, -30.0, 0.0, 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_220():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, -400.0, 400.0, 400.0, -60.0, float("nan"), 30.0) == [0.0, -1.0]

def test_v72_bounded_221():
    assert v72_bounded(float("nan"), 1.0, float("inf"), 1.0, -1, 3.141592653589793, 3.141592653589793, float("-inf"), False, -3.141592653589793, 15.0, 30.0, 0.0, 0.0, 60.0, float("inf"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_222():
    assert v72_bounded(float("nan"), 1.0, 1.0, float("nan"), -1, float("nan"), float("inf"), float("nan"), False, -3.141592653589793, float("nan"), float("nan"), -31.0, 31.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_223():
    assert v72_bounded(float("inf"), float("-inf"), 1.0, 0.0, -2, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, 0.0, -30.0, 30.0, 0.0, -60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_224():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), float("inf"), -3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("-inf"), 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_225():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), 1.0, 0, float("-inf"), float("nan"), 3.141592653589793, True, float("inf"), 15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_226():
    assert v72_bounded(1.0, -1.0, 1.0, -1.0, 0, -3.141592653589793, 3.141592653589793, 3.141592653589793, True, -3.141592653589793, 15.0, 400.0, 0.0, 400.0, float("-inf"), -60.0, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_227():
    assert v72_bounded(float("nan"), 0.0, float("nan"), float("nan"), 0, float("nan"), float("-inf"), float("inf"), False, -3.141592653589793, 15.0, 31.0, 31.0, 31.0, 60.0, float("nan"), 30.0) == [-1.0, 0.0]

def test_v72_bounded_228():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 5, 3.141592653589793, float("nan"), float("-inf"), False, float("inf"), float("nan"), 400.0, float("nan"), 400.0, 60.0, 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_229():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, 1.0, 4, -3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, 15.0, -30.0, 30.0, 0.0, 60.0, 60.0, float("nan")) == [0.0, 1.0]

def test_v72_bounded_230():
    assert v72_bounded(float("-inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, -3.141592653589793, float("inf"), False, float("inf"), float("nan"), -400.0, 400.0, 400.0, 60.0, 60.0, 0.5) == [-0.0, -1.0]

def test_v72_bounded_231():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), 1.0, -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("inf"), 15.0, 30.0, -30.0, 0.0, 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_232():
    assert v72_bounded(1.0, float("inf"), 1.0, -1.0, -1, -3.141592653589793, -3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, float("inf"), 400.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_233():
    assert v72_bounded(float("inf"), 1.0, 1.0, 1.0, 5, 0.0, -3.141592653589793, 3.141592653589793, False, 3.141592653589793, -15.0, float("nan"), 400.0, 400.0, 60.0, float("inf"), float("nan")) == [0.0, 1.0]

def test_v72_bounded_234():
    assert v72_bounded(1.0, 1.0, -1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("inf"), 15.0, 400.0, 400.0, 400.0, float("inf"), float("nan"), float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_235():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, -3.141592653589793, -15.0, -30.0, 30.0, 0.0, 60.0, float("nan"), 30.0) == [0.0, -1.0]

def test_v72_bounded_236():
    assert v72_bounded(float("inf"), 1.0, 1.0, 1.0, -1, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("nan"), 400.0, 400.0, 400.0, 60.0, -60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_237():
    assert v72_bounded(float("-inf"), float("-inf"), float("-inf"), 1.0, 0, float("inf"), float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, -400.0, 400.0, 0.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_238():
    assert v72_bounded(float("nan"), 0.0, -1.0, float("inf"), 0, float("-inf"), 0.0, float("nan"), False, float("nan"), float("-inf"), 0.0, 0.0, float("nan"), -60.0, float("nan"), float("nan")) == [-1.0, 0.0]

def test_v72_bounded_239():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 4, float("inf"), 3.141592653589793, 3.141592653589793, False, float("inf"), 15.0, 31.0, float("nan"), 31.0, float("nan"), 60.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_240():
    assert v72_bounded(float("-inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, -3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, 30.0, 30.0, 0.0, 60.0, 60.0, float("nan")) == [-0.0, -1.0]

def test_v72_bounded_241():
    assert v72_bounded(float("nan"), float("inf"), float("inf"), -1.0, 4, float("nan"), float("-inf"), float("-inf"), False, 3.141592653589793, 15.0, float("inf"), 0.0, 31.0, -60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_242():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, -1, float("nan"), -3.141592653589793, float("-inf"), True, float("-inf"), float("inf"), -30.0, 30.0, float("inf"), 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_243():
    assert v72_bounded(float("inf"), 1.0, float("-inf"), 1.0, 0, float("inf"), float("nan"), float("-inf"), False, -3.141592653589793, 15.0, -30.0, 30.0, float("nan"), 60.0, float("nan"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_244():
    assert v72_bounded(1.0, float("-inf"), float("inf"), float("inf"), 0, 3.141592653589793, 0.0, 3.141592653589793, True, float("inf"), float("nan"), float("inf"), 31.0, 31.0, 0.0, -60.0, 0.0) == [0.707106781, -0.707106781]

def test_v72_bounded_245():
    assert v72_bounded(float("-inf"), float("inf"), 0.0, 0.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, 3.141592653589793, -15.0, 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_246():
    assert v72_bounded(float("inf"), 1.0, 1.0, float("nan"), 0, float("nan"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("nan"), 400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_247():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 0, -3.141592653589793, 3.141592653589793, float("inf"), True, -3.141592653589793, -15.0, 30.0, 30.0, float("-inf"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_248():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), -1, 3.141592653589793, float("nan"), 3.141592653589793, True, 3.141592653589793, 15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, 30.0) == [1.0, 0.0]

def test_v72_bounded_249():
    assert v72_bounded(float("-inf"), float("inf"), float("nan"), 1.0, -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("nan"), 0.0, 400.0, 400.0, 400.0, 0.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_250():
    assert v72_bounded(1.0, 1.0, 0.0, 0.0, 4, -3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, float("nan"), 30.0, float("inf"), 60.0, float("nan"), 30.0) == [0.0, 1.0]

def test_v72_bounded_251():
    assert v72_bounded(0.5, 1.0, float("inf"), float("nan"), -1, float("inf"), float("inf"), float("-inf"), True, 3.141592653589793, float("inf"), float("nan"), -400.0, 400.0, -60.0, 60.0, 30.0) == [0.447213595, 0.894427191]

def test_v72_bounded_252():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 0.0, 0, float("nan"), 3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, -30.0, float("nan"), 0.0, 60.0, float("-inf"), 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_253():
    assert v72_bounded(float("inf"), float("inf"), -1.0, 1.0, 0, 3.141592653589793, float("inf"), 3.141592653589793, True, float("-inf"), 0.0, float("inf"), 30.0, float("inf"), -60.0, 60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_254():
    assert v72_bounded(1.0, float("inf"), float("inf"), 0.0, 0, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, -15.0, 400.0, 400.0, 400.0, 60.0, 60.0, float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_255():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), 4, 3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, float("inf"), 400.0, -60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_256():
    assert v72_bounded(float("nan"), float("nan"), 1.0, float("inf"), -1, 3.141592653589793, 3.141592653589793, 0.0, False, float("inf"), 15.0, 30.0, float("inf"), 0.0, 60.0, float("-inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_257():
    assert v72_bounded(0.0, -1.0, float("inf"), float("nan"), -2, -3.141592653589793, float("inf"), float("nan"), False, float("nan"), float("nan"), float("nan"), -400.0, 400.0, 60.0, 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_258():
    assert v72_bounded(float("inf"), float("-inf"), 1.0, 1.0, 0, float("inf"), float("nan"), float("inf"), True, float("-inf"), float("nan"), 400.0, float("inf"), 400.0, 60.0, 0.0, float("-inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_259():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("inf"), 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, -60.0, float("nan"), 30.0) == [0.0, -1.0]

def test_v72_bounded_260():
    assert v72_bounded(float("nan"), float("inf"), 1.0, 1.0, 4, float("nan"), float("inf"), 3.141592653589793, True, float("inf"), 15.0, float("nan"), float("inf"), 0.0, 0.0, 60.0, float("-inf")) == [0.0, 1.0]

def test_v72_bounded_261():
    assert v72_bounded(float("inf"), 1.0, float("inf"), float("nan"), 0, 0.0, -3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, 60.0, float("inf")) == [-0.707106781, 0.707106781]

def test_v72_bounded_262():
    assert v72_bounded(1.0, float("inf"), float("inf"), float("nan"), 0, float("-inf"), -3.141592653589793, float("inf"), False, float("inf"), -15.0, float("inf"), 400.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_263():
    assert v72_bounded(float("-inf"), 1.0, -1.0, float("-inf"), 4, 3.141592653589793, float("inf"), 3.141592653589793, True, float("-inf"), -1.9644660940672622, 30.0, -30.0, 0.0, 60.0, 60.0, 0.5) == [0.0, 1.0]

def test_v72_bounded_264():
    assert v72_bounded(float("inf"), float("inf"), 0.5, 1.0, 5, 3.141592653589793, float("inf"), 3.141592653589793, False, float("inf"), 15.0, float("nan"), 0.0, float("nan"), -60.0, -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_265():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, 1.0, 0, float("inf"), 3.141592653589793, 3.141592653589793, True, float("inf"), -15.0, 30.0, -30.0, float("inf"), float("inf"), 60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_266():
    assert v72_bounded(1.0, float("nan"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, -30.0, 30.0, float("inf"), 60.0, float("inf"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_267():
    assert v72_bounded(1.0, -1.0, 1.0, float("inf"), 4, 3.141592653589793, -3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("inf"), float("nan"), 30.0, 0.0, -60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_268():
    assert v72_bounded(float("nan"), -1.0, 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 30.0, float("-inf"), float("inf"), 0.0, -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_269():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, -1.0, 0, float("nan"), float("inf"), float("inf"), False, float("-inf"), 15.0, float("nan"), float("-inf"), float("nan"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_270():
    assert v72_bounded(float("inf"), float("nan"), 1.0, -1.0, 4, float("-inf"), float("inf"), float("inf"), False, float("nan"), float("inf"), float("-inf"), 0.0, 400.0, 60.0, float("-inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_271():
    assert v72_bounded(1.0, float("inf"), float("nan"), 1.0, -1, -3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("nan"), 15.0, float("nan"), 400.0, 400.0, 60.0, -60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_272():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, -1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, float("nan"), 15.0, 31.0, float("inf"), 31.0, float("-inf"), 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_273():
    assert v72_bounded(float("inf"), float("inf"), -1.0, 1.0, 0, -3.141592653589793, float("inf"), 3.141592653589793, True, float("inf"), 15.0, 31.0, float("nan"), 31.0, float("-inf"), 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_274():
    assert v72_bounded(float("-inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, -3.141592653589793, float("-inf"), False, float("inf"), 15.0, float("nan"), 30.0, 0.0, float("nan"), 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_275():
    assert v72_bounded(float("-inf"), 1.0, 1.0, -1.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, True, -3.141592653589793, -15.0, -400.0, -400.0, 400.0, float("nan"), 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_276():
    assert v72_bounded(float("nan"), 1.0, float("-inf"), float("nan"), 0, 3.141592653589793, float("nan"), 3.141592653589793, False, 0.0, 15.0, float("nan"), float("-inf"), 400.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_277():
    assert v72_bounded(1.0, 1.0, float("nan"), 0.0, 0, 3.141592653589793, float("nan"), 3.141592653589793, False, -3.141592653589793, 15.0, 3.141592653589793, -30.0, float("nan"), 60.0, 60.0, 30.0) == [0.707106781, 0.707106781]

def test_v72_bounded_278():
    assert v72_bounded(float("inf"), float("nan"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, float("inf"), False, 3.141592653589793, -15.0, 400.0, -400.0, 400.0, -60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_279():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), float("inf"), float("inf"), False, float("-inf"), 15.0, float("nan"), float("-inf"), 400.0, 60.0, float("-inf"), 30.0) == [0.0, -1.0]

def test_v72_bounded_280():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), float("inf"), -3.141592653589793, False, 3.141592653589793, 15.0, float("nan"), -31.0, 31.0, 60.0, float("nan"), 30.0) == [0.0, -1.0]

def test_v72_bounded_281():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), float("inf"), float("-inf"), False, float("-inf"), 15.0, float("nan"), float("inf"), 400.0, 60.0, float("-inf"), 30.0) == [0.0, -1.0]

def test_v72_bounded_282():
    assert v72_bounded(float("inf"), float("inf"), 1.0, float("nan"), 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, float("nan"), 15.0, 400.0, 400.0, 400.0, -60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_283():
    assert v72_bounded(float("inf"), float("-inf"), float("inf"), 1.0, 0, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_284():
    assert v72_bounded(float("-inf"), float("nan"), 1.0, -1.0, -1, -3.141592653589793, -3.141592653589793, float("nan"), False, -3.141592653589793, 15.0, 30.0, 30.0, float("nan"), -60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_285():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 0, 3.141592653589793, float("inf"), float("nan"), False, 3.141592653589793, float("inf"), 400.0, -400.0, 400.0, float("inf"), 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_286():
    assert v72_bounded(float("inf"), 1.0, 1.0, float("inf"), 4, float("nan"), float("-inf"), 3.141592653589793, False, float("inf"), float("inf"), float("inf"), 30.0, float("inf"), 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_287():
    assert v72_bounded(float("inf"), float("nan"), 1.0, 1.0, -1, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, float("nan"), 15.0, 400.0, -400.0, 400.0, -60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_288():
    assert v72_bounded(float("nan"), 1.0, float("inf"), 1.0, 0, float("inf"), 3.141592653589793, float("nan"), False, -3.141592653589793, 15.0, 400.0, float("nan"), 400.0, -60.0, 60.0, float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_289():
    assert v72_bounded(float("inf"), float("inf"), 1.0, -1.0, -1, float("nan"), float("inf"), float("inf"), False, float("-inf"), 15.0, float("nan"), float("-inf"), 400.0, 60.0, float("-inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_290():
    assert v72_bounded(1.0, float("inf"), float("inf"), 1.0, 0, 3.141592653589793, float("inf"), float("nan"), False, -3.141592653589793, float("inf"), 400.0, 400.0, 400.0, float("inf"), 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_291():
    assert v72_bounded(float("inf"), -1.0, float("nan"), 1.0, 0, float("-inf"), float("inf"), float("inf"), False, float("-inf"), -15.0, -30.0, 30.0, float("-inf"), float("nan"), float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_292():
    assert v72_bounded(float("-inf"), float("-inf"), 0.0, 1.0, 4, 3.141592653589793, float("-inf"), 3.141592653589793, False, float("-inf"), 15.0, 30.0, 30.0, 0.0, float("nan"), 60.0, float("-inf")) == [0.0, 1.0]

def test_v72_bounded_293():
    assert v72_bounded(float("-inf"), float("inf"), 0.5, 1.0, 5, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 30.0, 30.0, float("nan"), 60.0, -60.0, 0.25) == [0.0, 1.0]

def test_v72_bounded_294():
    assert v72_bounded(float("inf"), 1.0, -1.0, float("-inf"), 5, 3.141592653589793, float("-inf"), float("inf"), True, 3.141592653589793, 15.0, -30.0, -30.0, float("nan"), 60.0, float("nan"), 30.0) == [-0.0, -1.0]

def test_v72_bounded_295():
    assert v72_bounded(1.0, float("-inf"), float("inf"), -1.0, 0, float("inf"), float("nan"), -3.141592653589793, True, float("nan"), 15.0, 30.0, float("inf"), 0.0, float("nan"), float("inf"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_296():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, 3.141592653589793, float("nan"), float("-inf"), False, float("inf"), float("nan"), 31.0, 31.0, 31.0, float("inf"), float("inf"), 0.5) == [0.0, -1.0]

def test_v72_bounded_297():
    assert v72_bounded(float("nan"), float("inf"), float("nan"), 1.0, 4, float("inf"), float("inf"), float("-inf"), False, 3.141592653589793, 15.0, float("inf"), 0.0, 31.0, -60.0, float("nan"), 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_298():
    assert v72_bounded(float("inf"), float("inf"), -1.0, 0.0, 0, float("inf"), float("inf"), float("inf"), False, 3.141592653589793, float("inf"), float("inf"), 30.0, float("nan"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_299():
    assert v72_bounded(1.0, float("nan"), -1.0, float("-inf"), 4, float("nan"), float("inf"), 3.141592653589793, True, 3.141592653589793, 15.0, 399.0, 400.0, 400.0, 60.0, float("nan"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_300():
    assert v72_bounded(float("inf"), 0.0, -1.0, float("-inf"), 6, 3.141592653589793, 3.141592653589793, -3.141592653589793, False, 3.141592653589793, 15.0, 30.0, 30.0, float("nan"), 60.0, 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_301():
    assert v72_bounded(1.0, float("nan"), float("inf"), 1.0, 0, float("-inf"), float("inf"), 3.141592653589793, False, float("inf"), float("nan"), float("nan"), 0.0, 400.0, float("-inf"), 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_302():
    assert v72_bounded(float("nan"), 1.0, 1.0, float("nan"), -1, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, float("-inf"), 0.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_303():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), 4, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("nan"), float("inf"), -30.0, 30.0, 0.0, 60.0, float("nan"), 0.0) == [-0.0, -1.0]

def test_v72_bounded_304():
    assert v72_bounded(float("-inf"), float("inf"), -1.0, 1.0, 4, 3.141592653589793, float("nan"), float("-inf"), False, float("inf"), float("nan"), 31.0, 31.0, 31.0, float("inf"), float("inf"), 0.5) == [0.0, 1.0]

def test_v72_bounded_305():
    assert v72_bounded(float("nan"), float("inf"), float("inf"), 1.0, 0, 3.141592653589793, float("inf"), float("inf"), False, 3.141592653589793, -15.0, 400.0, -400.0, 400.0, 0.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_306():
    assert v72_bounded(float("inf"), float("inf"), 1.0, float("nan"), 0, float("nan"), float("nan"), 3.141592653589793, False, float("-inf"), float("nan"), 31.0, 31.0, 31.0, 60.0, float("inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_307():
    assert v72_bounded(float("nan"), 1.0, 1.0, 1.0, 4, 3.141592653589793, 3.141592653589793, float("inf"), True, 3.141592653589793, -7.8439202462555855, float("nan"), 400.0, 400.0, 60.0, -60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_308():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, -1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, float("nan"), 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_309():
    assert v72_bounded(float("-inf"), float("nan"), 1.0, -1.0, 5, 3.141592653589793, -3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, float("nan"), 0.0, 0.0, 60.0, float("inf"), 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_310():
    assert v72_bounded(float("-inf"), -1.0, float("nan"), -1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, -400.0, -400.0, 400.0, float("nan"), 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_311():
    assert v72_bounded(float("nan"), float("inf"), 1.0, float("nan"), 0, 3.141592653589793, 3.141592653589793, float("inf"), False, 3.141592653589793, 0.0, -30.0, 30.0, 0.0, 60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_312():
    assert v72_bounded(1.0, float("nan"), float("nan"), 1.0, 0, 3.141592653589793, 0.0, float("nan"), True, 3.141592653589793, 0.0, float("nan"), float("nan"), float("nan"), 60.0, 60.0, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_313():
    assert v72_bounded(1.0, float("nan"), float("nan"), float("-inf"), 4, 3.141592653589793, float("inf"), 3.141592653589793, False, float("-inf"), 0.0, 400.0, 400.0, 400.0, 60.0, float("-inf"), 0.0) == [-0.0, -1.0]

def test_v72_bounded_314():
    assert v72_bounded(float("inf"), 1.0, float("-inf"), 1.0, 0, 3.141592653589793, float("nan"), float("-inf"), False, -3.141592653589793, float("nan"), 400.0, -400.0, 400.0, float("nan"), 60.0, 0.5) == [-0.707106781, 0.707106781]

def test_v72_bounded_315():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, 4, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, -15.0, 400.0, -400.0, 400.0, 60.0, float("inf"), 30.0) == [0.0, 1.0]

def test_v72_bounded_316():
    assert v72_bounded(float("inf"), -1.0, 1.0, float("nan"), 5, float("inf"), 3.141592653589793, 3.141592653589793, False, float("nan"), float("nan"), -400.0, -400.0, 400.0, 60.0, 60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_317():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 4, float("nan"), float("nan"), float("-inf"), False, 3.141592653589793, 15.0, float("inf"), 30.0, float("inf"), 60.0, 60.0, float("-inf")) == [0.0, -1.0]

def test_v72_bounded_318():
    assert v72_bounded(0.0, 1.0, -1.0, float("inf"), -1, 3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, float("nan"), 30.0, float("nan"), 0.0, -60.0, float("inf"), 30.0) == [0.0, 1.0]

def test_v72_bounded_319():
    assert v72_bounded(float("inf"), 1.0, 1.0, 1.0, -1, -3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("inf"), float("nan"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_320():
    assert v72_bounded(1.0, float("-inf"), float("inf"), 0.0, 0, float("inf"), 3.141592653589793, float("nan"), False, float("-inf"), -15.0, float("nan"), float("-inf"), float("nan"), 60.0, 60.0, 0.5) == [0.707106781, -0.707106781]

def test_v72_bounded_321():
    assert v72_bounded(1.0, float("inf"), float("inf"), 1.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 400.0, -400.0, 400.0, 60.0, float("nan"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_322():
    assert v72_bounded(float("inf"), float("-inf"), 1.0, 0.0, 4, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, -30.0, 30.0, float("-inf"), float("inf"), 0.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_323():
    assert v72_bounded(float("-inf"), 1.0, float("inf"), float("inf"), 0, float("inf"), 3.141592653589793, float("nan"), True, float("-inf"), 15.0, float("inf"), 30.0, float("inf"), 60.0, -60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_324():
    assert v72_bounded(float("nan"), 1.0, 0.5, 1.0, 0, 3.141592653589793, 3.141592653589793, -3.141592653589793, True, float("nan"), 15.0, float("inf"), float("nan"), 400.0, 60.0, float("-inf"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_325():
    assert v72_bounded(1.0, float("inf"), 1.0, 1.0, 0, -3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, float("nan"), 400.0, 400.0, -60.0, -60.0, float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_326():
    assert v72_bounded(float("-inf"), 1.0, 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, -3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("nan"), 60.0, float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_327():
    assert v72_bounded(float("nan"), float("-inf"), float("inf"), -1.0, 4, float("nan"), float("inf"), float("nan"), False, 3.141592653589793, float("nan"), 31.0, 31.0, 31.0, float("inf"), 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_328():
    assert v72_bounded(float("nan"), float("inf"), -1.0, float("nan"), 4, float("inf"), -3.141592653589793, -3.141592653589793, True, float("-inf"), 15.0, float("nan"), 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_329():
    assert v72_bounded(float("inf"), 1.0, -1.0, float("-inf"), 4, 3.141592653589793, float("inf"), -3.141592653589793, True, float("inf"), 15.0, -400.0, 400.0, 400.0, 60.0, float("nan"), float("nan")) == [-0.0, -1.0]

def test_v72_bounded_330():
    assert v72_bounded(float("-inf"), 1.0, 1.0, float("inf"), 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("inf"), float("nan"), -30.0, float("inf"), 0.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_331():
    assert v72_bounded(1.0, 1.0, float("nan"), -1.0, -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("nan"), 15.0, float("inf"), -30.0, float("inf"), 60.0, 60.0, float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_332():
    assert v72_bounded(1.0, float("inf"), 1.0, float("inf"), 4, 3.141592653589793, 3.141592653589793, -3.141592653589793, False, -3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("nan"), 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_333():
    assert v72_bounded(float("inf"), float("nan"), float("inf"), 1.0, 0, float("nan"), float("inf"), float("nan"), False, 3.141592653589793, float("nan"), 399.0, 400.0, 400.0, 60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_334():
    assert v72_bounded(float("inf"), float("inf"), -1.0, 1.0, 0, float("nan"), float("-inf"), float("-inf"), False, 3.141592653589793, float("inf"), float("nan"), float("inf"), 400.0, -60.0, 0.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_335():
    assert v72_bounded(0.5, 0.5, 1.0, float("inf"), 0, float("inf"), 3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("nan"), -400.0, 400.0, 400.0, float("inf"), float("nan"), 30.0) == [0.5, 0.5]

def test_v72_bounded_336():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), 1.0, -1, float("-inf"), float("nan"), -3.141592653589793, False, float("-inf"), 15.0, 30.0, 30.0, 0.0, float("inf"), 60.0, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_337():
    assert v72_bounded(float("inf"), 1.0, 1.0, -1.0, 4, -3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, -15.0, 30.0, 30.0, float("nan"), 60.0, float("inf"), float("nan")) == [-0.0, -1.0]

def test_v72_bounded_338():
    assert v72_bounded(1.0, 0.0, 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("nan"), 30.0, float("inf"), float("nan"), float("inf"), 60.0, 30.0) == [1.0, 0.0]

def test_v72_bounded_339():
    assert v72_bounded(float("inf"), float("inf"), 0.0, float("inf"), -1, float("-inf"), 3.141592653589793, 0.0, False, 3.141592653589793, float("-inf"), float("-inf"), -400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_340():
    assert v72_bounded(float("-inf"), float("-inf"), -1.0, 1.0, 0, float("inf"), float("nan"), 3.141592653589793, False, float("inf"), float("nan"), 400.0, 0.0, 400.0, float("inf"), float("inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_341():
    assert v72_bounded(-1.0, float("nan"), 1.0, float("nan"), 5, -3.141592653589793, -3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, -400.0, 400.0, 400.0, float("nan"), 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_342():
    assert v72_bounded(float("inf"), 1.0, float("nan"), 1.0, 0, float("-inf"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, -15.0, 29.0, 30.0, float("inf"), float("nan"), 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_343():
    assert v72_bounded(float("nan"), 1.0, float("inf"), float("nan"), 0, float("inf"), float("-inf"), float("inf"), False, 3.141592653589793, float("inf"), float("inf"), 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_344():
    assert v72_bounded(float("nan"), 0.5, float("inf"), 1.0, 0, float("inf"), float("inf"), float("inf"), False, float("-inf"), 15.0, float("nan"), 30.0, 0.0, float("inf"), float("-inf"), float("inf")) == [-0.894427191, 0.447213595]

def test_v72_bounded_345():
    assert v72_bounded(float("inf"), 1.0, -1.0, float("-inf"), 4, 3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, float("-inf"), 30.0, 30.0, 0.0, 60.0, 60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_346():
    assert v72_bounded(float("inf"), 1.0, 0.0, float("-inf"), 4, float("-inf"), -3.141592653589793, float("inf"), True, float("-inf"), float("inf"), -30.0, 30.0, float("-inf"), 60.0, float("inf"), 0.0) == [0.0, -1.0]

def test_v72_bounded_347():
    assert v72_bounded(1.0, 0.0, float("nan"), float("inf"), 0, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, float("-inf"), float("nan"), -30.0, 0.0, -60.0, 60.0, 30.0) == [1.0, 0.0]

def test_v72_bounded_348():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), 1.0, -1, 3.141592653589793, -3.141592653589793, float("inf"), True, -3.141592653589793, float("inf"), 31.0, 31.0, 31.0, 60.0, 60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_349():
    assert v72_bounded(float("inf"), float("nan"), 1.0, float("inf"), -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("nan"), -15.0, -30.0, 30.0, 0.0, 60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_350():
    assert v72_bounded(1.0, float("nan"), float("inf"), float("nan"), 0, float("inf"), float("inf"), float("-inf"), False, 3.141592653589793, 15.0, float("inf"), -400.0, 400.0, float("inf"), 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_351():
    assert v72_bounded(float("-inf"), -1.0, 1.0, 1.0, -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, -400.0, float("inf"), 400.0, -60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_352():
    assert v72_bounded(float("-inf"), float("inf"), float("nan"), 1.0, 0, float("nan"), float("inf"), float("nan"), True, float("nan"), float("-inf"), 30.0, float("inf"), float("inf"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_353():
    assert v72_bounded(float("inf"), 0.5, 1.0, float("-inf"), 4, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 30.0, float("inf"), 0.0, 60.0, float("nan"), 0.0) == [-0.0, -1.0]

def test_v72_bounded_354():
    assert v72_bounded(float("nan"), float("inf"), 1.0, float("nan"), 4, 3.141592653589793, float("inf"), -3.141592653589793, True, float("-inf"), 10.5, 30.0, 0.0, float("inf"), float("inf"), 60.0, 0.0) == [0.707106781, -0.707106781]

def test_v72_bounded_355():
    assert v72_bounded(float("-inf"), -1.0, float("nan"), float("inf"), 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("-inf"), float("nan"), 30.0, 30.0, 0.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_356():
    assert v72_bounded(float("inf"), 1.0, 0.0, float("-inf"), 4, float("inf"), 0.0, 3.141592653589793, True, 3.141592653589793, 15.0, -30.0, float("nan"), float("nan"), float("inf"), float("nan"), 30.0) == [0.0, -1.0]

def test_v72_bounded_357():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 0, 3.141592653589793, float("inf"), 3.141592653589793, True, float("-inf"), 0.0, float("-inf"), float("nan"), 400.0, 60.0, float("nan"), 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_358():
    assert v72_bounded(float("-inf"), float("inf"), 0.0, 1.0, 4, 3.141592653589793, 3.141592653589793, float("inf"), True, float("inf"), 15.0, 30.0, 30.0, float("inf"), float("-inf"), float("inf"), 0.5) == [0.0, 1.0]

def test_v72_bounded_359():
    assert v72_bounded(float("nan"), float("-inf"), 1.0, -1.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, True, 3.141592653589793, -15.0, float("nan"), 400.0, 400.0, 60.0, -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_360():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 0.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, 0.0, 399.0, 400.0, 400.0, -60.0, float("nan"), float("inf")) == [0.0, 1.0]

def test_v72_bounded_361():
    assert v72_bounded(1.0, float("inf"), float("nan"), 1.0, 0, 3.141592653589793, 3.141592653589793, float("nan"), False, -3.141592653589793, 15.0, float("nan"), -400.0, 400.0, 60.0, 60.0, float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_362():
    assert v72_bounded(float("inf"), 1.0, float("inf"), 1.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, float("inf"), float("nan"), 400.0, 400.0, 400.0, 60.0, 60.0, float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_363():
    assert v72_bounded(float("inf"), float("inf"), 0.0, -1.0, 5, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, float("inf"), 0.0, 0.0, float("nan"), -60.0, -60.0, float("inf")) == [0.0, -1.0]

def test_v72_bounded_364():
    assert v72_bounded(float("inf"), float("inf"), 1.0, 1.0, 0, float("inf"), 3.141592653589793, float("-inf"), False, 3.141592653589793, 15.0, float("inf"), 30.0, float("inf"), float("nan"), 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_365():
    assert v72_bounded(float("nan"), 1.0, float("inf"), float("nan"), 0, float("inf"), float("inf"), float("-inf"), False, -3.141592653589793, -15.0, float("inf"), 400.0, 400.0, float("inf"), 60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_366():
    assert v72_bounded(float("nan"), -1.0, 1.0, float("-inf"), 4, 3.141592653589793, float("nan"), 3.141592653589793, True, 3.141592653589793, float("inf"), -400.0, 400.0, 400.0, 60.0, float("nan"), 0.0) == [-0.0, -1.0]

def test_v72_bounded_367():
    assert v72_bounded(float("-inf"), 0.0, -1.0, float("nan"), 6, float("nan"), 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, -400.0, float("nan"), 400.0, float("inf"), -60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_368():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), 1.0, 4, float("nan"), -3.141592653589793, float("inf"), False, float("inf"), float("inf"), 400.0, 400.0, 400.0, 60.0, -60.0, float("nan")) == [-0.0, 1.0]

def test_v72_bounded_369():
    assert v72_bounded(float("inf"), 0.5, 1.0, float("-inf"), 4, float("inf"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, 60.0, float("nan"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_370():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, -1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, float("nan"), 400.0, 400.0, 400.0, float("nan"), 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_371():
    assert v72_bounded(1.0, float("nan"), float("nan"), float("-inf"), 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, 5.0, 399.0, 400.0, 400.0, -60.0, 60.0, float("nan")) == [-0.0, -1.0]

def test_v72_bounded_372():
    assert v72_bounded(float("nan"), float("nan"), 1.0, -1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("inf"), 30.0, 30.0, float("nan"), 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_373():
    assert v72_bounded(float("inf"), 1.0, 0.0, float("-inf"), -1, float("inf"), 3.141592653589793, 3.141592653589793, False, float("inf"), float("nan"), 0.0, 0.0, float("nan"), -60.0, 60.0, float("inf")) == [-0.707106781, 0.707106781]

def test_v72_bounded_374():
    assert v72_bounded(1.0, float("inf"), float("nan"), float("-inf"), -1, float("inf"), float("inf"), float("inf"), False, float("inf"), 15.0, 30.0, 30.0, float("inf"), float("nan"), 60.0, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_375():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), 4, float("nan"), float("inf"), 3.141592653589793, False, 3.141592653589793, float("nan"), float("inf"), 30.0, float("inf"), 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_376():
    assert v72_bounded(float("-inf"), 1.0, float("inf"), 1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, False, float("nan"), 15.0, 30.0, 0.0, float("nan"), float("nan"), -60.0, float("-inf")) == [0.707106781, 0.707106781]

def test_v72_bounded_377():
    assert v72_bounded(float("inf"), -1.0, float("nan"), 1.0, 4, 3.141592653589793, float("inf"), float("nan"), False, -3.141592653589793, float("nan"), float("nan"), 31.0, 31.0, 60.0, float("nan"), 30.0) == [0.0, 1.0]

def test_v72_bounded_378():
    assert v72_bounded(1.0, float("nan"), float("inf"), 1.0, -1, 3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, 15.0, -400.0, 400.0, 400.0, 60.0, float("nan"), float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_379():
    assert v72_bounded(float("inf"), 1.0, 0.0, float("-inf"), 4, 3.141592653589793, float("inf"), -3.141592653589793, True, 3.141592653589793, 15.0, 399.0, 400.0, 400.0, 60.0, float("nan"), float("-inf")) == [0.0, -1.0]

def test_v72_bounded_380():
    assert v72_bounded(float("inf"), 1.0, -1.0, float("nan"), -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 0.0, 30.0, 30.0, float("nan"), 0.0, float("nan"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_381():
    assert v72_bounded(1.0, float("inf"), float("-inf"), float("-inf"), 0, float("-inf"), float("nan"), -3.141592653589793, False, float("inf"), float("inf"), -31.0, 0.0, 31.0, -60.0, float("-inf"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_382():
    assert v72_bounded(float("nan"), float("nan"), 0.0, -1.0, 0, -3.141592653589793, -3.141592653589793, -3.141592653589793, True, 3.141592653589793, 0.0, float("inf"), float("nan"), 0.0, 0.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_383():
    assert v72_bounded(1.0, 0.0, float("inf"), float("nan"), 0, float("nan"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("nan"), -400.0, -400.0, 400.0, 60.0, 60.0, float("nan")) == [1.0, 0.0]

def test_v72_bounded_384():
    assert v72_bounded(float("inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, 3.141592653589793, float("nan"), False, -3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("inf"), float("-inf"), 0.5) == [-0.0, -1.0]

def test_v72_bounded_385():
    assert v72_bounded(float("-inf"), float("inf"), float("inf"), float("inf"), 0, float("nan"), 3.141592653589793, 3.141592653589793, False, float("inf"), float("nan"), -30.0, 30.0, 0.0, 60.0, 0.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_386():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, float("inf"), 0, 3.141592653589793, float("nan"), -3.141592653589793, False, 0.0, float("-inf"), 30.0, 30.0, float("nan"), 60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_387():
    assert v72_bounded(float("inf"), float("inf"), 0.0, float("nan"), 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, -30.0, 30.0, float("-inf"), 60.0, 0.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_388():
    assert v72_bounded(1.0, float("inf"), float("inf"), 1.0, -1, float("inf"), 3.141592653589793, float("inf"), False, -3.141592653589793, 15.0, float("nan"), 400.0, 400.0, float("inf"), 0.0, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_389():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, -1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, -9.035533905932738, -30.0, 30.0, 0.0, 60.0, float("nan"), 0.0) == [0.707106781, -0.707106781]

def test_v72_bounded_390():
    assert v72_bounded(float("-inf"), float("-inf"), 0.0, -1.0, 4, 3.141592653589793, float("nan"), -3.141592653589793, False, 3.141592653589793, 15.0, 400.0, float("nan"), 400.0, -60.0, float("inf"), 0.0) == [0.0, -1.0]

def test_v72_bounded_391():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, 0.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, -9.035533905932738, -30.0, 30.0, 0.0, 60.0, 60.0, float("nan")) == [0.0, 1.0]

def test_v72_bounded_392():
    assert v72_bounded(float("nan"), float("inf"), float("inf"), -1.0, 4, float("-inf"), 3.141592653589793, float("inf"), False, 3.141592653589793, -15.0, 30.0, 30.0, float("nan"), 60.0, 0.0, float("nan")) == [-0.0, -1.0]

def test_v72_bounded_393():
    assert v72_bounded(float("nan"), 0.0, float("-inf"), float("-inf"), 5, float("inf"), -3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, 30.0, 30.0, 0.0, 60.0, float("inf"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_394():
    assert v72_bounded(float("inf"), 0.5, 1.0, float("-inf"), 4, float("inf"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("nan"), -400.0, 400.0, 400.0, -60.0, 60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_395():
    assert v72_bounded(float("inf"), float("-inf"), 1.0, 1.0, 0, 3.141592653589793, float("-inf"), 3.141592653589793, False, float("inf"), -15.0, 30.0, 30.0, float("-inf"), float("inf"), float("inf"), 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_396():
    assert v72_bounded(float("nan"), float("inf"), 1.0, 1.0, 4, 3.141592653589793, float("inf"), float("-inf"), False, float("inf"), float("nan"), float("inf"), float("inf"), 31.0, float("nan"), 60.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_397():
    assert v72_bounded(float("nan"), 1.0, 1.0, 1.0, 0, float("nan"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("inf"), float("nan"), 30.0, float("nan"), 60.0, float("nan"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_398():
    assert v72_bounded(float("inf"), float("-inf"), 0.0, 0.0, 4, 3.141592653589793, float("inf"), float("nan"), False, 3.141592653589793, float("inf"), 400.0, 400.0, 400.0, 60.0, float("inf"), float("inf")) == [0.0, 1.0]

def test_v72_bounded_399():
    assert v72_bounded(1.0, float("inf"), float("inf"), float("inf"), 0, float("-inf"), 3.141592653589793, float("inf"), False, 3.141592653589793, float("inf"), float("inf"), 400.0, 400.0, 60.0, 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_400():
    assert v72_bounded(float("inf"), float("nan"), 1.0, float("nan"), 4, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("inf"), -30.0, -30.0, 0.0, 60.0, -60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_401():
    assert v72_bounded(float("inf"), float("nan"), float("inf"), 1.0, 4, float("inf"), 3.141592653589793, float("inf"), False, float("inf"), 15.0, float("inf"), 0.0, 400.0, float("inf"), 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_402():
    assert v72_bounded(float("inf"), float("-inf"), 0.5, 1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, 10.476107714171773, -30.0, -30.0, 0.0, 60.0, float("nan"), 30.0) == [0.0, 1.0]

def test_v72_bounded_403():
    assert v72_bounded(float("nan"), 0.5, -1.0, 1.0, 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, -3.141592653589793, 0.0, float("nan"), float("-inf"), 400.0, float("inf"), 60.0, 0.25) == [-0.894427191, 0.447213595]

def test_v72_bounded_404():
    assert v72_bounded(float("inf"), float("inf"), float("-inf"), 1.0, 4, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, -15.0, -30.0, 30.0, 0.0, float("inf"), 60.0, 30.0) == [0.0, 1.0]

def test_v72_bounded_405():
    assert v72_bounded(float("nan"), float("nan"), 1.0, float("inf"), -1, 3.141592653589793, float("inf"), 3.141592653589793, False, float("inf"), -15.0, float("inf"), -400.0, 400.0, 60.0, float("nan"), 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_406():
    assert v72_bounded(float("inf"), -1.0, float("inf"), float("inf"), 0, 3.141592653589793, float("nan"), float("inf"), True, 3.141592653589793, float("inf"), 400.0, -400.0, 400.0, 60.0, 60.0, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_407():
    assert v72_bounded(float("inf"), float("nan"), float("nan"), 1.0, 0, float("nan"), 3.141592653589793, float("-inf"), False, float("inf"), float("nan"), 31.0, 31.0, 31.0, float("inf"), float("inf"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_408():
    assert v72_bounded(float("nan"), 1.0, float("nan"), float("inf"), 5, float("nan"), float("inf"), 3.141592653589793, False, float("inf"), float("inf"), float("nan"), float("nan"), 400.0, -60.0, 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_409():
    assert v72_bounded(float("-inf"), float("-inf"), 1.0, float("inf"), 0, float("nan"), 3.141592653589793, -3.141592653589793, False, 3.141592653589793, float("inf"), -400.0, 400.0, 400.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_410():
    assert v72_bounded(float("inf"), float("-inf"), float("inf"), float("nan"), 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, -3.141592653589793, 15.0, 30.0, 30.0, 0.0, 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_411():
    assert v72_bounded(float("nan"), float("inf"), float("inf"), 1.0, 4, float("nan"), float("nan"), float("-inf"), False, -3.141592653589793, float("nan"), float("inf"), 30.0, 0.0, float("inf"), 60.0, 30.0) == [-0.0, 1.0]

def test_v72_bounded_412():
    assert v72_bounded(float("inf"), float("inf"), 0.0, float("inf"), -1, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 0.0, 399.0, 400.0, 400.0, 60.0, float("inf"), 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_413():
    assert v72_bounded(float("inf"), 1.0, float("-inf"), 1.0, 4, float("nan"), 3.141592653589793, float("-inf"), False, -3.141592653589793, 15.0, 400.0, float("inf"), 400.0, 60.0, float("nan"), float("nan")) == [0.0, 1.0]

def test_v72_bounded_414():
    assert v72_bounded(float("inf"), 0.5, 1.0, float("nan"), 5, 3.141592653589793, float("nan"), 3.141592653589793, True, 3.141592653589793, float("inf"), 0.0, float("nan"), 400.0, 60.0, -60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_415():
    assert v72_bounded(float("nan"), float("nan"), 0.0, float("nan"), 0, float("-inf"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 30.0, 0.0, float("nan"), float("nan"), 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_416():
    assert v72_bounded(float("inf"), 1.0, -1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, float("inf"), float("nan"), 30.0, float("-inf"), float("nan"), float("nan"), -60.0, 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_417():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), 1.0, 0, float("nan"), 3.141592653589793, 3.141592653589793, True, 3.141592653589793, -15.0, 30.0, -30.0, 0.0, float("inf"), 60.0, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_418():
    assert v72_bounded(float("inf"), -1.0, float("inf"), float("inf"), 0, 3.141592653589793, 3.141592653589793, float("-inf"), False, 3.141592653589793, 15.0, float("inf"), 30.0, 0.0, 60.0, float("inf"), 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_419():
    assert v72_bounded(float("-inf"), float("-inf"), float("nan"), 1.0, 0, 3.141592653589793, float("nan"), 3.141592653589793, True, 3.141592653589793, 15.0, 29.0, 30.0, 0.0, 60.0, float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_420():
    assert v72_bounded(float("-inf"), float("inf"), float("inf"), 0.0, 0, -3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 30.0, -30.0, float("-inf"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_421():
    assert v72_bounded(float("inf"), float("nan"), 0.5, 1.0, 0, -3.141592653589793, 3.141592653589793, 0.0, False, 3.141592653589793, float("-inf"), float("nan"), 30.0, 0.0, -60.0, float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_422():
    assert v72_bounded(1.0, float("nan"), float("inf"), 0.0, 0, float("nan"), 3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("inf"), 400.0, float("inf"), 400.0, float("nan"), 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_423():
    assert v72_bounded(float("nan"), float("inf"), 1.0, float("nan"), 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, -5.5, -30.0, -30.0, 0.0, 60.0, float("nan"), float("inf")) == [0.0, 1.0]

def test_v72_bounded_424():
    assert v72_bounded(1.0, float("inf"), float("inf"), float("inf"), -1, float("nan"), float("inf"), -3.141592653589793, False, float("nan"), float("inf"), 30.0, 30.0, float("nan"), float("inf"), 60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_425():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 4, 3.141592653589793, float("inf"), -3.141592653589793, True, float("-inf"), 5.550000000000001, 399.0, 400.0, 400.0, 60.0, 60.0, 0.668807716974935) == [-0.0, -1.0]

def test_v72_bounded_426():
    assert v72_bounded(float("inf"), float("nan"), 1.0, float("-inf"), 0, -3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 400.0, float("-inf"), 400.0, 60.0, 60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_427():
    assert v72_bounded(float("inf"), float("inf"), 0.0, 1.0, 4, 3.141592653589793, float("inf"), 3.141592653589793, True, float("-inf"), -5.499999999999999, 30.0, 30.0, float("-inf"), float("inf"), 60.0, 0.0) == [0.0, 1.0]

def test_v72_bounded_428():
    assert v72_bounded(float("nan"), float("inf"), float("nan"), 1.0, -1, float("inf"), float("nan"), 3.141592653589793, False, float("nan"), 0.0, 400.0, float("nan"), 400.0, float("nan"), 60.0, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_429():
    assert v72_bounded(1.0, float("inf"), float("-inf"), float("inf"), 4, float("nan"), 3.141592653589793, float("nan"), True, float("-inf"), float("inf"), -30.0, 30.0, float("-inf"), 60.0, float("inf"), 0.0) == [-0.0, -1.0]

def test_v72_bounded_430():
    assert v72_bounded(1.0, float("nan"), float("nan"), float("nan"), -1, float("-inf"), 3.141592653589793, 3.141592653589793, False, -3.141592653589793, 15.0, 30.0, 0.0, float("nan"), float("nan"), 60.0, 0.0) == [0.707106781, -0.707106781]

def test_v72_bounded_431():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, 1.0, -1, 3.141592653589793, -3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, float("nan"), 400.0, 60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_432():
    assert v72_bounded(float("inf"), float("inf"), 0.0, float("-inf"), -1, 3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, float("nan"), 30.0, float("inf"), 60.0, 60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_433():
    assert v72_bounded(1.0, float("nan"), float("nan"), float("-inf"), 4, 3.141592653589793, float("inf"), 3.141592653589793, True, float("-inf"), 2.7872213177926706, 30.0, 0.0, float("inf"), -60.0, 60.0, 0.0) == [0.707106781, -0.707106781]

def test_v72_bounded_434():
    assert v72_bounded(float("-inf"), float("inf"), 0.5, 1.0, 5, float("inf"), 3.141592653589793, float("-inf"), False, float("nan"), float("inf"), float("nan"), float("inf"), 400.0, 60.0, float("-inf"), 30.0) == [0.0, 1.0]

def test_v72_bounded_435():
    assert v72_bounded(1.0, -1.0, -1.0, float("-inf"), 5, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("-inf"), float("inf"), 400.0, 400.0, float("nan"), -60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_436():
    assert v72_bounded(1.0, float("inf"), float("-inf"), float("-inf"), 4, float("nan"), float("nan"), float("inf"), False, 3.141592653589793, float("nan"), float("inf"), 400.0, 400.0, 60.0, float("nan"), 30.0) == [-0.0, -1.0]

def test_v72_bounded_437():
    assert v72_bounded(float("inf"), -1.0, float("inf"), float("inf"), 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, float("inf"), float("nan"), -30.0, 30.0, float("-inf"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_438():
    assert v72_bounded(float("inf"), float("inf"), 1.0, float("inf"), 0, 3.141592653589793, 3.141592653589793, float("inf"), False, 3.141592653589793, 0.0, float("-inf"), 400.0, 400.0, float("inf"), -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_439():
    assert v72_bounded(1.0, 0.0, float("nan"), float("-inf"), 0, 3.141592653589793, float("-inf"), 3.141592653589793, False, 3.141592653589793, float("inf"), float("nan"), 400.0, 400.0, 60.0, float("inf"), 30.0) == [1.0, 0.0]

def test_v72_bounded_440():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), 1.0, 0, float("inf"), float("nan"), 3.141592653589793, True, 3.141592653589793, float("inf"), 0.0, float("nan"), 400.0, -60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_441():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, float("nan"), 4, float("inf"), -3.141592653589793, 3.141592653589793, True, float("inf"), float("nan"), 30.0, float("inf"), 0.0, 60.0, float("nan"), 30.0) == [-0.0, -1.0]

def test_v72_bounded_442():
    assert v72_bounded(float("-inf"), float("inf"), 0.0, 1.0, 4, 3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, float("nan"), 400.0, 400.0, -60.0, float("nan"), float("nan")) == [0.0, 1.0]

def test_v72_bounded_443():
    assert v72_bounded(float("inf"), 0.5, 1.0, float("-inf"), 4, 3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("nan"), float("nan"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_444():
    assert v72_bounded(float("inf"), float("inf"), float("-inf"), 1.0, -1, 3.141592653589793, float("nan"), 3.141592653589793, False, -3.141592653589793, float("nan"), 30.0, 30.0, float("nan"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_445():
    assert v72_bounded(float("inf"), float("inf"), 1.0, float("inf"), 4, -3.141592653589793, 3.141592653589793, -3.141592653589793, False, float("inf"), 15.0, float("inf"), 400.0, 400.0, 60.0, float("inf"), 30.0) == [-0.0, -1.0]

def test_v72_bounded_446():
    assert v72_bounded(float("-inf"), float("nan"), float("-inf"), 1.0, 0, float("-inf"), float("nan"), 0.0, True, 0.0, float("inf"), float("-inf"), float("nan"), float("-inf"), float("nan"), 60.0, float("-inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_447():
    assert v72_bounded(float("nan"), 1.0, float("inf"), -1.0, 4, float("inf"), 3.141592653589793, float("nan"), True, float("nan"), float("nan"), float("inf"), float("nan"), float("inf"), float("inf"), 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_448():
    assert v72_bounded(float("nan"), float("inf"), 1.0, float("nan"), 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("inf"), -30.0, 30.0, float("inf"), 60.0, 60.0, 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_449():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), float("nan"), 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, 30.0, -30.0, 0.0, float("nan"), 0.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_450():
    assert v72_bounded(float("inf"), float("nan"), 1.0, float("nan"), 4, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, 15.0, 400.0, 400.0, 400.0, float("inf"), -60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_451():
    assert v72_bounded(float("inf"), float("nan"), float("inf"), 1.0, -1, 3.141592653589793, float("inf"), -3.141592653589793, False, 3.141592653589793, 15.0, 400.0, float("nan"), 400.0, -60.0, float("-inf"), 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_452():
    assert v72_bounded(float("inf"), float("nan"), float("nan"), float("inf"), 4, 3.141592653589793, float("inf"), float("inf"), False, -3.141592653589793, 0.0, float("-inf"), 30.0, float("nan"), 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_453():
    assert v72_bounded(1.0, float("inf"), float("inf"), float("inf"), 4, float("inf"), float("inf"), 3.141592653589793, False, 3.141592653589793, float("inf"), float("nan"), 400.0, 400.0, 60.0, 60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_454():
    assert v72_bounded(float("nan"), 1.0, float("inf"), 1.0, 4, 3.141592653589793, float("inf"), float("nan"), False, -3.141592653589793, float("nan"), float("nan"), 400.0, 400.0, 60.0, float("nan"), float("nan")) == [0.0, 1.0]

def test_v72_bounded_455():
    assert v72_bounded(1.0, float("inf"), float("inf"), float("inf"), 4, -3.141592653589793, 3.141592653589793, 3.141592653589793, False, float("inf"), -15.0, 400.0, -400.0, 400.0, float("nan"), 0.0, float("nan")) == [-0.0, -1.0]

def test_v72_bounded_456():
    assert v72_bounded(float("nan"), 0.0, float("nan"), float("inf"), 0, float("inf"), float("inf"), 3.141592653589793, False, float("inf"), 15.0, float("inf"), float("nan"), float("inf"), float("nan"), 60.0, 0.5) == [-1.0, 0.0]

def test_v72_bounded_457():
    assert v72_bounded(float("inf"), float("inf"), 1.0, float("nan"), 0, 3.141592653589793, -3.141592653589793, float("-inf"), False, float("inf"), float("nan"), 31.0, 31.0, 31.0, float("inf"), float("-inf"), 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_458():
    assert v72_bounded(float("nan"), float("inf"), float("inf"), 1.0, 0, float("inf"), float("nan"), 3.141592653589793, False, -3.141592653589793, float("-inf"), 0.0, float("nan"), float("-inf"), 60.0, 60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_459():
    assert v72_bounded(0.0, float("inf"), float("inf"), float("-inf"), -2, 3.141592653589793, float("inf"), 3.141592653589793, False, 3.141592653589793, float("-inf"), float("inf"), -400.0, 400.0, 60.0, 60.0, 30.0) == [0.0, -1.0]

def test_v72_bounded_460():
    assert v72_bounded(1.0, 0.0, float("nan"), float("inf"), 5, 3.141592653589793, float("nan"), 3.141592653589793, True, 3.141592653589793, float("inf"), 31.0, float("nan"), 31.0, float("nan"), 60.0, float("inf")) == [-0.0, -1.0]

def test_v72_bounded_461():
    assert v72_bounded(float("inf"), float("nan"), float("nan"), float("-inf"), 4, float("inf"), 3.141592653589793, float("nan"), False, float("nan"), float("inf"), 0.0, float("inf"), 31.0, float("nan"), 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_462():
    assert v72_bounded(float("inf"), float("inf"), 0.0, float("-inf"), 4, float("-inf"), 3.141592653589793, float("nan"), False, 3.141592653589793, float("nan"), -30.0, 30.0, float("-inf"), float("inf"), 60.0, 0.5) == [0.0, -1.0]

def test_v72_bounded_463():
    assert v72_bounded(float("inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, 3.141592653589793, float("inf"), False, float("inf"), float("nan"), 400.0, float("nan"), 400.0, -60.0, float("nan"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_464():
    assert v72_bounded(float("nan"), float("inf"), float("inf"), -1.0, 0, float("nan"), float("inf"), float("inf"), False, 3.141592653589793, float("inf"), 0.0, float("inf"), 31.0, float("nan"), 60.0, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_465():
    assert v72_bounded(float("inf"), float("nan"), 1.0, float("inf"), -2, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, 30.0, 30.0, float("inf"), -60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_466():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, False, 3.141592653589793, -15.0, -30.0, float("nan"), float("inf"), 60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_467():
    assert v72_bounded(1.0, float("nan"), float("nan"), float("-inf"), 4, 3.141592653589793, float("inf"), 3.141592653589793, False, float("-inf"), float("nan"), -400.0, float("nan"), 400.0, float("inf"), 60.0, 0.0) == [-0.0, -1.0]

def test_v72_bounded_468():
    assert v72_bounded(float("inf"), 0.0, float("inf"), float("inf"), 0, 3.141592653589793, 3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, float("-inf"), 30.0, 0.0, float("inf"), float("inf"), 30.0) == [-1.0, 0.0]

def test_v72_bounded_469():
    assert v72_bounded(1.0, float("inf"), float("inf"), 0.0, 0, 3.141592653589793, 3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, float("nan"), float("inf"), 400.0, float("inf"), float("nan"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_470():
    assert v72_bounded(float("nan"), float("inf"), float("inf"), float("inf"), 0, 3.141592653589793, float("nan"), float("nan"), False, float("inf"), 15.0, float("inf"), 30.0, float("inf"), 60.0, -60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_471():
    assert v72_bounded(float("inf"), float("inf"), 0.0, float("inf"), 0, float("inf"), 3.141592653589793, 3.141592653589793, False, 3.141592653589793, 15.0, float("nan"), 0.0, float("nan"), -60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_472():
    assert v72_bounded(float("-inf"), float("inf"), 1.0, float("nan"), 0, float("nan"), 3.141592653589793, -3.141592653589793, False, float("nan"), float("nan"), -400.0, 400.0, 400.0, float("nan"), 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_473():
    assert v72_bounded(float("inf"), 0.0, float("nan"), float("nan"), 4, 3.141592653589793, float("inf"), 3.141592653589793, True, 3.141592653589793, float("-inf"), float("nan"), 30.0, float("-inf"), 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_474():
    assert v72_bounded(float("nan"), float("inf"), float("-inf"), float("nan"), 0, float("nan"), 3.141592653589793, float("-inf"), False, 3.141592653589793, float("inf"), float("inf"), 400.0, 400.0, -60.0, -60.0, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_475():
    assert v72_bounded(float("inf"), float("inf"), float("-inf"), -1.0, 4, float("nan"), -3.141592653589793, 3.141592653589793, True, -3.141592653589793, 15.0, float("nan"), float("inf"), 0.0, float("inf"), 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_476():
    assert v72_bounded(float("inf"), float("nan"), 1.0, float("-inf"), 0, float("-inf"), 3.141592653589793, float("-inf"), False, float("nan"), float("inf"), float("inf"), 30.0, float("inf"), -60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_477():
    assert v72_bounded(1.0, float("inf"), 0.0, float("-inf"), 5, float("inf"), 3.141592653589793, 3.141592653589793, True, 3.141592653589793, -15.0, -30.0, float("nan"), float("nan"), float("inf"), -60.0, float("nan")) == [0.0, -1.0]

def test_v72_bounded_478():
    assert v72_bounded(float("inf"), float("-inf"), 1.0, -1.0, 0, -3.141592653589793, 3.141592653589793, float("inf"), False, 3.141592653589793, 15.0, float("nan"), float("inf"), 400.0, float("inf"), float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_479():
    assert v72_bounded(1.0, float("inf"), -1.0, float("nan"), -1, float("nan"), float("-inf"), float("inf"), False, -3.141592653589793, 15.0, float("-inf"), float("nan"), float("inf"), float("inf"), 60.0, float("-inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_480():
    assert v72_bounded(1.0, float("nan"), float("inf"), float("-inf"), 0, float("nan"), float("inf"), -3.141592653589793, False, float("inf"), float("-inf"), float("nan"), 400.0, 400.0, float("inf"), 60.0, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_481():
    assert v72_bounded(float("nan"), float("nan"), 1.0, -1.0, 0, -3.141592653589793, 3.141592653589793, -3.141592653589793, False, 3.141592653589793, 15.0, -400.0, float("-inf"), 400.0, float("inf"), float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_482():
    assert v72_bounded(float("inf"), float("nan"), 1.0, -1.0, 4, 3.141592653589793, -3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, float("inf"), float("nan"), 400.0, 60.0, float("-inf"), float("nan")) == [-0.0, -1.0]

def test_v72_bounded_483():
    assert v72_bounded(float("-inf"), 0.0, float("-inf"), float("inf"), 0, float("inf"), float("nan"), -3.141592653589793, False, float("inf"), float("nan"), 400.0, float("inf"), 400.0, float("inf"), float("inf"), 30.0) == [-1.0, 0.0]

def test_v72_bounded_484():
    assert v72_bounded(-1.0, float("inf"), 1.0, float("nan"), 0, 3.141592653589793, -3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("inf"), float("inf"), 30.0, 0.0, float("inf"), float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_485():
    assert v72_bounded(float("inf"), float("nan"), float("nan"), float("-inf"), 0, -3.141592653589793, 3.141592653589793, 3.141592653589793, False, 0.0, float("nan"), 400.0, float("inf"), 400.0, 60.0, float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_486():
    assert v72_bounded(float("nan"), float("inf"), 1.0, 1.0, 4, float("nan"), float("nan"), float("nan"), False, 3.141592653589793, float("nan"), float("nan"), float("nan"), float("inf"), 0.0, float("nan"), float("inf")) == [-0.0, 1.0]

def test_v72_bounded_487():
    assert v72_bounded(1.0, float("inf"), float("inf"), float("inf"), -1, float("inf"), float("nan"), 3.141592653589793, False, 3.141592653589793, float("inf"), float("inf"), 30.0, float("nan"), 60.0, float("inf"), 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_488():
    assert v72_bounded(float("nan"), float("nan"), 1.0, float("nan"), 0, -3.141592653589793, -3.141592653589793, -3.141592653589793, False, float("nan"), 15.0, float("nan"), float("inf"), 400.0, float("nan"), -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_489():
    assert v72_bounded(1.0, float("-inf"), float("inf"), float("-inf"), 4, float("nan"), 3.141592653589793, float("inf"), False, 3.141592653589793, float("inf"), float("nan"), float("inf"), float("inf"), 60.0, 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_490():
    assert v72_bounded(float("-inf"), 1.0, 1.0, float("-inf"), 4, -3.141592653589793, -3.141592653589793, -3.141592653589793, True, float("inf"), -1.9644660940672627, 399.0, 400.0, 400.0, 60.0, float("nan"), float("inf")) == [-0.0, 1.0]

def test_v72_bounded_491():
    assert v72_bounded(float("nan"), float("nan"), float("inf"), 1.0, 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, float("inf"), float("nan"), -30.0, float("inf"), 60.0, -60.0, 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_492():
    assert v72_bounded(float("inf"), float("-inf"), float("nan"), -1.0, 4, float("nan"), 3.141592653589793, 3.141592653589793, False, float("-inf"), float("inf"), float("nan"), 30.0, float("nan"), float("nan"), 60.0, 30.0) == [-0.0, -1.0]

def test_v72_bounded_493():
    assert v72_bounded(float("nan"), -1.0, float("nan"), float("-inf"), 4, float("nan"), -3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("nan"), 399.0, 400.0, 400.0, 60.0, float("nan"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_494():
    assert v72_bounded(float("inf"), float("inf"), float("inf"), 1.0, 0, float("inf"), float("inf"), 3.141592653589793, False, -3.141592653589793, float("-inf"), float("inf"), -400.0, 400.0, 60.0, float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_495():
    assert v72_bounded(float("inf"), 1.0, float("nan"), float("nan"), 4, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, -3.141592653589793, float("inf"), 399.0, 400.0, 400.0, 60.0, float("nan"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_496():
    assert v72_bounded(-1.0, float("inf"), 1.0, float("nan"), 0, -3.141592653589793, -3.141592653589793, -3.141592653589793, False, 3.141592653589793, float("inf"), float("-inf"), 400.0, 400.0, float("nan"), 60.0, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_497():
    assert v72_bounded(float("inf"), 1.0, float("inf"), float("nan"), -1, float("nan"), -3.141592653589793, 3.141592653589793, False, 3.141592653589793, float("nan"), 30.0, float("inf"), float("nan"), -60.0, float("nan"), 30.0) == [-0.707106781, 0.707106781]

def test_v72_bounded_498():
    assert v72_bounded(float("nan"), float("nan"), float("-inf"), float("inf"), 0, -3.141592653589793, 3.141592653589793, float("nan"), False, 3.141592653589793, 15.0, float("nan"), 400.0, 400.0, float("inf"), float("nan"), 30.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_499():
    assert v72_bounded(float("inf"), float("inf"), 0.0, float("inf"), 0, float("nan"), -3.141592653589793, float("inf"), False, 3.141592653589793, float("inf"), float("nan"), float("nan"), 400.0, float("nan"), float("-inf"), 0.5) == [-0.707106781, -0.707106781]

def test_v72_bounded_500():
    assert v72_bounded(1.0, float("nan"), float("nan"), float("-inf"), 4, 3.141592653589793, float("inf"), 3.141592653589793, True, float("-inf"), -9.035533905932738, float("-inf"), float("-inf"), float("-inf"), 0.0, -60.0, 30.0) == [0.707106781, -0.707106781]

def test_v72_bounded_501():
    assert v72_bounded(float("nan"), 1.0, float("inf"), float("inf"), 0, float("inf"), 3.141592653589793, 3.141592653589793, True, float("inf"), float("-inf"), float("nan"), 400.0, 400.0, float("nan"), float("-inf"), float("-inf")) == [-0.707106781, 0.707106781]

def test_v72_bounded_502():
    assert v72_bounded(float("nan"), float("-inf"), 1.0, float("inf"), 0, 3.141592653589793, 3.141592653589793, 3.141592653589793, True, 3.141592653589793, 15.0, float("-inf"), float("inf"), float("nan"), 60.0, 60.0, float("-inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_503():
    assert v72_bounded(float("inf"), float("inf"), 1.0, float("inf"), 0, 3.141592653589793, float("nan"), 3.141592653589793, False, 3.141592653589793, float("inf"), float("inf"), 30.0, float("-inf"), float("nan"), 60.0, float("-inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_504():
    assert v72_bounded(float("nan"), float("inf"), float("nan"), float("nan"), 0, float("nan"), 3.141592653589793, 3.141592653589793, False, float("-inf"), float("inf"), float("-inf"), float("inf"), float("nan"), 60.0, 60.0, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_505():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), -1, float("inf"), float("inf"), 4.000000000000001, False, float("inf"), 2.68156158598852e+154, 5e-324, float("inf"), float("inf"), float("inf"), float("inf"), 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_506():
    assert v72_bounded(float("inf"), float("inf"), 2.0000000000000004, float("nan"), -1, float("inf"), float("inf"), float("inf"), True, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_507():
    assert v72_bounded(2.0000000000000004, float("inf"), float("nan"), float("nan"), 0, float("inf"), -5e-324, float("inf"), False, -4.000000000000001, float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_508():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), -1, float("inf"), float("inf"), float("inf"), False, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_509():
    assert v72_bounded(float("inf"), float("inf"), -2.0000000000000004, float("nan"), 4, 4.000000000000001, float("inf"), float("inf"), True, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_510():
    assert v72_bounded(2.0000000000000004, float("inf"), 2.0000000000000004, -2.0000000000000004, 0, float("inf"), float("inf"), -5e-324, True, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_511():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, 4.000000000000001, float("inf"), float("inf"), True, float("inf"), float("nan"), 2.68156158598852e+154, float("inf"), float("inf"), float("inf"), float("inf"), float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_512():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154) == [-0.707106781, -0.707106781]

def test_v72_bounded_513():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), 2.68156158598852e+154, float("nan"), float("inf"), float("nan"), float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_514():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_515():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), -4.000000000000001, float("inf"), True, float("inf"), float("nan"), -2.68156158598852e+154, float("inf"), float("inf"), float("inf"), float("inf"), float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_516():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), float("inf"), float("inf"), True, float("inf"), 2.68156158598852e+154, float("nan"), float("inf"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154) == [-0.707106781, -0.707106781]

def test_v72_bounded_517():
    assert v72_bounded(float("inf"), float("inf"), 2.0000000000000004, 2.0000000000000004, 0, float("inf"), -4.000000000000001, float("nan"), False, float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_518():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), -1, float("inf"), float("inf"), float("inf"), True, float("inf"), 2.68156158598852e+154, float("nan"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_519():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), -1, float("inf"), float("inf"), float("inf"), False, float("inf"), 2.68156158598852e+154, float("nan"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_520():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), float("inf"), 4.000000000000001, False, 4.000000000000001, float("nan"), float("nan"), float("nan"), 2.68156158598852e+154, float("nan"), float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_521():
    assert v72_bounded(float("inf"), -2.0000000000000004, float("nan"), float("nan"), 0, 4.000000000000001, float("inf"), float("inf"), True, float("nan"), float("nan"), 2.68156158598852e+154, float("inf"), float("inf"), float("inf"), float("inf"), float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_522():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), float("inf"), float("inf"), False, float("inf"), float("nan"), 2.68156158598852e+154, float("nan"), 3.3376107877608025e-307, float("nan"), float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_523():
    assert v72_bounded(float("inf"), 2.0000000000000004, float("nan"), 2.0000000000000004, 0, float("inf"), float("inf"), float("inf"), False, -4.000000000000001, float("nan"), float("nan"), float("inf"), 2.68156158598852e+154, float("inf"), float("inf"), 5e-324) == [-0.707106781, 0.707106781]

def test_v72_bounded_524():
    assert v72_bounded(float("inf"), 2.0000000000000004, float("nan"), float("nan"), 0, 4.000000000000001, float("inf"), 4.000000000000001, False, 4.000000000000001, float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_525():
    assert v72_bounded(float("inf"), float("inf"), 2.0000000000000004, float("nan"), -2, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), 2.68156158598852e+154, float("inf"), float("inf"), float("inf"), float("inf"), float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_526():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), 4.000000000000001, float("inf"), True, float("inf"), 2.68156158598852e+154, float("nan"), float("inf"), 2.68156158598852e+154, float("inf"), float("inf"), float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_527():
    assert v72_bounded(float("inf"), float("inf"), 2.0000000000000004, float("nan"), -1, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), -2.68156158598852e+154, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_528():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), 2.68156158598852e+154, 2.68156158598852e+154, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_529():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), -1, float("inf"), float("inf"), float("inf"), False, -5e-324, float("nan"), 2.68156158598852e+154, 2.68156158598852e+154, 2.68156158598852e+154, float("nan"), float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_530():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 4, 4.000000000000001, 4.000000000000001, float("inf"), False, 4.000000000000001, float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154, float("nan")) == [-0.0, -1.0]

def test_v72_bounded_531():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), 2.0000000000000004, 0, float("inf"), float("inf"), float("inf"), False, float("inf"), 2.68156158598852e+154, float("nan"), float("inf"), 2.68156158598852e+154, float("nan"), float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_532():
    assert v72_bounded(2.0000000000000004, 2.0000000000000004, float("nan"), float("nan"), 4, float("inf"), 4.000000000000001, float("inf"), True, float("inf"), float("nan"), float("nan"), 2.68156158598852e+154, float("inf"), float("inf"), float("inf"), float("inf")) == [-0.0, -1.0]

def test_v72_bounded_533():
    assert v72_bounded(float("inf"), 2.0000000000000004, float("nan"), float("nan"), 0, 4.000000000000001, 4.000000000000001, float("inf"), False, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154) == [-0.707106781, 0.707106781]

def test_v72_bounded_534():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, 4.000000000000001, float("inf"), float("inf"), False, float("inf"), float("nan"), float("nan"), 2.68156158598852e+154, 3.3376107877608025e-307, float("nan"), float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_535():
    assert v72_bounded(2.0000000000000004, float("inf"), 2.0000000000000004, float("nan"), -1, float("inf"), 4.000000000000001, float("inf"), True, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), 2.68156158598852e+154, float("inf"), float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_536():
    assert v72_bounded(2.0000000000000004, float("inf"), float("nan"), float("nan"), 0, float("inf"), -4.000000000000001, float("inf"), False, 4.000000000000001, 2.68156158598852e+154, float("nan"), float("inf"), float("inf"), float("nan"), float("nan"), float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_537():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), 2.0000000000000004, -1, float("inf"), float("inf"), float("inf"), False, float("inf"), float("nan"), float("nan"), 2.68156158598852e+154, float("inf"), float("inf"), -2.68156158598852e+154, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_538():
    assert v72_bounded(float("inf"), 2.0000000000000004, float("nan"), float("nan"), -1, 4.000000000000001, float("nan"), float("inf"), False, 4.000000000000001, float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154) == [-0.707106781, 0.707106781]

def test_v72_bounded_539():
    assert v72_bounded(2.0000000000000004, float("inf"), 2.0000000000000004, float("nan"), 0, float("inf"), float("inf"), float("inf"), False, -5e-324, float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), -2.68156158598852e+154, 2.68156158598852e+154) == [0.707106781, -0.707106781]

def test_v72_bounded_540():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), -2.0000000000000004, 0, 4.000000000000001, float("nan"), -4.000000000000001, True, float("inf"), float("nan"), 2.68156158598852e+154, -2.68156158598852e+154, float("inf"), float("inf"), float("inf"), 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_541():
    assert v72_bounded(float("inf"), float("inf"), 2.0000000000000004, -2.0000000000000004, 4, float("inf"), -5e-324, float("inf"), False, float("nan"), float("nan"), float("nan"), float("inf"), 3.3376107877608025e-307, float("inf"), float("inf"), 2.68156158598852e+154) == [-0.0, -1.0]

def test_v72_bounded_542():
    assert v72_bounded(2.0000000000000004, 2.0000000000000004, float("nan"), float("nan"), -1, float("inf"), float("inf"), float("inf"), False, -5e-324, float("nan"), float("nan"), 2.68156158598852e+154, 3.3376107877608025e-307, float("nan"), float("nan"), float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_543():
    assert v72_bounded(2.0000000000000004, 2.0000000000000004, float("nan"), float("nan"), 0, float("inf"), float("inf"), float("inf"), True, float("inf"), 2.68156158598852e+154, float("nan"), 2.68156158598852e+154, float("inf"), float("inf"), float("inf"), float("inf")) == [0.707106781, 0.707106781]

def test_v72_bounded_544():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), float("inf"), 4.000000000000001, False, -4.000000000000001, 2.68156158598852e+154, float("nan"), float("inf"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154) == [-0.707106781, -0.707106781]

def test_v72_bounded_545():
    assert v72_bounded(2.0000000000000018, float("nan"), float("nan"), float("inf"), 0, float("inf"), float("inf"), 4.000000000000002, False, float("nan"), float("nan"), float("nan"), 2.68156158598852e+154, float("inf"), float("inf"), 2.68156158598852e+154, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_546():
    assert v72_bounded(float("inf"), float("nan"), float("nan"), 2.0000000000000004, 0, float("inf"), float("inf"), float("inf"), False, 4.000000000000001, float("nan"), -2.68156158598852e+154, float("inf"), float("inf"), 2.68156158598852e+154, float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_547():
    assert v72_bounded(2.0000000000000004, float("inf"), float("nan"), 2.0000000000000004, 0, float("inf"), 4.000000000000001, float("inf"), True, -5e-324, float("nan"), -2.68156158598852e+154, float("inf"), float("inf"), float("inf"), 2.68156158598852e+154, float("inf")) == [0.707106781, -0.707106781]

def test_v72_bounded_548():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), 2.0000000000000004, 0, float("inf"), 4.000000000000001, 4.000000000000001, False, float("inf"), float("nan"), -2.68156158598852e+154, float("inf"), float("inf"), float("inf"), -5e-324, 2.68156158598852e+154) == [-0.707106781, -0.707106781]

def test_v72_bounded_549():
    assert v72_bounded(2.0000000000000004, 2.0000000000000004, 2.0000000000000004, 2.0000000000000004, 0, float("inf"), float("inf"), float("inf"), False, -4.000000000000001, float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_550():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), 2.0000000000000004, 4, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), float("nan"), -2.68156158598852e+154, float("inf"), float("inf"), 2.68156158598852e+154, float("nan")) == [0.0, 1.0]

def test_v72_bounded_551():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, 4.000000000000001, float("inf"), float("inf"), True, float("inf"), float("nan"), 2.68156158598852e+154, 2.68156158598852e+154, float("inf"), float("inf"), 2.68156158598852e+154, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_552():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), float("nan"), 2.68156158598852e+154, float("inf"), 2.68156158598852e+154, 2.68156158598852e+154, float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_553():
    assert v72_bounded(2.0000000000000004, float("inf"), float("nan"), float("nan"), 0, 4.000000000000001, 4.000000000000001, float("inf"), False, float("inf"), 2.68156158598852e+154, 2.68156158598852e+154, float("inf"), float("inf"), float("nan"), float("nan"), float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_554():
    assert v72_bounded(float("inf"), 2.0000000000000004, float("nan"), float("nan"), -1, float("inf"), float("inf"), float("inf"), False, float("inf"), float("nan"), 2.68156158598852e+154, float("inf"), 2.68156158598852e+154, 2.68156158598852e+154, float("nan"), float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_555():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), 0, 4.000000000000001, float("inf"), 4.000000000000001, False, -4.000000000000001, float("nan"), float("nan"), float("inf"), 2.68156158598852e+154, 2.68156158598852e+154, float("nan"), float("nan")) == [-0.707106781, -0.707106781]

def test_v72_bounded_556():
    assert v72_bounded(float("inf"), float("inf"), -2.0000000000000004, float("inf"), -1, float("inf"), float("inf"), 4.000000000000001, True, -5e-324, float("nan"), 2.68156158598852e+154, float("inf"), 2.68156158598852e+154, float("inf"), 2.68156158598852e+154, float("inf")) == [-0.707106781, -0.707106781]

def test_v72_bounded_557():
    assert v72_bounded(float("inf"), 2.0000000000000004, 2.0000000000000004, 2.0000000000000004, 0, 4.000000000000001, 8.000000000000002, -4.000000000000001, False, 4.000000000000001, 5e-324, 5e-324, float("inf"), 2.68156158598852e+154, float("nan"), float("nan"), float("nan")) == [-0.707106781, 0.707106781]

def test_v72_bounded_558():
    assert v72_bounded(-2.0000000000000004, -2.0000000000000004, float("nan"), 2.0000000000000004, 0, -4.000000000000001, -4.000000000000001, 4.000000000000001, False, float("inf"), float("nan"), float("nan"), float("inf"), float("inf"), float("inf"), 2.68156158598852e+154, 0.0) == [-0.707106781, -0.707106781]

def test_v72_bounded_559():
    assert v72_bounded(float("inf"), float("inf"), float("nan"), float("nan"), -1, 4.000000000000001, float("inf"), 4.000000000000001, True, float("inf"), -2.68156158598852e+154, float("nan"), float("inf"), float("inf"), float("inf"), -2.68156158598852e+154, 2.68156158598852e+154) == [-0.707106781, -0.707106781]

def test_v72_bounded_560():
    assert v72_bounded(float("inf"), float("inf"), 2.0000000000000004, 2.0000000000000004, -1, float("inf"), float("inf"), -4.000000000000001, False, 4.000000000000001, float("nan"), float("nan"), 2.68156158598852e+154, float("inf"), float("inf"), float("inf"), 2.68156158598852e+154) == [-0.707106781, -0.707106781]

def test_v72_bounded_561():
    assert v72_bounded(2.0000000000000004, float("inf"), 2.0000000000000004, float("nan"), -1, float("inf"), 4.000000000000001, float("inf"), False, float("inf"), float("nan"), 2.68156158598852e+154, 2.68156158598852e+154, 2.68156158598852e+154, float("nan"), float("nan"), float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_562():
    assert v72_bounded(-2.0000000000000004, float("inf"), float("nan"), -2.0000000000000004, 4, 4.000000000000001, float("inf"), float("inf"), True, float("inf"), float("nan"), float("nan"), 2.68156158598852e+154, 3.3376107877608025e-307, float("inf"), float("inf"), 2.68156158598852e+154) == [-0.0, -1.0]

def test_v72_bounded_563():
    assert v72_bounded(2.0000000000000004, float("inf"), 2.0000000000000004, -2.0000000000000004, 0, 4.000000000000001, float("inf"), -5e-324, False, 4.000000000000001, 2.68156158598852e+154, 2.68156158598852e+154, float("inf"), float("inf"), float("inf"), 2.68156158598852e+154, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_564():
    assert v72_bounded(2.0000000000000004, float("inf"), float("nan"), float("nan"), 0, float("inf"), -4.000000000000001, 4.000000000000001, False, float("inf"), 2.68156158598852e+154, float("nan"), 2.68156158598852e+154, 2.68156158598852e+154, 2.68156158598852e+154, float("nan"), float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_565():
    assert v72_bounded(2.0000000000000004, 2.0000000000000004, -2.0000000000000004, 2.0000000000000004, -1, 4.000000000000001, -4.000000000000001, -4.000000000000001, False, float("inf"), float("nan"), 2.68156158598852e+154, float("inf"), 2.68156158598852e+154, float("nan"), float("nan"), float("nan")) == [0.707106781, 0.707106781]

def test_v72_bounded_566():
    assert v72_bounded(2.0000000000000004, -2.0000000000000004, float("nan"), 2.0000000000000004, 0, -5e-324, float("inf"), 4.000000000000001, False, 4.000000000000001, float("nan"), 2.68156158598852e+154, -2.68156158598852e+154, float("inf"), 2.68156158598852e+154, 2.68156158598852e+154, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_567():
    assert v72_bounded(2.0000000000000004, float("inf"), float("nan"), 2.0000000000000004, 0, 4.000000000000001, 4.000000000000001, float("inf"), False, 4.000000000000001, 2.68156158598852e+154, -2.68156158598852e+154, float("inf"), float("inf"), 2.68156158598852e+154, 2.68156158598852e+154, float("nan")) == [0.707106781, -0.707106781]

def test_v72_bounded_568():
    assert v72_bounded(-2.0000000000000004, 2.0000000000000004, 2.0000000000000004, -2.0000000000000004, 0, float("inf"), 4.000000000000001, 4.000000000000001, True, 4.000000000000001, float("nan"), 2.68156158598852e+154, 2.68156158598852e+154, 2.68156158598852e+154, float("inf"), float("inf"), float("inf")) == [-0.707106781, 0.707106781]



def test_diffbehavior_v62_vs_v72_straight_retreat():
    """CrossHair diffbehavior counterexample (classified: intended v72 fix). Three threats due west: v62 retreats
    straight east (kiting), v72 keeps v39's diagonal because the sideways gain (0.046) is below its margin."""
    from crosshair_props import v62_bounded
    args = (2.0000000000000004, 2.0000000000000004, 2.0000000000000004, 5e-324, 4, 4.000000000000001, float("inf"),
            4.000000000000001, False, 4.000000000000001, float("inf"), 2.68156158598852e+154, float("inf"), float("inf"),
            float("inf"), float("nan"), 2.68156158598852e+154)
    assert v62_bounded(*args) == [1.0, 0.0]
    assert v72_bounded(*args) == [0.707106781, 0.707106781]
