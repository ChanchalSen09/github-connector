export function StatCard({ label, value, change }) {
  return (
    <div className="rounded-[26px] border border-white/70 bg-white/80 p-5 shadow-panel backdrop-blur">
      <p className="text-sm font-medium text-slate-500">{label}</p>
      <div className="mt-4 flex items-end justify-between gap-4">
        <p className="text-4xl font-semibold text-ink">{value}</p>
        <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-medium text-primary">{change}</span>
      </div>
    </div>
  );
}
