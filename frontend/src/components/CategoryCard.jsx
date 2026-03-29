export function CategoryCard({ title, description, count, accent }) {
  return (
    <div className="rounded-[28px] border border-white/70 bg-white/90 p-5 shadow-panel">
      <div className={`h-2 w-24 rounded-full bg-gradient-to-r ${accent}`} />
      <h3 className="mt-5 text-xl font-semibold text-ink">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-slate-500">{description}</p>
      <div className="mt-6 inline-flex rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
        {count}
      </div>
    </div>
  );
}
