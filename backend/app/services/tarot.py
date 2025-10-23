from datetime import datetime
from typing import Dict, List
from ..database.mongodb import fortune_history
import random

class TarotReader:
    MAJOR_ARCANA = [
        {
            "name": "The Fool - Kẻ Khờ",
            "number": 0,
            "emoji": "🌟",
            "keywords": ["Khởi đầu mới", "Tự do", "Niềm tin", "Ngây thơ"],
            "meanings": {
                "upright": {
                    "general": "Bạn đang ở ngưỡng cửa của một cuộc phiêu lưu mới đầy hứng hẹn. Đây là lúc để tin vào bản năng của mình và bước đi với trái tim rộng mở. Hãy để sự tự nhiên và niềm tin dẫn lối cho bạn, đừng sợ hãi những điều chưa biết. Đôi khi, sự ngây thơ chính là điểm mạnh giúp bạn nhìn thấy những khả năng mà người khác không thấy được.",
                    "love": "Trong tình yêu, đây là thời điểm để dám mạo hiểm. Nếu bạn đang độc thân, hãy mở lòng với những trải nghiệm mới. Nếu đã có người yêu, đây là lúc để thêm sự tự phát và vui vẻ vào mối quan hệ của bạn.",
                    "career": "Cơ hội nghề nghiệp mới đang chờ đợi. Đừng ngại theo đuổi con đường khác thường hoặc thử điều gì đó hoàn toàn mới. Niềm đam mê và sự tò mò của bạn sẽ dẫn đến thành công.",
                    "advice": "Hãy tin vào hành trình. Đừng quá lo lắng về kết quả mà hãy tận hưởng từng bước đi. Sự tự nhiên và chân thật của bạn chính là điểm sáng nhất."
                },
                "reversed": {
                    "general": "Có thể bạn đang quá liều lĩnh hoặc ngược lại, quá sợ hãi để bước tiếp. Hãy cân bằng giữa sự tự phát và thận trọng. Đừng để sự thiếu chuẩn bị khiến bạn gặp rủi ro không cần thiết.",
                    "love": "Cẩn thận với việc vội vàng trong các quyết định tình cảm. Sự thiếu cam kết hoặc ngược lại, cam kết quá nhanh có thể gây ra vấn đề.",
                    "career": "Bạn có thể đang bỏ lỡ cơ hội do thiếu kế hoạch hoặc ngược lại, quá sợ hãi để thử điều mới. Hãy tìm sự cân bằng.",
                    "advice": "Hãy dừng lại và đánh giá tình hình trước khi hành động. Chuẩn bị kỹ càng hơn nhưng đừng để sợ hãi làm bạn mất cơ hội."
                }
            }
        },
        {
            "name": "The Magician - Nhà Ảo Thuật",
            "number": 1,
            "emoji": "✨",
            "keywords": ["Sức mạnh", "Kỹ năng", "Thể hiện", "Tài nguyên"],
            "meanings": {
                "upright": {
                    "general": "Bạn có tất cả những gì cần thiết để thành công. Đây là lúc để khai thác tiềm năng và sử dụng kỹ năng của mình một cách hiệu quả nhất. Sự tập trung và quyết tâm của bạn có thể biến ý tưởng thành hiện thực. Hãy tin vào khả năng của bản thân.",
                    "love": "Bạn có sức mạnh để tạo ra mối quan hệ mà mình mong muốn. Hãy chủ động trong tình yêu, thể hiện cảm xúc và tạo ra những trải nghiệm ý nghĩa.",
                    "career": "Đây là thời điểm vàng cho sự nghiệp. Kỹ năng và kinh nghiệm của bạn đang ở đỉnh cao. Hãy tận dụng cơ hội để thể hiện bản thân và đạt được mục tiêu.",
                    "advice": "Hãy hành động với sự tự tin. Bạn có mọi công cụ cần thiết - giờ là lúc sử dụng chúng. Tập trung vào mục tiêu và bạn sẽ thấy kết quả."
                },
                "reversed": {
                    "general": "Có thể bạn đang lạm dụng quyền lực hoặc thao túng người khác. Hoặc ngược lại, bạn chưa nhận ra tiềm năng thật sự của mình. Hãy kiểm tra động cơ của bạn.",
                    "love": "Cẩn thận với sự thao túng trong các mối quan hệ. Hãy chân thật và không dùng mánh khóe để đạt được điều mình muốn.",
                    "career": "Bạn có thể đang không sử dụng hết khả năng của mình hoặc thiếu kế hoạch rõ ràng. Hãy đánh giá lại chiến lược.",
                    "advice": "Hãy kiểm tra động cơ và đảm bảo bạn đang sử dụng tài năng của mình một cách đạo đức. Đừng đánh giá thấp bản thân."
                }
            }
        },
        {
            "name": "The High Priestess - Nữ Tư Tế Tối Cao",
            "number": 2,
            "emoji": "🌙",
            "keywords": ["Trực giác", "Bí ẩn", "Tiềm thức", "Trí tuệ"],
            "meanings": {
                "upright": {
                    "general": "Hãy lắng nghe giọng nói nội tâm của bạn. Đáp án bạn tìm kiếm không nằm ở bên ngoài mà ở sâu trong tâm hồn bạn. Đây là thời điểm để tin vào trực giác và khám phá sự thật ẩn giấu. Sự im lặng và thiền định sẽ mang đến sự sáng suốt.",
                    "love": "Có những điều chưa được nói ra trong mối quan hệ của bạn. Hãy dành thời gian để hiểu sâu hơn về cảm xúc của mình và đối phương.",
                    "career": "Đừng vội vàng đưa ra quyết định. Hãy quan sát, học hỏi và để trực giác dẫn dắt. Có thể có thông tin ẩn giấu mà bạn cần khám phá.",
                    "advice": "Tin vào trực giác của bạn. Dành thời gian cho sự yên tĩnh và nội quan. Đáp án sẽ đến khi bạn lắng nghe bên trong."
                },
                "reversed": {
                    "general": "Bạn có thể đang bỏ qua giọng nói nội tâm hoặc để người khác quyết định thay vì tin vào trực giác của mình. Hãy kết nối lại với bản thân.",
                    "love": "Có thể có sự thiếu giao tiếp hoặc bí mật trong mối quan hệ. Hãy mở lòng và chia sẻ cảm xúc thật sự.",
                    "career": "Bạn đang bỏ qua các dấu hiệu quan trọng hoặc không tin vào bản năng nghề nghiệp của mình.",
                    "advice": "Hãy dừng lại và lắng nghe bản thân. Đừng để tiếng ồn bên ngoài át đi giọng nói nội tâm của bạn."
                }
            }
        },
        {
            "name": "The Empress - Nữ Hoàng",
            "number": 3,
            "emoji": "👑",
            "keywords": ["Sinh sản", "Nuôi dưỡng", "Dồi dào", "Sáng tạo"],
            "meanings": {
                "upright": {
                    "general": "Đây là thời kỳ của sự thịnh vượng và phát triển. Mọi thứ đang nảy nở xung quanh bạn. Hãy nuôi dưỡng các dự án và mối quan hệ của mình với tình yêu và sự chăm sóc. Sự sáng tạo của bạn đang ở đỉnh cao và thiên nhiên đang ủng hộ bạn.",
                    "love": "Tình yêu đang nở rộ. Đây có thể là thời điểm của sự kết hôn, có con, hoặc đơn giản là mối quan hệ đang phát triển sâu sắc hơn.",
                    "career": "Công việc của bạn đang cho ra quả ngọt. Các dự án đang phát triển tốt và có thể mang lại lợi ích vật chất đáng kể.",
                    "advice": "Hãy tận hưởng giai đoạn này và tiếp tục nuôi dưỡng những gì quan trọng với bạn. Đừng quên chăm sóc bản thân."
                },
                "reversed": {
                    "general": "Có thể bạn đang bỏ bê bản thân hoặc các dự án của mình. Sự thiếu cân bằng giữa cho và nhận có thể gây ra kiệt sức.",
                    "love": "Cẩn thận với việc quá phụ thuộc vào đối phương hoặc ngược lại, không nuôi dưỡng mối quan hệ đủ.",
                    "career": "Các dự án có thể bị trì hoãn hoặc không phát triển như mong đợi. Hãy đánh giá lại chiến lược.",
                    "advice": "Hãy tìm lại sự cân bằng. Chăm sóc bản thân trước khi chăm sóc người khác."
                }
            }
        },
        {
            "name": "The Emperor - Hoàng Đế",
            "number": 4,
            "emoji": "⚔️",
            "keywords": ["Quyền lực", "Cấu trúc", "Kiểm soát", "Lãnh đạo"],
            "meanings": {
                "upright": {
                    "general": "Đây là lúc để thiết lập trật tự và cấu trúc trong cuộc sống của bạn. Hãy lãnh đạo với sự tự tin và quyết đoán. Kỷ luật và tổ chức sẽ giúp bạn đạt được mục tiêu. Bạn có khả năng kiểm soát tình hình và tạo ra sự ổn định.",
                    "love": "Bạn hoặc đối phương đang đóng vai trò bảo vệ và hỗ trợ trong mối quan hệ. Sự cam kết và ổn định là quan trọng.",
                    "career": "Đây là thời điểm tốt để lãnh đạo, xây dựng hệ thống và thiết lập quyền uy. Tổ chức và kế hoạch sẽ mang lại thành công.",
                    "advice": "Hãy tin vào khả năng lãnh đạo của bạn. Tạo cấu trúc và kỷ luật, nhưng đừng quá cứng nhắc."
                },
                "reversed": {
                    "general": "Có thể bạn đang quá độc đoán hoặc ngược lại, thiếu kiểm soát. Sự mất cân bằng trong quyền lực có thể gây ra vấn đề.",
                    "love": "Cẩn thận với sự kiểm soát quá mức hoặc thiếu sự cam kết trong mối quan hệ.",
                    "career": "Có thể có xung đột về quyền lực hoặc thiếu cấu trúc rõ ràng trong công việc.",
                    "advice": "Hãy tìm sự cân bằng giữa lãnh đạo và lắng nghe. Đừng để quyền lực làm bạn mất đi sự linh hoạt."
                }
            }
        },
        {
            "name": "The Hierophant - Giáo Hoàng",
            "number": 5,
            "emoji": "📿",
            "keywords": ["Truyền thống", "Giáo dục", "Niềm tin", "Tuân thủ"],
            "meanings": {
                "upright": {
                    "general": "Đây là thời điểm để học hỏi từ truyền thống và những người có kinh nghiệm. Hãy tôn trọng các giá trị đã được kiểm chứng và tìm kiếm sự hướng dẫn từ người khôn ngoan. Giáo dục và tâm linh đang đóng vai trò quan trọng trong cuộc sống bạn.",
                    "love": "Mối quan hệ của bạn có thể đang tiến đến một bước cam kết chính thức như kết hôn hoặc đính hôn.",
                    "career": "Hãy học từ những người có kinh nghiệm và tuân theo các quy trình đã được chứng minh. Giáo dục và đào tạo sẽ mang lại lợi ích.",
                    "advice": "Hãy cởi mở với sự học hỏi và tôn trọng truyền thống, nhưng cũng đừng quên suy nghĩ độc lập."
                },
                "reversed": {
                    "general": "Bạn có thể đang cảm thấy bị hạn chế bởi các quy tắc và truyền thống. Hoặc bạn đang phá vỡ các chuẩn mực một cách không cần thiết.",
                    "love": "Có thể có xung đột về giá trị hoặc niềm tin trong mối quan hệ.",
                    "career": "Bạn có thể đang cảm thấy bị kìm hãm bởi hệ thống hoặc muốn phá vỡ các quy tắc.",
                    "advice": "Hãy tìm sự cân bằng giữa tôn trọng truyền thống và tự do cá nhân."
                }
            }
        },
        {
            "name": "The Lovers - Người Yêu",
            "number": 6,
            "emoji": "💕",
            "keywords": ["Tình yêu", "Lựa chọn", "Hòa hợp", "Quan hệ"],
            "meanings": {
                "upright": {
                    "general": "Bạn đang đối mặt với một quyết định quan trọng, đặc biệt là trong các mối quan hệ. Hãy lắng nghe trái tim nhưng cũng cân nhắc lý trí. Sự hòa hợp và kết nối sâu sắc đang có thể xảy ra. Đây là thời điểm của tình yêu đích thực và sự cam kết.",
                    "love": "Tình yêu chân thật đang nở rộ. Đây có thể là mối quan hệ định mệnh hoặc thời điểm để cam kết sâu hơn.",
                    "career": "Sự hợp tác và đối tác kinh doanh có thể mang lại thành công. Hãy chọn đồng minh của bạn một cách khôn ngoan.",
                    "advice": "Hãy lắng nghe cả trái tim và lý trí. Lựa chọn phù hợp với giá trị của bạn."
                },
                "reversed": {
                    "general": "Có thể có sự mất cân bằng trong các mối quan hệ hoặc bạn đang đưa ra lựa chọn sai lầm. Giá trị của bạn có thể không phù hợp với người khác.",
                    "love": "Cẩn thận với các mối quan hệ không lành mạnh hoặc sự thiếu giao tiếp.",
                    "career": "Đối tác hoặc hợp tác có thể không hiệu quả. Hãy đánh giá lại các mối quan hệ công việc.",
                    "advice": "Hãy đảm bảo bạn đang trung thực với bản thân và không thỏa hiệp quá nhiều."
                }
            }
        },
        {
            "name": "The Chariot - Xe Chiến Xa",
            "number": 7,
            "emoji": "🏇",
            "keywords": ["Quyết tâm", "Chiến thắng", "Ý chí", "Kiểm soát"],
            "meanings": {
                "upright": {
                    "general": "Thành công đang trong tầm tay nếu bạn duy trì sự tập trung và quyết tâm. Hãy nắm quyền kiểm soát và tiến về phía trước với sự tự tin. Mặc dù có thể có những thách thức, nhưng ý chí mạnh mẽ của bạn sẽ giúp bạn vượt qua. Đây là thời điểm của sự tiến bộ nhanh chóng.",
                    "love": "Hãy chủ động trong tình yêu và vượt qua các trở ngại. Quyết tâm của bạn sẽ giúp mối quan hệ phát triển.",
                    "career": "Thành công nghề nghiệp đang đến gần. Hãy tập trung vào mục tiêu và không để bất cứ điều gì làm bạn xao lãng.",
                    "advice": "Hãy duy trì động lực và kiểm soát tình hình. Sự tự tin và quyết tâm là chìa khóa."
                },
                "reversed": {
                    "general": "Bạn có thể đang mất kiểm soát hoặc thiếu phương hướng rõ ràng. Sự thiếu tập trung có thể khiến bạn lạc lối.",
                    "love": "Có thể có xung đột về hướng đi của mối quan hệ. Cần sự điều chỉnh và thỏa hiệp.",
                    "career": "Kế hoạch của bạn có thể bị trật bánh. Hãy đánh giá lại mục tiêu và chiến lược.",
                    "advice": "Hãy dừng lại, đánh giá lại và lấy lại sự kiểm soát. Đừng cố gắng tiến về quá nhiều hướng cùng lúc."
                }
            }
        },
        {
            "name": "Strength - Sức Mạnh",
            "number": 8,
            "emoji": "🦁",
            "keywords": ["Can đảm", "Kiên nhẫn", "Lòng trắc ẩn", "Tự chủ"],
            "meanings": {
                "upright": {
                    "general": "Bạn có sức mạnh nội tâm để vượt qua mọi thách thức. Đây không phải là sức mạnh thô bạo mà là sự kiên nhẫn, lòng trắc ẩn và tự chủ. Hãy đối mặt với sợ hãi bằng lòng can đảm dịu dàng. Bạn mạnh mẽ hơn mình nghĩ nhiều.",
                    "love": "Tình yêu và lòng trắc ẩn sẽ vượt qua mọi khó khăn. Hãy kiên nhẫn và thấu hiểu.",
                    "career": "Hãy đối mặt với thách thức công việc bằng sự tự tin và kiềm chế. Bạn có khả năng xử lý mọi tình huống.",
                    "advice": "Sức mạnh thật sự đến từ bên trong. Hãy tin vào bản thân và đối xử với mọi người bằng lòng trắc ẩn."
                },
                "reversed": {
                    "general": "Có thể bạn đang nghi ngờ bản thân hoặc để cảm xúc điều khiển. Sự mất tự chủ có thể dẫn đến các quyết định sai lầm.",
                    "love": "Cẩn thận với sự thiếu kiên nhẫn hoặc để cảm xúc tiêu cực chi phối mối quan hệ.",
                    "career": "Bạn có thể đang thiếu tự tin để đối mặt với thách thức công việc.",
                    "advice": "Hãy tìm lại sự tự tin và tự chủ. Đừng để sợ hãi hoặc cảm xúc tiêu cực kiểm soát bạn."
                }
            }
        },
        {
            "name": "The Hermit - Ẩn Sĩ",
            "number": 9,
            "emoji": "🔦",
            "keywords": ["Nội quan", "Tìm kiếm", "Trí tuệ", "Đơn độc"],
            "meanings": {
                "upright": {
                    "general": "Đây là thời điểm để rút lui và tìm kiếm sự sáng suốt từ bên trong. Hãy dành thời gian cho bản thân, suy ngẫm và tìm kiếm sự thật sâu xa hơn. Sự đơn độc không phải là cô đơn mà là cơ hội để kết nối với bản chất thật của bạn. Hãy lắng nghe giọng nói nội tâm.",
                    "love": "Có thể bạn cần thời gian một mình để hiểu rõ hơn về bản thân trước khi cam kết trong một mối quan hệ.",
                    "career": "Hãy dành thời gian để suy nghĩ về con đường sự nghiệp của bạn. Đừng vội vàng đưa ra quyết định.",
                    "advice": "Hãy tôn trọng nhu cầu đơn độc của bạn. Sự sáng suốt sẽ đến khi bạn yên tĩnh tâm trí."
                },
                "reversed": {
                    "general": "Bạn có thể đang cô lập bản thân quá mức hoặc ngược lại, sợ ở một mình. Hãy tìm sự cân bằng giữa đơn độc và kết nối.",
                    "love": "Cẩn thận với việc đóng cửa trái tim hoặc tránh né các mối quan hệ.",
                    "career": "Bạn có thể đang thiếu sự hợp tác hoặc cô lập bản thân khỏi đồng nghiệp.",
                    "advice": "Hãy tìm sự cân bằng. Đừng cô lập bản thân nhưng cũng đừng sợ thời gian một mình."
                }
            }
        },
        {
            "name": "Wheel of Fortune - Bánh Xe Vận Mệnh",
            "number": 10,
            "emoji": "🎡",
            "keywords": ["Thay đổi", "Chu kỳ", "Vận mệnh", "Cơ hội"],
            "meanings": {
                "upright": {
                    "general": "Cuộc sống đang thay đổi và vận may đang đến với bạn. Hãy chấp nhận sự thay đổi và tin rằng mọi thứ đều xảy ra vì một lý do. Đây là thời điểm của cơ hội và chuyển biến tích cực. Bánh xe đang quay về phía bạn.",
                    "love": "Sự thay đổi tích cực trong tình yêu. Có thể gặp gỡ người mới hoặc mối quan hệ hiện tại phát triển lên tầm cao mới.",
                    "career": "Cơ hội nghề nghiệp bất ngờ có thể xuất hiện. Hãy sẵn sàng nắm bắt.",
                    "advice": "Hãy tin vào vận mệnh và chấp nhận sự thay đổi. Mọi thứ đều có chu kỳ của nó."
                },
                "reversed": {
                    "general": "Có thể bạn đang chống lại sự thay đổi hoặc gặp phải giai đoạn khó khăn. Hãy nhớ rằng bánh xe sẽ tiếp tục quay.",
                    "love": "Mối quan hệ có thể đang trải qua giai đoạn khó khăn, nhưng hãy kiên nhẫn.",
                    "career": "Có thể có sự chậm trễ hoặc trở ngại trong sự nghiệp, nhưng đây chỉ là tạm thời.",
                    "advice": "Hãy kiên nhẫn và tin rằng mọi thứ sẽ thay đổi. Đừng chống lại dòng chảy của cuộc sống."
                }
            }
        },
        {
            "name": "Justice - Công Lý",
            "number": 11,
            "emoji": "⚖️",
            "keywords": ["Công bằng", "Chân lý", "Luật pháp", "Cân bằng"],
            "meanings": {
                "upright": {
                    "general": "Chân lý và công lý sẽ thắng. Hãy đối mặt với các tình huống một cách trung thực và công bằng. Quyết định của bạn nên dựa trên sự thật và đạo đức. Những gì bạn gieo sẽ được gặt - karma đang hoạt động.",
                    "love": "Sự trung thực và công bằng là chìa khóa trong mối quan hệ. Hãy đối xử với đối phương một cách công bằng.",
                    "career": "Các vấn đề pháp lý hoặc hợp đồng có thể được giải quyết theo hướng có lợi. Hãy đảm bảo mọi thứ đều công bằng.",
                    "advice": "Hãy trung thực với bản thân và người khác. Đưa ra quyết định dựa trên lý trí và công bằng."
                },
                "reversed": {
                    "general": "Có thể có sự bất công hoặc thiếu trung thực. Hãy kiểm tra xem bạn có đang đối xử công bằng với bản thân và người khác không.",
                    "love": "Cẩn thận với sự thiếu cân bằng hoặc bất công trong mối quan hệ.",
                    "career": "Có thể có xung đột pháp lý hoặc các tình huống không công bằng tại nơi làm việc.",
                    "advice": "Hãy đối mặt với sự thật và cố gắng khôi phục sự cân bằng. Đừng tránh né trách nhiệm."
                }
            }
        },
        {
            "name": "The Hanged Man - Người Bị Treo",
            "number": 12,
            "emoji": "🙃",
            "keywords": ["Hy sinh", "Buông bỏ", "Góc nhìn mới", "Chờ đợi"],
            "meanings": {
                "upright": {
                    "general": "Đôi khi bạn cần dừng lại và nhìn mọi thứ từ góc độ khác. Sự buông bỏ và chấp nhận có thể mang lại sự giác ngộ. Hãy kiên nhẫn và tin vào quá trình. Những gì bạn hy sinh bây giờ sẽ mang lại lợi ích lớn hơn sau này.",
                    "love": "Có thể bạn cần hy sinh một số điều cho mối quan hệ. Hãy nhìn tình huống từ góc độ của đối phương.",
                    "career": "Đây không phải lúc để hành động vội vàng. Hãy chờ đợi và quan sát trước khi đưa ra quyết định.",
                    "advice": "Hãy buông bỏ những gì không còn phù hợp. Sự kiên nhẫn và góc nhìn mới sẽ mang lại sự sáng suốt."
                },
                "reversed": {
                    "general": "Bạn có thể đang cảm thấy bị kẹt hoặc không biết phải làm gì. Sự hy sinh của bạn có thể không được đánh giá cao.",
                    "love": "Cẩn thận với việc hy sinh quá nhiều mà không nhận lại gì. Hãy đảm bảo sự cân bằng.",
                    "career": "Bạn có thể đang bị trì hoãn không cần thiết. Hãy đánh giá xem có nên thay đổi hướng đi không.",
                    "advice": "Nếu sự chờ đợi không mang lại kết quả, có thể đã đến lúc hành động. Đừng hy sinh mãi mà không thấy tiến bộ."
                }
            }
        },
        {
            "name": "Death - Cái Chết",
            "number": 13,
            "emoji": "💀",
            "keywords": ["Kết thúc", "Chuyển hóa", "Tái sinh", "Thay đổi"],
            "meanings": {
                "upright": {
                    "general": "Một chương cũ đang kết thúc để mở đường cho điều mới tốt đẹp hơn. Đừng sợ sự thay đổi - đây là quá trình chuyển hóa cần thiết. Hãy buông bỏ quá khứ và đón nhận tương lai. Cái chết của cái cũ là sự tái sinh của cái mới.",
                    "love": "Một giai đoạn trong mối quan hệ đang kết thúc, nhưng điều này có thể mang lại sự phát triển sâu sắc hơn.",
                    "career": "Sự thay đổi nghề nghiệp có thể xảy ra. Hãy chấp nhận và chuẩn bị cho cơ hội mới.",
                    "advice": "Hãy chấp nhận sự thay đổi. Đừng bám víu vào quá khứ. Sự chuyển hóa này sẽ dẫn đến điều tốt đẹp hơn."
                },
                "reversed": {
                    "general": "Bạn có thể đang chống lại sự thay đổi cần thiết hoặc sợ buông bỏ. Sự trì trệ có thể khiến bạn bị mắc kẹt.",
                    "love": "Cẩn thận với việc giữ mối quan hệ đã hết ý nghĩa. Đôi khi buông bỏ là cần thiết.",
                    "career": "Bạn có thể đang ở trong công việc không còn phù hợp nhưng sợ thay đổi.",
                    "advice": "Đừng sợ buông bỏ. Sự thay đổi là cần thiết cho sự phát triển."
                }
            }
        },
        {
            "name": "Temperance - Tiết Độ",
            "number": 14,
            "emoji": "⚗️",
            "keywords": ["Cân bằng", "Hòa hợp", "Kiên nhẫn", "Điều hòa"],
            "meanings": {
                "upright": {
                    "general": "Hãy tìm sự cân bằng trong cuộc sống. Điều độ và kiên nhẫn sẽ mang lại hòa hợp. Đừng đi đến cực đoan - hãy tìm con đường trung dung. Sự kết hợp khéo léo các yếu tố khác nhau sẽ tạo ra điều kỳ diệu.",
                    "love": "Sự hòa hợp và cân bằng trong mối quan hệ. Hãy tìm điểm giữa và thỏa hiệp.",
                    "career": "Hãy kiên nhẫn và làm việc đều đặn. Thành công sẽ đến từ sự kiên trì và cân bằng.",
                    "advice": "Hãy điều độ trong mọi việc. Tìm sự cân bằng giữa công việc và cuộc sống, cho và nhận."
                },
                "reversed": {
                    "general": "Có thể có sự mất cân bằng trong cuộc sống của bạn. Bạn đang đi quá cực đoan ở một khía cạnh nào đó.",
                    "love": "Thiếu hòa hợp hoặc cân bằng trong mối quan hệ. Một người có thể đang cho quá nhiều.",
                    "career": "Công việc có thể đang áp đảo hoặc bạn thiếu sự kiên nhẫn cần thiết.",
                    "advice": "Hãy tìm lại sự cân bằng. Điều chỉnh lại các ưu tiên của bạn."
                }
            }
        },
        {
            "name": "The Devil - Ác Quỷ",
            "number": 15,
            "emoji": "😈",
            "keywords": ["Ràng buộc", "Cám dỗ", "Phụ thuộc", "Vật chất"],
            "meanings": {
                "upright": {
                    "general": "Bạn có thể đang bị trói buộc bởi những thói quen xấu, sự phụ thuộc hoặc lối sống vật chất. Hãy nhận ra những gì đang kiểm soát bạn và tìm cách giải thoát. Chuỗi xiềng chỉ tồn tại nếu bạn để chúng tồn tại. Bạn có quyền tự do lựa chọn.",
                    "love": "Cẩn thận với các mối quan hệ không lành mạnh hoặc có tính kiểm soát. Đừng để ham muốn che mắt bạn.",
                    "career": "Có thể bạn đang bị kẹt trong công việc vì tiền bạc mà không có sự thỏa mãn.",
                    "advice": "Hãy nhận ra những gì đang kiềm hãm bạn và tìm cách giải thoát. Bạn mạnh mẽ hơn những ràng buộc này."
                },
                "reversed": {
                    "general": "Bạn đang bắt đầu giải thoát khỏi những ràng buộc. Sự nhận thức về vấn đề là bước đầu tiên để tự do.",
                    "love": "Bạn đang nhận ra và thoát khỏi mối quan hệ không lành mạnh.",
                    "career": "Bạn đang tìm cách thoát khỏi công việc hoặc tình huống không thỏa mãn.",
                    "advice": "Hãy tiếp tục con đường giải thoát. Bạn đang đi đúng hướng."
                }
            }
        },
        {
            "name": "The Tower - Tháp",
            "number": 16,
            "emoji": "⚡",
            "keywords": ["Đổ vỡ", "Thay đổi đột ngột", "Giác ngộ", "Giải phóng"],
            "meanings": {
                "upright": {
                    "general": "Sự thay đổi đột ngột và mạnh mẽ đang xảy ra. Những nền tảng không vững chắc đang sụp đổ để tạo chỗ cho điều mới tốt hơn. Mặc dù đau đớn, đây là quá trình cần thiết. Sự đổ vỡ này sẽ dẫn đến giác ngộ và giải phóng.",
                    "love": "Mối quan hệ có thể trải qua thử thách lớn hoặc kết thúc đột ngột. Nhưng điều này sẽ giải phóng bạn.",
                    "career": "Có thể có sự thay đổi đột ngột trong công việc. Hãy chuẩn bị thích nghi.",
                    "advice": "Đừng chống lại sự đổ vỡ. Hãy tin rằng điều này đang xảy ra vì lý do tốt. Từ đống đổ nát, điều mới sẽ nảy sinh."
                },
                "reversed": {
                    "general": "Bạn có thể đang tránh né sự thay đổi cần thiết. Hoặc bạn đang phục hồi sau một biến cố lớn.",
                    "love": "Bạn có thể đang giữ mối quan hệ cần kết thúc hoặc đang phục hồi sau chia tay.",
                    "career": "Sự thay đổi có thể bị trì hoãn nhưng không thể tránh khỏi.",
                    "advice": "Đừng cố giữ những gì sắp sụp đổ. Hãy chấp nhận và chuẩn bị xây dựng lại."
                }
            }
        },
        {
            "name": "The Star - Ngôi Sao",
            "number": 17,
            "emoji": "⭐",
            "keywords": ["Hy vọng", "Cảm hứng", "Bình yên", "Chữa lành"],
            "meanings": {
                "upright": {
                    "general": "Sau những thử thách, hy vọng và ánh sáng đang trở lại. Đây là thời điểm của sự chữa lành và đổi mới. Hãy tin vào tương lai và giữ vững niềm tin. Vũ trụ đang ủng hộ bạn. Ước mơ của bạn có thể trở thành hiện thực.",
                    "love": "Tình yêu đích thực và chân thành đang đến. Hãy mở lòng và tin tưởng.",
                    "career": "Cơ hội mới đầy hứa hẹn. Hãy theo đuổi ước mơ nghề nghiệp của bạn với sự tự tin.",
                    "advice": "Hãy giữ vững niềm tin và hy vọng. Điều tốt đẹp đang đến với bạn."
                },
                "reversed": {
                    "general": "Có thể bạn đang mất hy vọng hoặc thiếu tự tin. Hãy tìm lại ánh sáng bên trong.",
                    "love": "Bạn có thể đang nghi ngờ về tình yêu. Hãy mở lòng trở lại.",
                    "career": "Có thể bạn đang mất phương hướng nghề nghiệp. Hãy tìm lại cảm hứng.",
                    "advice": "Đừng mất niềm tin. Ánh sáng vẫn ở đó, hãy tìm nó trong bóng tối."
                }
            }
        },
        {
            "name": "The Moon - Mặt Trăng",
            "number": 18,
            "emoji": "🌙",
            "keywords": ["Ảo ảnh", "Trực giác", "Sợ hãi", "Tiềm thức"],
            "meanings": {
                "upright": {
                    "general": "Không phải mọi thứ đều như bề ngoài. Hãy tin vào trực giác của bạn và nhìn xa hơn những ảo ảnh. Có thể có sự lừa dối hoặc nhầm lẫn. Hãy đối mặt với những sợ hãi ẩn giấu và lắng nghe tiềm thức của bạn. Bí ẩn sẽ dần được làm sáng tỏ.",
                    "love": "Có thể có sự không rõ ràng trong mối quan hệ. Hãy giao tiếp cởi mở và tin vào trực giác.",
                    "career": "Cẩn thận với sự lừa dối trong công việc. Hãy làm rõ mọi thứ trước khi quyết định.",
                    "advice": "Hãy tin vào trực giác nhưng cũng tìm kiếm sự thật. Đừng để sợ hãi kiểm soát bạn."
                },
                "reversed": {
                    "general": "Sự mơ hồ đang được làm rõ. Sợ hãi và lo lắng đang giảm bớt. Bạn đang nhìn thấy sự thật.",
                    "love": "Những hiểu lầm trong mối quan hệ đang được giải quyết.",
                    "career": "Tình hình công việc đang trở nên rõ ràng hơn.",
                    "advice": "Hãy tiếp tục tìm kiếm sự rõ ràng. Bạn đang đi đúng hướng."
                }
            }
        },
        {
            "name": "The Sun - Mặt Trời",
            "number": 19,
            "emoji": "☀️",
            "keywords": ["Niềm vui", "Thành công", "Sống động", "Tích cực"],
            "meanings": {
                "upright": {
                    "general": "Đây là thời điểm của niềm vui, thành công và sự sáng suốt. Mọi thứ đang rõ ràng và tích cực. Hãy tận hưởng giai đoạn này và chia sẻ ánh sáng của bạn với người khác. Thành công và hạnh phúc đang ở trong tầm tay. Hãy tỏa sáng!",
                    "love": "Tình yêu đang rực rỡ. Đây là thời điểm của hạnh phúc và sự kết nối sâu sắc.",
                    "career": "Thành công rực rỡ trong sự nghiệp. Nỗ lực của bạn đang được công nhận.",
                    "advice": "Hãy tận hưởng thành công và chia sẻ niềm vui với người khác. Bạn xứng đáng với điều này."
                },
                "reversed": {
                    "general": "Có thể bạn đang gặp khó khăn trong việc nhìn thấy mặt tích cực. Niềm vui có thể bị che khuất.",
                    "love": "Mối quan hệ có thể thiếu sự ấm áp. Hãy tìm lại niềm vui chung.",
                    "career": "Thành công có thể bị trì hoãn. Hãy kiên nhẫn.",
                    "advice": "Hãy tìm kiếm ánh sáng ngay cả trong bóng tối. Niềm vui vẫn có thể tìm thấy."
                }
            }
        },
        {
            "name": "Judgement - Phán Xét",
            "number": 20,
            "emoji": "📯",
            "keywords": ["Phản ánh", "Đánh giá", "Cứu chuộc", "Quyết định"],
            "meanings": {
                "upright": {
                    "general": "Đây là thời điểm để đánh giá lại cuộc sống của bạn và đưa ra những quyết định quan trọng. Hãy học từ quá khứ và tiến về phía trước với sự sáng suốt. Sự cứu chuộc và tha thứ (bản thân và người khác) là cần thiết. Một chương mới đang mở ra.",
                    "love": "Đánh giá lại mối quan hệ và đưa ra quyết định quan trọng. Hãy học từ quá khứ.",
                    "career": "Thời điểm để đánh giá sự nghiệp và có thể thay đổi hướng đi nếu cần.",
                    "advice": "Hãy trung thực với bản thân. Học từ quá khứ và đưa ra quyết định sáng suốt cho tương lai."
                },
                "reversed": {
                    "general": "Bạn có thể đang tự phê phán quá mức hoặc không học được từ quá khứ. Sự tha thứ là cần thiết.",
                    "love": "Cẩn thận với việc sống trong quá khứ hoặc không tha thứ cho những sai lầm.",
                    "career": "Bạn có thể đang bị kẹt vì không muốn thay đổi hoặc học hỏi.",
                    "advice": "Hãy tha thứ cho bản thân và người khác. Đừng để quá khứ kìm hãm bạn."
                }
            }
        },
        {
            "name": "The World - Thế Giới",
            "number": 21,
            "emoji": "🌍",
            "keywords": ["Hoàn thành", "Thành tựu", "Du lịch", "Viên mãn"],
            "meanings": {
                "upright": {
                    "general": "Bạn đã đạt được một cột mốc quan trọng. Một chu kỳ đã hoàn thành và bạn đang ở đỉnh cao. Hãy tự hào về những gì bạn đã đạt được và sẵn sàng cho chương tiếp theo. Thế giới đang mở ra trước mặt bạn với vô vàn khả năng.",
                    "love": "Mối quan hệ đã đạt đến sự viên mãn và hòa hợp. Đây có thể là thời điểm của cam kết lớn.",
                    "career": "Thành công lớn trong sự nghiệp. Bạn đã đạt được mục tiêu quan trọng.",
                    "advice": "Hãy tự hào về thành tựu của bạn nhưng cũng sẵn sàng cho cuộc phiêu lưu mới. Cuộc sống là một chu kỳ liên tục."
                },
                "reversed": {
                    "general": "Có thể bạn đang thiếu chút nữa để hoàn thành mục tiêu. Hoặc bạn sợ bước vào giai đoạn mới.",
                    "love": "Mối quan hệ có thể cần thêm nỗ lực để đạt sự viên mãn.",
                    "career": "Thành công đang gần nhưng chưa hoàn toàn đạt được. Hãy kiên trì.",
                    "advice": "Đừng bỏ cuộc khi đã gần đích. Hãy hoàn thành những gì bạn bắt đầu."
                }
            }
        }
    ]


    @staticmethod
    def interpret_cards(cards: List[Dict], spread_type: str, question: str = "") -> Dict:
        """Interpret selected cards based on spread type"""
        interpretations = []
        overall_message = ""
        
        if spread_type == "past_present_future":
            positions = [
                {"name": "Quá Khứ (Past)", "description": "Những gì đã xảy ra và ảnh hưởng đến bạn"},
                {"name": "Hiện Tại (Present)", "description": "Tình hình hiện tại của bạn"},
                {"name": "Tương Lai (Future)", "description": "Những gì sắp đến"}
            ]
            
            for card, position in zip(cards, positions):
                orientation = card.get("orientation", "upright")
                meanings = card["meanings"][orientation]
                
                interpretations.append({
                    "position": position["name"],
                    "position_description": position["description"],
                    "card_name": card["name"],
                    "card_number": card["number"],
                    "emoji": card["emoji"],
                    "orientation": "Xuôi" if orientation == "upright" else "Ngược",
                    "keywords": card["keywords"],
                    "general_meaning": meanings["general"],
                    "love_meaning": meanings["love"],
                    "career_meaning": meanings["career"],
                    "advice": meanings["advice"]
                })
            
            overall_message = f"""
            Hành trình của bạn bắt đầu từ {cards[0]['name']} - {cards[0]['meanings'][cards[0].get('orientation', 'upright')]['advice']}
            
            Hiện tại, bạn đang ở giai đoạn {cards[1]['name']} - {cards[1]['meanings'][cards[1].get('orientation', 'upright')]['advice']}
            
            Tương lai hứa hẹn điều {cards[2]['name'].lower()} - {cards[2]['meanings'][cards[2].get('orientation', 'upright')]['advice']}
            
            Tóm lại: Hãy học từ quá khứ, sống trọn vẹn hiện tại, và tin tưởng vào tương lai. Vũ trụ đang dẫn dắt bạn theo con đường tốt nhất.
            """
            
        elif spread_type == "celtic_cross":
            positions = [
                {"name": "Vị Trí 1: Tình Huống Hiện Tại", "description": "Bạn đang ở đâu ngay bây giờ"},
                {"name": "Vị Trí 2: Thách Thức", "description": "Điều gì đang cản trở bạn"},
                {"name": "Vị Trí 3: Nguyên Nhân", "description": "Cốt lõi của tình huống"},
                {"name": "Vị Trí 4: Quá Khứ", "description": "Nền tảng của vấn đề"},
                {"name": "Vị Trí 5: Khả Năng Tốt Nhất", "description": "Kết quả tích cực có thể xảy ra"},
                {"name": "Vị Trí 6: Tương Lai Gần", "description": "Điều gì sắp xảy ra"},
                {"name": "Vị Trí 7: Bạn", "description": "Thái độ và năng lượng của bạn"},
                {"name": "Vị Trí 8: Ảnh Hưởng Bên Ngoài", "description": "Yếu tố từ môi trường"},
                {"name": "Vị Trí 9: Hy Vọng và Sợ Hãi", "description": "Những gì bạn mong đợi"},
                {"name": "Vị Trí 10: Kết Quả", "description": "Kết cục cuối cùng"}
            ]
            
            for card, position in zip(cards, positions[:len(cards)]):
                orientation = card.get("orientation", "upright")
                meanings = card["meanings"][orientation]
                
                interpretations.append({
                    "position": position["name"],
                    "position_description": position["description"],
                    "card_name": card["name"],
                    "card_number": card["number"],
                    "emoji": card["emoji"],
                    "orientation": "Xuôi" if orientation == "upright" else "Ngược",
                    "keywords": card["keywords"],
                    "general_meaning": meanings["general"],
                    "advice": meanings["advice"]
                })
            
            overall_message = "Thập Giá Celtic cho thấy bức tranh toàn cảnh về tình huống của bạn. Hãy cân nhắc từng khía cạnh và đưa ra quyết định sáng suốt."
            
        elif spread_type == "single_card":
            card = cards[0]
            orientation = card.get("orientation", "upright")
            meanings = card["meanings"][orientation]
            
            interpretations.append({
                "position": "Lời Khuyên Hôm Nay",
                "position_description": "Thông điệp vũ trụ dành cho bạn",
                "card_name": card["name"],
                "card_number": card["number"],
                "emoji": card["emoji"],
                "orientation": "Xuôi" if orientation == "upright" else "Ngược",
                "keywords": card["keywords"],
                "general_meaning": meanings["general"],
                "love_meaning": meanings["love"],
                "career_meaning": meanings["career"],
                "advice": meanings["advice"]
            })
            
            overall_message = f"Hôm nay, vũ trụ gửi đến bạn thông điệp qua lá bài {card['name']}: {meanings['advice']}"
        
        return {
            "spread_type": spread_type,
            "spread_name": {
                "past_present_future": "Quá Khứ - Hiện Tại - Tương Lai",
                "celtic_cross": "Thập Giá Celtic",
                "single_card": "Một Lá Bài"
            }.get(spread_type, spread_type),
            "question": question,
            "cards": interpretations,
            "overall_message": overall_message.strip(),
            "total_cards": len(interpretations)
        }

async def get_tarot_reading(
    user_id: str, 
    spread_type: str = "past_present_future", 
    num_cards: int = None,
    question: str = ""
) -> Dict:
    """
    Get a tarot reading
    
    Args:
        user_id: User ID
        spread_type: Type of spread (past_present_future, celtic_cross, single_card)
        num_cards: Number of cards (auto-determined by spread_type if not provided)
        question: Optional question from user
    """
    # Determine number of cards based on spread type
    if num_cards is None:
        spread_card_count = {
            "single_card": 1,
            "past_present_future": 3,
            "celtic_cross": 10
        }
        num_cards = spread_card_count.get(spread_type, 3)
    
    # Randomly select cards from Major Arcana
    selected_indices = random.sample(range(len(TarotReader.MAJOR_ARCANA)), num_cards)
    selected_cards = []
    
    for idx in selected_indices:
        card = TarotReader.MAJOR_ARCANA[idx].copy()
        # Randomly determine if card is reversed (30% chance)
        card["orientation"] = "reversed" if random.random() < 0.3 else "upright"
        selected_cards.append(card)
    
    # Get interpretation
    result = TarotReader.interpret_cards(selected_cards, spread_type, question)
    
    # Create summary for history
    card_names = [card["name"] for card in selected_cards]
    summary = f"Bói Tarot: {result['spread_name']}"
    if question:
        summary += f" - Câu hỏi: {question}"
    
    # Save to history
    history_entry = {
        "user_id": user_id,
        "type": "tarot",
        "result_summary": summary,
        "result_detail": result,
        "created_at": datetime.now(),
        "is_favorite": False,
        "is_shared": False
    }
    
    await fortune_history.insert_one(history_entry)
    
    return result