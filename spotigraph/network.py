import unicodedata
import re
from typing import List, Tuple
from pathlib import Path

from .types import Artist

from .explore import get_first_gen


def build_links(
    nodes: List[Artist], verbose: bool = False
) -> List[Tuple[Artist, Artist]]:
    """Build link list: A->B if B is in related artist of A"""
    links = []
    for node in nodes:
        if verbose:
            print("-----------")
            print(node.name)
        related_nodes = get_first_gen(node.id)
        for related in related_nodes:
            if related in nodes:
                links.append((node, related))
                if verbose:
                    print("   ", related.name)
    return links


def normalize_name(artist_name: str) -> str:
    """Remove special char from string."""
    artist_name = unicodedata.normalize("NFKD", artist_name)
    artist_name = re.sub("\W+", "", artist_name)
    return artist_name


def to_integer_indexed_graph(
    nodes: List[Artist], links: List[Tuple[Artist, Artist]]
) -> Tuple[List[Artist], List[Tuple[int, int]]]:
    """Replace Artist Type node to interger id."""
    sorted_nodes = sorted(nodes, key=lambda n: n.id)
    node_id_to_idx = {node.id: idx for idx, node in enumerate(sorted_nodes)}

    links_by_ids = [
        (node_id_to_idx[src.id], node_id_to_idx[tgt.id]) for src, tgt in links
    ]
    return sorted_nodes, links_by_ids


def export_to_pajek(
    output_path: str, sorted_nodes: List[Artist], links_by_ids: List[Tuple[int, int]]
) -> None:
    """Export to Pajek text format."""
    Path(output_path).parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, "w") as f:

        f.write(f"*Vertices {len(sorted_nodes)}\n")
        for idx, node in enumerate(sorted_nodes):
            f.write(f'{idx} "{normalize_name(node.name)}"\n')

        f.write("\n")
        f.write(f"*Edges {len(links_by_ids)}\n")
        for idx_a, idx_b in links_by_ids:
            f.write(f"{idx_a} {idx_b}\n")

    print(f"Graph saved to {output_path}")
