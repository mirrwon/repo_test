import { createContext, useEffect } from "react";
import useNoticeActions from "./useNoticeActions";
import useNoticesReducer from "./useNoticesReducer";
import { STORAGE_KEY } from "../constant/notices";
import useResidentsActions from "./useResidentActions";
import useResidentsReducer from "./useResidentsReducer";

export const DataContext = createContext();
export const DataDispatchContext = createContext();
export const ResidentsContext = createContext([]);
export const ResidentsDispatchContext = createContext();

export function DataProvider({ children }) {
  const { state, dispatch } = useNoticesReducer();
  const noticesActions = useNoticeActions(dispatch);

  const { residents, dispatch: residentsDispatch } = useResidentsReducer();
  const residentsActions = useResidentsActions(residentsDispatch);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  return (
    <DataContext.Provider value={{ state }}>
      <DataDispatchContext.Provider value={noticesActions}>
        <ResidentsContext.Provider value={residents || []}>
          <ResidentsDispatchContext.Provider value={residentsActions}>
            {children}
          </ResidentsDispatchContext.Provider>
        </ResidentsContext.Provider>
      </DataDispatchContext.Provider>
    </DataContext.Provider>
  );
}
