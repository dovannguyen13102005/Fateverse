import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/layout/Layout';
import GlowButton from '../components/common/GlowButton';
import ResultCard from '../components/common/ResultCard';
import { useAuth } from '../contexts/AuthContext';
import { fortuneAPI, historyAPI } from '../utils/api';

interface DailyFortune {
  fortune_date: string;
  message: string;
  lucky_colors: string[];
  lucky_numbers: number[];
  emoji: string;
  quote: string;
  advice: string;
  area_focus: string;
}

const DailyFortunePage = () => {
  const { user } = useAuth();
  const [fortune, setFortune] = useState<DailyFortune | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastHistoryId, setLastHistoryId] = useState<string | null>(null);

  const fetchDailyFortune = async () => {
    if (!user) {
      setError('Vui lòng đăng nhập để xem vận may hôm nay');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fortuneAPI.dailyFortune(user.id);
      setFortune(response.data);
      
      // Get the latest history entry to get the ID for sharing
      const historyResponse = await historyAPI.getHistory(user.id, 1);
      if (historyResponse.data.length > 0) {
        setLastHistoryId(historyResponse.data[0].id);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Không thể lấy vận may hôm nay. Vui lòng thử lại.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchDailyFortune();
    }
  }, [user]);

  const handleSave = async () => {
    if (!lastHistoryId) {
      alert('Không thể lưu. Vui lòng thử lại.');
      return;
    }

    try {
      await historyAPI.toggleFavorite(lastHistoryId);
      alert('Đã lưu vào mục yêu thích! ⭐');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Không thể lưu. Vui lòng thử lại.');
    }
  };

  const handleShare = async () => {
    if (!lastHistoryId) {
      alert('Không thể chia sẻ. Vui lòng thử lại.');
      return;
    }

    try {
      const response = await historyAPI.createShareLink(lastHistoryId);
      const shareUrl = `${window.location.origin}${response.data.share_url}`;
      
      await navigator.clipboard.writeText(shareUrl);
      alert('Đã sao chép link chia sẻ! 🌟');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Không thể tạo link chia sẻ.');
    }
  };

  if (!user) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-8 text-center">
          <h2 className="text-2xl text-white">Vui lòng đăng nhập để xem vận may hôm nay</h2>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="max-w-3xl mx-auto"
        >
          <h1 className="text-3xl md:text-4xl font-display text-accent mb-2 text-center">
            🌈 Vận May Hôm Nay
          </h1>
          <p className="text-white/70 text-center mb-8">
            Khám phá những điều tốt đẹp đang chờ đón bạn
          </p>

          {isLoading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-accent mx-auto mb-4" />
              <p className="text-white">Đang xem vận may của bạn...</p>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-400 mb-4">{error}</p>
              <GlowButton onClick={fetchDailyFortune}>
                Thử Lại
              </GlowButton>
            </div>
          ) : fortune ? (
            <AnimatePresence>
              <div className="space-y-6">
                {/* Main Fortune Card */}
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5 }}
                  className="card text-center"
                >
                  <div className="text-6xl mb-4">{fortune.emoji}</div>
                  <h2 className="text-2xl font-display text-accent mb-4">
                    {fortune.area_focus}
                  </h2>
                  <p className="text-xl text-white mb-6 leading-relaxed">
                    {fortune.message}
                  </p>
                  <div className="inline-block px-4 py-2 bg-accent/20 rounded-full">
                    <p className="text-white/90 italic">"{fortune.quote}"</p>
                  </div>
                </motion.div>

                {/* Lucky Elements */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="grid grid-cols-1 md:grid-cols-2 gap-4"
                >
                  <div className="card">
                    <h3 className="text-lg font-display text-white mb-3 flex items-center gap-2">
                      🎨 Màu May Mắn
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {fortune.lucky_colors.map((color, index) => (
                        <span
                          key={index}
                          className="px-4 py-2 bg-white/10 rounded-full text-white"
                        >
                          {color}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="card">
                    <h3 className="text-lg font-display text-white mb-3 flex items-center gap-2">
                      🔢 Số May Mắn
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {fortune.lucky_numbers.map((number, index) => (
                        <span
                          key={index}
                          className="w-12 h-12 flex items-center justify-center bg-accent/20 rounded-full text-accent font-bold text-lg"
                        >
                          {number}
                        </span>
                      ))}
                    </div>
                  </div>
                </motion.div>

                {/* Advice Card */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <ResultCard title="Lời Khuyên" emoji="💫">
                    <p className="text-white/90 leading-relaxed">
                      {fortune.advice}
                    </p>
                  </ResultCard>
                </motion.div>

                {/* Action Buttons */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.6 }}
                  className="flex justify-center gap-4"
                >
                  <GlowButton variant="secondary" onClick={handleSave}>
                    💾 Lưu Lại
                  </GlowButton>
                  <GlowButton onClick={handleShare}>
                    🌟 Chia Sẻ
                  </GlowButton>
                  <GlowButton variant="secondary" onClick={fetchDailyFortune}>
                    🔄 Xem Lại
                  </GlowButton>
                </motion.div>
              </div>
            </AnimatePresence>
          ) : null}
        </motion.div>
      </div>
    </Layout>
  );
};

export default DailyFortunePage;