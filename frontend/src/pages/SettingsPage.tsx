import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import GlowButton from '../components/common/GlowButton';
import { useAuth } from '../contexts/AuthContext';
import { authAPI } from '../utils/api';

const themes = [
  { id: 'galaxy', name: 'Galaxy', emoji: '🌌', color: '#8A2BE2' },
  { id: 'nebula', name: 'Nebula', emoji: '🌠', color: '#4B0082' },
  { id: 'sunrise', name: 'Sunrise', emoji: '🌅', color: '#FFD700' },
  { id: 'ocean', name: 'Ocean', emoji: '🌊', color: '#1E90FF' },
  { id: 'forest', name: 'Forest', emoji: '🌲', color: '#228B22' },
  { id: 'sunset', name: 'Sunset', emoji: '🌇', color: '#FF6347' }
];

interface UserSettings {
  name: string;
  birth_date: string;
  gender: string;
  theme_preference: string;
  picture?: string;
  notification_enabled?: boolean;
}

interface UserStatistics {
  total_fortunes: number;
  by_type: {
    fortune: number;
    tarot: number;
    love: number;
    numerology: number;
    zodiac: number;
  };
  favorites_count: number;
  shared_count: number;
  last_fortune_date: string | null;
  member_since: string;
  days_active: number;
}

const SettingsPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [settings, setSettings] = useState<UserSettings>({
    name: '',
    birth_date: '',
    gender: '',
    theme_preference: 'galaxy',
    picture: '',
    notification_enabled: true
  });
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [statistics, setStatistics] = useState<UserStatistics | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [showStatistics, setShowStatistics] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  useEffect(() => {
    if (user) {
      loadUserProfile();
    }
  }, [user]);

  // Apply theme immediately when changed
  useEffect(() => {
    if (settings.theme_preference) {
      const themeColors: Record<string, { bg: string, accent: string }> = {
        galaxy: { bg: 'linear-gradient(to bottom, #0a0118, #1a0a2e)', accent: '#8a2be2' },
        nebula: { bg: 'linear-gradient(to bottom, #0d0221, #1a0d33)', accent: '#4b0082' },
        sunrise: { bg: 'linear-gradient(to bottom, #1a0f08, #2d1810)', accent: '#ffd700' },
        ocean: { bg: 'linear-gradient(to bottom, #001a33, #002244)', accent: '#1e90ff' },
        forest: { bg: 'linear-gradient(to bottom, #0a1f0a, #133013)', accent: '#228b22' },
        sunset: { bg: 'linear-gradient(to bottom, #1a0808, #2d1010)', accent: '#ff6347' }
      };
      
      const theme = themeColors[settings.theme_preference];
      if (theme) {
        document.body.style.background = theme.bg;
        document.body.style.backgroundAttachment = 'fixed';
        // Store accent color for potential use
        document.documentElement.style.setProperty('--theme-accent', theme.accent);
      }
    }
  }, [settings.theme_preference]);

  const loadUserProfile = async () => {
    if (!user) return;
    
    setIsLoading(true);
    try {
      const response = await authAPI.getProfile(user.id);
      const userData = response.data;
      
      setSettings({
        name: userData.name || '',
        birth_date: userData.birth_date ? new Date(userData.birth_date).toISOString().split('T')[0] : '',
        gender: userData.gender || '',
        theme_preference: userData.theme_preference || 'galaxy',
        picture: userData.picture || '',
        notification_enabled: userData.notification_enabled ?? true
      });
    } catch (err: any) {
      setMessage({ type: 'error', text: 'Không thể tải thông tin người dùng' });
    } finally {
      setIsLoading(false);
    }
  };

  const loadStatistics = async () => {
    if (!user) return;
    
    try {
      const response = await authAPI.getStatistics(user.id);
      setStatistics(response.data);
    } catch (err: any) {
      console.error('Failed to load statistics:', err);
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setMessage({ type: 'error', text: 'Vui lòng chọn file ảnh hợp lệ' });
        return;
      }

      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setMessage({ type: 'error', text: 'Kích thước ảnh không được vượt quá 5MB' });
        return;
      }

      setSelectedImage(file);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const convertImageToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const handleExportData = async () => {
    if (!user) return;

    try {
      setMessage({ type: 'success', text: 'Đang xuất dữ liệu...' });
      const response = await authAPI.exportData(user.id);
      
      // Create download link
      const dataStr = JSON.stringify(response.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `fateverse_data_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      setMessage({ type: 'success', text: 'Đã xuất dữ liệu thành công! ✅' });
    } catch (err: any) {
      setMessage({ 
        type: 'error', 
        text: 'Không thể xuất dữ liệu. Vui lòng thử lại.' 
      });
    }
  };

  const handleDeleteAccount = async () => {
    if (!user) return;

    setIsDeleting(true);
    try {
      await authAPI.deleteAccount(user.id);
      setMessage({ type: 'success', text: 'Tài khoản đã được xóa. Đang đăng xuất...' });
      setTimeout(() => {
        logout();
      }, 2000);
    } catch (err: any) {
      setMessage({ 
        type: 'error', 
        text: err.response?.data?.detail || 'Không thể xóa tài khoản. Vui lòng thử lại.' 
      });
      setIsDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  const handleSave = async () => {
    if (!user) return;

    setIsSaving(true);
    setMessage(null);

    try {
      const updateData: any = {
        name: settings.name,
        theme_preference: settings.theme_preference,
        notification_enabled: settings.notification_enabled
      };

      if (settings.birth_date) {
        updateData.birth_date = new Date(settings.birth_date).toISOString();
      }

      if (settings.gender) {
        updateData.gender = settings.gender;
      }

      // Handle image upload
      if (selectedImage) {
        const base64Image = await convertImageToBase64(selectedImage);
        updateData.picture = base64Image;
      }

      const response = await authAPI.updateProfile(user.id, updateData);
      setMessage({ type: 'success', text: 'Đã lưu thay đổi thành công! ✅' });
      
      // Update localStorage with new user info
      const updatedUser = response.data;
      const currentUserInfo = localStorage.getItem('userInfo');
      if (currentUserInfo) {
        const userInfo = JSON.parse(currentUserInfo);
        const newUserInfo = {
          ...userInfo,
          ...updatedUser
        };
        localStorage.setItem('userInfo', JSON.stringify(newUserInfo));
      }
      
      // Clear selected image after save
      setSelectedImage(null);
      setImagePreview('');
      
      // Only reload if image was uploaded (to refresh avatar everywhere)
      if (selectedImage) {
        setTimeout(() => {
          window.location.reload();
        }, 1500);
      } else {
        // Just hide the message after 3 seconds
        setTimeout(() => {
          setMessage(null);
        }, 3000);
      }
    } catch (err: any) {
      setMessage({ 
        type: 'error', 
        text: err.response?.data?.detail || 'Không thể lưu thay đổi. Vui lòng thử lại.' 
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleLogout = () => {
    if (confirm('Bạn có chắc muốn đăng xuất?')) {
      logout();
      navigate('/login');
    }
  };

  if (!user) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-8 text-center">
          <h2 className="text-2xl text-white">Vui lòng đăng nhập để truy cập cài đặt</h2>
        </div>
      </Layout>
    );
  }

  if (isLoading) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent mx-auto mb-4" />
          <p className="text-white">Đang tải...</p>
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
            ⚙️ Cài Đặt
          </h1>
          <p className="text-white/70 text-center mb-8">
            Quản lý thông tin cá nhân và tùy chỉnh trải nghiệm
          </p>

          <div className="card space-y-6">
            {/* Profile Picture */}
            <div className="flex flex-col items-center">
              <div className="relative group">
                <div className="w-32 h-32 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-white text-4xl overflow-hidden mb-4">
                  {imagePreview ? (
                    <img
                      src={imagePreview}
                      alt="Avatar Preview"
                      className="w-full h-full object-cover"
                    />
                  ) : settings.picture ? (
                    <img
                      src={settings.picture}
                      alt="Avatar"
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <span className="text-5xl">👤</span>
                  )}
                </div>
                <label className="absolute bottom-4 right-0 w-10 h-10 bg-accent hover:bg-accent/80 rounded-full flex items-center justify-center cursor-pointer shadow-lg transition-transform hover:scale-110">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="hidden"
                  />
                  <span className="text-white text-xl">📷</span>
                </label>
              </div>
              <p className="text-white/60 text-sm text-center">
                {selectedImage 
                  ? `Ảnh mới: ${selectedImage.name}` 
                  : settings.picture 
                  ? 'Ảnh đại diện từ Google Account' 
                  : 'Chưa có ảnh đại diện'}
              </p>
              <p className="text-white/50 text-xs text-center mt-1">
                Click vào icon 📷 để thay đổi ảnh (Tối đa 5MB)
              </p>
            </div>

            {/* Name */}
            <div>
              <label className="block text-white mb-2 font-display">
                👤 Họ và Tên
              </label>
              <input
                type="text"
                value={settings.name}
                onChange={(e) => setSettings({ ...settings, name: e.target.value })}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-accent"
                placeholder="Nhập họ tên của bạn"
              />
            </div>

            {/* Email (Read-only) */}
            <div>
              <label className="block text-white mb-2 font-display">
                📧 Email
              </label>
              <input
                type="email"
                value={user.email}
                disabled
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white/60 cursor-not-allowed"
              />
              <p className="text-white/50 text-sm mt-1">
                Email không thể thay đổi
              </p>
            </div>

            {/* Birth Date */}
            <div>
              <label className="block text-white mb-2 font-display">
                🎂 Ngày Sinh
              </label>
              <input
                type="date"
                value={settings.birth_date}
                onChange={(e) => setSettings({ ...settings, birth_date: e.target.value })}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-accent"
              />
              <p className="text-white/50 text-sm mt-1">
                Ngày sinh giúp tính toán chính xác hơn trong Thần Số Học
              </p>
            </div>

            {/* Gender */}
            <div>
              <label className="block text-white mb-2 font-display">
                ⚧️ Giới Tính
              </label>
              <select
                value={settings.gender}
                onChange={(e) => setSettings({ ...settings, gender: e.target.value })}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-accent"
              >
                <option value="">Chọn giới tính</option>
                <option value="male">Nam</option>
                <option value="female">Nữ</option>
                <option value="other">Khác</option>
              </select>
            </div>

            {/* Theme Selection */}
            <div>
              <label className="block text-white mb-3 font-display">
                🎨 Giao Diện
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {themes.map((theme) => (
                  <motion.button
                    key={theme.id}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setSettings({ ...settings, theme_preference: theme.id })}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      settings.theme_preference === theme.id
                        ? 'border-accent bg-accent/20'
                        : 'border-white/20 bg-white/5 hover:border-white/40'
                    }`}
                  >
                    <div className="text-4xl mb-2">{theme.emoji}</div>
                    <div className="text-white font-display">
                      {theme.name}
                    </div>
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Message */}
            {message && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`p-4 rounded-lg ${
                  message.type === 'success' 
                    ? 'bg-green-500/20 border border-green-500/50 text-green-200' 
                    : 'bg-red-500/20 border border-red-500/50 text-red-200'
                }`}
              >
                {message.text}
              </motion.div>
            )}

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
              <GlowButton
                onClick={handleSave}
                disabled={isSaving}
                className="flex-1"
              >
                {isSaving ? (
                  <>
                    <span className="animate-spin mr-2">🔄</span>
                    Đang lưu...
                  </>
                ) : (
                  <>💾 Lưu Thay Đổi</>
                )}
              </GlowButton>
              <GlowButton
                variant="secondary"
                onClick={handleLogout}
                className="flex-1"
              >
                🚪 Đăng Xuất
              </GlowButton>
            </div>

            {/* Notification Settings */}
            <div className="pt-4 border-t border-white/10">
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-white font-display">
                  🔔 Thông Báo
                </span>
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={settings.notification_enabled}
                    onChange={(e) => setSettings({ ...settings, notification_enabled: e.target.checked })}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-white/20 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-accent rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent"></div>
                </div>
              </label>
              <p className="text-white/50 text-sm mt-1">
                Nhận thông báo về tính năng mới và lời nhắc hàng ngày
              </p>
            </div>

            {/* Statistics Section */}
            <div className="pt-4 border-t border-white/10">
              <button
                onClick={() => {
                  setShowStatistics(!showStatistics);
                  if (!showStatistics && !statistics) {
                    loadStatistics();
                  }
                }}
                className="w-full flex items-center justify-between text-white font-display hover:text-accent transition-colors"
              >
                <span>📊 Thống Kê Cá Nhân</span>
                <span className="text-2xl">
                  {showStatistics ? '▼' : '▶'}
                </span>
              </button>
              
              {showStatistics && statistics && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className="mt-4 space-y-3"
                >
                  <div className="bg-white/5 rounded-lg p-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <div className="text-3xl font-bold text-accent">
                          {statistics.total_fortunes}
                        </div>
                        <div className="text-white/60 text-sm">
                          Tổng lượt bói
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="text-3xl font-bold text-accent">
                          {statistics.days_active}
                        </div>
                        <div className="text-white/60 text-sm">
                          Ngày hoạt động
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="text-3xl font-bold text-pink-400">
                          {statistics.favorites_count}
                        </div>
                        <div className="text-white/60 text-sm">
                          Yêu thích
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="text-3xl font-bold text-blue-400">
                          {statistics.shared_count}
                        </div>
                        <div className="text-white/60 text-sm">
                          Đã chia sẻ
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-white/5 rounded-lg p-4">
                    <h4 className="text-white font-display mb-3">Theo loại:</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">🌟 Lá số hôm nay</span>
                        <span className="text-white font-semibold">{statistics.by_type.fortune}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">🔮 Tarot</span>
                        <span className="text-white font-semibold">{statistics.by_type.tarot}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">💕 Tình duyên</span>
                        <span className="text-white font-semibold">{statistics.by_type.love}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">🔢 Thần số học</span>
                        <span className="text-white font-semibold">{statistics.by_type.numerology}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">⭐ Cung hoàng đạo</span>
                        <span className="text-white font-semibold">{statistics.by_type.zodiac}</span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </div>

            {/* Data Management */}
            <div className="pt-4 border-t border-white/10">
              <h3 className="text-white font-display mb-3">💾 Quản Lý Dữ Liệu</h3>
              <div className="space-y-2">
                <button
                  onClick={handleExportData}
                  className="w-full px-4 py-3 bg-blue-500/20 border border-blue-500/50 rounded-lg text-blue-200 hover:bg-blue-500/30 transition-colors text-left"
                >
                  📥 Xuất Dữ Liệu (JSON)
                </button>
                <p className="text-white/50 text-sm px-2">
                  Tải xuống toàn bộ dữ liệu cá nhân của bạn
                </p>
              </div>
            </div>

            {/* Danger Zone */}
            <div className="pt-4 border-t border-red-500/30">
              <h3 className="text-red-400 font-display mb-3">⚠️ Vùng Nguy Hiểm</h3>
              <div className="space-y-3">
                {!showDeleteConfirm ? (
                  <button
                    onClick={() => setShowDeleteConfirm(true)}
                    className="w-full px-4 py-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 hover:bg-red-500/30 transition-colors"
                  >
                    🗑️ Xóa Tài Khoản
                  </button>
                ) : (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="space-y-3 bg-red-500/10 border border-red-500/50 rounded-lg p-4"
                  >
                    <p className="text-red-200 font-semibold">
                      ⚠️ Bạn có chắc chắn muốn xóa tài khoản?
                    </p>
                    <p className="text-red-300/70 text-sm">
                      Hành động này không thể hoàn tác. Tất cả dữ liệu của bạn sẽ bị xóa vĩnh viễn bao gồm:
                    </p>
                    <ul className="text-red-300/70 text-sm list-disc list-inside space-y-1">
                      <li>Thông tin cá nhân</li>
                      <li>Lịch sử bói toán</li>
                      <li>Các mục yêu thích</li>
                      <li>Cài đặt và tùy chỉnh</li>
                    </ul>
                    <div className="flex gap-2 pt-2">
                      <button
                        onClick={handleDeleteAccount}
                        disabled={isDeleting}
                        className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-white font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isDeleting ? (
                          <>
                            <span className="animate-spin mr-2">🔄</span>
                            Đang xóa...
                          </>
                        ) : (
                          'Xác Nhận Xóa'
                        )}
                      </button>
                      <button
                        onClick={() => setShowDeleteConfirm(false)}
                        disabled={isDeleting}
                        className="flex-1 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Hủy
                      </button>
                    </div>
                  </motion.div>
                )}
              </div>
            </div>

            {/* Account Info */}
            <div className="pt-4 border-t border-white/10">
              <p className="text-white/50 text-sm text-center">
                Tài khoản được tạo: {user.created_at ? new Date(user.created_at).toLocaleDateString('vi-VN') : 'N/A'}
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default SettingsPage;