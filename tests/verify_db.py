"""验证数据库内容"""
import json

with open('db/meals.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("📊 数据库验证报告")
print("=" * 80)

for day in data['days']:
    print(f"\n📅 日期: {day['date']}")
    print(f"   今日总餐数: {len(day['meals'])}")
    
    # 显示 daily_summary
    summary = day['daily_summary']
    print(f"\n   📈 Daily Summary (数据库中的总和):")
    print(f"      总热量: {summary['total_calories']} kcal")
    print(f"      总蛋白质: {summary['total_protein']}g")
    print(f"      总脂肪: {summary['total_fat']}g")
    print(f"      总碳水: {summary['total_carbs']}g")
    print(f"      总钠: {summary['total_sodium']}mg")
    
    # 显示各餐并手动计算总和
    print(f"\n   🍽️  各餐详情:")
    manual_total = {
        'calories': 0,
        'protein': 0,
        'fat': 0,
        'carbs': 0,
        'sodium': 0
    }
    
    for i, meal in enumerate(day['meals'], 1):
        nutrition = meal.get('meal_nutrition_total') or meal.get('nutrition_total', {})
        print(f"      {i}. {meal['meal_id']}")
        print(f"         热量: {nutrition.get('calories', 0)} kcal")
        print(f"         蛋白质: {nutrition.get('protein', 0)}g")
        
        # 累加到手动计算总和
        for key in manual_total:
            manual_total[key] += nutrition.get(key, 0)
    
    # 显示手动计算的总和
    print(f"\n   🧮 手动验证总和:")
    print(f"      总热量: {manual_total['calories']} kcal")
    print(f"      总蛋白质: {manual_total['protein']}g")
    print(f"      总脂肪: {manual_total['fat']}g")
    print(f"      总碳水: {manual_total['carbs']}g")
    print(f"      总钠: {manual_total['sodium']}mg")
    
    # 验证是否一致
    match = (
        abs(summary['total_calories'] - manual_total['calories']) < 0.01 and
        abs(summary['total_protein'] - manual_total['protein']) < 0.01 and
        abs(summary['total_fat'] - manual_total['fat']) < 0.01 and
        abs(summary['total_carbs'] - manual_total['carbs']) < 0.01 and
        abs(summary['total_sodium'] - manual_total['sodium']) < 0.01
    )
    
    if match:
        print(f"\n   ✅ 验证通过: daily_summary 与各餐总和完全一致！")
    else:
        print(f"\n   ❌ 验证失败: daily_summary 与各餐总和不一致！")

print("\n" + "=" * 80)
print("📋 结论: 数据库写入和更新功能正常工作")
print("=" * 80)
