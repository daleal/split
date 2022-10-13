import { onMounted, onUnmounted } from 'vue';

/**
 * A hack to be able to use the view height attribute
 * when on mobile and avoid weird overflow bugs.
 * This works with the changes to the tailwind.config.cjs
 * file (the `theme.extend.height.screen` attribute)
 */
export const useViewHeightHack = () => {
  const setViewHeight = () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  };

  onMounted(() => {
    setViewHeight();
    window.addEventListener('resize', setViewHeight);
  });

  onUnmounted(() => {
    window.removeEventListener('resize', setViewHeight);
  });
};
