import React, { useState, FormEvent } from "react";

interface RegisterFormProps {
  onRegister: (username: string, email: string, password: string) => void;
  isLoading?: boolean;
  error?: string;
}

const RegisterForm: React.FC<RegisterFormProps> = ({
  onRegister,
  isLoading,
  error,
}) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (password !== confirm) {
      alert("Passwords do not match!");
      return;
    }

    onRegister(username, email, password);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-sm mx-auto">
      <div>
        <label className="block mb-1 text-sm font-medium" htmlFor="username">
          Username:
        </label>
        <input
          id="username"
          type="text"
          className="w-full border border-gray-300 rounded px-3 py-2"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          placeholder="Your username"
        />
      </div>

      <div>
        <label className="block mb-1 text-sm font-medium" htmlFor="email">
          Email:
        </label>
        <input
          id="email"
          type="email"
          className="w-full border border-gray-300 rounded px-3 py-2"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          placeholder="you@example.com"
        />
      </div>

      <div>
        <label className="block mb-1 text-sm font-medium" htmlFor="password">
          Password:
        </label>
        <input
          id="password"
          type="password"
          className="w-full border border-gray-300 rounded px-3 py-2"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          placeholder="Enter a secure password"
        />
      </div>

      <div>
        <label className="block mb-1 text-sm font-medium" htmlFor="confirm">
          Confirm Password:
        </label>
        <input
          id="confirm"
          type="password"
          className="w-full border border-gray-300 rounded px-3 py-2"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          required
          placeholder="Re-type your password"
        />
      </div>

      {error && (
        <p className="text-red-500 text-sm">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
      >
        {isLoading ? "Registering..." : "Register"}
      </button>
    </form>
  );
};

export default RegisterForm;
