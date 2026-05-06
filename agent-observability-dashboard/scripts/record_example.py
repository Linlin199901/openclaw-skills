#!/usr/bin/env python3
"""
记录示例数据到Agent Observability Dashboard
"""

import time
import random
from datetime import datetime
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入observability模块
from scripts.observability import record_metric, init_db

def record_example_data():
    """记录示例数据"""
    
    # 初始化数据库
    init_db()
    
    print("开始记录示例数据...")
    
    # 模拟不同的会话
    sessions = [
        "agent:main:session_001",
        "agent:main:session_002", 
        "agent:secondary:session_001"
    ]
    
    # 模拟的工具列表
    tools = [
        "web_search",
        "web_fetch", 
        "exec",
        "read",
        "write",
        "edit",
        "message",
        "memory_search",
        "browser",
        "cron"
    ]
    
    # 记录50个示例指标
    for i in range(50):
        session = random.choice(sessions)
        tool = random.choice(tools)
        
        # 模拟延迟（大部分在正常范围，偶尔有高延迟）
        if random.random() < 0.1:  # 10%的概率高延迟
            latency = random.uniform(2000, 5000)  # 2-5秒
        else:
            latency = random.uniform(100, 1500)  # 0.1-1.5秒
        
        # 模拟成功率（大部分成功，偶尔失败）
        success = random.random() < 0.9  # 90%成功率
        
        # 模拟token使用量
        tokens_used = random.randint(50, 5000)
        
        # 模拟参数
        params = {
            "query": f"示例查询 {i}" if tool in ["web_search", "memory_search"] else None,
            "path": f"/path/to/file_{i}.txt" if tool in ["read", "write", "edit"] else None,
            "command": f"echo 'test {i}'" if tool == "exec" else None
        }
        
        # 记录指标
        record_metric(
            session_id=session,
            agent_id=session.split(":")[1],
            tool_name=tool,
            latency_ms=latency,
            success=success,
            tokens_used=tokens_used,
            error_message=None if success else f"模拟错误 {i}",
            params=params
        )
        
        print(f"记录 {i+1}/50: {tool} - {latency:.0f}ms - {'成功' if success else '失败'}")
        time.sleep(0.1)  # 稍微延迟一下
    
    print("\n示例数据记录完成！")
    print(f"记录了50个指标到数据库")
    print("现在可以启动仪表板查看数据了")

def generate_realistic_data():
    """生成更真实的数据模式"""
    
    init_db()
    
    print("生成真实数据模式...")
    
    # 创建更真实的数据模式
    patterns = [
        # 模式1: 网页搜索会话
        {
            "session": "agent:main:web_research",
            "tools": ["web_search", "web_fetch", "read", "write"],
            "count": 15,
            "avg_latency": 1200,
            "success_rate": 0.95
        },
        # 模式2: 文件操作会话
        {
            "session": "agent:main:file_ops", 
            "tools": ["read", "write", "edit", "exec"],
            "count": 10,
            "avg_latency": 300,
            "success_rate": 0.98
        },
        # 模式3: 消息发送会话
        {
            "session": "agent:main:message_send",
            "tools": ["message", "memory_search"],
            "count": 8,
            "avg_latency": 800,
            "success_rate": 0.85
        },
        # 模式4: 浏览器自动化会话
        {
            "session": "agent:secondary:browser_auto",
            "tools": ["browser", "exec", "read"],
            "count": 12,
            "avg_latency": 2500,
            "success_rate": 0.75
        }
    ]
    
    total_records = 0
    
    for pattern in patterns:
        print(f"\n生成模式: {pattern['session']}")
        
        for i in range(pattern['count']):
            tool = random.choice(pattern['tools'])
            
            # 基于模式的延迟
            base_latency = pattern['avg_latency']
            latency = random.uniform(base_latency * 0.5, base_latency * 1.5)
            
            # 基于模式的成功率
            success = random.random() < pattern['success_rate']
            
            # 基于工具的token使用量
            if tool in ["web_search", "web_fetch"]:
                tokens_used = random.randint(1000, 5000)
            elif tool == "message":
                tokens_used = random.randint(500, 2000)
            else:
                tokens_used = random.randint(50, 500)
            
            # 工具特定参数
            if tool == "web_search":
                params = {"query": f"研究主题 {random.randint(1, 10)}"}
            elif tool == "web_fetch":
                params = {"url": f"https://example.com/article_{random.randint(1, 20)}"}
            elif tool in ["read", "write", "edit"]:
                params = {"path": f"/data/file_{random.randint(1, 50)}.md"}
            elif tool == "message":
                params = {"action": "send", "message": f"测试消息 {random.randint(1, 100)}"}
            elif tool == "browser":
                params = {"action": "navigate", "url": "https://deepseek.com"}
            else:
                params = {}
            
            record_metric(
                session_id=pattern['session'],
                agent_id=pattern['session'].split(":")[1],
                tool_name=tool,
                latency_ms=latency,
                success=success,
                tokens_used=tokens_used,
                error_message=None if success else f"{tool}操作失败",
                params=params
            )
            
            total_records += 1
            print(f"  记录: {tool} - {latency:.0f}ms")
    
    print(f"\n✅ 数据生成完成！")
    print(f"总记录数: {total_records}")
    print("数据模式包括:")
    print("  - 网页研究会话 (15条记录)")
    print("  - 文件操作会话 (10条记录)")
    print("  - 消息发送会话 (8条记录)")
    print("  - 浏览器自动化会话 (12条记录)")
    
    return total_records

if __name__ == "__main__":
    print("Agent Observability Dashboard - 数据生成工具")
    print("=" * 50)
    
    print("\n选择操作:")
    print("1. 生成简单示例数据 (50条随机记录)")
    print("2. 生成真实数据模式 (45条模式化记录)")
    print("3. 退出")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        record_example_data()
    elif choice == "2":
        generate_realistic_data()
    else:
        print("退出")
    
    print("\n下一步:")
    print("1. 启动仪表板: python scripts/observability.py --dashboard")
    print("2. 查看报告: python scripts/observability.py --report")
    print("3. 导出数据: python scripts/observability.py --export metrics.csv")