import React, { useState, useRef } from 'react';
import { Upload, File } from 'lucide-react';

const categories = [
  { id: 'bwindi_forest', name: 'Bwindi Forest' },
  { id: 'entebbe', name: 'Entebbe' },
  { id: 'gulu', name: 'Gulu' },
  { id: 'jinja', name: 'Jinja' },
  { id: 'kabale', name: 'Kabale' },
  { id: 'kampala', name: 'Kampala' },
  { id: 'kibale_national_park', name: 'Kibale National Park' },
  { id: 'kidepo_valley_national_park', name: 'Kidepo Valley National Park' },
  { id: 'lake_bunyonyi', name: 'Lake Bunyonyi' },
  { id: 'lake_mburo_national_park', name: 'Lake Mburo National Park' },
  { id: 'mbarara', name: 'Mbarara' },
  { id: 'murchison_falls_national_park', name: 'Murchison Falls National Park' },
  { id: 'queen_elizabeth_national_park', name: 'Queen Elizabeth National Park' },
  { id: 'rwenzori_mountains', name: 'Rwenzori Mountains' },
  { id: 'sipi_falls', name: 'Sipi Falls' }
];

export default function DocumentUpload() {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const inputRef = useRef(null);

  const handleDrag = function(e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = function(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleChange = function(e) {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = (newFiles) => {
    const validFiles = Array.from(newFiles).filter(file => 
      file.type === 'application/pdf' || 
      file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
      file.name.endsWith('.docx') ||
      file.name.endsWith('.pdf')
    );
    setFiles(prev => [...prev, ...validFiles]);
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 p-6 bg-white rounded-xl shadow-lg border border-gray-100">
      <h2 className="text-3xl font-bold mb-4 text-gray-800 text-center">Upload Documents</h2>
      <p className="text-gray-500 text-center mb-8">Upload your PDF or DOCX files to the knowledge base.</p>
      
      <div className="mb-6">
        <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">Select Category (City)</label>
        <select 
          id="category" 
          value={selectedCategory} 
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="w-full border border-gray-300 rounded-lg p-3 text-gray-700 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
        >
          <option value="" disabled>Select a category...</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
      </div>

      <form id="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()} className="relative">
        <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange} className="hidden" accept=".pdf,.docx" />
        <label id="label-file-upload" htmlFor="input-file-upload" className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-xl cursor-pointer transition-colors duration-300 ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50 hover:bg-gray-100'}`}>
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <Upload className={`w-12 h-12 mb-4 ${dragActive ? 'text-blue-500' : 'text-gray-400'}`} />
            <p className="mb-2 text-sm text-gray-500"><span className="font-semibold text-blue-600">Click to upload</span> or drag and drop</p>
            <p className="text-xs text-gray-400">PDF, DOCX (MAX. 10MB)</p>
          </div>
        </label>
        {dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop} className="absolute inset-0 w-full h-full rounded-xl"></div>}
      </form>

      {files.length > 0 && (
        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-4 text-gray-700">Selected Files ({files.length})</h3>
          <ul className="space-y-3">
            {files.map((file, idx) => (
              <li key={idx} className="flex items-center p-4 bg-gray-50 rounded-lg border border-gray-200">
                <File className="w-6 h-6 text-blue-500 mr-3" />
                <span className="text-sm font-medium text-gray-700 truncate flex-1">{file.name}</span>
                <span className="ml-4 text-xs text-gray-500 font-medium">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
              </li>
            ))}
          </ul>
          <button 
            disabled={!selectedCategory}
            className={`mt-6 w-full font-bold py-3 px-4 rounded-lg transition duration-300 shadow-md flex justify-center items-center ${!selectedCategory ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 'bg-blue-600 text-white hover:bg-blue-700'}`}
            title={!selectedCategory ? "Please select a category first" : ""}
          >
            <Upload className="w-5 h-5 mr-2" />
            Upload Files
          </button>
        </div>
      )}
    </div>
  );
}
