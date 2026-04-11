# SPIN模型检测教程

> **所属教程**: Tools/Tutorials | **预计学习时间**: 3-4小时 | **前置知识**: 基本编程、时序逻辑概念

## 概述

SPIN (Simple Promela Interpreter) 是用于验证分布式系统模型的著名模型检测工具。本教程将通过实际示例带您掌握SPIN的使用。

## 学习目标

完成本教程后，您将能够：

1. 使用Promela语言建模并发系统
2. 使用SPIN进行模型检测
3. 识别和修复并发错误
4. 验证安全性和活性性质
5. 理解模型检测的局限性和最佳实践

---

## 第1部分：环境搭建（30分钟）

### 1.1 安装SPIN

**Linux/macOS**:

```bash
# 从源码编译
wget https://github.com/nimble-code/Spin/archive/refs/tags/version-6.5.2.tar.gz
tar -xzf version-6.5.2.tar.gz
cd Spin-version-6.5.2/Src6.5.2

# 编译
make
sudo cp spin /usr/local/bin/

# 验证安装
spin -V
```

**Windows**:

- 下载预编译二进制: <http://spinroot.com/spin/whatispin.html>
- 或使用 WSL

### 1.2 安装辅助工具

```bash
# 安装iSpin (GUI前端，可选)
cd Spin-version-6.5.2/iSpin
./install.sh

# 安装GCC（用于pan.c编译）
sudo apt-get install gcc
```

### 1.3 首个SPIN验证

创建文件 `hello.pml`：

```promela
/* 最简单的Promela程序 */
init {
    printf("Hello, SPIN!")
}
```

**验证步骤**:

```bash
# 语法检查
spin -a hello.pml

# 解释执行
spin hello.pml

# 编译并运行
gcc -o pan pan.c
./pan

# 或一步完成
spin -run hello.pml
```

---

## 第2部分：Promela基础（1小时）

### 2.1 进程

```promela
/* 多进程示例 */
active proctype P() {
    printf("Process P")
}

active proctype Q() {
    printf("Process Q")
}
```

**执行特性**:

- 进程并发执行（交错语义）
- `active` 关键字自动启动进程
- 进程可以动态创建

### 2.2 变量和类型

```promela
/* 基本类型 */
bit     flag;           /* 0 或 1 */
bool    done;           /* false 或 true */
byte    count;          /* 0-255 */
short   temp;           /* -32768 到 32767 */
int     value;          /* 32位整数 */
pid     proc_id;        /* 进程ID */

/* 数组 */
int buffer[10];

/* 通道（进程间通信）*/
chan name = [0] of { byte };      /* 同步通道 */
chan queue = [10] of { int };     /* 异步通道（容量10）*/
chan msg = [5] of { byte, int };  /* 消息含两个字段 */
```

### 2.3 控制结构

```promela
/* 条件语句 */
if
:: (x > 0) -> x = x - 1
:: (x < 0) -> x = x + 1
:: (x == 0) -> break
fi

/* 循环 */
do
:: (x < 10) -> x++
:: (x >= 10) -> break
od

/* 选择守卫 */
do
:: atomic { (count < N) -> buffer[count] = msg; count++ }
:: atomic { (count > 0) -> count-- }
od
```

**练习1**: 编写一个产生-消费者模型，一个进程生产数据，一个消费数据。

---

## 第3部分：互斥验证（1小时）

### 3.1 Dekker算法

```promela
/* Dekker互斥算法 */
#define true    1
#define false   0
#define N       2

bool want[N];
bool turn;

active [N] proctype P() {
    pid i, j;

    i = _pid;
    j = 1 - _pid;

    do
    ::  want[i] = true;
        do
        :: !want[j] -> break
        :: want[j] ->
            if
            :: (turn == j) ->
                want[i] = false;
                (turn == i);
                want[i] = true
            :: (turn == i)
            fi
        od;

        /* 临界区 */
        printf("Process %d in critical section", i);

        turn = j;
        want[i] = false;

        /* 非临界区 */
    od
}
```

### 3.2 验证互斥性质

**添加断言**：

```promela
/* 添加在临界区 */
critical:
    assert(!(P[0]@critical && P[1]@critical));
    printf("Process %d in critical section", i);
```

**验证命令**：

```bash
# 安全性质验证（无断言违反）
spin -a dekker.pml
gcc -o pan pan.c
./pan -a

# 或
spin -run -a dekker.pml
```

### 3.3 活性验证

**添加进度标签**：

```promela
progress:
    printf("Process %d in critical section", i);
```

**验证无进展循环**：

```bash
# 检查无进展循环
./pan -l

# 或
spin -run -l dekker.pml
```

### 3.4 验证死锁

```bash
# 检查死锁
./pan -a

# 无死锁报告表示成功
```

**练习2**: 修改Dekker算法引入一个bug，观察SPIN如何发现。

---

## 第4部分：通信协议验证（1小时）

### 4.1 交替位协议

```promela
/* 交替位协议模型 */

#define DATA    5
#define TIMEOUT 10

chan sender_to_receiver = [1] of { byte, bit };
chan receiver_to_sender = [1] of { bit };

bit send_bit, recv_bit;

active proctype Sender() {
    byte data = 0;

    do
    ::  sender_to_receiver!data,send_bit;
        do
        ::  receiver_to_sender?recv_bit;
            if
            :: (recv_bit == send_bit) ->
                send_bit = 1 - send_bit;
                data = (data + 1) % DATA;
                break
            :: (recv_bit != send_bit)
            fi
        ::  timeout ->  /* 超时重传 */
            sender_to_receiver!data,send_bit
        od
    od
}

active proctype Receiver() {
    byte data;
    bit received_bit;

    do
    ::  sender_to_receiver?data,received_bit;
        if
        :: (received_bit == recv_bit) ->
            recv_bit = 1 - recv_bit
        :: (received_bit != recv_bit)  /* 重复，丢弃 */
        fi;
        receiver_to_sender!recv_bit
    od
}
```

### 4.2 性质验证

**数据正确性**：

```promela
/* 验证接收数据有序 */
byte last_received = 0;

active proctype Receiver() {
    byte data;
    bit received_bit;

    do
    ::  sender_to_receiver?data,received_bit;
        if
        :: (received_bit == recv_bit) ->
            assert(data == last_received);
            last_received = (last_received + 1) % DATA;
            recv_bit = 1 - recv_bit
        :: (received_bit != recv_bit)
        fi;
        receiver_to_sender!recv_bit
    od
}
```

**验证命令**：

```bash
# 验证所有性质
spin -run -a -l -f abp.pml
```

### 4.3 LTL性质

**定义LTL公式**（文件 `abp.ltl`）：

```ltl
/* 始终最终会收到正确数据 */
<>[] (received == expected)

/* 不会永远卡在发送状态 */
!([] (sender_state == WAITING))

/* 互斥：不会同时发送和接收同一帧 */
[](!(sending && receiving_same_frame))
```

**使用LTL验证**：

```bash
# 将LTL转换为never claim
spin -f '!([] (received == expected))' > abp_never.pml

# 合并并验证
cat abp.pml abp_never.pml > abp_check.pml
spin -a abp_check.pml
gcc -o pan pan.c
./pan -a -N
```

---

## 第5部分：高级特性（30分钟）

### 5.1 原子操作和d_step

```promela
/* 原子操作 - 不可中断 */
atomic {
    x = x + 1;
    y = y + 1
}

/* d_step - 确定性步骤，不可见中间状态 */
d_step {
    x = x + 1;
    y = y + 1
}
```

### 5.2 嵌入式C代码

```promela
/* 在模型中使用C函数 */
c_decl {
    #include <stdio.h>
    int external_counter = 0;
}

c_track "external_counter" "sizeof(int)";

proctype Example() {
    c_code {
        external_counter++;
        printf("Counter: %d", external_counter);
    };
    printf("Done")
}
```

### 5.3 随机化和模拟

```bash
# 随机模拟
spin -p -g -l -r hello.pml

# 交互式模拟
spin -i hello.pml

# 生成轨迹
spin -t -p hello.pml
```

---

## 综合练习：哲学家就餐问题

### 任务

使用SPIN验证Dijkstra哲学家就餐问题的解决方案。

**要求**:

1. 建模5个哲学家和5把叉子
2. 实现一种解决方案（如资源分级）
3. 验证无死锁
4. 验证无饥饿

**参考答案框架**：

```promela
#define N       5
#define THINKING    0
#define HUNGRY      1
#define EATING      2

byte state[N];
chan forks[N] = [1] of { bit };

/* 资源分级解决方案 */
active [N] proctype Philosopher() {
    byte left = _pid;
    byte right = (_pid + 1) % N;
    byte first, second;

    /* 按资源ID排序，避免循环等待 */
    if
    :: (left < right) ->
        first = left; second = right
    :: (right < left) ->
        first = right; second = left
    :: (left == right) -> assert(false) /* 错误情况 */
    fi;

    do
    ::  /* 思考 */
        state[_pid] = THINKING;

        /* 拿叉子 */
        state[_pid] = HUNGRY;
        forks[first]?1;
        forks[second]?1;

        /* 进食 */
        state[_pid] = EATING;
        printf("Philosopher %d is eating", _pid);

        /* 放叉子 */
        forks[second]!1;
        forks[first]!1;
    od
}

/* 初始化 */
init {
    byte i;
    atomic {
        for (i : 0 .. N-1) {
            forks[i]!1  /* 所有叉子可用 */
        }
    }
}

/* 安全性质：相邻哲学家不同时进食 */
#define left_neighbor ( (_pid + N - 1) % N )
#define right_neighbor ( (_pid + 1) % N )

/* 使用never claim验证无死锁 */
never {
    do
    :: skip  /* 接受任何状态 */
    od
}
```

**验证命令**：

```bash
# 检查死锁
spin -run -a dining.pml

# 检查无进展循环（饥饿）
spin -run -l dining.pml

# 生成反例（如果失败）
spin -t -p dining.pml
```

---

## 总结

### 关键概念回顾

1. **Promela语言**: 进程、通道、守卫命令
2. **交错语义**: 非确定性执行，全覆盖状态空间
3. **验证类型**: 断言、死锁、无进展、LTL性质
4. **验证流程**: 建模 -> 编译 -> 运行验证器 -> 分析结果

### SPIN命令速查

| 命令 | 作用 |
|------|------|
| `spin file.pml` | 解释执行 |
| `spin -a file.pml` | 生成验证器 |
| `spin -t file.pml` | 执行轨迹 |
| `spin -p file.pml` | 打印所有状态 |
| `./pan` | 运行验证器 |
| `./pan -a` | 检查断言 |
| `./pan -l` | 检查无进展循环 |
| `./pan -f` | 检查LTL性质 |

### 进一步学习资源

- [SPIN Homepage](http://spinroot.com/)
- [The SPIN Model Checker](https://spinroot.com/spin/Doc/) - 书籍和文档
- [Promela Manual](http://spinroot.com/spin/Man/promela.html)

### 最佳实践

1. **从小模型开始**，逐步增加复杂度
2. **使用atomic减少状态空间**
3. **限制数据范围**（如用 `byte` 代替 `int`）
4. **先验证安全性质**，再验证活性
5. **理解状态空间爆炸**，使用压缩或分片

---

## 常见问题解答

**Q: SPIN报告 "state space too large" 怎么办？**
A: 使用 `-DCOLLAPSE` 或 `-DMA=` 选项，或减少模型中的数据范围。

**Q: 如何减少误报？**
A: 仔细检查模型的环境假设，确保模型准确反映系统设计。

**Q: SPIN和TLA+如何选择？**
A: SPIN更适合细粒度并发协议，TLA+更适合高层分布式系统设计。

---

*本教程基于 SPIN 6.5+ 版本编写*
