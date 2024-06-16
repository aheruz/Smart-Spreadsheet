import React, { useState } from 'react';
import { PaperAirplaneIcon, PaperClipIcon } from '@heroicons/react/20/solid';
import { XCircleIcon, ArrowPathIcon } from '@heroicons/react/24/outline';
import loadingGif from '../../public/loading-icon.gif';

import axios from 'axios';

interface FixedInputSectionProps {
  input: string;
  setInput: (input: string) => void;
  handleSubmission: () => void;
}

export default function ChatInput({ input, setInput, handleSubmission }: FixedInputSectionProps) {
    const [file, setFile] = useState<File | null>(null);
    const [uploadStatus, setUploadStatus] = useState<string>('');
    const isInputEmpty = input.trim() === '' && !file;
    const [isUploading, setIsUploading] = useState<boolean>(false);

    /**
     * Handle file change
     * @param event 
     */
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
          setFile(event.target.files[0]);
        }
    };

    const handleFileUpload = async () => {
        if (file) {
          const formData = new FormData();
          formData.append('file', file);
          setIsUploading(true);
          try {
            setUploadStatus('Uploading...');
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            });
            if (response.status === 200) {
              setUploadStatus('Upload successful');
              setFile(null);
            } else {
              setUploadStatus('Upload failed');
            }
          } catch (error) {
            setUploadStatus('Upload failed');
          } finally {
            setIsUploading(false);
          }
        }
    };

  return (
    <div className="flex flex-row gap-2 p-2 bg-zinc-100 w-full">
        <div className="backdrop-blur-sm bg-white/30 fixed w-[98%] sm:w-[91%] ml-[1%] left-0 sm:ml-[-2%] sm:left-auto md:w-[91.5%] lg:w-[67.5%] xl:w-full max-w-3xl bottom-0">
            <div className="flex items-center w-full text-gray-500 bg-gray-100 rounded-2xl p-2 pl-4 sm:p-2 sm:pl-5 shadow-xl mb-2 sm:mb-3">
                <input
                    type="file"
                    id="file-upload"
                    accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    className="hidden"
                    onChange={handleFileChange}
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                    <PaperClipIcon className="h-6 w-6 mr-2" aria-hidden="true" />
                </label>
                {file ? (
                    <div className="flex flex-1 items-center space-x-2">
                        <span className="text-sm truncate">{file.name}</span>
                        {isUploading ? (
                            <img src={loadingGif.src} alt="Uploading..." className="h-[21px] w-[21px]" />
                        ) : (
                            <XCircleIcon className="h-5 w-5 cursor-pointer" aria-hidden="true" onClick={() => setFile(null)} />
                        )}
                    </div>
                ) : (
                    <input
                        type="text"
                        className="flex-1 bg-transparent text-base font-light focus:outline-none text-md placeholder:text-slate-400 placeholder:text-slate-400"
                        placeholder="Ask a question"
                        value={input}
                        onChange={event => setInput(event.target.value)}
                        onKeyDown={event => {
                            if (event.key === 'Enter' && !isInputEmpty) {
                            handleSubmission();
                            }
                        }}
                        disabled={!!file}
                    />
                )}
            
                <button
                    onClick={() => {
                        if (!isInputEmpty) {
                            if (file) {
                                handleFileUpload();
                            } else {
                                handleSubmission();
                            }
                        }
                    }}
                    className={`flex items-center justify-center h-9 w-9 rounded-xl px-2 py-1.5 text-sm font-semibold text-white shadow-sm ring-0 transition duration-200 ${isInputEmpty ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700'}`}
                    disabled={isInputEmpty}
                >
                    <PaperAirplaneIcon className="h-5 w-5 sm:h-6 sm:w-6 sm:ml-[2px] sm:mt-[0.25px] inline" aria-hidden="true"/>
                </button>
            </div>
            <p className="text-xs text-gray-500 text-center mb-2 sm:mb-3 mr-2 sm:mr-4">
                Made by Alfonso Hernandez. Review source code on <span className="font-semibold"><a href="https://github.com/aheruz/Smart-Spreadsheet" target="_blank" className="underline">GitHub</a></span>
            </p>
        </div>
    </div>
  );
}