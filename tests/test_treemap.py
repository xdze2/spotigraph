import numpy as np

from spotigraph.treemap import split_rect, Rect, iter_leaf


def test_split_rect():
    tl = np.array([0, 1])
    br = np.array([1, 0])

    sr0 = split_rect(Rect(tl, br), 5, 5)
    print(sr0)

    np.testing.assert_almost_equal(sr0[0].top_left, np.array([0, 1]))
    np.testing.assert_almost_equal(sr0[0].bottom_right, np.array([1, 0.5]))

    sr1 = split_rect(Rect(tl, np.array([0.1, 0])), 5, 5)
    print(sr1)
    # >>> ((array([0, 1]), array([0.1, 0.5])), (array([0. , 0.5]), array([0.1, 0. ])))

    np.testing.assert_almost_equal(sr1[0].top_left, np.array([0, 1]))
    np.testing.assert_almost_equal(sr1[0].bottom_right, np.array([0.1, 0.5]))




from scipy.cluster import hierarchy

def test_iter_leaf():
    rng = np.random.default_rng(1234)
    x = rng.random((5, 2))
    Z = hierarchy.linkage(x)

    rootnode = hierarchy.to_tree(Z)


    assert rootnode.left.count == 3  # dont change the seed

    rect = Rect(np.array([0, 1]), np.array([1, 0]))
    for leaf in iter_leaf(rootnode, rect):
        print(leaf)

    assert False

test_iter_leaf()