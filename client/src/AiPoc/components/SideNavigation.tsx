import React, { useState } from 'react';
import '../styles/SideNavigation.module.css';

interface SideBarProps {
    expandMode?: 'push' | 'overlay'; // push는 페이지 콘텐츠를 밀고, overlay는 덮음
    foldMode?: 'hide' | 'partial'; // hide는 완전 숨김, partial은 5% 남김
}

const SideNavigation: React.FC<SideBarProps> = ({ expandMode = 'push', foldMode = 'partial' }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const toggleSidebar = () => {
        setIsExpanded((prev) => !prev);
    };

    return (
        <div className={`sidebar ${isExpanded ? 'expanded' : 'folded'} ${expandMode} ${foldMode}`}>
            {/* 상단의 토글 버튼 */}
            <button className="toggle-button" onClick={toggleSidebar}>
                {isExpanded ? 'Fold' : 'Expand'}
            </button>

            {/* 카테고리 버튼 */}
            <div className="categories">
                <button className="category-button" onClick={toggleSidebar}>
                    Category 1
                </button>
                <button className="category-button" onClick={toggleSidebar}>
                    Category 2
                </button>
            </div>
        </div>
    );
};

export default SideNavigation;
