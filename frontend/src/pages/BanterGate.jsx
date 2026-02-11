import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function BanterGate() {
  const { user, updateFavoriteClub } = useAuth();
  const { addToast } = useToast();

  const switchClub = async () => {
    try {
      await updateFavoriteClub("Arsenal");
      addToast("Welcome home. Arsenal access unlocked.", "success");
    } catch (e) {
      addToast(e.message, "error");
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-2xl card p-8 text-center">
        <h1 className="text-4xl font-display text-arsenal-red tracking-wide">Banter Gate</h1>
        <p className="text-gray-600 mt-2">
          {user?.favorite_club === "Tottenham Hotspur"
            ? "Spurs detected. The aura is not compatible."
            : "Chelsea detected. The aura needs a reset."}
        </p>
        <div className="mt-6 space-y-2 text-sm text-gray-700">
          <p>Switch your club to Arsenal to unlock full access.</p>
          <p>No hate, just North London standards.</p>
          <p>Press the red button and let the cannon roar.</p>
        </div>
        <button
          onClick={switchClub}
          className="mt-6 bg-arsenal-red text-white px-6 py-3 rounded-lg font-semibold"
        >
          Switch to Arsenal
        </button>
      </div>
    </div>
  );
}
