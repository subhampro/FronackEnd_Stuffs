let currentTheme = 'default';
let isAdmin = false;

// Initialize the application
window.addEventListener('message', function(event) {
    const data = event.data;
    
    if (data.type === 'openGuidebook') {
        showGuidebook(data.pageId);
    }
    
    if (data.type === 'setPermissions') {
        isAdmin = data.isAdmin;
        updateUIForPermissions();
    }
});

// UI Functions
function showGuidebook(pageId) {
    $('#guidebook-container').show();
    if (pageId) {
        loadPage(pageId);
    }
}

function loadPage(pageId) {
    $.post('https://guidebook/getPage', JSON.stringify({
        pageId: pageId
    }), function(response) {
        $('#page-content').html(response.content);
    });
}

// Search functionality
$('#search').on('input', function() {
    const searchTerm = $(this).val().toLowerCase();
    searchContent(searchTerm);
});

// WYSIWYG Editor
function initEditor() {
    const editor = new FroalaEditor('#wysiwyg-editor', {
        toolbarButtons: ['bold', 'italic', 'underline', 'insertImage', 'insertLink', 'insertVideo'],
        imageUploadURL: 'https://yourserver.com/upload',
        videoUpload: true
    });
}

// Admin Panel Functions
function createCategory(data) {
    $.post('https://guidebook/createCategory', JSON.stringify(data));
}

function createPage(data) {
    $.post('https://guidebook/createPage', JSON.stringify(data));
}

function createHelpPoint(data) {
    $.post('https://guidebook/createHelpPoint', JSON.stringify(data));
}

// Search Implementation
function searchContent(term) {
    $('.searchable').each(function() {
        const content = $(this).text().toLowerCase();
        $(this).toggle(content.includes(term));
    });
}

// Theme Management
function applyTheme(themeName) {
    const theme = themes[themeName] || themes.default;
    Object.entries(theme).forEach(([key, value]) => {
        document.documentElement.style.setProperty(`--${key}`, value);
    });
}

// Website Embedding
function embedWebsite(url) {
    const embed = document.createElement('iframe');
    embed.src = url;
    embed.className = 'embedded-website';
    document.getElementById('page-content').appendChild(embed);
}

// Enhanced Search with Categories
function enhancedSearch(term) {
    const results = [];
    $('.searchable').each(function() {
        const element = $(this);
        const content = element.text().toLowerCase();
        const category = element.data('category');
        const score = content.split(term).length - 1;
        
        if (score > 0) {
            results.push({ element, score, category });
        }
    });
    
    results.sort((a, b) => b.score - a.score);
    displaySearchResults(results);
}

function displaySearchResults(results) {
    const container = $('#search-results');
    container.empty();
    
    results.forEach(result => {
        const element = result.element.clone();
        element.addClass('search-result');
        container.append(element);
    });
}

// Admin Panel Tab Management
$('.tab-btn').on('click', function() {
    const tabId = $(this).data('tab');
    $('.tab-btn').removeClass('active');
    $(this).addClass('active');
    $('.tab-content').addClass('hidden');
    $(`#${tabId}-tab`).removeClass('hidden');
});

// Category Management
$('#new-category').on('click', function() {
    const name = prompt('Category name:');
    if (name) {
        createCategory({ name });
    }
});

// List Management Functions
function refreshLists() {
    $.post('https://guidebook/getCategories', {}, updateCategoriesList);
    $.post('https://guidebook/getPages', {}, updatePagesList);
    $.post('https://guidebook/getHelpPoints', {}, updateHelpPointsList);
}

// Theme Management
$('#new-theme').on('click', function() {
    const customTheme = {
        name: prompt('Theme name:'),
        primary: $('#primary-color').val(),
        secondary: $('#secondary-color').val(),
        accent: $('#accent-color').val(),
        text: $('#text-color').val()
    };
    saveTheme(customTheme);
});

// Initialize Admin Panel
function initAdminPanel() {
    if (isAdmin) {
        refreshLists();
        initializeThemeSelector();
        $('#admin-panel').removeClass('hidden');
    }
}

// Update help point management
function updateHelpPointsList(points) {
    const container = $('#help-points-list');
    container.empty();
    
    points.forEach(point => {
        const element = $(`
            <div class="list-item" data-id="${point.id}">
                <span>${point.name}</span>
                <div class="action-buttons">
                    <button onclick="editHelpPoint(${point.id})">Edit</button>
                    <button onclick="deleteHelpPoint(${point.id})">Delete</button>
                </div>
            </div>
        `);
        container.append(element);
    });
}

function editHelpPoint(id) {
    const point = helpPoints.find(p => p.id === id);
    if (!point) return;
    
    const newData = {
        id: point.id,
        name: prompt('Point name:', point.name),
        blip_sprite: parseInt(prompt('Blip sprite:', point.blip_sprite)),
        blip_color: parseInt(prompt('Blip color:', point.blip_color))
    };
    
    if (newData.name && !isNaN(newData.blip_sprite) && !isNaN(newData.blip_color)) {
        $.post('https://guidebook/editHelpPoint', JSON.stringify(newData));
    }
}

// Debug logging
function debugLog(level, message) {
    if (Config.Debug.level >= level) {
        console.log(`[Guidebook] ${message}`);
    }
}

// More UI functions...