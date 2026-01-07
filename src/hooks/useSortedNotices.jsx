import { useMemo } from "react";

export function useSortedNotices(notices) {
     return useMemo(
        () => {
            if (!notices || notices.length === 0) {
                return []; // 데이터 없을 때 안전 처리
            }
            // state 불변성을 유지하기 위해 아래와 같이 처리함 [...notices]
            const sortedNotices = [...notices].sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
            
            return sortedNotices;
}, [notices]);
}
