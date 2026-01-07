//아파트 관리자 홈 페이지
// - 최근 등록된 공지 3개 표시
// - 각 동(101~104동) 주민 관리 페이지로 이동하는 네비게이션 버튼 제공

import { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { DataContext } from "../context/DataContext";
import "./Home.css";
import HomeNoticesSection from "../components/home/HomeNoticesSection";
import { useSortedNotices } from "../hooks/useSortedNotices";

export default function Home() {
    const { state } = useContext(DataContext);
    const { notices } = state;
    const [isDataLoaded, setIsDataLoaded] = useState(false);
    const recentNotices = useSortedNotices(notices).slice(0, 3); //React는 훅이 항상 같은 순서로 실행되어야 함. → 조건문 안에 넣지 않는다.

    useEffect(() => {
        setIsDataLoaded(true);
    }, [setIsDataLoaded])

    if (!isDataLoaded || !recentNotices) {
        return <div>데이터 로딩중...</div>
    }

    return (
        <div className="home-container">
            <h1 className="home-title">🏠 아파트 관리자 홈</h1>
            <HomeNoticesSection recentNotices={recentNotices}/>

            {/* 👥 각 동별 이동 버튼 */}
            <div className="nav-buttons">
                <Link to="/residents" className="btn btn-blue">
                    👥 101동
                </Link>
                <Link to="/residents" className="btn btn-blue">
                    👥 102동
                </Link>
                <Link to="/residents/page103" className="btn btn-blue">
                    👥 103동
                </Link>
                <Link to="/residents" className="btn btn-blue">
                    👥 104동
                </Link>
            </div>
        </div>
    );
}
