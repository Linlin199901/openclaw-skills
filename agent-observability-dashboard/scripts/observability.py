#!/usr/bin/env python3
"""
Agent Observability Dashboard
统一的可观测性工具，用于监控OpenClaw代理的性能指标、追踪和洞察
"""

import json
import sqlite3
import argparse
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

# 创建Flask应用
app = Flask(__name__)

# 数据库初始化
def init_db():
    """初始化SQLite数据库"""
    conn = sqlite3.connect('agent_metrics.db')
    cursor = conn.cursor()
    
    # 创建指标表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        session_id TEXT,
        agent_id TEXT,
        tool_name TEXT,
        latency_ms REAL,
        success INTEGER,
        tokens_used INTEGER,
        error_message TEXT,
        params TEXT
    )
    ''')
    
    # 创建会话表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        agent_id TEXT,
        start_time DATETIME,
        end_time DATETIME,
        total_tokens INTEGER DEFAULT 0,
        success_rate REAL DEFAULT 0.0,
        avg_latency_ms REAL DEFAULT 0.0
    )
    ''')
    
    conn.commit()
    conn.close()
    print("数据库初始化完成")

def record_metric(session_id, agent_id, tool_name, latency_ms, success, tokens_used=0, error_message=None, params=None):
    """记录指标到数据库"""
    conn = sqlite3.connect('agent_metrics.db')
    cursor = conn.cursor()
    
    params_json = json.dumps(params) if params else None
    
    cursor.execute('''
    INSERT INTO metrics (session_id, agent_id, tool_name, latency_ms, success, tokens_used, error_message, params)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session_id, agent_id, tool_name, latency_ms, 1 if success else 0, tokens_used, error_message, params_json))
    
    conn.commit()
    conn.close()
    print(f"记录指标: {tool_name} - 延迟: {latency_ms}ms - 成功: {success}")

def get_session_trace(session_id):
    """获取会话追踪"""
    conn = sqlite3.connect('agent_metrics.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT timestamp, tool_name, params, latency_ms, success, tokens_used, error_message
    FROM metrics
    WHERE session_id = ?
    ORDER BY timestamp
    ''', (session_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    trace = []
    for row in rows:
        trace.append({
            'timestamp': row[0],
            'tool': row[1],
            'params': json.loads(row[2]) if row[2] else {},
            'latency_ms': row[3],
            'success': bool(row[4]),
            'tokens_used': row[5],
            'error': row[6]
        })
    
    return {
        'session_id': session_id,
        'trace': trace,
        'total_calls': len(trace),
        'success_rate': sum(1 for t in trace if t['success']) / len(trace) if trace else 0,
        'avg_latency': sum(t['latency_ms'] for t in trace) / len(trace) if trace else 0
    }

def get_performance_report(period_hours=24):
    """获取性能报告"""
    conn = sqlite3.connect('agent_metrics.db')
    
    # 计算时间范围
    time_threshold = datetime.now() - timedelta(hours=period_hours)
    
    # 总体统计
    df = pd.read_sql_query(f'''
    SELECT 
        tool_name,
        COUNT(*) as call_count,
        AVG(latency_ms) as avg_latency,
        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
        SUM(tokens_used) as total_tokens
    FROM metrics
    WHERE timestamp >= '{time_threshold.strftime("%Y-%m-%d %H:%M:%S")}'
    GROUP BY tool_name
    ORDER BY call_count DESC
    ''', conn)
    
    # 时间序列数据
    time_series = pd.read_sql_query(f'''
    SELECT 
        strftime('%Y-%m-%d %H:00', timestamp) as hour,
        COUNT(*) as call_count,
        AVG(latency_ms) as avg_latency,
        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate
    FROM metrics
    WHERE timestamp >= '{time_threshold.strftime("%Y-%m-%d %H:%M:%S")}'
    GROUP BY hour
    ORDER BY hour
    ''', conn)
    
    conn.close()
    
    return {
        'period_hours': period_hours,
        'tool_stats': df.to_dict('records'),
        'time_series': time_series.to_dict('records'),
        'summary': {
            'total_calls': int(df['call_count'].sum()),
            'overall_success_rate': float(df['success_rate'].mean()) if not df.empty else 0,
            'avg_latency': float(df['avg_latency'].mean()) if not df.empty else 0,
            'total_tokens': int(df['total_tokens'].sum())
        }
    }

def export_to_csv(filename='agent_metrics.csv'):
    """导出数据到CSV"""
    conn = sqlite3.connect('agent_metrics.db')
    df = pd.read_sql_query('SELECT * FROM metrics', conn)
    conn.close()
    
    df.to_csv(filename, index=False)
    print(f"数据已导出到: {filename}")
    return filename

def set_alert_threshold(metric, threshold):
    """设置警报阈值"""
    # 这里可以集成到通知系统
    print(f"设置警报: {metric} 阈值 = {threshold}")
    return {
        'metric': metric,
        'threshold': threshold,
        'status': 'active'
    }

# Flask路由
@app.route('/')
def dashboard():
    """仪表板主页"""
    return render_template('dashboard.html')

@app.route('/api/metrics')
def api_metrics():
    """获取指标数据API"""
    period = request.args.get('period', '24')
    report = get_performance_report(int(period))
    return jsonify(report)

@app.route('/api/trace/<session_id>')
def api_trace(session_id):
    """获取会话追踪API"""
    trace = get_session_trace(session_id)
    return jsonify(trace)

@app.route('/api/record', methods=['POST'])
def api_record():
    """记录指标API"""
    data = request.json
    record_metric(
        session_id=data.get('session_id', 'unknown'),
        agent_id=data.get('agent_id', 'main'),
        tool_name=data.get('tool_name', 'unknown'),
        latency_ms=data.get('latency_ms', 0),
        success=data.get('success', True),
        tokens_used=data.get('tokens_used', 0),
        error_message=data.get('error_message'),
        params=data.get('params')
    )
    return jsonify({'status': 'success'})

@app.route('/api/export')
def api_export():
    """导出数据API"""
    filename = export_to_csv()
    return jsonify({'filename': filename, 'status': 'success'})

# 命令行接口
def main():
    parser = argparse.ArgumentParser(description='Agent Observability Dashboard')
    parser.add_argument('--dashboard', action='store_true', help='启动仪表板服务器')
    parser.add_argument('--record', action='store_true', help='记录指标')
    parser.add_argument('--session', type=str, help='会话ID')
    parser.add_argument('--agent', type=str, default='main', help='代理ID')
    parser.add_argument('--tool', type=str, help='工具名称')
    parser.add_argument('--latency', type=float, help='延迟(毫秒)')
    parser.add_argument('--success', type=bool, help='是否成功')
    parser.add_argument('--tokens', type=int, default=0, help='使用的token数量')
    parser.add_argument('--trace', action='store_true', help='查看会话追踪')
    parser.add_argument('--report', action='store_true', help='获取性能报告')
    parser.add_argument('--period', type=int, default=24, help='报告周期(小时)')
    parser.add_argument('--export', type=str, help='导出到CSV文件')
    parser.add_argument('--alert', action='store_true', help='设置警报阈值')
    parser.add_argument('--metric', type=str, help='指标名称')
    parser.add_argument('--threshold', type=float, help='阈值')
    
    args = parser.parse_args()
    
    # 初始化数据库
    init_db()
    
    if args.dashboard:
        # 创建HTML模板目录
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        os.makedirs(templates_dir, exist_ok=True)
        
        # 创建简单的仪表板HTML
        dashboard_html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Agent Observability Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .card { background: #f5f5f5; padding: 20px; border-radius: 8px; }
                h1 { color: #333; }
                .metric { margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>🤖 Agent Observability Dashboard</h1>
            <div class="dashboard">
                <div class="card">
                    <h2>📊 总体统计</h2>
                    <div id="summary"></div>
                </div>
                <div class="card">
                    <h2>📈 性能趋势</h2>
                    <canvas id="latencyChart"></canvas>
                </div>
                <div class="card">
                    <h2>✅ 成功率</h2>
                    <canvas id="successChart"></canvas>
                </div>
                <div class="card">
                    <h2>🛠️ 工具使用</h2>
                    <div id="tools"></div>
                </div>
            </div>
            
            <script>
                async function loadData() {
                    const response = await fetch('/api/metrics?period=24');
                    const data = await response.json();
                    
                    // 更新总体统计
                    document.getElementById('summary').innerHTML = `
                        <div class="metric">总调用次数: ${data.summary.total_calls}</div>
                        <div class="metric">平均成功率: ${data.summary.overall_success_rate.toFixed(1)}%</div>
                        <div class="metric">平均延迟: ${data.summary.avg_latency.toFixed(1)}ms</div>
                        <div class="metric">总Token数: ${data.summary.total_tokens}</div>
                    `;
                    
                    // 更新工具使用
                    let toolsHtml = '<ul>';
                    data.tool_stats.forEach(tool => {
                        toolsHtml += `<li>${tool.tool_name}: ${tool.call_count}次调用 (${tool.success_rate.toFixed(1)}% 成功率)</li>`;
                    });
                    toolsHtml += '</ul>';
                    document.getElementById('tools').innerHTML = toolsHtml;
                    
                    // 创建图表
                    createCharts(data.time_series);
                }
                
                function createCharts(timeSeries) {
                    const labels = timeSeries.map(item => item.hour);
                    const latencyData = timeSeries.map(item => item.avg_latency);
                    const successData = timeSeries.map(item => item.success_rate);
                    
                    // 延迟图表
                    new Chart(document.getElementById('latencyChart'), {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: '平均延迟 (ms)',
                                data: latencyData,
                                borderColor: 'rgb(75, 192, 192)',
                                tension: 0.1
                            }]
                        }
                    });
                    
                    // 成功率图表
                    new Chart(document.getElementById('successChart'), {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: '成功率 (%)',
                                data: successData,
                                backgroundColor: 'rgb(54, 162, 235)'
                            }]
                        }
                    });
                }
                
                // 每30秒刷新数据
                loadData();
                setInterval(loadData, 30000);
            </script>
        </body>
        </html>
        '''
        
        # 写入HTML文件
        with open(os.path.join(templates_dir, 'dashboard.html'), 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        print("启动Agent Observability Dashboard...")
        print("访问地址: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.record and args.session and args.tool and args.latency is not None:
        # 记录指标
        record_metric(
            session_id=args.session,
            agent_id=args.agent,
            tool_name=args.tool,
            latency_ms=args.latency,
            success=args.success if args.success is not None else True,
            tokens_used=args.tokens
        )
        print("指标记录成功")
    
    elif args.trace and args.session:
        # 查看追踪
        trace = get_session_trace(args.session)
        print(json.dumps(trace, indent=2, ensure_ascii=False))
    
    elif args.report:
        # 获取报告
        report = get_performance_report(args.period)
        print("性能报告:")
        print(f"时间段: 最近{args.period}小时")
        print(f"总调用次数: {report['summary']['total_calls']}")
        print(f"总体成功率: {report['summary']['overall_success_rate']:.1f}%")
        print(f"平均延迟: {report['summary']['avg_latency']:.1f}ms")
        print(f"总Token数: {report['summary']['total_tokens']}")
        
        print("\n工具统计:")
        for tool in report['tool_stats']:
            print(f"  {tool['tool_name']}: {tool['call_count']}次调用, {tool['success_rate']:.1f}% 成功率")
    
    elif args.export:
        # 导出数据
        filename = export_to_csv(args.export)
        print(f"数据已导出到: {filename}")
    
    elif args.alert and args.metric and args.threshold:
        # 设置警报
        alert = set_alert_threshold(args.metric, args.threshold)
        print(f"警报设置: {alert}")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()