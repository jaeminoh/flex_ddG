
import os
import functools as ft
import subprocess
import multiprocessing as mp

from flex_ddg.config import Configuration


def run_saturation(
    config: Configuration,
    case_name: str,
    input_pdb_path: str,
    chains_to_move: str,
    mut_aa: str,
    nstruct_i: int,
):
    output_directory = os.path.join(
        f"{config.output_path}/{config.pdb_id}",
        os.path.join(f"{case_name}{mut_aa}", f"{nstruct_i:02d}"),
    )
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    chain, site_to_mutate, insertion_code = config.residue_to_mutate
    resfile_path = os.path.join(
        output_directory,
        f"mutate_{chain}{site_to_mutate}{insertion_code}_to_{mut_aa}.resfile",
    )
    with open(resfile_path, "w") as f:
        f.write(
            f"NATRO\nstart\n{site_to_mutate}{insertion_code} {chain} PIKAA {mut_aa}\n"
        )

    flex_ddg_args = [
        os.path.abspath(config.rosetta_scripts_path),
        f"-s {os.path.abspath(input_pdb_path)}",
        "-parser:protocol",
        os.path.abspath(config.rosetta_backrub_path),
        "-parser:script_vars",
        f"chainstomove={chains_to_move}",
        f"mutate_resfile_relpath={os.path.abspath(resfile_path)}",
        f"number_backrub_trials={config.number_backrub_trials}",
        f"max_minimization_iter={config.max_minimization_iter}",
        f"abs_score_convergence_thresh={config.abs_score_convergence_thresh:.1f}",
        f"backrub_trajectory_stride={config.backrub_trajectory_stride}",
        "-restore_talaris_behavior",
        "-in:file:fullatom",
        "-ignore_unrecognized_res",
        "-ignore_zero_occupancy false",
        "-ex1",
        "-ex2",
    ]

    log_path = os.path.join(output_directory, "rosetta.out")

    print("Running Rosetta with args:")
    print(" ".join(flex_ddg_args))
    print("Output logged to:", os.path.abspath(log_path))
    print()

    outfile = open(log_path, "w")
    process = subprocess.Popen(
        flex_ddg_args,
        stdout=outfile,
        stderr=subprocess.STDOUT,
        close_fds=True,
        cwd=output_directory,
    )
    _ = process.wait()
    outfile.close()


def run_protocol(pdb_id: str, rosetta_path: str, num_cpus: int = 100, use_multiprocessing: bool = True):
    config = Configuration(pdb_id, rosetta_path, max_cpus=num_cpus)

    if not os.path.isfile(config.rosetta_scripts_path):
        print(
            'ERROR: "rosetta_scripts_path" variable must be set to the location of the "rosetta_scripts" binary executable'
        )
        raise Exception("Rosetta missing")

    input_pdb_path = os.path.join("assets", f"{config.pdb_id}_relaxed.pdb")
    mutation_chain, mutation_resi, mutation_icode = config.residue_to_mutate
    cases = []

    for nstruct_i in range(1, config.nstruct + 1):
        for site in range(331, 531 + 1):
            mutation_resi = site
            for mut_aa in "ACDEFGHIKLMNPQRSTVWY":
                cases.append(
                    (
                        f"{mutation_chain}_{mutation_resi}{mutation_icode}",
                        input_pdb_path,
                        config.chains_to_move,
                        mut_aa,
                        nstruct_i,
                    )
                )

    if use_multiprocessing:
        pool = mp.Pool(processes=min((max_cpus := mp.cpu_count()), config.max_cpus))
        if config.max_cpus > max_cpus:
            print(
                f"WARNING: max_cpus ({config.max_cpus}) is greater than the number of available CPUs ({max_cpus}). Using {max_cpus} instead."
            )

    _run = ft.partial(run_saturation, config)
    for args in cases:
        if use_multiprocessing:
            pool.apply_async(_run, args=args)
        else:
            _run(*args)

    if use_multiprocessing:
        pool.close()
        pool.join()


if __name__ == "__main__":
    import fire

    fire.Fire(run_protocol)