---
name: china-stocks
description: 获取中国A股市场数据，包括上证指数、深证成指、创业板指等主要指数。提供实时行情、历史数据和市场分析。
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["curl","python3"]},"os":["linux","darwin","win32"]}}
---

# 中国A股市场数据

获取中国A股市场实时行情、历史数据和市场分析。

## 功能特性

- 获取主要指数实时数据
- 查看个股行情
- 获取历史K线数据
- 市场涨跌统计
- 板块资金流向

## 主要指数代码

### 大盘指数
- **上证指数**: `sh000001`
- **深证成指**: `sz399001`
- **创业板指**: `sz399006`
- **科创50**: `sh000688`
- **沪深300**: `sh000300`
- **中证500**: `sh000905`

### 常用个股
- **贵州茅台**: `sh600519`
- **宁德时代**: `sz300750`
- **招商银行**: `sh600036`
- **中国平安**: `sh601318`
- **五粮液**: `sz000858`

## 使用方法

### 1. 获取实时行情（新浪财经API）

```bash
# 获取上证指数
curl -s "https://hq.sinajs.cn/list=sh000001"

# 获取多个指数
curl -s "https://hq.sinajs.cn/list=sh000001,sz399001,sz399006"

# 解析数据示例（返回格式：var hq_str_sh000001="上证指数,3479.12,3480.13,...";）
```

### 2. 使用Python获取数据

```python
import requests
import json

def get_stock_data(stock_code):
    """获取股票实时数据"""
    url = f"https://hq.sinajs.cn/list={stock_code}"
    headers = {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # 解析数据
            data = response.text
            # 格式: var hq_str_sh000001="名称,今开,昨收,当前,最高,最低,...";
            content = data.split('="')[1].split('"')[0]
            values = content.split(',')
            
            return {
                'name': values[0],
                'open': float(values[1]),
                'close': float(values[2]),
                'current': float(values[3]),
                'high': float(values[4]),
                'low': float(values[5]),
                'volume': float(values[8]),
                'amount': float(values[9])
            }
    except Exception as e:
        print(f"获取数据失败: {e}")
    
    return None

# 示例：获取上证指数
sh_index = get_stock_data('sh000001')
if sh_index:
    print(f"上证指数: {sh_index['current']} 点")
    print(f"涨跌: {sh_index['current'] - sh_index['close']:+.2f}")
    print(f"涨幅: {(sh_index['current']/sh_index['close'] - 1)*100:+.2f}%")
```

### 3. 获取历史数据

```python
import akshare as ak

# 安装: pip install akshare

def get_history_data(stock_code, start_date, end_date):
    """获取历史K线数据"""
    try:
        # 使用akshare获取数据
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"
        )
        return df
    except Exception as e:
        print(f"获取历史数据失败: {e}")
        return None

# 示例：获取贵州茅台最近30天数据
# df = get_history_data("600519", "20240101", "20240211")
```

### 4. 市场概况

```bash
# 获取涨跌家数（东方财富）
curl -s "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f2,f3,f4,f12,f14&secids=1.000001,0.399001,0.399006"

# 获取板块涨幅榜
curl -s "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152"
```

## 数据字段说明

### 新浪财经API返回字段（以sh000001为例）：
```
var hq_str_sh000001="上证指数,3479.12,3480.13,3478.56,3485.21,3465.43,3478.56,0,0,1234567890,12345678900,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2024-02-11,15:00:00,00,";
```

字段说明：
1. 指数名称
2. 今日开盘
3. 昨日收盘
4. 当前价格
5. 今日最高
6. 今日最低
7. 竞买价（买一）
8. 竞卖价（卖一）
9. 成交数量（手）
10. 成交金额（万元）
11. 买一量
12. 买一价
13. 买二量
14. 买二价
15. 买三量
16. 买三价
17. 买四量
18. 买四价
19. 买五量
20. 买五价
21. 卖一量
22. 卖一价
23. 卖二量
24. 卖二价
25. 卖三量
26. 卖三价
27. 卖四量
28. 卖四价
29. 卖五量
30. 卖五价
31. 日期
32. 时间
33. 状态

## 常用命令

### 查看今日大盘
```bash
# 查看主要指数
./scripts/check_market.sh

# 查看个股
./scripts/check_stock.sh 600519
```

### 市场分析
```bash
# 生成市场日报
./scripts/market_report.sh

# 技术分析
./scripts/technical_analysis.sh 000001
```

## 注意事项

1. **数据延迟**: 免费API通常有15分钟延迟
2. **访问频率**: 避免频繁请求，建议间隔至少5秒
3. **数据准确性**: 以交易所官方数据为准
4. **投资风险**: 数据仅供参考，不构成投资建议

## 数据源

1. **新浪财经**: `https://hq.sinajs.cn/`
2. **东方财富**: `https://push2.eastmoney.com/`
3. **腾讯财经**: `https://qt.gtimg.cn/`
4. **网易财经**: `https://api.money.126.net/`

## 扩展功能

### 添加监控提醒
```python
# 价格提醒
def price_alert(stock_code, target_price):
    current = get_stock_data(stock_code)['current']
    if current >= target_price:
        send_notification(f"{stock_code} 达到目标价 {target_price}")

# 涨跌幅提醒
def change_alert(stock_code, threshold=5):
    data = get_stock_data(stock_code)
    change_percent = (data['current'] / data['close'] - 1) * 100
    if abs(change_percent) >= threshold:
        send_notification(f"{stock_code} 涨跌幅 {change_percent:.2f}%")
```

### 数据可视化
```python
import matplotlib.pyplot as plt
import pandas as pd

def plot_stock_history(stock_code, days=30):
    """绘制股票走势图"""
    df = get_history_data(stock_code, days)
    if df is not None:
        plt.figure(figsize=(12, 6))
        plt.plot(df['日期'], df['收盘'])
        plt.title(f'{stock_code} 近期走势')
        plt.xlabel('日期')
        plt.ylabel('价格')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{stock_code}_chart.png')
        plt.show()
```

## 故障排除

### 常见问题
1. **API返回403**: 添加合适的请求头（Referer, User-Agent）
2. **数据为空**: 检查股票代码格式是否正确
3. **连接超时**: 检查网络连接，尝试其他数据源
4. **数据解析错误**: 确认API返回格式是否变化

### 调试命令
```bash
# 测试API连接
curl -v "https://hq.sinajs.cn/list=sh000001" -H "Referer: https://finance.sina.com.cn"

# 查看原始数据
curl -s "https://hq.sinajs.cn/list=sh000001" | head -c 200
```

## 更新日志

- v1.0.0: 初始版本，支持基本行情查询
- v1.1.0: 添加历史数据获取功能
- v1.2.0: 添加市场分析工具

## 免责声明

本技能提供的数据仅供参考，不构成任何投资建议。股市有风险，投资需谨慎。使用者应自行承担投资风险。