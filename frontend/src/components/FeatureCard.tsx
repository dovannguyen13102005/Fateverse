import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

interface FeatureCardProps {
  title: string;
  description: string;
  icon: string;
  path: string;
  color?: string;
}

const FeatureCard = ({ title, description, icon, path, color = 'purple' }: FeatureCardProps) => {
  const gradientColors = {
    purple: 'from-purple-500/20 to-purple-900/20',
    blue: 'from-blue-500/20 to-blue-900/20',
    pink: 'from-pink-500/20 to-pink-900/20',
    green: 'from-green-500/20 to-green-900/20',
    yellow: 'from-yellow-500/20 to-yellow-900/20'
  };

  return (
    <Link to={path}>
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className={`card bg-gradient-to-br ${gradientColors[color as keyof typeof gradientColors]} 
          backdrop-blur-lg border border-white/10 hover:border-accent/50 transition-all duration-300`}
      >
        <div className="text-4xl mb-4">{icon}</div>
        <h3 className="text-2xl font-cinzel text-accent mb-2">
          {title}
        </h3>
        <p className="text-white/70">{description}</p>
      </motion.div>
    </Link>
  );
};

export default FeatureCard;