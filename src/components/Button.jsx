export default function Button({ children, onClick, color = "blue" }) {
  const colorClass =
    color === "red"
      ? "bg-red-500"
      : color === "green"
      ? "bg-green-500"
      : "bg-blue-500";

  return (
    <button
      onClick={onClick}
      className={`${colorClass} text-white px-4 py-2 rounded-xl hover:opacity-80`}
    >
      {children}
    </button>
  );
}
