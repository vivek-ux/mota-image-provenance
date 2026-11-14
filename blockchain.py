"""
ProvenanceAI: Cryptographic Proof-of-Provenance Blockchain Ledger
Department of Computer Science & Engineering, NIT Meghalaya
Author: Vivek Negi (T25CS012) | Supervisor: Dr. Akhilendra Pratap Singh
"""

import hashlib
import json
import time
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

LEDGER_PATH = os.path.join(os.path.dirname(__file__), "blockchain_ledger.json")

def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

@dataclass
class ProvenanceRecord:
    image_hash: str          # SHA-256 of raw image bytes
    title: str               # Image name/title
    author: str              # Creator / Notarizer identity
    timestamp: float         # Unix timestamp of creation
    datetime_str: str        # Human-readable timestamp
    dimensions: str          # WxH
    perceptual_hash: str     # Perceptual hash for fuzzy matching
    is_composite: bool       # True if composite / derivative
    parent_hashes: List[str] # Empty for original, [Parent A, Parent B] for composite

@dataclass
class Block:
    index: int
    timestamp: float
    datetime_str: str
    records: List[Dict]
    previous_hash: str
    nonce: int
    current_hash: str

    @staticmethod
    def calculate_hash(index: int, timestamp: float, records: List[Dict], previous_hash: str, nonce: int) -> str:
        record_str = json.dumps(records, sort_keys=True)
        block_content = f"{index}{timestamp}{record_str}{previous_hash}{nonce}"
        return hashlib.sha256(block_content.encode("utf-8")).hexdigest()

class ProvenanceBlockchain:
    def __init__(self, ledger_file: str = LEDGER_PATH):
        self.ledger_file = ledger_file
        self.chain: List[Block] = []
        self.difficulty = 2  # Mining difficulty (e.g. hash starts with '00')
        self.load_or_create()

    def create_genesis_block(self):
        genesis_record = ProvenanceRecord(
            image_hash="0" * 64,
            title="NIT Meghalaya ProvenanceAI Genesis",
            author="System Admin (NITM CSE)",
            timestamp=1793491200.0,
            datetime_str="2026-11-01 00:00:00 UTC",
            dimensions="0x0",
            perceptual_hash="00000000",
            is_composite=False,
            parent_hashes=[]
        )
        t = time.time()
        dt_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(t))
        records = [asdict(genesis_record)]
        h = Block.calculate_hash(0, t, records, "0" * 64, 0)
        genesis = Block(0, t, dt_str, records, "0" * 64, 0, h)
        self.chain = [genesis]
        self.save()

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def get_block_height(self) -> int:
        return len(self.chain)

    def notarize_image(
        self,
        image_bytes: bytes,
        title: str,
        author: str = "Vivek Negi",
        dimensions: str = "512x512",
        perceptual_hash: str = "N/A",
        is_composite: bool = False,
        parent_hashes: Optional[List[str]] = None
    ) -> Dict:
        """
        Creates an immutable on-chain record for a new or composite image.
        """
        img_hash = compute_sha256(image_bytes)
        now = time.time()
        dt_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(now))

        record = ProvenanceRecord(
            image_hash=img_hash,
            title=title,
            author=author,
            timestamp=now,
            datetime_str=dt_str,
            dimensions=dimensions,
            perceptual_hash=perceptual_hash,
            is_composite=is_composite,
            parent_hashes=parent_hashes or []
        )

        # Mine new block
        prev_block = self.get_latest_block()
        new_index = prev_block.index + 1
        records_dict = [asdict(record)]
        nonce = 0
        target_prefix = "0" * self.difficulty

        while True:
            candidate_hash = Block.calculate_hash(new_index, now, records_dict, prev_block.current_hash, nonce)
            if candidate_hash.startswith(target_prefix):
                break
            nonce += 1

        new_block = Block(
            index=new_index,
            timestamp=now,
            datetime_str=dt_str,
            records=records_dict,
            previous_hash=prev_block.current_hash,
            nonce=nonce,
            current_hash=candidate_hash
        )

        self.chain.append(new_block)
        self.save()

        return {
            "block_index": new_index,
            "block_hash": candidate_hash,
            "image_hash": img_hash,
            "timestamp": dt_str,
            "nonce": nonce,
            "author": author,
            "title": title
        }

    def find_record_by_hash(self, img_hash: str) -> Optional[Dict]:
        for block in self.chain:
            for rec in block.records:
                if rec.get("image_hash") == img_hash:
                    return {
                        "block_index": block.index,
                        "block_hash": block.current_hash,
                        "record": rec
                    }
        return None

    def verify_temporal_precedence(self, parent_hash: str, composite_timestamp: float) -> Dict:
        """
        Mathematically verifies that a parent image was notarized on-chain
        BEFORE the creation of the composite image.
        """
        found = self.find_record_by_hash(parent_hash)
        if not found:
            return {"verified": False, "reason": "Parent hash not found in on-chain ledger"}

        parent_ts = found["record"]["timestamp"]
        if parent_ts <= composite_timestamp:
            return {
                "verified": True,
                "parent_title": found["record"]["title"],
                "parent_author": found["record"]["author"],
                "parent_notarized_at": found["record"]["datetime_str"],
                "time_difference_sec": round(composite_timestamp - parent_ts, 2),
                "block_index": found["block_index"],
                "block_hash": found["block_hash"]
            }
        else:
            return {
                "verified": False,
                "reason": "Parent timestamp post-dates composite! (Contradiction)"
            }

    def save(self):
        data = [asdict(b) for b in self.chain]
        with open(self.ledger_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_or_create(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, "r") as f:
                    data = json.load(f)
                    self.chain = [Block(**b) for b in data]
                return
            except Exception:
                pass
        self.create_genesis_block()
