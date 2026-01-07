//공지사항 관리 페이지 컴포넌트
// - 공지사항 입력 및 등록
// - 등록된 공지 목록 출력

import { useContext } from "react";
import { DataContext, DataDispatchContext } from "../context/DataContext"; // 상태 및 액션 context
import "./Notices.css";
import NoticesFrom from "../components/notices/NoticesForm";
import NoticesList from "../components/notices/NoticesList";
import { useSortedNotices } from "../hooks/useSortedNotices";

export default function Notices() {
    const { state } = useContext(DataContext);                  // 전체 데이터 상태 가져오기
    const { onCreateNoti } = useContext(DataDispatchContext);   // 공지 생성 액션
    const { notices } = state;                                  // 공지사항 목록

    // 최신 등록된 순으로 공지 정렬
    const sortedNotices = useSortedNotices(notices);

    return (
        <div className="notices-container">
            <h1 className="notices-title">📢 공지사항 관리</h1>
            <NoticesFrom onCreate={onCreateNoti} />
            <NoticesList sortedData={sortedNotices} />
        </div>
    );
}
