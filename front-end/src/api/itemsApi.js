import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

API.interceptors.request.use((req) => {

  const token = localStorage.getItem("token");

  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }

  return req;
});

export const signupUser = (data) =>
  API.post("/signup", data);

export const loginUser = (data) =>
  API.post("/login", data);

export const getProfile = () =>
  API.get("/profile");

export const getItems = () => API.get("/items");

export const getItem = (id) => API.get(`/items/${id}`);

export const createItem = (data) =>
  API.post("/items", data);

export const updateItem = (id, data) =>
  API.put(`/items/${id}`, data);

export const deleteItem = (id) =>
  API.delete(`/items/${id}`);

export const workflowAction = (id, action) =>
  API.post(`/items/${id}/${action}`);

// SEARCH
export const searchItems = (query) =>
  API.get(`/items/search?q=${query}`);

// PAGINATION
export const paginateItems = (limit, offset) =>
  API.get(`/items/paginate?limit=${limit}&offset=${offset}`);

// SEARCH + PAGINATION
export const searchPaginatedItems = (
  query,
  limit,
  offset
) =>
  API.get(
    `/items/search/paginated?q=${query}&limit=${limit}&offset=${offset}`
  );


export const logoutUser = async (token) => {

  return API.post(
    "/logout",
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );
};