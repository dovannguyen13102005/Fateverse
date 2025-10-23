import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import Layout from '../components/Layout';

const features = [
  {
    title: 'Thần Số Học',
    description: 'Khám phá con số vận mệnh và định hướng cuộc đời của bạn',
    icon: '🔢',
    path: '/numerology',
    color: 'purple',
    gradient: 'from-purple-500/20 to-purple-800/20'
  },
  {
    title: 'Cung Hoàng Đạo',
    description: 'Xem cung hoàng đạo và sự tương hợp của bạn',
    icon: '♉',
    path: '/zodiac',
    color: 'blue',
    gradient: 'from-blue-500/20 to-blue-800/20'
  },
  {
    title: 'Bói Tình Duyên',
    description: 'Tính toán độ hợp đôi và dự đoán tình duyên',
    icon: '💘',
    path: '/love',
    color: 'pink',
    gradient: 'from-pink-500/20 to-pink-800/20'
  },
  {
    title: 'Tarot',
    description: 'Khám phá thông điệp từ các lá bài Tarot',
    icon: '🔮',
    path: '/tarot',
    color: 'yellow',
    gradient: 'from-amber-500/20 to-amber-800/20'
  },
  {
    title: 'Lá Số Hôm Nay',
    description: 'Dự đoán vận may và lời khuyên cho ngày mới',
    icon: '🌟',
    path: '/daily',
    color: 'green',
    gradient: 'from-emerald-500/20 to-emerald-800/20'
  }
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { y: 20, opacity: 0 },
  show: { y: 0, opacity: 1 }
};

const HomePage = () => {
  return (
    <Layout title="FateVerse - Khám Phá Vận Mệnh">
      <div className="container mx-auto px-4 py-8 md:py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto text-center mb-12"
        >
          <h1 className="text-4xl md:text-6xl font-display bg-gradient-to-r from-accent via-secondary to-primary bg-clip-text text-transparent mb-6">
            Welcome to FateVerse
          </h1>
          <p className="text-xl text-white/80">
            Khám phá vận mệnh của bạn thông qua sự kết hợp của trí tuệ cổ xưa và công nghệ hiện đại
          </p>
        </motion.div>

        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {features.map((feature) => (
            <motion.div key={feature.path} variants={item}>
              <Link to={feature.path}>
                <motion.div
                  whileHover={{ 
                    scale: 1.05,
                    backgroundColor: 'rgba(255, 255, 255, 0.1)'
                  }}
                  whileTap={{ scale: 0.95 }}
                  className={"card relative overflow-hidden bg-gradient-to-br " + feature.gradient + " backdrop-blur-lg border border-white/10 hover:border-white/20 transition-all duration-300"}
                >
                  <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-white/5 to-white/0 pointer-events-none" />
                  <div className="relative p-6">
                    <span className="text-4xl mb-4 block animate-float">{feature.icon}</span>
                    <h3 className="text-2xl font-display text-white mb-2">{feature.title}</h3>
                    <p className="text-white/70">{feature.description}</p>
                  </div>
                </motion.div>
              </Link>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-16 text-center"
        >
          <Link to="/daily">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="glow-button"
            >
              Xem Lá Số Hôm Nay ✨
            </motion.button>
          </Link>
        </motion.div>
      </div>
    </Layout>
  );
};

export default HomePage;