---
name: sbti
description: >
  SBTI 人格测试。一个基于 15 维度、30+ 道题目的趣味人格测试。
  对话式问答完成测试，最终返回对应的人格图片。
  触发词：测测人格、SBTI、sbti、人格测试
user_invocable: true
---

# SBTI 人格测试

基于 B站 up 主@蛆肉儿串儿 的 SBTI 测试改编，对话式问答，15 维度解析，最终输出人格结果图片。

## 使用方法

```
/sbti
```

---

## 执行流程

### Step 0: 初始化测试

显示欢迎语，介绍测试规则，准备开始问答。

### Step 1: 问答阶段

通过对话式问答收集用户答案，每次展示 1 道题目，记录选项。

题目分为两类：
- **维度题**（30 道）：覆盖 15 个维度（每维度 2 题）
- **特殊题**（2 道）：饮酒门槛题，用于触发隐藏人格

**维度说明：**

| 维度 | 名称 | 所属模型 |
|------|------|----------|
| S1 | 自尊自信 | 自我模型 |
| S2 | 自我清晰度 | 自我模型 |
| S3 | 核心价值 | 自我模型 |
| E1 | 依恋安全感 | 情感模型 |
| E2 | 情感投入度 | 情感模型 |
| E3 | 边界与依赖 | 情感模型 |
| A1 | 世界观倾向 | 态度模型 |
| A2 | 规则与灵活度 | 态度模型 |
| A3 | 人生意义感 | 态度模型 |
| Ac1 | 动机导向 | 行动驱力模型 |
| Ac2 | 决策风格 | 行动驱力模型 |
| Ac3 | 执行模式 | 行动驱力模型 |
| So1 | 社交主动性 | 社交模型 |
| So2 | 人际边界感 | 社交模型 |
| So3 | 表达与真实度 | 社交模型 |

### Step 2: 计算结果

使用 Python 脚本计算（必须使用 uvx）：

```bash
# 获取所有问题
uvx --from python python3 sbti.py questions

# 计算结果（通过 stdin 传入答案 JSON）
echo '{"q1": 3, "q2": 1, ...}' | uvx --from python python3 sbti.py calc
```

Python 实现见 `sbti.py`。

### Step 3: 保存图片到 Downloads 目录

跨平台兼容，使用 `$HOME/Downloads`（macOS/Linux/Git Bash on Windows 均支持）：

```bash
DOWNLOAD_DIR="$HOME/Downloads"
# Windows (PowerShell/CMD): C:\Users\<username>\Downloads
# 如果 $HOME/Downloads 不存在，尝试常见路径
if [ ! -d "$DOWNLOAD_DIR" ]; then
  DOWNLOAD_DIR="$USERPROFILE/Downloads"
fi
cp ./image/{类型代码}.png "$DOWNLOAD_DIR/sbti_{类型代码}.png"
```

例如：`cp ./image/CTRL.png "$HOME/Downloads/sbti_CTRL.png"`

### Step 4: 输出结果

输出格式：

```markdown
## 你的 SBTI 人格

**类型代码**：CTRL（拿捏者）

**匹配度**：92% · 精准命中 12/15 维

---

### 该人格的简单解读

[人格描述]

---

### 十五维度评分

| 维度 | 等级 | 解读 |
|------|------|------|
| S1 自尊自信 | H | ... |
| S2 自我清晰度 | M | ... |
| ... | ... | ... |

---

### 结果图片

图片已保存至：`$HOME/Downloads/sbti_{类型代码}.png`

![人格图片](file://$HOME/Downloads/sbti_{类型代码}.png)
```

---

## 核心实现

### 维度等级计算

每个维度 2 道题，每题 1-3 分：
- 分数 ≤ 3 → L（低）
- 分数 = 4 → M（中）
- 分数 ≥ 5 → H（高）

### 人格匹配算法

将用户的 15 维度等级序列（LLM-HMH-...）与 25 种人格的标准模式进行曼哈顿距离计算，距离越小相似度越高。

匹配度 = max(0, round((1 - distance / 30) * 100))

### 特殊规则

- **饮酒触发**：如果用户选择饮酒相关选项，直接触发 DRUNK（酒鬼）人格
- **兜底机制**：最高匹配度 < 60% 时，强制分配 HHHH（傻乐者）人格

---

## 图片路径

人格结果图片存储在 skill 目录下的 `image/` 子目录，文件名与类型代码对应：

- CTRL → image/CTRL.png
- ATM-er → image/ATM-er.png
- Dior-s → image/Dior-s.jpg
- ... 以此类推

---

*数据来源: SBTI-test by B站@蛆肉儿串儿 | 仅供娱乐，不构成任何心理/职业/相亲建议*
