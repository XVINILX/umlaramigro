import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/authSlice";
import petsReducer from "./slices/petSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    pets: petsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
