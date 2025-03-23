// transmbd.js - 统一交互脚本

document.addEventListener('DOMContentLoaded', function() {
    // Debug banner visibility
    const banner = document.querySelector('.main-banner');
    if (banner) {
        console.log('Banner found:', banner);
        console.log('Banner computed style:', window.getComputedStyle(banner));
    } else {
        console.error('Banner not found in DOM');
    }
    
    // Check content padding
    const mainContainer = document.querySelector('.main-container');
    if (mainContainer) {
        console.log('Main container padding:', window.getComputedStyle(mainContainer).padding);
    }
    
    // Add subtle scroll effect to the banner
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 80) {
            // Scrolling down & past initial position - slightly reduce banner size
            if (banner) {
                banner.style.height = '56px';
                banner.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.15)';
            }
        } else {
            // Scrolling up or at top - restore original size
            if (banner) {
                banner.style.height = '64px';
                banner.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
            }
        }
        
        lastScrollTop = scrollTop;
    });
    
    // 侧边栏折叠功能
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            document.body.classList.toggle('sidebar-toggled');
            document.querySelector('.sidebar').classList.toggle('toggled');
        });
    }
    
    // 自动高亮当前导航项
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-nav .nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href)) {
            link.classList.add('active');
        }
    });
    
    // 确保用户下拉菜单可通过键盘访问
    const userInfo = document.querySelector('.user-info');
    if (userInfo) {
        userInfo.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                const dropdownMenu = this.querySelector('.dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.style.display = 
                        dropdownMenu.style.display === 'block' ? 'none' : 'block';
                }
            }
        });
        
        userInfo.setAttribute('tabindex', '0');
        userInfo.setAttribute('role', 'button');
        userInfo.setAttribute('aria-haspopup', 'true');
    }
    
    // 对话滚动到底部
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // 表格排序和搜索功能
    const dataTable = document.getElementById('dataTable');
    if (dataTable) {
        enhanceDataTable(dataTable);
    }
    
    // 动态添加淡入效果
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('fade-in');
    });
    
    // 卡片折叠功能
    document.querySelectorAll('.card-collapsible').forEach(card => {
        const header = card.querySelector('.card-header');
        const body = card.querySelector('.card-body');
        
        if (header && body) {
            header.addEventListener('click', function() {
                body.classList.toggle('collapse');
                const icon = header.querySelector('.collapse-icon');
                if (icon) {
                    icon.classList.toggle('fa-chevron-down');
                    icon.classList.toggle('fa-chevron-up');
                }
            });
        }
    });
    
    // 初始化提示工具
    initTooltips();
    
    // 绘制空图表
    drawEmptyCharts();
});

// 增强表格功能
function enhanceDataTable(table) {
    // 添加搜索功能
    const wrapper = document.createElement('div');
    wrapper.className = 'table-wrapper';
    
    const searchContainer = document.createElement('div');
    searchContainer.className = 'table-search mb-3';
    
    const searchInput = document.createElement('input');
    searchInput.type = 'search';
    searchInput.className = 'form-control';
    searchInput.placeholder = '搜索...';
    searchInput.addEventListener('input', function() {
        filterTable(table, this.value);
    });
    
    searchContainer.appendChild(searchInput);
    
    // 插入搜索框到表格前
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(searchContainer);
    wrapper.appendChild(table);
    
    // 添加排序功能
    const headers = table.querySelectorAll('th');
    headers.forEach(header => {
        if (!header.classList.contains('no-sort')) {
            header.style.cursor = 'pointer';
            header.innerHTML += ' <i class="fas fa-sort text-muted ms-1"></i>';
            header.addEventListener('click', function() {
                sortTable(table, Array.from(headers).indexOf(this));
                
                // 更新排序图标
                headers.forEach(h => {
                    const icon = h.querySelector('i');
                    if (icon) {
                        icon.className = 'fas fa-sort text-muted ms-1';
                    }
                });
                
                const icon = this.querySelector('i');
                if (icon) {
                    if (this.asc) {
                        icon.className = 'fas fa-sort-up ms-1';
                    } else {
                        icon.className = 'fas fa-sort-down ms-1';
                    }
                }
            });
        }
    });
}

// 表格搜索过滤
function filterTable(table, query) {
    query = query.toLowerCase();
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
    });
}

// 表格排序
function sortTable(table, columnIndex) {
    const header = table.querySelectorAll('th')[columnIndex];
    if (!header) return;
    
    const isAsc = !header.asc;
    header.asc = isAsc;
    
    const body = table.querySelector('tbody');
    if (!body) return;
    
    const rows = Array.from(body.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const cellsA = a.querySelectorAll('td');
        const cellsB = b.querySelectorAll('td');
        
        if (columnIndex >= cellsA.length || columnIndex >= cellsB.length) return 0;
        
        const cellA = cellsA[columnIndex].textContent.trim();
        const cellB = cellsB[columnIndex].textContent.trim();
        
        // 尝试数字排序
        const numA = parseFloat(cellA);
        const numB = parseFloat(cellB);
        
        if (!isNaN(numA) && !isNaN(numB)) {
            return isAsc ? numA - numB : numB - numA;
        }
        
        // 字符串排序
        return isAsc 
            ? cellA.localeCompare(cellB, 'zh-CN') 
            : cellB.localeCompare(cellA, 'zh-CN');
    });
    
    rows.forEach(row => body.appendChild(row));
}

// 初始化提示工具
function initTooltips() {
    if (typeof bootstrap !== 'undefined' && typeof bootstrap.Tooltip !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// 图表颜色设置
const chartColors = {
    primary: '#4e73df',
    success: '#1cc88a',
    info: '#36b9cc',
    warning: '#f6c23e',
    danger: '#e74a3b',
    secondary: '#858796',
    light: '#f8f9fc',
    dark: '#5a5c69'
};

// 加载等待指示器
function showLoading(element) {
    if (!element) return;
    
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border text-primary';
    spinner.setAttribute('role', 'status');
    
    const span = document.createElement('span');
    span.className = 'visually-hidden';
    span.textContent = '加载中...';
    
    spinner.appendChild(span);
    
    const container = document.createElement('div');
    container.className = 'text-center my-4 loading-indicator';
    container.appendChild(spinner);
    
    element.innerHTML = '';
    element.appendChild(container);
}

function hideLoading(element) {
    if (!element) return;
    
    const loading = element.querySelector('.loading-indicator');
    if (loading) {
        loading.remove();
    }
}

// AJAX辅助函数
async function fetchData(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        showAlert('获取数据失败，请稍后重试。', 'danger');
        return null;
    }
}

// 显示提醒
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) {
        return;
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alert);
    
    // 5秒后自动关闭
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 5000);
}

// 绘制空状态的图表
function drawEmptyCharts() {
    if (typeof Chart === 'undefined') return;
    
    // 严重程度分布图表
    const severityChartElement = document.getElementById('severityPieChart');
    if (severityChartElement) {
        const ctx = severityChartElement.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['正常', '轻度', '中度', '重度'],
                datasets: [{
                    data: [0, 0, 0, 0],
                    backgroundColor: [
                        '#1cc88a', '#f6c23e', '#36b9cc', '#e74a3b'
                    ],
                    hoverBackgroundColor: [
                        '#169c6b', '#dda20a', '#2a9faf', '#c72a1c'
                    ],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }]
            },
            options: {
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}