#!/usr/bin/env python3
"""SkillNet 快速开始示例"""

from skillnet_ai import SkillNetClient

# 初始化客户端
client = SkillNetClient()

print("=" * 60)
print("SkillNet 快速开始")
print("=" * 60)

# 1. 搜索技能
print("\n🔍 搜索 'python' 相关技能...")
results = client.search(q="python", limit=5)

for i, skill in enumerate(results, 1):
    print(f"\n{i}. {skill.skill_name}")
    print(f"   ⭐ {skill.stars} | 类别: {skill.category}")
    print(f"   描述: {skill.skill_description[:80]}...")
    print(f"   URL: {skill.skill_url}")

# 2. 下载技能（可选）
if results:
    print("\n" + "=" * 60)
    print("💡 下载技能示例:")
    print(f"skillnet download {results[0].skill_url} -d ./my_skills")

    # 或使用 SDK
    # local_path = client.download(
    #     url=results[0].skill_url,
    #     target_dir="./my_skills"
    # )
    # print(f"✅ 已下载到: {local_path}")

print("\n" + "=" * 60)
print("📚 更多功能:")
print("  • 创建技能: client.create(prompt='...')")
print("  • 评估技能: client.evaluate(target='./skill')")
print("  • 分析关系: client.analyze(skills_dir='./skills')")
print("=" * 60)
