# =============================================================================
# Copyright (C) 2025 Commissariat a l'energie atomique et aux energies alternatives (CEA)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the names of CEA, nor the names of the contributors may be used to
#   endorse or promote products derived from this software without specific
#   prior written  permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# =============================================================================
from typing import Protocol, Iterable, Any

import dask.array as da
import numpy as np


class SlidingWindowInterface(Protocol):
    class SlidingWindowCallbackInterface(Protocol):
        def __call__(self, *darrs: list[da.Array], timestep: int) -> None: ...

    class ExceptionHandlerInterface(Protocol):
        def __call__(self, array_name: str, exception: BaseException) -> None: ...

    # TODO: register_sliding_window_callback with only 1 array_name
    # @overload
    # def register_sliding_window_callback(self, callback: SlidingWindowCallbackInterface,
    #                                      array_name: str, window_size: int,
    #                                      exception_handler: ExceptionHandlerInterface) -> None: ...
    #
    # @overload
    def register_sliding_window_callback(self, callback: SlidingWindowCallbackInterface,
                                         array_names: Iterable[tuple[str, int]],  # [(array_name, windows_size), (...)]
                                         exception_handler: ExceptionHandlerInterface) -> None: ...

    def unregister_sliding_window_callback(self, array_name: str) -> None: ...


class GetArrayInterface(Protocol):
    def get_array(self, array_name: str, timeout=None) -> tuple[da.Array, int]: ...


class FrameworkClientInterface(Protocol):
    def connect(self, address: str, *args, **kwargs) -> Any: ...

    def disconnect(self) -> None: ...

    def publish_data(self, data: Any, *args, **kwargs) -> None: ...


class DeisaInterface(SlidingWindowInterface, GetArrayInterface, Protocol):

    def __init__(self, address: str | FrameworkClientInterface, *args, **kwargs): ...

    def close(self) -> None: ...


class BridgeInterface(Protocol):
    def __init__(self, address: str | FrameworkClientInterface, *args, **kwargs):
        pass

    def publish_data(self, array_name: str, data: np.ndarray, timestep: int) -> None:
        pass
