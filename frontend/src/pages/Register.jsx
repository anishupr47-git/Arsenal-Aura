import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { premierLeagueTeams } from "../data/teams";

export default function Register() {
  const { register } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [favoriteClub, setFavoriteClub] = useState("Arsenal");

  const submit = async (e) => {
    e.preventDefault();
    try {
      await register(email, password, favoriteClub);
      addToast("Account created. Please log in.", "success");
      navigate("/login");
    } catch (e2) {
      if (e2.message.toLowerCase().includes("email already registered")) {
        addToast("Email already registered. Please log in.", "error");
        navigate("/login");
        return;
      }
      addToast(e2.message, "error");
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-md card p-6">
        <h1 className="text-3xl font-display text-arsenal-red tracking-wide">Create Account</h1>
        <p className="text-sm text-gray-600 mt-1">Join Arsenal Aura in seconds.</p>
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
          <div>
            <label className="text-sm font-semibold">Favorite Club</label>
            <select
              value={favoriteClub}
              onChange={(e) => setFavoriteClub(e.target.value)}
              className="w-full border rounded-lg px-3 py-2 mt-1"
            >
              {premierLeagueTeams.map((team) => (
                <option key={team} value={team}>
                  {team}
                </option>
              ))}
            </select>
          </div>
          <button className="w-full bg-arsenal-red text-white py-2 rounded-lg font-semibold">
            Create Account
          </button>
        </form>
        <p className="text-sm mt-4">
          Already have an account?{" "}
          <Link to="/login" className="text-arsenal-red font-semibold">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}
