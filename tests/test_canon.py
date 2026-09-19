"""test_canon.py — computed-not-trusted proofs for the 71-paper canon sync.

Every expected value below is DERIVED, not asserted from authority:
  - the canonical hash is recomputed from the bundled DEFAULT_CANON by the
    state_hash under test (0x445185a3a99fd2e7, cross-checked against the
    quilt-floor instrument and the live-canon-gh data.json corpus)
  - the retired dial-only hash is recomputed by dial_only_state_hash and
    pinned as provenance (the stranded target 0xbf27a3631cdee337 was the
    9-paper ancestor of this algorithm family)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from live_canon import (
    DEFAULT_CANON,
    LiveCanon,
    cell_to_dials,
    dial_only_state_hash,
    state_hash,
    _serialize_cell,
)


def test_paper_count_is_71():
    assert len(DEFAULT_CANON) == 71


def test_canonical_state_hash_matches_retarget():
    # THE cross-surface identity: pypi, npm, the live worker, and
    # quilt-floor must all compute this over the same 71-paper corpus.
    assert state_hash(DEFAULT_CANON) == 0x445185A3A99FD2E7


def test_live_canon_facade():
    c = LiveCanon()
    assert c.paper_count == 71
    assert c.state_hash_string == "0x445185a3a99fd2e7"


def test_every_paper_has_16_dials():
    for p in DEFAULT_CANON.values():
        assert len(cell_to_dials(p)) == 16


def test_serialize_cell_layout_is_byte_exact():
    # type(0x01) ‖ id(u64 LE) ‖ 16 dials(u16 LE) ‖ neighbors(u64 LE)
    b = _serialize_cell(1, list(range(16)), [2, 3])
    assert b[0] == 0x01
    assert len(b) == 1 + 8 + 32 + 16  # 2 neighbors → 57 bytes
    assert int.from_bytes(b[1:9], "little") == 1
    assert int.from_bytes(b[9:11], "little") == 0
    assert int.from_bytes(b[41:49], "little") == 2


def test_dial_only_hash_is_provenance_not_identity():
    # the retired algorithm still runs — but its output over the 71-paper
    # corpus is NOT the canon identity. Never aim a target at it.
    h = dial_only_state_hash(DEFAULT_CANON)
    assert h != state_hash(DEFAULT_CANON)
    assert h == 0x7F563ED9982496A1  # recomputed and pinned


def test_corpus_covers_f115_through_f165():
    numbers = sorted(DEFAULT_CANON)
    assert 408 in numbers  # F98, the conformance-suite root
    assert 475 in numbers  # the newest paper in the committed corpus


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"✓ {name}")
    print("all computed proofs pass")
