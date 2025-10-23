from datetime import datetime
from typing import Dict, List
from ..database.mongodb import fortune_history
import random

class DailyFortuneGenerator:
    FORTUNE_TEMPLATES = [
        {
            "message": "Hôm nay là ngày cho những khởi đầu mới. Hãy tin tưởng vào trực giác và bước những bước đầu tiên với sự tự tin. Vũ trụ đang ủng hộ bạn!",
            "lucky_colors": ["Xanh Dương", "Bạc"],
            "lucky_numbers": [3, 7, 21],
            "emoji": "✨",
            "quote": "Mỗi khoảnh khắc là một khởi đầu mới.",
            "advice": "Hãy mở lòng với những cơ hội mới và không sợ hãi thất bại. Đây là thời điểm tốt để bắt đầu dự án hoặc thử điều gì đó khác biệt.",
            "area_focus": "Sự nghiệp và phát triển cá nhân"
        },
        {
            "message": "Những cơ hội bất ngờ sẽ đến với bạn. Hãy tỉnh táo và sẵn sàng nắm bắt chúng. Sự chuẩn bị của bạn sẽ tạo nên sự khác biệt.",
            "lucky_colors": ["Tím", "Vàng Kim"],
            "lucky_numbers": [5, 8, 13],
            "emoji": "🌟",
            "quote": "May mắn là khi sự chuẩn bị gặp được cơ hội.",
            "advice": "Hãy chú ý đến các chi tiết nhỏ và tin vào năng lực của bản thân. Cơ hội có thể đến từ những nơi bạn không ngờ tới.",
            "area_focus": "Tài chính và cơ hội kinh doanh"
        },
        {
            "message": "Hãy tập trung chăm sóc bản thân hôm nay. Tâm trí và cơ thể bạn cần được quan tâm để duy trì sự hài hòa. Hãy dành thời gian cho bản thân.",
            "lucky_colors": ["Xanh Lá", "Trắng"],
            "lucky_numbers": [2, 6, 9],
            "emoji": "🧘",
            "quote": "Chăm sóc bản thân là một phần của việc chăm sóc số mệnh của bạn.",
            "advice": "Thiền định, tập yoga hoặc đơn giản là đi dạo trong thiên nhiên. Sức khỏe tinh thần và thể chất cần được cân bằng.",
            "area_focus": "Sức khỏe và tinh thần"
        },
        {
            "message": "Những điều tốt đẹp đang chờ đợi phía trước. Hãy giữ vững niềm tin và tiếp tục tiến bước. Ánh sáng cuối đường hầm đang hiện ra!",
            "lucky_colors": ["Hồng", "Vàng"],
            "lucky_numbers": [1, 11, 22],
            "emoji": "🌈",
            "quote": "Niềm tin là ánh sáng dẫn đường cho những điều kỳ diệu.",
            "advice": "Đừng bỏ cuộc khi gặp khó khăn. Mọi thử thách đều là cơ hội để bạn trưởng thành và mạnh mẽ hơn.",
            "area_focus": "Tình yêu và các mối quan hệ"
        },
        {
            "message": "Hôm nay là ngày thích hợp để kết nối với những người xung quanh. Một cuộc gặp gỡ có thể mang đến điều bất ngờ và ý nghĩa.",
            "lucky_colors": ["Cam", "Xanh Ngọc"],
            "lucky_numbers": [4, 10, 15],
            "emoji": "🤝",
            "quote": "Mỗi người bạn gặp đều là một duyên phận.",
            "advice": "Hãy chủ động liên lạc với bạn bè cũ hoặc gặp gỡ người mới. Mạng lưới quan hệ của bạn có thể mở ra nhiều cánh cửa.",
            "area_focus": "Quan hệ xã hội và networking"
        },
        {
            "message": "Sự sáng tạo của bạn đang ở đỉnh cao. Hãy để trí tưởng tượng bay xa và thể hiện ý tưởng của mình một cách tự do nhất.",
            "lucky_colors": ["Đỏ", "Vàng Cam"],
            "lucky_numbers": [3, 5, 12],
            "emoji": "🎨",
            "quote": "Sáng tạo là sự thông minh đang vui chơi.",
            "advice": "Đây là thời điểm tốt để bắt đầu dự án nghệ thuật, viết lách hoặc bất kỳ hoạt động sáng tạo nào. Đừng tự giới hạn bản thân.",
            "area_focus": "Sáng tạo và biểu đạt cá nhân"
        },
        {
            "message": "Hãy kiên nhẫn và bình tĩnh. Những gì bạn đang chờ đợi sẽ đến đúng lúc. Vũ trụ có thời gian của riêng nó.",
            "lucky_colors": ["Xanh Nước Biển", "Bạc"],
            "lucky_numbers": [7, 14, 21],
            "emoji": "⏳",
            "quote": "Kiên nhẫn là chìa khóa mở cánh cửa niềm vui.",
            "advice": "Đừng vội vàng đưa ra quyết định quan trọng. Hãy quan sát và chờ đợi dấu hiệu rõ ràng hơn.",
            "area_focus": "Phát triển tâm linh và trí tuệ"
        },
        {
            "message": "Hôm nay, lòng tốt của bạn sẽ được đền đáp. Hãy tiếp tục lan tỏa năng lượng tích cực và giúp đỡ người khác.",
            "lucky_colors": ["Vàng", "Trắng"],
            "lucky_numbers": [6, 9, 18],
            "emoji": "💝",
            "quote": "Điều bạn cho đi sẽ quay trở lại gấp bội.",
            "advice": "Làm một việc tốt mà không mong đợi đền đáp. Karma tích cực sẽ mang lại điều tốt đẹp cho bạn.",
            "area_focus": "Từ thiện và phục vụ cộng đồng"
        },
        {
            "message": "Hãy tin vào năng lực của bản thân. Bạn mạnh mẽ và có khả năng vượt qua mọi thách thức. Đừng để ai làm bạn nghi ngờ điều đó.",
            "lucky_colors": ["Đỏ Tía", "Vàng Đồng"],
            "lucky_numbers": [1, 8, 17],
            "emoji": "💪",
            "quote": "Sức mạnh không đến từ khả năng thể chất mà từ ý chí không khuất phục.",
            "advice": "Đối mặt với nỗi sợ của bạn và chứng minh cho bản thân thấy bạn có thể làm được. Tự tin là vũ khí mạnh nhất.",
            "area_focus": "Tự tin và phát triển bản thân"
        },
        {
            "message": "Hôm nay là ngày của sự may mắn và bất ngờ thú vị. Hãy mở lòng đón nhận những điều kỳ diệu đang đến với bạn!",
            "lucky_colors": ["Xanh Dương Nhạt", "Bạc Lung Linh"],
            "lucky_numbers": [11, 22, 33],
            "emoji": "🎁",
            "quote": "Phép màu xảy ra mỗi ngày nếu bạn tin vào chúng.",
            "advice": "Hãy để mọi thứ diễn ra tự nhiên. Đôi khi những điều tốt nhất đến khi bạn không cố gắng kiểm soát mọi thứ.",
            "area_focus": "May mắn và cơ hội bất ngờ"
        }
    ]

    @staticmethod
    def generate_fortune() -> Dict:
        """Generate a random daily fortune"""
        template = random.choice(DailyFortuneGenerator.FORTUNE_TEMPLATES)
        return {
            "fortune_date": datetime.now(),
            **template
        }

async def get_daily_fortune(user_id: str) -> Dict:
    """
    Get daily fortune for user
    Generates a new fortune each time it's called
    """
    # Generate fortune
    fortune = DailyFortuneGenerator.generate_fortune()
    
    # Create summary for history
    summary = f"Vận May Hôm Nay - {fortune['emoji']} {fortune['area_focus']}"
    
    # Save to user's history
    history_entry = {
        "user_id": user_id,
        "type": "fortune",
        "result_summary": summary,
        "result_detail": fortune,
        "created_at": datetime.now(),
        "is_favorite": False,
        "is_shared": False
    }
    
    await fortune_history.insert_one(history_entry)
    
    return fortune