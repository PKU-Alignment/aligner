# Copyright 2023-2024 PKU-Alignment Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import annotations
import json
# from datasets import load_dataset

from training.datasets.base import RawSample
from training.datasets.base import RawDataset
CORRECTION_INSTRUCTION='##Question: {question}\n##Answer: {answer}\n##Correction: '

__all__ = [
    'CorrectionJSONDataset',
    'BeavertailsJSONDataset',
    'BeavertailsTestJSONDataset',
    'BeavertailsTrainJSONDataset',
]

class CorrectionJSONDataset(RawDataset):
    NAME: str = 'correction-json'

    def __init__(self, path) -> None:  # noqa: ANN001
        self.path = path
        with open(self.path, encoding='utf-8') as f:
            self.data = json.load(f)

    def __getitem__(self, index: int) -> RawSample:
        data = self.data[index]
        input = CORRECTION_INSTRUCTION.format(question=data['question'], answer=data['answer'])
        answer = data['correction']
        return RawSample(input=input, answer=answer)

    def __len__(self) -> int:
        return len(self.data)


class BeavertailsJSONDataset(RawDataset):
    def __init__(self, path) -> None:  # noqa: ANN001
        self.path = path
        with open(self.path, encoding='utf-8') as f:
            self.data = json.load(f)

    def __getitem__(self, index: int) -> RawSample:
        data = self.data[index]
        return RawSample(
            input=(' '.join((data['prompt'], data['response']))),
            answer=data['response'],
        )

    def __len__(self) -> int:
        return len(self.data)


class BeavertailsTestJSONDataset(BeavertailsJSONDataset):
    NAME: str = 'beavertails-json/test'


class BeavertailsTrainJSONDataset(BeavertailsJSONDataset):
    NAME: str = 'beavertails-json/train'
