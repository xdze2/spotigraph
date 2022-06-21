# TreeMap
from scipy.cluster.hierarchy import dendrogram, linkage, leaves_list, ClusterNode
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class TreeNode:
    top_left: np.ndarray
    bottom_right: np.ndarray
    is_leaf: bool
    z_node: ClusterNode
    top_or_left_area: float
    bottom_or_right_area: float
    top_or_left_node: "TreeNode" = None
    bottom_or_right_node: "TreeNode" = None
    node_id: str = None


@dataclass
class Rect:
    top_left: np.ndarray
    bottom_right: np.ndarray


def iter_leaf(node: ClusterNode, rect: Rect):

    if node.is_leaf():
        center = (rect.top_left + rect.bottom_right) / 2
        yield center
    else:
        left_rect, right_rect = split_rect(rect, node.left.count, node.right.count)
        yield from iter_leaf(node.left, left_rect)
        yield from iter_leaf(node.right, right_rect)


def split_rect(rect: Rect, count_a: float, count_b: float) -> Tuple[Rect, Rect]:
    top_left = rect.top_left
    bottom_right = rect.bottom_right
    diag = top_left - bottom_right
    ratio = count_a / (count_a + count_b)
    if diag[1] > diag[0]:
        # split vertical
        tl_a = top_left
        br_a = bottom_right + np.array([0, diag[1] * ratio])

        tl_b = top_left - np.array([0, diag[1] * ratio])
        br_b = bottom_right

    else:
        # split horizontal
        tl_a = top_left
        br_a = bottom_right + np.array([diag[0] * ratio, 0])

        tl_b = top_left - np.array([diag[0] * ratio, 0])
        br_b = bottom_right

    return (Rect(tl_a, br_a), Rect(tl_b, br_b))
