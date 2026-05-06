#!/usr/bin/env python3
"""
AI视频生成提示词优化工具
简化版优化脚本
"""

import re
import argparse
from typing import List, Dict


def analyze_prompt(prompt: str) -> Dict:
    """分析提示词"""
    elements = [e.strip() for e in prompt.split('+') if e.strip()]
    
    stats = {
        "total": len(elements),
        "scenes": 0,
        "characters": 0,
        "actions": 0,
        "dialogues": 0,
        "camera": 0,
        "audio": 0,
        "effects": 0
    }
    
    for elem in elements:
        if any(kw in elem for kw in ["场景", "地点", "背景"]):
            stats["scenes"] += 1
        elif any(kw in elem for kw in ["角色", "人物", "主角"]):
            stats["characters"] += 1
        elif any(kw in elem for kw in ["动作", "运动", "做", "走", "跑"]):
            stats["actions"] += 1
        elif "：" in elem or '"' in elem:
            stats["dialogues"] += 1
        elif "镜头" in elem:
            stats["camera"] += 1
        elif any(kw in elem for kw in ["音效", "音乐", "声音"]):
            stats["audio"] += 1
        elif any(kw in elem for kw in ["特效", "效果", "光效"]):
            stats["effects"] += 1
    
    return stats


def optimize_for_platform(prompt: str, platform: str) -> str:
    """针对平台优化"""
    elements = [e.strip() for e in prompt.split('+') if e.strip()]
    
    if platform == "douyin":
        # 抖音：前3秒钩子，快速节奏
        if not any("快速节奏" in e for e in elements):
            elements.insert(0, "[快速节奏，前3秒视觉钩子]")
        if not any("大字标题" in e for e in elements):
            elements.insert(1, "[大字标题吸引注意力]")
    
    elif platform == "bilibili":
        # B站：玩梗密度，情绪波动
        if not any("玩梗密度" in e for e in elements):
            elements.insert(0, "[高玩梗密度，每30秒情绪变化]")
        if not any("专业解说" in e for e in elements):
            elements.append("[专业解说元素]")
    
    elif platform == "hongguo":
        # 红果：情感引入，柔光效果
        if not any("情感引入" in e for e in elements):
            elements.insert(0, "[前5秒情感引入]")
        if not any("柔光效果" in e for e in elements):
            elements.append("[柔光效果，慢动作]")
    
    return " + ".join(elements)


def check_character_consistency(prompt: str) -> List[str]:
    """检查角色一致性"""
    issues = []
    
    # 提取角色标签
    character_pattern = r'\[([^：]+)[：,]'
    characters = re.findall(character_pattern, prompt)
    
    if not characters:
        issues.append("未找到角色标签")
        return issues
    
    # 检查唯一性
    unique_chars = set(characters)
    if len(characters) != len(unique_chars):
        duplicates = [c for c in characters if characters.count(c) > 1]
        issues.append(f"角色标签重复：{duplicates}")
    
    # 检查对话引用
    dialogue_pattern = r'\[([^：]+)[：,].*?："[^"]*"'
    dialogue_speakers = re.findall(dialogue_pattern, prompt)
    
    for char in unique_chars:
        if char not in dialogue_speakers:
            issues.append(f"角色'{char}'未在对话中出现")
    
    return issues


def add_camera_variety(prompt: str) -> str:
    """增加镜头多样性"""
    elements = [e.strip() for e in prompt.split('+') if e.strip()]
    
    camera_count = sum(1 for e in elements if "镜头" in e)
    
    if camera_count < 2:
        # 添加基础镜头
        camera_options = ["[镜头切换]", "[特写聚焦]", "[缓慢拉近]", "[镜头环绕]"]
        for cam in camera_options[:2]:
            if cam not in " ".join(elements):
                elements.append(cam)
    
    return " + ".join(elements)


def add_audio_elements(prompt: str) -> str:
    """添加音频元素"""
    elements = [e.strip() for e in prompt.split('+') if e.strip()]
    
    has_ambient = any("环境音" in e for e in elements)
    has_music = any("音乐" in e for e in elements)
    has_sound = any("音效" in e for e in elements)
    
    if not has_ambient:
        elements.append("[环境音：基础氛围]")
    
    if not has_music and not has_sound:
        elements.append("[背景音乐：情绪匹配]")
    
    return " + ".join(elements)


def main():
    parser = argparse.ArgumentParser(description="AI视频生成提示词优化器")
    parser.add_argument("input", help="输入提示词文件或直接输入提示词")
    parser.add_argument("--platform", "-p", choices=["douyin", "bilibili", "hongguo", "general"],
                       default="general", help="目标平台")
    parser.add_argument("--output", "-o", help="输出文件")
    
    args = parser.parse_args()
    
    # 读取输入
    try:
        if os.path.exists(args.input):
            with open(args.input, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
        else:
            prompt = args.input
    except:
        prompt = args.input
    
    print("=" * 60)
    print("AI视频生成提示词优化")
    print("=" * 60)
    print(f"原始提示词长度：{len(prompt)} 字符")
    print(f"目标平台：{args.platform}")
    print()
    
    # 分析
    stats = analyze_prompt(prompt)
    print("【元素分析】")
    for key, value in stats.items():
        if key != "total":
            print(f"  {key:8s}：{value:2d}")
    print(f"  总计：{stats['total']} 个元素")
    print()
    
    # 检查角色一致性
    print("【角色检查】")
    char_issues = check_character_consistency(prompt)
    if char_issues:
        for issue in char_issues:
            print(f"  ⚠️ {issue}")
    else:
        print("  ✓ 角色一致性良好")
    print()
    
    # 优化
    optimized = prompt
    
    # 1. 平台优化
    optimized = optimize_for_platform(optimized, args.platform)
    
    # 2. 镜头多样性
    optimized = add_camera_variety(optimized)
    
    # 3. 音频完整性
    optimized = add_audio_elements(optimized)
    
    # 输出结果
    print("【优化完成】")
    print(f"优化后长度：{len(optimized)} 字符")
    print(f"增加元素：{len(optimized.split('+')) - stats['total']} 个")
    print()
    
    # 保存结果
    output_path = args.output or f"optimized_{args.platform}_prompt.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(optimized)
    
    print(f"结果已保存到：{output_path}")
    print()
    
    # 显示优化后提示词（前200字符）
    print("【优化后提示词预览】")
    preview = optimized[:200] + ("..." if len(optimized) > 200 else "")
    print(preview)
    print()
    
    # 平台特定建议
    print("【平台建议】")
    if args.platform == "douyin":
        print("• 前3秒必须有强烈视觉冲击")
        print("• 使用大字标题和快速切换")
        print("• 保持高节奏，避免冗长")
    elif args.platform == "bilibili":
        print("• 增加玩梗密度和专业知识")
        print("• 每30秒要有情绪或节奏变化")
        print("• 可以加入解说或评论元素")
    elif args.platform == "hongguo":
        print("• 前5秒情感引入很重要")
        print("• 使用柔光效果和慢动作")
        print("• 注重情感发展和内心戏")
    else:
        print("• 保持结构完整均衡")
        print("• 确保所有必要元素齐全")
        print("• 测试不同版本效果")
    
    print("=" * 60)


if __name__ == "__main__":
    import os
    main()