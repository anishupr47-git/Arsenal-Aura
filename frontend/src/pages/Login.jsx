import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function Login() {
  const { login } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      addToast("Welcome back, Gooner.", "success");
      navigate("/");
    } catch (e2) {
      addToast(e2.message, "error");
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-md card p-6">
        <h1 className="text-3xl font-display text-arsenal-red tracking-wide">Login</h1>
        <p className="text-sm text-gray-600 mt-1">Enter your Arsenal Aura account.</p>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="w-full border rounded-lg px-3 py-2"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full border rounded-lg px-3 py-2"
            required
          />
          <button className="w-full bg-arsenal-red text-white py-2 rounded-lg font-semibold">
            Login
          </button>
        </form>
        <p className="text-sm mt-4">
          New here?{" "}
          <Link to="/register" className="text-arsenal-red font-semibold">
            Create account
          </Link>
        </p>
      </div>
    </div>
  );
}
