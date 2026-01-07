import './HomeNoticesSection.css'

function HomeNoticesSection({recentNotices}) {

    return (
        //  📢 공지사항 영역
        <div className="notice-section-home">
            <section className="notice-section-home">
                <h2 className="notice-title-home">📢 공지사항</h2>

                {/* 공지사항이 있으면 최근 3개 표시, 없으면 안내 문구 */}
                {recentNotices.length > 0 ? (
                    <ul>
                        {recentNotices.map((notice) => (
                            <li key={notice.id} className="notice-item-home">
                                <p>{notice.text}</p>
                                <span className="date">{notice.createdAt}</span>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>공지사항이 없습니다.</p>
                )}
            </section>
        </div>
    );
}

export default HomeNoticesSection;