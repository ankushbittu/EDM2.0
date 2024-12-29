import React, { useState } from "react";
import LoginForm from "../components/Auth/LoginForm";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (email: string, password: string) => {
    setIsLoading(true);
    setError("");

    try {
      // Example API call (adjust endpoint and response structure as needed)
      const response = await api.post("/auth/login", { email, password });
      
      // If successful, you might store the token in AuthContext or localStorage
      const { token, userInfo } = response.data;
      
      // For now, just log success
      console.log("Login success", token, userInfo);

      // Navigate to dashboard or wherever you want
      navigate("/dashboard");
    } catch (err: any) {
      console.error("Login error", err);
      setError("Invalid email or password");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <LoginForm onLogin={handleLogin} isLoading={isLoading} error={error} />
      <p className="mt-4 text-sm">
        Don&apos;t have an account?{" "}
        <span
          className="text-blue-600 cursor-pointer"
          onClick={() => navigate("/register")}
        >
          Register here
        </span>
      </p>
    </div>
  );
};

export default Login;
