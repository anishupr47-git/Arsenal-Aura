import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  return (
    <nav className="bg-white border-b border-gray-100">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-arsenal-red grid place-items-center text-white font-bold">
            A
          </div>
          <div className="text-xl font-display tracking-wide text-arsenal-red">ARSENAL AURA</div>
        </div>
        <div className="flex items-center gap-6 text-sm font-semibold">
          <NavLink to="/" className="hover:text-arsenal-red">
            Home
          </NavLink>
          <NavLink to="/predictor" className="hover:text-arsenal-red">
            Predictor
          </NavLink>
          <NavLink to="/info" className="hover:text-arsenal-red">
            Info
          </NavLink>
          {!user ? (
            <NavLink to="/login" className="hover:text-arsenal-red">
              Login
            </NavLink>
          ) : (
            <button onClick={logout} className="hover:text-arsenal-red">
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
