
async function fetchData() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        renderDashboard(data);
    } catch (err) {
        console.error('Error fetching data:', err);
    }
}

function renderDashboard(data) {
    // 1. KPI Cards
    const totalRev = data.orders.reduce((sum, o) => sum + o.total_amount, 0);
    const totalOrders = data.orders.length;
    const aov = totalRev / totalOrders;

    document.getElementById('total-revenue').innerText = `â‚¬${totalRev.toLocaleString(undefined, {minimumFractionDigits: 2})}`;
    document.getElementById('total-orders').innerText = totalOrders;
    document.getElementById('aov').innerText = `â‚¬${aov.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    // 2. Category Chart
    const catData = {};
    data.order_items.forEach(item => {
        const prod = data.products.find(p => p.id === item.product_id);
        if (prod) {
            catData[prod.category] = (catData[prod.category] || 0) + (item.quantity * item.price_at_purchase);
        }
    });

    const categoryChart = echarts.init(document.getElementById('category-chart'), 'dark');
    categoryChart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'item', formatter: '{b}: â‚¬{c} ({d}%)' },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: { borderRadius: 10, borderColor: '#161b22', borderWidth: 2 },
            label: { show: false },
            data: Object.entries(catData).map(([name, value]) => ({ name, value: Math.round(value) }))
        }]
    });

    // 3. Trends Chart
    const trends = {};
    data.orders.forEach(o => {
        const date = o.order_date.split('T')[0];
        trends[date] = (trends[date] || 0) + o.total_amount;
    });

    const sortedDates = Object.keys(trends).sort();
    const trendChart = echarts.init(document.getElementById('trends-chart'), 'dark');
    trendChart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: sortedDates, axisLabel: { hideOverlap: true } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#30363d' } } },
        series: [{
            data: sortedDates.map(d => Math.round(trends[d])),
            type: 'line',
            smooth: true,
            areaStyle: { opacity: 0.1 },
            color: '#58a6ff'
        }]
    });
}

fetchData();
