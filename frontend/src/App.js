import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { MediaProvider } from './contexts/MediaContext';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import InterviewSetup from './pages/InterviewSetup';
import InterviewSession from './pages/InterviewSession';
import ResultsPage from './pages/ResultsPage';
import './App.css';

function App() {
  return (
    <MediaProvider>
      <Router>
        <div className="App min-h-screen bg-gray-50">
          <Header />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/setup" element={<InterviewSetup />} />
              <Route path="/interview/:sessionId" element={<InterviewSession />} />
              <Route path="/results/:sessionId" element={<ResultsPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </MediaProvider>
  );
}

export default App;