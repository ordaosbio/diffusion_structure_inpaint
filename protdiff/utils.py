"""
Misc shared utility functions
"""
from typing import *

import torch


def extract(a, t, x_shape):
    """
    Return the t-th item in a for each item in t
    """
    batch_size = t.shape[0]
    out = a.gather(-1, t.cpu())
    return out.reshape(batch_size, *((1,) * (len(x_shape) - 1))).to(t.device)


def num_to_groups(num: int, divisor: int) -> List[int]:
    """
    Generates a list of ints of value at most divisor that sums to 
    
    >>> num_to_groups(18, 16)
    [16, 2]
    >>> num_to_groups(33, 8)
    [8, 8, 8, 8, 1]
    """
    groups = num // divisor
    remainder = num % divisor
    arr = [divisor] * groups
    if remainder > 0:
        arr.append(remainder)
    assert sum(arr) == num
    return arr


def broadcast_mod(x: torch.Tensor, m: Union[float, torch.Tensor]) -> torch.Tensor:
    """
    Perform modulo on x % m while broadcasting
    >>> broadcast_mod(torch.arange(24).reshape(2, 3, 4), torch.tensor([5, 7, 9, 11]))
    tensor([[[0, 1, 2, 3],
             [4, 5, 6, 7],
             [3, 2, 1, 0]],
    <BLANKLINE>
            [[2, 6, 5, 4],
             [1, 3, 0, 8],
             [0, 0, 4, 1]]])
    """
    if isinstance(m, float):
        return torch.remainder(x, m)
    # m is a tensor so we need to broadcast
    # https://pytorch.org/docs/stable/generated/torch.Tensor.expand.html#torch.Tensor.expand
    return torch.remainder(x, m.expand(*x.shape))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
