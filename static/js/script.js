document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navUl = document.querySelector('nav ul');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navUl.classList.toggle('show');
        });
    }
    
    // Chatbot functionality
    const chatbotIcon = document.querySelector('.chatbot-icon');
    const chatbotContainer = document.querySelector('.chatbot-container');
    const closeChat = document.querySelector('.close-chat');
    const userMessageInput = document.getElementById('user-message');
    const sendMessageButton = document.getElementById('send-message');
    const chatbotMessages = document.querySelector('.chatbot-messages');
    
    if (chatbotIcon && chatbotContainer) {
        chatbotIcon.addEventListener('click', function() {
            chatbotContainer.style.display = 'flex';
            chatbotIcon.style.display = 'none';
        });
    }
    
    if (closeChat) {
        closeChat.addEventListener('click', function() {
            chatbotContainer.style.display = 'none';
            chatbotIcon.style.display = 'flex';
        });
    }
    
    // Send message functionality
    if (sendMessageButton && userMessageInput) {
        const sendMessage = function() {
            const message = userMessageInput.value.trim();
            if (message !== '') {
                // Add user message to chat
                const userMessageDiv = document.createElement('div');
                userMessageDiv.classList.add('message', 'user-message');
                userMessageDiv.textContent = message;
                chatbotMessages.appendChild(userMessageDiv);
                
                // Clear input
                userMessageInput.value = '';
                
                // Scroll to bottom of chat
                chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
                
                // Get bot response via AJAX
                fetch('/chatbot', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                })
                .then(response => response.json())
                .then(data => {
                    // Add bot response to chat
                    const botMessageDiv = document.createElement('div');
                    botMessageDiv.classList.add('message', 'bot-message');
                    botMessageDiv.textContent = data.response;
                    chatbotMessages.appendChild(botMessageDiv);
                    
                    // Scroll to bottom of chat
                    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        };
        
        sendMessageButton.addEventListener('click', sendMessage);
        
        userMessageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    // AI Recommendation form submission
    const recommendationForm = document.getElementById('recommendation-form');
    const resultsContainer = document.getElementById('recommendation-results');
    
    if (recommendationForm) {
        recommendationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(recommendationForm);
            
            fetch('/get_recommendation', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                
                // Add AI explanation
                const explanationDiv = document.createElement('div');
                explanationDiv.classList.add('ai-explanation');
                explanationDiv.innerHTML = `
                    <h3><i class="fas fa-robot"></i> AI Recommendation Explanation</h3>
                    <p>${data.explanation}</p>
                `;
                resultsContainer.appendChild(explanationDiv);
                
                // Add car recommendations
                const recommendationsDiv = document.createElement('div');
                recommendationsDiv.classList.add('car-grid');
                
                data.recommendations.forEach(recommendation => {
                    const car = recommendation.car;
                    const matchScore = recommendation.match_score;
                    
                    const carCard = document.createElement('div');
                    carCard.classList.add('car-card');
                    carCard.innerHTML = `
                        <img src="${car.image}" alt="${car.name}" class="car-image">
                        <div class="car-content">
                            <div class="car-title">
                                <h3>${car.name}</h3>
                                <div class="car-price">$${car.price_per_day}/day</div>
                            </div>
                            <span class="car-category">${car.category}</span>
                            <div class="car-features">
                                <span><i class="fas fa-user"></i> ${car.seats} seats</span>
                                <span><i class="fas fa-cog"></i> ${car.transmission}</span>
                            </div>
                            <div class="car-rating">
                                <i class="fas fa-star"></i>
                                <span>${car.rating}/5</span>
                            </div>
                            <span class="match-score">${matchScore}% match</span>
                            <div style="margin-top: 15px;">
                                <button class="btn">Book Now</button>
                            </div>
                        </div>
                    `;
                    recommendationsDiv.appendChild(carCard);
                });
                
                resultsContainer.appendChild(recommendationsDiv);
                
                // Scroll to results
                resultsContainer.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
    
    // Smart pricing date selection
    const dateSelector = document.getElementById('date-selector');
    const priceTables = document.querySelectorAll('.price-table tbody');
    
    if (dateSelector && priceTables.length > 0) {
        dateSelector.addEventListener('change', function() {
            const selectedDate = this.value;
            
            // Update UI to highlight selected date
            document.querySelectorAll('.price-table tr').forEach(row => {
                row.classList.remove('selected-date');
                if (row.dataset.date === selectedDate) {
                    row.classList.add('selected-date');
                }
            });
        });
    }
    
    // Virtual tour controls
    const angleButtons = document.querySelectorAll('.angle-button');
    const tourVideo = document.getElementById('tour-video');
    
    if (angleButtons.length > 0 && tourVideo) {
        angleButtons.forEach(button => {
            button.addEventListener('click', function() {
                const angle = this.dataset.angle;
                // In a real implementation, this would change the video source or 3D view
                // For now, just update the UI
                document.getElementById('current-angle').textContent = angle;
                
                // Remove active class from all buttons
                angleButtons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');
            });
        });
    }
    
    // Search functionality highlight
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('q');
    
    if (searchQuery) {
        // Highlight search results
        const contentElements = document.querySelectorAll('.car-title h3, .car-features span, .car-category');
        contentElements.forEach(element => {
            const content = element.textContent;
            if (content.toLowerCase().includes(searchQuery.toLowerCase())) {
                const regex = new RegExp(searchQuery, 'gi');
                element.innerHTML = content.replace(regex, match => `<mark>${match}</mark>`);
            }
        });
    }
    
    // Initialize charts for Smart Pricing page if Chart.js is loaded
    if (typeof Chart !== 'undefined' && document.getElementById('price-trends-chart')) {
        const ctx = document.getElementById('price-trends-chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['May 1', 'May 2', 'May 3', 'May 4', 'May 5', 'May 6', 'May 7', 'May 8', 'May 9', 'May 10', 'May 11', 'May 12', 'May 13', 'May 14'],
                datasets: [{
                    label: 'Economy Cars',
                    data: [65, 70, 75, 90, 95, 110, 115, 90, 85, 80, 85, 90, 95, 100],
                    borderColor: '#4a6bff',
                    tension: 0.4,
                    fill: false
                },
                {
                    label: 'Luxury Cars',
                    data: [200, 210, 220, 250, 270, 300, 310, 290, 280, 270, 280, 290, 310, 330],
                    borderColor: '#00d4c8',
                    tension: 0.4,
                    fill: false
                },
                {
                    label: 'SUVs',
                    data: [150, 160, 170, 190, 210, 230, 240, 220, 200, 190, 195, 210, 220, 230],
                    borderColor: '#ff6b6b',
                    tension: 0.4,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'AI-Predicted Price Trends (May 2025)'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Price (USD)'
                        }
                    }
                }
            }
        });
    }
    
    // Maintenance prediction charts
    document.querySelectorAll('.reliability-meter .fill').forEach(element => {
        const score = parseInt(element.dataset.score || 0);
        element.style.width = `${score}%`;
    });
});