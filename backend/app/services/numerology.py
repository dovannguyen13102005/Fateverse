from datetime import datetime
from typing import Dict, List
from ..database.mongodb import fortune_history

class NumerologyCalculator:
    @staticmethod
    def calculate_life_path_number(birth_date: datetime) -> int:
        date_str = birth_date.strftime("%Y%m%d")
        number = sum(int(digit) for digit in date_str)
        while number > 9 and number != 11 and number != 22:
            number = sum(int(digit) for digit in str(number))
        return number

    @staticmethod
    def calculate_expression_number(name: str) -> int:
        # Pythagorean Numerology system
        letter_values = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
            'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
            's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
        }
        
        name = name.lower().replace(' ', '')
        number = sum(letter_values.get(char, 0) for char in name)
        
        while number > 9 and number != 11 and number != 22:
            number = sum(int(digit) for digit in str(number))
        return number

    @staticmethod
    def calculate_personality_number(name: str) -> int:
        consonants = 'bcdfghjklmnpqrstvwxyz'
        name = name.lower()
        consonant_value = sum(NumerologyCalculator.calculate_expression_number(c) 
                            for c in name if c in consonants)
        
        while consonant_value > 9 and consonant_value != 11 and consonant_value != 22:
            consonant_value = sum(int(digit) for digit in str(consonant_value))
        return consonant_value

    @staticmethod
    def calculate_soul_urge_number(name: str) -> int:
        vowels = 'aeiou'
        name = name.lower()
        vowel_value = sum(NumerologyCalculator.calculate_expression_number(c) 
                         for c in name if c in vowels)
        
        while vowel_value > 9 and vowel_value != 11 and vowel_value != 22:
            vowel_value = sum(int(digit) for digit in str(vowel_value))
        return vowel_value

    @staticmethod
    def get_number_meaning(number: int) -> Dict[str, str]:
        meanings = {
            1: {
                "title": "Nhà Lãnh Đạo - Người Tiên Phong",
                "traits": "Bạn sinh ra với khả năng lãnh đạo tự nhiên và tinh thần độc lập mạnh mẽ. Sự sáng tạo và quyết đoán là điểm mạnh của bạn. Bạn không ngại đi tiên phong, khám phá những con đường mới và truyền cảm hứng cho người khác theo đuổi ước mơ của họ.",
                "career": "Doanh nhân, Giám đốc điều hành, Nhà sáng chế, Kiến trúc sư, Nhà thiết kế, Lãnh đạo chính trị. Bạn thích hợp với những vai trò đòi hỏi sáng kiến, quyết đoán và khả năng dẫn dắt người khác.",
                "challenges": "Thách thức lớn nhất của bạn là học cách lắng nghe và hợp tác. Đôi khi bạn có thể quá cứng đầu, thống trị hoặc thiếu kiên nhẫn với người khác. Hãy nhớ rằng sức mạnh thực sự đến từ việc nâng đỡ người khác, không phải áp đặt ý chí của mình.",
                "advice": "Hãy cân bằng giữa sự tự tin và khiêm tốn. Sử dụng khả năng lãnh đạo của bạn để tạo ra tác động tích cực, nhưng đừng quên lắng nghe và học hỏi từ người khác. Sự độc lập của bạn là món quà, nhưng đừng để nó trở thành sự cô lập."
            },
            2: {
                "title": "Người Hòa Giải - Cầu Nối Hòa Bình",
                "traits": "Bạn có khả năng đặc biệt trong việc hiểu và kết nối mọi người. Sự nhạy cảm, kiên nhẫn và khả năng ngoại giao của bạn giúp hóa giải mâu thuẫn và tạo ra sự hài hòa. Bạn là người biết lắng nghe, thấu hiểu và luôn tìm cách cân bằng trong mọi tình huống.",
                "career": "Cố vấn, Nhà ngoại giao, Trung gian hòa giải, Giáo viên, Nhân viên xã hội, Nghệ sĩ, Y tá. Bạn xuất sắc trong các vai trò đòi hỏi sự hợp tác, đồng cảm và khả năng làm việc nhóm.",
                "challenges": "Bạn dễ bị ảnh hưởng bởi cảm xúc người khác và có thể quá phụ thuộc vào sự chấp nhận. Sự thiếu quyết đoán và xu hướng tránh né xung đột có thể khiến bạn bỏ lỡ cơ hội. Đôi khi bạn cần học cách đặt ranh giới và bảo vệ năng lượng của chính mình.",
                "advice": "Tin tưởng vào trực giác của bạn và đừng sợ đưa ra quyết định. Sự nhạy cảm của bạn là sức mạnh, không phải điểm yếu. Hãy học cách nói 'không' khi cần thiết và nhớ rằng bạn không thể làm hài lòng tất cả mọi người."
            },
            3: {
                "title": "Người Giao Tiếp - Nghệ Sĩ Của Cuộc Sống",
                "traits": "Bạn mang trong mình năng lượng sáng tạo và niềm vui sống tràn đầy. Khả năng giao tiếp xuất sắc, óc hài hước và sự lạc quan tự nhiên giúp bạn thu hút mọi người. Bạn có tài năng biến những ý tưởng trừu tượng thành hiện thực thông qua nghệ thuật, ngôn từ hoặc biểu diễn.",
                "career": "Nhà văn, Diễn giả, Nghệ sĩ, Nhạc sĩ, Diễn viên, Nhà thiết kế đồ họa, Chuyên gia marketing, Giáo viên nghệ thuật. Bạn thành công trong môi trường cho phép sự sáng tạo và tự do biểu đạt.",
                "challenges": "Xu hướng phân tán năng lượng vào quá nhiều dự án cùng lúc có thể khiến bạn thiếu tập trung. Bạn có thể trở nên hời hợt hoặc tránh né những vấn đề sâu sắc. Sự nhạy cảm với lời chỉ trích đôi khi khiến bạn mất tự tin.",
                "advice": "Tập trung năng lượng sáng tạo của bạn vào một vài dự án quan trọng thay vì lan man. Hãy phát triển kỷ luật để hoàn thành những gì bạn bắt đầu. Sử dụng tài năng giao tiếp để truyền cảm hứng và nâng cao tinh thần người khác."
            },
            4: {
                "title": "Người Xây Dựng - Nền Tảng Vững Chắc",
                "traits": "Bạn là người đáng tin cậy, thực tế và có tổ chức tốt. Sự chăm chỉ, kiên trì và kỷ luật của bạn giúp biến ước mơ thành hiện thực. Bạn xây dựng mọi thứ với nền tảng vững chắc, từng bước một, và luôn hoàn thành những gì mình cam kết.",
                "career": "Kỹ sư, Kiến trúc sư, Kế toán, Quản lý dự án, Nhà thầu xây dựng, Phân tích dữ liệu, Lập trình viên. Bạn xuất sắc trong các lĩnh vực đòi hỏi sự chính xác, chi tiết và lập kế hoạch dài hạn.",
                "challenges": "Bạn có thể quá cứng nhắc, bảo thủ và khó thích nghi với thay đổi. Xu hướng làm việc quá sức và bỏ qua sự cân bằng cuộc sống có thể gây kiệt sức. Đôi khi bạn cần học cách linh hoạt hơn và tin tưởng vào sự bất ổn.",
                "advice": "Hãy cân bằng giữa kỷ luật và linh hoạt. Cho phép bản thân thư giãn và tận hưởng quá trình, không chỉ tập trung vào kết quả. Sự kiên định của bạn là tài sản quý giá, nhưng đừng sợ thử nghiệm những cách tiếp cận mới."
            },
            5: {
                "title": "Người Tự Do - Nhà Thám Hiểm Cuộc Đời",
                "traits": "Bạn khao khát tự do, phiêu lưu và trải nghiệm mới. Sự đa năng, thích nghi và tò mò không ngừng khiến bạn luôn tìm kiếm kiến thức và khám phá. Bạn mang lại năng lượng tươi mới và sự thay đổi tích cực cho mọi nơi bạn đến.",
                "career": "Nhà báo, Hướng dẫn viên du lịch, Nhiếp ảnh gia, Chuyên gia marketing, Nhà tư vấn, Doanh nhân startup, Phi công. Bạn cần môi trường làm việc linh hoạt, đa dạng và không bị ràng buộc.",
                "challenges": "Sự bồn chồn và thiếu cam kết có thể khiến bạn bỏ dở nhiều điều. Bạn có thể tránh né trách nhiệm hoặc các mối quan hệ sâu sắc vì sợ bị gò bó. Xu hướng thiếu kiên nhẫn đôi khi khiến bạn bỏ lỡ cơ hội tốt.",
                "advice": "Học cách tìm tự do trong cam kết, không phải tránh né nó. Sử dụng năng lượng phiêu lưu của bạn để mở rộng chân trời, nhưng cũng học cách ổn định khi cần. Sự đa dạng là món quà, nhưng độ sâu cũng quan trọng không kém."
            },
            6: {
                "title": "Người Chăm Sóc - Trái Tim Yêu Thương",
                "traits": "Bạn mang trong mình tình yêu thương sâu sắc và khao khát chăm sóc người khác. Trách nhiệm, sự quan tâm chân thành và khả năng tạo ra môi trường ấm áp, hài hòa là điểm mạnh của bạn. Bạn tìm thấy ý nghĩa trong việc phục vụ và nâng đỡ cộng đồng.",
                "career": "Giáo viên, Y tá, Bác sĩ, Cố vấn gia đình, Nhà trị liệu, Đầu bếp, Nhà thiết kế nội thất, Nhân viên xã hội. Bạn thịnh vượng trong các vai trò nuôi dưỡng và hỗ trợ người khác.",
                "challenges": "Xu hướng hy sinh bản thân quá mức có thể dẫn đến kiệt sức và oán giận. Bạn có thể quá can thiệp vào cuộc sống người khác hoặc mong đợi sự đáp lễ. Học cách chăm sóc bản thân cũng quan trọng như chăm sóc người khác.",
                "advice": "Đặt ranh giới lành mạnh và nhớ rằng bạn không thể cứu vãn tất cả mọi người. Sự chăm sóc của bạn nên bắt đầu từ chính mình. Cho phép người khác học hỏi từ sai lầm của họ thay vì luôn cứu giúp."
            },
            7: {
                "title": "Người Tìm Kiếm - Nhà Hiền Triết",
                "traits": "Bạn có trí tuệ sâu sắc và khao khát tìm hiểu ý nghĩa đằng sau mọi thứ. Khả năng phân tích, trực giác mạnh mẽ và sự tò mò về tâm linh khiến bạn không ngừng tìm kiếm chân lý. Bạn cần thời gian một mình để suy ngẫm và kết nối với nội tâm.",
                "career": "Nhà nghiên cứu, Triết gia, Nhà khoa học, Giáo viên tâm linh, Nhà tâm lý học, Nhà phân tích, Lập trình viên. Bạn xuất sắc trong các lĩnh vực đòi hỏi tư duy sâu sắc và nghiên cứu kỹ lưỡng.",
                "challenges": "Bạn có thể quá cô lập, xa cách và khó gần. Xu hướng hoàn hảo chủ nghĩa đôi khi khiến bạn chỉ trích bản thân và người khác quá mức. Sự hoài nghi có thể cản trở bạn mở lòng với những trải nghiệm mới.",
                "advice": "Cân bằng giữa thế giới nội tâm và thế giới bên ngoài. Hãy chia sẻ sự thông thái của bạn với người khác thay vì giữ nó cho riêng mình. Tin tưởng vào trực giác và cho phép bản thân trải nghiệm cuộc sống, không chỉ phân tích nó."
            },
            8: {
                "title": "Người Thành Đạt - Bậc Thầy Quyền Lực",
                "traits": "Bạn mang trong mình sức mạnh, quyết tâm và tham vọng vĩ đại. Khả năng lãnh đạo, tầm nhìn chiến lược và sự tự tin giúp bạn đạt được thành công vượt trội. Bạn hiểu rõ giá trị của công việc chăm chỉ và không ngại đương đầu với thách thức để đạt được mục tiêu.",
                "career": "Giám đốc điều hành, Doanh nhân, Cố vấn tài chính, Luật sư, Chính khách, Nhà đầu tư, Nhà phát triển bất động sản. Bạn thịnh vượng trong các vai trò quyền lực và quản lý nguồn lực lớn.",
                "challenges": "Nguy cơ nghiện việc, coi trọng vật chất quá mức và bỏ qua các giá trị tinh thần. Bạn có thể trở nên độc đoán hoặc không cân bằng giữa công việc và cuộc sống. Đôi khi bạn cần học cách buông bỏ sự kiểm soát.",
                "advice": "Sử dụng quyền lực và thành công của bạn để tạo ra tác động tích cực. Hãy nhớ rằng thành công thực sự không chỉ đo bằng tài sản mà còn bằng di sản bạn để lại. Cân bằng giữa tham vọng và nhân văn."
            },
            9: {
                "title": "Người Nhân Đạo - Linh Hồn Cao Thượng",
                "traits": "Bạn có trái tim rộng lớn và khao khát phục vụ nhân loại. Lòng từ bi sâu sắc, sự hào phóng và tầm nhìn toàn cầu giúp bạn kết nối với mọi người. Bạn là người lý tưởng, nghệ sĩ của cuộc đời và luôn tìm cách làm cho thế giới tốt đẹp hơn.",
                "career": "Nhà hoạt động xã hội, Nghệ sĩ, Nhà nhân đạo, Giáo viên, Bác sĩ, Nhà trị liệu, Nhà tư vấn phi lợi nhuận. Bạn tìm thấy ý nghĩa trong việc phục vụ cộng đồng và tạo ra thay đổi tích cực.",
                "challenges": "Bạn có thể quá lý tưởng hóa mọi thứ và thất vọng khi thực tế không đáp ứng kỳ vọng. Xu hướng hi sinh bản thân quá mức có thể dẫn đến kiệt sức. Đôi khi bạn cần học cách buông bỏ những gì không thuộc về bạn.",
                "advice": "Hãy chăm sóc bản thân trước khi chăm sóc thế giới. Sử dụng sự thông thái và từ bi của bạn một cách cân bằng. Chấp nhận rằng bạn không thể thay đổi tất cả mọi thứ, nhưng mỗi hành động nhỏ đều có ý nghĩa."
            },
            11: {
                "title": "Bậc Thầy Trực Giác - Người Truyền Cảm Hứng",
                "traits": "Bạn sở hữu trực giác mạnh mẽ và khả năng kết nối với nguồn năng lượng cao hơn. Bạn là nguồn cảm hứng tự nhiên, có tầm nhìn sâu sắc về tâm linh và khả năng soi sáng con đường cho người khác. Sự nhạy cảm đặc biệt giúp bạn cảm nhận những điều mà người khác không thấy.",
                "career": "Giáo viên tâm linh, Cố vấn, Nghệ sĩ, Nhà tâm lý học, Nhà trị liệu năng lượng, Nhà tiên tri, Diễn giả truyền cảm hứng. Bạn có sứ mệnh nâng cao ý thức của nhân loại.",
                "challenges": "Sự nhạy cảm cao độ có thể khiến bạn dễ bị tổn thương và choáng ngợp. Bạn có thể gặp khó khăn trong việc xử lý các vấn đề thực tế và dễ bị căng thẳng. Áp lực từ tiềm năng cao có thể gây stress.",
                "advice": "Học cách bảo vệ năng lượng và thiết lập ranh giới. Hãy tin tưởng vào trực giác mạnh mẽ của bạn và sử dụng nó để dẫn dắt người khác. Cân bằng giữa thế giới tâm linh và vật chất là chìa khóa cho sự thành công của bạn."
            },
            22: {
                "title": "Bậc Thầy Xây Dựng - Kiến Trúc Sư Ước Mơ",
                "traits": "Bạn kết hợp tầm nhìn cao cả với khả năng thực thi thực tế tuyệt vời. Bạn có sức mạnh biến những ước mơ lớn lao thành hiện thực hữu hình. Khả năng lãnh đạo xuất chúng và sự kiên trì phi thường giúp bạn tạo ra những di sản lâu dài.",
                "career": "Kiến trúc sư lớn, Doanh nhân quốc tế, Lãnh đạo chính trị, Nhà phát triển dự án lớn, Giám đốc điều hành tổ chức toàn cầu. Bạn có khả năng tạo ra những thay đổi có ảnh hưởng rộng lớn.",
                "challenges": "Áp lực từ tiềm năng vĩ đại có thể gây căng thẳng và lo lắng. Bạn có thể đặt ra những kỳ vọng quá cao cho bản thân và người khác. Cần học cách cân bằng giữa tham vọng và sức khỏe tinh thần.",
                "advice": "Tin tưởng vào khả năng phi thường của bạn nhưng đừng để nó trở thành gánh nặng. Hãy kiên nhẫn với bản thân trong hành trình dài. Sử dụng sức mạnh của bạn để tạo ra những thay đổi tích cực cho nhân loại, không chỉ cho lợi ích cá nhân."
            }
        }
        return meanings.get(number, {
            "title": "Số Đặc Biệt",
            "traits": "Bạn mang một năng lượng độc đáo cần được khám phá sâu hơn.",
            "career": "Hãy tìm kiếm lĩnh vực phù hợp với bản chất thực sự của bạn.",
            "challenges": "Mỗi con số đều có những bài học riêng.",
            "advice": "Hãy lắng nghe trực giác và tin vào con đường của chính mình."
        })

async def calculate_numerology(user_id: str, name: str, birth_date: datetime) -> Dict:
    calculator = NumerologyCalculator()
    
    life_path = calculator.calculate_life_path_number(birth_date)
    expression = calculator.calculate_expression_number(name)
    soul_urge = calculator.calculate_soul_urge_number(name)
    personality = calculator.calculate_personality_number(name)
    
    result = {
        "life_path": {
            "number": life_path,
            **calculator.get_number_meaning(life_path)
        },
        "expression": {
            "number": expression,
            **calculator.get_number_meaning(expression)
        },
        "soul_urge": {
            "number": soul_urge,
            **calculator.get_number_meaning(soul_urge)
        },
        "personality": {
            "number": personality,
            **calculator.get_number_meaning(personality)
        }
    }
    
    # Save to history
    history_entry = {
        "user_id": user_id,
        "type": "numerology",
        "result_summary": f"Life Path: {life_path}, Expression: {expression}",
        "result_detail": result,
        "created_at": datetime.now()
    }
    
    await fortune_history.insert_one(history_entry)
    
    return result