from closest_sum_to_zero_after_sign_flip_python import closest_sum_to_zero_after_sign_flip_python


def test_example_1():
    nums = [1, 3, 2, 5]
    assert closest_sum_to_zero_after_sign_flip_python(nums) == 1


def test_example_2():
    nums = [-4, 0, -3, -3]
    assert closest_sum_to_zero_after_sign_flip_python(nums) == 2


def test_example_3():
    nums = [4, -3, 5, -7]
    assert closest_sum_to_zero_after_sign_flip_python(nums) == 1


def test_all_zeros():
    nums = [0, 0, 0]
    assert closest_sum_to_zero_after_sign_flip_python(nums) == 0


def test_single_positive_element():
    nums = [5]
    assert closest_sum_to_zero_after_sign_flip_python(nums) == 5


def test_single_negative_element():
    nums = [-7]
    assert closest_sum_to_zero_after_sign_flip_python(nums) == 7


