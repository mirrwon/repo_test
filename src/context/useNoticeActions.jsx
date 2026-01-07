import { useCallback } from "react";
import { getFormattedDate } from "../utils";
import { useMemo } from "react";
import { ACTIONS } from "../constant/notices";

function useNoticeActions(dispatch) {
    // 공지 생성
    const onCreateNoti = useCallback((text) => {
        dispatch({
            type: ACTIONS.CREATE_NOTICE,
            data: {
                text: text,
                createdAt: getFormattedDate(new Date()),
            },
        });
    }, [dispatch]);

    // 공지 수정
    const onUpdateNoti = useCallback((targetId, text, date) => {
        dispatch({
            type: ACTIONS.UPDATE_NOTICE,
            data: {
                id: targetId,
                text: text,
                createdAt: date,
            },
        });
    }, [dispatch]);

    // 공지 삭제
    const onDeleteNoti = useCallback((targetId) => {
        dispatch({
            type: ACTIONS.DELETE_NOTICE,
            targetId,
        });
    }, [dispatch]);

    // actions 묶어서 제공
    const noticesActions = useMemo(() => {
        return { onCreateNoti, onUpdateNoti, onDeleteNoti };
    }, [ onCreateNoti, onUpdateNoti, onDeleteNoti ]);

    return noticesActions;
}

export default useNoticeActions;