import { useReducer, useEffect } from "react";
import { dummyResidents } from "../data/dummyResidents";

export const RESIDENT_ACTIONS = {
  CREATE: "CREATE_RESIDENT",
  UPDATE: "UPDATE_RESIDENT",
  DELETE: "DELETE_RESIDENT",
};

function reducer(state, action) {
  switch (action.type) {
    case RESIDENT_ACTIONS.CREATE:
      return [...state, action.data];
    case RESIDENT_ACTIONS.UPDATE:
      return state.map((it) =>
        it.unit === action.data.unit ? { ...it, ...action.data } : it
      );
    case RESIDENT_ACTIONS.DELETE:
      return state.filter((it) => it.unit !== action.unit);
    default:
      return state;
  }
}

export default function useResidentsReducer() {
  const saved = localStorage.getItem("RESIDENTS");
  const initial = saved ? JSON.parse(saved) : dummyResidents;
  const [residents, dispatch] = useReducer(reducer, initial);

  useEffect(() => {
    localStorage.setItem("RESIDENTS", JSON.stringify(residents));
  }, [residents]);

  return { residents, dispatch };
}
