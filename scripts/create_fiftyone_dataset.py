"""Visualize predictions of models in a fiftyone dashboard."""

import hydra
from omegaconf import DictConfig
from lightning_pose.utils.fiftyone import (
    FiftyOneImagePlotter,
    FiftyOneKeypointVideoPlotter,
    check_dataset,
    FiftyOneFactory,
)
import fiftyone as fo

from lightning_pose.utils import pretty_print_str


@hydra.main(config_path="configs", config_name="config_toy-dataset")
def build_fo_dataset(cfg: DictConfig) -> None:
    pretty_print_str(
        "Launching a job that creates %s FiftyOne.Dataset"
        % cfg.eval.fiftyone.dataset_to_create
    )
    FiftyOneClass = FiftyOneFactory(
        dataset_to_create=cfg.eval.fiftyone.dataset_to_create
    )()
    fo_plotting_instance = FiftyOneClass(cfg=cfg)  # initializes everything
    dataset = fo_plotting_instance.create_dataset()  # internally loops over models
    check_dataset(dataset)  # create metadata and print if there are problems
    fo_plotting_instance.dataset_info_print()  # print the name of the dataset

    if cfg.eval.fiftyone.launch_app_from_script:
        # launch an interactive session
        session = fo.launch_app(
            dataset,
            remote=cfg.eval.fiftyone.remote,
            address=cfg.eval.fiftyone.address,
            port=cfg.eval.fiftyone.port,
        )
        session.wait()
    # otherwise launch from an ipython session


if __name__ == "__main__":
    build_fo_dataset()
