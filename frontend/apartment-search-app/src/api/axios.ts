import axios from "axios";

const Base_URL = "http://localhost:8000/api";

const axiosInstance = axios.create({
    baseURL: Base_URL
});

export const axiosPrivate = axios.create({
    baseURL: Base_URL,
    headers: {"Content-Type": "application/json"},
    withCredentials: true
});

export default axiosInstance;
