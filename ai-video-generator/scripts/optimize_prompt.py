#!/usr/bin/env python3
"""
AI视频生成提示词优化脚本
优化现有提示词，提高生成质量
"""

import re
import json
import argparse
from typing import List, Dict, Tuple
import os
from datetime import datetime


class PromptOptimizer:
    """提示词优化器"""
    
    def __init__(self):
        self.platform_rules = {
            "douyin": {
                "hook_seconds": 3,
                "max_duration": 60,
                "required_elements": ["快速节奏", "视觉冲击", "大字标题"],
                "camera_style": ["剧烈晃动", "快速切换", "特写聚焦"]
            },
            "bilibili": {
                "hook_seconds": 5,
                "max_duration": 300,
                "required_elements": ["玩梗密度", "专业解说", "情绪波动"],
                "camera_style": ["稳定推轨", "多角度", "分屏展示"]
            },
            "hongguo": {
                "hook_seconds": 5,
                "max_duration": 180,
                "required_elements": ["情感引入", "柔光效果", "内心独白"],
                "camera_style": ["缓慢拉近", "柔光镜头", "情感特写"]
            },
            "general": {
                "hook_seconds": 5,
                "max_duration": 120,
                "required_elements": ["基础结构", "清晰描述", "完整元素"],
                "camera_style": ["标准切换", "基础运镜", "常规特写"]
            }
        }
        
        self.optimization_rules = {
            "character_consistency": self._check_character_consistency,
            "camera_variety": self._check_camera_variety,
            "audio_completeness": self._check_audio_completeness,
            "timing_logic": self._check_timing_logic,
            "emotional_arc": self._check_emotional_arc,
            "platform_optimization": self._check_platform_optimization
        }
    
    def optimize(self, prompt_text: str, target_platform: str = "general") -> Dict:
        """优化提示词"""
        analysis = self.analyze_prompt(prompt_text)
        
        optimizations = []
        suggestions = []
        
        # 应用所有优化规则
        for rule_name, rule_func in self.optimization_rules.items():
            result = rule_func(prompt_text, analysis, target_platform)
            if result["needs_optimization"]:
                optimizations.append({
                    "rule": rule_name,
                    "issue": result["issue"],
                    "suggestion": result["suggestion"]
                })
                suggestions.append(result["suggestion"])
        
        # 生成优化后的提示词
        optimized_text = self._apply_optimizations(prompt_text, optimizations, target_platform)
        
        return {
            "original": prompt_text,
            "optimized": optimized_text,
            "analysis": analysis,
            "optimizations": optimizations,
            "suggestions": suggestions,
            "platform": target_platform
        }
    
    def analyze_prompt(self, prompt_text: str) -> Dict:
        """分析提示词结构"""
        # 分割提示词元素
        elements = [elem.strip() for elem in prompt_text.split('+') if elem.strip()]
        
        # 分类统计
        categories = {
            "scenes": [],
            "characters": [],
            "actions": [],
            "dialogues": [],
            "camera": [],
            "audio": [],
            "effects": [],
            "other": []
        }
        
        for elem in elements:
            category = self._categorize_element(elem)
            categories[category].append(elem)
        
        # 提取角色信息
        characters = self._extract_characters(categories["characters"])
        
        # 分析对话时序
        dialogue_timing = self._analyze_dialogue_timing(categories["dialogues"])
        
        # 计算复杂度
        complexity_score = self._calculate_complexity(categories)
        
        return {
            "total_elements": len(elements),
            "categories": {k: len(v) for k, v in categories.items()},
            "character_count": len(characters),
            "characters": characters,
            "dialogue_timing": dialogue_timing,
            "complexity_score": complexity_score,
            "element_details": categories
        }
    
    def _categorize_element(self, element: str) -> str:
        """分类提示词元素"""
        element_lower = element.lower()
        
        # 场景判断
        scene_keywords = ["场景", "地点", "背景", "环境"]
        if any(keyword in element for keyword in scene_keywords):
            return "scenes"
        
        # 角色判断
        role_keywords = ["角色", "人物", "主角", "配角", "特工", "助手"]
        if any(keyword in element for keyword in role_keywords):
            return "characters"
        
        # 动作判断
        action_keywords = ["动作", "运动", "做", "走", "跑", "跳", "躲避", "攻击"]
        if any(keyword in element for keyword in action_keywords):
            return "actions"
        
        # 对话判断
        if "：" in element or '"' in element or "说" in element:
            return "dialogues"
        
        # 镜头判断
        camera_keywords = ["镜头", "运镜", "特写", "拉近", "切换", "跟随"]
        if any(keyword in element for keyword in camera_keywords):
            return "camera"
        
        # 音频判断
        audio_keywords = ["音效", "音乐", "声音", "对话", "唱歌", "环境音"]
        if any(keyword in element for keyword in audio_keywords):
            return "audio"
        
        # 特效判断
        effect_keywords = ["特效", "效果", "光效", "粒子", "数字", "BUG"]
        if any(keyword in element for keyword in effect_keywords):
            return "effects"
        
        return "other"
    
    def _extract_characters(self, character_elements: List[str]) -> List[Dict]:
        """提取角色信息"""
        characters = []
        
        for elem in character_elements:
            # 尝试提取角色标签
            match = re.search(r'\[([^：]+)[：,]', elem)
            if match:
                label = match.group(1).strip()
                
                # 提取外貌描述
                appearance = ""
                if "，" in elem:
                    parts = elem.split("，")
                    if len(parts) > 1:
                        appearance = parts[1].replace("]", "").strip()
                
                characters.append({
                    "label": label,
                    "appearance": appearance,
                    "element": elem
                })
        
        return characters
    
    def _analyze_dialogue_timing(self, dialogue_elements: List[str]) -> Dict:
        """分析对话时序"""
        timing_words = ["紧接着", "随后", "同时", "这时候", "停顿"]
        
        has_timing = False
        timing_count = 0
        
        for elem in dialogue_elements:
            for word in timing_words:
                if word in elem:
                    has_timing = True
                    timing_count += 1
                    break
        
        return {
            "has_timing": has_timing,
            "timing_count": timing_count,
            "total_dialogues": len(dialogue_elements),
            "timing_ratio": timing_count / max(len(dialogue_elements), 1)
        }
    
    def _calculate_complexity(self, categories: Dict) -> float:
        """计算提示词复杂度"""
        weights = {
            "scenes": 1.0,
            "characters": 2.0,
            "actions": 1.5,
            "dialogues": 2.0,
            "camera": 1.0,
            "audio": 1.5,
            "effects": 1.0,
            "other": 0.5
        }
        
        total_score = 0
        for category, elements in categories.items():
            total_score += len(elements) * weights.get(category, 1.0)
        
        return total_score
    
    def _check_character_consistency(self, prompt_text: str, analysis: Dict, platform: str) -> Dict:
        """检查角色一致性"""
        characters = analysis["characters"]
        
        if len(characters) == 0:
            return {
                "needs_optimization": False,
                "issue": "无角色信息",
                "suggestion": "提示词中缺少角色描述"
            }
        
        # 检查角色标签唯一性
        labels = [char["label"] for char in characters]
        unique_labels = set(labels)
        
        if len(labels) != len(unique_labels):
            duplicate_labels = [label for label in labels if labels.count(label) > 1]
            return {
                "needs_optimization": True,
                "issue": f"角色标签重复：{duplicate_labels}",
                "suggestion": f"为重复角色分配唯一标签，如[角色A:xxx]、[角色B:xxx]"
            }
        
        # 检查角色在对话中的引用
        dialogue_elements = analysis["element_details"]["dialogues"]
        dialogue_text = " ".join(dialogue_elements)
        
        missing_in_dialogue = []
        for char in characters:
            if char["label"] not in dialogue_text:
                missing_in_dialogue.append(char["label"])
        
        if missing_in_dialogue:
            return {
                "needs_optimization": True,
                "issue": f"角色未在对话中出现：{missing_in_dialogue}",
                "suggestion": f"为这些角色添加对话或动作描述"
            }
        
        return {
            "needs_optimization": False,
            "issue": "",
            "suggestion": "角色一致性良好"
        }
    
    def _check_camera_variety(self, prompt_text: str, analysis: Dict, platform: str) -> Dict:
        """检查镜头多样性"""
        camera_elements = analysis["element_details"]["camera"]
        
        if len(camera_elements) == 0:
            return {
                "needs_optimization": True,
                "issue": "缺少镜头描述",
                "suggestion": "添加至少2-3种镜头运动，如[镜头切换]、[特写聚焦]、[缓慢拉近]"
            }
        
        if len(camera_elements) < 2:
            return {
                "needs_optimization": True,
                "issue": "镜头描述过少",
                "suggestion": "增加镜头变化，提高视觉丰富度"
            }
        
        # 检查镜头类型多样性
        camera_types = set()
        for elem in camera_elements:
            if "切换" in elem:
                camera_types.add("切换")
            if "特写" in elem:
                camera_types.add("特写")
            if "拉近" in elem or "推远" in elem:
                camera_types.add("推拉")
            if "环绕" in elem:
                camera_types.add("环绕")
            if "跟随" in elem:
                camera_types.add("跟随")
        
        if len(camera_types) < 2:
            return {
                "needs_optimization": True,
                "issue": f"镜头类型单一：{camera_types}",
                "suggestion": "混合使用不同镜头类型，如切换+特写+推拉组合"
            }
        
        return {
            "needs_optimization": False,
            "issue": "",
            "suggestion": "镜头多样性良好"
        }
    
    def _check_audio_completeness(self, prompt_text: str, analysis: Dict, platform: str) -> Dict:
        """检查音频完整性"""
        audio_elements = analysis["element_details"]["audio"]
        dialogue_elements = analysis["element_details"]["dialogues"]
        
        has_dialogue = len(dialogue_elements) > 0
        has_other_audio = len(audio_elements) > 0
        
        if not has_dialogue and not has_other_audio:
            return {
                "needs_optimization": True,
                "issue": "完全缺少音频元素",
                "suggestion": "添加至少一种音频元素：对话、音效、环境音或背景音乐"
            }
        
        if has_dialogue and not has_other_audio:
            return {
                "needs_optimization": True,
                "issue": "只有对话，缺少其他音频",
                "suggestion": "添加环境音、音效或背景音乐增强氛围"
            }
        
        # 检查环境音
        has_ambient = any("环境音" in elem for elem in audio_elements)
        if not has_ambient:
            return {
                "needs_optimization": True,
                "issue": "缺少环境音",
                "suggestion": "添加场景对应的环境音，如[环境音：城市车流]、[环境音：森林鸟鸣]"
            }
        
        return {
            "needs_optimization": False,
            "issue": "",
            "suggestion": "音频元素完整"
        }
    
    def _check_timing_logic(self, prompt_text: str, analysis: Dict, platform: str) -> Dict:
        """检查时序逻辑"""
        timing_info = analysis["dialogue_timing"]
        
        if timing_info["total_dialogues"] >= 2 and not timing_info["has_timing"]:
            return {
                "needs_optimization": True,
                "issue": "多句对话缺少时序控制",
                "suggestion": "在对话间添加时序词：紧接着、随后、同时、这时候说话人切换"
            }
        
        return {
            "needs_optimization": False,
            "issue": "",
            "suggestion": "时序逻辑合理"
        }
    
    def _check_emotional_arc(self, prompt_text: str, analysis: Dict, platform: str) -> Dict:
        """检查情绪弧线"""
        # 简单情绪检测
        emotion_keywords = {
            "紧张": ["紧张", "恐惧", "惊慌", "危急"],
            "欢乐": ["开心", "欢乐", "大笑", "愉快"],
            "悲伤": ["悲伤", "伤心", "哭泣", "难过"],
            "浪漫": ["浪漫", "温柔", "深情", "甜蜜"],
            "愤怒": ["愤怒", "生气", "发火", "怒吼"]
        }
        
        emotions_present = []
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in prompt_text for keyword in keywords):
                emotions_present.append(emotion)
        
        if len(emotions_present) == 0:
            return {
                "needs_optimization": True,
                "issue": "缺少情感描述",
                "suggestion": "为角色和场景添加情感标签，如[紧张氛围]、[欢乐情绪]"
            }
        
        if len(emotions_present) == 1:
            return {
                "needs_optimization": True,
                "issue": f"情感单一：{emotions_present[0]}",
                "suggestion": "添加情感变化，创造情绪弧线"
            }
        
        return {
            "needs_optimization": False,
            "issue": "",
            "suggestion": f"情感丰富：{', '.join(emotions_present)}"
        }
    
    def _check_platform_optimization(self, prompt_text: str, analysis: Dict, platform: str) -> Dict:
        """检查平台优化"""
        platform_rules = self.platform_rules.get(platform, self.platform_rules["general"])
        
        issues = []
        suggestions = []
        
        # 检查必要元素
        for required in platform_rules["required_elements"]:
            if required not in prompt_text:
                issues.append(f"缺少{platform}必要元素：{required}")
                suggestions.append(f"添加[{required}]元素")
        
        # 检查镜头风格
        camera_style_match = False
        for style in platform_rules["camera_style"]:
            if style in prompt_text:
                camera_style_match = True
                break
        
        if not camera_style_match:
            issues.append(f"镜头风格不符合{platform}特点")
            suggestions.append(f"添加{platform}典型镜头：{', '.join(platform_rules['camera_style'][:2])}")
        
        if issues:
            return {
                "needs_optimization": True,
                "issue": "; ".join(issues),
                "suggestion": "; ".join(suggestions)
            }
        
        return {
            "needs_optimization": False,
            "issue": "",
            "suggestion": f"已针对{platform}平台优化"
        }
    
    def _apply_optimizations(self, prompt_text: str, optimizations: List[Dict], platform: str) -> str:
        """应用优化建议"""
        if not optimizations:
            return prompt_text
        
        elements = [elem.strip() for elem in prompt_text.split('+') if elem.strip()]
        optimized_elements = elements.copy()
        
        platform_rules = self.platform_rules.get(platform, self.platform_rules["general"])
        
        # 应用平台优化
        if platform != "general":
            # 添加平台标签
            platform_tag = f"[{platform.upper()}优化]"
            if platform_tag not in " ".join(optimized_elements):
                optimized_elements.append(platform_tag)
            
            # 确保必要元素
            for required in platform_rules["required_elements"]:
                if not any(required in elem for elem in optimized_elements):
                    optimized_elements.append(f"[{required}]")
        
        # 应用其他优化
        for opt in optimizations:
            rule = opt["rule"]
            
            if rule == "character_consistency":
                # 简化处理：添加角色一致性提示
                if not any("角色一致性" in elem for elem in optimized_elements):
                    optimized_elements.append("[角色标签唯一，视觉锚定]")
            
            elif rule == "camera_variety":
                # 添加更多镜头
                camera_count = sum(1 for elem in optimized_elements if "镜头" in elem)
                if camera_count < 3:
                    additional_cameras = ["[镜头切换]", "[特写聚焦]", "[缓慢拉近]"][:3-camera_count