from datetime import datetime
from typing import Dict, List
from ..database.mongodb import fortune_history
from .numerology import NumerologyCalculator
from .zodiac import ZodiacCalculator

class LoveCalculator:
    @staticmethod
    def calculate_name_compatibility(name1: str, name2: str) -> float:
        # Calculate numerology numbers for both names
        calc = NumerologyCalculator()
        name1_number = calc.calculate_expression_number(name1)
        name2_number = calc.calculate_expression_number(name2)
        
        # Define compatibility scores for different number combinations
        number_compatibility = {
            (1, 1): 80, (1, 3): 90, (1, 5): 85, (1, 7): 70, (1, 9): 85,
            (2, 2): 85, (2, 4): 90, (2, 6): 95, (2, 8): 80,
            (3, 3): 75, (3, 5): 85, (3, 7): 80, (3, 9): 90,
            (4, 4): 80, (4, 6): 90, (4, 8): 95,
            (5, 5): 70, (5, 7): 85, (5, 9): 80,
            (6, 6): 85, (6, 8): 90,
            (7, 7): 75, (7, 9): 85,
            (8, 8): 80,
            (9, 9): 85
        }
        
        # Get compatibility score (considering both combinations)
        score = number_compatibility.get(
            (name1_number, name2_number),
            number_compatibility.get((name2_number, name1_number), 75)
        )
        
        return score

    @staticmethod
    def calculate_birth_date_compatibility(date1: datetime, date2: datetime) -> float:
        # Get zodiac signs
        calc = ZodiacCalculator()
        sign1 = calc.get_zodiac_sign(date1)
        sign2 = calc.get_zodiac_sign(date2)
        
        # Get zodiac compatibility
        compatibility = calc.get_compatibility(sign1, sign2)
        return compatibility["compatibility_score"]

    @staticmethod
    def get_compatibility_description(score: float) -> Dict[str, str]:
        if score >= 90:
            return {
                "level": "Tuyệt Vời - Linh Hồn Song Sinh",
                "emoji": "💕✨",
                "description": """Hai bạn có sự kết nối đặc biệt và hiếm có! Năng lượng của hai người không chỉ bổ trợ mà còn khuếch đại lẫn nhau, tạo nên một mối quan hệ hài hòa sâu sắc. 

Sự tương hợp này cho thấy hai bạn có thể hiểu nhau ở mức độ tâm linh, nơi lời nói đôi khi trở nên không cần thiết. Bạn có khả năng cảm nhận cảm xúc và suy nghĩ của nhau một cách tự nhiên, tạo nên một sự đồng điệu kỳ diệu.

Trong mối quan hệ này, cả hai đều cảm thấy được chấp nhận hoàn toàn với con người thật của mình. Sự khác biệt giữa hai người không phải là rào cản mà là nguồn cảm hứng giúp mỗi người trưởng thành. Tình yêu ở đây không chỉ là cảm xúc mà là sự hòa quyện của hai tâm hồn, hai số phận được định sẵn để gặp nhau.""",
                "advice": """Hãy trân trọng món quà quý giá này từ vũ trụ! Mối quan hệ đặc biệt như thế này không đến với mọi người, vì vậy hãy nuôi dưỡng nó với tất cả tình yêu và sự chân thành.

**Giao tiếp sâu sắc:** Dù hai bạn hiểu nhau tốt, đừng bao giờ ngừng chia sẻ suy nghĩ và cảm xúc. Hãy tạo không gian an toàn để cả hai có thể thể hiện bản thân một cách chân thật nhất, kể cả những khía cạnh yếu đuối.

**Tôn trọng cá nhân:** Trong khi hai bạn rất hợp nhau, hãy nhớ rằng mỗi người vẫn là một cá thể riêng biệt. Cho nhau không gian để phát triển bản thân, theo đuổi đam mê riêng, và duy trì những mối quan hệ khác. Sự độc lập này sẽ làm mối quan hệ thêm phần phong phú.

**Chia sẻ ước mơ:** Hãy xây dựng tương lai chung dựa trên những giá trị và ước mơ của cả hai. Lập kế hoạch cho những mục tiêu lớn và nhỏ, và cùng nhau biến chúng thành hiện thực. Sự đồng lòng trong tầm nhìn sẽ làm tình yêu của bạn ngày càng bền chặt.

**Duy trì sự lãng mạn:** Đừng để thói quen làm mờ đi sự kỳ diệu. Tạo ra những bất ngờ nhỏ, thể hiện tình cảm thường xuyên, và không ngừng tìm cách khiến nhau cảm thấy được yêu thương và trân trọng.

**Vượt qua thử thách cùng nhau:** Khi khó khăn đến (và chúng sẽ đến), hãy nhớ rằng hai bạn là một đội. Đối mặt với vấn đề với tư cách là đối tác, không phải là đối thủ. Sức mạnh kết hợp của hai bạn có thể vượt qua mọi thử thách.""",
                "strengths": [
                    "Hiểu nhau sâu sắc ở cấp độ tâm linh",
                    "Giao tiếp tự nhiên và trôi chảy",
                    "Hỗ trợ lẫn nhau trong mọi hoàn cảnh",
                    "Cân bằng và bổ sung năng lượng cho nhau",
                    "Tin tưởng tuyệt đối và sự trung thành"
                ],
                "growth_areas": [
                    "Tránh phụ thuộc quá mức vào nhau",
                    "Duy trì sự tươi mới và bất ngờ",
                    "Giải quyết xung đột một cách xây dựng",
                    "Cân bằng giữa 'chúng ta' và 'tôi'"
                ]
            }
        elif score >= 80:
            return {
                "level": "Rất Tốt - Hài Hòa Tuyệt Vời",
                "emoji": "💖🌟",
                "description": """Hai bạn có sự tương hợp mạnh mẽ với tiềm năng tuyệt vời cho một mối quan hệ viên mãn và bền vững. Năng lượng của hai người kết nối một cách tự nhiên, tạo nên sự cân bằng đẹp đẽ.

Mối quan hệ này được xây dựng trên nền tảng vững chắc của sự tôn trọng, tin tưởng và hiểu biết lẫn nhau. Hai bạn có nhiều điểm chung về giá trị sống, cách nhìn cuộc đời, và mục tiêu trong tương lai. Điều này tạo ra một nền tảng vững chắc cho tình yêu phát triển.

Bạn cảm thấy thoải mái khi là chính mình bên cạnh người kia. Có sự cân bằng tốt giữa sự đồng điệu và sự đa dạng - hai bạn đủ giống nhau để hiểu nhau, nhưng cũng đủ khác biệt để giữ cho mối quan hệ luôn thú vị và đầy màu sắc.

Tình yêu ở đây mang lại cảm giác an toàn, ấm áp và niềm vui. Hai bạn có khả năng xây dựng một cuộc sống chung đầy ý nghĩa, nơi cả hai đều có thể phát triển và thực hiện tiềm năng của mình.""",
                "advice": """Mối quan hệ của bạn có nền tảng vững chắc, nhưng vẫn cần được chăm sóc và nuôi dưỡng để nở hoa rực rỡ.

**Giao tiếp chân thành:** Duy trì thói quen chia sẻ suy nghĩ và cảm xúc một cách cởi mở. Đừng giả định rằng người kia "phải biết" điều bạn đang nghĩ hay cảm nhận. Hãy thể hiện rõ ràng nhu cầu, mong muốn và ranh giới của mình. Lắng nghe tích cực khi đối phương chia sẻ, không chỉ nghe để đáp lại mà nghe để hiểu.

**Đầu tư thời gian chất lượng:** Trong nhịp sống hối hả, hãy chủ động tạo ra những khoảnh khắc đặc biệt cho hai người. Không nhất thiết phải là những hoạt động xa hoa - đôi khi chỉ là buổi tối cùng nấu ăn, đi dạo, hay ngồi trò chuyện mà không có sự phân tâm của điện thoại.

**Xử lý bất đồng khéo léo:** Khi có xung đột (điều này hoàn toàn bình thường), hãy nhớ rằng mục tiêu không phải là "thắng" mà là tìm giải pháp cùng có lợi. Đừng để ego chi phối. Hãy thể hiện sự tôn trọng ngay cả khi không đồng ý, và sẵn sàng thỏa hiệp khi cần thiết.

**Khám phá và phát triển cùng nhau:** Hãy thử những hoạt động mới, học hỏi những kỹ năng mới, và khám phá thế giới cùng nhau. Những trải nghiệm chung sẽ tạo ra kỷ niệm đẹp và củng cố sự kết nối. Đồng thời, hỗ trợ nhau trong hành trình phát triển cá nhân.

**Tôn vinh những điểm mạnh của nhau:** Hãy là người cổ vũ lớn nhất của đối phương. Công nhận và đánh giá cao những nỗ lực, thành tựu và phẩm chất tốt đẹp của nhau. Lời khen chân thành có sức mạnh to lớn trong việc nuôi dưỡng tình yêu.

**Giữ gìn sự lãng mạn:** Đừng để tình yêu trở thành thói quen. Tạo ra những bất ngờ nhỏ, viết những lời nhắn yêu thương, và thể hiện tình cảm qua cả lời nói lẫn hành động. Sự lãng mạn không phải chỉ dành cho giai đoạn đầu mối quan hệ.""",
                "strengths": [
                    "Nền tảng tin tưởng và tôn trọng vững chắc",
                    "Giá trị sống và mục tiêu tương đồng",
                    "Giao tiếp hiệu quả và cởi mở",
                    "Hỗ trợ và động viên lẫn nhau",
                    "Cân bằng tốt giữa đồng điệu và đa dạng"
                ],
                "growth_areas": [
                    "Duy trì sự lãng mạn và tươi mới",
                    "Quản lý xung đột một cách xây dựng",
                    "Cân bằng giữa thời gian chung và riêng tư",
                    "Thích nghi với sự thay đổi của nhau"
                ]
            }
        elif score >= 70:
            return {
                "level": "Tốt - Tiềm Năng Phát Triển",
                "emoji": "💗🌱",
                "description": """Hai bạn có một sự tương hợp tốt với tiềm năng phát triển thành một mối quan hệ ý nghĩa và bền vững. Mặc dù có thể có một số khác biệt, nhưng những điểm chung của hai bạn đủ mạnh để tạo nên nền tảng cho tình yêu.

Mối quan hệ này yêu cầu cả hai phải có sự nỗ lực và cam kết, nhưng đó không phải là điều tiêu cực. Trên thực tế, những thử thách này có thể giúp hai bạn trưởng thành và hiểu nhau sâu sắc hơn. Khi hai người cùng vượt qua khó khăn, tình yêu sẽ trở nên bền chặt hơn.

Bạn có thể nhận thấy rằng hai người có những cách tiếp cận khác nhau đối với cuộc sống, nhưng đây có thể là một lợi thế nếu bạn biết cách tận dụng. Mỗi người mang đến góc nhìn độc đáo giúp mở rộng chân trời của người kia. Sự khác biệt này, nếu được tôn trọng và đánh giá cao, có thể làm phong phú thêm cuộc sống của cả hai.

Thành công của mối quan hệ phụ thuộc vào khả năng thấu hiểu, kiên nhẫn và sẵn sàng học hỏi từ nhau. Với thái độ đúng đắn và nỗ lực chung, hai bạn hoàn toàn có thể xây dựng một mối quan hệ hạnh phúc và viên mãn.""",
                "advice": """Mối quan hệ của bạn giống như một khu vườn đẹp - nó cần được chăm sóc và nuôi dưỡng thường xuyên để nở hoa.

**Tìm hiểu sâu hơn về nhau:** Hãy dành thời gian thực sự tìm hiểu về đối phương - không chỉ ở bề mặt mà ở tận sâu thẳm. Tìm hiểu về quá khứ, ước mơ, nỗi sợ hãi, và những giá trị cốt lõi của nhau. Càng hiểu nhau nhiều, càng dễ dàng kết nối và đồng cảm.

**Xây dựng điểm chung:** Tích cực tạo ra những trải nghiệm chung và phát triển những sở thích chung. Điều này có thể là một môn thể thao, một sở thích nghệ thuật, hoặc đơn giản là một chương trình truyền hình yêu thích. Những điểm chung này sẽ tạo ra sự gắn kết và cho bạn nhiều chủ đề để trò chuyện.

**Tôn trọng sự khác biệt:** Đừng cố gắng thay đổi đối phương để họ giống bạn hơn. Thay vào đó, hãy tìm hiểu tại sao họ có cách suy nghĩ và hành động như vậy. Đôi khi những khác biệt chính là điều làm cho mối quan hệ thêm phần thú vị. Học cách đánh giá cao những phẩm chất mà bạn không có.

**Giao tiếp rõ ràng và kiên nhẫn:** Vì hai bạn có thể có cách giao tiếp khác nhau, hãy đặc biệt chú ý đến việc thể hiện rõ ràng ý định và cảm xúc của mình. Đừng giả định. Hỏi khi không chắc chắn. Lắng nghe không phán xét. Kiên nhẫn khi giải thích và tìm hiểu.

**Xử lý xung đột một cách xây dựng:** Khi có bất đồng (và chắc chắn sẽ có), hãy tập trung vào vấn đề chứ không phải vào tính cách của người kia. Sử dụng "tôi cảm thấy..." thay vì "bạn luôn luôn...". Tìm kiếm giải pháp thỏa hiệp thay vì cố gắng "thắng" cuộc tranh luận.

**Đầu tư nỗ lực liên tục:** Đừng bằng lòng với hiện trạng. Luôn tìm cách cải thiện mối quan hệ. Đọc sách về tình yêu, tham gia các hoạt động cùng nhau, hoặc thậm chí tham khảo tư vấn nếu cần. Nỗ lực của bạn sẽ được đền đáp xứng đáng.

**Tạo kỷ niệm đẹp:** Những trải nghiệm tích cực chung sẽ tạo ra một kho tàng kỷ niệm giúp hai bạn vượt qua những thời điểm khó khăn. Hãy tạo ra những khoảnh khắc đặc biệt thường xuyên.""",
                "strengths": [
                    "Có điểm chung đủ để xây dựng nền tảng",
                    "Khác biệt tạo nên sự đa dạng và thú vị",
                    "Tiềm năng học hỏi và trưởng thành cùng nhau",
                    "Động lực để nỗ lực vì mối quan hệ"
                ],
                "growth_areas": [
                    "Cần nhiều thời gian để thấu hiểu nhau",
                    "Học cách giao tiếp hiệu quả hơn",
                    "Xây dựng thêm điểm chung và sở thích chung",
                    "Phát triển kỹ năng giải quyết xung đột",
                    "Cân bằng giữa sự độc lập và sự gắn kết"
                ]
            }
        elif score >= 60:
            return {
                "level": "Trung Bình - Cần Nỗ Lực",
                "emoji": "💛⚖️",
                "description": """Mối quan hệ của hai bạn nằm ở vùng trung gian - có cả những điểm tương hợp và những thách thức đáng kể. Điều này không có nghĩa là mối quan hệ không thể thành công, nhưng nó đòi hỏi sự cam kết mạnh mẽ và nỗ lực từ cả hai phía.

Hai bạn có thể nhận thấy rằng đôi khi dễ dàng kết nối với nhau, nhưng đôi khi lại cảm thấy như đang nói hai ngôn ngữ khác nhau. Có những khoảnh khắc hòa hợp tuyệt vời, xen kẽ với những lúc hiểu lầm và căng thẳng. Sự dao động này là hoàn toàn bình thường trong trường hợp của bạn.

Những khác biệt giữa hai người có thể liên quan đến giá trị sống, cách thể hiện tình cảm, phong cách giao tiếp, hoặc mục tiêu cuộc sống. Những khác biệt này không phải là bất khả thi, nhưng chúng đòi hỏi sự nhận thức, chấp nhận và thích nghi.

Thành công của mối quan hệ này phụ thuộc rất nhiều vào mức độ sẵn sàng của cả hai trong việc làm việc cùng nhau để khắc phục những khác biệt. Nếu cả hai đều có động lực và cam kết, những thách thức này có thể được vượt qua. Tuy nhiên, nếu một hoặc cả hai người không sẵn sàng nỗ lực, mối quan hệ có thể gặp nhiều khó khăn.""",
                "advice": """Mối quan hệ của bạn giống như một chuyến leo núi - đầy thử thách nhưng cũng có thể đạt được đỉnh cao tuyệt đẹp nếu cả hai cùng nỗ lực.

**Đánh giá thực tế:** Hãy thành thật với bản thân về những gì bạn mong đợi và những gì bạn sẵn sàng cam kết. Liệu bạn có đủ động lực để vượt qua những thách thức? Liệu mối quan hệ này có đáng để bạn đầu tư không? Không có câu trả lời đúng hay sai - chỉ có sự trung thực với bản thân.

**Giao tiếp cực kỳ quan trọng:** Trong mối quan hệ này, giao tiếp không chỉ là quan trọng - nó là then chốt để tồn tại. Hãy nói rõ ràng về nhu cầu, mong đợi, và ranh giới của bạn. Đừng giả định điều gì cả. Kiểm tra lại sự hiểu biết thường xuyên. Sử dụng câu hỏi như "Ý bạn là...?" hay "Bạn có thể giải thích thêm được không?" để tránh hiểu lầm.

**Tìm điểm chung:** Hãy tích cực tìm kiếm và xây dựng những điểm chung. Điều gì làm cả hai bạn cùng phấn khích? Những giá trị nào bạn cùng chia sẻ? Những hoạt động nào cả hai đều thích? Tập trung vào những điểm này và để chúng trở thành nền tảng của mối quan hệ.

**Chấp nhận và thích nghi:** Có những khác biệt mà bạn không thể (và không nên cố gắng) thay đổi. Học cách chấp nhận những khác biệt này và tìm cách thích nghi. Đôi khi điều này có nghĩa là thỏa hiệp, đôi khi là tìm cách để cả hai cùng được thỏa mãn mặc dù có cách tiếp cận khác nhau.

**Quản lý kỳ vọng:** Đừng kỳ vọng mối quan hệ sẽ luôn dễ dàng. Sẽ có những ngày khó khăn, và điều đó không có nghĩa là mối quan hệ "sai". Tuy nhiên, hãy đảm bảo rằng những ngày tốt đẹp nhiều hơn những ngày khó khăn. Nếu bạn cảm thấy kiệt sức hoặc không hạnh phúc phần lớn thời gian, đó là dấu hiệu cần cân nhắc lại.

**Tìm kiếm hỗ trợ:** Đừng ngần ngại tìm kiếm sự giúp đỡ từ bên ngoài. Tham vấn tình yêu, sách về mối quan hệ, hoặc lời khuyên từ những người có kinh nghiệm có thể cung cấp công cụ và góc nhìn mới để cải thiện mối quan hệ.

**Chăm sóc bản thân:** Đừng quên chăm sóc sức khỏe tinh thần và cảm xúc của riêng bạn. Một mối quan hệ không nên làm bạn kiệt sức hoặc đánh mất bản thân. Duy trì những sở thích, mối quan hệ và hoạt động độc lập của bạn.

**Định kỳ đánh giá lại:** Thường xuyên (có thể mỗi vài tháng) ngồi lại với nhau để đánh giá xem mối quan hệ đang tiến triển như thế nào. Những gì đang hiệu quả? Những gì cần cải thiện? Cả hai có đang hạnh phúc không?""",
                "strengths": [
                    "Có tiềm năng nếu cả hai cùng cam kết",
                    "Thách thức có thể giúp cả hai trưởng thành",
                    "Còn có điểm chung để xây dựng"
                ],
                "growth_areas": [
                    "Cần nỗ lực đáng kể trong giao tiếp",
                    "Phải chủ động xây dựng sự kết nối",
                    "Học cách thỏa hiệp và thích nghi",
                    "Quản lý xung đột hiệu quả",
                    "Cân bằng giữa cho và nhận",
                    "Tìm điểm chung giữa những khác biệt lớn"
                ]
            }
        else:
            return {
                "level": "Thách Thức - Cần Cân Nhắc Kỹ",
                "emoji": "💙🔄",
                "description": """Mối quan hệ giữa hai bạn có những khác biệt đáng kể có thể tạo ra nhiều thách thức. Năng lượng, giá trị, và cách tiếp cận cuộc sống của hai người có vẻ khác nhau ở mức độ cơ bản, điều này có thể dẫn đến những hiểu lầm thường xuyên và sự mệt mỏi về mặt cảm xúc.

Điều quan trọng cần hiểu là điểm số thấp không có nghĩa là tình yêu không thể tồn tại, nhưng nó cho thấy rằng mối quan hệ này sẽ đòi hỏi nỗ lực phi thường từ cả hai phía. Hai bạn có thể cảm thấy như đang liên tục "làm việc" trong mối quan hệ thay vì tự nhiên tận hưởng nó.

Có những cặp đôi với sự tương hợp thấp vẫn có thể xây dựng được mối quan hệ bền vững, nhưng điều này thường đòi hỏi sự trưởng thành cao, khả năng tự nhận thức mạnh mẽ, và cam kết không ngừng nghỉ. Hai người phải sẵn sàng thay đổi, học hỏi, và thích nghi liên tục.

Trước khi đầu tư sâu hơn vào mối quan hệ này, hãy tự hỏi bản thân một cách trung thực: Liệu bạn có thực sự hạnh phúc? Liệu những thách thức này có làm bạn trưởng thành hay chúng đang làm bạn kiệt sức? Liệu tình yêu có đủ mạnh để bù đắp cho những khó khăn?

Đôi khi, lựa chọn khó khăn nhất lại là lựa chọn khôn ngoan nhất. Nếu mối quan hệ liên tục khiến bạn đau khổ hơn là hạnh phúc, có thể đó là dấu hiệu rằng hai bạn không thực sự phù hợp với nhau, và điều đó hoàn toàn không sao.""",
                "advice": """Đây là thời điểm cần sự trung thực sâu sắc với bản thân và sự suy ngẫm nghiêm túc về tương lai.

**Đánh giá thành thật và sâu sắc:** Hãy dành thời gian thực sự suy nghĩ về mối quan hệ này. Đừng để cảm xúc tạm thời hoặc sự quen thuộc làm lu mờ sự thật. Hỏi bản thân những câu hỏi khó: Tôi có thực sự hạnh phúc không? Mối quan hệ này có làm tôi trở thành phiên bản tốt hơn của chính mình không? Tôi có cảm thấy được yêu thương và trân trọng không? Liệu tôi có đang hy sinh quá nhiều không?

**Nhận diện các dấu hiệu cảnh báo:** Hãy chú ý đến các dấu hiệu của một mối quan hệ không lành mạnh: xung đột thường xuyên, thiếu tôn trọng, giao tiếp tiêu cực, cảm giác kiệt sức liên tục, mất đi bản thân, hoặc cảm giác bị kiểm soát. Nếu những dấu hiệu này xuất hiện, đó là lúc phải hành động.

**Giao tiếp cực kỳ rõ ràng:** Nếu quyết định tiếp tục, giao tiếp phải trở thành ưu tiên hàng đầu. Không để bất cứ điều gì không được nói ra. Sử dụng "tôi cảm thấy..." và tránh buộc tội. Lắng nghe không phán xét, ngay cả khi khó khăn. Có thể cần học các kỹ năng giao tiếp chuyên sâu hoặc tìm kiếm tư vấn chuyên nghiệp.

**Thiết lập ranh giới rõ ràng:** Ranh giới lành mạnh là cần thiết trong bất kỳ mối quan hệ nào, nhưng đặc biệt quan trọng ở đây. Hãy rõ ràng về những gì bạn có thể chấp nhận và không thể chấp nhận. Tôn trọng ranh giới của nhau và không cố gắng vi phạm chúng.

**Tìm kiếm sự trợ giúp chuyên nghiệp:** Đừng do dự về việc tìm kiếm tư vấn tình yêu từ chuyên gia. Một người thứ ba trung lập có thể giúp hai bạn giao tiếp hiệu quả hơn, hiểu nhau sâu hơn, và phát triển các chiến lược để vượt qua khác biệt. Nếu chỉ một người muốn đi tư vấn, hãy đi một mình để được hỗ trợ.

**Phát triển bản thân trước tiên:** Đôi khi vấn đề không chỉ ở sự tương hợp mà còn ở sự trưởng thành cá nhân. Hãy làm việc để trở thành phiên bản tốt nhất của chính mình - độc lập với mối quan hệ. Điều trị liệu pháp cá nhân, phát triển bản thân, và xây dựng lòng tự trọng có thể giúp bạn đưa ra quyết định sáng suốt hơn.

**Chuẩn bị cho mọi khả năng:** Hãy thành thật rằng mối quan hệ này có thể không kéo dài. Đó không phải là thất bại - đó là sự trưởng thành khi nhận ra rằng không phải tình yêu nào cũng được định sẵn để tồn tại mãi. Đôi khi, tình yêu có nghĩa là biết buông tay để cả hai có thể tìm được hạnh phúc thực sự.

**Tin vào trực giác:** Sâu thẳm trong lòng, bạn có thể đã biết câu trả lời. Hãy lắng nghe tiếng nói nội tâm của mình. Nếu mọi thứ luôn cảm thấy như một cuộc đấu tranh, nếu bạn thường xuyên tự hỏi "có phải thế này không?", đó có thể là câu trả lời của vũ trụ.

**Yêu thương bản thân:** Dù kết quả như thế nào, hãy nhớ rằng bạn xứng đáng được hạnh phúc, được tôn trọng, và được yêu thương. Đừng ở trong một mối quan hệ chỉ vì sợ cô đơn, vì đã đầu tư quá nhiều, hoặc vì hy vọng người kia sẽ thay đổi. Tình yêu bản thân là nền tảng của mọi mối quan hệ lành mạnh.

**Cho phép bản thân buông bỏ nếu cần:** Nếu sau khi cân nhắc kỹ lưỡng, bạn quyết định rằng mối quan hệ này không phù hợp, hãy có can đảm để buông tay. Kết thúc một mối quan hệ không phù hợp không phải là thất bại - đó là sự khôn ngoan. Nó mở ra cơ hội cho cả hai tìm được người thực sự phù hợp hơn.""",
                "strengths": [
                    "Thử thách có thể dạy bạn nhiều về bản thân",
                    "Nếu vượt qua được, sẽ rất mạnh mẽ",
                    "Học được tầm quan trọng của sự tương hợp"
                ],
                "growth_areas": [
                    "Đánh giá lại liệu mối quan hệ có phù hợp",
                    "Phát triển kỹ năng giao tiếp chuyên sâu",
                    "Học cách thiết lập và tôn trọng ranh giới",
                    "Tìm kiếm hỗ trợ chuyên nghiệp",
                    "Chăm sóc sức khỏe tinh thần của bản thân",
                    "Phát triển bản thân độc lập với mối quan hệ",
                    "Có thể cần cân nhắc về tương lai dài hạn"
                ]
            }

async def calculate_love_compatibility(
    user_id: str,
    name1: str,
    birth_date1: datetime,
    name2: str,
    birth_date2: datetime
) -> Dict:
    calculator = LoveCalculator()
    
    # Calculate different aspects of compatibility
    name_score = calculator.calculate_name_compatibility(name1, name2)
    birth_score = calculator.calculate_birth_date_compatibility(birth_date1, birth_date2)
    
    # Calculate overall compatibility score (weighted average)
    overall_score = (name_score * 0.4) + (birth_score * 0.6)
    
    result = {
        "overall_compatibility": round(overall_score, 2),
        "name_compatibility": round(name_score, 2),
        "zodiac_compatibility": round(birth_score, 2),
        **calculator.get_compatibility_description(overall_score)
    }
    
    # Save to history
    history_entry = {
        "user_id": user_id,
        "type": "love",
        "result_summary": f"Love compatibility: {round(overall_score)}%",
        "result_detail": result,
        "created_at": datetime.now()
    }
    
    await fortune_history.insert_one(history_entry)
    
    return result