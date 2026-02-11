import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function Home() {
  const { accessToken } = useAuth();
  const { addToast } = useToast();
  const [modes, setModes] = useState([]);
  const [players, setPlayers] = useState([]);
  const [mode, setMode] = useState("praise");
  const [player, setPlayer] = useState("");
  const [intensity, setIntensity] = useState("medium");
  const [output, setOutput] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const modesData = await apiFetch("/api/modes", { method: "GET" }, accessToken);
        setModes(modesData);
        const playersData = await apiFetch("/api/players", { method: "GET" }, accessToken);
        setPlayers(playersData);
      } catch (e) {
        addToast(e.message, "error");
      }
    };
    load();
  }, [accessToken]);

  const generate = async () => {
    try {
      const params = new URLSearchParams({
        mode,
        intensity,
        player: player || ""
      });
      const data = await apiFetch(`/api/generate?${params.toString()}`, { method: "GET" }, accessToken);
      setOutput(data.text);
    } catch (e) {
      addToast(e.message, "error");
    }
  };

  const copy = async () => {
    if (!output) return;
    await navigator.clipboard.writeText(output);
    addToast("Copied to clipboard.", "success");
  };

  return (
    <div>
      <section className="hero-arsenal text-white">
        <div className="max-w-6xl mx-auto px-4 py-12 text-center relative">
          <div className="absolute right-6 top-6 opacity-90">
            <svg width="70" height="44" viewBox="0 0 140 88" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="30" cy="58" r="16" fill="white" fillOpacity="0.15" stroke="white" strokeWidth="4" />
              <rect x="44" y="40" width="70" height="16" rx="8" fill="white" fillOpacity="0.2" />
              <rect x="96" y="30" width="28" height="10" rx="5" fill="white" fillOpacity="0.2" />
              <rect x="58" y="56" width="40" height="10" rx="5" fill="white" fillOpacity="0.2" />
            </svg>
          </div>
          <h1 className="text-5xl md:text-6xl font-display tracking-wide">ARSENAL AURA</h1>
          <p className="mt-2 text-sm md:text-base">Pure North London Energy</p>
        </div>
      </section>
      <div className="glyph-strip"></div>

      <section className="max-w-5xl mx-auto px-4 -mt-10 pb-16 glyph-rain">
        <div className="card p-6 md:p-8">
          <div className="grid md:grid-cols-2 gap-6 items-end">
            <div className="space-y-4">
              <div>
                <label className="text-sm font-semibold">Mode</label>
                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  className="w-full border rounded-lg px-3 py-2 mt-1"
                >
                  {modes.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-semibold">Select Player</label>
                <select
                  value={player}
                  onChange={(e) => setPlayer(e.target.value)}
                  className="w-full border rounded-lg px-3 py-2 mt-1"
                >
                  <option value="">Any Arsenal Player</option>
                  {players.map((p) => (
                    <option key={p.id} value={p.name}>
                      {p.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-semibold">Intensity</label>
                <div className="flex gap-2 mt-2">
                  {["low", "medium", "high"].map((lvl) => (
                    <button
                      key={lvl}
                      onClick={() => setIntensity(lvl)}
                      className={`px-3 py-2 rounded-lg border text-sm font-semibold ${
                        intensity === lvl ? "bg-arsenal-red text-white border-arsenal-red" : "bg-white"
                      }`}
                    >
                      {lvl.charAt(0).toUpperCase() + lvl.slice(1)}
                    </button>
                  ))}
                </div>
              </div>
              <button onClick={generate} className="w-full bg-arsenal-red text-white py-2 rounded-lg font-semibold">
                Generate
              </button>
            </div>
            <div>
              <div className="border-l-4 border-arsenal-red bg-arsenal-light rounded-xl p-4">
                <div className="text-3xl text-arsenal-red leading-none">“</div>
                <p className="text-gray-800 text-lg mt-2">{output || "Generate a line to light up the Emirates."}</p>
                <div className="text-3xl text-arsenal-red text-right leading-none">”</div>
              </div>
              <button
                onClick={copy}
                className="mt-3 w-full bg-white border border-arsenal-red text-arsenal-red py-2 rounded-lg font-semibold"
              >
                Copy
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
