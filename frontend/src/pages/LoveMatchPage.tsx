import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/layout/Layout';
import GlowButton from '../components/common/GlowButton';
import ResultCard from '../components/common/ResultCard';
import { useAuth } from '../contexts/AuthContext';
import { fortuneAPI } from '../utils/api';

interface LoveMatchResult {
  overall_compatibility: number;
  name_compatibility: number;
  zodiac_compatibility: number;
  level: string;
  description: string;
  advice: string;
}

const LoveMatchPage = () => {
  const { user } = useAuth();
  const [name1, setName1] = useState('');
  const [birthDate1, setBirthDate1] = useState('');
  const [name2, setName2] = useState('');
  const [birthDate2, setBirthDate2] = useState('');
  const [result, setResult] = useState<LoveMatchResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fortuneAPI.loveMatch(user.id, {
        name1,
        birth_date1: new Date(birthDate1),
        name2,
        birth_date2: new Date(birthDate2),
      });

      setResult(response.data);
    } catch (error: any) {
      console.error('Love match calculation failed:', error);
      setError(error.response?.data?.detail || 'Có lỗi xảy ra khi tính toán độ hợp đôi');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setName1('');
    setBirthDate1('');
    setName2('');
    setBirthDate2('');
    setResult(null);
    setError(null);
  };

  const getCompatibilityColor = (score: number) => {
    if (score >= 90) return 'from-emerald-500/20 to-emerald-800/20';
    if (score >= 80) return 'from-blue-500/20 to-blue-800/20';
    if (score >= 70) return 'from-yellow-500/20 to-yellow-800/20';
    if (score >= 60) return 'from-orange-500/20 to-orange-800/20';
    return 'from-red-500/20 to-red-800/20';
  };

  const getCompatibilityEmoji = (score: number) => {
    if (score >= 90) return '💖';
    if (score >= 80) return '💕';
    if (score >= 70) return '💝';
    if (score >= 60) return '💌';
    return '💔';
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="max-w-4xl mx-auto"
        >
          <div className="text-center mb-12">
            <motion.h1
              initial={{ y: -20 }}
              animate={{ y: 0 }}
              className="text-4xl md:text-5xl font-display text-accent mb-4"
            >
              💘 Bói Tình Duyên
            </motion.h1>
            <p className="text-xl text-white/80">
              Khám phá độ tương hợp giữa hai trái tim
            </p>
          </div>

          {!result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card mb-8"
            >
              <form onSubmit={handleSubmit} className="space-y-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {/* Person 1 */}
                  <div className="space-y-4">
                    <h3 className="text-xl font-display text-accent text-center">
                      💝 Người thứ nhất
                    </h3>
                    <div>
                      <label className="block text-white/80 mb-2">Tên</label>
                      <input
                        type="text"
                        value={name1}
                        onChange={(e) => setName1(e.target.value)}
                        className="input-field w-full"
                        placeholder="Nhập tên của bạn"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-white/80 mb-2">Ngày sinh</label>
                      <input
                        type="date"
                        value={birthDate1}
                        onChange={(e) => setBirthDate1(e.target.value)}
                        className="input-field w-full"
                        required
                      />
                    </div>
                  </div>

                  {/* Person 2 */}
                  <div className="space-y-4">
                    <h3 className="text-xl font-display text-accent text-center">
                      💕 Người thứ hai
                    </h3>
                    <div>
                      <label className="block text-white/80 mb-2">Tên</label>
                      <input
                        type="text"
                        value={name2}
                        onChange={(e) => setName2(e.target.value)}
                        className="input-field w-full"
                        placeholder="Nhập tên người ấy"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-white/80 mb-2">Ngày sinh</label>
                      <input
                        type="date"
                        value={birthDate2}
                        onChange={(e) => setBirthDate2(e.target.value)}
                        className="input-field w-full"
                        required
                      />
                    </div>
                  </div>
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

                <div className="text-center">
                  <GlowButton
                    type="submit"
                    disabled={isLoading}
                    className="w-full md:w-auto"
                  >
                    {isLoading ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                        Đang tính toán...
                      </>
                    ) : (
                      'Xem Độ Hợp 💘'
                    )}
                  </GlowButton>
                </div>
              </form>
            </motion.div>
          )}

          {/* Results */}
          <AnimatePresence>
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                {/* Main Compatibility Score */}
                <ResultCard
                  title="Độ Tương Hợp"
                  emoji={getCompatibilityEmoji(result.overall_compatibility)}
                  className={`bg-gradient-to-br ${getCompatibilityColor(result.overall_compatibility)} text-center`}
                >
                  <div className="space-y-4">
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.2 }}
                      className="text-6xl font-display text-white"
                    >
                      {result.overall_compatibility}%
                    </motion.div>
                    <div className="text-2xl font-display text-accent">
                      {result.level}
                    </div>
                    <p className="text-white/90 text-lg">
                      {result.description}
                    </p>
                  </div>
                </ResultCard>

                {/* Detailed Breakdown */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <ResultCard
                    title="Tương Hợp Tên"
                    emoji="📝"
                    className="bg-gradient-to-br from-purple-500/20 to-purple-800/20"
                  >
                    <div className="text-center">
                      <div className="text-3xl font-display text-white mb-2">
                        {result.name_compatibility}%
                      </div>
                      <p className="text-white/80">
                        Dựa trên thần số học của tên
                      </p>
                    </div>
                  </ResultCard>

                  <ResultCard
                    title="Tương Hợp Cung"
                    emoji="♉"
                    className="bg-gradient-to-br from-indigo-500/20 to-indigo-800/20"
                  >
                    <div className="text-center">
                      <div className="text-3xl font-display text-white mb-2">
                        {result.zodiac_compatibility}%
                      </div>
                      <p className="text-white/80">
                        Dựa trên cung hoàng đạo
                      </p>
                    </div>
                  </ResultCard>
                </div>

                {/* Advice */}
                <ResultCard
                  title="Lời Khuyên"
                  emoji="💌"
                  className="bg-gradient-to-br from-pink-500/20 to-pink-800/20"
                >
                  <p className="text-white/90 text-lg leading-relaxed">
                    {result.advice}
                  </p>
                </ResultCard>

                {/* Action Buttons */}
                <div className="flex justify-center gap-4 mt-8">
                  <GlowButton
                    variant="secondary"
                    onClick={resetForm}
                  >
                    Tính Lại 🔄
                  </GlowButton>
                  <GlowButton
                    variant="accent"
                    onClick={() => {/* TODO: Implement share */}}
                  >
                    Chia Sẻ 💌
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

export default LoveMatchPage;