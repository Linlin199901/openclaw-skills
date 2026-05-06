#!/usr/bin/env python3
"""
精准视频提示词转换脚本
将剧本严格转换为标准化视频生成提示词
确保完全忠实于原始内容，减少AI误解
"""

import re
import json
import argparse
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class ScriptElement:
    """剧本元素基类"""
    type: str
    content: str
    line_num: int
    
    def to_prompt_element(self) -> str:
        """转换为提示词元素"""
        raise NotImplementedError


@dataclass
class SceneElement(ScriptElement):
    """场景元素"""
    location: str
    time: str
    atmosphere: str
    
    def to_prompt_element(self) -> str:
        return f"[场景：{self.location}，{self.time}，{self.atmosphere}]"


@dataclass
class CharacterElement(ScriptElement):
    """角色元素"""
    name: str
    description: str
    position: str
    
    def to_prompt_element(self) -> str:
        return f"[角色：{self.name}，{self.description}，{self.position}]"


@dataclass
class ActionElement(ScriptElement):
    """动作元素"""
    character: str
    action: str
    intensity: str = ""
    
    def to_prompt_element(self) -> str:
        if self.intensity:
            return f"[动作：{self.character}{self.intensity}{self.action}]"
        return f"[动作：{self.character}{self.action}]"


@dataclass
class DialogueElement(ScriptElement):
    """对话元素"""
    speaker: str
    emotion: str
    text: str
    
    def to_prompt_element(self) -> str:
        return f'[对话：{self.speaker}，{self.emotion}]："{self.text}"'


@dataclass
class CameraElement(ScriptElement):
    """镜头元素"""
    shot_type: str
    target: str
    movement: str = ""
    
    def to_prompt_element(self) -> str:
        if self.movement:
            return f"[镜头：{self.shot_type}，{self.target}，{self.movement}]"
        return f"[镜头：{self.shot_type}，{self.target}]"


@dataclass
class AudioElement(ScriptElement):
    """音频元素"""
    audio_type: str
    description: str
    volume: str = "正常"
    
    def to_prompt_element(self) -> str:
        return f"[音频：{self.audio_type}，{self.description}，音量{self.volume}]"


@dataclass
class EffectElement(ScriptElement):
    """特效元素"""
    effect_type: str
    description: str
    intensity: str = "中等"
    
    def to_prompt_element(self) -> str:
        return f"[特效：{self.effect_type}，{self.description}，强度{self.intensity}]"


class PreciseConverter:
    """精准转换器"""
    
    def __init__(self):
        self.elements = []
        self.characters = {}  # 角色注册表
        self.current_scene = None
        
    def parse_script(self, script_text: str) -> List[ScriptElement]:
        """解析剧本文本"""
        lines = script_text.strip().split('\n')
        self.elements = []
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            element = self._parse_line(line, i)
            if element:
                self.elements.append(element)
        
        return self.elements
    
    def _parse_line(self, line: str, line_num: int) -> ScriptElement:
        """解析单行剧本"""
        line_lower = line.lower()
        
        # 场景检测
        if line.startswith("场景：") or "场景：" in line:
            return self._parse_scene(line, line_num)
        
        # 角色检测
        elif line.startswith("角色：") or "角色：" in line:
            return self._parse_character(line, line_num)
        
        # 动作检测
        elif any(keyword in line_lower for keyword in ["动作", "做", "走", "跑", "跳", "敲", "打", "拿"]):
            return self._parse_action(line, line_num)
        
        # 对话检测
        elif "：" in line and "说" in line_lower:
            return self._parse_dialogue(line, line_num)
        elif "：" in line and any(keyword in line_lower for keyword in ["道", "问", "答", "喊", "叫"]):
            return self._parse_dialogue(line, line_num)
        
        # 镜头检测（分镜）
        elif any(keyword in line_lower for keyword in ["镜头", "特写", "全景", "中景", "近景", "远景"]):
            return self._parse_camera(line, line_num)
        
        # 音频检测
        elif any(keyword in line_lower for keyword in ["音效", "音乐", "声音", "音频", "响起", "播放"]):
            return self._parse_audio(line, line_num)
        
        # 特效检测
        elif any(keyword in line_lower for keyword in ["特效", "效果", "光效", "闪烁", "发光", "爆炸"]):
            return self._parse_effect(line, line_num)
        
        # 默认作为描述性文本
        else:
            return self._parse_description(line, line_num)
    
    def _parse_scene(self, line: str, line_num: int) -> SceneElement:
        """解析场景"""
        # 提取场景描述
        if "场景：" in line:
            scene_desc = line.split("场景：", 1)[1].strip()
        else:
            scene_desc = line
        
        # 简单解析地点、时间、氛围
        parts = scene_desc.split("，")
        location = parts[0] if len(parts) > 0 else "未知地点"
        time = parts[1] if len(parts) > 1 else "未知时间"
        atmosphere = parts[2] if len(parts) > 2 else "普通氛围"
        
        element = SceneElement(
            type="scene",
            content=scene_desc,
            line_num=line_num,
            location=location,
            time=time,
            atmosphere=atmosphere
        )
        
        self.current_scene = element
        return element
    
    def _parse_character(self, line: str, line_num: int) -> CharacterElement:
        """解析角色"""
        if "角色：" in line:
            char_desc = line.split("角色：", 1)[1].strip()
        else:
            char_desc = line
        
        # 提取角色名
        name_match = re.search(r'^([^，]+)', char_desc)
        name = name_match.group(1) if name_match else "未知角色"
        
        # 提取描述和位置
        parts = char_desc.split("，")
        description = parts[1] if len(parts) > 1 else "无描述"
        position = parts[2] if len(parts) > 2 else "未知位置"
        
        # 注册角色
        self.characters[name] = {
            "description": description,
            "position": position
        }
        
        return CharacterElement(
            type="character",
            content=char_desc,
            line_num=line_num,
            name=name,
            description=description,
            position=position
        )
    
    def _parse_action(self, line: str, line_num: int) -> ActionElement:
        """解析动作"""
        # 尝试提取角色名
        character = "未知角色"
        for char_name in self.characters.keys():
            if char_name in line:
                character = char_name
                break
        
        # 提取动作描述
        action_desc = line
        
        # 检测强度副词
        intensity = ""
        intensity_words = ["快速", "缓慢", "猛烈", "轻轻", "突然", "慢慢"]
        for word in intensity_words:
            if word in action_desc:
                intensity = word
                break
        
        return ActionElement(
            type="action",
            content=action_desc,
            line_num=line_num,
            character=character,
            action=action_desc.replace(character, "").strip(),
            intensity=intensity
        )
    
    def _parse_dialogue(self, line: str, line_num: int) -> DialogueElement:
        """解析对话"""
        # 分割说话者和内容
        if "：" in line:
            speaker_part, text_part = line.split("：", 1)
        else:
            speaker_part, text_part = line, ""
        
        # 提取说话者
        speaker = speaker_part.strip()
        
        # 清理说话者中的"说"等词
        speaker = re.sub(r'[说问道答喊叫]', '', speaker).strip()
        
        # 提取情感
        emotion = "正常"
        emotion_words = {
            "愤怒": ["生气", "愤怒", "发火"],
            "悲伤": ["伤心", "哭泣", "难过"],
            "欢乐": ["开心", "高兴", "大笑"],
            "疑惑": ["疑惑", "奇怪", "不解"],
            "紧张": ["紧张", "害怕", "惊恐"]
        }
        
        for emo, keywords in emotion_words.items():
            if any(keyword in text_part for keyword in keywords):
                emotion = emo
                break
        
        # 清理文本中的引号
        text = text_part.strip().strip('"').strip("'")
        
        return DialogueElement(
            type="dialogue",
            content=line,
            line_num=line_num,
            speaker=speaker,
            emotion=emotion,
            text=text
        )
    
    def _parse_camera(self, line: str, line_num: int) -> CameraElement:
        """解析镜头"""
        # 常见镜头类型
        shot_types = ["特写", "全景", "中景", "近景", "远景", "过肩", "俯视", "仰视"]
        
        shot_type = "未知镜头"
        for st in shot_types:
            if st in line:
                shot_type = st
                break
        
        # 提取目标
        target = "未知目标"
        for char_name in self.characters.keys():
            if char_name in line:
                target = char_name
                break
        
        # 检测运动
        movement = ""
        movement_words = ["推近", "拉远", "平移", "旋转", "跟随", "固定"]
        for word in movement_words:
            if word in line:
                movement = word
                break
        
        return CameraElement(
            type="camera",
            content=line,
            line_num=line_num,
            shot_type=shot_type,
            target=target,
            movement=movement
        )
    
    def _parse_audio(self, line: str, line_num: int) -> AudioElement:
        """解析音频"""
        audio_type = "音效"
        if "音乐" in line:
            audio_type = "音乐"
        elif "对话" in line:
            audio_type = "对话"
        elif "环境音" in line:
            audio_type = "环境音"
        
        description = line
        
        return AudioElement(
            type="audio",
            content=line,
            line_num=line_num,
            audio_type=audio_type,
            description=description
        )
    
    def _parse_effect(self, line: str, line_num: int) -> EffectElement:
        """解析特效"""
        effect_type = "光效"
        if "爆炸" in line:
            effect_type = "爆炸"
        elif "粒子" in line:
            effect_type = "粒子"
        elif "烟雾" in line:
            effect_type = "烟雾"
        
        description = line
        
        return EffectElement(
            type="effect",
            content=line,
            line_num=line_num,
            effect_type=effect_type,
            description=description
        )
    
    def _parse_description(self, line: str, line_num: int) -> ActionElement:
        """解析描述性文本为动作"""
        # 默认作为描述性动作
        return ActionElement(
            type="action",
            content=line,
            line_num=line_num,
            character="场景",
            action=line
        )
    
    def convert_to_prompt(self, platform: str = "general") -> str:
        """转换为提示词"""
        prompt_elements = []
        
        for element in self.elements:
            prompt_elements.append(element.to_prompt_element())
        
        # 添加平台优化
        if platform == "jimeng":
            prompt_elements.append("[即梦优化：清晰指令，减少误解]")
        elif platform == "keling":
            prompt_elements.append("[可灵优化：精确描述，忠实原作]")
        else:
            prompt_elements.append("[通用优化：标准化结构]")
        
        return " + ".join(prompt_elements)
    
    def generate_report(self) -> Dict:
        """生成转换报告"""
        element_counts = {}
        for element in self.elements:
            element_counts[element.type] = element_counts.get(element.type, 0) + 1
        
        return {
            "total_elements": len(self.elements),
            "element_counts": element_counts,
            "characters": list(self.characters.keys()),
            "scenes": 1 if self.current_scene else 0,
            "conversion_quality": self._assess_quality()
        }
    
    def _assess_quality(self) -> str:
        """评估转换质量"""
        if len(self.elements) == 0:
            return "空剧本"
        
        # 检查必要元素
        has_scene = any(e.type == "scene" for e in self.elements)
        has_character = any(e.type == "character" for e in self.elements)
        has_action = any(e.type == "action" for e in self.elements)
        
        if not has_scene:
            return "缺少场景描述"
        elif not has_character:
            return "缺少角色描述"
        elif not has_action:
            return "缺少动作描述"
        
        return "良好"


def main():
    parser = argparse.ArgumentParser(description="精准视频提示词转换器")
    parser.add_argument("input", help="输入剧本文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--platform", "-p", choices=["jimeng", "keling", "general"], 
                       default="general", help="目标平台")
    parser.add_argument("--report", "-r", action="store_true", help="生成详细报告")
    
    args = parser.parse_args()
    
    try:
        # 读取剧本
        with open(args.input, 'r', encoding='utf-8') as f:
            script_text = f.read()
        
        # 转换
        converter = PreciseConverter()
        elements = converter.parse_script(script_text)
        prompt = converter.convert_to_prompt(args.platform)
        report = converter.generate_report()
        
        # 输出结果
        output_path = args.output or f"转换后_{args.platform}_提示词.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print("=" * 60)
        print("精准视频提示词转换完成")
        print("=" * 60)
        print(f"输入文件：{args.input}")
        print(f"输出文件：{output_path}")
        print(f"目标平台：{args.platform}")
        print()
        
        # 显示报告
        print("【转换报告】")
        print(f"总元素数：{report['total_elements']}")
        print("元素分布：")
        for elem_type, count in report['element_counts'].items():
            print(f"  {elem_type:10s}：{count:3d} 个")
        print(f"角色列表：{', '.join(report['characters'])}")
        print(f"转换质量：{report['conversion_quality']}")
        print()
        
        # 显示提示词预览
        print("【生成的提示词】")
        print(prompt[:200] + ("..." if len(prompt) > 200 else ""))
        print()
        
        # 详细报告
        if args.report:
            report_path = output_path.replace(".txt", "_报告.json")
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"详细报告已保存到：{report_path}")
        
        print("=" * 60)
        
        return 0
    
    except Exception as e:
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())