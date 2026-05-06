#!/usr/bin/env python3
"""
Ultimate Webdrama Creator 使用示例
演示如何创建、优化和导出网剧项目
"""

import json
from main import UltimateWebdramaCreator

def example_create_crazy_shark():
    """示例：创建《狂鲨末世》项目"""
    print("=" * 60)
    print("示例1: 创建《狂鲨末世》科幻悬疑网剧")
    print("=" * 60)
    
    # 初始化创作系统
    creator = UltimateWebdramaCreator()
    
    # 创建项目
    project = creator.create_project(
        title="狂鲨末世",
        genre="sci-fi",
        episodes=5
    )
    
    # 保存项目
    with open("crazy_shark_apocalypse.json", 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 项目创建完成!")
    print(f"📝 标题: {project['title']}")
    print(f"🎭 类型: {project['concept']['genre_name']}")
    print(f"📊 集数: {project['episodes']}")
    print(f"👥 人物数量: {len(project['characters'])}")
    
    # 显示数据预测
    print("\n📈 数据预测:")
    predictions = project['predictions']
    print(f"  前3秒留存率: {predictions['retention_3s']}")
    print(f"  完播率: {predictions['completion_rate']}")
    print(f"  互动率: {predictions['engagement_rate']}")
    print(f"  爆款概率: {predictions['viral_probability']}")
    
    return project

def example_optimize_for_platforms(project):
    """示例：为不同平台优化"""
    print("\n" + "=" * 60)
    print("示例2: 平台专属优化")
    print("=" * 60)
    
    creator = UltimateWebdramaCreator()
    
    # 抖音优化
    print("\n🎯 抖音优化版本:")
    douyin_optimized = creator.optimize_for_platform(project, 'douyin')
    
    # 检查优化内容
    if 'storyboard_outline' in douyin_optimized:
        episode = douyin_optimized['storyboard_outline'][0]
        if 'platform_optimization' in episode:
            opt = episode['platform_optimization']
            print(f"  平台: {opt['platform']}")
            print(f"  重点: {opt['focus']}")
            print(f"  技巧: {', '.join(opt['techniques'])}")
    
    # 红果优化
    print("\n🎯 红果优化版本:")
    hongguo_optimized = creator.optimize_for_platform(project, 'hongguo')
    
    if 'storyboard_outline' in hongguo_optimized:
        episode = hongguo_optimized['storyboard_outline'][0]
        if 'platform_optimization' in episode:
            opt = episode['platform_optimization']
            print(f"  平台: {opt['platform']}")
            print(f"  重点: {opt['focus']}")
            print(f"  技巧: {', '.join(opt['techniques'])}")
    
    return douyin_optimized, hongguo_optimized

def example_export_project(project):
    """示例：导出项目"""
    print("\n" + "=" * 60)
    print("示例3: 导出完整创作包")
    print("=" * 60)
    
    creator = UltimateWebdramaCreator()
    
    # 导出完整包
    export_result = creator.export_project(project, 'full_package')
    
    print(f"\n📤 导出结果:")
    print(f"  成功: {export_result['success']}")
    print(f"  输出路径: {export_result['output_path']}")
    print(f"  文件数量: {export_result['total_files']}")
    
    print(f"\n📄 生成的文件:")
    for file in export_result['files']:
        print(f"  - {file}")
    
    return export_result

def example_ab_testing(project):
    """示例：A/B测试"""
    print("\n" + "=" * 60)
    print("示例4: A/B测试不同开场")
    print("=" * 60)
    
    creator = UltimateWebdramaCreator()
    
    # 运行A/B测试
    test_results = creator.run_ab_test(
        project=project,
        variable="opening_hook",
        variants=3
    )
    
    print(f"\n🔬 A/B测试配置:")
    print(f"  测试变量: {test_results['variable']}")
    print(f"  变体数量: {test_results['variants']}")
    
    # 生成测试变体
    print(f"\n🎭 生成的变体:")
    variants = [
        "变体A: 视觉冲击开场 - 狂鲨眼睛特写 + 警报",
        "变体B: 悬念开场 - 深海低频声波 + 黑影",
        "变体C: 情感开场 - 科学家担忧表情 + 实验数据"
    ]
    
    for i, variant in enumerate(variants, 1):
        print(f"  变体{i}: {variant}")
    
    print("\n📊 预期测试指标:")
    print("  - 前3秒留存率")
    print("  - 30秒完播率")
    print("  - 互动率（评论/分享）")
    print("  - 追剧意愿")

def example_emotional_drama():
    """示例：创建情感剧"""
    print("\n" + "=" * 60)
    print("示例5: 创建情感共鸣剧《时光里的我们》")
    print("=" * 60)
    
    creator = UltimateWebdramaCreator()
    
    # 创建情感剧项目
    project = creator.create_project(
        title="时光里的我们",
        genre="emotional",
        episodes=3
    )
    
    print(f"\n✅ 情感剧项目创建完成!")
    print(f"📝 标题: {project['title']}")
    print(f"🎭 类型: {project['concept']['genre_name']}")
    print(f"💖 核心钩子: {project['concept']['opening_hook']}")
    
    # 显示人物
    print(f"\n👥 主要人物:")
    for char in project['characters']:
        print(f"  - {char['name']} ({char['age']}岁, {char['occupation']})")
    
    # 数据预测
    predictions = project['predictions']
    print(f"\n📈 情感剧数据预测:")
    print(f"  前3秒留存率: {predictions['retention_3s']} (情感引入效果)")
    print(f"  完播率: {predictions['completion_rate']} (情感持续力)")
    print(f"  爆款概率: {predictions['viral_probability']}")

def main():
    """主示例函数"""
    print("🌟 Ultimate Webdrama Creator 使用示例 🌟")
    print("融合 ai-webdrama-storyboard 和 viral-webdrama-creator 的终极创作系统")
    print()
    
    try:
        # 示例1: 创建科幻悬疑剧
        project = example_create_crazy_shark()
        
        # 示例2: 平台优化
        douyin_proj, hongguo_proj = example_optimize_for_platforms(project)
        
        # 示例3: 导出项目
        export_result = example_export_project(project)
        
        # 示例4: A/B测试
        example_ab_testing(project)
        
        # 示例5: 创建情感剧
        example_emotional_drama()
        
        print("\n" + "=" * 60)
        print("🎉 所有示例完成!")
        print("=" * 60)
        
        print("\n📁 生成的文件:")
        print("  - crazy_shark_apocalypse.json (项目文件)")
        print("  - output/ (导出目录)")
        print("  - 包含: 创意概念、人物档案、分镜大纲、数据预测等")
        
        print("\n🚀 下一步:")
        print("  1. 查看生成的项目文件了解详细内容")
        print("  2. 根据平台优化建议调整创作")
        print("  3. 使用CLI命令进行批量创作")
        print("  4. 集成到OpenClaw技能系统中")
        
    except Exception as e:
        print(f"\n❌ 示例执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()