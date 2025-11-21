#!/usr/bin/env python3
import argparse


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Quick zk proof cost estimator (gas + USD)."
    )
    p.add_argument("--num-proofs", type=int, required=True,
                   help="Number of proofs.")
    p.add_argument("--gas-per-proof", type=int, required=True,
                   help="On-chain gas cost per proof (verification, etc.).")
    p.add_argument("--gas-price-gwei", type=float, required=True,
                   help="Gas price in gwei (e.g. 30).")
    p.add_argument("--eth-price-usd", type=float, required=True,
                   help="ETH price in USD (e.g. 3200).")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    num = args.num_proofs
        if num > 10_000_000:
        print("WARNING: num_proofs is very large; check that this is intentional.")
    gas_per = args.gas_per_proof
    gas_price_gwei = args.gas_price_gwei
    eth_price = args.eth_price_usd

    total_gas = num * gas_per                     # gas
    total_eth = total_gas * gas_price_gwei * 1e-9  # gwei -> ETH
    total_usd = total_eth * eth_price

    print(f"Number of proofs      : {num}")
    print(f"Gas per proof         : {gas_per:,} gas")
    print(f"Total gas             : {total_gas:,} gas")
    print(f"Gas price             : {gas_price_gwei:.3f} gwei")
    print(f"ETH price             : ${eth_price:,.2f} / ETH")
    print("-" * 40)
    print(f"Total cost (ETH)      : {total_eth:.6f} ETH")
    print(f"Total cost (USD)      : ${total_usd:,.2f}")


if __name__ == "__main__":
    main()
