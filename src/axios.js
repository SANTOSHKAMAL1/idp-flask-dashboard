const instance = axios.create({
  baseURL: "http://127.0.0.1:5000", // ✅ Local Flask server
});

export default instance;
