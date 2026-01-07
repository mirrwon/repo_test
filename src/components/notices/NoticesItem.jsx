import React, { useState, useContext } from "react";
import { DataDispatchContext } from "../../context/DataContext";
import Button from "./NoticesButton";
import "./NoticesItem.css";

function NoticesItem({ id, text, createdAt }) {
    // 공지사항 수정/삭제 함수 가져오기
    const { onUpdateNoti, onDeleteNoti } = useContext(DataDispatchContext);

    // 수정 모드 여부
    const [isEdit, setIsEdit] = useState(false);
    // 수정 중인 텍스트 상태
    const [editText, setEditText] = useState(text);

    // 입력값 변경 핸들러
    const handleChangeText = (e) => {
        setEditText(e.target.value);
    };

    // 수정 저장
    const handleUpdateNotice = () => {
        onUpdateNoti(id, editText, createdAt);
        setIsEdit(false); // 수정 모드 종료
    };

    // 삭제
    const handleDeleteNotice = () => {
        if (window.confirm("공지사항을 정말 삭제할까요? (복구 불가)")) {
            onDeleteNoti(id);
        }
    };

    // 수정 버튼 클릭 → 수정 모드 진입
    const handleEditNotice = () => {
        setIsEdit(true);
    };

    // 취소 버튼 클릭 → 수정 모드 해제
    const handleCancelNotice = () => {
        setIsEdit(false);
    };

    return (
        <div>
            {!isEdit ? (
                // 기본 보기 모드
                <div className="notice-item">
                    <div className="notice-content">
                        <p className="notice-text">{text}</p>
                        <small className="notice-date">
                            작성일: {createdAt}
                        </small>
                    </div>

                    <div className="notice-actions">
                        <div className="btns">
                            <Button type="edit" onClick={handleEditNotice}>
                                수정
                            </Button>
                            <Button type="delete" onClick={handleDeleteNotice}>
                                삭제
                            </Button>
                        </div>
                    </div>
                </div>
            ) : (
                // 수정 모드
                <div className="notice-item">
                    <div className="notice-edit">
                        <input
                            type="text"
                            value={editText}
                            onChange={handleChangeText}
                        />
                        <small className="notice-date">
                            작성일: {createdAt}
                        </small>
                    </div>

                    <div className="notice-actions">
                        <div className="btns">
                            <Button type="save" onClick={handleUpdateNotice}>
                                저장
                            </Button>
                            <Button type="cancel" onClick={handleCancelNotice}>
                                취소
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default React.memo(NoticesItem);
