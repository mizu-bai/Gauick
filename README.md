# Gauick

External Script for Invoking QUICK from Gaussian

## Prerequests

- [Gaussian](https://gaussian.com)
- [QUICK](https://github.com/merzlab/QUICK)
- Python3

## Usage

- `gauick.py`
- `gauick.json`

These two files should be put under the same directory where Gaussian input file exists. In json file `gauick.json`, QUICK executable and calculation job must be specified and here is an example.

```json
{
    "exec": "mpirun -np 1 quick.cuda.MPI",
    "job": "DFT B3LYP GD3BJ BASIS=6-31G*"
}
```

The Gaussian input file for optimization and frequencies tasks should look like

```
%nproc=1
%chk=water.chk
#p external="python3 -u gauick.py" opt=nomicro

water

0 1
 O                 -0.06756756   -0.31531531    0.00000000
 H                  0.89243244   -0.31531531    0.00000000
 H                 -0.38802215    0.58962052    0.00000000


--link1--
%nproc=1
%chk=water.chk
#p external="python3 -u gauick.py" freq=num geom=allcheck


```

