import api from "../api/axios";

export const getProducts = () => api.get("/products");

export const createProduct = (data) =>
  api.post("/products", data);

export const deleteProduct = (id) =>
  api.delete(`/products/${id}`);