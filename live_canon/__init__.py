"""live_canon/__init__.py — Live Canon: AI-Writings as a navigable cell fabric.

This is the PyPI package version of the Live Canon. It exposes the
LiveCanon class with the 5 novel operations:
  1. NAVIGATE  - BFS through citations
  2. CONFLUENCE - join 2+ papers, suggest synthesis
  3. LINEAGE   - trace F-number through time
  4. GHOST     - find paper that should exist by shape proximity
  5. TICK      - re-balance the canon

Polyformal: byte-exact with Python, C99, Rust, Verilog, VHDL, JavaScript.
State hash = 0xbf27a3631cdee337 for the 9 bundled papers.
"""
from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

__version__ = "0.1.0"
__all__ = ["LiveCanon", "DEFAULT_CANON", "fnv1a_64", "cell_to_dials", "state_hash"]


# FNV-1a 64-bit hash (UTF-8, byte-exact with Python/C/Rust/Verilog/VHDL/JS)
def fnv1a_64(s: str) -> int:
    h = 0xCBF29CE484222325
    for byte in s.encode("utf-8"):
        h ^= byte
        h = (h * 0x00000100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


# Cell encoding (16 x Q1.15 dials, byte-exact with the worker)
def cell_to_dials(paper: Dict[str, Any]) -> List[int]:
    year = int(paper.get("date", "1970-01-01")[:4]) if paper.get("date") else 1970
    year_q = (year - 1970) * 546
    phase_q = paper.get("phase", 0) * 218
    f_q = paper.get("f_number", 0) * 218
    n_refs = len(paper.get("ref_papers", [])) + len(paper.get("ref_f_numbers", []))
    n_refs_q = min(0x7FFF, n_refs * 256)
    th = fnv1a_64(paper.get("title", ""))
    title_lo = th & 0xFFFF
    title_hi = (th >> 16) & 0xFFFF
    num = min(paper.get("number", 0), 500)
    num_q = num * 131
    return [num_q, title_lo, f_q, phase_q, year_q, n_refs_q, title_hi, 0,
            0, 0, 0, 0, 0, 0, 0, 0]


# State hash (FNV-1a over sorted dials)
def state_hash(papers: Dict[int, Dict]) -> int:
    all_dials = [cell_to_dials(p) for p in papers.values()]
    all_dials.sort(key=lambda d: d[0])
    h = 0xCBF29CE484222325
    for d in all_dials:
        for v in d:
            lo = v & 0xFF
            hi = (v >> 8) & 0xFF
            h ^= lo
            h = (h * 0x00000100000001B3) & 0xFFFFFFFFFFFFFFFF
            h ^= hi
            h = (h * 0x00000100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def _cosine(a, b):
    dot = na = nb = 0.0
    for i in range(16):
        dot += a[i] * b[i]
        na += a[i] * a[i]
        nb += b[i] * b[i]
    na = math.sqrt(na)
    nb = math.sqrt(nb)
    return dot / (na * nb) if na and nb else 0.0


# Default 9-paper canon (F115-F130 polyformalism cascade)
DEFAULT_CANON: Dict[int, Dict] = {
    425: {"number": 425, "title": "F115 — The Logical Routes: VHDL × Verilog × the QUF bit-exactness", "f_number": 115, "phase": 237, "date": "2026-09-03", "ref_papers": [426, 427], "ref_f_numbers": []},
    426: {"number": 426, "title": "F116 — The 5+1+1+1+1+1+1+1+1+1+1 Opcodes in 5 Substrates: A Polyformalism Atlas", "f_number": 116, "phase": 238, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [115]},
    427: {"number": 427, "title": "F117 — The 5-Substrate Polyformalism: Python × C × Rust × Verilog × VHDL, One Cell", "f_number": 117, "phase": 239, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [115, 116]},
    428: {"number": 428, "title": "F118 — The Polyformalism in Production: A Play-Test + Benchmark", "f_number": 118, "phase": 240, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [115, 116, 117]},
    429: {"number": 429, "title": "F119 — The 6-Substrate Polyformalism: cell-runtime Joins the Canon", "f_number": 119, "phase": 241, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [115, 116, 117, 118]},
    432: {"number": 432, "title": "F122 — The Shape Store: 5 Indices on Cloudflare Vectorize", "f_number": 122, "phase": 244, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [120, 121]},
    433: {"number": 433, "title": "F123 — The Composer Agent: 5 Cells, 80 Parameters", "f_number": 123, "phase": 245, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [120, 122]},
    439: {"number": 439, "title": "F129 — The Live Canon: Papers as Cells, Reading as Navigation", "f_number": 129, "phase": 251, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [115, 120, 122, 125]},
    440: {"number": 440, "title": "F130 — The Polyformal Live Canon: One Cell, Five Substrates", "f_number": 130, "phase": 251, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [115, 129]},
}


class LiveCanon:
    """The Live Canon — read papers as a navigable cell fabric."""

    def __init__(self, canon: Optional[Dict[int, Dict]] = None):
        self.canon = canon or dict(DEFAULT_CANON)

    @property
    def state_hash(self) -> int:
        return state_hash(self.canon)

    @property
    def state_hash_string(self) -> str:
        return f"0x{self.state_hash:016x}"

    @property
    def paper_count(self) -> int:
        return len(self.canon)

    def papers(self):
        return list(self.canon.values())

    def navigate(self, start: int, depth: int = 2) -> List[Dict]:
        visited: Set[int] = {start}
        result = []
        queue = [(start, 0)]
        while queue:
            num, d = queue.pop(0)
            paper = self.canon.get(num)
            if paper:
                result.append({"depth": d, "paper": paper})
                if d < depth:
                    for ref in paper.get("ref_papers", []):
                        if ref in self.canon and ref not in visited:
                            visited.add(ref)
                            queue.append((ref, d + 1))
        return result

    def confluence(self, paper_nums: List[int]) -> Dict:
        if not paper_nums:
            return {"error": "no papers"}
        shared_refs: Optional[Set] = None
        shared_f: Optional[Set] = None
        titles = []
        for num in paper_nums:
            p = self.canon.get(num)
            if not p:
                continue
            titles.append(p["title"])
            refs = set(p.get("ref_papers", []))
            shared_refs = set(refs) if shared_refs is None else shared_refs & refs
            fs = set(p.get("ref_f_numbers", []))
            shared_f = set(fs) if shared_f is None else shared_f & fs
        suggested = f"Composition of {len(paper_nums)} papers"
        if shared_f:
            first = min(shared_f)
            suggested = f"F{first} Synthesis: {', '.join(titles)}"
        max_n = max(self.canon.keys())
        return {
            "input_papers": paper_nums,
            "input_titles": titles,
            "shared_refs": sorted(shared_refs) if shared_refs else [],
            "shared_f_numbers": sorted(shared_f) if shared_f else [],
            "suggested_title": suggested,
            "ghost_paper": f"paper-{max_n + 1}.md",
        }

    def lineage(self, f_number: int) -> List[Dict]:
        result = [p for p in self.canon.values() if f_number in p.get("ref_f_numbers", [])]
        result.sort(key=lambda p: (p.get("phase", 0), p.get("number", 0)))
        return result

    def ghost(self, paper_num: int, k: int = 5) -> Dict:
        target = self.canon.get(paper_num)
        if not target:
            return {"error": "missing paper"}
        target_dials = cell_to_dials(target)
        scored = []
        for n, p in self.canon.items():
            if n == paper_num:
                continue
            score = _cosine(target_dials, cell_to_dials(p))
            scored.append({"id": f"p{n:04d}", "score": round(score, 4)})
        scored.sort(key=lambda x: -x["score"])
        return {
            "source_paper": f"paper-{paper_num}.md",
            "neighbors": scored[:k],
            "suggested_title": f"A Bridge between F{target.get('f_number', 0)} and its neighbors",
        }

    def tick(self) -> Dict:
        return {"ticked_cells": self.paper_count}
