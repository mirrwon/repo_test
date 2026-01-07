import "./Page103.css";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { ResidentsContext } from "../../../context/DataContext";

export default function Page103() {
  const residents = useContext(ResidentsContext) || [];
  const navigate = useNavigate();

  const floors = [7,6,5, 4, 3, 2, 1];
  const rooms = ["01", "02", "03"];

  return (
    <div className="page103-container">
      {floors.map((floor) => (
        <div key={floor} className="floor-row">
          {rooms.map((room) => {
            const unit = `103-${floor}${room}`;
            const resident = residents.find((r) => r.unit === unit);
            const isEmpty = !resident;

            return (
              <button
                key={unit}
                className={`unit-button ${isEmpty ? "unit-empty" : "unit-occupied"}`}
                onClick={() => navigate(`/residents/Info103/${unit}`)}
              >
                {unit}
              </button>
            );
          })}
        </div>
      ))}
    </div>
  );
}
