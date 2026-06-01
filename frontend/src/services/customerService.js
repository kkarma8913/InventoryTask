import api from "../api/axios";

export const getCustomers = () =>
  api.get("/customers");

export const createCustomer = (data) =>
  api.post("/customers", data);