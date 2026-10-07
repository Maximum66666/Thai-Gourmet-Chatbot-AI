# Common allergen and health restriction ingredient mapping for Thai foods
FOOD_PROFILE = {
    # Seafood / Shellfish / Shrimp allergies
    "shrimp": {
        "keywords": ["กุ้ง", "เคย", "กะปิ", "ต้มยำกุ้ง", "ผัดไทย", "ทอดมันกุ้ง"],
        "name": "กุ้ง / สัตว์น้ำมีเปลือก (Shrimp/Crustaceans)"
    },
    "crab": {
        "keywords": ["ปู", "ปูดอง", "ปูม้า", "ปูเค็ม", "ข้าวผัดปู"],
        "name": "ปู (Crab)"
    },
    "fish": {
        "keywords": ["ปลา", "น้ำปลา", "ปลาร้า", "ไตปลา", "ทอดมันปลากราย", "ห่อหมก", "แกงส้ม", "แกงไตปลา"],
        "name": "ปลา / ผลิตภัณฑ์จากปลา (Fish/Fish Sauce)"
    },
    "peanuts": {
        "keywords": ["ถั่ว", "ถั่วลิสง", "ส้มตำ", "ผัดไทย", "มัสมั่น", "สะเต๊ะ", "น้ำจิ้มถั่ว"],
        "name": "ถั่วลิสง / ถั่วเปลือกแข็ง (Peanuts/Nuts)"
    },
    "egg": {
        "keywords": ["ไข่", "ไข่เค็ม", "ไข่เจียว", "ไข่ดาว", "ไข่พะโล้", "ทองหยิบ", "ทองหยอด", "ฝอยทอง", "สังขยา"],
        "name": "ไข่ (Eggs)"
    },
    "dairy": {
        "keywords": ["นม", "เนย", "ชีส", "วิปครีม", "นมข้น"],
        "name": "นมวัวและผลิตภัณฑ์จากนม (Dairy)"
    },
    "gluten": {
        "keywords": ["บะหมี่", "แป้งสาลี", "เกี๊ยว", "ปาท่องโก๋", "โรตี"],
        "name": "แป้งสาลี / กลูเตน (Gluten/Wheat)"
    },
    "pork": {
        "keywords": ["หมู", "หมูกรอบ", "เบคอน", "กุนเชียง", "หมูสับ", "หมูแดง", "แคบหมู", "แหนม"],
        "name": "เนื้อหมู (Pork - ไม่ฮาลาล)"
    },
    "beef": {
        "keywords": ["เนื้อ", "เนื้อวัว", "ซุปเนื้อ"],
        "name": "เนื้อวัว (Beef)"
    }
}

# Health conditions
HEALTH_CONDITIONS = {
    "diabetes": {
        "keywords": ["หวาน", "ทองหยิบ", "ทองหยอด", "ฝอยทอง", "สังขยา", "ลอดช่อง", "บัวลอย", "ข้าวเหนียวมะม่วง", "วุ้น", "ฝอยทอง"],
        "name": "เบาหวาน (จำกัดน้ำตาล/ของหวาน)",
        "warning": "อาหารนี้มีน้ำตาลสูงหรือเป็นขนมหวาน ควรระมัดระวังระดับน้ำตาลในเลือด"
    },
    "hypertension": {
        "keywords": ["เค็ม", "ไข่เค็ม", "ปลาร้า", "ปูดอง", "ไตปลา", "แกงไตปลา", "ผัดกะเพรา", "ส้มตำปูปลาร้า"],
        "name": "ความดันโลหิตสูง / โรคไต (โซเดียมสูง)",
        "warning": "อาหารนี้อาจมีโซเดียมสูง หรือปรุงด้วยเครื่องปรุงหมักดอง/น้ำปลา/ปลาร้าปริมาณมาก"
    },
    "gerd": {
        "keywords": ["ต้มยำ", "ส้มตำ", "ยำ", "แกงป่า", "ผัดพริก", "ผัดกะเพรา", "แกงส้ม", "คั่วกลิ้ง"],
        "name": "กรดไหลย้อน / กระเพาะอาหาร (จำกัดรสเผ็ด/เปรี้ยวจัด)",
        "warning": "อาหารนี้มีรสเผ็ดจัด หรือเปรี้ยวจัด อาจกระตุ้นอาการกรดไหลย้อนหรือระคายเคืองกระเพาะ"
    },
    "halal": {
        "keywords": ["หมู", "หมูกรอบ", "เบคอน", "กุนเชียง", "หมูสับ", "หมูแดง", "แคบหมู", "แหนม", "เลือด"],
        "name": "อิสลาม / มังสวิรัติ (หลีกเลี่ยงหมู)",
        "warning": "อาหารนี้มีส่วนประกอบของหมูหรือผลิตภัณฑ์จากหมู ไม่ใช่อาหารฮาลาล"
    },
    "vegetarian": {
        "keywords": ["หมู", "ไก่", "เนื้อ", "ปลา", "กุ้ง", "ปู", "ไข่", "น้ำปลา", "กะปิ", "ปลาร้า"],
        "name": "มังสวิรัติ / เจ (Vegetarian/Vegan)",
        "warning": "อาหารนี้มีเนื้อสัตว์ หรือเครื่องปรุงที่ทำจากสัตว์ (เช่น กะปิ น้ำปลา)"
    }
}

def analyze_health_warnings(food_name, selected_allergies, selected_health_conditions, custom_restrictions=""):
    """
    Analyzes food name against user's allergy history and health conditions.
    Returns a list of warning objects.
    """
    warnings = []
    food_name_lower = food_name.strip().lower()

    # Check allergies
    for allergy in selected_allergies:
        if allergy in FOOD_PROFILE:
            profile = FOOD_PROFILE[allergy]
            match = any(kw in food_name_lower for kw in profile["keywords"])
            if match:
                warnings.append({
                    "type": "allergy",
                    "severity": "danger",
                    "title": f"⚠️ แจ้งเตือนสารก่อภูมิแพ้: {profile['name']}",
                    "detail": f"ชื่ออาหาร '{food_name}' บ่งชี้ว่าอาจมีส่วนประกอบของ {profile['name']} ซึ่งตรงกับประวัติการแพ้ของคุณ"
                })

    # Check health conditions
    for cond in selected_health_conditions:
        if cond in HEALTH_CONDITIONS:
            cprofile = HEALTH_CONDITIONS[cond]
            match = any(kw in food_name_lower for kw in cprofile["keywords"])
            if match:
                warnings.append({
                    "type": "health",
                    "severity": "warning",
                    "title": f"🩺 คำแนะนำสุขภาพ: {cprofile['name']}",
                    "detail": cprofile["warning"]
                })

    # Check custom user keywords
    if custom_restrictions:
        custom_items = [c.strip() for c in custom_restrictions.replace(',', ' ').split() if c.strip()]
        for item in custom_items:
            if item.lower() in food_name_lower:
                warnings.append({
                    "type": "custom",
                    "severity": "danger",
                    "title": f"⚠️ ตรงกับสิ่งที่คุณระบุว่าแพ้/หลีกเลี่ยง: '{item}'",
                    "detail": f"พบคำว่า '{item}' ในชื่ออาหาร '{food_name}' โปรดตรวจสอบส่วนผสมก่อนรับประทาน"
                })

    return warnings
