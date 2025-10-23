import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';

declare global {
  interface Window {
    google: any;
  }
}

interface GoogleLoginButtonProps {
  onSuccess?: () => void;
  onError?: (error: any) => void;
}

const GoogleLoginButton: React.FC<GoogleLoginButtonProps> = ({
  onSuccess,
  onError,
}) => {
  const { loginWithGoogle } = useAuth();
  const googleButtonRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Load Google Identity Services script
    const loadGoogleScript = () => {
      if (window.google) {
        initializeGoogleSignIn();
        return;
      }

      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      script.onload = initializeGoogleSignIn;
      document.head.appendChild(script);
    };

    const initializeGoogleSignIn = () => {
      const clientId = (import.meta as any).env.VITE_GOOGLE_CLIENT_ID;
      
      if (window.google && googleButtonRef.current) {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: handleCredentialResponse,
          auto_select: false,
          cancel_on_tap_outside: true,
        });

        window.google.accounts.id.renderButton(
          googleButtonRef.current,
          {
            theme: 'filled_black',
            size: 'large',
            width: 400,
            text: 'signin_with',
            shape: 'rectangular',
          }
        );
      }
    };

    const handleCredentialResponse = async (response: any) => {
      try {
        await loginWithGoogle(response.credential);
        onSuccess?.();
      } catch (error) {
        console.error('Login error:', error);
        onError?.(error);
      }
    };

    loadGoogleScript();

    return () => {
      // Cleanup - remove script if needed
      const scripts = document.querySelectorAll('script[src*="gsi/client"]');
      scripts.forEach(script => script.remove());
    };
  }, [loginWithGoogle, onSuccess, onError]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full"
    >
      <div
        ref={googleButtonRef}
        className="w-full flex justify-center"
      />
    </motion.div>
  );
};

export default GoogleLoginButton;