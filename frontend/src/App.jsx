import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import ChatWidget from "./components/ChatWidget";
import Home from "./pages/Home";
import Predictor from "./pages/Predictor";
import Info from "./pages/Info";
import Login from "./pages/Login";
import Register from "./pages/Register";
import BanterGate from "./pages/BanterGate";

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  const location = useLocation();
  if (loading) {
    return <div className="min-h-screen grid place-items-center text-lg">Loading...</div>;
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (user.banter_mode && location.pathname !== "/banter") {
    return <Navigate to="/banter" replace />;
  }
  return children;
}

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-arsenal-gray app-shell">
      <Navbar />
      {children}
      <ChatWidget />
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout>
              <Home />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/predictor"
        element={
          <ProtectedRoute>
            <Layout>
              <Predictor />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/info"
        element={
          <ProtectedRoute>
            <Layout>
              <Info />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/banter"
        element={
          <ProtectedRoute>
            <Layout>
              <BanterGate />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/login"
        element={
          <Layout>
            <Login />
          </Layout>
        }
      />
      <Route
        path="/register"
        element={
          <Layout>
            <Register />
          </Layout>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
