import os
import types
from pathlib import Path
from typing import Optional
from copy import deepcopy
from itertools import chain

import numpy as np
import pickle5 as pickle
from hydra.utils import get_original_cwd
import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from src.utils.data import dataset_info, data_keys


class DataModule(pl.LightningDataModule):

    def __init__(self,
                 dataset: str, data_path: str, mode: str,
                 train_batch_size: int = 1, eval_batch_size: int = 1, eff_train_batch_size: int = 1, num_workers: int = 0,
                 num_train: int = None, num_dev: int = None, num_test: int = None,
                 num_train_seed: int = None, num_dev_seed: int = None, num_test_seed: int = None,
                 pct_train_rationales: float = None, pct_train_rationales_seed: int = None, train_rationales_batch_factor: float = None,
                 attr_algo: str = None, train_shuffle: bool = False, train_rationale_selection: str = None,
                 ):
        super().__init__()

        self.dataset = dataset
        self.data_path = data_path # ${data_dir}/${.dataset}/${model.arch}/

        self.train_batch_size = train_batch_size
        self.eval_batch_size = eval_batch_size
        self.eff_train_batch_size = eff_train_batch_size
        self.num_workers = num_workers

        self.num_samples = {'train': num_train, 'dev': num_dev, 'test': num_test}
        self.num_samples_seed = {'train': num_train_seed, 'dev': num_dev_seed, 'test': num_test_seed}
        self.pct_train_rationales = pct_train_rationales
        self.pct_train_rationales_seed = pct_train_rationales_seed
        self.train_rationales_batch_factor = train_rationales_batch_factor

        self.attr_algo = attr_algo
        self.train_shuffle = train_shuffle
        self.train_rationale_selection = train_rationale_selection

    def load_dataset(self, split):
        dataset = {}
        data_path = os.path.join(self.data_path, split)
        assert Path(data_path).exists()
        
        for key in tqdm(data_keys, desc=f'Loading {split} set'):
            if key == 'rationale_indices' and split == 'train' and self.pct_train_rationales is not None:
                filename = f'{key}_{self.train_rationale_selection}_{self.pct_train_rationales}_{self.pct_train_rationales_seed}.pkl'
            elif self.num_samples[split] is not None:
                filename = f'{key}_{self.num_samples[split]}_{self.num_samples_seed[split]}.pkl'
            else:
                filename = f'{key}.pkl'

            with open(os.path.join(data_path, filename), 'rb') as f:
                cur_data = pickle.load(f)
                if not any([x is None for x in cur_data]):
                    dataset[key] = cur_data

        if split == 'train' and self.pct_train_rationales is not None:
            dataset_ = deepcopy(dataset)
            dataset_keys = dataset_.keys()
            rationale_indices = dataset_['rationale_indices']
            dataset, train_rationales_dataset = {}, {}
            for key in dataset_keys:
                if key != 'rationale_indices':
                    dataset[key] = [x for i, x in enumerate(dataset_[key]) if i not in rationale_indices]
                    train_rationales_dataset[key] = [x for i, x in enumerate(dataset_[key]) if i in rationale_indices]
            assert sorted(rationale_indices) == train_rationales_dataset['item_idx']
        else:
            train_rationales_dataset = None

        return dataset, train_rationales_dataset

    def setup(self, splits=['all']):
        self.data = {}
        splits = ['train', 'dev', 'test'] if splits == ['all'] else splits
        for split in splits:
            dataset, train_rationales_dataset = self.load_dataset(split)
            self.data[split] = TextClassificationDataset(dataset, split, train_rationales_dataset, self.train_batch_size)

    def train_dataloader(self):
        if self.pct_train_rationales is not None:
            assert self.train_batch_size >= 2
            assert self.train_rationales_batch_factor > 1
            batch_size = self.train_batch_size - int(max(1, self.train_batch_size / self.train_rationales_batch_factor))
        else:
            batch_size = self.train_batch_size

        return DataLoader(
            self.data['train'],
            batch_size=batch_size,
            num_workers=self.num_workers,
            collate_fn=self.data['train'].collater,
            shuffle=self.train_shuffle,
            pin_memory=True
        )

    def val_dataloader(self, test=False):
        if test:
            return DataLoader(
                self.data['dev'],
                batch_size=self.eval_batch_size,
                num_workers=self.num_workers,
                collate_fn=self.data['dev'].collater,
                pin_memory=True
            )

        return [
            DataLoader(
            self.data[eval_split],
            batch_size=self.eval_batch_size,
            num_workers=self.num_workers,
            collate_fn=self.data[eval_split].collater,
            pin_memory=True)
            
            for eval_split in ['dev', 'test']
        ]

    def test_dataloader(self):
        return DataLoader(
            self.data['test'],
            batch_size=self.eval_batch_size,
            num_workers=self.num_workers,
            collate_fn=self.data['test'].collater,
            pin_memory=True
        )


class TextClassificationDataset(Dataset):
    def __init__(self, dataset, split, train_rationales_dataset=None, train_batch_size=None):
        self.data = dataset
        self.split = split
        self.train_rationales_dataset = train_rationales_dataset
        self.train_batch_size = train_batch_size
        assert not (split != 'train' and train_rationales_dataset is not None)
        if train_rationales_dataset is not None:
            self.len_train_rationales_dataset = len(train_rationales_dataset['item_idx'])

    def __len__(self):
        return len(self.data['item_idx'])

    def __getitem__(self, idx):
        item_idx = torch.LongTensor([self.data['item_idx'][idx]])
        input_ids = torch.LongTensor(self.data['input_ids'][idx])
        attention_mask = torch.LongTensor(self.data['attention_mask'][idx])
        rationale = torch.FloatTensor(self.data['rationale'][idx]) if self.data.get('rationale') else None
        has_rationale = torch.LongTensor([self.data['has_rationale'][idx]])
        if self.train_rationales_dataset is not None:
            has_rationale *= 0
        label = torch.LongTensor([self.data['label'][idx]])

        return (
            item_idx, input_ids, attention_mask, rationale, has_rationale, label
        )

    def sample_train_rationale_indices(self, num_samples):
        return list(np.random.choice(self.len_train_rationales_dataset, size=num_samples, replace=False))

    def get_train_rationale_item(self, idx):
        item_idx = torch.LongTensor([self.train_rationales_dataset['item_idx'][idx]])
        input_ids = torch.LongTensor(self.train_rationales_dataset['input_ids'][idx])
        attention_mask = torch.LongTensor(self.train_rationales_dataset['attention_mask'][idx])
        rationale = torch.FloatTensor(self.train_rationales_dataset['rationale'][idx])
        has_rationale = torch.LongTensor([self.train_rationales_dataset['has_rationale'][idx]])
        label = torch.LongTensor([self.train_rationales_dataset['label'][idx]])

        return (
            item_idx, input_ids, attention_mask, rationale, has_rationale, label
        )

    def collater(self, items):
        batch_size = len(items)
        if self.train_rationales_dataset is not None:
            num_train_rationale_indices = int(max(1, self.train_batch_size - batch_size))
            train_rationale_indices = self.sample_train_rationale_indices(num_train_rationale_indices)
            for idx in train_rationale_indices:
                items.append(self.get_train_rationale_item(idx))
        batch = {
            'item_idx': torch.cat([x[0] for x in items]),
            'input_ids': torch.stack([x[1] for x in items], dim=0),
            'attention_mask': torch.stack([x[2] for x in items], dim=0),
            'rationale': torch.stack([x[3] for x in items], dim=0) if self.data.get('rationale') else None,
            'has_rationale': torch.cat([x[4] for x in items]),
            'label': torch.cat([x[5] for x in items]),
            'split': self.split, # when evaluate_ckpt=true, split always test
        }
        
        return batch