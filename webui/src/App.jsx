import React, { useEffect, useState } from "react";
import { Activity, Gauge, Network, Upload, Wrench } from "lucide-react";
import { createRoot } from "react-dom/client";
import "./main.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Metric({ icon: Icon, label, value }) {
  return (
    <div className="rounded-md border border-zinc-800 bg-zinc-950 p-4">
      <div className="flex items-center gap-3 text-zinc-400">
        <Icon size={18} />
        <span className="text-sm">{label}</span>
      </div>
      <div className="mt-3 text-2xl font-semibold">{value}</div>
    </div>
  );
}

function App() {
  const [summary, setSummary] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [result, setResult] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [imageSize, setImageSize] = useState(null);
  const [busy, setBusy] = useState(false);

  async function refreshSummary() {
    const response = await fetch(`${API_URL}/telemetry/summary`);
    setSummary(await response.json());
  }

  async function refreshRoadmap() {
    const response = await fetch(`${API_URL}/roadmap`);
    setRoadmap(await response.json());
  }

  async function uploadImage(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(URL.createObjectURL(file));
    setImageSize(null);
    setBusy(true);
    const data = new FormData();
    data.append("image", file);
    const response = await fetch(`${API_URL}/detect`, { method: "POST", body: data });
    setResult(await response.json());
    await refreshSummary();
    setBusy(false);
  }

  useEffect(() => {
    refreshSummary().catch(() => setSummary({ total_events: 0, detected_events: 0, average_confidence: 0, top_families: [] }));
    refreshRoadmap().catch(() => setRoadmap(null));
  }, []);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const bboxStyle =
    result?.bbox && imageSize
      ? {
          left: `${(result.bbox.x / imageSize.width) * 100}%`,
          top: `${(result.bbox.y / imageSize.height) * 100}%`,
          width: `${(result.bbox.width / imageSize.width) * 100}%`,
          height: `${(result.bbox.height / imageSize.height) * 100}%`,
        }
      : null;

  return (
    <main className="min-h-screen">
      <section className="border-b border-zinc-800 bg-zinc-950">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-md bg-amber-400 text-zinc-950">
              <Wrench size={22} />
            </div>
            <div>
              <h1 className="text-xl font-semibold">BlackMamba ScrewVision</h1>
              <p className="text-sm text-zinc-400">Mechanical intelligence runtime</p>
            </div>
          </div>
          <label className="inline-flex cursor-pointer items-center gap-2 rounded-md bg-amber-400 px-4 py-2 text-sm font-semibold text-zinc-950">
            <Upload size={17} />
            {busy ? "Analyzing" : "Upload"}
            <input className="hidden" type="file" accept="image/*" onChange={uploadImage} />
          </label>
        </div>
      </section>

      <section className="mx-auto grid max-w-6xl gap-5 px-5 py-6 md:grid-cols-3">
        <Metric icon={Activity} label="Events" value={summary?.total_events ?? 0} />
        <Metric icon={Wrench} label="Detections" value={summary?.detected_events ?? 0} />
        <Metric icon={Gauge} label="Avg confidence" value={summary?.average_confidence ?? 0} />
      </section>

      <section className="mx-auto grid max-w-6xl gap-5 px-5 pb-8 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-md border border-zinc-800 bg-zinc-950 p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <h2 className="text-lg font-semibold">Latest Analysis</h2>
            {result && (
              <div className="inline-flex w-fit items-center gap-2 rounded-md border border-zinc-800 px-3 py-2 text-sm text-zinc-300">
                <Activity size={16} />
                {result.detector} {result.model ? `/ ${result.model}` : ""}
              </div>
            )}
          </div>
          {result ? (
            <div className="mt-4 space-y-4">
              {previewUrl && (
                <div className="relative overflow-hidden rounded-md border border-zinc-800 bg-zinc-900">
                  <img
                    className="block max-h-[420px] w-full object-contain"
                    src={previewUrl}
                    alt="Uploaded screw"
                    onLoad={(event) =>
                      setImageSize({
                        width: event.currentTarget.naturalWidth,
                        height: event.currentTarget.naturalHeight,
                      })
                    }
                  />
                  {bboxStyle && (
                    <div className="absolute border-2 border-amber-300 bg-amber-300/10" style={bboxStyle}>
                      <span className="absolute left-0 top-0 bg-amber-300 px-2 py-1 text-xs font-semibold text-zinc-950">
                        {Math.round(result.confidence * 100)}%
                      </span>
                    </div>
                  )}
                </div>
              )}

              <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                <Metric icon={Wrench} label="Type" value={result.screw_type} />
                <Metric icon={Gauge} label="Confidence" value={result.confidence} />
                <Metric icon={Activity} label="Wear" value={result.wear} />
                <Metric icon={Network} label="Material" value={result.material} />
              </div>

              <pre className="max-h-[360px] overflow-auto rounded-md bg-zinc-900 p-4 text-sm text-zinc-100">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          ) : (
            <div className="mt-4 rounded-md border border-dashed border-zinc-700 p-10 text-center text-zinc-400">
              Upload a screw image to inspect morphology, geometry, and wear signals.
            </div>
          )}
        </div>

        <div className="rounded-md border border-zinc-800 bg-zinc-950 p-5">
          <h2 className="text-lg font-semibold">Inventory Signals</h2>
          <div className="mt-4 space-y-3">
            {(summary?.top_families || []).map((item) => (
              <div key={item.family} className="flex items-center justify-between border-b border-zinc-800 pb-2 text-sm">
                <span className="text-zinc-300">{item.family}</span>
                <span className="font-semibold">{item.count}</span>
              </div>
            ))}
            {!summary?.top_families?.length && <p className="text-sm text-zinc-400">No inventory telemetry yet.</p>}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-5 pb-10">
        <div className="rounded-md border border-zinc-800 bg-zinc-950 p-5">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-semibold">Mechanical Intelligence Roadmap</h2>
              <p className="text-sm text-zinc-400">{roadmap?.vision || "Physics -> Vision -> Semantics -> Autonomy"}</p>
            </div>
            <div className="inline-flex w-fit items-center gap-2 rounded-md border border-zinc-800 px-3 py-2 text-sm text-zinc-300">
              <Network size={16} />
              {roadmap?.phases?.length ?? 0} phases
            </div>
          </div>

          <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            {(roadmap?.phases || []).map((phase) => (
              <div key={phase.phase} className="rounded-md border border-zinc-800 bg-zinc-900 p-4">
                <div className="flex items-center justify-between gap-3">
                  <span className="text-xs font-semibold uppercase text-amber-300">Phase {phase.phase}</span>
                  <span className="text-xs text-zinc-500">{phase.architecture}</span>
                </div>
                <h3 className="mt-3 text-base font-semibold">{phase.name}</h3>
                <p className="mt-2 min-h-12 text-sm text-zinc-400">{phase.goal}</p>
                <div className="mt-4 space-y-2">
                  {phase.deliverables.slice(0, 3).map((item) => (
                    <div key={item.component} className="flex items-center justify-between gap-3 text-xs">
                      <span className="text-zinc-300">{item.component}</span>
                      <span className={item.status === "in_progress" ? "text-amber-300" : "text-zinc-500"}>
                        {item.status.replace("_", " ")}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
            {!roadmap?.phases?.length && <p className="text-sm text-zinc-400">Roadmap API unavailable.</p>}
          </div>
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
