async function submitForm() {

    const jobDesc = document.getElementById("jobDescription").value;
    const category = document.getElementById("jobCategory").value;
    const files = document.getElementById("resumeFiles").files;

    const resultsDiv = document.getElementById("results");
    const btn = document.getElementById("analyzeBtn");

    if (!jobDesc || files.length === 0) {
        resultsDiv.innerHTML =
            "<h3 style='color:red;'>Please enter Job Description and upload at least one resume.</h3>";
        return;
    }

    const formData = new FormData();

    formData.append("job_description", jobDesc);
    formData.append("category", category);

    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    btn.disabled = true;
    btn.innerText = "Analyzing...";

    resultsDiv.innerHTML =
        "<h2 style='text-align:center;'>⏳ AI is analyzing resumes...</h2>";

    try {

        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server Error : " + response.status);
        }

        const data = await response.json();

        console.log(data);

        let html = `
        <div class="dashboard-header">
        <h2>📋 Resume Analysis Results</h2>
        <p>${data.results.length} Candidate(s) Analyzed</p>
        </div>
        `;

        data.results.forEach(r => {

            let color = "green";
            let icon = "🟢";

            if (r.similarity === "Medium Match") {
                color = "orange";
                icon = "🟡";
            }

            if (r.similarity === "Low Match") {
                color = "red";
                icon = "🔴";
            }
                        html += `
            <div class="result-card">

                <h2>🏆 Rank ${r.rank}</h2>

                <div class="summary-card">
                    <h3>Resume Summary</h3>

                    <p><b>👤 Candidate:</b> ${r.candidate_name}</p>
                    <p><b>🎓 Education:</b> ${r.education}</p>
                    <p><b>💼 Experience:</b> ${r.experience}</p>
                    <p><b>📁 Projects:</b> ${r.projects}</p>
                    <p><b>🏅 Certifications:</b> ${r.certifications}</p>
                </div>

                <div class="status-card">
                    <h3>📊 Status</h3>
                    
                    <p><b>Rank:</b> ${r.rank}</p>
                    
                    <p><b>Recommendation:</b></p>
                    
                    <p style="color:${color};font-weight:bold;">
                        ${icon} ${r.suitability}
                    </p>
                </div>

                <div class="score-card">
                    <p><b>📄 Resume:</b> ${r.filename}</p>
                    <p><b>📂 Category:</b> ${r.category}</p>

                    <p><b>🎯 ATS Score:</b> ${r.score}%</p>

                    <div class="progress-container">
                        <div class="progress-bar" style="width:${r.score}%;">
                            ${r.score}%
                        </div>
                    </div>

                    <p><b>📊 Similarity:</b> ${r.similarity}</p>

                    <p style="color:${color};font-weight:bold;">
                        ${icon} ${r.suitability}
                    </p>
                </div>

                <div class="stats-card">

                    <h3>📊 Skill Statistics</h3>

                    <p>✅ Matched Skills :
                        <b>${r.matched_skills.length}</b>
                    </p>

                    <p>❌ Missing Skills :
                        <b>${r.missing_skills.length}</b>
                    </p>

                    <p>🎯 Total Skills :
                        <b>${r.matched_skills.length + r.missing_skills.length}</b>
                    </p>
                                        <hr>

                    <h4>✅ Matched Skills</h4>

                    <ul>
                        ${r.matched_skills.map(skill => `<li>✔ ${skill}</li>`).join("")}
                    </ul>

                    <h4>❌ Missing Skills</h4>

                    <ul>
                        ${r.missing_skills.map(skill => `<li>✖ ${skill}</li>`).join("")}
                    </ul>

                    <h4>💡 Suggestions</h4>

                    <ul>
                        ${r.suggestions.map(item => `<li>${item}</li>`).join("")}
                    </ul>

                    <h4>🎯 Interview Questions</h4>
                    
                    <ul>
                         ${(r.interview_questions || []).map(q => `<li>${q}</li>`).join("")}
                         
                    </ul>

                    <hr>
                    
                    <h3>📊 Skill Analysis</h3>
                    
                    <div class="chart-box">
                    
                        <canvas class="skillChart"></canvas>

                    </div>
                    
                    </div>   <!-- closes stats-card -->
                    
                    </div>   <!-- closes result-card -->
                
            `;
        });


        const total = data.results.length;

const highest = Math.max(...data.results.map(r => r.score));

const average = Math.round(
    data.results.reduce((sum, r) => sum + r.score, 0) / total
);

const recommended = data.results.filter(
    r => r.score >= 80
).length;

html += `
<div class="dashboard-stats">

    <div class="stat-card">
        <h3>Total Candidates</h3>
        <h1>${total}</h1>
    </div>

    <div class="stat-card">
        <h3>Highest ATS</h3>
        <h1>${highest}%</h1>
    </div>

    <div class="stat-card">
        <h3>Average ATS</h3>
        <h1>${average}%</h1>
    </div>

    <div class="stat-card">
        <h3>Recommended</h3>
        <h1>${recommended}</h1>
    </div>

</div>
`;

        resultsDiv.innerHTML = html;

        const downloadBtn = document.getElementById("downloadBtn");

if (downloadBtn) {
    downloadBtn.style.display = "inline-block";
}

        console.log("HTML inserted successfully");
        // ===== Skill Analysis Charts =====

const charts = document.querySelectorAll(".skillChart");

charts.forEach((canvas, index) => {

    const candidate = data.results[index];

    if (!candidate) return;

    new Chart(canvas, {
        type: "doughnut",

        data: {
            labels: [
                "Matched Skills",
                "Missing Skills"
            ],

            datasets: [{
                data: [
                    candidate.matched_skills.length,
                    candidate.missing_skills.length
                ],

                backgroundColor: [
                    "#22c55e",
                    "#ef4444"
                ]
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });

});

    } catch (error) {

        console.error(error);

        resultsDiv.innerHTML =
            "<h2 style='color:red;text-align:center;'>❌ Error analyzing resumes.</h2>";

    }

    btn.disabled = false;
    btn.innerText = "Analyze Candidates";
}

function downloadReport() {
    window.open("http://127.0.0.1:8000/download-report", "_blank");
}

function searchCandidate() {

    const input = document
        .getElementById("searchInput")
        .value
        .trim()
        .toLowerCase();

    const cards = document.querySelectorAll(".result-card");

    cards.forEach(card => {

        const candidateText = card.innerText.toLowerCase();

        if (input === "" || candidateText.includes(input)) {
            card.style.display = "grid";
        } else {
            card.style.display = "none";
        }

    });

}