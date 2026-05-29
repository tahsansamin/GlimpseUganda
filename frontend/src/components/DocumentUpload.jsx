import React, { useState, useRef } from 'react';
import { Upload, File, Trash2 } from 'lucide-react';
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

  const handleDeleteFile = (indexToDelete) => {
    setFiles(prev => prev.filter((_, idx) => idx !== indexToDelete));
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

      // If verification passes, upload to Supabase
      console.log(`my path is ${selectedCategory}/${files[0].name}`); //del later
      console.log(`{text: ${verificationResponse.data.summary.is_directly_related}}`); //del later
      if (!verificationResponse.data.summary.is_directly_related) {
        setUploadStatus({ 
          type: 'error', 
          message: 'Document is not directly related to the selected category' 
        });
        return;
      } 
      const {data,error} =  await supabase.storage.from('test bucket').upload(
        `${selectedCategory}/${files[0].name}`, 
        files[0]
      );
      const { data1, error1 } = await supabase
        .from('pinecone_docs')
        .insert([
          {
            city: selectedCategory,
            file_name: files[0].name,
            storage_path: `${selectedCategory}/${files[0].name}`, // Template literal instead of f""
            mime_type: 'application/pdf',
            status: 'processing'
          }
        ]);

      if (error1) {
        console.error('Error inserting row:', error);
      }
      
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
        message: `Upload failed: ${error}` 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mx-auto mt-8 max-w-3xl rounded-[14px] border border-[rgba(61,82,56,0.18)] bg-[var(--color-white)] p-6 shadow-lg">
      <h2 className="mb-2 text-center text-3xl font-bold text-[var(--color-forest-deep)]">
        Upload documents
      </h2>
      <p className="mb-8 text-center text-[var(--color-text-muted)]">
        Upload your PDF or DOCX files to the knowledge base.
      </p>
      
      <div className="mb-6">
        <label htmlFor="category" className="mb-2 block text-sm font-semibold text-[var(--color-forest-deep)]">
          Select category (city)
        </label>
        <select 
          id="category" 
          value={selectedCategory} 
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="theme-input w-full p-3 text-[var(--color-text)] shadow-sm"
        >
          <option value="" disabled>Select a category...</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
      </div>

      <form id="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()} className="relative">
        <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange} className="hidden" accept=".pdf,.docx" />
        <label id="label-file-upload" htmlFor="input-file-upload" className={`flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed transition-colors duration-300 ${dragActive ? "border-[var(--color-water)] bg-[rgba(90,143,178,0.08)]" : "border-[rgba(61,82,56,0.28)] bg-[var(--color-cream)] hover:bg-[var(--color-cream-dark)]"}`}>
          <div className="flex flex-col items-center justify-center pb-6 pt-5">
            <Upload className={`mb-4 h-12 w-12 ${dragActive ? "text-[var(--color-water)]" : "text-[var(--color-text-muted)]"}`} />
            <p className="mb-2 text-sm text-[var(--color-text-muted)]">
              <span className="font-semibold text-[var(--color-maroon)]">Click to upload</span> or drag and drop
            </p>
            <p className="text-xs text-[var(--color-text-muted)]">PDF, DOCX (MAX. 10MB)</p>
          </div>
        </label>
        {dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop} className="absolute inset-0 w-full h-full rounded-xl"></div>}
      </form>

      {uploadStatus.message && !files.length && (
        <div
          className={`mt-6 flex items-center rounded-lg border p-4 text-sm font-medium ${
            uploadStatus.type === "success"
              ? "border-[rgba(107,142,94,0.45)] bg-[rgba(168,198,159,0.25)] text-[var(--color-forest-deep)]"
              : "border-[rgba(139,69,69,0.35)] bg-[rgba(139,69,69,0.08)] text-[var(--color-maroon)]"
          }`}
        >
          <span className="mr-2 text-lg">{uploadStatus.type === 'success' ? '✓' : '✕'}</span>
          {uploadStatus.message}
        </div>
      )}

      {files.length > 0 && (
        <div className="mt-8">
          <h3 className="mb-4 text-lg font-semibold text-[var(--color-forest-deep)]">
            Selected files ({files.length})
          </h3>
          <ul className="space-y-3">
            {files.map((file, idx) => (
              <li
                key={idx}
                className="flex items-center rounded-lg border border-[rgba(61,82,56,0.15)] bg-[var(--color-cream)] p-4"
              >
                <File className="mr-3 h-6 w-6 text-[var(--color-water)]" />
                <span className="flex-1 truncate text-sm font-medium text-[var(--color-text)]">{file.name}</span>
                <span className="ml-4 text-xs font-medium text-[var(--color-text-muted)]">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </span>
                <button
                  onClick={() => handleDeleteFile(idx)}
                  className="ml-4 rounded-lg p-2 text-[var(--color-maroon)] transition-colors duration-200 hover:bg-[rgba(139,69,69,0.1)]"
                  title="Delete file"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </li>
            ))}
          </ul>
          <button 
            onClick={handleUpload}
            disabled={!selectedCategory || isLoading}
            className={`mt-6 flex w-full items-center justify-center rounded-lg px-4 py-3 font-bold shadow-md transition duration-300 ${
              !selectedCategory || isLoading
                ? "cursor-not-allowed bg-[var(--color-cream-dark)] text-[var(--color-text-muted)]"
                : "theme-btn-primary"
            }`}
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
            <div
              className={`mt-4 flex items-center rounded-lg border p-4 text-sm font-medium ${
                uploadStatus.type === "success"
                  ? "border-[rgba(107,142,94,0.45)] bg-[rgba(168,198,159,0.25)] text-[var(--color-forest-deep)]"
                  : "border-[rgba(139,69,69,0.35)] bg-[rgba(139,69,69,0.08)] text-[var(--color-maroon)]"
              }`}
            >
              <span className="mr-2 text-lg">{uploadStatus.type === 'success' ? '✓' : '✕'}</span>
              {uploadStatus.message}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
