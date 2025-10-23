import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/layout/Layout';
import GlowButton from '../components/common/GlowButton';
import ResultCard from '../components/common/ResultCard';
import { useAuth } from '../contexts/AuthContext';
import { fortuneAPI } from '../utils/api';

interface TarotCard {
  position: string;
  position_description: string;
  card_name: string;
  card_number: number;
  emoji: string;
  orientation: string;
  keywords: string[];
  general_meaning: string;
  love_meaning?: string;
  career_meaning?: string;
  advice: string;
}

interface TarotResult {
  spread_type: string;
  spread_name: string;
  question: string;
  cards: TarotCard[];
  overall_message: string;
  total_cards: number;
}

const TarotPage = () => {
  const { user } = useAuth();
  const [spreadType, setSpreadType] = useState<string>('past_present_future');
  const [question, setQuestion] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<TarotResult | null>(null);
  const [showCards, setShowCards] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const spreadTypes = [
    {
      value: 'single_card',
      label: '🎴 Một Lá Bài',
      description: 'Rút 1 lá để nhận lời khuyên hôm nay',
      cards: 1
    },
    {
      value: 'past_present_future',
      label: '🔮 Quá Khứ - Hiện Tại - Tương Lai',
      description: 'Xem hành trình của bạn qua 3 lá bài',
      cards: 3
    },
    {
      value: 'celtic_cross',
      label: '✨ Thập Giá Celtic',
      description: 'Phân tích sâu với 10 lá bài',
      cards: 10
    }
  ];

  const handleReadTarot = async () => {
    if (!user) {
      setError('Vui lòng đăng nhập để xem bói Tarot');
      return;
    }

    setIsLoading(true);
    setError(null);
    setShowCards(false);

    try {
      const response = await fortuneAPI.tarot(user.id, {
        spread_type: spreadType,
        question: question.trim()
      });

      setResult(response.data);
      
      // Delay showing cards for dramatic effect
      setTimeout(() => {
        setShowCards(true);
      }, 500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Không thể xem bói Tarot. Vui lòng thử lại.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setShowCards(false);
    setQuestion('');
    setError(null);
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="max-w-6xl mx-auto"
        >
          <h1 className="text-3xl md:text-4xl font-display text-accent mb-2 text-center">
            🔮 Bói Bài Tarot
          </h1>
          <p className="text-white/70 text-center mb-8">
            Để lá bài hé lộ những bí ẩn của vận mệnh bạn
          </p>

          {!result ? (
            <div className="card max-w-2xl mx-auto">
              <h2 className="text-2xl font-display text-white mb-6">
                Chọn Cách Trải Bài
              </h2>

              <div className="space-y-4 mb-6">
                {spreadTypes.map((type) => (
                  <motion.div
                    key={type.value}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setSpreadType(type.value)}
                    className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                      spreadType === type.value
                        ? 'border-accent bg-accent/10'
                        : 'border-white/20 hover:border-white/40'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="text-lg font-display text-white mb-1">
                          {type.label}
                        </h3>
                        <p className="text-sm text-white/70">{type.description}</p>
                      </div>
                      <span className="text-accent font-bold">{type.cards} lá</span>
                    </div>
                  </motion.div>
                ))}
              </div>

              <div className="mb-6">
                <label className="block text-white mb-2 font-display">
                  Câu Hỏi Của Bạn (Tùy chọn)
                </label>
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Nhập câu hỏi mà bạn muốn lá bài trả lời..."
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-accent resize-none"
                  rows={3}
                  maxLength={200}
                />
                <p className="text-sm text-white/50 mt-1">
                  {question.length}/200 ký tự
                </p>
              </div>

              {error && (
                <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
                  {error}
                </div>
              )}

              <GlowButton
                onClick={handleReadTarot}
                disabled={isLoading || !user}
                className="w-full"
              >
                {isLoading ? (
                  <>
                    <span className="animate-spin mr-2">�</span>
                    Đang rút bài...
                  </>
                ) : (
                  <>🎴 Bắt Đầu Rút Bài</>
                )}
              </GlowButton>

              {!user && (
                <p className="text-center text-white/70 mt-4">
                  Vui lòng đăng nhập để sử dụng tính năng này
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-8">
              {/* Header */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="card text-center"
              >
                <h2 className="text-2xl font-display text-accent mb-2">
                  {result.spread_name}
                </h2>
                {result.question && (
                  <p className="text-white/80 italic">
                    Câu hỏi: "{result.question}"
                  </p>
                )}
              </motion.div>

              {/* Cards Grid */}
              <div className={`grid gap-6 ${
                result.total_cards === 1 ? 'grid-cols-1 max-w-md mx-auto' :
                result.total_cards === 3 ? 'grid-cols-1 md:grid-cols-3' :
                'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
              }`}>
                <AnimatePresence>
                  {showCards && result.cards.map((card, index) => (
                    <motion.div
                      key={index}
                      initial={{ rotateY: 180, opacity: 0 }}
                      animate={{ rotateY: 0, opacity: 1 }}
                      transition={{ 
                        duration: 0.6, 
                        delay: index * 0.3,
                        type: "spring"
                      }}
                      className="card hover:border-accent/40 transition-colors"
                    >
                      <div className="text-center mb-4">
                        <div className="text-6xl mb-3">{card.emoji}</div>
                        <h3 className="text-xl font-display text-white mb-1">
                          {card.card_name}
                        </h3>
                        <p className="text-sm text-accent mb-2">
                          {card.position}
                        </p>
                        <p className="text-xs text-white/60 mb-3">
                          {card.position_description}
                        </p>
                        <div className="inline-block px-3 py-1 bg-accent/20 rounded-full text-xs text-accent">
                          {card.orientation}
                        </div>
                      </div>

                      <div className="space-y-3 text-sm">
                        <div>
                          <div className="flex flex-wrap gap-2 mb-2">
                            {card.keywords.map((keyword, i) => (
                              <span
                                key={i}
                                className="px-2 py-1 bg-white/10 rounded text-xs text-white/80"
                              >
                                {keyword}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h4 className="text-white font-semibold mb-1">✨ Ý Nghĩa:</h4>
                          <p className="text-white/80 text-xs leading-relaxed">
                            {card.general_meaning}
                          </p>
                        </div>

                        {card.love_meaning && (
                          <div>
                            <h4 className="text-white font-semibold mb-1">💕 Tình Yêu:</h4>
                            <p className="text-white/80 text-xs leading-relaxed">
                              {card.love_meaning}
                            </p>
                          </div>
                        )}

                        {card.career_meaning && (
                          <div>
                            <h4 className="text-white font-semibold mb-1">💼 Sự Nghiệp:</h4>
                            <p className="text-white/80 text-xs leading-relaxed">
                              {card.career_meaning}
                            </p>
                          </div>
                        )}

                        <div className="pt-2 border-t border-white/10">
                          <h4 className="text-accent font-semibold mb-1">💫 Lời Khuyên:</h4>
                          <p className="text-white/90 text-xs leading-relaxed">
                            {card.advice}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>

              {/* Overall Message */}
              {showCards && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: result.total_cards * 0.3 + 0.5 }}
                >
                  <ResultCard title="Thông Điệp Tổng Quan" emoji="🌟">
                    <p className="text-white/90 leading-relaxed whitespace-pre-line">
                      {result.overall_message}
                    </p>
                  </ResultCard>
                </motion.div>
              )}

              {/* Actions */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: result.total_cards * 0.3 + 0.7 }}
                className="flex justify-center gap-4"
              >
                <GlowButton onClick={handleReset}>
                  🔄 Rút Bài Lại
                </GlowButton>
              </motion.div>
            </div>
          )}
        </motion.div>
      </div>
    </Layout>
  );
};

export default TarotPage;