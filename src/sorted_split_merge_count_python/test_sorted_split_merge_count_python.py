from sorted_split_merge_count_python import sortedSplitMergeCount


def test_readme_example():
    nums = [1, 3, 2, 4]
    assert sortedSplitMergeCount(nums) == 2


def test_min_length_sorted():
    nums = [1, 2]
    assert sortedSplitMergeCount(nums) == 1


def test_min_length_reverse():
    nums = [2, 1]
    assert sortedSplitMergeCount(nums) == 0


def test_already_sorted_all_splits_valid():
    nums = [1, 2, 3, 4, 5]
    # Splits at positions 1..4 => 4 valid
    assert sortedSplitMergeCount(nums) == 4


def test_all_equal_elements():
    nums = [2, 2, 2, 2]
    # All splits valid since max(left) <= min(right) always holds
    assert sortedSplitMergeCount(nums) == 3


def test_one_valid_split_in_middle():
    nums = [3, 1, 2, 4]
    # Only split before last element works
    assert sortedSplitMergeCount(nums) == 1


def test_two_valid_splits():
    nums = [2, 1, 3, 4]
    # Splits after index 1 and 2 are valid
    assert sortedSplitMergeCount(nums) == 2


def test_reverse_sorted_none_valid():
    nums = [4, 3, 2, 1]
    assert sortedSplitMergeCount(nums) == 0


