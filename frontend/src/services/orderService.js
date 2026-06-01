import api from "../api/axios";

export const getOrders = () =>
  api.get("/orders");

export const createOrder = (data) =>
  api.post("/orders", data);