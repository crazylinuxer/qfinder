
function renderStars(average = 0) {
    average = average || 0;
    const percent = (average * 100) / 5;
    
    return `
    <div class="rating">
        <div class="stars-a">
            <div class="on" style="width: ${percent}%;"></div>
                <div class="live">
                    <span data-rate="1"></span>
                    <span data-rate="2"></span>
                    <span data-rate="3"></span>
                    <span data-rate="4"></span>
                    <span data-rate="5"></span>
                </div>
            </div>
        </div>
    `;
}

const isLogged = () => {
    return Boolean(sessionStorage.getItem('user')) && Boolean(sessionStorage.getItem('access_token')) && Boolean(sessionStorage.getItem('refresh_token'));
}