from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Iterable

import numpy as np
import torch
from datasets import load_dataset
from torch.utils.data import Dataset, Subset, random_split
from torchvision import datasets, transforms

from ProFed.UTKFaceDataset import UTKFaceHFDataset

__all__ = [
    "PartitionConfig",
    "Region",
    "Environment",
    "download_dataset",
    "split_train_validation",
    "partition_to_subregions",
]


@dataclass(frozen=True)
class PartitionConfig:
    partitioning_method: str
    number_of_regions: int
    seed: int = 0
    dirichlet_alpha: float = 0.5
    min_region_size: int = 10

    def normalized_method(self) -> str:
        return self.partitioning_method.strip().lower()

    def validate(self) -> None:
        if self.number_of_regions <= 0:
            raise ValueError("number_of_regions must be greater than 0")
        if self.dirichlet_alpha <= 0:
            raise ValueError("dirichlet_alpha must be greater than 0")
        if self.min_region_size < 0:
            raise ValueError("min_region_size must be non-negative")


@dataclass
class Region:
    mid: int
    training_data: Subset
    validation_data: Subset
    seed: int

    def distribute_to_devices(self, number_of_devices: int) -> dict[int, tuple[Subset, Subset]]:
        if number_of_devices <= 0:
            raise ValueError("number_of_devices must be greater than 0")

        training_dataset, training_indices = self.training_data.dataset, np.array(self.training_data.indices, dtype=int)
        validation_dataset, validation_indices = self.validation_data.dataset, np.array(self.validation_data.indices, dtype=int)
        rng = np.random.default_rng(self.seed)
        rng.shuffle(training_indices)
        rng.shuffle(validation_indices)

        device_to_subset = {}
        training_split = np.array_split(training_indices, number_of_devices)
        validation_split = np.array_split(validation_indices, number_of_devices)
        for index, (training, validation) in enumerate(zip(training_split, validation_split)):
            device_to_subset[index] = (
                Subset(training_dataset, training.tolist()),
                Subset(validation_dataset, validation.tolist()),
            )
        return device_to_subset


class Environment:
    def __init__(self, partitions: dict[int, tuple[Subset, Subset]], seed: int):
        self.seed = seed
        self.regions = [
            Region(region_id, training_data, validation_data, seed + region_id)
            for region_id, (training_data, validation_data) in sorted(partitions.items())
        ]

    def from_subregion_to_devices(self, region_id: int, number_of_devices: int) -> dict[int, tuple[Subset, Subset]]:
        return self.regions[region_id].distribute_to_devices(number_of_devices)


def download_dataset(
    dataset_name: str,
    transform: transforms.Compose | None = None,
    download_path: str = "dataset",
) -> tuple[Dataset, Dataset]:
    """
    Download the specified dataset from torchvision.
    Valid datasets are: MNIST, FashionMNIST, EMNIST, CIFAR10, CIFAR100 and UTKFace.
    """
    if transform is None:
        transform = transforms.Compose([transforms.ToTensor()])

    if dataset_name == "MNIST":
        train_dataset = datasets.MNIST(root=download_path, train=True, download=True, transform=transform)
        test_dataset = datasets.MNIST(root=download_path, train=False, download=True, transform=transform)
    elif dataset_name == "CIFAR10":
        train_dataset = datasets.CIFAR10(root=download_path, train=True, download=True, transform=transform)
        test_dataset = datasets.CIFAR10(root=download_path, train=False, download=True, transform=transform)
    elif dataset_name == "CIFAR100":
        train_dataset = datasets.CIFAR100(root=download_path, train=True, download=True, transform=transform)
        test_dataset = datasets.CIFAR100(root=download_path, train=False, download=True, transform=transform)
    elif dataset_name == "EMNIST":
        train_dataset = datasets.EMNIST(root=download_path, split="letters", train=True, download=True, transform=transform)
        test_dataset = datasets.EMNIST(root=download_path, split="letters", train=False, download=True, transform=transform)
    elif dataset_name == "FashionMNIST":
        train_dataset = datasets.FashionMNIST(root=download_path, train=True, download=True, transform=transform)
        test_dataset = datasets.FashionMNIST(root=download_path, train=False, download=True, transform=transform)
    elif dataset_name == "UTKFace":
        ds = load_dataset("py97/UTKFace-Cropped", split="train")
        dataset = UTKFaceHFDataset(ds, transform=transform)
        train_dataset, test_dataset = split_train_validation(dataset, 0.85)
    else:
        raise ValueError(f"Dataset {dataset_name} not supported")
    return train_dataset, test_dataset


def split_train_validation(dataset: Dataset, train_validation_ratio: float) -> tuple[Subset, Subset]:
    """
    Split a dataset into training and validation subsets.
    """
    if not 0 < train_validation_ratio < 1:
        raise ValueError("train_validation_ratio must be between 0 and 1")

    dataset_size = len(dataset)
    training_size = int(dataset_size * train_validation_ratio)
    validation_size = dataset_size - training_size
    training_data, validation_data = random_split(dataset, [training_size, validation_size])
    return training_data, validation_data


def partition_to_subregions(
    training_dataset: Subset,
    validation_dataset: Subset,
    dataset_name: str,
    partitioning_method: str,
    number_of_regions: int,
    seed: int,
    dirichlet_alpha: float = 0.5,
    min_region_size: int = 10,
) -> Environment:
    """
    Partition train and validation subsets into regions.

    The API keeps backwards compatibility with the original signature while exposing
    Dirichlet-specific controls through keyword arguments.
    """
    config = PartitionConfig(
        partitioning_method=partitioning_method,
        number_of_regions=number_of_regions,
        seed=seed,
        dirichlet_alpha=dirichlet_alpha,
        min_region_size=min_region_size,
    )
    config.validate()

    training_partitions = _partition_subset(training_dataset, dataset_name, config)
    validation_partitions = _partition_subset(validation_dataset, dataset_name, config)

    partitions = {
        region_id: (
            Subset(training_dataset.dataset, training_partitions[region_id]),
            Subset(validation_dataset.dataset, validation_partitions[region_id]),
        )
        for region_id in range(config.number_of_regions)
    }
    return Environment(partitions, config.seed)


def _partition_subset(data: Subset, dataset_name: str, config: PartitionConfig) -> dict[int, list[int]]:
    method = config.normalized_method()
    if method == "dirichlet":
        if dataset_name == "UTKFace":
            raise ValueError("Dirichlet partitioning is not implemented for UTKFace")
        return _partition_dirichlet(data, config.number_of_regions, config.seed, config.dirichlet_alpha, config.min_region_size)
    if method == "hard":
        if dataset_name == "UTKFace":
            return __partition_regression(data, config.number_of_regions)
        return _partition_hard(data, config.number_of_regions, config.seed)
    if method == "iid":
        if dataset_name == "UTKFace":
            raise ValueError("IID partitioning is not implemented for UTKFace")
        return _partition_iid(data, config.number_of_regions, config.seed)
    raise ValueError(f"Partitioning method {config.partitioning_method} not supported")


def _partition_hard(data: Subset, areas: int, seed: int) -> dict[int, list[int]]:
    labels = _label_count(data)
    label_groups = np.array_split(np.arange(labels), areas)
    class_to_indices = _group_indices_by_class(data, seed)
    partitions = {area: [] for area in range(areas)}
    for area, group in enumerate(label_groups):
        for label in group:
            partitions[area].extend(class_to_indices.get(int(label), []))
    return _shuffle_partitions(partitions, seed)


def _partition_iid(data: Subset, areas: int, seed: int) -> dict[int, list[int]]:
    class_to_indices = _group_indices_by_class(data, seed)
    partitions = {area: [] for area in range(areas)}
    for label_indices in class_to_indices.values():
        splits = np.array_split(np.array(label_indices, dtype=int), areas)
        for area, split in enumerate(splits):
            partitions[area].extend(split.tolist())
    return _shuffle_partitions(partitions, seed)


def _partition_dirichlet(
    data: Subset,
    areas: int,
    seed: int,
    alpha: float,
    min_region_size: int,
) -> dict[int, list[int]]:
    # Implemented following https://proceedings.mlr.press/v97/yurochkin19a.html
    rng = np.random.default_rng(seed)
    indices = list(data.indices)
    total_instances = len(indices)
    class_to_indices = _group_indices_by_class(data, seed)
    partitions = {area: [] for area in range(areas)}

    if not indices:
        return partitions

    min_size = -1
    while min_size < min_region_size:
        idx_batch = [[] for _ in range(areas)]
        for label in sorted(class_to_indices.keys()):
            idx_k = np.array(class_to_indices[label], dtype=int)
            rng.shuffle(idx_k)
            proportions = rng.dirichlet(np.repeat(alpha, areas))
            balance_mask = np.array([len(idx_j) < total_instances / areas for idx_j in idx_batch], dtype=float)
            proportions = proportions * balance_mask
            if proportions.sum() == 0:
                proportions = np.repeat(1 / areas, areas)
            else:
                proportions = proportions / proportions.sum()
            split_points = (np.cumsum(proportions) * len(idx_k)).astype(int)[:-1]
            for area, split in enumerate(np.split(idx_k, split_points)):
                idx_batch[area].extend(split.tolist())
        min_size = min(len(idx_j) for idx_j in idx_batch)

    for area in range(areas):
        rng.shuffle(idx_batch[area])
        partitions[area] = idx_batch[area]
    return partitions


def _targets_tensor(dataset: Dataset) -> torch.Tensor:
    if not hasattr(dataset, "targets"):
        raise ValueError("The provided dataset does not expose a 'targets' attribute")
    targets = dataset.targets
    if isinstance(targets, torch.Tensor):
        return targets
    return torch.tensor(targets)


def _group_indices_by_class(data: Subset, seed: int) -> dict[int, list[int]]:
    targets = _targets_tensor(data.dataset)
    rng = np.random.default_rng(seed)
    class_to_indices: dict[int, list[int]] = defaultdict(list)
    for index in data.indices:
        class_to_indices[int(targets[index].item())].append(int(index))
    for label_indices in class_to_indices.values():
        rng.shuffle(label_indices)
    return dict(class_to_indices)


def _label_count(data: Subset) -> int:
    dataset = data.dataset
    if hasattr(dataset, "classes"):
        return len(dataset.classes)
    targets = _targets_tensor(dataset)
    return int(targets.max().item()) + 1


def _shuffle_partitions(partitions: dict[int, list[int]], seed: int) -> dict[int, list[int]]:
    rng = np.random.default_rng(seed)
    for indices in partitions.values():
        rng.shuffle(indices)
    return partitions


def find_bounds(data: Iterable[tuple[torch.Tensor, torch.Tensor]]) -> tuple[float, float]:
    ys = []
    for _, y in data:
        ys.append(y.item())
    return min(ys), max(ys)


def __partition_regression(data: Subset, areas: int) -> dict[int, list[int]]:
    lower_bound, upper_bound = find_bounds(data)
    bins = np.linspace(lower_bound, upper_bound, areas + 1)
    ys = []
    indices = []
    for idx in range(len(data)):
        _, y = data[idx]
        ys.append(y.item())
        indices.append(data.indices[idx])
    ys = np.array(ys)
    bin_indices = np.digitize(ys, bins, right=True)
    bin_indices = np.clip(bin_indices, 1, len(bins) - 1)
    mapping: dict[int, list[int]] = defaultdict(list)
    for idx, bin_id in enumerate(bin_indices):
        mapping[int(bin_id) - 1].append(indices[idx])
    return {area: mapping.get(area, []) for area in range(areas)}
