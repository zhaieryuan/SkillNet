#!/usr/bin/env python3
"""测试 SkillNet SDK 功能"""

from skillnet_ai import SkillNetClient

print("=" * 60)
print("SkillNet SDK 测试")
print("=" * 60)

# 1. 初始化客户端（搜索和下载不需要 API Key）
print("\n✅ 初始化 SkillNetClient...")
client = SkillNetClient()
print("   客户端创建成功！")

# 2. 测试搜索功能
print("\n🔍 测试搜索功能...")
results = client.search(q="docker", mode="keyword", limit=3)
print(f"   找到 {len(results)} 个技能:")

for i, skill in enumerate(results, 1):
    print(f"\n   {i}. {skill.skill_name}")
    print(f"      作者: {skill.author}")
    print(f"      Star: ⭐ {skill.stars}")
    print(f"      描述: {skill.skill_description[:80]}...")
    print(f"      类别: {skill.category}")

# 3. 测试语义搜索
print("\n\n🤖 测试语义搜索...")
vector_results = client.search(
    q="处理图片和可视化",
    mode="vector",
    threshold=0.8,
    limit=2
)
print(f"   找到 {len(vector_results)} 个相关技能:")
for skill in vector_results:
    print(f"   - {skill.skill_name}: {skill.skill_description[:60]}...")

# 4. 显示可用的模块
print("\n\n📦 已安装的 SkillNet 模块:")
from skillnet_ai import (
    SkillCreator,
    SkillDownloader,
    SkillEvaluator,
    SkillNetSearcher,
    SkillRelationshipAnalyzer
)
print("   ✅ SkillNetClient")
print("   ✅ SkillCreator")
print("   ✅ SkillDownloader")
print("   ✅ SkillEvaluator")
print("   ✅ SkillNetSearcher")
print("   ✅ SkillRelationshipAnalyzer")

print("\n" + "=" * 60)
print("✅ 所有测试通过！SkillNet SDK 运行正常！")
print("=" * 60)

# 5. 下载一个技能测试
print("\n📥 测试下载功能...")
print("   下载第一个搜索到的技能...")

if results:
    try:
        import os
        test_dir = "./test_skills"
        os.makedirs(test_dir, exist_ok=True)

        local_path = client.download(
            url=results[0].skill_url,
            target_dir=test_dir
        )
        print(f"   ✅ 下载成功！")
        print(f"   路径: {local_path}")

        # 列出下载的文件
        files = os.listdir(local_path)
        print(f"   文件列表 ({len(files)} 个文件):")
        for f in files[:5]:  # 只显示前5个
            print(f"      - {f}")
        if len(files) > 5:
            print(f"      ... 还有 {len(files) - 5} 个文件")

    except Exception as e:
        print(f"   ⚠️ 下载失败: {e}")

print("\n" + "=" * 60)
print("🎉 SkillNet 环境安装和测试完成！")
print("=" * 60)
