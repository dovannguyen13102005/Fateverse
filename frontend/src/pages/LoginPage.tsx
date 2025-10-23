import { motion } from 'framer-motion';
import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import GoogleLoginButton from '../components/auth/GoogleLoginButton';
import { useAuth } from '../contexts/AuthContext';

const LoginPage = () => {
  const { isAuthenticated, isLoading, loginWithEmail, registerWithEmail } = useAuth();
  const [loginError, setLoginError] = useState<string | null>(null);
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    confirmPassword: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Redirect if already authenticated
  if (isAuthenticated && !isLoading) {
    return <Navigate to="/" replace />;
  }

  const handleLoginSuccess = () => {
    setLoginError(null);
    // Navigation will be handled by the redirect above
  };

  const handleLoginError = (error: any) => {
    setLoginError(error.message || 'Đăng nhập thất bại. Vui lòng thử lại.');
  };

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);
    setIsSubmitting(true);

    try {
      if (isRegisterMode) {
        // Validate
        if (formData.password !== formData.confirmPassword) {
          setLoginError('Mật khẩu xác nhận không khớp');
          setIsSubmitting(false);
          return;
        }
        if (formData.password.length < 6) {
          setLoginError('Mật khẩu phải có ít nhất 6 ký tự');
          setIsSubmitting(false);
          return;
        }
        if (!formData.name.trim()) {
          setLoginError('Vui lòng nhập tên của bạn');
          setIsSubmitting(false);
          return;
        }

        // Register
        await registerWithEmail({
          email: formData.email,
          password: formData.password,
          name: formData.name
        });
      } else {
        // Login
        await loginWithEmail(formData.email, formData.password);
      }
      handleLoginSuccess();
    } catch (error: any) {
      handleLoginError(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full"
      >
        <div className="card bg-white/10 backdrop-blur-lg border border-white/20">
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2 }}
              className="text-6xl mb-4"
            >
              🔮
            </motion.div>
            <h1 className="text-3xl font-display text-accent mb-2">
              Chào mừng đến FateVerse
            </h1>
            <p className="text-white/70">
              {isRegisterMode ? 'Đăng ký tài khoản mới' : 'Đăng nhập để khám phá vận mệnh của bạn'}
            </p>
          </div>

          {loginError && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg text-red-200 text-sm"
            >
              {loginError}
            </motion.div>
          )}

          <div className="space-y-6">
            {/* Tab Selector */}
            <div className="flex gap-2 bg-white/5 rounded-lg p-1">
              <button
                type="button"
                onClick={() => setIsRegisterMode(false)}
                className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                  !isRegisterMode
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                    : 'text-white/70 hover:text-white'
                }`}
              >
                Đăng nhập
              </button>
              <button
                type="button"
                onClick={() => setIsRegisterMode(true)}
                className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                  isRegisterMode
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                    : 'text-white/70 hover:text-white'
                }`}
              >
                Đăng ký
              </button>
            </div>

            {/* Email/Password Form */}
            <form onSubmit={handleEmailSubmit} className="space-y-4">
              {isRegisterMode && (
                <div>
                  <label className="block text-white/70 text-sm mb-2">
                    Tên của bạn
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/30 focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/50 transition-all"
                    placeholder="Nhập tên của bạn"
                    required={isRegisterMode}
                  />
                </div>
              )}

              <div>
                <label className="block text-white/70 text-sm mb-2">
                  Email
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/30 focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/50 transition-all"
                  placeholder="your@email.com"
                  required
                />
              </div>

              <div>
                <label className="block text-white/70 text-sm mb-2">
                  Mật khẩu
                </label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/30 focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/50 transition-all"
                  placeholder="••••••••"
                  required
                />
              </div>

              {isRegisterMode && (
                <div>
                  <label className="block text-white/70 text-sm mb-2">
                    Xác nhận mật khẩu
                  </label>
                  <input
                    type="password"
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/30 focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/50 transition-all"
                    placeholder="••••••••"
                    required={isRegisterMode}
                  />
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-lg"
              >
                {isSubmitting ? 'Đang xử lý...' : (isRegisterMode ? 'Đăng ký ngay' : 'Đăng nhập')}
              </button>
            </form>

            {/* Divider */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-white/20"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-transparent text-white/50">hoặc tiếp tục với</span>
              </div>
            </div>

            {/* Google Login */}
            <GoogleLoginButton
              onSuccess={handleLoginSuccess}
              onError={handleLoginError}
            />

            <div className="text-center text-white/50 text-sm">
              Bằng việc đăng nhập, bạn đồng ý với{' '}
              <a href="#" className="text-accent hover:underline">
                Điều khoản sử dụng
              </a>{' '}
              và{' '}
              <a href="#" className="text-accent hover:underline">
                Chính sách bảo mật
              </a>{' '}
              của chúng tôi.
            </div>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-center mt-8 text-white/60"
        >
          <p>
            Khám phá thần số học, cung hoàng đạo, tình duyên và nhiều hơn nữa...
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default LoginPage;