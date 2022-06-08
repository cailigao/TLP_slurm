## TLP_slurm

[English](README.md) | 简体中文

**使用[`Slurm`](https://github.com/SchedMD/slurm)完成多节点任务级并行。适用于数据可以分割的程序。**

任务分为两个步骤进行：数据分割、主程序处理。

**数据分割**：将需要处理的数据分割为多个小数据。

**主程序**：执行主程序分别处理这些小数据。

## 依赖

python>=3.6

simple_slurm=0.2.3

## 使用

### 1. 准备

在json文件中按照如下格式（[example_args.json](example_args.json)）编写命令行参数，配置文件包含数据分割程序参数配置(split)和主程序参数配置（main）两个部分。

[example_args.json](example_args.json)：

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

| key                    | value                                      |
| ---------------------- | ------------------------------------------ |
| **bin**                | 程序的路径                                 |
| **type**               | 程序的类型: python/C/java                  |
| **input.my_input**     | 你程序的输入形参                           |
| **input.value**        | 你程序的输入实参，**注意主程序不需要设置** |
| **output.my_output**   | 你程序的输出形参                           |
| **output.value**       | 你程序的输出实参                           |
| **threads.my_threads** | 你程序的线程形参                           |
| **threads.value**      | 你程序的线程实参                           |
| **my_args** [optional] | 程序的其他参数都可以放到这里               |

### 2. 开始

设置好参数json文件中的值后，通过以下命令传递参数json文件并开始执行程序

```shell
$ python start.py example_args.json
```

## 例子

example是一个分割fastq数据并打印的程序，包含分割程序([split.py](example/split.py))、主程序([main.py](example/main.py))、测试数据([test.fastq](example/test.fastq))、参数json文件([args.json](example/args.json))。[args.json](example/args.json)内容如下：

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

然后执行以下命令:

```shell
$ python start.py example/args.json
```

在`example/output`中可以看到输出

