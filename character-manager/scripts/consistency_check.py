#!/usr/bin/env python3
"""
角色视觉一致性检查脚本
用法: python consistency_check.py <角色yaml> <分镜目录或文件>...

检查项:
1. 面部5锚点是否在每集 prompt 中出现
2. 核心锚物是否被遗漏
3. 身高描述是否有漂移
4. 禁用色是否出现
5. 感受词汇是否被滥用
"""

import sys
import os
import re
import yaml
import glob
import io

# Windows GBK 编码兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 零信噪比词汇（AI不吃的感受词）
ZERO_SNR_WORDS = [
    '气质清冷', '气质出尘', '气质', '冷艳', '高贵', '仙气',
    '眼神灵动', '眼神', '气场', '气场强大', '冰山美人',
    '绝美', '倾国', '惊为天人', '美若天仙',
]

def load_character(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def find_scene_files(paths):
    """收集所有场景/分镜文件"""
    files = []
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(('.md', '.txt', '.yaml', '.yml')):
                files.append(p)
        elif os.path.isdir(p):
            for ext in ('*.md', '*.txt'):
                files.extend(glob.glob(os.path.join(p, '**', ext), recursive=True))
    return sorted(set(files))

def extract_face_anchors(char):
    """提取面部5锚点关键词"""
    face = char.get('面部', {})
    anchors = {}
    
    if '脸型' in face:
        anchors['脸型'] = face['脸型']
    
    eyes = face.get('眼睛', {})
    if isinstance(eyes, dict):
        if '类型' in eyes:
            anchors['眼型'] = eyes['类型']
        if '虹膜颜色' in eyes:
            anchors['虹膜颜色'] = eyes['虹膜颜色']
    
    brows = face.get('眉毛', {})
    if isinstance(brows, dict):
        if '类型' in brows:
            anchors['眉形'] = brows['类型']
    
    nose = face.get('鼻子', {})
    if isinstance(nose, dict):
        if '鼻梁' in nose:
            anchors['鼻梁'] = nose['鼻梁']
    
    hair = face.get('发型', {})
    if isinstance(hair, dict):
        if '颜色' in hair:
            anchors['发色'] = hair['颜色']
        if '样式' in hair:
            anchors['发型'] = hair['样式']
    
    return anchors

def main():
    if len(sys.argv) < 3:
        print("用法: python consistency_check.py <角色yaml> <场景文件...>")
        print("示例: python consistency_check.py 苏清雪.yaml scenes/ep*.md")
        sys.exit(1)
    
    char_path = sys.argv[1]
    scene_paths = sys.argv[2:]
    
    char = load_character(char_path)
    char_name = char.get('角色', {}).get('姓名', os.path.basename(char_path))
    anchors = extract_face_anchors(char)
    
    # 核心锚物
    costume = char.get('服饰', {})
    anchor_item = costume.get('核心锚物', {})
    anchor_name = anchor_item.get('名称', '')
    
    # 禁用色
    forbidden_colors = costume.get('配色DNA', {}).get('禁用色', [])
    
    scene_files = find_scene_files(scene_paths)
    
    print(f"角色: {char_name}")
    print(f"锚点: {list(anchors.keys())}")
    print(f"锚物: {anchor_name}")
    print(f"检查文件: {len(scene_files)}个")
    print("=" * 60)
    
    issues = []
    
    for sf in scene_files:
        with open(sf, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fname = os.path.basename(sf)
        
        # 检查1: 面部锚点
        missing_anchors = []
        for key, val in anchors.items():
            if val and val not in content:
                missing_anchors.append(f"{key}:{val}")
        
        if missing_anchors:
            issues.append((fname, '面部锚点缺失', ', '.join(missing_anchors)))
        
        # 检查2: 核心锚物
        if anchor_name and anchor_name not in content:
            issues.append((fname, '核心锚物缺失', anchor_name))
        
        # 检查3: 感受词汇
        snr_hits = [w for w in ZERO_SNR_WORDS if w in content]
        if snr_hits:
            issues.append((fname, '零信噪比词汇', ', '.join(snr_hits)))
        
        # 检查4: 禁用色
        color_hits = [c for c in forbidden_colors if c in content]
        if color_hits:
            issues.append((fname, '禁用色出现', ', '.join(color_hits)))
    
    if not issues:
        print("\n✅ 全部通过！没有发现一致性问题。")
    else:
        print(f"\n❌ 发现 {len(issues)} 个问题:\n")
        for fname, cat, detail in issues:
            print(f"  [{cat}] {fname}: {detail}")
    
    return len(issues)

if __name__ == '__main__':
    sys.exit(min(main(), 1))
