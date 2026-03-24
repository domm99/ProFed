import torch
from torch.utils.data import Dataset, Subset

from ProFed.partitioner import partition_to_subregions


class DummyVisionDataset(Dataset):
    def __init__(self, labels_per_class: int = 12, num_classes: int = 6):
        self.classes = list(range(num_classes))
        self.targets = torch.tensor(
            [label for label in range(num_classes) for _ in range(labels_per_class)],
            dtype=torch.long,
        )

    def __len__(self) -> int:
        return len(self.targets)

    def __getitem__(self, idx: int):
        return torch.tensor([float(idx)]), self.targets[idx]


def _make_subsets():
    dataset = DummyVisionDataset()
    train_indices = list(range(48))
    validation_indices = list(range(48, len(dataset)))
    return dataset, Subset(dataset, train_indices), Subset(dataset, validation_indices)


def _assigned_indices(environment):
    return [index for region in environment.regions for index in region.training_data.indices]


def test_partition_methods_use_each_sample_exactly_once():
    _, training_data, validation_data = _make_subsets()

    for method in ("IID", "Hard", "Dirichlet"):
        environment = partition_to_subregions(
            training_data,
            validation_data,
            "MNIST",
            method,
            3,
            7,
            dirichlet_alpha=0.3,
            min_region_size=1,
        )
        assigned = _assigned_indices(environment)
        assert len(assigned) == len(training_data)
        assert len(set(assigned)) == len(training_data)
        assert set(assigned) == set(training_data.indices)


def test_hard_partition_keeps_disjoint_label_groups():
    dataset, training_data, validation_data = _make_subsets()
    environment = partition_to_subregions(training_data, validation_data, "MNIST", "Hard", 3, 11)

    region_labels = []
    for region in environment.regions:
        labels = {int(dataset.targets[index].item()) for index in region.training_data.indices}
        region_labels.append(labels)

    assert set.union(*region_labels) == set(dataset.classes)
    for left in range(len(region_labels)):
        for right in range(left + 1, len(region_labels)):
            assert region_labels[left].isdisjoint(region_labels[right])


def test_iid_partition_is_stratified_per_class():
    dataset, training_data, validation_data = _make_subsets()
    environment = partition_to_subregions(training_data, validation_data, "MNIST", "IID", 3, 19)

    class_counts_per_region = []
    for region in environment.regions:
        counts = torch.bincount(dataset.targets[region.training_data.indices], minlength=len(dataset.classes))
        class_counts_per_region.append(counts.tolist())

    for label in dataset.classes:
        counts = [region_counts[label] for region_counts in class_counts_per_region]
        assert max(counts) - min(counts) <= 1


def test_device_distribution_covers_region_without_overlap():
    _, training_data, validation_data = _make_subsets()
    environment = partition_to_subregions(training_data, validation_data, "MNIST", "IID", 3, 23)

    region = environment.regions[0]
    device_mapping = region.distribute_to_devices(4)
    assigned = [index for training_subset, _ in device_mapping.values() for index in training_subset.indices]

    assert len(assigned) == len(region.training_data)
    assert len(set(assigned)) == len(region.training_data)
    assert set(assigned) == set(region.training_data.indices)
