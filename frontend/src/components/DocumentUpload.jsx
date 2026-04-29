import React, { useState, useRef } from 'react';
import { Upload, File } from 'lucide-react';
import { supabase } from '../utils/supabase';
import apiClient from '../api';

const categories = [
  { id: 'bwindi_forests', name: 'Bwindi Forest' },
  { id: 'entebbe', name: 'Entebbe' },
  { id: 'gulu', name: 'Gulu' },
  { id: 'jinja', name: 'Jinja' },
  { id: 'kabale', name: 'Kabale' },
  { id: 'kampala', name: 'Kampala' },
  { id: 'kibale_national_park', name: 'Kibale National Park' },
  { id: 'kidepo_national_park', name: 'Kidepo National Park' },
  { id: 'lake_bunyonyi', name: 'Lake Bunyonyi' },
  { id: 'mburo_national_park', name: 'Lake Mburo National Park' },
  { id: 'mbarara', name: 'Mbarara' },
  { id: 'murchison_falls', name: 'Murchison Falls National Park' },
  { id: 'queen_elizabeth_national_park', name: 'Queen Elizabeth National Park' },
  { id: 'rwenzori_mountains', name: 'Rwenzori Mountains' },
  { id: 'sipi_falls', name: 'Sipi Falls' }
];

export default function DocumentUpload() {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState({ type: '', message: '' });
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

  const handleUpload = async () => {
    // Validation
    if (!selectedCategory) {
      setUploadStatus({ type: 'error', message: 'Please select a category' });
      return;
    }

    if (files.length === 0) {
      setUploadStatus({ type: 'error', message: 'Please select files to upload' });
      return;
    }

    // Check file sizes (10MB limit)
    const maxSize = 10 * 1024 * 1024;
    const oversizedFiles = files.filter(file => file.size > maxSize);
    if (oversizedFiles.length > 0) {
      setUploadStatus({ type: 'error', message: `Files exceed 10MB limit: ${oversizedFiles.map(f => f.name).join(', ')}` });
      return;
    }

    setIsLoading(true);
    setUploadStatus({ type: '', message: '' });

    try {
      // Read file as bytes
      const formData = new FormData();
      formData.append('document', files[0]); // files[0] is the actual File object
      formData.append('filename', files[0].name);
      formData.append('category', selectedCategory);

      const verificationResponse = await apiClient.post('/verify_document', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      

      if (!verificationResponse.data.status == 'verified') {
        setUploadStatus({ 
          type: 'error', 
          message: verificationResponse.data.error || 'Document verification failed' 
        });
        return;
      }
      console.log('Document verified successfully, proceeding to upload...'); //del later

      // If verification passes, upload to Supabase
      console.log(`my path is ${selectedCategory}/${files[0].name}`); //del later
      const {data,error} = await supabase.storage.from('test bucket').upload(
        `${selectedCategory}/${files[0].name}`, 
        files[0]
      );
      
      if (error) {
        setUploadStatus({ 
          type: 'error', 
          message: `Upload failed: ${error.message}` 
        });
        return;
      }

      // Clear form after successful upload
      setUploadStatus({ 
        type: 'success', 
        message: `Successfully uploaded ${files[0].name}` 
      });
      setFiles([]);
      setSelectedCategory('');
      if (inputRef.current) {
        inputRef.current.value = '';
      }

    } catch (error) {
      setUploadStatus({ 
        type: 'error', 
        message: `Upload failed: ${error.message}` 
      });
    } finally {
      setIsLoading(false);
    }
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

      {uploadStatus.message && !files.length && (
        <div className={`mt-6 p-4 rounded-lg text-sm font-medium ${
          uploadStatus.type === 'success' 
            ? 'bg-green-50 text-green-800 border border-green-200 flex items-center' 
            : 'bg-red-50 text-red-800 border border-red-200 flex items-center'
        }`}>
          <span className="mr-2 text-lg">{uploadStatus.type === 'success' ? '✓' : '✕'}</span>
          {uploadStatus.message}
        </div>
      )}

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
            onClick={handleUpload}
            disabled={!selectedCategory || isLoading}
            className={`mt-6 w-full font-bold py-3 px-4 rounded-lg transition duration-300 shadow-md flex justify-center items-center ${!selectedCategory || isLoading ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 'bg-blue-600 text-white hover:bg-blue-700'}`}
            title={!selectedCategory ? "Please select a category first" : ""}
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Uploading...
              </>
            ) : (
              <>
                <Upload className="w-5 h-5 mr-2" />
                Upload Files
              </>
            )}
          </button>

          {uploadStatus.message && (
            <div className={`mt-4 p-4 rounded-lg text-sm font-medium flex items-center ${
              uploadStatus.type === 'success' 
                ? 'bg-green-50 text-green-800 border border-green-200' 
                : 'bg-red-50 text-red-800 border border-red-200'
            }`}>
              <span className="mr-2 text-lg">{uploadStatus.type === 'success' ? '✓' : '✕'}</span>
              {uploadStatus.message}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
