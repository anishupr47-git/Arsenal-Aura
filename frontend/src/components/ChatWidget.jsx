import { useState } from "react";
import { apiFetch } from "../api";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function ChatWidget() {
  const { accessToken, user } = useAuth();
  const { addToast } = useToast();
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const send = async () => {
    if (!user) {
      addToast("Login to chat.", "error");
      return;
    }
    if (!input.trim()) return;
    const text = input.trim();
    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    try {
      const data = await apiFetch(
        "/api/chat",
        { method: "POST", body: JSON.stringify({ message: text }) },
        accessToken
      );
      setMessages((prev) => [...prev, { role: "bot", text: data.reply }]);
    } catch (e) {
      addToast(e.message, "error");
    }
  };

  return (
    <div className="fixed bottom-5 right-5 z-40">
      {open && (
        <div className="w-72 sm:w-80 bg-white rounded-2xl shadow-soft border border-gray-100 mb-3 overflow-hidden">
          <div className="bg-arsenal-red text-white px-4 py-3 font-semibold">Arsenal Aura Bot</div>
          <div className="p-3 space-y-2 max-h-56 overflow-y-auto bg-arsenal-light">
            {messages.length === 0 && (
              <div className="text-xs text-gray-600">Ask about Invincibles, Wenger, Saka, or the Emirates.</div>
            )}
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`text-sm px-3 py-2 rounded-xl ${
                  msg.role === "user" ? "bg-white border" : "bg-red-50 border border-red-100"
                }`}
              >
                {msg.text}
              </div>
            ))}
          </div>
          <div className="p-3 flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 border rounded-lg px-3 py-2 text-sm"
              placeholder="Type a message..."
            />
            <button
              onClick={send}
              className="bg-arsenal-red text-white px-3 py-2 rounded-lg text-sm font-semibold"
            >
              Send
            </button>
          </div>
        </div>
      )}
      <button
        onClick={() => setOpen((s) => !s)}
        className="w-12 h-12 rounded-full bg-arsenal-red text-white shadow-soft grid place-items-center"
      >
        <div className="w-7 h-7 rounded-lg bg-white/20 grid place-items-center">
          <div className="flex gap-1">
            <span className="w-1.5 h-1.5 bg-white rounded-full"></span>
            <span className="w-1.5 h-1.5 bg-white rounded-full"></span>
          </div>
        </div>
      </button>
    </div>
  );
}
