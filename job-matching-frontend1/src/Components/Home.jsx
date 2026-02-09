import React from "react";
import heroImage from "../assets/react.svg"; // Fallback hero image (react.svg)
import Upload from './Upload'
import Chat from './Chat'

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-r from-indigo-50 via-white to-purple-50 font-sans">
      {/* Navbar */}
      <nav className="flex justify-between items-center p-6 bg-white shadow-md">
        <h1 className="text-2xl font-bold text-indigo-600">AI Job Matcher</h1>
        <div className="space-x-6">
          <a href="#features" className="text-gray-700 hover:text-indigo-600 font-medium">Features</a>
          <a href="/upload" className="text-white bg-indigo-600 px-4 py-2 rounded-lg hover:bg-indigo-500 transition">Upload CV</a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="flex flex-col md:flex-row items-center justify-between px-6 md:px-20 py-20">
        <div className="md:w-1/2 space-y-6">
          <h2 className="text-4xl md:text-5xl font-bold text-indigo-700">Get Your Dream Job Faster</h2>
          <p className="text-gray-600 text-lg">
            Analyze your resume, discover skill gaps, and match with the perfect jobs using AI-powered recommendations.
          </p>
          <a href="/upload" className="inline-block bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-500 transition">
            Upload Your Resume
          </a>
        </div>
        <div className="md:w-1/2 mt-10 md:mt-0">
          <img src={heroImage} alt="AI Job Matching" className="w-full rounded-lg shadow-lg" />
        </div>
      </section>

      {/* Upload / Analyze */}
      <section className="px-6 md:px-20 py-12 bg-gray-50">
        <Upload />
      </section>

      {/* Chatbot */}
      <section className="px-6 md:px-20 py-12 bg-white">
        <Chat />
      </section>

      {/* Features Section */}
      <section id="features" className="px-6 md:px-20 py-20 bg-white">
        <h3 className="text-3xl font-bold text-center text-indigo-700 mb-12">Features</h3>
        <div className="grid md:grid-cols-3 gap-10 text-center">
          <div className="p-6 bg-indigo-50 rounded-xl shadow hover:shadow-lg transition">
            <h4 className="text-xl font-semibold mb-2">Resume Parsing</h4>
            <p className="text-gray-600">Automatically extract your skills, experience, and education from your resume.</p>
          </div>
          <div className="p-6 bg-indigo-50 rounded-xl shadow hover:shadow-lg transition">
            <h4 className="text-xl font-semibold mb-2">Job Matching</h4>
            <p className="text-gray-600">Get a suitability score for each job and know exactly where you fit best.</p>
          </div>
          <div className="p-6 bg-indigo-50 rounded-xl shadow hover:shadow-lg transition">
            <h4 className="text-xl font-semibold mb-2">Skill Gap Analysis</h4>
            <p className="text-gray-600">Identify missing skills and receive curated course recommendations.</p>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-indigo-600 text-white text-center">
        <h3 className="text-3xl font-bold mb-4">Start Your Career Journey Today!</h3>
        <p className="mb-6 text-lg">Upload your resume and let AI guide you to your dream job.</p>
        <a href="/upload" className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition">
          Upload Resume
        </a>
      </section>

      {/* Footer */}
      <footer className="bg-white py-6 text-center text-gray-500 shadow-inner">
        &copy; 2026 Abdullah Zuhry - AI Job Matcher. All rights reserved.
      </footer>
    </div>
  );
};

export default Home;
