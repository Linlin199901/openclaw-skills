        base_filename = f"{project_title}_{timestamp}"
        
        for fmt in formats:
            if fmt == "json":
                filename = self.output_dir / f"{base_filename}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(project, f, ensure_ascii=False, indent=2)
                exported_files.append(str(filename))
                print(f"  ✅ JSON导出: {filename}")
            
            elif fmt == "markdown":
                filename = self.output_dir / f"{base_filename}.md"
                self._export_markdown(project, filename)
                exported_files.append(str(filename))
                print(f"  ✅ Markdown导出: {filename}")
            
            elif fmt == "yaml":
                filename = self.output_dir / f"{base_filename}.yaml"
                with open(filename, 'w', encoding='utf-8') as f:
                    yaml.dump(project, f, allow_unicode=True)
                exported_files.append(str(filename))
                print(f"  ✅ YAML导出: {filename}")
            
            else:
                print(f"  ⚠️  不支持格式: {fmt}")
        
        return exported_files
    
    def _export_markdown(self, project, filename):
        """导出为Markdown格式"""
        idea = project["idea"]
        characters = project["characters"]
        storyboard = project["storyboard"]
        predictions = project["predictions"]
        
        with open(filename, 'w', encoding='utf-8') as f:
            # 标题
            f.write(f"# {idea['title']} - 爆款网剧项目方案\n\n")
            f.write(f"**生成时间**: {project['metadata']['created_at']}\n")
            f.write(f"**目标平台**: {idea['target_platform']}\n")
            f.write(f"**题材类型**: {idea['primary_genre']} - {idea['secondary_genre']}\n")
            f.write(f"**集数**: {idea['episode_count']}\n\n")
            
            # 项目概述
            f.write("## 📋 项目概述\n\n")
            f.write(f"**核心冲突**: {idea['core_conflict']}\n\n")
            f.write(f"**情感内核**: {idea['emotional_core']}\n\n")
            f.write(f"**一句话梗概**: {idea['logline']}\n\n")
            
            # 人物设定
            f.write("## 👥 人物设定\n\n")
            
            # 主角
            prot = characters['protagonist']
            f.write(f"### 主角: {prot['name']}\n")
            f.write(f"- **年龄**: {prot['age']}岁\n")
            f.write(f"- **职业**: {prot['occupation']}\n")
            f.write(f"- **性格特质**: {', '.join(prot['traits'])}\n")
            f.write(f"- **成长弧线**: {prot['growth_arc']}\n")
            f.write(f"- **记忆点**: {prot['memorable_trait']}\n")
            f.write(f"- **情感锚点**: {prot['emotional_anchor']}\n\n")
            
            # 反派
            ant = characters['antagonist']
            f.write(f"### 反派: {ant['name']}\n")
            f.write(f"- **年龄**: {ant['age']}岁\n")
            f.write(f"- **关系**: {ant['relationship']}\n")
            f.write(f"- **性格特质**: {', '.join(ant['traits'])}\n")
            f.write(f"- **动机**: {ant['motivation']}\n")
            f.write(f"- **可救赎性**: {'可救赎' if ant['redemption_possible'] else '不可救赎'}\n\n")
            
            # 配角
            f.write("### 配角阵容\n")
            for i, sup in enumerate(characters['supporting_characters'], 1):
                f.write(f"{i}. **{sup['name']}** ({sup['role']})\n")
                f.write(f"   - 功能: {sup['function']}\n")
                f.write(f"   - 特质: {', '.join(sup['traits'])}\n")
            f.write("\n")
            
            # 分镜详情
            f.write("## 🎬 分镜详情\n\n")
            f.write(f"**平台优化**: {storyboard['platform_optimized']}\n")
            f.write(f"**优化重点**: {storyboard['optimization_focus']}\n\n")
            
            for ep in storyboard['episodes']:
                f.write(f"### 第{ep['episode']}集\n")
                f.write(f"- **时长**: {ep['duration_seconds']}秒\n")
                f.write(f"- **镜头数**: {ep['shot_count']}个\n")
                f.write(f"- **平均镜头时长**: {ep['average_shot_duration']}\n")
                f.write(f"- **情绪曲线**: {ep['emotional_curve']}\n\n")
                
                f.write("**黄金时间设计**:\n")
                for time, desc in ep['golden_time'].items():
                    f.write(f"- {time}: {desc}\n")
                f.write("\n")
                
                f.write("**关键场景**:\n")
                for scene in ep['key_scenes']:
                    f.write(f"- {scene}\n")
                f.write("\n")
            
            # 数据预测
            f.write("## 📈 数据预测\n\n")
            f.write(f"**总体评估**: {predictions['overall_assessment']}\n\n")
            
            f.write("**关键指标预测**:\n")
            for metric, value in predictions['predictions'].items():
                f.write(f"- {metric}: {value}\n")
            f.write("\n")
            
            f.write("**优化建议**:\n")
            for suggestion in predictions['optimization_suggestions']:
                f.write(f"- {suggestion}\n")
            f.write("\n")
            
            # 制作建议
            f.write("## 💡 制作建议\n\n")
            platform = idea['target_platform']
            if platform == "douyin":
                f.write("### 抖音平台特别建议\n")
                f.write("1. **前3秒必须抓人**: 使用视觉冲击或强烈冲突\n")
                f.write("2. **节奏要快**: 平均镜头时长1-1.5秒\n")
                f.write("3. **爽点密集**: 每30秒一个情绪波动\n")
                f.write("4. **字幕强化**: 关键信息用大字幕突出\n")
                f.write("5. **互动引导**: 结尾引导评论和分享\n")
            else:
                f.write("### 红果平台特别建议\n")
                f.write("1. **情感铺垫**: 前5秒建立情感氛围\n")
                f.write("2. **内心戏足**: 给人物内心成长空间\n")
                f.write("3. **镜头稳定**: 多用固定镜头，少用快速剪辑\n")
                f.write("4. **主题深刻**: 每集要有情感升华时刻\n")
                f.write("5. **系列连贯**: 注重人物成长连续性\n")
            
            f.write("\n## 🎯 成功关键\n")
            f.write("1. **精准的平台适配**: 根据不同平台算法优化内容\n")
            f.write("2. **鲜明的人物塑造**: 每个角色都要有记忆点\n")
            f.write("3. **节奏把控**: 根据平台特性控制叙事节奏\n")
            f.write("4. **情感共鸣**: 找到能与观众共鸣的情感内核\n")
            f.write("5. **数据驱动**: 根据预测数据优化制作重点\n")
            
            f.write("\n---\n")
            f.write("*本方案由「爆款网剧创作大师」生成*\n")
            f.write(f"*工具版本: {project['metadata']['tool_version']}*\n")

def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(description='爆款网剧创作大师')
    parser.add_argument('action', choices=['generate', 'analyze', 'optimize', 'predict', 'export'],
                       help='执行动作')
    parser.add_argument('--title', help='剧集标题')
    parser.add_argument('--genre', choices=['逆袭爽剧', '情感共鸣', '悬疑烧脑', '甜宠治愈', '科幻奇幻'],
                       help='题材类型')
    parser.add_argument('--platform', choices=['douyin', 'hongguo'], help='目标平台')
    parser.add_argument('--episodes', type=int, default=3, help='集数')
    parser.add_argument('--input', help='输入文件路径')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--format', choices=['json', 'markdown', 'yaml', 'all'],
                       default='markdown', help='输出格式')
    parser.add_argument('--config', help='配置文件路径')
    
    args = parser.parse_args()
    
    # 创建创作器实例
    creator = HotWebDramaCreator(config_path=args.config)
    
    if args.action == 'generate':
        # 生成新项目
        project = creator.create_project(
            title=args.title,
            genre=args.genre,
            platform=args.platform,
            episodes=args.episodes
        )
        
        # 导出项目
        if args.format == 'all':
            formats = ['json', 'markdown', 'yaml']
        else:
            formats = [args.format]
        
        exported_files = creator.export_project(project, formats)
        
        print("\n" + "=" * 50)
        print("🎉 项目创建完成!")
        print(f"项目标题: {project['idea']['title']}")
        print(f"生成文件: {len(exported_files)}个")
        for file in exported_files:
            print(f"  📄 {file}")
        
        # 显示关键信息
        print("\n📊 关键数据预测:")
        for metric, value in project['predictions']['predictions'].items():
            if "留存率" in metric or "完播率" in metric or "互动率" in metric:
                print(f"  {metric}: {value}")
        
        print(f"\n💡 优化建议: {project['predictions']['optimization_suggestions'][0]}")
    
    elif args.action == 'analyze':
        print("市场分析功能开发中...")
        # TODO: 实现市场分析
    
    elif args.action == 'optimize':
        print("分镜优化功能开发中...")
        # TODO: 实现分镜优化
    
    elif args.action == 'predict':
        print("数据预测功能开发中...")
        # TODO: 实现数据预测
    
    elif args.action == 'export':
        print("导出功能开发中...")
        # TODO: 实现导出功能
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()