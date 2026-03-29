import { FiChevronDown, FiChevronsLeft, FiChevronsRight, FiFileText, FiMoreVertical } from "react-icons/fi";

function KebabIcon() {
  return <FiMoreVertical className="h-4 w-4 text-[#8c8c97]" />;
}

function EmptyState({ message }) {
  return (
    <div className="flex h-full min-h-[320px] items-center justify-center">
      <div className="flex flex-col items-center text-center text-[#8e8e98]">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-[22px] border-[3px] border-[#a3a3ad]">
          <FiFileText className="h-8 w-8" />
        </div>
        <p className="text-[14px]">{message}</p>
      </div>
    </div>
  );
}

function Footer({ totalRows }) {
  return (
    <div className="flex items-center justify-between px-6 py-4 text-[12px] text-[#555563]">
      <span>{totalRows} rows</span>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span>Rows per page</span>
          <div className="flex h-9 w-14 items-center justify-center rounded-lg border border-[#e7e7ee] bg-white text-[#8d8d97]">
            10 <FiChevronDown className="ml-1 text-[10px]" />
          </div>
        </div>
        <span>page 1 of 1</span>
        <div className="flex items-center gap-1 text-[#b2b2bc]">
          <button type="button" className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#ececf3]"><FiChevronsLeft /></button>
          <button type="button" className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#ececf3]">‹</button>
          <button type="button" className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#ececf3]">›</button>
          <button type="button" className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#ececf3]"><FiChevronsRight /></button>
        </div>
      </div>
    </div>
  );
}

export function ArticleList({ items, loading, error }) {
  const renderContent = () => {
    if (loading) {
      return <EmptyState message="Loading knowledge bases..." />;
    }

    if (error) {
      return <EmptyState message={error} />;
    }

    if (!items.length) {
      return <EmptyState message="No Knowledge Bases Found" />;
    }

    return (
      <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3">
        {items.map((card) => (
          <div key={card.id} className="rounded-xl border border-[#e8ebf2] bg-white p-4 shadow-[0_1px_2px_rgba(15,23,42,0.03)]">
            <div className="mb-2 flex items-start justify-between gap-3">
              <div>
                <h2 className="text-[14px] font-medium text-[#2f2f37]">{card.name}</h2>
                <div className="mt-1.5 flex flex-wrap gap-1.5">
                  <span className="rounded bg-[#f3f2ff] px-1.5 py-0.5 text-[10px] text-[#5b4ef7]">{card.vector_store}</span>
                  <span className="rounded bg-[#f5f5f8] px-1.5 py-0.5 text-[10px] text-[#777785]">{card.embedding_model}</span>
                </div>
              </div>
              <button type="button" className="-mr-1 -mt-1">
                <KebabIcon />
              </button>
            </div>
            <p className="min-h-[92px] text-[11px] leading-5 text-[#8a8a96]">{card.description}</p>
            <div className="mt-5 border-t border-[#efeff5] pt-3 text-[11px] text-[#7f7f8b]">
              Created On: {card.created_on}
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="flex min-h-0 flex-1 flex-col justify-between overflow-hidden">
      <div className="min-h-0 flex-1 px-6 py-5">
        <div className="flex h-full min-h-0 flex-col rounded-[14px] border border-[#e8ebf2] bg-white p-3">
          <div className="min-h-0 flex-1 overflow-auto">{renderContent()}</div>
        </div>
      </div>
      <Footer totalRows={items.length} />
    </div>
  );
}
