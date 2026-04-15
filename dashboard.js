async function loadDashboard() {
    try {
        const res = await fetch("/dashboard");
        const data = await res.json();

        // -----------------------------
        // UPDATE BUILD OPPORTUNITIES
        // -----------------------------
        const buildTable = document.getElementById("build-table");

        if (buildTable) {
            buildTable.innerHTML = "";

            data.build_opportunities.forEach(item => {
                const row = `
                    <tr>
                        <td>${item.keyword}</td>
                        <td>BUILD</td>
                        <td>${item.score}</td>
                    </tr>
                `;
                buildTable.innerHTML += row;
            });
        }

        // -----------------------------
        // UPDATE PROTECTION LAYER
        // -----------------------------
        const protectTable = document.getElementById("protect-table");

        if (protectTable) {
            protectTable.innerHTML = "";

            data.protection_layer.forEach(item => {
                const row = `
                    <tr>
                        <td>${item.url}</td>
                        <td>${item.risk}</td>
                        <td>${item.action}</td>
                    </tr>
                `;
                protectTable.innerHTML += row;
            });
        }

        // -----------------------------
        // UPDATE WINNERS
        // -----------------------------
        const winnerTable = document.getElementById("winner-table");

        if (winnerTable) {
            winnerTable.innerHTML = "";

            data.winners.forEach(item => {
                const row = `
                    <tr>
                        <td>${item.url}</td>
                        <td>${item.status}</td>
                    </tr>
                `;
                winnerTable.innerHTML += row;
            });
        }

    } catch (err) {
        console.error("Dashboard load error:", err);
    }
}

// Auto refresh every 10 seconds
setInterval(loadDashboard, 10000);

// Initial load
loadDashboard();
