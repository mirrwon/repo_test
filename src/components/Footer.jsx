import "./Footer.css";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        
        {/* 로고 및 소개 */}
        <div className="footer-section">
          <h4>🏢 아파트 관리자</h4>
          <p>입주민과 함께하는 스마트 아파트 관리 시스템</p>
        </div>

        {/* 빠른 메뉴 */}
        <div className="footer-section">
          <h4>📌 빠른 메뉴</h4>
          <ul>
            <li><a href="/home">홈</a></li>
            <li><a href="/notices">공지 관리</a></li>
            <li><a href="/parkings">주차 관리</a></li>
          </ul>
        </div>

        {/* 연락처 정보 */}
        <div className="footer-section">
          <h4>📞 연락처</h4>
          <p>관리사무소: 02-123-4567</p>
          <p>Email: admin@apartment.com</p>
        </div>
      </div>

      {/* 하단 저작권 표시 */}
      <div className="footer-bottom">
        <p>© {year} 아파트 관리자 | All Rights Reserved</p>
      </div>
    </footer>
  );
};

export default Footer;
