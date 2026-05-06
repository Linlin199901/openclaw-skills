#!/usr/bin/env python3
"""
AI视频生成提示词生成脚本
将剧本文本转化为结构化视频生成提示词
"""

import re
import json
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class Character:
    """角色信息"""
    name: str
    label: str  # 提示词中使用的标签
    appearance: str
    voice_traits: str
    special_effects: List[str]


@dataclass
class Scene:
    """场景信息"""
    description: str
    location: str
    time: str
    mood: str
    environment_sounds: List[str]


@dataclass
class Action:
    """动作信息"""
    character_label: str
    action_description: str
    intensity: str  # 快速、缓慢、剧烈等
    camera_angle: str


@dataclass
class Dialogue:
    """对话信息"""
    character_label: str
    text: str
    emotion: str
    voice_traits: str
    timing: Optional[str] = None  # 紧接着、随后等


@dataclass
class AudioElement:
    """音频元素"""
    type: str  # dialogue, music, sound_effect, ambient
    description: str
    details: Dict


@dataclass
class VideoPrompt:
    """完整的视频提示词"""
    scene: Scene
    characters: List[Character]
    actions: List[Action]
    dialogues: List[Dialogue]
    audio_elements: List[AudioElement]
    camera_movements: List[str]
    special_effects: List[str]
    platform: str  # 目标平台
    duration_seconds: int
    
    def to_prompt_text(self) -> str:
        """转换为文本提示词"""
        lines = []
        
        # 场景描述
        lines.append(f"[{self.scene.location}场景，{self.scene.time}，{self.scene.mood}氛围]")
        
        # 角色引入
        for char in self.characters:
            lines.append(f"[{char.label}，{char.appearance}]")
        
        # 动作序列
        for action in self.actions:
            lines.append(f"[{action.character_label}]{action.intensity}[{action.action_description}]")
            if action.camera_angle:
                lines.append(f"[{action.camera_angle}]")
        
        # 对话
        for i, dialogue in enumerate(self.dialogues):
            timing = f" {dialogue.timing}，" if dialogue.timing else ""
            lines.append(f"[{dialogue.character_label}，{dialogue.emotion}{timing}{dialogue.voice_traits}]：\"{dialogue.text}\"")
        
        # 音频元素
        for audio in self.audio_elements:
            if audio.type == "sound_effect":
                lines.append(f"[音效：{audio.description}]")
            elif audio.type == "ambient":
                lines.append(f"[环境音：{audio.description}]")
            elif audio.type == "music":
                lines.append(f"[背景音乐：{audio.description}]")
        
        # 镜头运动
        for camera in self.camera_movements:
            lines.append(f"[{camera}]")
        
        # 特效
        for effect in self.special_effects:
            lines.append(f"[特效：{effect}]")
        
        # 平台优化标签
        if self.platform == "douyin":
            lines.append("[抖音优化：前3秒视觉钩子，快速节奏]")
        elif self.platform == "bilibili":
            lines.append("[B站优化：玩梗密度高，每30秒情绪变化]")
        elif self.platform == "hongguo":
            lines.append("[红果优化：情感引入，柔光效果]")
        
        return " + ".join(lines)
    
    def to_json(self) -> str:
        """转换为JSON格式"""
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


class ScriptParser:
    """剧本解析器"""
    
    def __init__(self):
        self.characters = {}
        self.scenes = []
        self.dialogues = []
        self.actions = []
    
    def parse_script(self, script_text: str) -> Dict:
        """解析剧本文本"""
        lines = script_text.strip().split('\n')
        
        current_scene = None
        current_character = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测场景描述
            if line.startswith("场景：") or line.startswith("SCENE:"):
                scene_desc = line.split("：", 1)[-1] if "：" in line else line.split(":", 1)[-1]
                current_scene = {
                    "description": scene_desc,
                    "location": self._extract_location(scene_desc),
                    "time": self._extract_time(scene_desc),
                    "mood": self._extract_mood(scene_desc)
                }
                self.scenes.append(current_scene)
            
            # 检测角色介绍
            elif line.startswith("角色：") or re.match(r'^[A-Z][A-Za-z]+:', line):
                char_info = line.split("：", 1)[-1] if "：" in line else line.split(":", 1)[-1]
                char_name = line.split("：")[0] if "：" in line else line.split(":")[0]
                self._parse_character(char_name.strip(), char_info)
            
            # 检测对话
            elif "：" in line or ":" in line:
                if "：" in line:
                    char, text = line.split("：", 1)
                else:
                    char, text = line.split(":", 1)
                
                if char in self.characters:
                    dialogue = {
                        "character": char.strip(),
                        "text": text.strip(),
                        "emotion": self._detect_emotion(text),
                        "voice_traits": self.characters[char.strip()].get("voice", "正常")
                    }
                    self.dialogues.append(dialogue)
            
            # 检测动作描述
            elif any(keyword in line for keyword in ["动作", "行动", "做", "走", "跑", "跳"]):
                action = {
                    "description": line,
                    "character": current_character,
                    "intensity": self._detect_intensity(line)
                }
                self.actions.append(action)
        
        return {
            "characters": self.characters,
            "scenes": self.scenes,
            "dialogues": self.dialogues,
            "actions": self.actions
        }
    
    def _extract_location(self, text: str) -> str:
        """从文本提取地点"""
        locations = ["室内", "室外", "山上", "水中", "城市", "森林", "房间", "办公室"]
        for loc in locations:
            if loc in text:
                return loc
        return "未知地点"
    
    def _extract_time(self, text: str) -> str:
        """从文本提取时间"""
        times = ["白天", "夜晚", "清晨", "黄昏", "中午", "午夜"]
        for time in times:
            if time in text:
                return time
        return "未知时间"
    
    def _extract_mood(self, text: str) -> str:
        """从文本提取氛围"""
        moods = ["紧张", "浪漫", "喜剧", "悬疑", "悲伤", "欢乐", "恐怖"]
        for mood in moods:
            if mood in text:
                return mood
        return "普通"
    
    def _parse_character(self, name: str, info: str):
        """解析角色信息"""
        traits = {
            "外貌": "",
            "声音": "正常",
            "特征": ""
        }
        
        # 简单解析
        if "外貌" in info:
            traits["外貌"] = info.split("外貌")[-1].split("，")[0]
        if "声音" in info:
            traits["声音"] = info.split("声音")[-1].split("，")[0]
        
        self.characters[name] = {
            "name": name,
            "label": f"角色{len(self.characters)+1}",
            **traits
        }
    
    def _detect_emotion(self, text: str) -> str:
        """检测对话情感"""
        emotions = {
            "愤怒": ["生气", "愤怒", "发火", "怒吼"],
            "悲伤": ["伤心", "哭泣", "难过", "悲哀"],
            "欢乐": ["开心", "高兴", "大笑", "欢乐"],
            "紧张": ["紧张", "害怕", "恐惧", "惊慌"],
            "平静": ["平静", "冷静", "淡定", "从容"]
        }
        
        for emotion, keywords in emotions.items():
            if any(keyword in text for keyword in keywords):
                return emotion
        
        return "正常"
    
    def _detect_intensity(self, text: str) -> str:
        """检测动作强度"""
        intensities = {
            "快速": ["快速",迅速", "急忙", "飞快"],
            "缓慢": ["缓慢", "慢慢", "缓缓", "从容"],
            "剧烈": ["剧烈", "猛烈", "强烈", "用力"],
            "轻微": ["轻微", "轻轻", "小心", "温柔"]
        }
        
        for intensity, keywords in intensities.items():
            if any(keyword in text for keyword in keywords):
                return intensity
        
        return "正常"


def generate_from_script(script_path: str, platform: str = "general") -> VideoPrompt:
    """从剧本文件生成提示词"""
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    parser = ScriptParser()
    parsed = parser.parse_script(script_text)
    
    # 创建场景
    scene_data = parsed["scenes"][0] if parsed["scenes"] else {
        "description": "默认场景",
        "location": "室内",
        "time": "白天",
        "mood": "普通"
    }
    
    scene = Scene(
        description=scene_data["description"],
        location=scene_data["location"],
        time=scene_data["time"],
        mood=scene_data["mood"],
        environment_sounds=["基本环境音"]
    )
    
    # 创建角色
    characters = []
    for i, (name, data) in enumerate(parsed["characters"].items()):
        char = Character(
            name=name,
            label=data["label"],
            appearance=data.get("外貌", "普通外貌"),
            voice_traits=data.get("声音", "正常声音"),
            special_effects=[]
        )
        characters.append(char)
    
    # 创建动作
    actions = []
    for action_data in parsed["actions"][:3]:  # 取前3个动作
        action = Action(
            character_label=action_data.get("character", "未知角色"),
            action_description=action_data["description"],
            intensity=action_data.get("intensity", "正常"),
            camera_angle="镜头特写"
        )
        actions.append(action)
    
    # 创建对话
    dialogues = []
    for i, dialogue_data in enumerate(parsed["dialogues"][:4]):  # 取前4句对话
        timing = "紧接着" if i > 0 else None
        dialogue = Dialogue(
            character_label=dialogue_data["character"],
            text=dialogue_data["text"],
            emotion=dialogue_data["emotion"],
            voice_traits=dialogue_data["voice_traits"],
            timing=timing
        )
        dialogues.append(dialogue)
    
    # 音频元素
    audio_elements = [
        AudioElement(
            type="ambient",
            description=f"{scene.location}环境音",
            details={"volume": "中等"}
        )
    ]
    
    # 镜头运动
    camera_movements = ["镜头切换", "镜头缓慢推进"]
    
    # 特效
    special_effects = ["基础光效"]
    
    # 创建完整提示词
    prompt = VideoPrompt(
        scene=scene,
        characters=characters,
        actions=actions,
        dialogues=dialogues,
        audio_elements=audio_elements,
        camera_movements=camera_movements,
        special_effects=special_effects,
        platform=platform,
        duration_seconds=60
    )
    
    return prompt


def main():
    parser = argparse.ArgumentParser(description="AI视频生成提示词生成器")
    parser.add_argument("input", help="输入剧本文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径（默认：提示词.txt）")
    parser.add_argument("--platform", "-p", choices=["douyin", "bilibili", "hongguo", "general"], 
                       default="general", help="目标平台")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", 
                       help="输出格式")
    
    args = parser.parse_args()
    
    try:
        prompt = generate_from_script(args.input, args.platform)
        
        if args.format == "text":
            output_text = prompt.to_prompt_text()
        else:
            output_text = prompt.to_json()
        
        output_path = args.output or "提示词.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)
        
        print(f"提示词已生成到：{output_path}")
        print(f"平台优化：{args.platform}")
        print(f"格式：{args.format}")
        
        # 预览前5行
        print("\n预览：")
        for line in output_text.split('\n')[:5]:
            print(line[:100] + "..." if len(line) > 100 else line)
    
    except Exception as e:
        print(f"错误：{e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())