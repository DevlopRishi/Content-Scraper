// src/hooks/useScraper.js
import { useState, useEffect } from 'react';

export const useScraper = () => {
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const startScraping = async (url, options = {}) => {
    try {
      const response = await fetch('/api/scrape/website', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          max_pages: options.maxPages || 100,
          max_workers: options.maxWorkers || 5,
          include_subdomains: options.includeSubdomains || true,
        }),
      });

      const data = await response.json();
      setTaskId(data.task_id);
      setStatus('PENDING');
      return data.task_id;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const checkStatus = async (id) => {
    try {
      const response = await fetch(`/api/task/${id}`);
      const data = await response.json();
      setStatus(data.status);
      if (data.result) {
        setResult(data.result);
      }
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  useEffect(() => {
    let interval;
    if (taskId && status !== 'COMPLETED' && status !== 'FAILED') {
      interval = setInterval(() => {
        checkStatus(taskId);
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [taskId, status]);

  return {
    startScraping,
    status,
    result,
    error,
  };
};

// Update ScraperApp.jsx to use the new hook
import React, { useState } from 'react';
import { useScraper } from './hooks/useScraper';

const ScraperApp = () => {
  const [url, setUrl] = useState('');
  const [options, setOptions] = useState({
    maxPages: 100,
    maxWorkers: 5,
    includeSubdomains: true,
  });
  
  const { startScraping, status, result, error } = useScraper();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await startScraping(url, options);
    } catch (err) {
      console.error('Failed to start scraping:', err);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Previous UI code remains the same */}
      
      {/* Add options controls */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            Maximum Pages
          </label>
          <input
            type="number"
            value={options.maxPages}
            onChange={(e) => setOptions({
              ...options,
              maxPages: parseInt(e.target.value)
            })}
            className="w-full px-4 py-2 border rounded-md"
          />
        </div>

        <div>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={options.includeSubdomains}
              onChange={(e) => setOptions({
                ...options,
                includeSubdomains: e.target.checked
              })}
              className="rounded"
            />
            <span className="text-sm">Include Subdomains</span>
          </label>
        </div>
      </div>

      {/* Status and results display */}
      {status && (
        <div className="bg-gray-50 p-4 rounded-md">
          <h3 className="font-medium">Status: {status}</h3>
          {result && (
            <div className="mt-2">
              <p>Pages Scraped: {result.pages_scraped}</p>
              {result.download_url && (
                <a
                  href={result.download_url}
                  className="text-blue-500 hover:underline"
                  download
                >
                  Download Results
                </a>
              )}
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="bg-red-50 text-red-700 p-4 rounded-md">
          {error}
        </div>
      )}
    </div>
  );
};

export default ScraperApp;