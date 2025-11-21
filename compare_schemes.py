#!/usr/bin/env python3
import argparse

def parse_args():
    p = argparse.ArgumentParser(
        description="Compare cost of two zk-proof parameter sets."
    )
    p.add_argument("--num-proofs", type=int, required=True,
                   help="Number of proofs to estimate.")
    p.add_argument("--gas-per-proof-a", type=int, required=True,
                   help="Gas cost per proof for scheme A.")
    p.add_argument("--gas-per-proof-b", type=int, required=True,
                   help="Gas cost per proof for scheme B.")
    p.add_argument("--gas-price-gwei", type=float, required=True,
                   help="Gas price in gwei (e.g. 30).")
    p.add_argument("--eth-price-usd", type=float, required=True,
                   help="ETH price in USD (e.g. 3200).")
    return p.parse_args()

def estimate_cost(num_proofs, gas_per_proof, gas_price_gwei, eth_price_usd):
    """Return (total_gas, total_eth, total_usd) for a given scheme."""
    total_gas = num_proofs * gas_per_proof
    total_eth = total_gas * gas_price_gwei * 1e-9  # gwei->ETH
    total_usd = total_eth * eth_price_usd
    return total_gas, total_eth, total_usd

def main():
    args = parse_args()
    num = args.num_proofs
    gas_price = args.gas_price_gwei
    eth_usd = args.eth_price_usd

    gas_a, eth_a, usd_a = estimate_cost(num, args.gas_per_proof_a, gas_price, eth_usd)
    gas_b, eth_b, usd_b = estimate_cost(num, args.gas_per_proof_b, gas_price, eth_usd)

    print("Scheme A:")
    print(f"  Gas per proof      : {args.gas_per_proof_a:,} gas")
    print(f"  Total gas (A)      : {gas_a:,} gas")
    print(f"  Total cost (A)     : {eth_a:.6f} ETH ≈ ${usd_a:,.2f}")

    print("\nScheme B:")
    print(f"  Gas per proof      : {args.gas-per_proof_b:,} gas")
    print(f"  Total gas (B)      : {gas_b:,} gas")
    print(f"  Total cost (B)     : {eth_b:.6f} ETH ≈ ${usd_b:,.2f}")

    diff_usd = usd_b - usd_a
    diff_eth = eth_b - eth_a
    print("\nComparison (B minus A):")
    print(f"  Extra cost         : {diff_eth:.6f} ETH ≈ ${diff_usd:,.2f}")
    if diff_usd > 0:
        print("  => Scheme B is more expensive.")
    elif diff_usd < 0:
        print("  => Scheme B is cheaper.")
    else:
        print("  => Costs are equal.")

if __name__ == "__main__":
    main()
