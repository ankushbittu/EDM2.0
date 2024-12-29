import React, { useState } from "react";
import RegisterForm from "../components/Auth/RegisterForm";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

const Register: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async (username: string, email: string, password: string) => {
    setIsLoading(true);
    setError("");

    try {
      // Example backend endpoint
      const response = await api.post("/auth/register", {
        username,
        email,
        password,
      });

      console.log("Registration success", response.data);

      // Optionally, auto-login the user or just navigate to login
      navigate("/login");
    } catch (err: any) {
      console.error("Registration error", err);
      setError("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Register</h1>
      <RegisterForm onRegister={handleRegister} isLoading={isLoading} error={error} />
      <p className="mt-4 text-sm">
        Already have an account?{" "}
        <span
          className="text-blue-600 cursor-pointer"
          onClick={() => navigate("/login")}
        >
          Login here
        </span>
      </p>
    </div>
  );
};

export default Register;
