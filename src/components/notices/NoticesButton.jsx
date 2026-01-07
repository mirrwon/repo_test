import "./NoticesButton.css";

// 공통 버튼 컴포넌트
// - children: 버튼 내부에 표시할 텍스트/아이콘
// - onClick: 클릭 이벤트 핸들러
// - type: 스타일 지정용 클래스 (default, edit, delete, save, cancel 등)
function NoticesButton({ children, onClick, type = "default" }) {
    return (
        <button 
            className={`btn-notices ${type}`} // type에 따라 다른 CSS 적용
            onClick={onClick}
        >
            {children}
        </button>
    );
};

export default NoticesButton;
