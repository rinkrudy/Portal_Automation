// PageLayout.tsx
import React, { ReactNode } from 'react';
import '../styles/Layout.modules.css';

type LayoutType = 'single-column' | 'two-column' | 'three-column' | 'header-main-footer' | 'card-grid';

interface PageLayoutProps {
  layout: LayoutType;
  children: ReactNode;
}

const Layout: React.FC<PageLayoutProps> = ({ layout, children }) => {
  return <div className={layout}>{children}</div>;
};

export default Layout;
