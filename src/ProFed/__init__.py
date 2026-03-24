"""A benchmark for proximity-based non-IID Federated Learning"""

__version__ = "0.0.1"

from ProFed.partitioner import (
    Environment,
    PartitionConfig,
    Region,
    download_dataset,
    partition_to_subregions,
    split_train_validation,
)

__all__ = [
    "Environment",
    "PartitionConfig",
    "Region",
    "download_dataset",
    "partition_to_subregions",
    "split_train_validation",
]
