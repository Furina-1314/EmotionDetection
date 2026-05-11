# Emotion Detection Counter

这个项目可以读取多条以换行分隔的英文评论，识别每条评论中包含的情绪（支持一条评论对应多个情绪），并统计每个情绪出现的频数。

## 支持的情绪（英文）

- joy
- sadness
- anger
- fear
- surprise
- disgust

## 使用方法

### 1) 从文件读取

```bash
python emotion_counter.py --file comments.txt
```

### 2) 从标准输入读取

```bash
cat comments.txt | python emotion_counter.py
```

## 输入格式

- 每行一条英文评论。
- 空行会被自动忽略。

## 输出格式

输出 `emotion<TAB>count` 表格，例如：

```text
emotion  count
anger    1
disgust  0
fear     2
joy      3
sadness  1
surprise 0
```
