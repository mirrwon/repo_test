import NoticesItem from './NoticesItem';
import './NoticesList.css';

function NoticesList({sortedData}) {

    return (
        //  공지 목록 영역
        <div className="notice-section">
            <ul className="notice-list">
                {sortedData.length === 0 ? (
                    <p className="empty">등록된 공지가 없습니다.</p>
                ) : (
                    sortedData.map((it) => (
                        <NoticesItem
                            key={it.id}
                            {...it} // 개별 공지 데이터 전달
                        />
                    ))
                )}
            </ul>
        </div>
    );
}

export default NoticesList;