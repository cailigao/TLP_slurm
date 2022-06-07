## TLP_slurm

Multi-node task-level parallelism using `Slurm`. Suitable for programs where data can be split.

The task is divided into two steps: data split, main program processing.

Data split: Split the data to be processed into several small data pieces.

Main program: Execute the main program to process the small data.

## Dependencies

python>=3.6

simple_slurm=0.2.3

## Usage

#### 1. prepare

在json文件中按照如下格式（example_args.json）编写命令行参数，配置文件包含数据分割程序参数配置(split)和主程序参数配置（main）两个部分。

example_args.json如下：

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

| key                | value                                      |
| ------------------ | ------------------------------------------ |
| bin                | 执行程序的位置                             |
| type               | 执行程序类型：python、c、java              |
| input.my_input     | 你程序的输入形参                           |
| input.value        | 你程序的输入实参，**注意主程序不需要设置** |
| output.my_output   | 你程序的输出形参                           |
| output.value       | 你程序的输出实参                           |
| threads.my_threads | 你程序的线程形参                           |
| threads.value      | 你程序的线程实参                           |
| my_args            | 程序的其他参数都可以放到这里               |

#### 2.执行程序

设置好参数json文件中的值后，通过一下命令开始执行程序

```shell
# 指定参数json文件位置
python start.py example_args.json
```

## Example

example是一个分割fastq数据并打印的程序，包含分割程序（split.py）、主程序（main.py）、测试数据（test.fastq）、参数json文件（args.json)。args.json内容如下：

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

然后执行以下命令

```shell
python start.py example/args.json
```

