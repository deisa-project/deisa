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
from typing import Protocol, Any, Callable, overload, List, Union, Tuple

import dask.array as da
import numpy as np
from distributed import Future, Client


class SlidingWindowInterface(Protocol):
    Callback_args = Union[str, Tuple[str], Tuple[str, int]]  # array_name, (array_name, ...), (array_name, window_size)

    class SlidingWindowCallbackInterface(Protocol):
        def __call__(self, *window: List[da.Array], timestep: int) -> None: ...

    class ExceptionHandlerInterface(Protocol):
        def __call__(self, array_name: str, exception: BaseException) -> None: ...

    @overload
    def register_sliding_window_callback(self, callback: SlidingWindowCallbackInterface,
                                         array_name: str, *, window_size: int = 1,
                                         exception_handler: ExceptionHandlerInterface) -> None: ...

    @overload
    def register_sliding_window_callback(self, callback: SlidingWindowCallbackInterface,
                                         *callback_args: Callback_args,
                                         exception_handler: ExceptionHandlerInterface,
                                         when='AND') -> None: ...

    def register_sliding_window_callback(self, callback: SlidingWindowCallbackInterface,
                                         *callback_args: Callback_args,
                                         window_size: int = 1,
                                         exception_handler: ExceptionHandlerInterface,
                                         when: str = 'AND') -> str: ...

    def unregister_sliding_window_callback(self, *array_names: Callback_args) -> None: ...


class GetArrayInterface(Protocol):
    def get_array(self, array_name: str, timeout=None) -> tuple[da.Array, int]: ...


class DeisaInterface(SlidingWindowInterface, GetArrayInterface, Protocol):

    def __init__(self, get_connection_info: Callable[[], Client], *args, **kwargs): ...

    def set(self, name: str, data: Union[Future, object], chunked=False) -> None: ...

    def delete(self, key: str) -> None: ...

    def close(self) -> None: ...


class BridgeInterface(Protocol):
    def __init__(self, id: int, arrays_metadata: dict[str, dict], system_metadata: dict[str, Any], *args, **kwargs): ...

    def send(self, array_name: str, data: np.ndarray, timestep: int, chunked: bool) -> None: ...

    def get(self, key: str, default: Any, chunked: bool, delete: bool) -> Any: ...
