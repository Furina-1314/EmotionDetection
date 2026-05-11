# Emotion Detection Counter

读取多条以换行分隔的英文评论，识别每条评论中的情绪（可多标签），并统计每个情绪出现频数。

## 支持情绪（28类）

admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride, realization, relief, remorse, sadness, surprise, neutral

> `neutral` 规则：当一条评论没有命中任何其他情绪词时，记为 `neutral`。

## 使用方法

```bash
python emotion_counter.py --file comments.txt
```

或：

```bash
cat comments.txt | python emotion_counter.py
```

## 输入格式

- 每行一条英文评论
- 空行自动忽略

## 输出格式

输出 `emotion<TAB>count`。
