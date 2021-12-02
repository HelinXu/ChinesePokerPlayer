# AI Project 1: Chinese Poker

Author: HelinXu

<img width="1274" alt="image-20211105140356503" src="https://user-images.githubusercontent.com/59716259/144416927-9a475219-3c50-43ee-bb1a-b7ac5042bc3e.png">

## Requirements

- macOS Big Sur 11.5.2
- python 3.7.10
- tk 8.6.10
- pillow 8.3.2
- numpy 1.20.2

## File organization

```shell
.
├── bfs_play.py # 宽度优先搜索算法实现，但是效率过低。
├── card_game.py # 动态规划算法实现。
├── contest.py # 选做：模拟一对一对打。
├── dfs_play.py # 第一问：深度优先搜索算法实现。
├── dfs_play_2.py # 第二问：深度优先搜索算法实现。
├── play.py # 界面：运行此程序以可视化。
├── readme.md
└── resource # 扑克牌png
    └── pokers
```

## Usage

To run UI:

```shell
cd source
python play.py
```

You should see UI within seconds.

To test 1.1 and 1.2 separately:

```shell
python dfs_play.py -n NUM_OF_CARDS
python dfs_play_2.py -n NUM_OF_CARDS
```
