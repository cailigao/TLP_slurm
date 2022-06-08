## TLP_slurm

**Multi-node task-level parallelism using [`Slurm`](https://github.com/SchedMD/slurm). Suitable for programs where data can be split.**

The task is divided into two steps: data split, main program processing.

**Data split**: Split the data to be processed into several small data pieces.

**Main program**: Execute the main program to process the small data.

## Dependencies

python>=3.6

simple_slurm=0.2.3

## Usage

#### 1. prepare

Write command line parameters in the JSON file in the following format ([example_args.json](example/example_args.json)). The configuration file consists of two parts: data split program parameter configuration (`split`) and main program parameter configuration (`main`).

[example_args.json](example/example_args.json)：

```json
{
  "split": {
    "bin": "example/split.py",
    "type": "python",
    "input": {
      "my_input": "-i",
      "value": "example/test.fastq"
    },
    "output": {
      "my_output": "-o",
      "value": "example/output"
    },
    "my_args": "-threads 4 -mode fast"
  },
  "main": {
    "bin": "example/main.py",
    "type": "python",
    "input": {
      "my_input": "-i"
    },
    "output": {
      "my_output": "-o",
      "value": "example/result"
    },
    "threads": {
      "my_threads": "-t",
      "value": 8
    },
    "my_args": "-useSlurm=True -d ./test"
  }
}
```

| key                    | value                                                   |
| ---------------------- | ------------------------------------------------------- |
| bin                    | path to execute the program                             |
| type                   | program type: python/C/java                             |
| input.my_input         | input of your program                                   |
| input.value            | input path, **The main program does not need to set**   |
| output.my_output       | output of your program                                  |
| output.value           | output path                                             |
| threads.my_threads     | threads of your program                                 |
| threads.value          | number of threads                                       |
| my_args **[optional]** | all the other parameters of the program can be put here |

#### 2. start

After setting the values in the parameter JSON file, pass the parameter JSON file with the following command and start executing the program.

```shell
python start.py example_args.json
```

## Example

example is a program that split and print fastq data, including a split program ([split.py](example/split.py)), a main program ([main.py](example/main.py)), test data ([test.fastq](example/test.fastq)), and a parameter JSON file ([args.json](example/args.json)). [args.json](example/args.json) contents are as follows:

```json
{
  "split": {
    "bin": "example/split.py",
    "type": "python",
    "input": {
      "my_input": "-i",
      "value": "example/test.fastq"
    },
    "output": {
      "my_output": "-o",
      "value": "example/output"
    }
  },
  "main": {
    "bin": "example/main.py",
    "type": "python",
    "input": {
      "my_input": "-i"
    },
    "output": {
      "my_output": "-o",
      "value": "example/result"
    }
  }
}
```

Then execute the following command:

```shell
python start.py example/args.json
```

You can see the output in the example/output directory.