from dataclasses import dataclass


@dataclass
class Configuration:
    """
    Important: The variables below are set to values that will make the run complete faster (as a tutorial example), but will not give scientifically valid results.
    Please change them to the "normal" default values before a real run.
    """
    pdb_id: str | None = None
    rosetta_path: str | None = None
    chains_to_move: str = "C"
    site_to_mutate: int = 331
    insertion_code: str = ""
    nstruct: int = 3  # Normally 35
    max_minimization_iter: int = 5  # Normally 5000
    abs_score_convergence_thresh: float = 200.0  # Normally 1.0
    number_backrub_trials: int = 10  # Normally 35000
    backrub_trajectory_stride: int = 5  # Can be whatever you want, if you would like to see results from earlier time points in the backrub trajectory. 7000 is a reasonable number, to give you three checkpoints for a 35000 step run, but you could also set it to 35000 for quickest run time (as the final minimization and packing steps will only need to be run one time).
    rosetta_backrub_path: str = "flex_ddg/backrub.xml"
    max_cpus: int = 8  # We might want to not run on the full number of cores, as Rosetta take about 2 Gb of memory per instance
    output_path: str = "outputs"
    rosetta_output_file_name: str = "rosetta.out"
    output_database_name: str = "ddG.db3"
    trajectory_stride: int = 5

    def __post_init__(self):
        self.rosetta_scripts_path = f"{self.rosetta_path}/bin/rosetta_scripts.static.linuxgccrelease"

    @property
    def residue_to_mutate(self):
        # Residue position to perform saturation mutagenesis. Format: (Chain, PDB residue number, insertion code).
        return (self.chains_to_move, self.site_to_mutate, self.insertion_code)