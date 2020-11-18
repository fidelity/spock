# -*- coding: utf-8 -*-
from spock.backend.dataclass.args import IntArg, ListArg, IntOptArg, ChoiceArg, SavePathOptArg
from spock.config import spock
from spock.config import spock_config
from typing import List
from typing import Optional
from typing import Tuple
from enum import Enum
from spock.builder import ConfigArgBuilder
from spock.backend.attr.typed import SavePath


class Choice(Enum):
    pear = 'pear'
    banana = 'banana'


class Features(Enum):
    mfcc = 'mfcc'
    spectrogram = 'spectrogram'
    logfbank = 'logfbank'


class Window(Enum):
    hann = 'hann'
    hamming = 'hamming'



@spock
class LoaderConfig:
    batch_size: int
    drop_odd_batch: bool
    shuffle: bool
    n_workers: Optional[int] = 0
    distributed: bool


@spock
class ManifestConfig:
    manifest_path: str
    wav_name: str
    transcript_name: str
    duration_name: str
    sample_name: str
    bitrate_name: str
    min_duration: Optional[float]
    max_duration: Optional[float]
    sorted: bool


@spock
class TrainingManifestConfig(ManifestConfig):
    ...


@spock
class ValidationManifestConfig(ManifestConfig):
    ...


@spock
class TranscriptConfig:
    vocab: str


@spock
class AudioConfig:
    root_dir: str
    features: Features
    dither: Optional[float]
    trim_silence: bool
    normalize_signal: bool
    gain: Optional[float]
    per_feature_norm: bool
    window_ms: int
    stride_ms: int
    pre_emphasis: float
    n_fft: int
    window_fnc: Window
    speed_perturb: Optional[List[float]]
    n_features: Optional[int]


@spock
class TrainingAudioConfig(AudioConfig):
    ...


@spock
class ValidationAudioConfig(AudioConfig):
    ...


@spock
class Test:
    new_choice: Choice = 'banana'
    # fix_me: Tuple[Tuple[int]]
    new: int
    fail: bool
    # fail: List
    test: List[int]
    # fail: List[List[int]]
    # save_path: SavePath = '/tmp'
    # other: Optional[int]
    # value: Optional[List[int]] = [1, 2]

# @spock
# class Test2:
#     new_other: int
#
#
# @spock
# class Test3(Test2, Test):
#     ccccombo_breaker: int


def main():
    # test = Test()

    attrs_class = ConfigArgBuilder(TrainingManifestConfig, TranscriptConfig,
                                   TrainingAudioConfig, LoaderConfig,
                                   ValidationAudioConfig, ValidationManifestConfig
                                   ).generate()
    print(attrs_class)
    # dc_class = ConfigArgBuilder(OldInherit).generate()
    # print(dc_class)


if __name__ == '__main__':
    main()