import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/layout/Layout';
import GlowButton from '../components/common/GlowButton';
import { useAuth } from '../contexts/AuthContext';
import { historyAPI } from '../utils/api';

interface HistoryItem {
  id: string;
  _id: string;
  user_id: string;
  type: string;
  result_summary: string;
  result_detail: any;
  created_at: string;
  is_favorite?: boolean;
  is_shared?: boolean;
  share_token?: string;
}

const TYPE_LABELS: { [key: string]: string } = {
  'numerology': 'Thần Số Học',
  'zodiac': 'Cung Hoàng Đạo',
  'tarot': 'Bài Tarot',
  'love': 'Tình Duyên',
  'fortune': 'Vận May Hàng Ngày'
};

const TYPE_ICONS: { [key: string]: string } = {
  'numerology': '🔢',
  'zodiac': '⭐',
  'tarot': '🃏',
  'love': '💕',
  'fortune': '🔮'
};

const HistoryPage = () => {
  const { user } = useAuth();
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState<string>('all');

  useEffect(() => {
    if (user) {
      loadHistory();
    }
  }, [user, selectedType]);

  const loadHistory = async () => {
    if (!user) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = selectedType === 'all'
        ? await historyAPI.getHistory(user.id, 50)
        : await historyAPI.getHistoryByType(user.id, selectedType, 50);
      
      setHistoryItems(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Không thể tải lịch sử');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (historyId: string) => {
    if (!confirm('Bạn có chắc muốn xóa mục này?')) return;
    
    try {
      await historyAPI.deleteHistory(historyId);
      setHistoryItems(historyItems.filter(item => item.id !== historyId));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Không thể xóa lịch sử');
    }
  };

  const handleToggleFavorite = async (historyId: string) => {
    try {
      const response = await historyAPI.toggleFavorite(historyId);
      setHistoryItems(historyItems.map(item => 
        item.id === historyId 
          ? { ...item, is_favorite: response.data.is_favorite }
          : item
      ));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Không thể cập nhật yêu thích');
    }
  };

  const handleShare = async (historyId: string) => {
    try {
      const response = await historyAPI.createShareLink(historyId);
      const shareUrl = `${window.location.origin}${response.data.share_url}`;
      
      // Copy to clipboard
      navigator.clipboard.writeText(shareUrl);
      alert('Đã sao chép link chia sẻ!');
      
      // Update state
      setHistoryItems(historyItems.map(item => 
        item.id === historyId 
          ? { ...item, is_shared: true, share_token: response.data.share_token }
          : item
      ));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Không thể tạo link chia sẻ');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!user) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-8 text-center">
          <h2 className="text-2xl text-white">Vui lòng đăng nhập để xem lịch sử</h2>
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
          className="max-w-4xl mx-auto"
        >
          <h1 className="text-3xl md:text-4xl font-display text-accent mb-6 text-center">
            📜 Lịch Sử Xem Bói
          </h1>

          {/* Filter tabs */}
          <div className="flex flex-wrap gap-2 mb-6 justify-center">
            <GlowButton
              variant={selectedType === 'all' ? 'primary' : 'secondary'}
              onClick={() => setSelectedType('all')}
            >
              Tất cả
            </GlowButton>
            {Object.entries(TYPE_LABELS).map(([type, label]) => (
              <GlowButton
                key={type}
                variant={selectedType === type ? 'primary' : 'secondary'}
                onClick={() => setSelectedType(type)}
              >
                {TYPE_ICONS[type]} {label}
              </GlowButton>
            ))}
          </div>

          {isLoading ? (
            <div className="text-center text-white py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent mx-auto mb-4" />
              <p>Đang tải lịch sử...</p>
            </div>
          ) : error ? (
            <div className="text-center text-red-400 py-12">
              <p>{error}</p>
              <GlowButton onClick={loadHistory} className="mt-4">
                Thử lại
              </GlowButton>
            </div>
          ) : historyItems.length === 0 ? (
            <div className="text-center text-white/60 py-12">
              <p className="text-xl mb-4">Bạn chưa có lịch sử xem bói nào</p>
              <p>Hãy thử các tính năng xem bói để bắt đầu! ✨</p>
            </div>
          ) : (
            <div className="space-y-4">
              <AnimatePresence>
                {historyItems.map((item, index) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, x: -100 }}
                    transition={{ delay: index * 0.05 }}
                    className="card hover:border-accent/40 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-2xl">{TYPE_ICONS[item.type]}</span>
                          <h3 className="text-lg font-display text-white">
                            {TYPE_LABELS[item.type] || item.type}
                          </h3>
                          {item.is_favorite && <span className="text-yellow-400">⭐</span>}
                          {item.is_shared && <span className="text-green-400">🔗</span>}
                        </div>
                        <p className="text-white/80 mb-2">{item.result_summary}</p>
                        <p className="text-sm text-white/50">
                          {formatDate(item.created_at)}
                        </p>
                      </div>
                      
                      <div className="flex flex-wrap gap-2">
                        <GlowButton
                          variant="secondary"
                          onClick={() => handleToggleFavorite(item.id)}
                          title={item.is_favorite ? 'Bỏ yêu thích' : 'Yêu thích'}
                        >
                          {item.is_favorite ? '⭐' : '☆'}
                        </GlowButton>
                        
                        <GlowButton
                          variant="secondary"
                          onClick={() => handleShare(item.id)}
                          title="Chia sẻ"
                        >
                          �
                        </GlowButton>
                        
                        <GlowButton
                          variant="secondary"
                          onClick={() => handleDelete(item.id)}
                          title="Xóa"
                        >
                          🗑️
                        </GlowButton>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          )}
        </motion.div>
      </div>
    </Layout>
  );
};

export default HistoryPage;