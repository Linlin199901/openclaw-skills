#!/usr/bin/env python3
"""
中国A股市场数据检查脚本
获取今日A股主要指数信息
"""

import requests
import json
from datetime import datetime

def get_stock_data(stock_code):
    """获取股票实时数据（新浪财经API）"""
    url = f"https://hq.sinajs.cn/list={stock_code}"
    headers = {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # 解析数据
            data = response.text
            if '="' in data:
                content = data.split('="')[1].split('"')[0]
                values = content.split(',')
                
                if len(values) >= 32:
                    return {
                        'name': values[0],
                        'open': float(values[1]) if values[1] else 0,
                        'close': float(values[2]) if values[2] else 0,
                        'current': float(values[3]) if values[3] else 0,
                        'high': float(values[4]) if values[4] else 0,
                        'low': float(values[5]) if values[5] else 0,
                        'volume': float(values[8]) if values[8] else 0,
                        'amount': float(values[9]) if values[9] else 0,
                        'date': values[30] if len(values) > 30 else '',
                        'time': values[31] if len(values) > 31 else ''
                    }
    except Exception as e:
        print(f"获取 {stock_code} 数据失败: {e}")
    
    return None

def format_change(current, close):
    """计算涨跌和涨幅"""
    if close == 0:
        return 0, 0
    
    change = current - close
    change_percent = (change / close) * 100
    return change, change_percent

def print_stock_info(stock_code, name):
    """打印股票信息"""
    data = get_stock_data(stock_code)
    if data:
        change, change_percent = format_change(data['current'], data['close'])
        
        # 判断涨跌颜色
        if change > 0:
            change_str = f"\033[92m+{change:.2f}\033[0m"
            percent_str = f"\033[92m+{change_percent:.2f}%\033[0m"
        elif change < 0:
            change_str = f"\033[91m{change:.2f}\033[0m"
            percent_str = f"\033[91m{change_percent:.2f}%\033[0m"
        else:
            change_str = f"{change:.2f}"
            percent_str = f"{change_percent:.2f}%"
        
        print(f"{name:10} {data['current']:8.2f} {change_str:>10} {percent_str:>10}")
        return data['current'], change_percent
    else:
        print(f"{name:10} {'N/A':8} {'N/A':>10} {'N/A':>10}")
        return None, None

def main():
    """主函数"""
    print("=" * 60)
    print("             今日A股市场概况")
    print("=" * 60)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    print(f"{'指数名称':10} {'当前点位':8} {'涨跌':>10} {'涨幅':>10}")
    print("-" * 60)
    
    # 主要指数
    indices = [
        ('sh000001', '上证指数'),
        ('sz399001', '深证成指'),
        ('sz399006', '创业板指'),
        ('sh000688', '科创50'),
        ('sh000300', '沪深300'),
        ('sh000905', '中证500')
    ]
    
    results = []
    for code, name in indices:
        current, change_percent = print_stock_info(code, name)
        if current is not None and change_percent is not None:
            results.append({
                'name': name,
                'current': current,
                'change_percent': change_percent
            })
    
    print("-" * 60)
    
    # 统计信息
    if results:
        # 计算平均涨跌幅
        avg_change = sum(r['change_percent'] for r in results) / len(results)
        
        # 找出最强和最弱指数
        strongest = max(results, key=lambda x: x['change_percent'])
        weakest = min(results, key=lambda x: x['change_percent'])
        
        print(f"平均涨跌幅: {avg_change:+.2f}%")
        print(f"最强指数: {strongest['name']} ({strongest['change_percent']:+.2f}%)")
        print(f"最弱指数: {weakest['name']} ({weakest['change_percent']:+.2f}%)")
    
    print("=" * 60)
    print("数据来源: 新浪财经 (https://finance.sina.com.cn)")
    print("备注: 数据可能有15分钟延迟")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")