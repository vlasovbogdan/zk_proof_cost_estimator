#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ProvingSystem:
    key: str
    name: str
    family: str
    description: str
    base_ms_per_proof: float      # milliseconds at 128-bit security
    base_usd_per_proof: float     # abstract cost in USD at 128-bit
    scaling_factor: float         # scaling per 10k tx (efficiency factor)


SYSTEMS: Dict[str, ProvingSystem] = {
    "aztec": ProvingSystem(
        key="aztec",
        name="Aztec-style zk SNARK System",
        family="zk-snark",
        description="Privacy-focused zk rollup proving for encrypted state and contracts.",
        base_ms_per_proof=420.0,
        base_usd_per_proof=0.18,
        scaling_factor=0.85,
    ),
    "zama": ProvingSystem(
        key="zama",
        name="Zama-style FHE + Proof Hybrid",
        family="fhe-hybrid",
        description="FHE-heavy design where zk proofs attest to encrypted compute pipelines.",
        base_ms_per_proof=780.0,
        base_usd_per_proof=0.35,
        scaling_factor=0.72,
    ),
    "soundness": ProvingSystem(
        key="soundness",
        name="Soundness-first Minimal Circuit System",
        family="verified-zk",
        description="Formally specified circuits tuned for clarity and soundness over raw speed.",
        base_ms_per_proof=500.0,
        base_usd_per_proof=0.22,
        scaling_factor=0.90,
    ),
}


SECURITY_LEVELS = {
    128: 1.0,
    192: 1.35,
    256: 1.70,
}


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def estimate_cost(
    system: ProvingSystem,
    tx_count: int,
    batch_size: int,
    security_bits: int,
    hardware_scale: float,
) -> Dict[str, Any]:
    if tx_count <= 0:
        raise ValueError("tx_count must be positive.")
    if batch_size <= 0:
        raise ValueError("batch_size must be positive.")
    if security_bits not in SECURITY_LEVELS:
        raise ValueError(f"security_bits must be one of {sorted(SECURITY_LEVELS.keys())}.")
    if hardware_scale <= 0:
        raise ValueError("hardware_scale must be > 0.")

    batches = (tx_count + batch_size - 1) // batch_size
    sec_factor = SECURITY_LEVELS[security_bits]

    # Efficiency improvement/degradation depending on size
    volume_factor = clamp(system.scaling_factor + (tx_count / 10_000) * 0.02, 0.5, 1.25)

    per_proof_ms = system.base_ms_per_proof * sec_factor / hardware_scale
    per_proof_ms *= volume_factor

    per_proof_usd = system.base_usd_per_proof * sec_factor / hardware_scale
    per_proof_usd *= volume_factor

    total_ms = per_proof_ms * batches
    total_usd = per_proof_usd * batches

    per_tx_ms = total_ms / tx_count
    per_tx_usd = total_usd / tx_count

    return {
        "system": system.key,
        "systemName": system.name,
        "family": system.family,
        "description": system.description,
        "securityBits": security_bits,
        "txCount": tx_count,
        "batchSize": batch_size,
        "batches": batches,
        "hardwareScale": hardware_scale,
        "perProofMs": round(per_proof_ms, 3),
        "perProofUsd": round(per_proof_usd, 6),
        "totalMs": round(total_ms, 3),
        "totalUsd": round(total_usd, 6),
        "perTxMs": round(per_tx_ms, 5),
        "perTxUsd": round(per_tx_usd, 8),
        "volumeFactor": round(volume_factor, 4),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="zk_proof_cost_estimator",
        description=(
            "Offline zk/FHE proof cost estimator inspired by Aztec-style zk rollups, "
            "Zama-style FHE hybrids, and soundness-first proving systems."
        ),
    )
    parser.add_argument(
        "tx_count",
        type=int,
        help="Number of transactions you plan to prove.",
    )
    parser.add_argument(
        "--system",
        choices=list(SYSTEMS.keys()),
        default="aztec",
        help="Proving system profile (default: aztec).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=512,
        help="Transactions per proof/batch (default: 512).",
    )
    parser.add_argument(
        "--security-bits",
        type=int,
        choices=sorted(SECURITY_LEVELS.keys()),
        default=128,
        help="Security level in bits (default: 128).",
    )
    parser.add_argument(
        "--hardware-scale",
        type=float,
        default=1.0,
        help="Relative hardware scale factor; >1 for better hardware (default: 1.0).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON instead of human-readable text.",
    )
    return parser.parse_args()


def print_human(summary: Dict[str, Any]) -> None:
    print("🧮 zk_proof_cost_estimator")
    print(f"System        : {summary['systemName']} ({summary['system']})")
    print(f"Family        : {summary['family']}")
    print(f"Description   : {summary['description']}")
    print("")
    print(f"Transactions  : {summary['txCount']}")
    print(f"Batch size    : {summary['batchSize']}")
    print(f"Batches       : {summary['batches']}")
    print(f"Security bits : {summary['securityBits']}")
    print(f"Hardware x    : {summary['hardwareScale']}")
    print(f"Volume factor : {summary['volumeFactor']}")
    print("")
    print("Per-proof estimate:")
    print(f"  Time        : {summary['perProofMs']:.3f} ms")
    print(f"  Cost        : ${summary['perProofUsd']:.6f}")
    print("")
    print("Per-transaction estimate:")
    print(f"  Time        : {summary['perTxMs']:.5f} ms/tx")
    print(f"  Cost        : ${summary['perTxUsd']:.8f} per tx")
    print("")
    print("Total estimate:")
    print(f"  Time        : {summary['totalMs']:.3f} ms")
    print(f"  Cost        : ${summary['totalUsd']:.6f}")


def main() -> None:
    args = parse_args()
    system = SYSTEMS[args.system]

    try:
        summary = estimate_cost(
            system=system,
            tx_count=args.tx_count,
            batch_size=args.batch_size,
            security_bits=args.security_bits,
            hardware_scale=args.hardware_scale,
        )
    except ValueError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print_human(summary)


if __name__ == "__main__":
    main()
