// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Residents from "./pages/Residents"; // index.jsx에서 하위 라우팅 처리
import ParkingList from "./pages/Parking/ParkingList";
import ParkingForm from "./pages/Parking/ParkingForm";
import { DataProvider } from "./context/DataContext";
import Header from "./components/Header";
import Notices from "./pages/Notices";
import Footer from "./components/Footer";
import Page103 from "./pages/Residents/Building103/Page103";
import Info103 from "./pages/Residents/Building103/Info103";



export default function App() {
  return (
    <DataProvider>
      <Router>
        <Header />
        <Routes>
          {/* 기본 경로 → Home으로 리다이렉트 */}
          <Route path="/" element={<Navigate to="/home" />} />

          {/* 홈 */}
          <Route path="/home" element={<Home />} />

          {/* 공지 관리 */}
          <Route path="/notices" element={<Notices />} />

          {/* 주민 관리 (동별 페이지는 Residents/index.jsx에서 처리) */}
          <Route path="/residents/Page103" element={<Page103 />} />
          <Route path="/residents/Info103/:unit" element={<Info103 />} />
          

          {/* 주차 관리 */}
          <Route path="/parking" element={<ParkingList />} />
          <Route path="/parking/new" element={<ParkingForm />} />
        </Routes>
        <Footer />
      </Router>
    </DataProvider>
  );
}
