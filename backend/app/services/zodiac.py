from datetime import datetime
from typing import Dict, List
from ..database.mongodb import fortune_history

class ZodiacCalculator:
    ZODIAC_SIGNS = {
        "Aries": {
            "start": (3, 21), 
            "end": (4, 19), 
            "element": "Fire",
            "symbol": "♈",
            "description": "Năng động, dũng cảm và đầy nhiệt huyết",
            "date_range": "21/3 - 19/4"
        },
        "Taurus": {
            "start": (4, 20), 
            "end": (5, 20), 
            "element": "Earth",
            "symbol": "♉",
            "description": "Kiên định, trung thành và yêu thích sự ổn định",
            "date_range": "20/4 - 20/5"
        },
        "Gemini": {
            "start": (5, 21), 
            "end": (6, 20), 
            "element": "Air",
            "symbol": "♊",
            "description": "Thông minh, linh hoạt và giao tiếp tốt",
            "date_range": "21/5 - 20/6"
        },
        "Cancer": {
            "start": (6, 21), 
            "end": (7, 22), 
            "element": "Water",
            "symbol": "♋",
            "description": "Nhạy cảm, chu đáo và yêu gia đình",
            "date_range": "21/6 - 22/7"
        },
        "Leo": {
            "start": (7, 23), 
            "end": (8, 22), 
            "element": "Fire",
            "symbol": "♌",
            "description": "Tự tin, hào phóng và có khả năng lãnh đạo",
            "date_range": "23/7 - 22/8"
        },
        "Virgo": {
            "start": (8, 23), 
            "end": (9, 22), 
            "element": "Earth",
            "symbol": "♍",
            "description": "Cẩn thận, tỉ mỉ và có tính phân tích cao",
            "date_range": "23/8 - 22/9"
        },
        "Libra": {
            "start": (9, 23), 
            "end": (10, 22), 
            "element": "Air",
            "symbol": "♎",
            "description": "Hòa bình, công bằng và yêu thích cái đẹp",
            "date_range": "23/9 - 22/10"
        },
        "Scorpio": {
            "start": (10, 23), 
            "end": (11, 21), 
            "element": "Water",
            "symbol": "♏",
            "description": "Bí ẩn, mãnh liệt và đầy trực giác",
            "date_range": "23/10 - 21/11"
        },
        "Sagittarius": {
            "start": (11, 22), 
            "end": (12, 21), 
            "element": "Fire",
            "symbol": "♐",
            "description": "Lạc quan, phiêu lưu và yêu tự do",
            "date_range": "22/11 - 21/12"
        },
        "Capricorn": {
            "start": (12, 22), 
            "end": (1, 19), 
            "element": "Earth",
            "symbol": "♑",
            "description": "Có kỷ luật, tham vọng và kiên trì",
            "date_range": "22/12 - 19/1"
        },
        "Aquarius": {
            "start": (1, 20), 
            "end": (2, 18), 
            "element": "Air",
            "symbol": "♒",
            "description": "Độc lập, sáng tạo và nhân đạo",
            "date_range": "20/1 - 18/2"
        },
        "Pisces": {
            "start": (2, 19), 
            "end": (3, 20), 
            "element": "Water",
            "symbol": "♓",
            "description": "Mơ mộng, nhạy cảm và đầy nghệ sĩ",
            "date_range": "19/2 - 20/3"
        }
    }

    ELEMENT_TRAITS = {
        "Fire": {
            "traits": ["Nhiệt huyết", "Năng động", "Dũng cảm"],
            "lucky_colors": ["Đỏ", "Cam", "Vàng"],
            "lucky_numbers": [1, 4, 7],
            "compatible_signs": ["Aries", "Leo", "Sagittarius"]
        },
        "Earth": {
            "traits": ["Thực tế", "Trung thành", "Ổn định"],
            "lucky_colors": ["Xanh lá", "Nâu", "Vàng đồng"],
            "lucky_numbers": [2, 5, 8],
            "compatible_signs": ["Taurus", "Virgo", "Capricorn"]
        },
        "Air": {
            "traits": ["Thông minh", "Giao tiếp", "Xã hội"],
            "lucky_colors": ["Xanh nhạt", "Trắng", "Tím"],
            "lucky_numbers": [3, 6, 9],
            "compatible_signs": ["Gemini", "Libra", "Aquarius"]
        },
        "Water": {
            "traits": ["Cảm xúc", "Trực giác", "Chăm sóc"],
            "lucky_colors": ["Xanh dương", "Bạc", "Aqua"],
            "lucky_numbers": [4, 7, 2],
            "compatible_signs": ["Cancer", "Scorpio", "Pisces"]
        }
    }

    @staticmethod
    def get_zodiac_sign(birth_date: datetime) -> str:
        month = birth_date.month
        day = birth_date.day

        for sign, dates in ZodiacCalculator.ZODIAC_SIGNS.items():
            start_month, start_day = dates["start"]
            end_month, end_day = dates["end"]

            # Special case for Capricorn (spans December-January)
            if sign == "Capricorn":
                if (month == 12 and day >= start_day) or (month == 1 and day <= end_day):
                    return sign
            else:
                if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                    return sign
        
        return "Unknown"

    @staticmethod
    def get_compatibility(sign1: str, sign2: str) -> Dict:
        # Compatibility based on elements
        elements = {
            sign1: ZodiacCalculator.ZODIAC_SIGNS[sign1]["element"],
            sign2: ZodiacCalculator.ZODIAC_SIGNS[sign2]["element"]
        }

        # Element compatibility scores (out of 100)
        element_compatibility = {
            ("Fire", "Fire"): 90,
            ("Fire", "Air"): 85,
            ("Fire", "Earth"): 60,
            ("Fire", "Water"): 40,
            ("Earth", "Earth"): 95,
            ("Earth", "Water"): 90,
            ("Earth", "Fire"): 60,
            ("Earth", "Air"): 50,
            ("Air", "Air"): 85,
            ("Air", "Fire"): 85,
            ("Air", "Water"): 60,
            ("Air", "Earth"): 50,
            ("Water", "Water"): 95,
            ("Water", "Earth"): 90,
            ("Water", "Air"): 60,
            ("Water", "Fire"): 40
        }

        score = element_compatibility.get(
            (elements[sign1], elements[sign2]),
            element_compatibility.get((elements[sign2], elements[sign1]), 50)
        )

        return {
            "compatibility_score": score,
            "element_combination": f"{elements[sign1]} + {elements[sign2]}",
            "recommendation": ZodiacCalculator._get_compatibility_advice(score)
        }

    @staticmethod
    def _get_compatibility_advice(score: int) -> str:
        if score >= 90:
            return "Perfect match! Your elements naturally enhance each other."
        elif score >= 75:
            return "Great compatibility! You have a strong foundation for a relationship."
        elif score >= 60:
            return "Good potential, but may need work on understanding differences."
        elif score >= 40:
            return "Challenging but possible. Focus on growth and communication."
        else:
            return "This combination requires extra effort and understanding."

    @staticmethod
    def get_sign_details(sign: str) -> Dict:
        if sign not in ZodiacCalculator.ZODIAC_SIGNS:
            return {}

        sign_info = ZodiacCalculator.ZODIAC_SIGNS[sign]
        element = sign_info["element"]
        element_traits = ZodiacCalculator.ELEMENT_TRAITS[element]

        return {
            "name": sign,
            "symbol": sign_info["symbol"],
            "element": element,
            "description": sign_info["description"],
            "date_range": sign_info["date_range"],
            "traits": element_traits["traits"],
            "lucky_colors": element_traits["lucky_colors"],
            "lucky_numbers": element_traits["lucky_numbers"],
            "compatible_signs": element_traits["compatible_signs"]
        }

async def calculate_zodiac(user_id: str, birth_date: datetime) -> Dict:
    calculator = ZodiacCalculator()
    
    sign = calculator.get_zodiac_sign(birth_date)
    details = calculator.get_sign_details(sign)
    
    result = {
        "zodiac_sign": sign,
        **details
    }
    
    # Save to history
    history_entry = {
        "user_id": user_id,
        "type": "zodiac",
        "result_summary": f"Cung Hoàng Đạo: {sign}",
        "result_detail": result,
        "created_at": datetime.now()
    }
    
    await fortune_history.insert_one(history_entry)
    
    return result