import { useCallback, useMemo } from "react";
import { RESIDENT_ACTIONS } from "./useResidentsReducer";

export default function useResidentsActions(dispatch) {
  const createResident = useCallback(
    (data) => dispatch({ type: RESIDENT_ACTIONS.CREATE, data }),
    [dispatch]
  );

  const updateResident = useCallback(
    (data) => dispatch({ type: RESIDENT_ACTIONS.UPDATE, data }),
    [dispatch]
  );

  const deleteResident = useCallback(
    (unit) => dispatch({ type: RESIDENT_ACTIONS.DELETE, unit }),
    [dispatch]
  );

  return useMemo(() => ({ createResident, updateResident, deleteResident }), [
    createResident,
    updateResident,
    deleteResident,
  ]);
}
