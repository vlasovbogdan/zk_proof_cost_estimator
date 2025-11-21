# zk_proof_cost_estimator

This repository contains a tiny offline estimator for proving costs in Web3-style systems.  
It focuses on architectures inspired by:

- Aztec style zk rollups  
- Zama style FHE plus proof hybrids  
- Soundness first proving systems with formally specified circuits  

The goal is to provide a quick way to reason about how many proofs you might require, how they scale with transaction volume, and what the relative time and abstract cost might look like.



Repository layout

There are exactly two files in the repository:

- app.py  
- README.md  



Concept

zk_proof_cost_estimator does not connect to a blockchain or any RPC endpoint.  
Instead it uses simple profiles and formulas to approximate:

## Why this exists

This tool provides quick, offline proof-cost intuition without requiring
a prover, RPC endpoint, or blockchain node.  
It is meant for early-stage protocol modeling, documentation, research,
and fast comparisons between different proving architectures.

- proof count based on transaction count and batch size  
- effect of security level (128, 192, 256 bits)  
- rough per proof latency in milliseconds  
- rough per proof abstract cost in USD  
- total and per transaction estimates for time and cost  

Three built in proving system profiles are included:

- aztec  
  Represents a zk SNARK style privacy rollup with relatively optimized proof systems for private state.

- zama  
  Represents an FHE heavy system where proving also needs to attest to or compose with encrypted compute pipelines.

- soundness  
  Represents a system whose circuits are designed around clarity and formal soundness, not just raw proving speed.



Installation

Requirements:

- Python 3.10 or newer

Steps:

1. Create a new GitHub repository with any name.  
2. Place app.py and this README.md in the root directory.  
3. Ensure python is available on your PATH.  
4. No external libraries are required; the script uses only the Python standard library.  



Usage

From the root directory of the repository, run:

Estimate using the Aztec style profile:

python app.py 10000

Use the Zama style FHE hybrid with higher security and stronger hardware:

python app.py 20000 --system zama --security-bits 192 --hardware-scale 2.0

Use the soundness first system with smaller batches:

python app.py 8000 --system soundness --batch-size 256

Request JSON output for dashboards or scripts:

python app.py 12000 --system aztec --security-bits 256 --json  



Parameters

tx_count  
Number of transactions you want to include in your estimate.  

system  
Which proving system profile to use. One of aztec, zama, soundness.  

batch_size  
How many transactions feed into a single proof or batch.  

security_bits  
Logical security level in bits. The model supports 128, 192, and 256.  

hardware_scale  
Relative hardware factor compared to a baseline reference. Values larger than 1.0 represent more capable hardware.  



Output

Human readable mode shows:

- system name and family  
- description  
- number of transactions, batch size, and derived batch count  
- security level and hardware scaling  
- per proof time and cost estimates  
- per transaction time and cost estimates  
- total time and cost for the scenario  

JSON mode returns a dictionary with keys such as system, systemName, family, securityBits, txCount, batchSize, batches, perProofMs, perProofUsd, totalMs, totalUsd, perTxMs, perTxUsd, and volumeFactor.  



Notes

- All numbers are illustrative. They do not represent real benchmarking data from Aztec, Zama, or any production system.  
- The model is intentionally simple to make it easy to modify, extend, or embed into other tools.  
- You can add more proving systems, adjust base costs, or change the scaling logic to align with your own measurements.
