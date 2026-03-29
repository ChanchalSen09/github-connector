import { useEffect, useState } from "react";
import { FiChevronDown, FiX } from "react-icons/fi";

const vectorStoreOptions = ["Qdrant", "Pinecone", "Weaviate"];
const embeddingModelOptions = ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"];

function CloseIcon() {
  return <FiX className="h-4 w-4" />;
}

function FieldLabel({ label, required = false, disabledHint = false }) {
  return (
    <label className="mb-1.5 block text-[12px] font-medium text-[#2f2f38]">
      {label}
      {required ? <span className="text-[#d53939]">*</span> : null}
      {disabledHint ? <span className="text-[#d53939]"> (Cannot be edited later)*</span> : null}
    </label>
  );
}

export function CreateKnowledgeModal({ open, onClose, onSubmit, submitting, error }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    vector_store: "Qdrant",
    embedding_model: "text-embedding-ada-002",
  });

  useEffect(() => {
    if (!open) {
      setFormData({
        name: "",
        description: "",
        vector_store: "Qdrant",
        embedding_model: "text-embedding-ada-002",
      });
    }
  }, [open]);

  if (!open) {
    return null;
  }

  const handleChange = (field) => (event) => {
    setFormData((current) => ({
      ...current,
      [field]: event.target.value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-[rgba(33,33,43,0.36)]">
      <div className="h-full w-full max-w-[470px] bg-white shadow-[-20px_0_50px_rgba(15,23,42,0.08)]">
        <div className="flex items-start justify-between border-b border-[#f0f0f5] px-5 py-5">
          <div>
            <h2 className="text-[15px] font-semibold text-[#22222d]">Create New Knowledge Base</h2>
            <p className="mt-1 max-w-[320px] text-[11px] leading-5 text-[#8b8b98]">
              Best for quick answers from documents, websites and text files.
            </p>
          </div>
          <button type="button" onClick={onClose} className="text-[#7f7f8c]" disabled={submitting}>
            <CloseIcon />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex h-[calc(100%-84px)] flex-col justify-between px-5 py-5">
          <div className="space-y-4">
            <div>
              <FieldLabel label="Name" disabledHint />
              <input
                value={formData.name}
                onChange={handleChange("name")}
                placeholder="Name"
                className="h-11 w-full rounded-md border border-[#e7e7ee] px-3 text-[12px] text-[#2f2f38] outline-none placeholder:text-[#b0b0bb] focus:border-[#5b4ef7]"
                required
              />
            </div>

            <div>
              <FieldLabel label="Description" />
              <textarea
                value={formData.description}
                onChange={handleChange("description")}
                placeholder="Description"
                className="min-h-[96px] w-full resize-none rounded-md border border-[#e7e7ee] px-3 py-3 text-[12px] text-[#2f2f38] outline-none placeholder:text-[#b0b0bb] focus:border-[#5b4ef7]"
              />
            </div>

            <div className="relative">
              <FieldLabel label="Vector Store" required />
              <select
                value={formData.vector_store}
                onChange={handleChange("vector_store")}
                className="h-11 w-full appearance-none rounded-md border border-[#e7e7ee] bg-white px-3 pr-10 text-[12px] text-[#2f2f38] outline-none focus:border-[#5b4ef7]"
              >
                {vectorStoreOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
              <FiChevronDown className="pointer-events-none absolute right-3 top-[36px] text-[14px] text-[#8f8f9b]" />
            </div>

            <div className="relative">
              <FieldLabel label="LLM Embedding Model" required />
              <select
                value={formData.embedding_model}
                onChange={handleChange("embedding_model")}
                className="h-11 w-full appearance-none rounded-md border border-[#e7e7ee] bg-white px-3 pr-10 text-[12px] text-[#2f2f38] outline-none focus:border-[#5b4ef7]"
              >
                {embeddingModelOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
              <FiChevronDown className="pointer-events-none absolute right-3 top-[36px] text-[14px] text-[#8f8f9b]" />
            </div>

            {error ? <p className="text-[11px] text-[#d53939]">{error}</p> : null}
          </div>

          <div className="flex justify-end pb-2">
            <button
              type="submit"
              disabled={submitting}
              className="rounded-md bg-[#5b4ef7] px-5 py-2.5 text-[12px] font-medium text-white shadow-[0_10px_24px_rgba(91,78,247,0.25)] disabled:cursor-not-allowed disabled:opacity-70"
            >
              {submitting ? "Creating..." : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
