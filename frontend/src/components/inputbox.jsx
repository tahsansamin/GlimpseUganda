export default function ChatInput({ submitfunc, changefunc }) {
  return (
    <div className="flex w-full flex-1 items-center justify-center">
      <div className="flex w-full gap-2">
        <input
          type="text"
          placeholder="Ask about this place…"
          className="theme-input min-w-0 flex-1 px-4 py-3 text-sm shadow-sm"
          onChange={changefunc}
        />
        <button
          type="button"
          className="theme-btn-primary shrink-0 px-5 py-3 text-sm shadow-sm"
          onClick={submitfunc}
        >
          Send
        </button>
      </div>
    </div>
  );
}
