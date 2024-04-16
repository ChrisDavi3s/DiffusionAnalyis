from enum import Enum
from typing import Tuple, Union, Optional

class TimeUnit(Enum):
    '''
    Time unit enumeration for the mean squared displacement (MSD) analysis.
    TODO - this class should probably be made optional and the user should be able to specify the time unit in the plot_msd method.
    '''
    FEMTOSECONDS = 'fs'
    PICOSECONDS = 'ps'
    NANOSECONDS = 'ns'
    MICROSECONDS = 'us'
    MILLISECONDS = 'ms'
    SECONDS = 's'

    def get_time_as_seconds(self) -> float:
        """
        Get the time factor based on the time unit.

        Returns:
            float: The time factor to convert the timestep to the desired time unit.
        """
        if self == TimeUnit.FEMTOSECONDS:
            return 1e-15
        elif self == TimeUnit.PICOSECONDS:
            return 1e-12
        elif self == TimeUnit.NANOSECONDS:
            return 1e-9
        elif self == TimeUnit.MICROSECONDS:
            return 1e-6
        elif self == TimeUnit.MILLISECONDS:
            return 1e-3
        else:  # SECONDS
            return 1
        
    @staticmethod
    def adjust_timestep_and_unit(timestep: float, time_unit: Union[str, 'TimeUnit']) -> Tuple[float, 'TimeUnit']:
        """
        Adjust the timestep and time unit based on the magnitude of the timestep.

        Returns:
            Tuple[float, TimeUnit]: The adjusted timestep and time unit.
        """
        if isinstance(time_unit, str):
            time_unit = TimeUnit(time_unit)

        time_units = list(TimeUnit)
        current_index = time_units.index(time_unit)

        while timestep >= 1000 and current_index < len(time_units) - 1:
            timestep /= 1000
            current_index += 1
            time_unit = time_units[current_index]

        while timestep < 0.1 and current_index > 0:
            timestep *= 1000
            current_index -= 1
            time_unit = time_units[current_index]

        return timestep, time_unit

class TimeData:
    def __init__(self,
                 timestep: float = 1,
                 time_unit: Union[str, TimeUnit] = 'ps',
                 start_offset: Optional[float] = None,
                 structures_slice: Optional[Union[slice, int]] = None,
                 number_of_steps: Optional[int] = None
                 ):
        
        self.timestep = timestep
        self.time_unit = TimeUnit(time_unit) if isinstance(time_unit, str) else time_unit
        self.number_of_steps = number_of_steps

        if structures_slice is None:
            self.start_offset = 0 if start_offset is None else start_offset
        elif isinstance(structures_slice, slice):
            self.start_offset = structures_slice.start if structures_slice.start is not None else 0
            self.timestep *= structures_slice.step if structures_slice.step is not None else 1
            self.timestep, self.time_unit = TimeUnit.adjust_timestep_and_unit(self.timestep, self.time_unit)
            self.number_of_steps = structures_slice.stop - structures_slice.start if structures_slice.stop
        else:
            self.start_offset = structures_slice

    @property
    def time_unit_in_seconds(self) -> float:
        """
        Get the time factor based on the time unit.

        Returns:
            float: The time factor to convert the timestep to the desired time unit.
        """
        return self.time_unit.get_time_as_seconds()
    
    @property
    def start_time(self) -> float:
        return self.start_offset
    
    @property
    def end_time(self) -> float:
        if self.number_of_steps is None:
            raise ValueError("The number of steps is not defined.")
        return self.start_offset + self.number_of_steps * self.timestep
    
    
