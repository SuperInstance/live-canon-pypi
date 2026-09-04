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


# Default 22-paper canon (F115-F140 polyformalism + operational fictions + wearable + negative space)
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
    441: {"number": 441, "title": "F131 — The 3-Package Polyformalism: One Cell, Three Registries", "f_number": 131, "phase": 252, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [115, 130]},
    442: {"number": 442, "title": "F132 — Operational Fictions as Concrete System-Prompt Noun-Phrases", "f_number": 132, "phase": 253, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": []},
    443: {"number": 443, "title": "F133 — Operational Fictions as Falsifiable Claims (avg divergence 0.861)", "f_number": 133, "phase": 254, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [132]},
    444: {"number": 444, "title": "F134 — The Quilt Cowboy: Orchestrator Over 12 Cheap Voices", "f_number": 134, "phase": 254, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [132, 133]},
    445: {"number": 445, "title": "F135 — The Wheelhouse Test: Scoring Fictions for 0300-in-a-Gale Tolerability", "f_number": 135, "phase": 254, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [132, 133]},
    446: {"number": 446, "title": "F136 — The Edge of the Doctrine — 6 Experiments", "f_number": 136, "phase": 254, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [132, 133, 134, 135]},
    447: {"number": 447, "title": "F137 — The Word-Level Metric is Broken (semantic divergence is real)", "f_number": 137, "phase": 254, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [133, 136]},
    448: {"number": 448, "title": "F138 — The Real Numbers — 12 Pairs with Semantic Divergence (0.231 vs 0.171)", "f_number": 138, "phase": 254, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [133, 137]},
    449: {"number": 449, "title": "F139 — Wearable Neural Devices + Quilt — The Synergy of Signaling-as-Play", "f_number": 139, "phase": 256, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [129, 130, 131]},
    450: {"number": 450, "title": "F140 — The Negative Space: Decomposition × Composition × Double-Entry Bookkeeping of the Self", "f_number": 140, "phase": 257, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [129, 133, 137, 138, 139]},
    451: {"number": 451, "title": "F141 — The Co-Captain: A Symbiotic Digital Twin with a Hand-On / Hands-Off Dial", "f_number": 141, "phase": 258, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [129, 140, 139]},
    452: {"number": 452, "title": "F142 — The Back-Deck Game: Multi-Dimensional Scoring for Industrial Operations", "f_number": 142, "phase": 258, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [140, 141, 143]},
    453: {"number": 453, "title": "F143 — The Mudra-Band Emulator: Webcam-Based Hand Pose for Industrial Training", "f_number": 143, "phase": 258, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [140, 141, 142]},
    454: {"number": 454, "title": "F144 — The Co-Captain in 5 Substrates: A Polyformalism Atlas", "f_number": 144, "phase": 259, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [141, 143]},
    455: {"number": 455, "title": "F145 — Bottle-Router → Cell-Router: Lifting A2A Bottles into Quilt Cells", "f_number": 145, "phase": 259, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [141, 144]},
    456: {"number": 456, "title": "F146 — Real MediaPipe Hands in the Back-Deck Game: From Simulator to Production", "f_number": 146, "phase": 259, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [142, 143]},
    457: {"number": 457, "title": "F150 — Tetris + F140: The Audit Game", "f_number": 150, "phase": 260, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [140, 141, 142, 151]},
    458: {"number": 458, "title": "F151 — The Wheelhouse Game: Weather Routing as an F140 Audit", "f_number": 151, "phase": 260, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [140, 141, 142, 150]},
    459: {"number": 459, "title": "F149 — Quilt for the Crew: A Non-Technical Handbook", "f_number": 149, "phase": 260, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [140, 141, 142, 143, 144, 145, 146, 150, 151]},
  # F148 expansion: 9 older papers
    408: {"number": 408, "title": "F98 — The 165-Test Polyformalism Conformance Suite", "f_number": 98, "phase": 222, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [97]},
    409: {"number": 409, "title": "F99 — The Quilt Atlas: 47 Repositories, 280K Lines of Code, 1500+ Tests", "f_number": 99, "phase": 223, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [100, 115]},
    410: {"number": 410, "title": "F100 — Anatomy of quilt-substrate: 11 Primitives, 4 Properties, 19 Openers, 405 Tests", "f_number": 100, "phase": 224, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [99, 104, 115]},
    414: {"number": 414, "title": "F104 — Polyformalism Benchmark: 1.71 µs/step (C) vs 228 µs/step (Python)", "f_number": 104, "phase": 228, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [100, 115, 116, 117]},
    417: {"number": 417, "title": "F107 — Forecasts as Durable Semantic Objects: Multi-Agent CRDT Merge", "f_number": 107, "phase": 231, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [95, 100]},
    419: {"number": 419, "title": "F109 — The Playtest Workflow: End-to-End Verification of AI Systems", "f_number": 109, "phase": 233, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [98, 100, 115]},
    420: {"number": 420, "title": "F110 — Polyformalism: When the Same Cell Shape Works in C, Python, Rust, and Beyond", "f_number": 110, "phase": 234, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [100, 104, 115, 116, 117, 118]},
    423: {"number": 423, "title": "F113 — QUF: Quilt Universal Format — The 6th Cutting-Edge Adoption", "f_number": 113, "phase": 235, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [100, 115, 116]},
    424: {"number": 424, "title": "F114 — Verilog Cells Meet Time-Series Forecasters: The q_cell × TimeCell Synergy", "f_number": 114, "phase": 236, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [100, 113, 115, 116, 117]},
    461: {"number": 461, "title": "F152 — The Co-Captain REST API: From Local to Fleet", "f_number": 152, "phase": 261, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [141, 144, 145]},
    462: {"number": 462, "title": "F153 — The 5-Substrate Echo Test: Polyformalism as a Deployment Substrate", "f_number": 153, "phase": 261, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [144]},
    463: {"number": 463, "title": "F154 — The Cowbell: A Persistent Crew-Member Notification System", "f_number": 154, "phase": 261, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [141, 142, 149, 151]},
    464: {"number": 464, "title": "F155 — The Canon Zoo: A System Prompt for Inspiration Through Play", "f_number": 155, "phase": 262, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [140, 152, 154, 110, 115]},
    465: {"number": 465, "title": "F156 — The Algebra of the 4-Move Pipeline: R ∘ D ∘ C ∘ L", "f_number": 156, "phase": 263, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [140, 141, 144, 152, 154]},
    466: {"number": 466, "title": "F157 — Canon Expansion II: Lifting F120-F139 from AI-Writings to Live Canon", "f_number": 157, "phase": 263, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [148, 110, 130, 150, 300]},
    467: {"number": 467, "title": "F158 — The Mechanic Doctrine: Agent Priming for Vibe-Coders", "f_number": 158, "phase": 264, "date": "2026-09-03", "ref_papers": [], "ref_f_numbers": [110, 140, 152, 154, 156]},
    468: {"number": 468, "title": "F159 — Seven Novel Enhancements from 2026 Agent-Prompting Best Practices", "f_number": 159, "phase": 265, "date": "2026-09-04", "ref_papers": [], "ref_f_numbers": [158, 110, 140, 152, 156]},
    469: {"number": 469, "title": "F160 — The Working Animal Doctrine: From Mechanic to Shepherd", "f_number": 160, "phase": 266, "date": "2026-09-04", "ref_papers": [], "ref_f_numbers": [158, 110, 115, 140, 154]},
    470: {"number": 470, "title": "F161 — Conservation Laws as Fences: The Physics of Working Animals", "f_number": 161, "phase": 266, "date": "2026-09-04", "ref_papers": [], "ref_f_numbers": [158, 159, 140, 156]},
    471: {"number": 471, "title": "F162 — The PLATO Room Protocol: A Cell as a Room, A Room as a Cell", "f_number": 162, "phase": 266, "date": "2026-09-04", "ref_papers": [], "ref_f_numbers": [115, 116, 117, 118, 119, 161]},
    472: {"number": 472, "title": "F163 — Sonar Vision as 5 Quilt Cells: A Vessel's Perception Decomposed", "f_number": 163, "phase": 267, "date": "2026-09-04", "ref_papers": [], "ref_f_numbers": [115, 117, 119, 144, 161, 162]},
    473: {"number": 473, "title": "F164 — cocapn-marine: The Working Animal Stack for the Vessel", "f_number": 164, "phase": 267, "date": "2026-09-04", "ref_papers": [], "ref_f_numbers": [160, 161, 162, 163]},
    474: {"number": 474, "title": "F165 — The Agent Priming Toolkit: 4 Layers, 3 Jobs, 1 Contract", "f_number": 165, "phase": 268, "date": "2026-09-04", "ref_papers": [], "ref_f_numbers": [158, 159, 160, 161, 162]},
    475: {"number": 475, "title": "F166 — The Mudra Vessel Bridge: Neural Input for Commercial Fishing", "f_number": 166, "phase": 268, "date": "2026-09-04", "ref_papers": [], "ref_f_numbers": [158, 159, 163, 164]},
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
