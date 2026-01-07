import { useState } from "react";
import './NoticesForm.css';

function NoticesFrom({ onCreate }) {
    const [text, setText] = useState('');                       // 입력창 상태

    // 입력창 값 변경 핸들러
    const handleChangetext = (e) => {
        setText(e.target.value);
    }

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            if (!text) {
                alert('등록할 공지사항을 입력하세요!!!');
            } else {
                onCreate(text); // 새로운 공지 등록
                setText('');        // 입력창 초기화
            }
        }
    };

    // 공지 등록 버튼 클릭 시 실행
    const onAddNotice = () => {
        if (!text) {
            alert('등록할 공지사항을 입력하세요!!!');
        } else {
            onCreate(text); // 새로운 공지 등록
            setText('');        // 입력창 초기화
        }
    }


    return (
        // 공지 작성 영역
        <div className="notice-input">
            <input
                type="text"
                placeholder="공지사항 입력"
                value={text}
                onChange={handleChangetext}
                onKeyDown={handleKeyDown}
            />
            <button onClick={onAddNotice}>등록</button>
        </div>
    );
}

export default NoticesFrom;