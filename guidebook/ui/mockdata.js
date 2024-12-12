const testData = {
    title: "Guidebook",
    categories: [
        {
            id: "welcome",
            name: "🌟 Welcome",
            pages: [
                {
                    id: "welcome-intro",
                    label: "Introduction",
                    key: "intro",
                    categoryId: "welcome",
                    order: "1", 
                    enabled: true,
                    content: "<div style='background: rgba(0, 247, 255, 0.1); padding: 20px; border-radius: 15px;'><h2 style='color: #00f7ff; text-align: center;'>Welcome to Our Roleplay Server! 🌟</h2><p style='color: #ffffff; font-size: 16px;'>We're thrilled to have you join our immersive roleplay community. This guidebook will help you understand everything you need to know about roleplay and our server.</p><div style='margin: 20px 0; padding: 15px; background: rgba(255, 215, 0, 0.1); border-radius: 10px;'><h3 style='color: #ffd700'>Server Features ✨</h3><ul style='color: #ffffff'><li>Realistic Economy System</li><li>Custom Jobs & Businesses</li><li>Player Housing</li><li>Advanced Criminal System</li><li>Active Staff Support</li></ul></div></div>"
                }
            ]
        },
        // Add more test categories and pages as needed
    ],
    points: [
        {
            id: "spawn",
            label: "City Spawn",
            key: "spawn-point",
            textSize: 1.2,
            drawDistance: 50,
            textColor: "#00f7ff",
            font: 4,
            content: "Welcome to Los Santos! Visit the Town Hall to get started."
        },
        {
            id: "police-dept",
            label: "Police Department", 
            key: "pd-point",
            textSize: 1.2,
            drawDistance: 40,
            textColor: "#0066ff",
            font: 4,
            content: "Los Santos Police Department - Protecting & Serving"
        },
        {
            id: "hospital",
            label: "Hospital",
            key: "hospital-point", 
            textSize: 1.2,
            drawDistance: 40,
            textColor: "#ff4444",
            font: 4,
            content: "Los Santos Medical Center - Emergency Services Available"
        },
        {
            "id": "housing",
            "name": "🏠 Housing System",
            "pages": [
                {
                    "id": "housing-guide",
                    "label": "Housing Guide",
                    "key": "housing",
                    "categoryId": "housing",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: rgba(255, 215, 0, 0.1); padding: 20px; border-radius: 15px;'><h2 style='color: #ffd700'>Housing System Guide 🏡</h2><div class='housing-info'><h3 style='color: #00f7ff'>Property Types</h3><ul><li>Apartments: Affordable starter homes</li><li>Houses: Mid-tier properties</li><li>Mansions: Luxury living</li><li>Businesses: Commercial properties</li></ul></div><div class='housing-info'><h3 style='color: #00f7ff'>Property Features</h3><ul><li>Storage System</li><li>Furniture Customization</li><li>Security Systems</li><li>Garages</li></ul></div></div>"
                }
            ]
        },
        {
            "id": "rules-regulations",
            "name": "📜 Rules & Regulations",
            "pages": [
                {
                    "id": "general-rules",
                    "label": "General Rules",
                    "key": "general-rules",
                    "categoryId": "rules-regulations",
                    "order": "1",
                    "enabled": true,
                    "content": "<div class='rule-container' style='background: linear-gradient(45deg, rgba(0, 247, 255, 0.1), rgba(255, 0, 247, 0.1)); padding: 25px; border-radius: 15px; animation: fadeIn 1s ease-out;'><h2 style='color: #00f7ff; text-align: center; text-shadow: 0 0 10px rgba(0, 247, 255, 0.5);'>📋 Server Rules</h2><div class='rule-section' style='margin: 20px 0; padding: 15px; background: rgba(255, 255, 255, 0.05); border-radius: 10px; border-left: 3px solid #00f7ff; transform: translateX(0); transition: all 0.3s ease;' onmouseover='this.style.transform=\"translateX(10px)\"' onmouseout='this.style.transform=\"translateX(0)\"'><h3 style='color: #ffd700'>1. Respect & Communication 🤝</h3><p style='color: #ffffff'>- Treat all players with respect<br>- No harassment, discrimination, or hate speech<br>- Use appropriate language in all channels</p></div><div class='rule-section' style='margin: 20px 0; padding: 15px; background: rgba(255, 255, 255, 0.05); border-radius: 10px; border-left: 3px solid #ff00f7;'><h3 style='color: #ffd700'>2. Roleplay Standards 🎭</h3><p style='color: #ffffff'>- Stay in character at all times<br>- No breaking character without reason<br>- Respect others' roleplay scenarios</p></div></div>"
                },
                {
                    "id": "rp-guidelines",
                    "label": "Roleplay Guidelines",
                    "key": "rp-guidelines",
                    "categoryId": "rules-regulations",
                    "order": "2",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(135deg, rgba(0, 247, 255, 0.1), rgba(255, 0, 247, 0.1)); padding: 25px; border-radius: 15px; position: relative; overflow: hidden;'><div class='glow-overlay' style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, rgba(0, 247, 255, 0.1) 0%, transparent 70%); animation: pulse 2s infinite;'></div><h2 style='color: #00f7ff; text-align: center; margin-bottom: 30px;'>🎮 Roleplay Guidelines</h2><div class='guideline-card' style='background: rgba(10, 25, 41, 0.7); padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid #00f7ff; transition: transform 0.3s ease;' onmouseover='this.style.transform=\"scale(1.02)\"' onmouseout='this.style.transform=\"scale(1)\"'><h3 style='color: #ffd700'>Fear RP 😨</h3><p style='color: #ffffff'>React appropriately to dangerous situations. If someone has a weapon pointed at you, show fear and comply with reasonable demands.</p></div><div class='guideline-card' style='background: rgba(10, 25, 41, 0.7); padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid #ff00f7;'><h3 style='color: #ffd700'>Combat RP ⚔️</h3><p style='color: #ffffff'>No random killing. All combat must have valid RP reason and proper initiation.</p></div></div>"
                }
            ]
        },
        {
            "id": "character-creation",
            "name": "👤 Character Creation",
            "pages": [
                {
                    "id": "character-guide",
                    "label": "Character Guide",
                    "key": "char-guide",
                    "categoryId": "character-creation",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(45deg, rgba(0, 247, 255, 0.1), rgba(255, 0, 247, 0.1)); padding: 25px; border-radius: 15px; position: relative;'><div class='header-glow' style='position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 80%; height: 2px; background: #00f7ff; filter: blur(2px); animation: glow 2s infinite;'></div><h2 style='color: #00f7ff; text-align: center;'>Character Creation Guide 🎭</h2><div class='creation-step' style='margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid rgba(0, 247, 255, 0.3); transition: all 0.3s ease;' onmouseover='this.style.boxShadow=\"0 0 20px rgba(0, 247, 255, 0.2)\"' onmouseout='this.style.boxShadow=\"none\"'><h3 style='color: #ffd700'>Step 1: Appearance 👔</h3><p style='color: #ffffff'>Create a unique look that fits your character's background and personality.</p></div></div>"
                }
            ]
        },
        {
            "id": "gangs-organizations",
            "name": "🎭 Gangs & Organizations",
            "pages": [
                {
                    "id": "gang-guide",
                    "label": "Gang Guidelines",
                    "key": "gang-guide",
                    "categoryId": "gangs-organizations",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(45deg, rgba(255, 0, 0, 0.1), rgba(0, 0, 0, 0.2)); padding: 25px; border-radius: 15px; position: relative;'><div class='danger-tape' style='position: absolute; top: 10px; right: -30px; background: #ff0000; color: #ffffff; padding: 5px 40px; transform: rotate(45deg); font-size: 12px; animation: flash 2s infinite;'>RESTRICTED</div><h2 style='color: #ff0000; text-align: center;'>Gang Operations 🎭</h2><div class='gang-info' style='margin: 20px 0; padding: 20px; background: rgba(0, 0, 0, 0.5); border-radius: 10px; border-left: 3px solid #ff0000;'><h3 style='color: #ffd700'>Territory Rules</h3><p style='color: #ffffff'>Respect territory boundaries and proper war declaration procedures.</p></div></div>"
                }
            ]
        },
        {
            "id": "vehicles",
            "name": "🚗 Vehicles & Transport",
            "pages": [
                {
                    "id": "vehicle-guide",
                    "label": "Vehicle System",
                    "key": "vehicle-system",
                    "categoryId": "vehicles",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(45deg, rgba(0, 247, 255, 0.1), rgba(0, 0, 0, 0.2)); padding: 25px; border-radius: 15px; position: relative;'><h2 style='color: #00f7ff; text-align: center;'>Vehicle System 🚗</h2><div class='vehicle-info' style='margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.05); border-radius: 10px; border: 1px solid #00f7ff; transform: translateY(0); transition: all 0.3s ease;' onmouseover='this.style.transform=\"translateY(-5px)\"' onmouseout='this.style.transform=\"translateY(0)\"'><h3 style='color: #ffd700'>Vehicle Classes</h3><p style='color: #ffffff'>Browse our extensive collection of vehicles across different categories.</p><ul style='color: #ffffff'><li>Economy Class: $5,000 - $25,000</li><li>Sports Class: $25,000 - $100,000</li><li>Luxury Class: $100,000+</li></ul></div></div>"
                }
            ]
        },
        {
            "id": "properties",
            "name": "🏠 Properties & Real Estate",
            "pages": [
                {
                    "id": "property-guide",
                    "label": "Property Guide",
                    "key": "property-guide",
                    "categoryId": "properties",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(45deg, rgba(255, 215, 0, 0.1), rgba(0, 0, 0, 0.2)); padding: 25px; border-radius: 15px; position: relative;'><div class='luxury-corner' style='position: absolute; top: -5px; right: -5px; width: 100px; height: 100px; background: linear-gradient(45deg, transparent 50%, rgba(255, 215, 0, 0.1) 50%);'></div><h2 style='color: #ffd700; text-align: center;'>Property Guide 🏠</h2><div class='property-card' style='margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.05); border-radius: 10px; border: 1px solid #ffd700; transition: all 0.3s ease;' onmouseover='this.style.boxShadow=\"0 0 20px rgba(255, 215, 0, 0.2)\"' onmouseout='this.style.boxShadow=\"none\"'><h3 style='color: #00f7ff'>Available Properties</h3><p style='color: #ffffff'>From modest apartments to luxury mansions, find your perfect home!</p></div></div>"
                }
            ]
        },
        {
            "id": "server-info",
            "name": "ℹ️ Server Information",
            "pages": [
                {
                    "id": "server-features",
                    "label": "Features & Systems",
                    "key": "features",
                    "categoryId": "server-info",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(45deg, rgba(0, 247, 255, 0.1), rgba(0, 0, 0, 0.3)); padding: 25px; border-radius: 15px; position: relative; overflow: hidden;'><div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, rgba(0, 247, 255, 0.2) 0%, transparent 70%); animation: pulse 3s infinite;'></div><h2 style='color: #00f7ff; text-align: center; text-shadow: 0 0 10px rgba(0, 247, 255, 0.5);'>Server Features 🌟</h2><div class='feature-grid' style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;'><div class='feature-card' style='background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 10px; border: 1px solid #00f7ff; transform: translateY(0); transition: all 0.3s ease;' onmouseover='this.style.transform=\"translateY(-5px)\"; this.style.boxShadow=\"0 10px 20px rgba(0, 247, 255, 0.2)\"' onmouseout='this.style.transform=\"translateY(0)\"; this.style.boxShadow=\"none\"'><h3 style='color: #ffd700'>Custom Phone System 📱</h3><p style='color: #ffffff'>Advanced mobile experience with apps, messaging, and more!</p></div><div class='feature-card' style='background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 10px; border: 1px solid #00f7ff;'><h3 style='color: #ffd700'>Dynamic Weather 🌦️</h3><p style='color: #ffffff'>Real-time weather system affecting gameplay and visuals</p></div></div></div>"
                }
            ]
        },
        {
            "id": "advanced-mechanics",
            "name": "🔧 Advanced Mechanics",
            "pages": [
                {
                    "id": "combat-system",
                    "label": "Combat System",
                    "key": "combat",
                    "categoryId": "advanced-mechanics",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(0, 0, 0, 0.3)); padding: 25px; border-radius: 15px; position: relative;'><div style='position: absolute; top: -10px; right: -10px; background: #ff0000; color: white; padding: 5px 15px; transform: rotate(15deg); font-size: 12px; animation: flash 2s infinite;'>COMBAT ZONE</div><h2 style='color: #ff0000; text-align: center; margin-bottom: 30px;'>Combat System ⚔️</h2><div class='combat-info' style='background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 10px; border: 1px solid #ff0000; margin: 15px 0; transition: all 0.3s ease;' onmouseover='this.style.transform=\"scale(1.02)\"' onmouseout='this.style.transform=\"scale(1)\"'><h3 style='color: #ffd700'>Damage System</h3><p style='color: #ffffff'>Realistic damage zones with location-based injuries</p></div></div>"
                }
            ]
        },
        {
            "id": "social-features",
            "name": "🤝 Social Features",
            "pages": [
                {
                    "id": "social-guide",
                    "label": "Social Systems",
                    "key": "social-systems",
                    "categoryId": "social-features",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(45deg, rgba(0, 247, 255, 0.1), rgba(255, 192, 203, 0.1)); padding: 25px; border-radius: 15px; position: relative;'><div class='pulse-overlay' style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at center, rgba(255, 182, 193, 0.1) 0%, transparent 70%); animation: pulse 2s infinite alternate;'></div><h2 style='color: #ff69b4; text-align: center;'>Social Features 🤝</h2><div class='social-card' style='margin: 20px 0; padding: 20px; background: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid #ff69b4; transition: all 0.3s ease;' onmouseover='this.style.transform=\"translateY(-5px)\"' onmouseout='this.style.transform=\"translateY(0)\"'><h3 style='color: #ffd700'>Phone System 📱</h3><p style='color: #ffffff'>Connect with other players, send messages, make calls, and more!</p></div></div>"
                }
            ]
        },
        {
            "id": "custom-items",
            "name": "🎒 Custom Items",
            "pages": [
                {
                    "id": "items-guide",
                    "label": "Items Guide",
                    "key": "items",
                    "categoryId": "custom-items",
                    "order": "1",
                    "enabled": true,
                    "content": "<div style='background: linear-gradient(45deg, rgba(255, 215, 0, 0.1), rgba(0, 0, 0, 0.2)); padding: 25px; border-radius: 15px; position: relative;'><div class='sparkle' style='position: absolute; top: 10px; right: 10px; width: 20px; height: 20px; background: #ffd700; clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%); animation: spin 3s linear infinite;'></div><h2 style='color: #ffd700; text-align: center;'>Custom Items 🎒</h2><div class='item-grid' style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px;'><div class='item-card' style='background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid #ffd700; transition: all 0.3s ease;' onmouseover='this.style.transform=\"scale(1.05)\"' onmouseout='this.style.transform=\"scale(1)\"'><h3 style='color: #00f7ff'>Special Items</h3><p style='color: #ffffff'>Discover unique items with special abilities!</p></div></div></div>"
                }
            ]
        }
    ]
};

// Mock responses for browser development
const mockResponses = {
    "welcome-intro": {
        label: "Introduction",
        content: testData.categories[0].pages[0].content
    },
    "rp-rules": {
        label: "Roleplay Rules",
        content: testData.categories[1].pages[0].content
    },
    "legal-jobs": {
        label: "Legal Careers",
        content: testData.categories[2].pages[0].content
    }
    // Add more mock responses for other pages as needed
};

// Make available for browser testing
window.testData = testData;
window.mockResponses = mockResponses;
