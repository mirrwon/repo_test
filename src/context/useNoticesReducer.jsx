import { notices } from "../data/dummyData";
import { useReducer, useEffect } from "react";
import { ACTIONS, STORAGE_KEY } from "../constant/notices";

// Reducer: 액션에 따라 상태 변경
const reducer = (state, action) => {
    switch (action.type) {
        case ACTIONS.CREATE_NOTICE:
            return {
                ...state,
                    notices: [
                        ...state.notices,
                        { id: state.noticesId, ...action.data },
                    ], // 새 공지 맨 뒤에 추가
                noticesId: state.noticesId + 1,
            };

        case ACTIONS.UPDATE_NOTICE:
            return {
                ...state,
                    notices: state.notices.map((it) =>
                        Number(it.id) === Number(action.data.id) ? { ...it, text: action.data.text } : it
                    ),
            };

        case ACTIONS.DELETE_NOTICE:
            return {
                ...state,
                    notices: state.notices.filter(
                        (it) => Number(it.id) !== Number(action.targetId)
                    ),
            };

        default:
            return state;
    }
};

function useNoticesReducer() {
    const [state, dispatch] = useReducer(reducer, { notices: [], noticesId: 0 });

    useEffect(() => {
        // 초기 데이터 로드 (localStorage → 없으면 dummyData)
        // localStorage.clear(); // 필요시 초기화용
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            const localData = JSON.parse(saved);
            state.notices = localData.notices;
            state.noticesId = localData.noticesId;
        } else {
            state.notices = notices;
            if (state.notices.length > 0) {
                state.noticesId = Math.max(...state.notices.map((n) => n.id)) + 1;
            }
        }

    }, [])

    return { state, dispatch };
}

export default useNoticesReducer;