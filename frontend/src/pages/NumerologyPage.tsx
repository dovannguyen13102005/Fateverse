import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/layout/Layout';
import GlowButton from '../components/common/GlowButton';
import ResultCard from '../components/common/ResultCard';
import { useAuth } from '../contexts/AuthContext';
import { fortuneAPI } from '../utils/api';

interface NumerologyNumber {
  number: number;
  title: string;
  traits: string;
  career: string;
  challenges: string;
}

interface NumerologyResult {
  life_path: NumerologyNumber;
  expression: NumerologyNumber;
  soul_urge: NumerologyNumber;
  personality: NumerologyNumber;
}

export default function NumerologyPage() {
  const { user } = useAuth();
  const [name, setName] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [result, setResult] = useState<NumerologyResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fortuneAPI.numerology(user.id, {
        name,
        birth_date: new Date(birthDate),
      });

      setResult(response.data);
    } catch (error: any) {
      console.error('Numerology calculation failed:', error);
      setError(error.response?.data?.detail || 'Có lỗi xảy ra khi tính toán thần số học');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setName('');
    setBirthDate('');
    setResult(null);
    setError(null);
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
              🔢 Thần Số Học
            </motion.h1>
            <p className="text-xl text-white/80">
              Khám phá những con số định mệnh của bạn
            </p>
          </div>

          {!result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card mb-8"
            >
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-white/80 mb-2">Họ và Tên</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="input-field w-full"
                    placeholder="Nhập họ tên của bạn"
                    required
                  />
                </div>

                <div>
                  <label className="block text-white/80 mb-2">Ngày Sinh</label>
                  <input
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
                  type="submit" 
                  className="w-full"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                      Đang tính toán...
                    </>
                  ) : (
                    'Tính Số Mệnh 🔮'
                  )}
                </GlowButton>
              </form>
            </motion.div>
          )}

          <AnimatePresence>
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <ResultCard
                    title="Con Số Chủ Đạo"
                    emoji="🌟"
                    className="bg-gradient-to-br from-primary/20 to-accent/20"
                  >
                    <div className="text-center">
                      <div className="text-4xl font-display text-white mb-2">
                        {result.life_path.number}
                      </div>
                      <h4 className="text-xl font-display text-accent mb-2">
                        {result.life_path.title}
                      </h4>
                      <p className="text-white/80 mb-2">{result.life_path.traits}</p>
                      <p className="text-sm text-white/60">
                        <strong>Nghề nghiệp:</strong> {result.life_path.career}
                      </p>
                    </div>
                  </ResultCard>

                  <ResultCard
                    title="Số Biểu Đạt"
                    emoji="💫"
                    className="bg-gradient-to-br from-secondary/20 to-accent/20"
                  >
                    <div className="text-center">
                      <div className="text-4xl font-display text-white mb-2">
                        {result.expression.number}
                      </div>
                      <h4 className="text-xl font-display text-accent mb-2">
                        {result.expression.title}
                      </h4>
                      <p className="text-white/80 mb-2">{result.expression.traits}</p>
                      <p className="text-sm text-white/60">
                        <strong>Nghề nghiệp:</strong> {result.expression.career}
                      </p>
                    </div>
                  </ResultCard>

                  <ResultCard
                    title="Số Linh Hồn"
                    emoji="🎭"
                    className="bg-gradient-to-br from-accent/20 to-primary/20"
                  >
                    <div className="text-center">
                      <div className="text-4xl font-display text-white mb-2">
                        {result.soul_urge.number}
                      </div>
                      <h4 className="text-xl font-display text-accent mb-2">
                        {result.soul_urge.title}
                      </h4>
                      <p className="text-white/80 mb-2">{result.soul_urge.traits}</p>
                      <p className="text-sm text-white/60">
                        <strong>Thách thức:</strong> {result.soul_urge.challenges}
                      </p>
                    </div>
                  </ResultCard>

                  <ResultCard
                    title="Số Tính Cách"
                    emoji="🎲"
                    className="bg-gradient-to-br from-accent/20 to-secondary/20"
                  >
                    <div className="text-center">
                      <div className="text-4xl font-display text-white mb-2">
                        {result.personality.number}
                      </div>
                      <h4 className="text-xl font-display text-accent mb-2">
                        {result.personality.title}
                      </h4>
                      <p className="text-white/80 mb-2">{result.personality.traits}</p>
                      <p className="text-sm text-white/60">
                        <strong>Thách thức:</strong> {result.personality.challenges}
                      </p>
                    </div>
                  </ResultCard>
                </div>

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