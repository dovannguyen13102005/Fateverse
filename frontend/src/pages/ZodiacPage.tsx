import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/layout/Layout';
import ResultCard from '../components/common/ResultCard';
import { useAuth } from '../contexts/AuthContext';
import { fortuneAPI } from '../utils/api';
import GlowButton from '../components/common/GlowButton';

interface ZodiacSign {
  zodiac_sign: string;
  name: string;
  symbol: string;
  element: string;
  description: string;
  date_range: string;
  traits: string[];
  lucky_colors: string[];
  lucky_numbers: number[];
  compatible_signs: string[];
}

const ZODIAC_TRANSLATIONS: { [key: string]: string } = {
  'Aries': 'Bạch Dương',
  'Taurus': 'Kim Ngưu',
  'Gemini': 'Song Tử',
  'Cancer': 'Cự Giải',
  'Leo': 'Sư Tử',
  'Virgo': 'Xử Nữ',
  'Libra': 'Thiên Bình',
  'Scorpio': 'Thiên Yết',
  'Sagittarius': 'Nhân Mã',
  'Capricorn': 'Ma Kết',
  'Aquarius': 'Bảo Bình',
  'Pisces': 'Song Ngư'
};

const ELEMENT_TRANSLATIONS: { [key: string]: string } = {
  'Fire': 'Hỏa',
  'Earth': 'Thổ',
  'Air': 'Khí',
  'Water': 'Thủy'
};

const ZodiacPage = () => {
  const { user } = useAuth();
  const [birthDate, setBirthDate] = useState('');
  const [sign, setSign] = useState<ZodiacSign | null>(null);
  const [showConstellation, setShowConstellation] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (sign) {
      setShowConstellation(true);
    }
  }, [sign]);

  const calculateZodiacSign = async () => {
    if (!user || !birthDate) return;
    
    setIsLoading(true);
    setError(null);

    try {
      const response = await fortuneAPI.zodiac(user.id, {
        birth_date: new Date(birthDate),
      });

      setSign(response.data);
    } catch (error: any) {
      console.error('Zodiac calculation failed:', error);
      setError(error.response?.data?.detail || 'Có lỗi xảy ra khi tính cung hoàng đạo');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setBirthDate('');
    setSign(null);
    setError(null);
    setShowConstellation(false);
  };

  return (
    <Layout title="Cung Hoàng Đạo">
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="max-w-3xl mx-auto"
        >
          {/* Input Form */}
          {!sign && (
            <div className="card mb-8">
              <div className="space-y-6">
                <div>
                  <label htmlFor="birthDate" className="block text-white/80 mb-2">
                    Ngày Sinh
                  </label>
                  <input
                    id="birthDate"
                    type="date"
                    value={birthDate}
                    onChange={(e) => setBirthDate(e.target.value)}
                    className="input-field w-full"
                    required
                  />
                </div>

                {error && (
                  <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="p-4 bg-red-500/20 border border-red-500/30 rounded-lg text-red-200"
                  >
                    {error}
                  </motion.div>
                )}

                <GlowButton
                  onClick={calculateZodiacSign}
                  className="w-full"
                  disabled={isLoading || !birthDate}
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                      Đang tính toán...
                    </>
                  ) : (
                    'Xem Cung Hoàng Đạo ✨'
                  )}
                </GlowButton>
              </div>
            </div>
          )}

          {/* Results */}
          <AnimatePresence mode="wait">
            {sign && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-6"
              >
                {/* Constellation Animation */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: showConstellation ? 1 : 0 }}
                  className="relative h-64 mb-8 card overflow-hidden bg-gradient-to-br from-blue-900/30 to-purple-900/30"
                >
                  <div className="absolute inset-0">
                    {/* Add dynamic constellation points and lines here */}
                    {Array.from({ length: 12 }).map((_, i) => (
                      <motion.div
                        key={i}
                        className="absolute w-1 h-1 bg-white rounded-full"
                        initial={{ opacity: 0 }}
                        animate={{
                          opacity: [0.2, 0.8, 0.2],
                          scale: [1, 1.2, 1],
                        }}
                        transition={{
                          duration: 2,
                          delay: i * 0.1,
                          repeat: Infinity,
                        }}
                        style={{
                          left: `${Math.random() * 100}%`,
                          top: `${Math.random() * 100}%`,
                        }}
                      />
                    ))}
                  </div>
                  <div className="relative z-10 flex items-center justify-center h-full">
                    <motion.span
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="text-8xl"
                    >
                      {sign.symbol}
                    </motion.span>
                  </div>
                </motion.div>

                {/* Sign Details */}
                <ResultCard
                  title={`${sign.name} - ${ZODIAC_TRANSLATIONS[sign.name]}`}
                  emoji={sign.symbol}
                  className="bg-gradient-to-br from-indigo-500/20 to-purple-800/20"
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-accent mb-2">Nguyên Tố</h4>
                      <p className="text-white/80">
                        {sign.element} ({ELEMENT_TRANSLATIONS[sign.element]})
                      </p>
                    </div>
                    <div>
                      <h4 className="text-accent mb-2">Thời Gian</h4>
                      <p className="text-white/80">{sign.date_range}</p>
                    </div>
                  </div>
                  <div className="mt-4">
                    <h4 className="text-accent mb-2">Đặc Điểm</h4>
                    <p className="text-white/80 mb-2">{sign.description}</p>
                    <div className="flex flex-wrap gap-2">
                      {sign.traits.map((trait: string) => (
                        <span key={trait} className="px-2 py-1 bg-white/10 rounded text-sm">
                          {trait}
                        </span>
                      ))}
                    </div>
                  </div>
                </ResultCard>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <ResultCard
                    title="Con Số May Mắn"
                    emoji="🎲"
                    className="bg-gradient-to-br from-emerald-500/20 to-emerald-800/20"
                  >
                    <p className="text-2xl font-display text-white">
                      {sign.lucky_numbers.join(', ')}
                    </p>
                  </ResultCard>

                  <ResultCard
                    title="Màu Sắc May Mắn"
                    emoji="🎨"
                    className="bg-gradient-to-br from-amber-500/20 to-amber-800/20"
                  >
                    <div className="flex flex-wrap gap-2">
                      {sign.lucky_colors.map((color: string) => (
                        <span
                          key={color}
                          className="px-3 py-1 rounded-full bg-white/10 text-white/80 capitalize"
                        >
                          {color}
                        </span>
                      ))}
                    </div>
                  </ResultCard>
                </div>

                <ResultCard
                  title="Cung Hợp"
                  emoji="💫"
                  className="bg-gradient-to-br from-pink-500/20 to-pink-800/20"
                >
                  <div className="flex flex-wrap gap-3">
                    {sign.compatible_signs.map((compatSign: string) => (
                      <motion.span
                        key={compatSign}
                        whileHover={{ scale: 1.1 }}
                        className="px-4 py-2 rounded-full bg-white/10 text-white/80"
                      >
                        {compatSign} - {ZODIAC_TRANSLATIONS[compatSign]}
                      </motion.span>
                    ))}
                  </div>
                </ResultCard>

                <div className="flex justify-center gap-4 mt-8">
                  <GlowButton 
                    variant="secondary"
                    onClick={resetForm}
                  >
                    Tính Lại 🔄
                  </GlowButton>
                  <GlowButton
                    variant="accent"
                    onClick={() => {/* Implement share functionality */}}
                  >
                    Chia Sẻ 🌠
                  </GlowButton>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </Layout>
  );
};

export default ZodiacPage;