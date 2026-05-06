---
name: ai-webdrama-storyboard
version: "1.0.0"
description: AI网剧分镜制作技能。提供符合短视频平台（抖音、红果等）黄金时间法则的分镜模板和生成工具，用于将网剧剧本转化为标准化分镜脚本。
---

# AI网剧分镜制作技能

## 技能概述
这是一个专门用于AI网剧分镜制作的OpenClaw技能。基于市场数据分析，提供符合短视频平台（抖音、红果等）黄金时间法则的分镜模板和生成工具。

## 功能特性

### 核心功能
1. **市场数据分析**：基于AI网剧市场数据生成分镜策略
2. **黄金时间优化**：自动优化前5秒和30秒关键镜头
3. **类型模板**：提供情感、逆袭、悬疑、甜宠四大类型模板
4. **人物刻画**：自动生成人物设定和成长弧线
5. **场景设计**：提供视觉风格和拍摄建议
6. **平台适配**：针对不同平台优化分镜节奏
7. **运镜设计**：17种运镜语言（基础→电影级→大师级），每镜必含运镜+景别+时长

### 🎥 运镜体系（17种，3级递进）

> 参考：[运镜语言参考库](../references/camera-movement-reference.md)

#### 每镜标准格式
```
[镜号] | [场景] | [运镜类型] | [景别] | [时长] | [描述]
运镜：[起点]→[终点] | 速度：[缓慢/匀速/快速] | 情绪：[关键词]
```

#### 基础运镜（6种）- 新手必会
| 运镜 | 英文 | 适用场景 | 示例指令 |
|------|------|----------|----------|
| 固定镜头 | Fixed Shot | 对话、独白、情绪酝酿 | 固定机位，[景别]，画面保持静止不动 |
| 推镜头 | Dolly In | 聚焦细节、悬念揭晓 | 画面从[全景]向前推进至[特写] |
| 拉镜头 | Dolly Out | 环境揭示、结尾升华 | 画面从[特写]向后缓缓退开至[远景] |
| 水平摇镜 | Pan Shot | 展示空间全貌 | 画面从[左/右]向[右/左]缓慢平移 |
| 垂直摇镜 | Tilt Shot | 人物登场、高度展示 | 画面从[下/上]向[上/下]缓缓移动 |
| 跟随镜头 | Follow Shot | 行走、追逐、探索 | 画面从[侧后/正后]方紧跟[主体]移动 |

#### 电影级运镜（6种）- 高手进阶
| 运镜 | 英文 | 适用场景 | 示例指令 |
|------|------|----------|----------|
| 环绕镜头 | Circular Tracking | 高光时刻、boss出场 | 画面围绕[主体]做360度旋转 |
| 升降镜头 | Crane Shot | 宏大开场、结尾 | 画面从[高度A]垂直[上升/下降]至[高度B] |
| 希区柯克变焦 | Dolly Zoom | 震惊、顿悟、崩溃 | 主体大小不变，背景透视拉伸变形 |
| 一镜到底 | Long Take | 空间漫游、沉浸探索 | 无剪切，画面从[起点]→[路径]→[终点] |
| 快速甩镜 | Whip Pan | 场景切换、反转 | 画面极速甩出→运动模糊→切换 |
| 鸟瞰俯拍 | Bird's-Eye | 建立镜头、布局展示 | 正上方垂直向下呈现 |

#### 大师级运镜（5种）- 导演签名式
| 导演风格 | 组合方式 | 标志特征 |
|----------|----------|----------|
| 斯皮尔伯格式 | 推镜头+固定+仰拍 | 看画外→表情变化，观众被带入 |
| 王家卫式 | 跟随+慢动作+高饱和 | 抽帧跳帧，红绿蓝霓虹，孤独迷人 |
| 韦斯·安德森式 | 固定+对称构图+平移 | 精确镜像对称，色彩统一极致 |
| 诺兰式 | 推拉交替+色调对比 | 双时空交叉，暖黄vs冷蓝 |
| 塔可夫斯基式 | 极慢一镜到底+环境细节 | 每个细节都变"角色"，诗意凝视 |

### 数据支持
- 用户画像：18-35岁为主，女性60%
- 播放权重：抖音45%，红果25%，其他30%
- 爆款分类：情感类35%，逆袭类25%，悬疑类20%，甜宠类15%
- 核心要素：开篇钩子30%，情绪共鸣25%，视觉冲击20%

## 使用方法

### 基本命令
```bash
# 生成完整分镜框架
python ai_webdrama.py generate --title "水世界狂鲨" --genre "sci-fi" --episodes 5

# 分析市场数据
python ai_webdrama.py analyze --platform "douyin"

# 优化黄金时间
python ai_webdrama.py optimize --input storyboard.json --focus "5s-30s"

# 导出为不同格式
python ai_webdrama.py export --input storyboard.json --format "markdown"
python ai_webdrama.py export --input storyboard.json --format "json"
python ai_webdrama.py export --input storyboard.json --format "excel"
```

### OpenClaw集成
```python
from skills.ai_webdrama_storyboard import WebDramaStoryboard

# 创建分镜生成器
generator = WebDramaStoryboard()

# 生成分镜
storyboard = generator.generate(
    title="水世界狂鲨",
    genre="sci-fi",
    episodes=5,
    target_platforms=["douyin", "hongguo"],
    focus_golden_time=True
)

# 获取分镜详情
print(storyboard.get_summary())
print(storyboard.get_episode(1))
print(storyboard.get_golden_time_analysis())
```

## 文件结构

```
ai-webdrama-storyboard/
├── SKILL.md                    # 技能说明文档
├── ai_webdrama.py              # 主程序
├── templates/                  # 分镜模板
│   ├── emotional.json         # 情感类模板
│   ├── revenge.json           # 逆袭类模板
│   ├── suspense.json          # 悬疑类模板
│   └── sweet.json             # 甜宠类模板
├── data/                      # 市场数据
│   ├── market_analysis.json   # 市场分析数据
│   ├── platform_rules.json    # 平台规则
│   └── golden_time_rules.json # 黄金时间规则
├── examples/                  # 示例
│   └── water_world_shark/     # 水世界狂鲨示例
└── utils/                     # 工具函数
    ├── analyzer.py           # 数据分析器
    ├── optimizer.py          # 分镜优化器
    └── exporter.py           # 导出工具
```

## 安装依赖

```bash
pip install pandas numpy matplotlib openpyxl
```

## 详细功能说明

### 1. 市场数据分析模块
- **平台特性分析**：抖音（快节奏）、红果（重情感）
- **用户偏好识别**：年龄、性别、观看时段
- **竞品分析**：爆款网剧元素提取
- **趋势预测**：热门题材和表现手法

### 2. 黄金时间优化器
- **前5秒优化**：
  - 视觉冲击检测
  - 情绪共鸣评分
  - 信息密度分析
  - 声音设计建议

- **30秒优化**：
  - 情节推进节奏
  - 人物关系建立
  - 悬念设置强度
  - 情绪曲线设计

### 3. 类型模板系统
- **情感类模板**：
  - 核心：情绪共鸣，家庭/爱情/友情
  - 节奏：情感积累→爆发→解决
  - 视觉：温暖色调，特写镜头

- **逆袭类模板**：
  - 核心：弱者反击，职场/人生翻盘
  - 节奏：压抑→转折→逆袭→胜利
  - 视觉：对比色调，仰拍/俯拍切换

- **悬疑类模板**：
  - 核心：神秘事件，身份谜团
  - 节奏：引入→发展→转折→揭示
  - 视觉：冷色调，阴影运用，主观镜头

- **甜宠类模板**：
  - 核心：甜蜜互动，浪漫误会
  - 节奏：相遇→误会→甜蜜→承诺
  - 视觉：明亮色调，柔光效果

### 4. 人物刻画工具
- **主角生成**：姓名、年龄、职业、性格、目标、冲突
- **配角设计**：反派、盟友、爱情线
- **成长弧线**：初始状态→挑战→成长→新平衡
- **关系网络**：人物关系图，情感发展线

### 5. 场景设计系统
- **主要场景**：开场、冲突、转折、高潮、结尾
- **视觉风格**：色调、镜头、运动、灯光、特效
- **声音设计**：音效、音乐、台词、静默
- **拍摄技巧**：主观镜头、狭窄构图、快速剪辑

## API参考

### WebDramaStoryboard类

#### 初始化
```python
generator = WebDramaStoryboard(
    data_dir="data",          # 数据目录
    template_dir="templates", # 模板目录
    use_ai_suggestions=True   # 是否使用AI建议
)
```

#### 生成分镜
```python
storyboard = generator.generate(
    title="剧集标题",
    genre="sci-fi",          # 类型：sci-fi, emotional, revenge, suspense, sweet
    episodes=5,              # 集数
    target_platforms=["douyin", "hongguo"],  # 目标平台
    focus_golden_time=True,  # 是否优化黄金时间
    custom_rules={}          # 自定义规则
)
```

#### 分析方法
```python
# 市场分析
analysis = generator.analyze_market(platform="douyin")

# 分镜优化
optimized = generator.optimize_golden_time(
    storyboard, 
    focus_seconds=[5, 30]
)

# 导出分镜
generator.export(
    storyboard, 
    format="markdown", 
    output_path="output/"
)
```

#### 获取信息
```python
# 获取摘要
summary = storyboard.get_summary()

# 获取单集分镜
episode1 = storyboard.get_episode(1)

# 获取黄金时间分析
golden_time = storyboard.get_golden_time_analysis()

# 获取人物设定
characters = storyboard.get_characters()

# 获取场景设计
scenes = storyboard.get_scenes()
```

## 示例：水世界狂鲨

### 生成命令
```bash
python ai_webdrama.py generate \
  --title "水世界狂鲨" \
  --genre "sci-fi" \
  --episodes 5 \
  --platforms "douyin,hongguo" \
  --output "output/water_world_shark"
```

### 输出文件
```
output/water_world_shark/
├── summary.md              # 项目摘要
├── episode_1.md           # 第1集分镜
├── episode_2.md           # 第2集分镜
├── episode_3.md           # 第3集分镜
├── episode_4.md           # 第4集分镜
├── episode_5.md           # 第5集分镜
├── characters.json        # 人物设定
├── scenes.json           # 场景设计
├── golden_time_analysis.md # 黄金时间分析
└── market_analysis.md     # 市场分析报告
```

## 配置选项

### 配置文件：config.json
```json
{
  "market_data": {
    "user_profile": {
      "age_range": "18-35",
      "gender_ratio": {"female": 60, "male": 40},
      "preferred_genres": ["emotional", "revenge", "suspense", "sweet"]
    },
    "platform_distribution": {
      "douyin": 45,
      "hongguo": 25,
      "others": 30
    },
    "success_factors": {
      "opening_hook": 30,
      "emotional_resonance": 25,
      "visual_impact": 20,
      "rhythm_control": 15,
      "plot_twist": 10
    }
  },
  "golden_time_rules": {
    "first_5_seconds": {
      "visual_impact": "required",
      "emotional_setup": "required",
      "core_conflict": "hinted",
      "sound_design": "important"
    },
    "first_30_seconds": {
      "plot_progression": "required",
      "character_relationship": "established",
      "suspense_setup": "required",
      "rhythm_control": "fast"
    }
  },
  "export_options": {
    "formats": ["markdown", "json", "excel"],
    "include_analysis": true,
    "include_templates": true,
    "create_examples": true
  }
}
```

## 故障排除

### 常见问题
1. **依赖安装失败**：确保使用Python 3.8+
2. **模板加载错误**：检查templates目录文件格式
3. **导出格式不支持**：确认安装了openpyxl（Excel导出）
4. **内存不足**：减少集数或关闭AI建议

### 调试模式
```bash
python ai_webdrama.py generate --debug --verbose
```

## 更新日志

### v1.0.0 (2026-04-10)
- 初始版本发布
- 支持四大类型模板
- 黄金时间优化功能
- 多平台导出支持
- 水世界狂鲨示例

## 贡献指南
欢迎提交Issue和Pull Request，共同完善AI网剧分镜制作工具。

## 许可证
MIT License