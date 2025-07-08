const instance = axios.create({
  baseURL:
    process.env.NODE_ENV === "development"
      ? "http://127.0.0.1:5000" // ✅ Local Flask server
      : "https://idp-flask-dashboard.onrender.com/", //  actual deployed backend URL
});

export default instance;
