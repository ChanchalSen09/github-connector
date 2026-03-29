import { useEffect, useMemo, useState } from "react";
import { listKnowledgeBases, createKnowledgeBase } from "./api/knowledgeBase";
import { ArticleList } from "./components/ArticleList";
import { CreateKnowledgeModal } from "./components/CreateKnowledgeModal";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { TopBar } from "./components/TopBar";

function App() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [knowledgeBases, setKnowledgeBases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchValue, setSearchValue] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const loadKnowledgeBases = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await listKnowledgeBases();
        setKnowledgeBases(data);
      } catch (requestError) {
        setError(requestError.message || "Failed to load knowledge bases.");
      } finally {
        setLoading(false);
      }
    };

    loadKnowledgeBases();
  }, []);

  const filteredKnowledgeBases = useMemo(() => {
    const query = searchValue.trim().toLowerCase();
    if (!query) {
      return knowledgeBases;
    }

    return knowledgeBases.filter((item) => {
      return [item.name, item.description, item.vector_store, item.embedding_model].some((value) =>
        value.toLowerCase().includes(query)
      );
    });
  }, [knowledgeBases, searchValue]);

  const handleCreateKnowledgeBase = async (payload) => {
    try {
      setSubmitting(true);
      setSubmitError("");
      const createdItem = await createKnowledgeBase(payload);
      setKnowledgeBases((current) => [createdItem, ...current]);
      setIsDrawerOpen(false);
    } catch (requestError) {
      setSubmitError(requestError.message || "Failed to create knowledge base.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="h-screen overflow-hidden bg-[#f4f6fb] text-[#1f1f2a]">
      <TopBar />

      <div className="flex h-[calc(100vh-54px)] overflow-hidden">
        <Sidebar />

        <main className="flex-1 overflow-hidden bg-[#f6f7fb] px-5 py-5">
          <div className="mx-auto flex h-full w-full flex-col rounded-[18px] border border-[#e5e8f0] bg-white shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
            <Header
              onCreateNew={() => {
                setSubmitError("");
                setIsDrawerOpen(true);
              }}
              searchValue={searchValue}
              onSearchChange={setSearchValue}
            />
            <ArticleList items={filteredKnowledgeBases} loading={loading} error={error} />
          </div>
        </main>
      </div>

      <CreateKnowledgeModal
        open={isDrawerOpen}
        onClose={() => {
          setSubmitError("");
          setIsDrawerOpen(false);
        }}
        onSubmit={handleCreateKnowledgeBase}
        submitting={submitting}
        error={submitError}
      />
    </div>
  );
}

export default App;
