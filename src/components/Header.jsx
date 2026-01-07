// Header 컴포넌트
// - 상단 공통 헤더 UI
// - 아파트 관리자 로고 + 네비게이션 메뉴 제공
// - React.memo 사용 → 불필요한 리렌더링 방지

import { Link } from "react-router-dom";
import "./Header.css";

function Header() {
    return (
        <header className="header">
            <div className="header-container">
                {/* 로고 */}
                <h1 className="logo">🏢 아파트 관리자</h1>

                {/* 네비게이션 메뉴 */}
                <nav className="nav">
                    <Link to="/" className="nav-link">
                        홈
                    </Link>
                    <Link to="/notices" className="nav-link">
                        공지 관리
                    </Link>
                    <Link to="/parking" className="nav-link">
                        주차 관리
                    </Link>
                </nav>
            </div>
        </header>
    );
}

export default Header;
