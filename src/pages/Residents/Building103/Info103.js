import "./Info103.css";
import { useParams, useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { ResidentsContext, ResidentsDispatchContext } from "../../../context/DataContext";
import Button from "../../../components/Button";

export default function Info103() {
  const { unit } = useParams();
  const residents = useContext(ResidentsContext) || [];
  const { createResident, updateResident, deleteResident } =
    useContext(ResidentsDispatchContext);
  const navigate = useNavigate();

  const existing = residents.find((r) => r.unit === unit);
  const [form, setForm] = useState(
    existing || {
      id: Date.now(),
      building: "103",
      unit,
      head: "",
      phone: "",
      members: "",
      moveInDate: "",
      moveOutDate: "",
    }
  );

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSave = () => {

    if (!form.head || !form.phone || !form.members || !form.moveInDate) {
      alert("정보를 입력하세요.");
      return;
    }

    if (existing) {
      updateResident(form);
      alert("수정되었습니다.");
    } else {
      createResident(form);
      alert("입주를 환영합니다.");
    }
    navigate("/residents/Page103");
  };

  const handleDelete = () => {
    if (window.confirm("정말 삭제하시겠습니까?")) {
      deleteResident(unit);
      alert("삭제되었습니다.");
      navigate("/residents/Page103");
    }
  };

  return (
    <div className="info103-container">
      <h2>{unit} 상세 정보</h2>

      <input name="head" value={form.head} onChange={handleChange} placeholder="세대주" />
      <input name="phone" value={form.phone} onChange={handleChange} placeholder="연락처" />
      <input name="members" type="number" value={form.members} onChange={handleChange} placeholder="세대원 수" />
      <input name="moveInDate" type="date" value={form.moveInDate} onChange={handleChange} />
      <input name="moveOutDate" type="date" value={form.moveOutDate} onChange={handleChange} />

      <div className="button-group">
        <Button onClick={handleSave}>저장</Button>
        {existing && <Button color="red" onClick={handleDelete}>삭제</Button>}
      </div>
    </div>
  );
}
