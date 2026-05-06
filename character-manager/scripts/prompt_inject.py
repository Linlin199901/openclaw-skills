#!/usr/bin/env python3
"""
角色锚点注入脚本
用法: python prompt_inject.py <角色yaml> <分镜文件> [--output <输出文件>]

将角色7维锚点自动注入到分镜/视频 prompt 的指定位置。
"""

import sys
import os
import yaml
import glob
import re
import io

# Windows GBK 编码兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_character(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def detect_shot_type(content):
    """检测镜头类型"""
    content_lower = content.lower()
    if any(w in content_lower for w in ['特写', 'close-up', 'closeup']):
        return 'closeup'
    if any(w in content_lower for w in ['全景', 'wide', 'full shot', '全身']):
        return 'wide'
    return 'medium'  # 默认中景

def detect_angle(content):
    """检测镜头角度"""
    if any(w in content for w in ['侧面', '侧脸', 'profile', 'side']):
        return 'side'
    if any(w in content for w in ['背面', '背后', 'back', 'rear']):
        return 'back'
    return 'front'

def build_face_block(face, shot_type, angle):
    """根据镜头类型和角度构建面部描述块"""
    lines = []
    
    face_type = face.get('脸型', '')
    face_detail = face.get('脸型细节', '')
    if face_type:
        fdesc = face_type + ('，' + face_detail if face_detail else '')
        lines.append(f"脸型：{fdesc}")
    
    eyes = face.get('眼睛', {})
    if isinstance(eyes, dict):
        eye_parts = []
        if eyes.get('类型'): eye_parts.append(eyes['类型'])
        if eyes.get('虹膜颜色'): eye_parts.append(eyes['虹膜颜色'] + '虹膜')
        if eyes.get('双眼皮'): eye_parts.append('双眼皮' + eyes['双眼皮'])
        if eye_parts:
            lines.append(f"眼睛：{'，'.join(eye_parts)}")
    
    brows = face.get('眉毛', {})
    if isinstance(brows, dict):
        b_parts = []
        if brows.get('类型'): b_parts.append(brows['类型'])
        if brows.get('颜色'): b_parts.append(brows['颜色'])
        if b_parts:
            lines.append(f"眉毛：{'，'.join(b_parts)}")
    
    nose = face.get('鼻子', {})
    if isinstance(nose, dict):
        n_parts = []
        if nose.get('鼻梁'): n_parts.append('鼻梁' + nose['鼻梁'])
        if nose.get('鼻头'): n_parts.append('鼻头' + nose['鼻头'])
        if n_parts:
            lines.append(f"鼻子：{'，'.join(n_parts)}")
    
    lips = face.get('嘴唇', {})
    if isinstance(lips, dict):
        l_parts = []
        if lips.get('唇色'): l_parts.append(lips['唇色'])
        if l_parts:
            lines.append(f"嘴唇：{'，'.join(l_parts)}")
    
    skin = face.get('肤色', {})
    if isinstance(skin, dict):
        s_parts = []
        if skin.get('色调'): s_parts.append(skin['色调'])
        if skin.get('质感'): s_parts.append(skin['质感'])
        if s_parts:
            lines.append(f"皮肤：{'，'.join(s_parts)}")
    
    hair = face.get('发型', {})
    if isinstance(hair, dict):
        h_parts = []
        if hair.get('长度'): h_parts.append(hair['长度'])
        if hair.get('颜色'): h_parts.append(hair['颜色'])
        if hair.get('样式'): h_parts.append(hair['样式'])
        if hair.get('分线'): h_parts.append(hair['分线'])
        if hair.get('刘海'): h_parts.append(hair['刘海'])
        if h_parts:
            lines.append(f"发型：{'，'.join(h_parts)}")
    
    # 识别特征（侧面角度额外强调）
    ident = face.get('识别特征', '')
    if ident:
        lines.append(f"识别特征：{ident}")
    
    return '，'.join(lines)

def build_body_block(body, shot_type):
    """构建身体描述块"""
    parts = []
    if body.get('身高'):
        parts.append(f"身高{body['身高']}cm")
    if body.get('头身比'):
        parts.append(f"{body['头身比']}")
    if body.get('骨架类型'):
        parts.append(body['骨架类型'])
    return '，'.join(parts)

def build_costume_block(costume, scene='日常'):
    """构建服饰描述块"""
    lines = []
    
    # 核心锚物（最高优先级）
    anchor = costume.get('核心锚物', {})
    if anchor.get('名称'):
        loc = anchor.get('位置', '')
        desc = anchor.get('描述', '')
        lines.append(f"{loc}{anchor['名称']}（{desc}）")
    
    # 场景服饰
    scene_costume = costume.get('场景服饰', {})
    if isinstance(scene_costume, dict):
        outfit = scene_costume.get(scene + '装', '') or scene_costume.get('日常装', '')
        if outfit:
            lines.append(outfit)
    
    return '，'.join(lines) if lines else ''

def inject_character(char, scene_text, shot_type=None, angle=None, scene='日常'):
    """将角色锚点注入到场景文本"""
    
    if shot_type is None:
        shot_type = detect_shot_type(scene_text)
    if angle is None:
        angle = detect_angle(scene_text)
    
    face = char.get('面部', {})
    body = char.get('身体', {})
    costume = char.get('服饰', {})
    posture = char.get('体态', {})
    
    char_name = char.get('角色', {}).get('姓名', '')
    
    face_block = build_face_block(face, shot_type, angle)
    body_block = build_body_block(body, shot_type)
    costume_block = build_costume_block(costume, scene)
    posture_block = posture.get('AI翻译', '')
    
    # 构建注入块
    injection = f"\n\n【{char_name}-视觉锚点-{shot_type}/{angle}】\n"
    if face_block:
        injection += f"面部：{face_block}\n"
    if body_block:
        injection += f"体态：{body_block}\n"
    if posture_block:
        injection += f"姿态：{posture_block}\n"
    if costume_block:
        injection += f"服饰：{costume_block}\n"
    
    # 检查是否已有注入标记（避免重复注入）
    if '【' + char_name + '-视觉锚点' in scene_text:
        # 替换已有注入
        pattern = r'\n\n【' + re.escape(char_name) + r'-视觉锚点[^】]*】.*?(?=\n\n---|\n\n【|\Z)'
        scene_text = re.sub(pattern, injection, scene_text, flags=re.DOTALL)
    else:
        # 在文件末尾追加
        scene_text = scene_text.rstrip() + injection
    
    return scene_text

def main():
    if len(sys.argv) < 3:
        print("用法: python prompt_inject.py <角色yaml> <分镜文件>... [--output <目录>]")
        print("示例: python prompt_inject.py 苏清雪.yaml scene_15.md --output injected/")
        sys.exit(1)
    
    char_path = sys.argv[1]
    args = sys.argv[2:]
    
    output_dir = None
    scene_paths = []
    
    i = 0
    while i < len(args):
        if args[i] == '--output' and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        else:
            scene_paths.append(args[i])
            i += 1
    
    char = load_character(char_path)
    char_name = char.get('角色', {}).get('姓名', os.path.basename(char_path))
    
    # 收集文件
    files = []
    for p in scene_paths:
        if os.path.isfile(p):
            files.append(p)
        elif os.path.isdir(p):
            for ext in ('*.md', '*.txt'):
                files.extend(glob.glob(os.path.join(p, '**', ext), recursive=True))
    
    files = sorted(set(files))
    
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = inject_character(char, content)
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            out_path = os.path.join(output_dir, os.path.basename(fp))
        else:
            out_path = fp
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"✅ {os.path.basename(fp)} → {out_path}")
    
    print(f"\n完成: {len(files)} 个文件已注入 '{char_name}' 角色锚点")

if __name__ == '__main__':
    main()
