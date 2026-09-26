from check import legal_target, solve_target, valid_target


def test_hand_cases():
    empty = {"vertices": 0, "edges": []}
    assert solve_target(empty) == {"heads": []}
    one_loop = {"vertices": 1, "edges": [[0, 0]]}
    assert solve_target(one_loop) == {"status": "NO-SOLUTION"}
    two_parallel = {"vertices": 2, "edges": [[0, 1], [0, 1]]}
    assert valid_target(two_parallel, {"heads": [0, 0]})
    assert not valid_target(two_parallel, {"heads": [0, 1]})
    four_loops = {"vertices": 1, "edges": [[0, 0]] * 4}
    assert valid_target(four_loops, {"heads": [0] * 4})
    assert not legal_target({"vertices": 1, "edges": []})


if __name__ == "__main__":
    test_hand_cases()
