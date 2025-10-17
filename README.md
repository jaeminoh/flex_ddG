# Flex ddG

A fork of [flex_ddg_tutorial](https://github.com/Kortemme-Lab/flex_ddG_tutorial).

## Installation

1. `git clone https://github.com/jaeminoh/flex_ddG.git`
2. `uv sync`

## Example

- Run the protocol: `python flex_ddg/protocol.py --pdb_id=$pdb_id --rosetta_path=$rosetta_path --num_cpus=100`
- Analyze the output: `python flex_ddg/analysis.py analyze_results --pdb_id=$pdb_id`