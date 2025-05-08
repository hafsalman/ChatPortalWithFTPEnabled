import React, { useState } from 'react';
import { uploadFile, downloadFile } from '../utils/api';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState('');
  const [error, setError] = useState('');

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file.');
      return;
    }

    try {
      await uploadFile(file);
      alert('File uploaded successfully!');
      setFile(null);
      setError('');
    } catch (err) {
      setError('Failed to upload file.');
    }
  };

  const handleDownload = async (e) => {
    e.preventDefault();
    if (!filename) {
      setError('Please enter a filename.');
      return;
    }

    try {
      await downloadFile(filename);
      alert(`File ${filename} downloaded successfully!`);
      setFilename('');
      setError('');
    } catch (err) {
      setError('Failed to download file.');
    }
  };

  return (
    <div style={styles.container}>
      <h3>File Upload</h3>
      <form onSubmit={handleUpload} style={styles.form}>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          style={styles.input}
        />
        <button type="submit" style={styles.button}>Upload</button>
      </form>

      <h3>File Download</h3>
      <form onSubmit={handleDownload} style={styles.form}>
        <input
          type="text"
          value={filename}
          onChange={(e) => setFilename(e.target.value)}
          placeholder="Enter filename (e.g., example.txt)"
          style={styles.input}
        />
        <button type="submit" style={styles.button}>Download</button>
      </form>

      {error && <p style={styles.error}>{error}</p>}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '600px',
    margin: '20px auto',
    padding: '10px',
  },
  form: {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px',
  },
  input: {
    flex: 1,
    padding: '8px',
    fontSize: '16px',
  },
  button: {
    padding: '8px 16px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
  },
  error: {
    color: 'red',
    marginTop: '10px',
  },
};

export default FileUpload;