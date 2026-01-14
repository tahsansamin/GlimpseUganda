
export default function ChatInput({submitfunc, changefunc}) {
  return (
    <div className="flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="text-black bg-white flex gap-3">
          <input
            type="text"
            placeholder="Type your message..."
            className="flex-1 px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-sm"
            onChange={changefunc}
          />
          <button className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-xl font-medium transition-colors duration-200 shadow-sm hover:shadow-md whitespace-nowrap" onClick={submitfunc}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}