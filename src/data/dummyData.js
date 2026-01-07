// 주민 데이터
export const residents = [
    {
        id: 1,
        building: "101",
        unit: "101",
        head: "홍길동",
        phone: "010-1234-5678",
        members: 3,
        moveInDate: "2024-01-01",
        moveOutDate: null,
    },
    {
        id: 2,
        building: "101",
        unit: "302",
        head: "김철수",
        phone: "010-9876-5432",
        members: 4,
        moveInDate: "2024-03-15",
        moveOutDate: null,
    },
    {
        id: 3,
        building: "102",
        unit: "501",
        head: "이영희",
        phone: "010-5555-3333",
        members: 2,
        moveInDate: "2023-11-20",
        moveOutDate: null,
    },
];

// 차량 데이터
export const parkings = [
    {
        id: 1,
        carNumber: "12가3456",
        ownerId: 1,
        parkingSpot: "P1",
    },
    {
        id: 2,
        carNumber: "34나5678",
        ownerId: 2,
        parkingSpot: "P2",
    },
    {
        id: 3,
        carNumber: "56다7890",
        ownerId: 3,
        parkingSpot: "P5",
    },
];

// 공지사항 데이터
export const notices = [
    {
        id: 1,
        text: "9월 15일 오전 10시에 소방 안전 점검이 있습니다.",
        createdAt: "2025-09-01 09:00:11",
    },
    {
        id: 2,
        text: "주차장 보수 공사가 9월 20일에 진행됩니다.",
        createdAt: "2025-09-05 14:30:22",
    },
    {
        id: 3,
        text: "엘리베이터 정기 점검: 9월 10일 오전 9시 ~ 12시",
        createdAt: "2025-09-07 18:00:33",
    },
];
