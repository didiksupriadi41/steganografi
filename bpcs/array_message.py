from math import ceil
import numpy as np
from functools import reduce

from .logger import log
from .bpcs_steg import conjugate, arr_bpcs_complexity, max_bpcs_complexity, checkerboard

def get_conj_grid_prefix(dims, alpha):
    n = reduce(lambda x,y: x*y, dims, 1)
    checkered = checkerboard(*dims).reshape(-1).tolist()
    nprefix = int(ceil(alpha*n))
    prefix = checkered[:nprefix]
    assert len(prefix) == nprefix
    return prefix

def get_next_message_grid_sized(arr, dims, min_alpha=None):
    if arr.size == 0:
        raise Exception("cannot get a grid from empty array")
    n = reduce(lambda x,y: x*y, dims, 1)
    arr = arr.reshape(-1).tolist()
    if min_alpha:
        prefix = get_conj_grid_prefix(dims, min_alpha)
        assert len(prefix) < n
        arr = prefix + arr
    if len(arr) < n:
        arr += [0]*(len(arr) - n)
    cur_arr, arr = np.array(arr[:n]), np.array(arr[n:])
    cur_arr.resize(dims)
    if min_alpha:
        assert arr_bpcs_complexity(cur_arr) >= min_alpha, '{0} < {1}'.format(arr_bpcs_complexity(cur_arr), min_alpha)
    return cur_arr, arr

def list_to_grids(arr, dims):
    area = dims[0]*dims[1]
    rem = (len(arr) % area)
    length_missing = area - rem if rem else 0
    arr += [0]*length_missing
    arr = np.array(arr)
    ngrids = int(len(arr) / area)
    assert len(arr) % area == 0
    return np.resize(arr, [ngrids, dims[0], dims[1]])

def str_to_grids(message, grid_size):
    def bits(out):
        bytes = (ord(b) for b in out)
        for b in bytes:
            for i in reversed(range(8)):
                yield (b >> i) & 1
    bits_list = list(bits(message))
    # return bits_list
    return list_to_grids(bits_list, grid_size)

def read_message_grids(messagefile, grid_size):
    with open(messagefile, 'r') as f:
        return str_to_grids(f.read(), grid_size)

def grids_to_list(grids):
    grids = [np.array(grid).reshape(-1) for grid in grids]
    return np.hstack(grids).flatten().tolist()

def grids_to_str(grids):
    bits = grids_to_list(grids)
    nspare = len(bits) % 8
    # bits += [0]*nspare
    # since the message was initially read by the byte
    # any spares must have been added to create a grid
    bits = bits[:len(bits)-nspare]
    nbytes = int(len(bits) / 8)
    bytes = np.resize(np.array(bits), [nbytes, 8])
    byte_to_str = lambda byte: int('0b' + ''.join(str(x) for x in byte.tolist()), 2)
    byte_to_char = lambda byte: chr(byte_to_str(byte))
    return ''.join([byte_to_char(byte) for byte in bytes])

def write_message_grids(outfile, grids):
    with open(outfile, 'w') as f:
        f.write(grids_to_str(grids))

def get_message_grid_from_grids(mgrids, conj_map):
    assert len(conj_map) >= len(mgrids), '{0} < {1}'.format(len(conj_map), len(mgrids))
    for i, mgrid in enumerate(mgrids):
        if conj_map[i]:
            mgrids[i] = conjugate(mgrid)
    return mgrids

def get_n_message_grids(nbits_per_map, ngrids):
    x, y = ngrids-1, 1
    is_valid = lambda x, y, ngrids, nbits_per_map: ngrids==x+y and sum(nbits_per_map[-(y-1):]) < x <= sum(nbits_per_map[-y:])
    while not is_valid(x, y, ngrids, nbits_per_map) and x > 0:
        x, y = x-1, y+1
    if x <= 0 and ngrids == 2:
        # edge case
        return 1
    assert x > 0
    assert y > 0
    return x

def separate_conj_map_from_message(grids, alpha):
    if not grids:
        log.critical('No message grids found')
        return [], [], []

    get_nignored = lambda grid: len(get_conj_grid_prefix((grid.shape[0], grid.shape[1]), alpha))
    get_nbits_per_map = lambda grid: grid.shape[0]*grid.shape[1] - get_nignored(grid)
    nbits_per_map = [get_nbits_per_map(grid) for grid in grids]

    ngrids = len(grids)
    x = get_n_message_grids(nbits_per_map, ngrids)
    log.critical('Found {0} message grids and {1} conjugation maps'.format(x, ngrids-x))
    return grids[:x], grids[x:], nbits_per_map[x:]

def get_conj_map(cgrids, nbits_per_map):
    cgrids = [grid.reshape(-1).tolist()[-nbits_per_map[i]:] for i, grid in enumerate(cgrids)]
    conj_map = np.hstack(cgrids).reshape(-1).tolist()
    assert len(conj_map) == sum(nbits_per_map), '{0} != {1}'.format(len(conj_map), sum(nbits_per_map))
    return conj_map

def write_conjugated_message_grids(outfile, grids, alpha):
    messages, conj_map_grids, nbits_per_map = separate_conj_map_from_message(grids, alpha)
    if len(conj_map_grids) == 0:
        return
    conj_map = get_conj_map(conj_map_grids, nbits_per_map)
    message_grids = get_message_grid_from_grids(messages, conj_map)
    write_message_grids(outfile, message_grids)
