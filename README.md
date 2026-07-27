<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TruthSchool AI — App Launcher & Search</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-center items-center font-sans p-6 selection:bg-cyan-500 selection:text-black">
    <div class="max-w-xl w-full bg-slate-900/60 border border-slate-800/80 rounded-2xl p-8 backdrop-blur shadow-2xl text-center space-y-6">
        <div class="h-3 w-3 rounded-full bg-cyan-400 animate-pulse shadow-lg shadow-cyan-400/50 mx-auto"></div>
        <div>
            <h1 class="text-2xl font-bold tracking-tight bg-gradient-to-r from-cyan-400 via-fuchsia-400 to-indigo-500 bg-clip-text text-transparent">
                TruthSchool AI Portal
            </h1>
            <p class="text-xs text-slate-400 mt-1 uppercase tracking-widest font-mono">Student Production Edition</p>
        </div>

        <div class="relative">
            <input type="text" id="appSearch" placeholder="Search curriculum topics, math, science, or lyrics..." class="w-full bg-slate-950 border border-slate-700/80 rounded-xl px-5 py-4 text-sm focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 outline-none transition text-slate-200 placeholder-slate-500 shadow-inner" onkeydown="if(event.key==='Enter') launchApp()">
        </div>

        <div class="flex gap-4 justify-center">
            <a href="http://127.0.0.1:8000" target="_blank" class="bg-gradient-to-r from-cyan-600 via-blue-600 to-fuchsia-600 hover:opacity-95 font-semibold py-3 px-6 rounded-xl transition shadow-lg shadow-cyan-500/20 text-sm tracking-wide text-white inline-flex items-center gap-2">
                Launch Local App 🚀
            </a>
            <a href="https://github.com/lilcrazer19931993-afk/TruthSchool-AI" target="_blank" class="bg-slate-800 hover:bg-slate-700 border border-slate-700 font-semibold py-3 px-6 rounded-xl transition text-sm text-slate-200 inline-flex items-center gap-2">
                GitHub Repository 📦
            </a>
        </div>
    </div>

    <script>
        function launchApp() {
            window.open('http://127.0.0.1:8000', '_blank');
        }
    </script>
</body>
</html>
