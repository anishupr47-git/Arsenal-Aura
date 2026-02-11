import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function Info() {
  const { accessToken } = useAuth();
  const { addToast } = useToast();
  const [honors, setHonors] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [links, setLinks] = useState([]);
  const honorImages = ["/arse.1.jpg", "/arse.2.jpg", "/arse.3.jpg"];
  const timelineImages = ["/arse.4.jpg", "/arse.5.jpg", "/arse.6.jpg", "/arse.7.jpg", "/arse.8.jpg"];

  useEffect(() => {
    const load = async () => {
      try {
        const honorsData = await apiFetch("/api/info/honors", { method: "GET" }, accessToken);
        const timelineData = await apiFetch("/api/info/timeline", { method: "GET" }, accessToken);
        const linksData = await apiFetch("/api/info/links", { method: "GET" }, accessToken);
        setHonors(honorsData);
        setTimeline(timelineData);
        setLinks(linksData);
      } catch (e) {
        addToast(e.message, "error");
      }
    };
    load();
  }, [accessToken]);

  return (
    <div>
      <section className="hero-archive text-white">
        <div className="max-w-6xl mx-auto px-4 py-12 text-center relative">
          <h1 className="text-5xl md:text-6xl font-display tracking-wide">THE ARSENAL ARCHIVE</h1>
          <p className="mt-2 text-sm md:text-base">A Legacy of Greatness</p>
        </div>
      </section>
      <section className="max-w-6xl mx-auto px-4 -mt-10 pb-16 info-sheen">
        <div className="card p-6 md:p-8 gold-glow info-card">
          <h2 className="text-xl font-semibold">Our Honors</h2>
          <div className="mt-4 grid md:grid-cols-3 gap-4">
            {honors.map((h, index) => (
              <div
                key={h.id}
                className="rounded-xl p-4 text-center info-card image-fade-card"
                style={{ ["--bg-url"]: `url(${honorImages[index] || ""})` }}
              >
                <div className="text-3xl font-display text-arsenal-red">{h.count}</div>
                <div className="mt-2 font-semibold">{h.title}</div>
                <div className="text-xs text-gray-600">{h.subtitle}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="card p-6 md:p-8 mt-6 gold-glow info-card">
          <h2 className="text-xl font-semibold">Timeline</h2>
          <div className="mt-4 space-y-4">
            {timeline.map((t, index) => (
              <div
                key={t.id}
                className="rounded-xl p-4 info-card image-fade-card"
                style={{ ["--bg-url"]: `url(${timelineImages[index] || ""})` }}
              >
                <div className="font-semibold">{t.title}</div>
                <div className="text-xs text-gray-600">{t.period}</div>
                <div className="text-sm text-gray-700 mt-1">{t.description}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="card p-6 md:p-8 mt-6 gold-glow info-card">
          <h2 className="text-xl font-semibold">Latest News</h2>
          <div className="mt-4 space-y-3">
            {links.map((l) => (
              <div key={l.id} className="flex items-center justify-between border-b border-red-100 pb-3">
                <div className="text-sm font-semibold">{l.title}</div>
                <a
                  href={l.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-arsenal-red text-sm font-semibold"
                >
                  Read more
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
