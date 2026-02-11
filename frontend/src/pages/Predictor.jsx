import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function Predictor() {
  const { accessToken } = useAuth();
  const { addToast } = useToast();
  const [match, setMatch] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [homeScore, setHomeScore] = useState(2);
  const [awayScore, setAwayScore] = useState(1);
  const [result, setResult] = useState(null);
  const [matchError, setMatchError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const next = await apiFetch("/api/fixtures/next", { method: "GET" }, accessToken);
        if (next?.unavailable) {
          setMatch(null);
          setMatchError(next.detail || "Match data unavailable.");
        } else {
          setMatch(next);
          setMatchError("");
        }
        const latest = await apiFetch("/api/predictions/latest", { method: "GET" }, accessToken);
        if (latest?.id) {
          setPrediction(latest);
          setHomeScore(latest.predicted_home);
          setAwayScore(latest.predicted_away);
        }
      } catch (e) {
        setMatchError(e.message || "Unable to load match data.");
        addToast(e.message, "error");
      }
    };
    load();
  }, [accessToken]);

  const savePrediction = async () => {
    if (!match) return;
    try {
      const payload = {
        match_id: match.match_id,
        opponent: match.opponent,
        arsenal_is_home: match.arsenal_is_home,
        kickoff: match.utcDate,
        predicted_home: Number(homeScore),
        predicted_away: Number(awayScore)
      };
      const data = await apiFetch("/api/predictions", { method: "POST", body: JSON.stringify(payload) }, accessToken);
      setPrediction(data);
      addToast("Prediction saved.", "success");
    } catch (e) {
      addToast(e.message, "error");
    }
  };

  const checkResult = async () => {
    if (!prediction) return;
    try {
      const data = await apiFetch(`/api/predictions/${prediction.id}/check`, { method: "POST", body: "{}" }, accessToken);
      setResult(data);
    } catch (e) {
      addToast(e.message, "error");
    }
  };

  return (
    <div>
      <section className="hero-bg text-white">
        <div className="max-w-6xl mx-auto px-4 py-12 text-center">
          <h1 className="text-5xl md:text-6xl font-display tracking-wide">MATCH PREDICTOR</h1>
          <p className="mt-2 text-sm md:text-base">Predict the next match</p>
        </div>
      </section>
      <section className="max-w-4xl mx-auto px-4 -mt-10 pb-16">
        <div className="card p-6 md:p-8">
          {match ? (
            <>
              <div className="text-center">
                <div className="text-lg font-semibold">{match.competition}</div>
                <div className="text-sm text-gray-600">
                  {new Date(match.utcDate).toLocaleString()}
                </div>
              </div>
              <div className="mt-6 grid grid-cols-3 items-center text-center gap-3">
                <div className="font-semibold flex flex-col items-center gap-2">
                  {((match.arsenal_is_home && match.homeBadge) || (!match.arsenal_is_home && match.awayBadge)) && (
                    <img
                      src={match.arsenal_is_home ? match.homeBadge : match.awayBadge}
                      alt="Arsenal badge"
                      className="w-12 h-12 object-contain"
                    />
                  )}
                  Arsenal
                </div>
                <div className="text-2xl font-bold text-arsenal-red">vs</div>
                <div className="font-semibold flex flex-col items-center gap-2">
                  {((match.arsenal_is_home && match.awayBadge) || (!match.arsenal_is_home && match.homeBadge)) && (
                    <img
                      src={match.arsenal_is_home ? match.awayBadge : match.homeBadge}
                      alt="Opponent badge"
                      className="w-12 h-12 object-contain"
                    />
                  )}
                  {match.opponent}
                </div>
              </div>
              <div className="text-xs text-gray-600 text-center mt-2">
                {match.arsenal_is_home ? "Arsenal at home" : "Arsenal away"}
                {match.stale && " • Showing last cached match"}
              </div>
              <div className="mt-6 flex items-center justify-center gap-4">
                <input
                  type="number"
                  min="0"
                  value={homeScore}
                  onChange={(e) => setHomeScore(e.target.value)}
                  className="w-16 text-center border rounded-lg py-2"
                />
                <div className="text-xl font-bold">-</div>
                <input
                  type="number"
                  min="0"
                  value={awayScore}
                  onChange={(e) => setAwayScore(e.target.value)}
                  className="w-16 text-center border rounded-lg py-2"
                />
              </div>
              <button
                onClick={savePrediction}
                className="mt-6 w-full bg-arsenal-red text-white py-2 rounded-lg font-semibold"
              >
                Save Prediction
              </button>
            </>
          ) : matchError ? (
            <div className="text-center text-red-600 text-sm">{matchError}</div>
          ) : (
            <div className="text-center text-gray-600">Loading next match...</div>
          )}
        </div>

        <div className="mt-6 card p-6">
          <div className="flex items-center justify-between">
            <div className="font-semibold">Check Result</div>
            <button
              onClick={checkResult}
              className="bg-arsenal-red text-white px-4 py-2 rounded-lg text-sm font-semibold"
            >
              Check
            </button>
          </div>
          {result && (
            <div
              className={`mt-4 rounded-xl p-4 text-sm ${
                result.result_color === "green"
                  ? "bg-green-100 text-green-800"
                  : result.result_color === "yellow"
                  ? "bg-yellow-100 text-yellow-800"
                  : "bg-red-100 text-red-800"
              }`}
            >
              <div className="font-semibold">Points: {result.points}</div>
              <div className="mt-1">{result.message}</div>
            </div>
          )}
          {!result && <div className="text-xs text-gray-600 mt-4">Check back after the match.</div>}
        </div>
      </section>
    </div>
  );
}
