import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            User Registration
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Create your account to get started
          </p>
        </div>
        <div className="bg-white py-8 px-6 shadow rounded-lg">
          <p className="text-gray-500 text-center">
            Form implementation goes here
          </p>
          <p className="text-gray-400 text-center text-sm mt-4">
            Use Codex to build the complete registration form
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;