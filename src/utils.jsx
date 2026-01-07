// 날짜(Date 객체)를 "YYYY-MM-DD HH:mm:ss" 형식의 문자열로 변환하는 함수
export function getFormattedDate(targetDate) {
    const year = targetDate.getFullYear();                       // 연도
    const month = String(targetDate.getMonth() + 1).padStart(2, "0"); // 월 (0부터 시작하므로 +1, 두 자리수 보정)
    const date = String(targetDate.getDate()).padStart(2, "0");       // 일 (두 자리수 보정)

    const hours = String(targetDate.getHours()).padStart(2, "0");     // 시 (두 자리수 보정)
    const minutes = String(targetDate.getMinutes()).padStart(2, "0"); // 분 (두 자리수 보정)
    const seconds = String(targetDate.getSeconds()).padStart(2, "0"); // 초 (두 자리수 보정)

    // "2025-09-11 10:05:32" 와 같은 형식으로 반환
    return `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
}
