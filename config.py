from typing import Dict
from pydantic import BaseModel

class XAxisConfig(BaseModel):
    label: str
    interval: int

class YAxisConfig(BaseModel):
    label: str | None
    range_min: float = 0
    range_max: float = 1
    interval: float = 0.2

class AxesConfig(BaseModel):
    x: XAxisConfig
    y: YAxisConfig

class LabelsConfig(BaseModel):
    font_size: int
    gap: float

class VideoConfig(BaseModel):
    duration_seconds: float

class DataConfig(BaseModel):
    delimiter: str

class Config(BaseModel):
    data: DataConfig
    axes: AxesConfig
    data_sets: Dict[str, str]
    labels: LabelsConfig
    video: VideoConfig

